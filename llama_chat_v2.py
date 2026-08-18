# llama_chat_v2.py - Llama + Governance V2 + Mission
from core.groq_config import get_groq_client
from core.vscode_agent import VSCodeAgent
from core.file_ops_agent import FileOpsAgent
from core.governance import MissionContext
from core.secretary import Secretary
from core.identity import verify_identity_claim
import json

IDENTITY = "agent_llama" # Agent chay duoi identity nay, khong phai vinh

# Mission mac dinh: chi duoc research, khong duoc xoa
CURRENT_MISSION = MissionContext(
    name="research_rc007",
    allow_delete=False, # Mac dinh KHONG cho xoa
    allowed_scopes=["research/*", "docs/*", "tmp/*"]
)

vscode_agent = VSCodeAgent(IDENTITY)
file_agent = FileOpsAgent(IDENTITY, mission=CURRENT_MISSION)
client = get_groq_client()

# FIX-1: Secretary — chi ghi nguyen van, khong bao gio duoc goi de quyet
# dinh hanh dong. Secretary KHONG thay the IntentRouter/Llama tool-calling
# o tren — no chi la 1 duong ghi log song song, doc lap.
secretary = Secretary()

TOOLS = [
    {"type": "function", "function": {"name": "create_and_open", "description": "Tao file moi", "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}}},
    {"type": "function", "function": {"name": "edit_file", "description": "Sua file da co", "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}}},
    {"type": "function", "function": {"name": "create_folder", "description": "Tao folder", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
    {"type": "function", "function": {"name": "delete_file", "description": "Xoa file (se Soft-Delete vao trash)", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
]

def execute_tool(name, args):
    try:
        if name == "create_and_open":
            result = file_agent.create_file(args["path"], args.get("content",""))
            vscode_agent.open_file(args["path"])
            return result
        if name == "edit_file":
            result = file_agent.edit_file(args["path"], args["content"])
            vscode_agent.open_file(args["path"])
            return result
        if name == "create_folder":
            return file_agent.create_folder(args["path"])
        if name == "delete_file":
            return file_agent.delete_file(args["path"])
    except Exception as e:
        return f"⛔ GOVERNANCE DENY: {e}"

print(f"=== LLAMA V2 + GOVERNANCE | Identity: {IDENTITY} | Mission: {CURRENT_MISSION.name} | AllowDelete={CURRENT_MISSION.allow_delete} ===")
print("Test thu:")
print("1. 'Tao folder research/RC007 va viet README' -> CREATE ✅")
print("2. 'Cap nhat file research/RC007/README.md' -> EDIT ✅")
print("3. 'Xoa toan bo meetings/' -> DENY ❌")
print("4. 'Xoa file research/RC007/README.md' -> DENY vi Mission chua cho phep DELETE")
print("-"*70)

messages = [{"role": "system", "content": f"Ban la Agent identity {IDENTITY}, Mission {CURRENT_MISSION.name}. Ban phai dung tools. Tra loi tieng Viet."}]

while True:
    user_text = input("\n> Anh Vinh: ")
    if user_text.lower() in ["thoat","exit"]:
        break
    if user_text.startswith("/mission delete"):
        # FIX-2: khong con mutate CURRENT_MISSION tu conversation nua.
        # Mission authority KHONG duoc thay doi tu chat, bat ke ai go lenh.
        print('⛔ REJECT: Mission authority cannot be changed from conversation.')
        continue

    # FIX-1: Secretary luon ghi nguyen van truoc, doc lap voi viec Llama co
    # goi tool hay khong. Secretary khong dien giai, khong quyet dinh gi ca.
    secretary.receive("vinh", user_text)

    # FIX-4: phat hien claim identity khac RUNTIME_IDENTITY (vd Agent tu
    # xung la Xu). Chi ghi log UNVERIFIED, KHONG cap them quyen gi ca —
    # IDENTITY dung de GOV.check() van la "agent_llama" nhu cu.
    identity_warning = verify_identity_claim(IDENTITY, user_text, CURRENT_MISSION)
    if identity_warning:
        print(f"⚠ {identity_warning}")

    messages.append({"role": "user", "content": user_text})
    try:
        response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=messages, tools=TOOLS, tool_choice="auto", temperature=0.2)
        msg = response.choices[0].message
        if msg.tool_calls:
            messages.append(msg)
            for tool_call in msg.tool_calls:
                func_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                print(f"[Llama goi] {func_name} {args}")
                result = execute_tool(func_name, args)
                print(f"[Governance] {result}")
                messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})
            final_resp = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=messages, temperature=0.2)
            print(f"\nLlama: {final_resp.choices[0].message.content}")
            messages.append({"role": "assistant", "content": final_resp.choices[0].message.content})
        else:
            print(f"\nLlama: {msg.content}")
            messages.append({"role": "assistant", "content": msg.content})
    except Exception as e:
        print(f"Loi: {e}")