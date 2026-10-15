# BIÊN BẢN THỐNG NHẤT PHƯƠNG ÁN XÂY DỰNG TOOL ROOM-HOP
Ngày: 2026-10-14 (+07)
Work: 28 — MCP-8020-TOOLING-PLATFORM
Phạm vi: Chuẩn hóa nền tảng tool dùng chung cho ROOM-HOP; không mở rộng ngoài mục tiêu Work 28.
Quyền quyết định cuối cùng: Vinh.
Điều phối triển khai: Xu; phối hợp review kỹ thuật/bảo mật và E2E theo phân công hiện hành.

## 1. Quyết định đã thống nhất
- Work 28 được định hướng là nền tảng Tooling dùng chung cho ROOM-HOP, không chỉ là danh sách MCP tools.
- Không đặt số lượng tool cố định cho toàn hệ thống. Tool được bổ sung theo nhu cầu đã xác minh, mỗi tool có mục đích rõ, hợp đồng dữ liệu, quyền, phạm vi Work và bằng chứng kiểm định.
- Không tạo Work/Core/runtime/PC bridge trùng lặp; tái sử dụng các seam canonical hiện có.
- Core :8000 là authority duy nhất cho authorization và WorkContext; MCP :8020 là adapter.
- Không đăng ký hoặc bật python_run/arbitrary execution khi các cổng bảo mật và runtime chưa được chứng minh. Trạng thái hiện tại tiếp tục NO-GO cho execution; python_run = NOT REGISTERED / NOT ENABLED.

## 2. Mô hình kiến trúc mục tiêu
1. Tool Registry: danh mục, phiên bản, schema, trạng thái và nguồn đăng ký.
2. Tool Router: tìm/chọn tool phù hợp và kiểm tra khả năng truy cập.
3. Policy & Permission Gate: quyền, Work scope, mức rủi ro và yêu cầu phê duyệt.
4. Execution Adapter: MCP/API và runtime canonical được phê duyệt; không unrestricted shell.
5. Result & Evidence: kết quả thật, lỗi, log, checkpoint, định danh tương quan và readback.

Đây là mô hình mục tiêu; không được ghi nhận các lớp là đã triển khai nếu chưa có bằng chứng source/runtime.

## 3. Nhóm chức năng tool
- READ: đọc trạng thái, tài liệu, file và dữ liệu được cấp quyền.
- BUILD: tạo/sửa artifact trong Work scope.
- EXECUTE: chạy tác vụ đã đăng ký qua runtime được phê duyệt.
- VERIFY: kiểm thử, xác minh kết quả và thu bằng chứng.
- RELEASE: commit/push/triển khai theo quyền và chính sách.
- CONTROL: quyền, trạng thái, checkpoint, audit và dừng an toàn.

Một tool có thể hỗ trợ nhiều quy trình, nhưng phải có một mục đích chính, schema rõ và chính sách quyền có thể kiểm tra. Mỗi Agent chỉ được cung cấp tập tool cần thiết cho nhiệm vụ.

## 4. Hợp đồng tối thiểu cho mỗi tool
- tool_id, purpose, version/status.
- input_schema và output_schema.
- permissions và allowed_work_scope.
- risk_level và approval_policy.
- timeout/retry_policy; idempotency khi phù hợp.
- evidence_policy và định danh request/task/run khi áp dụng.
- Trạng thái chuẩn: PASS, FAIL, BLOCKED, DENIED, TIMEOUT, NOT_FOUND hoặc INVALID_REQUEST phù hợp ngữ cảnh.
- Không được tạo PASS nếu thiếu bằng chứng thực thi bắt buộc; lỗi hoặc dependency không sẵn sàng phải báo đúng trạng thái, không giả lập thành công.

## 5. Thứ tự thi công
WP0 — READ/TRACE: kiểm kê source, registry live, deployed revision, Core authorization/WorkContext và runtime canonical; ghi path/revision/SHA và dependency. Không suy diễn endpoint hoặc quyền từ tài liệu.
WP1 — Registry + contract: đối chiếu 18 tool đang quan sát qua connector với registry live trên PC; chuẩn hóa tool contracts và trạng thái đăng ký.
WP2 — Security hardening: đóng các lỗ hổng hợp đồng, kiểm tra path containment, identity/principal binding, quyền, timeout, giới hạn tài nguyên và tính toàn vẹn bằng chứng.
WP3 — Approved runner: chỉ dùng runtime canonical sau khi xác minh OS isolation, không lộ secrets, không truy cập host/network/loopback trái phép, dọn process tree và lưu bằng chứng được bảo vệ.
WP4 — Regression + independent review: chạy test bằng runner được duyệt; Cla review bảo mật, Go kiểm tra khả năng E2E độc lập; giữ nguyên báo cáo gốc.
WP5 — Live E2E: chạy qua entry point MCP thật theo ma trận test; thu request/task/run ID, exit code, output/log đã redacted, source hash và evidence reference; đọc lại bằng chứng độc lập.
WP6 — Release decision: chỉ chuyển gate sang PASS khi đủ bằng chứng; nếu thiếu dependency thì BLOCKED. Work vẫn ACTIVE / NOT LOCKED cho đến khi Vinh phê duyệt đóng.

## 6. Quy tắc không được vi phạm
- Không Core 2, không execution host thứ hai, không bypass Core.
- Không tin caller-supplied authorized/identity như bằng chứng cấp quyền.
- Không cung cấp shell/Python tùy ý không được cô lập.
- Không tự phê duyệt thay đổi của chính mình; sửa lỗi phải giữ lịch sử và chạy lại kiểm thử.
- Không ghi PASS từ việc tạo file, đọc lại file, HTTP 200 hoặc liệt kê tool.
- Giữ nguyên artifact review của Cla/Go; chỉ bổ sung hoặc tạo phiên bản mới, không ghi đè bằng chứng độc lập.

## 7. Trạng thái và bước kế tiếp
- DONE: Vinh thống nhất phương án xây dựng Tooling theo biên bản này trong hội thoại ngày 2026-10-14.
- BLOCKED: registry live/deployed PC revision, approved Python runner, OS isolation, G3–G6 và live E2E chưa được xác minh đầy đủ theo evidence hiện có.
- NEXT: Xu tiếp tục từ WP0, đối chiếu nguồn thực tế và cập nhật nhật ký; không yêu cầu Vinh chạy từng thao tác nhỏ khi có thể tự xử lý qua các công cụ được cấp quyền.
- Work 28: ACTIVE / NOT LOCKED.
