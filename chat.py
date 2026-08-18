from core.vscode_agent import VSCodeAgent
from core.file_ops_agent import FileOpsAgent
from core.intent_router import IntentRouter, IntentRouterError
from core.llama_intent_router import LlamaIntentRouter
from core.gemini_intent_router import GeminiIntentRouter
from core.secretary import Secretary
from core.identity import verify_identity_claim
import re


class ChatBot:
    def __init__(self, identity="vinh"):
        # FIX-5: identity nay la CONVERSATION PRINCIPAL — dung de FileOpsAgent
        # (Action Request) check quyen qua Governance. Secretary o duoi KHONG
        # dung identity nay — no khong can quyen gi ca vi khong tao Action.
        self.identity = identity
        self.agent = VSCodeAgent(identity)
        self.file_agent = FileOpsAgent(identity)

        # FIX-1: Secretary tach rieng khoi Conversation Principal. Chi ghi
        # nguyen van, khong bao gio duoc goi IntentRouter hay quyet dinh gi.
        self.secretary = Secretary()

        # FAILOVER CHAIN — chỉ 1 router "thắng" tại mỗi lượt handle(), không
        # bao giờ 2 router cùng ra lệnh 1 lúc (tránh xung đột action).
        # Thứ tự thử: Llama (Groq, free) -> Gemini (Google, free tier) ->
        # Claude (Anthropic, tra phi, dung sau cung de tiet kiem quota) ->
        # regex co ban (khong bao gio het "quota", luon co san).
        # Router nao khong co key (available=False) thi bi bo qua ngay,
        # khong tinh vao chuoi thu (khong tao delay/goi API thua).
        candidates = [
            (LlamaIntentRouter(), "LLAMA (Groq, mien phi)"),
            (GeminiIntentRouter(), "GEMINI (Google, free tier)"),
            (IntentRouter(), "CLAUDE (Anthropic, tinh phi)"),
        ]
        self.routers = [(r, name) for r, name in candidates if r.available]

        self.history: list[str] = []

        print(f"=== ROOM HOP CHAT AGENT | Identity: {identity} ===")
        if self.routers:
            chain = " -> ".join(name for _, name in self.routers)
            print(f"Che do: THONG MINH (chuoi failover): {chain} -> regex co ban")
        else:
            print("Che do: CO BAN (regex) - chua co GROQ_API_KEY / GEMINI_API_KEY / ANTHROPIC_API_KEY.")
            print("De bat che do thong minh (mien phi): set GROQ_API_KEY=gsk_... (console.groq.com) roi chay lai.")
        print("Chi can go lenh, khong can go '> Anh Vinh:'")
        print("-" * 50)

    def clean_input(self, text: str):
        text = text.replace("> Anh Vinh:", "").replace("Anh Vinh:", "").replace(">", "").replace("Agent:", "").strip()
        return text

    # -- thực thi hành động đã được xác định (dù từ router AI hay regex) --
    # Việc thực thi LUÔN đi qua self.agent / self.file_agent, tức là vẫn
    # qua đúng cơ chế phân quyền (GOV) hiện có trên máy - không đổi.
    def _dispatch(self, action: str, params: dict) -> str:
        if action == "tao_file":
            path = params.get("path")
            content = params.get("content") or f"# {path}"
            return self.agent.create_and_open(path, content)
        if action == "mo_file":
            return self.agent.open_file(params.get("path"))
        if action == "tao_thu_muc":
            path = params.get("path")
            self.file_agent.create_folder(path)
            self.agent.open_folder(path)
            return f"Da tao va mo thu muc: {path}"
        if action == "doc_file":
            content = self.file_agent.read_file(params.get("path"))
            return f"\n--- {params.get('path')} ---\n{content[:3000]}"
        if action == "xoa_file":
            path = params.get("path")
            self.file_agent.delete_file(path)
            return f"Da xoa: {path}"
        if action == "tro_chuyen":
            return params.get("reply", "...")
        return "Minh chua hieu. Thu go: tao file docs/test.md noi dung hello"

    # -- chế độ cơ bản (regex cứng), dùng khi chưa có ANTHROPIC_API_KEY --
    # hoặc khi gọi router AI bị lỗi (mạng, key sai...), để ChatBot không
    # bao giờ bị đứng im hoàn toàn.
    def _handle_legacy_regex(self, t: str) -> str:
        low = t.lower()

        if "tao file" in low or "tạo file" in low:
            m = re.search(r"t[aạ]o file\s+([^\s]+)(?:\s+(?:noi dung|nội dung)\s+(.*))?", t, re.IGNORECASE)
            if m:
                path = m.group(1)
                content = m.group(2) or f"# {path}"
                return self.agent.create_and_open(path, content)

        if "mo file" in low or "mở file" in low:
            m = re.search(r"m[oở] file\s+([^\s]+)", t, re.IGNORECASE)
            if m:
                return self.agent.open_file(m.group(1))

        if "tao thu muc" in low or "tạo thư mục" in low or "tao folder" in low:
            m = re.search(r"t[aạ]o (?:thu muc|thư mục|folder)\s+([^\s]+)", t, re.IGNORECASE)
            if m:
                path = m.group(1)
                self.file_agent.create_folder(path)
                self.agent.open_folder(path)
                return f"Da tao va mo thu muc: {path}"

        if "doc file" in low or "đọc file" in low or "xem file" in low:
            m = re.search(r"(?:doc|đọc|xem) file\s+([^\s]+)", t, re.IGNORECASE)
            if m:
                content = self.file_agent.read_file(m.group(1))
                return f"\n--- {m.group(1)} ---\n{content[:3000]}"

        if "xoa file" in low or "xóa file" in low:
            m = re.search(r"x[oó]a file\s+([^\s]+)", t, re.IGNORECASE)
            if m:
                self.file_agent.delete_file(m.group(1))
                return f"Da xoa: {m.group(1)}"

        return "Minh chua hieu. Thu go: tao file docs/test.md noi dung hello"

    def handle(self, text: str):
        t = self.clean_input(text)

        # FIX-1: Secretary luon ghi nguyen van TRUOC, doc lap voi routing/
        # dispatch ben duoi. Secretary khong dien giai, khong quyet dinh.
        self.secretary.receive(self.identity, t)

        # FIX-4: canh bao neu co claim identity khac CONVERSATION PRINCIPAL
        # hien tai. Chi ghi log UNVERIFIED, khong cap them quyen gi ca.
        identity_warning = verify_identity_claim(self.identity, t)

        try:
            result = None
            errors = []
            # Thu lan luot tung router trong chuoi failover. Dung ngay khi
            # 1 router tra ve ket qua hop le - khong bao gio 2 router cung
            # ra lenh trong cung 1 luot handle().
            for router, name in self.routers:
                try:
                    parsed = router.route(t, self.history)
                    result = self._dispatch(parsed.get("action"), parsed.get("params", {}))
                    self.history.append(f"Vinh: {t}")
                    self.history.append(f"Agent: {result}")
                    break
                except IntentRouterError as e:
                    # Router nay loi (het quota, mang, key sai...) -> ghi lai
                    # va thu router ke tiep trong chuoi, khong crash ChatBot.
                    errors.append(f"{name}: {e}")
                    continue

            if result is None:
                # Ca chuoi failover deu loi (hoac khong co router nao co san)
                # -> roi ve che do regex co ban, ChatBot khong bao gio dung im.
                fallback = self._handle_legacy_regex(t)
                if errors:
                    detail = "; ".join(errors)
                    result = f"{fallback}\n(⚠ Ca chuoi router AI deu loi, dung che do co ban: {detail})"
                else:
                    result = fallback
        except Exception as e:
            result = f"⛔ {e}"

        if identity_warning:
            result = f"{result}\n⚠ {identity_warning}"
        return result


if __name__ == "__main__":
    bot = ChatBot("vinh")
    while True:
        try:
            user_input = input("\n> Anh Vinh: ")
            if user_input.lower() in ["thoat", "exit", "quit"]:
                break
            if not user_input.strip():
                continue
            result = bot.handle(user_input)
            print(f"Agent: {result}")
        except KeyboardInterrupt:
            break
