# BIÊN BẢN THIẾT KẾ — WORK 502: MÊ AUTONOMOUS AI BUILDER
- Document ID: W502-BB-001
- Version: 0.1
- Date: 2026-11-18 (Asia/Ho_Chi_Minh)
- Chủ trì / thẩm quyền cuối cùng: Vinh
- Điều phối: Xu / AI-01
- Status: PROVISIONAL DESIGN BASELINE — CHỜ PHẢN BIỆN ĐỘC LẬP; BUILD NOT AUTHORIZED

## 1. Mục tiêu sản phẩm
MÊ nhận một yêu cầu ngôn ngữ tự nhiên, tự làm rõ mục tiêu bằng giả định có kiểm soát, tạo PRD/kế hoạch, điều phối các vai trò chuyên môn, thao tác công cụ trong vùng được cấp quyền, tự kiểm tra/sửa có giới hạn và bàn giao sản phẩm có source, bằng chứng, hướng dẫn chạy và link demo khi đã triển khai hợp lệ.

## 2. Quyết định kiến trúc đã thống nhất
1. Sử dụng AutoGPT Platform làm nền tảng Agent/workflow execution candidate, ưu tiên self-host; không chọn AutoGPT Hosted vì mô hình hosted có tính phí.
2. Tích hợp vào ROOM-HOP nhưng AutoGPT vận hành như một execution engine độc lập, được ROOM-HOP kiểm soát qua adapter/gateway; không thay thế ROOM-HOP Core.
3. Tạo Work riêng 502; không nhập MÊ vào Work 500 (Product Demo), Work 501 (LLM Hub) hoặc Work 30 (GPT Autonomous Build Team).
4. MÊ có 1 Manager/Orchestrator và 6 vai trò: Research, Architect, Coder, Designer, QA, Deploy. Vai trò là cấu hình nhiệm vụ; không mặc định đồng nghĩa với 6 LLM hoặc 6 tiến trình.
5. Model topology phải linh hoạt: cùng một LLM có thể chạy tất cả vai trò; hoặc mỗi vai trò dùng model khác nhau. Việc chọn model/provider được Work 501 quản lý theo policy, capability, quota và chi phí.
6. Mặc định triển khai thử nghiệm bằng một model đủ năng lực, zero-cost/local nếu có thể; chỉ bật multi-model sau khi Work 501 cung cấp model/provider đã được duyệt. Đây là mặc định thiết kế, chưa phải model selection.
7. Một LLM/Agent không được tự chứng nhận sản phẩm mình tạo. QA cần test tự động có bằng chứng và review độc lập; kết quả phải phân biệt PASS, FAIL, BLOCKED, NOT RUN.
8. Tự lấp chỗ trống chỉ với giả định có thể đảo ngược, rủi ro thấp; mọi giả định và quyết định phải ghi lại. Hỏi Vinh hoặc dừng khi liên quan chi phí, dữ liệu nhạy cảm, quyền truy cập, xóa/mất dữ liệu, pháp lý, bảo mật hoặc triển khai production.
9. Không tự phát sinh chi phí. Không có paid fallback im lặng. Khi không có model/tool đủ điều kiện, trả BLOCKED thay vì tự ý đổi sang dịch vụ tính phí.
10. Không triển khai production công khai khi chưa có phê duyệt riêng và cổng bảo mật/acceptance đạt yêu cầu.

## 3. Phân vai
- MÊ Manager: tiếp nhận một câu, tạo intake/spec, chia task, quản lý state, giao vai trò, retry và tổng hợp bàn giao.
- Research: nghiên cứu nguồn, đối thủ, thư viện, giấy phép, tài liệu và bằng chứng.
- Architect: PRD, kiến trúc, dữ liệu, API, ADR, tiêu chí nghiệm thu.
- Coder: sửa/tạo source trong workspace được cấp quyền; không được tự đổi kiến trúc hoặc vượt scope.
- Designer: UI/UX, design system, asset và responsive; asset bên ngoài phải rõ nguồn/license.
- QA: unit/integration/browser/E2E, regression, accessibility và security checks theo phạm vi; lưu log, ảnh và kết quả thật.
- Deploy: build/package/deploy vào môi trường được cho phép; secrets server-side; preview trước production; không tự mở public access.

## 4. Luồng vận hành chuẩn
INTAKE → DISCOVER → DEFINE/PRD → ARCHITECT → PLAN → ASSIGN → BUILD → VERIFY → REPAIR (bounded) → ACCEPT → RELEASE/DEPLOY → HANDOFF.
- Task độc lập có thể chạy song song sau khi khóa giao diện và vùng source; task có phụ thuộc phải chạy tuần tự.
- Retry tối đa 3 lần cho cùng một phương án. Sau đó phải dừng, ghi nguyên nhân và chọn phương án khác hoặc BLOCKED; không lặp vô hạn.
- Mỗi task có owner role, input/output contract, dependencies, acceptance criteria, timeout, retry budget, allowed tools, cost/resource budget và evidence pointer.
- Mọi thao tác có side effect phải qua policy/permission gate; command/tool output là dữ liệu không đáng tin cho tới khi xác minh.

## 5. Ranh giới tích hợp
- ROOM-HOP Core: identity, authorization, agent registry, session/task authority, global policy và audit authority.
- Work 501: provider/model registry, model capability, routing, quota/cost policy, invocation audit và model arena. Work 501 hiện đang ở design/consultation; chưa coi là runtime ready.
- AutoGPT Platform: agent graph, block execution, workflow/task runtime, queue/memory/storage nội bộ AutoGPT theo cấu hình được duyệt.
- MÊ Adapter: chuyển task có cấu trúc từ ROOM-HOP sang AutoGPT, map identity/session/task, áp dụng allowlist, giới hạn tool, nhận trạng thái/evidence và trả kết quả.
- ROOM-HOP Sandbox/Execution Host: source workspace, command execution và browser test chỉ thông qua runtime được xác minh; không trao quyền shell/host trực tiếp không giới hạn cho AutoGPT.
- GitHub: source/version history canonical sau khi path/branch được phê duyệt; AI không tự merge/push nếu policy hiện hữu không cho phép.

## 6. Những nội dung chưa chốt
AutoGPT version/tag; license review chi tiết; Docker/host topology; cấu hình database/queue/cache/memory; provider/model baseline; hardware; adapter API; tool/block allowlist; sandbox isolation; file/source ownership; authentication mapping; secrets; dashboard; data retention; backup/restore; concurrency; rate/resource limits; deployment targets; acceptance thresholds.

## 7. Điều kiện trước BUILD
Hoàn tất source/contract discovery của ROOM-HOP Core, Gateway, Agent Runtime, Sandbox/Execution Host, Work 501, Work 14, Work 30, Work 15, Work 16, Work 22 và Work 50; phản biện độc lập; xác minh AutoGPT release/license/security/deployment requirements; chốt threat model, data flow, API contracts, test strategy, rollback và resource budget; Vinh phê duyệt rõ ràng cho BUILD.

## 8. Phạm vi phiên hiện tại
Đã tạo Sandbox Work 502 bằng identity xu được ROOM-HOP xác nhận hợp lệ. Đã ghi nhận kiến trúc thiết kế sơ bộ. Chưa cài đặt AutoGPT, tải image/model, tạo key, gọi API, bật billing, tạo cloud resource, chạy test runtime hoặc triển khai. GitHub main sync chưa được thực hiện trong lần này.