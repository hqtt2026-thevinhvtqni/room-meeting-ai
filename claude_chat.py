# claude_chat.py - Chat với não Claude thật, tay vẫn là VSCodeAgent + FileOpsAgent
import os
import anthropic
from core.vscode_agent import VSCodeAgent
from core.file_ops_agent import FileOpsAgent
from core.secretary import Secretary
from core.identity import verify_identity_claim

# Identity của anh - đổi thành "xu" "claude" nếu muốn test quyền
IDENTITY = "vinh"
vscode_agent = VSCodeAgent(IDENTITY)
file_agent = FileOpsAgent(IDENTITY)
secretary = Secretary()

# FIX-3: BUILD phase chưa cần circuit breaker phức tạp — chỉ cần giới hạn
# nhỏ + dừng ngay khi gặp DENY, không để model tự thử path khác.
MAX_TOOL_TURNS = 3


def _is_deny(result: str) -> bool:
    return "DENY" in (result or "").upper()

# Định nghĩa bộ công cụ cho Claude dùng
TOOLS = [
    {
        "name": "create_and_open",
        "description": "Tạo file mới với nội dung và mở trong VSCode. Không được ghi đè file đã tồn tại.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Đường dẫn file, vd: research/RC007/README.md"},
                "content": {"type": "string", "description": "Nội dung file"}
            },
            "required": ["path", "content"]
        }
    },
    {
        "name": "open_file",
        "description": "Mở file có sẵn trong VSCode",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"]
        }
    },
    {
        "name": "create_folder",
        "description": "Tạo thư mục và mở trong VSCode",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"]
        }
    },
    {
        "name": "read_file",
        "description": "Đọc nội dung file để trả lời",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"]
        }
    },
    {
        "name": "list_dir",
        "description": "Liệt kê file trong thư mục",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"]
        }
    },
    {
        "name": "delete_file",
        "description": "Xóa file",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"]
        }
    }
]

def execute_tool(name, inp):
    try:
        if name == "create_and_open":
            return vscode_agent.create_and_open(inp["path"], inp.get("content",""))
        if name == "open_file":
            return vscode_agent.open_file(inp["path"])
        if name == "create_folder":
            file_agent.create_folder(inp["path"])
            vscode_agent.open_folder(inp["path"])
            return f"Đã tạo và mở thư mục {inp['path']}"
        if name == "read_file":
            return file_agent.read_file(inp["path"])
        if name == "list_dir":
            return str(file_agent.list_dir(inp["path"]))
        if name == "delete_file":
            file_agent.delete_file(inp["path"])
            return f"Đã xóa {inp['path']}"
    except Exception as e:
        return f"LỖI/GOVERNANCE DENY: {e}"

# --- MAIN CHAT ---
def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("⛔ Chưa có API Key. Làm như sau:")
        print("1. Vào https://console.anthropic.com/ -> tạo API Key")
        print("2. Trong PowerShell gõ: $env:ANTHROPIC_API_KEY='sk-ant-...'")
        print("3. Rồi chạy lại py claude_chat.py")
        return

    client = anthropic.Anthropic(api_key=api_key)
    print(f"=== CLAUDE CHAT AGENT | Identity: {IDENTITY} ===")
    print("Gõ tự nhiên: 'Tạo cho anh folder RC007 và viết README giới thiệu dự án'")
    print("Gõ 'thoat' để thoát")
    print("-"*60)

    messages = []
    while True:
        user_text = input("\n> Anh Vinh: ")
        if user_text.lower() in ["thoat", "exit", "quit"]:
            break

        # FIX-1: Secretary ghi nguyen van truoc, doc lap, khong dien giai.
        secretary.receive("vinh", user_text)

        # FIX-4: canh bao neu co claim identity khac RUNTIME_IDENTITY,
        # khong cap them quyen gi ca.
        identity_warning = verify_identity_claim(IDENTITY, user_text)
        if identity_warning:
            print(f"⚠ {identity_warning}")

        messages.append({"role": "user", "content": user_text})

        # Gọi Claude
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            system=f"""Bạn là Room Hop Agent. Bạn điều khiển VSCode và file system qua các tool đã cho.
Identity hiện tại là {IDENTITY}. Mọi thao tác đều bị Governance kiểm tra, nếu bị DENY hãy báo lại cho user.
Bạn phải luôn dùng tool để thao tác file, không được bịa.
Luôn trả lời tiếng Việt.""",
            tools=TOOLS,
            messages=messages
        )

        # Xử lý tool use loop — FIX-3: dừng ngay khi có DENY, và giới hạn
        # tối đa MAX_TOOL_TURNS vòng trong 1 câu hỏi để Agent không "đánh
        # nhau" với Governance bằng cách tự thử path khác liên tục.
        turns = 0
        denied = False
        while response.stop_reason == "tool_use" and turns < MAX_TOOL_TURNS:
            turns += 1
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"[Claude đang gọi] {block.name}({block.input})")
                    result = execute_tool(block.name, block.input)
                    print(f"[Kết quả] {result[:200]}")
                    if _is_deny(result):
                        denied = True
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})

            if denied:
                print("⛔ Governance DENY — dừng chuỗi hành động hiện tại, trả về user.")
                break
            if turns >= MAX_TOOL_TURNS:
                print(f"⛔ Đã đạt giới hạn {MAX_TOOL_TURNS} lượt gọi tool — dừng lại, trả về user.")
                break

            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                system=f"Bạn là Room Hop Agent. Identity {IDENTITY}.",
                tools=TOOLS,
                messages=messages
            )

        if response.stop_reason == "tool_use":
            # Bị dừng vì DENY hoặc hết lượt — ép Claude trả lời bằng text,
            # KHÔNG cho gọi thêm tool nào nữa (bỏ tools= khỏi lệnh gọi này).
            messages.append({
                "role": "user",
                "content": "(Hệ thống: đã dừng chuỗi hành động do bị Governance DENY hoặc hết lượt cho phép. "
                            "Hãy trả lời bằng text, không gọi thêm tool nào.)"
            })
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                system=f"Bạn là Room Hop Agent. Identity {IDENTITY}.",
                messages=messages
            )

        # Trả lời cuối
        final_text = "".join([b.text for b in response.content if hasattr(b, 'text')])
        print(f"\nClaude: {final_text}")
        messages.append({"role": "assistant", "content": final_text})

if __name__ == "__main__":
    main()