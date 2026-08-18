"""
core/gemini_intent_router.py — ROOM HOP

Bộ định tuyến ý định (intent router) dùng Gemini (Google, có free tier)
làm lớp dự phòng THỨ 2 trong chuỗi failover, đứng giữa Llama (Groq, free,
ưu tiên #1) và Claude (Anthropic, trả phí, ưu tiên cuối cùng).

Cùng interface với core/intent_router.IntentRouter và
core/llama_intent_router.LlamaIntentRouter (available, route()) nên
chat.py chỉ cần thêm vào danh sách thử, không cần đổi logic dispatch.

AN TOÀN — giống hệt nguyên tắc của 2 router kia:
- Dùng tool-calling GỐC của Gemini, chỉ khai báo 5 tool tương ứng 5 action
  file-ops đã có (tao_file, mo_file, tao_thu_muc, doc_file, xoa_file).
  Không có tool nào khác.
- Router CHỈ trả về {action, params} nằm trong ALLOWED_ACTIONS — không tự
  thực thi gì. Việc THỰC THI thật vẫn do FileOpsAgent/VSCodeAgent đảm
  nhiệm (chat.py gọi qua _dispatch()), vẫn qua đúng GOV/governance.py
  hiện có, không đổi gì ở tầng đó.
- Nếu Gemini không gọi tool nào (chỉ trả lời chữ) -> coi là "tro_chuyen",
  KHÔNG suy diễn thành hành động file.
- Nếu KHÔNG có GEMINI_API_KEY/GOOGLE_API_KEY trong môi trường, hoặc gọi
  API lỗi (mạng, key sai, hết quota free tier...), router raise
  IntentRouterError rõ ràng — chat.py sẽ tự thử router kế tiếp trong
  chuỗi, không bao giờ crash vì thiếu key hay hết quota.

KHÔNG hardcode API key trong file này — chỉ đọc từ biến môi trường
GEMINI_API_KEY hoặc GOOGLE_API_KEY (đúng cách gemini_chat.py đang làm).
"""

from __future__ import annotations

import os

from core.intent_router import ALLOWED_ACTIONS, IntentRouterError

# Model alias hoạt động cho key mới (giống gemini_chat.py) - tự fallback
# sang các model khác nếu bị 404/chặn.
PRIMARY_MODEL = "gemini-flash-latest"
FALLBACK_MODELS = ["gemini-2.5-flash-lite", "gemini-2.5-flash", "gemini-2.0-flash-lite", "gemini-1.5-flash"]

SYSTEM_PROMPT = """Ban la Room Hop Agent, tro ly ky thuat cho Vinh - nguoi
dieu hanh du an ROOM HOP. Khi Vinh yeu cau tao/mo/doc/xoa file hoac tao
thu muc, LUON dung tool tuong ung. Neu khong ro la lenh file (chao hoi,
hoi dap, giao vai tro, thao luan y tuong...), KHONG goi tool nao ca, chi
tra loi tu nhien bang tieng Viet, ngan gon, nhu mot tro ly thong minh.
KHONG BAO GIO tra loi "khong hieu" - luon phan hoi hop ly."""


def _build_tools():
    """Khai bao tool bang schema cua google-genai (types.Tool/FunctionDeclaration)."""
    from google.genai import types

    def decl(name, description, path_desc, needs_content=False):
        props = {"path": types.Schema(type="STRING", description=path_desc)}
        required = ["path"]
        if needs_content:
            props["content"] = types.Schema(type="STRING", description="Noi dung file")
        return types.FunctionDeclaration(
            name=name,
            description=description,
            parameters=types.Schema(type="OBJECT", properties=props, required=required),
        )

    declarations = [
        decl("tao_file", "Tao file moi voi noi dung. Khong ghi de file da ton tai.",
             "Duong dan file, vd: docs/test.md", needs_content=True),
        decl("mo_file", "Mo 1 file co san trong VSCode.", "Duong dan file"),
        decl("tao_thu_muc", "Tao 1 thu muc moi va mo trong VSCode.", "Duong dan thu muc"),
        decl("doc_file", "Doc noi dung 1 file co san.", "Duong dan file"),
        decl("xoa_file", "Xoa 1 file.", "Duong dan file"),
    ]
    return [types.Tool(function_declarations=declarations)]


class GeminiIntentRouter:
    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        self.model = model or os.environ.get("ROOM_HOP_GEMINI_MODEL", PRIMARY_MODEL)
        self._client = None  # lazy init, chi tao khi that su goi route()

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    def _get_client(self):
        if self._client is None:
            try:
                from google import genai
            except ImportError as e:
                raise IntentRouterError(
                    "Chua cai package 'google-genai'. Chay: pip install google-genai"
                ) from e
            self._client = genai.Client(api_key=self.api_key)
        return self._client

    def route(self, text: str, history: list[str] | None = None) -> dict:
        """
        Tra ve {"action": <str trong ALLOWED_ACTIONS>, "params": {...}}.
        Raise IntentRouterError neu chua co key, thieu package, goi API loi
        (bao gom het quota free tier), hoac Gemini tra ve du lieu khong hop le.
        """
        if not self.available:
            raise IntentRouterError(
                "Chua co GEMINI_API_KEY/GOOGLE_API_KEY trong moi truong. "
                "Set bien moi truong roi chay lai de bat router nay."
            )

        from google.genai import types

        client = self._get_client()
        history = history or []
        convo = "\n".join(history[-6:])
        user_msg = f"{convo}\nVinh: {text}" if convo else f"Vinh: {text}"

        contents = [types.Content(role="user", parts=[types.Part(text=user_msg)])]
        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=_build_tools(),
        )

        models_to_try = [self.model] + [m for m in FALLBACK_MODELS if m != self.model]
        last_err = None
        response = None
        for m in models_to_try:
            try:
                response = client.models.generate_content(model=m, contents=contents, config=config)
                break
            except Exception as e:
                last_err = e
                # 404/NOT_FOUND -> model nay khong dung duoc voi key, thu model ke tiep.
                # Cac loi khac (het quota, mang, key sai...) cung fail-fast ve chat.py.
                if "404" in str(e) or "NOT_FOUND" in str(e):
                    continue
                raise IntentRouterError(f"Loi goi Gemini API: {e}") from e

        if response is None:
            raise IntentRouterError(f"Loi goi Gemini API (het model de thu): {last_err}")

        try:
            parts = response.candidates[0].content.parts
        except (AttributeError, IndexError, TypeError) as e:
            raise IntentRouterError(f"Gemini tra ve du lieu khong hop le: {e}") from e

        function_calls = [p.function_call for p in parts if getattr(p, "function_call", None)]

        if not function_calls:
            reply = "".join(p.text for p in parts if getattr(p, "text", None)).strip()
            return {"action": "tro_chuyen", "params": {"reply": reply or "..."}}

        fc = function_calls[0]
        action = fc.name
        params = dict(fc.args) if fc.args else {}
        if action not in ALLOWED_ACTIONS:
            # An toan: neu Gemini "sang tao" tool la ngoai whitelist (khong nen
            # xay ra vi chi khai bao 5 tool o tren), ep ve tro_chuyen.
            return {"action": "tro_chuyen", "params": {"reply": str(params)}}
        return {"action": action, "params": params}
