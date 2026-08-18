"""
core/intent_router.py — ROOM HOP

Dùng Claude thật (Anthropic API) để hiểu ý định tự do của Vinh khi gõ
trong ChatBot (chat.py), thay vì chỉ đoán bằng regex cứng.

AN TOÀN:
- Router CHỈ được trả về 1 action nằm trong ALLOWED_ACTIONS (whitelist).
  Nó không tự thực thi gì cả — việc thực thi thật (tạo/sửa/xóa file) vẫn
  do FileOpsAgent/VSCodeAgent đảm nhiệm y như trước, tức là vẫn đi qua
  đúng cơ chế phân quyền (GOV / governance.py) hiện có trên máy anh,
  không đổi gì ở tầng đó.
- Nếu KHÔNG có ANTHROPIC_API_KEY trong môi trường, hoặc gọi API lỗi
  (mạng, key sai, hết quota...), router báo `available=False` / raise
  lỗi rõ ràng — ChatBot (chat.py) sẽ tự rơi về chế độ regex cũ, không
  bao giờ crash vì thiếu key.
"""

from __future__ import annotations

import json
import os
import re

import requests

API_URL = "https://api.anthropic.com/v1/messages"
DEFAULT_MODEL = "claude-sonnet-4-5-20250929"

ALLOWED_ACTIONS = {
    "tao_file",      # params: path, content
    "mo_file",       # params: path
    "tao_thu_muc",   # params: path
    "doc_file",      # params: path
    "xoa_file",      # params: path
    "tro_chuyen",    # params: reply  (Claude tự trả lời tự do, KHÔNG đụng file)
}

SYSTEM_PROMPT = """Ban la bo dieu huong y dinh (intent router) cho ROOM HOP ChatBot,
mot tro ly ky thuat cho Vinh - nguoi dung dieu hanh du an ROOM HOP.

Nhiem vu: doc cau tieng Viet (co the khong dau) cua Vinh, tra ve DUY NHAT
1 doi tuong JSON (khong markdown, khong giai thich them) theo dung schema:

{"action": "<mot trong: tao_file, mo_file, tao_thu_muc, doc_file, xoa_file, tro_chuyen>",
 "params": {...}}

Quy tac chon action:
- tao_file: khi Vinh muon tao file moi. params: {"path": "...", "content": "..."}
- mo_file: khi Vinh muon mo 1 file co san. params: {"path": "..."}
- tao_thu_muc: khi Vinh muon tao folder moi. params: {"path": "..."}
- doc_file / xoa_file: tuong tu, params co "path".
- tro_chuyen: MOI truong hop khac (chao hoi, hoi dap, giao vai tro, thao
  luan y tuong, khong ro la lenh file) -> tra loi tu nhien, thong minh,
  dung vai tro tro ly ky thuat cua ROOM HOP. params: {"reply": "<cau tra
  loi bang tieng Viet>"}.

Vi du:
"tao file docs/test.md noi dung hello"
-> {"action":"tao_file","params":{"path":"docs/test.md","content":"hello"}}

"ban la thu ky cua phong, tu gio ghi lai moi cuoc trao doi"
-> {"action":"tro_chuyen","params":{"reply":"Da hieu, tu gio minh se dong vai thu ky va ho tro ghi lai noi dung trao doi trong phong. Anh cu tiep tuc."}}

"chu de: HQTT company"
-> {"action":"tro_chuyen","params":{"reply":"Da nhan chu de: HQTT company. Anh muon minh chuan bi hay ghi chu gi cho chu de nay khong?"}}

QUAN TRONG: KHONG BAO GIO tra loi "khong hieu" - neu khong chac la lenh
file thi luon dung tro_chuyen va phan hoi hop ly, tu nhien nhu mot tro ly
thong minh that su. CHI tra ve JSON, khong them chu nao khac, khong dung
markdown code fence."""


class IntentRouterError(Exception):
    """Lỗi khi gọi API hoặc parse kết quả — ChatBot nên bắt lỗi này và fallback."""


class IntentRouter:
    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.model = model or os.environ.get("ROOM_HOP_INTENT_MODEL", DEFAULT_MODEL)

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    def route(self, text: str, history: list[str] | None = None) -> dict:
        """
        Trả về {"action": <str trong ALLOWED_ACTIONS>, "params": {...}}.
        Raise IntentRouterError nếu chưa có key, gọi API lỗi, hoặc Claude
        trả về JSON không hợp lệ.
        """
        if not self.available:
            raise IntentRouterError(
                "Chua co ANTHROPIC_API_KEY trong moi truong. "
                "Set bien moi truong ANTHROPIC_API_KEY=sk-ant-... roi chay lai de bat che do thong minh."
            )

        history = history or []
        convo = "\n".join(history[-6:])
        user_msg = f"{convo}\nVinh: {text}" if convo else f"Vinh: {text}"

        try:
            resp = requests.post(
                API_URL,
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": self.model,
                    "max_tokens": 500,
                    "system": SYSTEM_PROMPT,
                    "messages": [{"role": "user", "content": user_msg}],
                },
                timeout=30,
            )
            resp.raise_for_status()
        except requests.RequestException as e:
            raise IntentRouterError(f"Loi goi Anthropic API: {e}") from e

        data = resp.json()
        raw = "".join(
            block.get("text", "")
            for block in data.get("content", [])
            if block.get("type") == "text"
        ).strip()

        # Claude đôi khi vẫn bọc ```json ... ``` dù đã dặn không làm vậy — dọn cho chắc.
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw).strip()

        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError as e:
            raise IntentRouterError(f"Claude tra ve JSON khong hop le: {raw!r} ({e})") from e

        action = parsed.get("action")
        params = parsed.get("params", {})
        if action not in ALLOWED_ACTIONS:
            # An toàn: nếu action lạ (Claude "sáng tạo" ngoài whitelist),
            # ép về tro_chuyen thay vì thực thi hành động không xác định.
            return {"action": "tro_chuyen", "params": {"reply": raw}}
        return {"action": action, "params": params}
