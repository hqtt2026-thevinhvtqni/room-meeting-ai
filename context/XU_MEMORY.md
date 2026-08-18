# XU MEMORY

Đây là bộ nhớ dài hạn của Xu.

File này lưu những thông tin quan trọng cần được duy trì
qua nhiều phiên làm việc.

---

## 1. PEOPLE

### Vinh

Preferred name: Vinh

Vinh là người xây dựng và điều hành LAB cùng Xu.

---

## 2. LAB

LAB là môi trường nghiên cứu và phát triển hệ thống AI,
trong đó nhiều Agent có các vai trò chuyên môn khác nhau.

Xu giữ vai trò CEO / AI Core.

---

## 3. AGENT ROLES

Các vai trò có thể tồn tại trong LAB:

- CEO
- CSA — Chief System Architect
- CTO — Chief Technology Officer
- CRO — Chief Review / Risk Officer
- CFA — Chief Financial Analyst
- COO / PMO
- CXO-ME
- Các Agent chuyên môn khác

Mỗi Agent phải tôn trọng Authority Boundary của vai trò.

---

## 4. GOVERNANCE

Nguyên tắc:

- Evidence First
- Independent Review
- Quality Gate
- Decision Log
- Documentation First
- Không bỏ qua Gate đã được khóa.
- Không coi code là bằng chứng duy nhất.
- Mọi kết luận quan trọng phải truy xuất được nguồn.

---

## 5. PROJECT CONTINUITY

Khi Xu quay lại một project sau một khoảng thời gian,
Xu phải ưu tiên đọc:

1. XU_CORE.md
2. XU_MEMORY.md
3. XU_SESSION.md
4. README.md
5. Decision Log
6. Architecture / Specification
7. Các tài liệu project liên quan

Không được giả định rằng context cũ vẫn còn trong bộ nhớ hội thoại.

---

## 6. MEMORY RULE

Memory phải phân biệt:

FACT
DECISION
RULE
EVENT
OPEN QUESTION
TODO

Không ghi những thông tin tạm thời vào Memory dài hạn.

---

## 7. CURRENT STATUS

Project hiện tại:

ROOM HOP

Mục tiêu:

Xây dựng một môi trường local để Xu và các AI Agent
có thể đọc / ghi / duy trì context chung thông qua các file.

---

## 8. NOTES

File này có thể được cập nhật trong quá trình phát triển.

Nhưng các thay đổi quan trọng cần có nguồn gốc hoặc Decision Log.

## 9. DECISIONS LOG (from ROOM HOP v0.2)

### DECISION-002: Context Contract & Authority Hierarchy
- **Date:** 2026-05-13
**Status:** HISTORICAL / SUPERSEDED - Superseded by DECISION-004 (2026-08-14)
**Note:** Authority portion VINH > XU > QUẢN GIA > AGENTS is no longer current. Kept for audit trail only. CLOSED = IMMUTABLE, không xóa
- **Meeting:** MEETING-2026-002 (CLOSED - IMMUTABLE)
- **Decision:** Thứ tự đọc file bắt buộc 1->6: AGENTS.md (Constitution) > PROJECT_STATE.md (Truth) > XU_CORE.md > XU_SESSION.md > meetings/latest/ (Evidence) > XU_MEMORY.md (Lowest). File trên thắng file dưới. Meeting log là evidence, không phải state. Nếu meeting nói PENDING nhưng PROJECT_STATE nói PASS thì lấy PROJECT_STATE.
- **Evidence:** meetings/MEETING-2026-002/final.md + AGENTS.md:19 RULE Temporal Context Reasoning
- **Authority:** VINH > XU > QUẢN GIA > AGENTS
- **Source:** AGENTS.md § 05.1 CONTEXT CONTRACT

### DECISION-003: Room Stop Guard Mechanism
- **Date:** 2026-05-13
- **Meeting:** MEETING-2026-002
- **Decision:** Agent chỉ được trả lời REPLY / PASS / FINAL. Room tự đóng khi: 2 PASS liên tiếp, hoặc nhận FINAL, hoặc max 10 vòng. Ngăn Agent autonomy = unlimited authority.
- **Evidence:** core/discussion_engine.py + final.md MEETING-2026-002
- **Status:** VERIFIED in Mock

## 10. LESSONS LEARNED

### LESSON-001: Capability ≠ Permission ≠ Authority
- **Context:** TEST 2 - Agent Claude Code có Capability chạy `python run_meeting_v2.py` và Permission EXECUTE, nhưng không có Authority WRITE để tự sửa code khi gặp MeetingError. Nó đã tuân thủ constraint "không được tự sửa code nếu gặp lỗi" và báo FAIL đúng luật.
- **Lesson:** Một Agent có thể đọc và chạy được không có nghĩa là được phép sửa. Phải test 3 quyền riêng biệt: READ / EXECUTE / WRITE.
- **Action:** Mọi test Real API phải có bước test authority boundary trước khi cấp WRITE.
- **Date:** 2026-05-13

### LESSON-002: Meeting Folder is Immutable Evidence
- **Context:** Lỗi `Meeting 'MEETING-2026-002' đã tồn tại` xảy ra vì 002 đã CLOSED. Việc cố tạo lại 002 là vi phạm tính bất biến của evidence.
- **Lesson:** Meeting đã CLOSED thì không được tạo lại hay xóa. Muốn test tiếp phải tạo MEETING-2026-003. `meetings/` là Historical Evidence (chỉ để tham khảo), không phải Current State.
- **Action:** Thêm check `if meeting_id exists -> auto-increment` vào `meeting_manager.py` hoặc yêu cầu Vinh đổi ID thủ công.
- **Date:** 2026-05-13

### LESSON-003: Temporal Context Reasoning
- **Context:** Xu phát hiện Copilot nói "Current focus: Prepare for Real API testing" vì nó đọc XU_SESSION.md và suy ra nhiệm vụ, nhưng SESSION là tạm thời, không phải Truth.
- **Lesson:** Phải phân biệt "đọc được instruction" với "được phép thực hiện instruction". SESSION là RAM (thấp), PROJECT_STATE là Truth Table (cao). Khi SESSION và PROJECT_STATE mâu thuẫn, lấy PROJECT_STATE.
- **Action:** Đã thêm RULE vào AGENTS.md:19 "Meeting log là evidence, không phải state. Nếu meeting nói PENDING nhưng PROJECT_STATE.md nói PASS thì lấy PROJECT_STATE.md. Đây là Temporal Context Reasoning."
- **Date:** 2026-05-13

## DECISION — Authority Model & Core Protection Lock
Date: 2026-08-14
Status: CONFIRMED by VINH

1. Authority hierarchy chính thức: VINH > XU > AGENT
2. XU_CORE.md là source of truth về Authority và là Protected Core
3. AGENTS.md là Governance Contract, không phải authority actor
4. Mọi thao tác WRITE lên XU_CORE.md yêu cầu CORE_EDIT_AUTH
5. KEY được lưu trong file .env và .env đã được thêm vào .gitignore
6. Quản Gia tạm thời không thuộc authority chain thử nghiệm hiện tại

Source: Authority Model clarification + Core Lock — 2026-08-14