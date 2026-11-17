# BIÊN BẢN / MINUTES — WORK 802001

- Work ID: 802001
- Version: 1.2 — GOVERNANCE REFERENCE CORRECTION
- Date: 2026-11-17
- Chủ trì: Xu / AI-01; thẩm quyền cuối cùng: Vinh
- Chuẩn bắt buộc: Work 70 — DOC-001, DOC-004, DOC-005, DOC-033, DOC-035, DOC-057
- Status: BUSINESS SCOPE BASELINE — TECHNICAL DESIGN / IMPLEMENTATION NOT APPROVED

## 1. Mục tiêu đúng của Work 802001
Work 802001 chuẩn hóa nghiệp vụ **theo dõi, nhắc nhở, hướng dẫn và điều chỉnh Agent trong suốt quá trình Agent thực hiện Work/assignment/thi công**, dựa trên nghiệp vụ và quy trình đã được phê duyệt trong Work tương ứng.

Trọng tâm không phải xây một bộ máy kỹ thuật Gate độc lập trước. Trọng tâm là làm rõ cách ROOM-HOP/điều phối viên nhận biết Agent đang làm gì, đang ở bước nào, có bám nhiệm vụ và chuẩn nghiệp vụ không; khi có dấu hiệu sai/lệch/chậm/thiếu bằng chứng thì nhắc đúng lúc, hướng dẫn đúng tài liệu và yêu cầu điều chỉnh; sau đó kiểm tra lại và ghi nhận kết quả.

## 2. Phạm vi nghiệp vụ chuẩn
1. Tiếp nhận assignment, xác định Work/WP, Agent, vai trò, phạm vi, đầu ra, deadline/mốc và nguồn chuẩn.
2. Hướng dẫn Agent trước khi làm: đọc Manifest, Biên bản/Decision, kế hoạch, tiêu chuẩn, tài liệu liên quan và yêu cầu nhật ký.
3. Theo dõi tiến độ và dấu vết thực hiện theo checkpoint/mốc; so sánh hành động, sản phẩm và bằng chứng với kế hoạch đã duyệt.
4. Phát hiện sai nghiệp vụ, lệch scope, bỏ bước, sai cấu trúc, dùng sai nguồn, thiếu nhật ký/bằng chứng, báo cáo không đúng thực tế, chậm hoặc bị mắc kẹt.
5. Nhắc nhở theo mức độ và thời điểm; không spam, không nhắc chung chung; gắn với finding, căn cứ và hành động cần làm.
6. Hướng dẫn sửa sai theo từng bước, trỏ đúng tài liệu/path/tiêu chí; nêu việc được phép tiếp tục và việc phải dừng.
7. Theo dõi việc tiếp thu và sửa sai; yêu cầu Agent phản hồi/submit lại; kiểm tra lại độc lập hoặc chuyển reviewer phù hợp.
8. Escalate cho điều phối viên/chủ Work/người có thẩm quyền khi Agent lặp lỗi, không phản hồi, vượt quyền hoặc có rủi ro cao.
9. Ghi toàn bộ nhắc nhở, hướng dẫn, phản hồi, điều chỉnh, kiểm tra và kết quả vào Nhật ký/nguồn dữ liệu canonical.

## 3. Phân biệt chuẩn Work 70 và nghiệp vụ W802001
- W70 là chuẩn gốc về cấu trúc Work, lifecycle, state, Gate vòng đời, tài liệu, evidence, nhật ký và dashboard.
- W70 G0–G9 không bị thay thế hoặc đánh số lại bởi W802001.
- DOC-057 Work Entry Gate kiểm tra điều kiện tham gia/nhận việc; không thay thế việc theo dõi Agent trong lúc thi công.
- DOC-033 điều chỉnh tài liệu/lưu trữ; DOC-035 là nhật ký thi công cấp Work và quy định cách ghi nhận sự kiện, kết quả, trạng thái, bằng chứng. DOC-057 kiểm tra điều kiện tham gia/nhận assignment. DOC-096 là tài liệu Retrieval/DecisionRAG, không phải chuẩn phiên hoặc nhật ký và không được dùng làm căn cứ cho nghiệp vụ W802001.
- Nghiệp vụ W802001 là lớp vận hành theo dõi và hỗ trợ tuân thủ trong quá trình thực hiện. Gate chặn hành động chỉ là một biện pháp áp dụng khi có rủi ro, không phải toàn bộ sản phẩm.

