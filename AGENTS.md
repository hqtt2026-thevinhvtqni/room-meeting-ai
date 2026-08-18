## IMPORTANT DISTINCTION

Document precedence MUST NOT be interpreted as authority precedence.

- Document precedence: AGENTS.md > PROJECT_STATE.md > XU_CORE.md ... nghĩa là khi 2 tài liệu mâu thuẫn về state/context, cái nào được ưu tiên đọc.
- Authority hierarchy: VINH > XU > AGENT nghĩa là ai có quyền quyết định.

AGENTS.md is a Governance Contract. It is not an authority actor.

# ROOM HOP v0.2 — Agent Constitution
# Nguồn quyền lực: VINH > XU > AGENT
# QUẢN GIA tạm thời OUTSIDE authority chain thử nghiệm

## 01. IDENTITY & HIERARCHY (Quan trọng nhất)

**Kiến trúc quyền lực:**

## 05.1 CONTEXT CONTRACT - Thứ tự đọc bắt buộc

Agent vào ROOM HOP phải đọc theo thứ tự này, file trên thắng file dưới:

1. AGENTS.md - SYSTEM RULES (Constitution - cao nhất)
2. PROJECT_STATE.md - VERIFIED PROJECT STATE (Truth mới nhất)
3. XU_CORE.md - IDENTITY / AUTHORITY
4. XU_SESSION.md - CURRENT WORKING STATE (RAM)
5. meetings/{latest}/ - HISTORICAL EVIDENCE (chỉ để tham khảo, không được biến thành state)
6. XU_MEMORY.md - LONG-TERM MEMORY (thấp nhất)

> RULE: Meeting log là evidence, không phải state. Nếu meeting nói PENDING nhưng PROJECT_STATE.md nói PASS thì lấy PROJECT_STATE.md.
> Đây là Temporal Context Reasoning.

## Core Protection Rule

- Agent TUYỆT ĐỐI KHÔNG được tự ý chỉnh sửa XU_CORE.md, XU_MEMORY.md nếu không có CORE_EDIT_AUTH.
- Nếu task yêu cầu sửa XU_CORE.md:
    1. Không thực thi ngay
    2. Báo cáo về XU: "Task yêu cầu Core Edit, cần CORE_EDIT_AUTH từ VINH"
    3. Chờ XU xác thực XU_CORE_EDIT_KEY từ VINH
    4. Chỉ thực thi khi XU xác nhận AUTH = PASSED