# KIẾN TRÚC NGHIỆP VỤ THEO DÕI & HƯỚNG DẪN AGENT / AGENT WORK SUPERVISION AND GUIDANCE

- Work: 802001
- Artifact ID: W802001-ARCH-AOG-001
- Version: 1.2 — GOVERNANCE REFERENCE CORRECTION
- Date: 2026-11-17
- Status: BUSINESS BASELINE / TECHNICAL DESIGN NOT APPROVED
- Authority: Vinh

## 1. Mục đích
Chuẩn hóa cách ROOM-HOP theo dõi Agent trong suốt quá trình nhận việc và thi công; phát hiện sớm sai nghiệp vụ, lệch tiến độ, thiếu hồ sơ/bằng chứng hoặc hành vi vượt quyền; nhắc nhở và hướng dẫn Agent điều chỉnh theo nguồn chuẩn của Work; kiểm tra lại và lưu vết đến khi hoàn tất hoặc escalated.

AOG (Agent Operational Gate) là tên lớp kiểm soát/điểm quyết định trong nghiệp vụ này, không phải toàn bộ sản phẩm. Nghiệp vụ trung tâm là Agent Work Supervision & Guidance (theo dõi và hướng dẫn Agent trong quá trình làm việc).

## 2. Đối tượng và context bắt buộc
Mỗi assignment cần có Work ID, WP/Assignment ID, Agent/Actor ID, vai trò được xác minh, người giao việc, scope, deliverables, deadline/checkpoints, acceptance criteria, canonical sources/revisions, dependencies, risk level và nơi ghi nhật ký/evidence. Thiếu dữ liệu phải tạo clarification/blocker; không tự suy diễn.

## 3. Quy trình nghiệp vụ end-to-end
1. ASSIGNMENT INTAKE: tiếp nhận nhiệm vụ, owner, Agent, phạm vi, đầu ra, thời hạn và quyền.
2. BASELINE & BRIEFING: đọc Work Manifest, Biên bản/Decision, kế hoạch, WP, tiêu chuẩn, source of truth; gửi hướng dẫn trước khi Agent bắt đầu.
3. ACKNOWLEDGEMENT: ghi nhận Agent đã nhận việc/hiểu yêu cầu; nếu chưa xác nhận hoặc hiểu sai thì làm rõ trước bước có rủi ro.
4. CHECKPOINT SETUP: xác định mốc kiểm tra theo rủi ro, thời lượng, dependency và deliverable; tránh giám sát dày gây lãng phí.
5. PROGRESS OBSERVATION: thu thập status, hoạt động, artifact, commit/tool evidence, journal, blocker và thời điểm cập nhật.
6. COMPLIANCE & DRIFT CHECK: so sánh thực tế với assignment, quy trình, cấu trúc W70, quyền, source revision, acceptance và checkpoint.
7. CLASSIFY & REMIND: phân loại ON_TRACK / AT_RISK / BLOCKED / DEVIATION_FOUND / NO_RESPONSE; gửi nhắc nhở đúng người, đúng việc, nêu căn cứ và hạn xử lý.
8. GUIDED CORRECTION: hướng dẫn sửa theo thứ tự, dẫn đúng tài liệu/path/tiêu chí; chỉ rõ điều phải dừng và việc an toàn vẫn được làm.
9. CORRECTION SUBMISSION: Agent nộp phản hồi và bằng chứng sửa; không coi lời xác nhận đơn thuần là hoàn thành.
10. RECHECK: đối chiếu lại artifact/evidence, yêu cầu reviewer độc lập nếu cần.
11. RESUME / CLOSE / ESCALATE: cho tiếp tục khi đạt điều kiện; xác nhận hoàn thành khi evidence đủ; escalate khi lặp lỗi, quá hạn, im lặng hoặc vượt thẩm quyền.
12. JOURNAL & LEARNING: ghi đầy đủ chuỗi theo dõi; đề xuất cập nhật hướng dẫn/policy qua phê duyệt, không tự thay đổi chuẩn.

