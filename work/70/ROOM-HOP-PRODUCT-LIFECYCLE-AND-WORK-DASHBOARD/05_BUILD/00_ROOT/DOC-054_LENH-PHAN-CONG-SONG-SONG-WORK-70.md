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


---

## ADDENDUM 2026-11-02 — PHÂN CÔNG BỔ SUNG KA / VI / AN: RUNTIME RECONCILIATION

**Trạng thái:** ASSIGNMENT READY — ACK PENDING — NOT A BUILD AUTHORIZATION  
**Điều phối:** Xu / AI-01  
**Quyền quyết định:** Vinh

### WP70-KA-RUNTIME — Architecture reconciliation
**Owner:** Ka / AI-02  
**Mục tiêu:** chốt ranh giới trách nhiệm giữa `wee/`, `execution_host/`, Work 70 Lifecycle Engine, Core, Evidence Registry và Dashboard; không thiết kế lại từ đầu nếu có thể tái sử dụng.
**Việc phải làm:**
1. Đọc DOC-005, DOC-016, DOC-017, DOC-060, DOC-061, DOC-063 và source hiện hành.
2. Lập capability matrix: existing / partial / missing / unverified, kèm file + symbol + test evidence.
3. Vẽ luồng runtime và trust boundary; chỉ rõ ai giữ state, authorization, persistence, evidence và audit.
4. Đề xuất phần tái sử dụng, phần adapter cần nối, phần còn thiếu; nêu migration/integration risks.
5. Xác định tối thiểu contract và test cần có để chứng minh controller thật sự gọi execution/test entrypoint.
**Bàn giao:** architecture delta/ADR, diagram, component ownership matrix, decision list.
**Giới hạn:** read-only; không sửa code, không đổi Gate, không tuyên bố G4 PASS.

### WP70-VI-CORE-TRACE — Core capability and integration trace
**Owner:** Vi  
**Mục tiêu:** xác minh Core hiện có gì bằng source-level evidence, không suy diễn từ tài liệu hoặc API dự kiến.
**Việc phải làm:**
1. Truy vết router → service → model/schema → authorization → persistence → tests.
2. Lập endpoint/capability inventory cho Work, Work Package, assignment/ACK, lifecycle transition, evidence upload/read/version, audit, export.
3. Mỗi capability ghi rõ VERIFIED / PARTIAL / NOT FOUND IN INSPECTED SCOPE / NOT VERIFIED; kèm path, symbol, route, test và lý do.
4. Đánh giá khả năng dùng Core hiện tại; không tạo database/parallel store, không dùng Meeting artifact làm Work evidence nếu chưa có contract.
5. Đề xuất adapter/API gap tối thiểu, phân biệt mock / snapshot / live và điều kiện để Dashboard đọc đúng nguồn.
**Bàn giao:** Core trace report, route/service/schema/auth matrix, API gap list, đề xuất tích hợp.
**Giới hạn:** read-only; không thêm route, migration, database, Dashboard live claim hoặc sửa Core.

### WP70-AN-CONTROLLER-QA — Independent execution-path test
**Owner:** An — Tester  
**Mục tiêu:** kiểm tra độc lập tuyên bố thực thi của WEE LifecycleController và execution_host, tìm false PASS và đường đi bị bỏ qua.
**Việc phải làm:**
1. Xây test matrix cho RESOLVE → BIND → VALIDATE → PREPARE → EXECUTE → TEST; xác minh mỗi stage có hành vi thật và evidence.
2. Kiểm tra controller có thực sự gọi bound test entrypoint hay chỉ ghi PASS sau capability discovery.
3. Negative tests: authority missing/expired/mismatch; wrong Work/repo/branch/HEAD; command denied; timeout; process failure; test entrypoint missing; evidence write/hash failure; retry/idempotency; partial execution.
4. Tách rõ unit test, integration test, direct adapter test và controller E2E; không dùng test của adapter để kết luận controller PASS.
5. Chạy test khi có runtime phù hợp; nếu không có test runner/quyền truy cập, ghi BLOCKED cùng lệnh cần chạy và evidence còn thiếu, không giả lập PASS.
**Bàn giao:** test matrix, reproducible test commands, raw outputs, defect list, evidence refs và kết luận PASS/FAIL/BLOCKED theo từng stage.
**Giới hạn:** không sửa implementation để làm test xanh; không tự nghiệm thu code của mình; không mở G4/BUILD.

### Thứ tự và quy tắc phối hợp
- Ka định nghĩa ownership và integration contract; Vi cung cấp Core trace độc lập; An kiểm tra execution behavior theo source hiện hành.
- Ba track chạy song song, không sửa cùng file. Mọi đề xuất thay đổi phải nêu file, lý do, tác động và owner trước khi thực hiện.
- Mỗi AI phải xác nhận ACK bằng phản hồi/artefact định danh. Lệnh này chưa chứng minh AI đã nhận việc.
- Xu tổng hợp kết quả, xử lý xung đột và trình Vinh quyết định; không chuyển sang BUILD chỉ vì ba báo cáo hoàn tất.
- Exit condition: đủ ba báo cáo có evidence; unresolved gaps được phân loại; Ka/Vi/An không tự cấp Gate hoặc quyền BUILD.