## 4. Nguyên tắc vận hành
- Theo dõi theo assignment và checkpoint, không giám sát mơ hồ.
- Nhắc sớm để phòng sai; không đợi đến nghiệm thu mới phát hiện.
- Hướng dẫn dựa trên nguồn chuẩn hiện hành, không tự bịa nghiệp vụ.
- Phân biệt rõ: chưa làm, đang làm, chậm, blocked, làm sai, thiếu evidence, đã sửa, đã được xác minh.
- Agent tự báo cáo không đồng nghĩa đã hoàn thành; phải đối chiếu artifact/evidence và readback.
- Agent không tự xác nhận PASS cho chính lỗi/đầu ra cần reviewer độc lập.
- Chỉ dừng hành động có nguy cơ gây sai lệch/tác động; cho phép đọc, phân tích, thu thập evidence và khắc phục an toàn.
- Mọi nhắc nhở/quyết định có căn cứ, người nhận, thời điểm, hạn xử lý và kết quả.

## 5. Trạng thái nghiệp vụ theo dõi Agent
ASSIGNED → BRIEFED → IN_PROGRESS → (ON_TRACK | AT_RISK | BLOCKED | DEVIATION_FOUND) → REMINDED/COACHED → CORRECTION_SUBMITTED → RECHECK → (RESUMED | VERIFIED_DONE | ESCALATED).
Trạng thái này là trạng thái theo dõi assignment; không thay thế state machine vòng đời Work 70.

## 6. Phân loại phát hiện
SCOPE/ROLE; PROCESS; SOURCE-OF-TRUTH; STRUCTURE/NAMING; EVIDENCE/JOURNAL; QUALITY/ACCEPTANCE; STATUS/REPORTING; DELAY/NO-RESPONSE; SAFETY/SECURITY; UNKNOWN.
Mỗi finding phải có: mô tả cụ thể, căn cứ, evidence, mức độ, tác động, yêu cầu cần sửa, thời hạn, người chịu trách nhiệm, reviewer và điều kiện đóng.

## 7. Quyết định phạm vi
- Work 70 được dùng làm chuẩn gốc; W802001 bám sát chuẩn này.
- Phạm vi chính thức được làm rõ theo mục 1–6 của biên bản này.
- Hồ sơ E2E auto-wake/transcript-response cũ được bảo toàn như legacy/source evidence; không xóa, không tự động tiếp tục nhánh đó.
- Chưa triển khai code/runtime enforcement trước khi hoàn tất DISCOVER, DEFINE, truy vết luồng vận hành và phê duyệt kiến trúc.
- Không tuyên bố hệ thống đã tự theo dõi/nhắc Agent nếu chưa có kiểm chứng runtime thực tế.

## 8. Hồ sơ canonical
Biên bản: 00_ROOT/BIEN_BAN.md; Manifest: 00_ROOT/WORK_MANIFEST.md; Kế hoạch: 04_PLAN/IMPLEMENTATION_ROADMAP.md; Kiến trúc nghiệp vụ: 03_ARCHITECT/AGENT_OPERATIONAL_GATE_ARCHITECTURE.md; Nhật ký: 00_ROOT/NHAT_KY_THI_CONG.md; Verification: 06_VERIFY/VERIFICATION_PLAN.md; Evidence: EVIDENCE/EVIDENCE_REGISTER.md; Dashboard: DASHBOARD/README.md.