## 4. Quy tắc nhắc nhở
- Reminder 1 — nhắc nhẹ: sắp đến checkpoint/deadline hoặc thiếu cập nhật; nêu việc cần cập nhật và thời hạn.
- Reminder 2 — cảnh báo: đã trễ mốc hoặc có dấu hiệu lệch; nêu evidence và yêu cầu kế hoạch khắc phục.
- Correction Notice — yêu cầu điều chỉnh: xác định rõ quy tắc bị vi phạm, hành động sai, cách sửa, đầu ra cần nộp và điều kiện recheck.
- Escalation — chuyển cấp: lỗi lặp lại, không phản hồi, vi phạm quyền/an toàn, hoặc ảnh hưởng critical path; chuyển người có thẩm quyền.
Ngưỡng thời gian và số lần nhắc phải được DEFINE theo loại Work/risk; không hard-code một lịch nhắc chung cho mọi Agent.

## 5. Hợp đồng finding/hướng dẫn sửa sai
Mỗi finding/reminder gồm: ID; Work/WP/assignment; Agent; timestamp; checkpoint; status; severity; rule/source path và version; mô tả sai lệch; evidence quan sát; expected behavior; tác động; việc phải dừng; việc vẫn được phép làm; hướng dẫn sửa theo thứ tự; deliverable/evidence phải nộp; deadline; owner; reviewer; recheck method; exit criteria; escalation condition.
Không dùng lời nhắc chung chung như “làm đúng quy trình”. Nếu chưa đủ căn cứ, đánh dấu UNKNOWN/NEEDS_CLARIFICATION và hỏi người có thẩm quyền.

## 6. Trạng thái theo dõi assignment
ASSIGNED → BRIEFED → IN_PROGRESS → ON_TRACK / AT_RISK / BLOCKED / DEVIATION_FOUND → REMINDED / COACHED → CORRECTION_SUBMITTED → RECHECK → RESUMED / VERIFIED_DONE / ESCALATED.
Đây là operational workflow của assignment, không thay thế lifecycle Work 70 và không tự tạo PASS cho Gate vòng đời.

## 7. Phân tầng kiểm soát
- Work 70 governance: lifecycle, cấu trúc, tài liệu, Gate vòng đời và trạng thái Work.
- Assignment supervision: theo dõi Agent, checkpoint, tiến độ, nhắc nhở, hướng dẫn, correction và escalation.
- Policy/decision control: xác định hành động nào được phép, cần review hoặc phải dừng.
- Enforcement: nếu có, phải chặn tại execution boundary; prompt/dashboard không phải enforcement.
- Journal/evidence: lưu vết có thể đọc lại, truy nguyên actor, thời gian, source và kết quả.

## 8. Phân biệt với Work 70
W70 G0–G9 kiểm soát chuyển pha Work; DOC-057 kiểm soát điều kiện tham gia/nhận assignment; DOC-033 điều chỉnh tài liệu/lưu trữ; DOC-035 là nhật ký thi công cấp Work. DOC-096 là tài liệu Retrieval/DecisionRAG, không phải chuẩn phiên/nhật ký. W802001 chuẩn hóa nghiệp vụ giám sát/hướng dẫn Agent trong khi thực hiện assignment và dùng đúng các chuẩn W70 làm căn cứ. Các lớp bổ sung nhau, không thay thế nhau.

## 9. Nguyên tắc dữ liệu và trách nhiệm
- Mọi status phải gắn source, timestamp, owner và freshness.
- Agent tự báo cáo không đủ để xác nhận tiến độ/hoàn thành; cần đối chiếu evidence.
- Không suy diễn identity, không trao quyền ngoài assignment.
- Không cho Agent tự đóng finding nghiêm trọng hoặc tự duyệt correction của chính mình.
- Không xóa lịch sử sai; correction là bản ghi nối tiếp.
- Nhật ký là nguồn truy vết; dashboard chỉ là read-only projection.

## 10. Nội dung cần khảo sát trước thiết kế kỹ thuật
Cách lấy tín hiệu tiến độ từ Agent/Room; mô hình assignment/checkpoint; nơi lưu reminder và correction; cách xác thực Agent identity; quyền đọc artifact/journal; cơ chế reviewer/escalation; các execution paths có thể cần enforcement; hành vi khi Agent offline hoặc nguồn dữ liệu stale. Không chọn công nghệ trước READ/TRACE.
