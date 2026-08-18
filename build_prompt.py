import os
import sys
import pyperclip
from pathspec import PathSpec
from datetime import datetime

# 1. Các file cốt lõi bắt buộc
CORE_FILE = "context/XU_CORE.md"
MEMORY_FILE = "context/XU_MEMORY.md"
SESSION_FILE = "context/XU_SESSION.md"
PROJECT_STATE_FILE = "context/PROJECT_STATE.md"
IGNORE_FILE = ".xuignore"

def read_file_content(filepath):
    """Đọc nội dung file an toàn, trả về chuỗi rỗng nếu không tìm thấy."""
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception as e:
            print(f"⚠ Không thể đọc file {filepath}: {e}")
    return ""

def load_ignore_spec():
    """Tải quy tắc ignore từ file .xuignore."""
    if os.path.exists(IGNORE_FILE):
        with open(IGNORE_FILE, "r", encoding="utf-8") as f:
            patterns = f.read().splitlines()
        return PathSpec.from_lines("gitwildmatch", patterns)
    return PathSpec.from_lines("gitwildmatch", [])

def build_workspace_prompt(target_doc_path=None, task_description=""):
    """Gom tất cả ngữ cảnh thành 1 Prompt hoàn chỉnh."""
    spec = load_ignore_spec()
    
    # Đọc Core, Memory, Session, State
    core_content = read_file_content(CORE_FILE)
    memory_content = read_file_content(MEMORY_FILE)
    session_content = read_file_content(SESSION_FILE)
    project_state_content = read_file_content(PROJECT_STATE_FILE)

    # --- LOG ĐỂ XU TRÊN PC BIẾT AGENT ĐÃ SỬA GÌ ---
    log_path = "log.jsonl"
    thoi_gian = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a", encoding="utf-8") as log:
        log.write(f'{thoi_gian} | BUILD_PROMPT | SESSION_len={len(session_content)} | STATE_len={len(project_state_content)}\n')
    # --- HẾT LOG ---
    
    # Đọc Tài liệu mục tiêu
    target_content = ""
    if target_doc_path:
        if spec.match_file(target_doc_path):
            print(f"❌ Cảnh báo: File '{target_doc_path}' nằm trong danh sách .xuignore!")
            return None
        target_content = read_file_content(target_doc_path)
        if not target_content:
            print(f"❌ Cảnh báo: File '{target_doc_path}' rỗng hoặc không tồn tại!")

    # Đóng gói Prompt theo chuẩn Room Hop Multi-AI
    prompt = f"""# ==========================================
# CONTEXT 1: XU CORE (Bản sắc & Nguyên tắc)
# ==========================================
{core_content if core_content else "[Chưa có XU_CORE.md]"}

# ==========================================
# CONTEXT 2: XU MEMORY (Tri thức & Ký ức)
# ==========================================
{memory_content if memory_content else "[Chưa có XU_MEMORY.md]"}

# ==========================================
# CONTEXT 2.5: XU SESSION (Phiên hiện tại - Agent được sửa)
# ==========================================
{session_content if session_content else "[Chưa có XU_SESSION.md]"}

# ==========================================
# CONTEXT 2.6: PROJECT STATE (Trạng thái dự án)
# ==========================================
{project_state_content if project_state_content else "[Chưa có PROJECT_STATE.md]"}

# ==========================================
# CONTEXT 3: TÀI LIỆU CẦN XỬ LÝ ({target_doc_path if target_doc_path else 'N/A'})
# ==========================================
{target_content if target_content else "[Không đính kèm tài liệu]"}

# ==========================================
# NHIỆM VỤ (TASK) & MÔ HÌNH ROOM HOP
# ==========================================
Yêu cầu: Hãy kích hoạt mô hình **Room Hop** phân tích tài liệu/yêu cầu trên dưới 3 góc nhìn AI độc lập:
1. **Xu (Lead Synthesizer):** Định hướng logic, tổng hợp & chốt giải pháp.
2. **Claude/Technical Angle:** Soi chi tiết cấu trúc, logic lập luận, tính tối ưu.
3. **Risk-AI/Devil's Advocate:** Tìm điểm gãy, rủi ro, lỗi logic hoặc điểm yếu.

Nhiệm vụ cụ thể:
{task_description if task_description else "Phân tích và cho ý kiến chi tiết về tài liệu trên."}

Sau khi phân tích xong, hãy trích xuất các **Decisions** (Quyết định) và **Lessons** (Bài học) chuẩn format Markdown để chuẩn bị merge vào XU_MEMORY.md.
"""
    return prompt

if __name__ == "__main__":
    print("🚀 === XU WORKSPACE PROMPT BUNDLER ===")
    target_file = input("📄 Nhập đường dẫn file tài liệu cần xử lý (hoặc bấm Enter để bỏ qua): ").strip()
    task = input("📝 Nhập yêu cầu/nhiệm vụ cần thực hiện: ").strip()
    final_prompt = build_workspace_prompt(
        target_doc_path=target_file if target_file else None, 
        task_description=task
    )
    if final_prompt:
        pyperclip.copy(final_prompt)
        print("\n" + "="*50)
        print("✅ ĐÃ COPY PROMPT VÀO CLIPBOARD THÀNH CÔNG!")
        print("👉 Bây giờ bạn chỉ cần sang Web (Gemini / Claude / ChatGPT) và bấm 'Ctrl + V' để dán.")
        print("="*50)