# gemini_chat.py - Bản não Gemini FREE, tay VSCodeAgent + Governance (FIXED 2026-08)
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from core.vscode_agent import VSCodeAgent
from core.file_ops_agent import FileOpsAgent
from core.secretary import Secretary
from core.identity import verify_identity_claim

load_dotenv()

IDENTITY = "vinh"
vscode_agent = VSCodeAgent(IDENTITY)
file_agent = FileOpsAgent(IDENTITY)
secretary = Secretary()

MAX_TOOL_TURNS = 3
# Model alias hoạt động cho key mới tạo T8/2026 - tự fallback nếu bị chặn
PRIMARY_MODEL = "gemini-flash-latest"
FALLBACK_MODELS = ["gemini-2.5-flash-lite", "gemini-2.5-flash", "gemini-2.0-flash-lite", "gemini-1.5-flash"]

def _is_deny(result: str) -> bool:
    return "DENY" in (result or "").upper()

# --- Tools ---
def create_and_open(path: str, content: str = ""):
    try:
        return vscode_agent.create_and_open(path, content)
    except Exception as e:
        return f"LOI/DENY: {e}"

def open_file(path: str):
    try:
        return vscode_agent.open_file(path)
    except Exception as e:
        return f"LOI/DENY: {e}"

def create_folder(path: str):
    try:
        file_agent.create_folder(path)
        vscode_agent.open_folder(path)
        return f"Da tao va mo thu muc {path}"
    except Exception as e:
        return f"LOI/DENY: {e}"

def read_file(path: str):
    try:
        return file_agent.read_file(path)[:5000]
    except Exception as e:
        return f"LOI/DENY: {e}"

def list_dir(path: str):
    try:
        return str(file_agent.list_dir(path))
    except Exception as e:
        return f"LOI/DENY: {e}"

def delete_file(path: str):
    try:
        file_agent.delete_file(path)
        return f"Da xoa {path}"
    except Exception as e:
        return f"LOI/DENY: {e}"

tools = [create_and_open, open_file, create_folder, read_file, list_dir, delete_file]
TOOL_MAP = {f.__name__: f for f in tools}

def call_with_fallback(client, contents, config):
    """Thử model chính, nếu 404 thì tự thử fallback - đúng tinh thần Gate"""
    models_to_try = [PRIMARY_MODEL] + FALLBACK_MODELS
    last_err = None
    for m in models_to_try:
        try:
            # cập nhật config model cho lần thử này
            resp = client.models.generate_content(
                model=m,
                contents=contents,
                config=config,
            )
            if m != PRIMARY_MODEL:
                print(f"ℹ Model {PRIMARY_MODEL} bị chặn, đang dùng fallback: {m}")
            return resp, m
        except Exception as e:
            if "404" in str(e) or "NOT_FOUND" in str(e):
                last_err = e
                continue
            else:
                raise e
    raise last_err

def main():
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("⛔ Chưa có GEMINI_API_KEY trong .env")
        return

    client = genai.Client(api_key=api_key)

    system_instruction = f"""Bạn là Room Hop Agent, identity hiện tại là {IDENTITY}.
Bạn điều khiển file và VSCode qua các tool.
- Luôn dùng tool khi user yêu cầu tạo/mở/đọc/xóa file
- Mọi thao tác đều bị Governance kiểm tra, nếu bị DENY hãy giải thích bằng tiếng Việt
- Trả lời tiếng Việt, ngắn gọn
"""

    print(f"=== GEMINI 2.5 CHAT AGENT (FIXED 2026) | Identity: {IDENTITY} | Model: {PRIMARY_MODEL} ===")
    print("Go tu nhien: 'Tao cho anh folder RC007 va viet README'")
    print("-"*60)

    contents = []
    base_config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        tools=tools,
    )
    plain_config = types.GenerateContentConfig(
        system_instruction=system_instruction,
    )

    while True:
        user_text = input("\n> Anh Vinh: ")
        if user_text.lower() in ["thoat", "exit", "quit"]:
            break

        secretary.receive("vinh", user_text)
        identity_warning = verify_identity_claim(IDENTITY, user_text)
        if identity_warning:
            print(f"⚠ {identity_warning}")

        contents.append(types.Content(role="user", parts=[types.Part(text=user_text)]))

        try:
            turns = 0
            while turns < MAX_TOOL_TURNS:
                response, used_model = call_with_fallback(client, contents, base_config)
                contents.append(response.candidates[0].content)

                parts = response.candidates[0].content.parts
                function_calls = [p.function_call for p in parts if p.function_call]

                if not function_calls:
                    text = "".join([p.text for p in parts if p.text]) if parts else ""
                    print(f"\nGemini ({used_model}): {text}")
                    break

                turns += 1
                denied = False
                tool_response_parts = []

                for fc in function_calls:
                    name = fc.name
                    args = dict(fc.args) if fc.args else {}
                    print(f"[Gemini goi] {name}({args})")
                    func = TOOL_MAP.get(name)
                    result = func(**args) if func else f"LOI: khong biet tool {name}"
                    print(f"[Ket qua] {result}")
                    if _is_deny(str(result)):
                        denied = True
                    tool_response_parts.append(
                        types.Part.from_function_response(name=name, response={"result": str(result)})
                    )

                contents.append(types.Content(role="tool", parts=tool_response_parts))

                if denied:
                    print("⛔ Governance DENY — dừng chuỗi hành động hiện tại.")
                    final_resp, _ = call_with_fallback(client, contents, plain_config)
                    final_text = "".join([p.text for p in final_resp.candidates[0].content.parts if p.text])
                    print(f"\nGemini: {final_text}")
                    contents.append(final_resp.candidates[0].content)
                    break

            if turns >= MAX_TOOL_TURNS:
                print(f"⛔ Đã đạt giới hạn {MAX_TOOL_TURNS} lượt gọi tool.")

        except Exception as e:
            print(f"⛔ Lỗi Gemini: {e}")
            # Gợi ý debug nhanh
            if "404" in str(e):
                print("-> Gợi ý: chạy list_models.py để xem key này được phép dùng model nào.")

if __name__ == "__main__":
    main()
