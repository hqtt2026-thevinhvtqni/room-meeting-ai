"""
core/llama_intent_router.py — ROOM HOP

Bộ định tuyến ý định (intent router) dùng Llama 3.3 70B qua Groq API
(MIỄN PHÍ, có rate-limit) thay vì Claude (Anthropic, tính phí). Dùng
tool-calling GỐC của Groq — đáng tin cậy hơn nhiều so với bắt model tự
viết JSON tay (cách IntentRouter/Claude ở core/intent_router.py làm),
vì Groq tự đảm bảo tham số đúng schema.

Cùng interface với core/intent_router.IntentRouter (available, route())
nên chat.py chỉ cần đổi import, không cần đổi logic dispatch/fallback.

AN TOÀN — giống hệt nguyên tắc của IntentRouter (Claude):
- CHỈ 5 tool tương ứng 5 action file-ops đã có (tao_file, mo_file,
  tao_thu_muc, doc_file, xoa_file) được khai báo cho Llama gọi. Không có
  tool nào khác (không có "run_shell", "delete_folder_recursive"...).
- Việc THỰC THI vẫn do FileOpsAgent/VSCodeAgent đảm nhiệm (chat.py gọi
  qua _dispatch()), tức vẫn qua đúng GOV/governance.py hiện có — Llama
  chỉ đề xuất hành động, không tự làm gì trên đĩa.
- Nếu Llama không gọi tool nào (chỉ trả lời chữ) -> coi là "tro_chuyen",
  KHÔNG suy diễn thành hành động file.

KHÔNG hardcode API key trong file này — chỉ đọc từ biến môi trường
GROQ_API_KEY. Anh Vinh set biến này trên máy (PowerShell):
    $env:GROQ_API_KEY="gsk_..."
(Lấy tại console.groq.com — miễn phí, có giới hạn request/phút.)
"""

from __future__ import annotations

import json
import os
import time

from core.intent_router import ALLOWED_ACTIONS, IntentRouterError
from core.usage_ledger import extract_usage, new_usage_event, record_usage_event, sha256_text

DEFAULT_MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """Ban la Room Hop Agent, tro ly ky thuat cho Vinh - nguoi
dieu hanh du an ROOM HOP. Khi Vinh yeu cau tao/mo/doc/xoa file hoac tao
thu muc, LUON dung tool tuong ung. Neu khong ro la lenh file (chao hoi,
hoi dap, giao vai tro, thao luan y tuong...), KHONG goi tool nao ca, chi
tra loi tu nhien bang tieng Viet, ngan gon, nhu mot tro ly thong minh.
KHONG BAO GIO tra loi "khong hieu" - luon phan hoi hop ly."""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "tao_file",
            "description": "Tao file moi voi noi dung. Khong ghi de file da ton tai.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Duong dan file, vd: docs/test.md"},
                    "content": {"type": "string", "description": "Noi dung file"},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "mo_file",
            "description": "Mo 1 file co san trong VSCode.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "tao_thu_muc",
            "description": "Tao 1 thu muc moi va mo trong VSCode.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "doc_file",
            "description": "Doc noi dung 1 file co san.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "xoa_file",
            "description": "Xoa 1 file.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
        },
    },
]


class LlamaIntentRouter:
    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        self.model = model or os.environ.get("ROOM_HOP_LLAMA_MODEL", DEFAULT_MODEL)
        self._client = None  # lazy init, chỉ tạo khi thật sự gọi route()

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    def _get_client(self):
        if self._client is None:
            try:
                from groq import Groq
            except ImportError as e:
                raise IntentRouterError(
                    "Chua cai package 'groq'. Chay: pip install groq"
                ) from e
            self._client = Groq(api_key=self.api_key)
        return self._client

    def route(self, text: str, history: list[str] | None = None) -> dict:
        """
        Trả về {"action": <str trong ALLOWED_ACTIONS>, "params": {...}}.
        Raise IntentRouterError nếu chưa có key, gọi API lỗi, hoặc phản
        hồi không parse được.
        """
        if not self.available:
            raise IntentRouterError(
                "Chua co GROQ_API_KEY trong moi truong. "
                "Set bien moi truong GROQ_API_KEY=gsk_... (mien phi tai console.groq.com) roi chay lai."
            )

        client = self._get_client()
        started = time.monotonic()
        usage_event = new_usage_event(
            provider="groq", model=self.model, ai_id="llama_intent_router",
            ai_role="intent_router", caller="intent_router",
        )
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for line in (history or [])[-6:]:
            # history đang lưu dạng "Vinh: ..." / "Agent: ..." (string đơn giản
            # từ chat.py) — quy về role user/assistant cho đúng chuẩn chat API.
            if line.startswith("Vinh:"):
                messages.append({"role": "user", "content": line[len("Vinh:"):].strip()})
            elif line.startswith("Agent:"):
                messages.append({"role": "assistant", "content": line[len("Agent:"):].strip()})
        messages.append({"role": "user", "content": text})

        try:
            resp = client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
                temperature=0.2,
            )
        except Exception as e:
            usage_event.update(status="error", error_class=type(e).__name__,
                               latency_ms=round((time.monotonic() - started) * 1000))
            record_usage_event(usage_event)
            raise IntentRouterError(f"Loi goi Groq API: {e}") from e

        msg = resp.choices[0].message
        groq_usage = getattr(getattr(resp, "x_groq", None), "usage", None) or getattr(resp, "usage", None)
        usage_event.update(extract_usage("groq", groq_usage))
        usage_event["provider_request_id"] = getattr(resp, "id", None)
        usage_event["latency_ms"] = round((time.monotonic() - started) * 1000)
        usage_event["content_hash"] = sha256_text(getattr(msg, "content", None))
        record_usage_event(usage_event)

        if not msg.tool_calls:
            # Llama không gọi tool nào -> coi là hội thoại tự do.
            return {"action": "tro_chuyen", "params": {"reply": msg.content or "..."}}

        # ChatBot (chat.py) chỉ xử lý 1 hành động mỗi lượt -> lấy tool_call đầu tiên.
        call = msg.tool_calls[0]
        action = call.function.name
        try:
            params = json.loads(call.function.arguments)
        except json.JSONDecodeError as e:
            raise IntentRouterError(f"Llama tra ve tham so khong hop le: {call.function.arguments!r} ({e})") from e

        if action not in ALLOWED_ACTIONS:
            # An toàn: tool lạ ngoài whitelist (không nên xảy ra vì TOOLS chỉ
            # khai báo 5 cái) -> ép về tro_chuyen thay vì thực thi mù.
            return {"action": "tro_chuyen", "params": {"reply": f"(tool la '{action}', bo qua)"}}
        return {"action": action, "params": params}
