# DOC-054 — LỆNH PHÂN CÔNG SONG SONG WORK 70
- **STT / Document ID:** DOC-054
- **Priority:** P0
- **Read order:** 54
- **Depends on:** DOC-001; DOC-042; DOC-043; DOC-044
- **Status:** ACTIVE / ASSIGNMENT READY
- **Version / Updated:** 1.0 / 2026-10-31
- **Owner:** Xu / AI-01
- **Authority:** Vinh
- Work: 70 — Bộ máy Room
- Ngày: 2026-10-31
- Điều phối: Xu / AI-01
- Quyền quyết định cuối: Vinh
- Trạng thái: ASSIGNMENT READY — chưa xác nhận AI đã nhận việc

## 1. Mục tiêu
Tăng tốc xây dựng bộ máy thực thi Work Lifecycle thật. Chia module độc lập, hợp đồng giao tiếp chung, tích hợp qua Xu. Không tiếp tục chỉ bổ sung tài liệu quản trị.

## 2. Phân công

### WP70-KA — Kiến trúc và hợp đồng tích hợp
- Owner đề xuất: Ka / AI-02
- Phạm vi: kiến trúc runtime; state machine; điều kiện chuyển trạng thái; API contract giữa Lifecycle Engine, Core và Dashboard; event/audit model; concurrency và idempotency.
- Đầu ra: architecture decision record; sơ đồ thành phần/luồng; OpenAPI hoặc JSON contract; bảng state-transition; rủi ro và quyết định cần Vinh.
- Không sửa code engine hoặc Dashboard của Co/Vi.
- Điều kiện hoàn tất: mọi interface có request/response, lỗi, auth scope, versioning và acceptance tests rõ ràng.

### WP70-CO — Lifecycle Engine
- Owner đề xuất: Co / AI-07
- Phạm vi: domain engine độc lập với LLM; Work/Work Package registry; state transition guard; dependency validation; assignment lifecycle; event/audit trail; idempotent command handling.
- Đầu ra: source code, unit tests, migration/schema nếu cần, README chạy local, test evidence.
- Dùng contract tạm thời đã công bố; không tự đổi API contract. Nếu cần đổi, mở đề xuất cho Xu/Ka.
- Không truy cập/sửa Dashboard hoặc Core integration của Vi.
- Không tự đánh dấu PASS cho test do chính Co viết.

### WP70-VI — API Adapter và Dashboard
- Owner đề xuất: Vi / coder
- Phạm vi: điều tra Core route hiện có; lập capability gap có bằng chứng; xây read adapter/API client và Dashboard read-only theo contract của Ka; mock server/fixtures để chạy độc lập khi Core chưa sẵn sàng.
- Đầu ra: API adapter; Dashboard; loading/empty/error/unauthorized states; integration tests; bằng chứng phân biệt mock/snapshot/live.
- Không tạo nguồn dữ liệu thứ hai; không giả lập Core live. Không sửa domain engine của Co.
- Nếu Core thiếu endpoint, báo gap; không tự ý mở rộng Core ngoài phạm vi.

### WP70-QA — Test độc lập
- Owner đề xuất: Qw / AI-05 (hoặc Test được Vinh chỉ định)
- Phạm vi: test strategy; contract tests; state-transition matrix; negative/security tests; dependency/race/idempotency tests; regression và E2E sau tích hợp.
- Đầu ra: test plan, test cases, defect log, reproducible commands, raw test results, independent QE report.
- Viết test độc lập với implementation; không sửa code của Co/Vi để làm test xanh.
- Không PASS khi test không chạy, thiếu dependency hoặc chỉ dùng mock nhưng báo live.

## 3. Thứ tự chạy song song
- Track A: Ka chốt contract phiên bản v1 trước; Co có thể dựng domain model và unit-test skeleton nhưng không khóa interface trước khi contract được phát hành.
- Track B: Vi điều tra Core và dựng Dashboard với mock fixtures; sau contract v1 thì adapter phải khớp contract.
- Track C: Qw viết test matrix và contract tests dựa trên contract v1; sau đó chạy độc lập trên tích hợp thật.
- Xu điều phối dependency, review thay đổi, tích hợp, xử lý xung đột và cập nhật register/evidence.

## 4. Quy tắc làm việc
1. Một module có một owner; không hai AI cùng sửa một file.
2. Mọi thay đổi phải ở nhánh riêng/PR riêng; không commit trực tiếp vào main.
3. Trước khi code: đọc baseline, nêu files dự kiến sửa và dependencies.
4. Mỗi bàn giao gồm commit/PR, file list, test commands, kết quả thật, evidence refs, known gaps.
5. Không ghi DONE/PASS nếu chưa chạy kiểm chứng tương ứng.
6. Không dùng MCP 8020. Sandbox/MCP 8030 là kênh đọc/ghi Sandbox; quyền ghi Sandbox không đồng nghĩa quyền dispatch AI.
7. Xu chỉ xác nhận AI đã nhận việc khi có phản hồi/artefact định danh từ chính AI đó.

## 5. Gate tích hợp
- G0: Ka contract v1 được Xu review.
- G1: Co unit tests + Qw contract tests chạy độc lập.
- G2: Vi adapter/dashboard khớp contract; mock và live được phân biệt.
- G3: integrated E2E, auth/negative tests, persistence/recovery tests.
- G4: Qw independent QE report; Xu đối soát; Vinh quyết định nghiệm thu.
Không tự động mở release khi bất kỳ gate nào chưa đạt.

## 6. Giới hạn năng lực điều phối hiện tại
MCP 8030 hiện cung cấp thao tác Sandbox và Meeting, không có công cụ dispatch trực tiếp Co/Vi/Ka/Qw trong phiên này. Tài liệu này là lệnh phân công đã chuẩn bị và lưu vào Sandbox; chưa được xem là đã gửi/được nhận bởi các AI. Xu phải chuyển lệnh qua kênh làm việc thực tế của từng AI hoặc công cụ điều phối được xác minh, rồi ghi nhận phản hồi nhận việc.
