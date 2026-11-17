# KẾ HOẠCH TRIỂN KHAI — WORK 501
- Phiên bản: 0.1 | Ngày: 2026-11-17 | Trạng thái: DESIGN PLAN — BUILD NOT AUTHORIZED
## Mục tiêu
Thiết kế LLM Hub provider-neutral, local-first, global-controlled, có Model Arena và zero-cost guard; tích hợp vào ROOM-HOP mà không tạo hệ thống identity/orchestration trùng lặp.
## Work Packages
| WP | Nội dung | Đầu ra | Trạng thái |
|---|---|---|---|
| 501-01 | READ/TRACE Works 01,11,23,52,70,22,50 và runtime | Inventory, source/version, ownership, contracts | IN_PROGRESS |
| 501-02 | Kiểm kê phần cứng và local feasibility | Hardware profile, runtime comparison, capacity | BLOCKED — chưa có số liệu phần cứng xác minh |
| 501-03 | Requirements và global policy | Requirements, Agent grants, data classes, cost policy | PLANNED |
| 501-04 | Architecture và ADR | Diagrams, API contract, trust boundary, decisions | PLANNED |
| 501-05 | Provider/model catalog | Schema, capability, license, provenance | PLANNED |
| 501-06 | Router/fallback/cost guard | Routing rules, failure matrix, paid-deny tests | PLANNED |
| 501-07 | Model Arena | Blind first pass, challenge, rubric, evidence model | PLANNED |
| 501-08 | Security/privacy review | Threat model, secrets, egress, retention | PLANNED |
| 501-09 | QE and acceptance | Test matrix, measurable gates, negative tests | PLANNED |
| 501-10 | Dashboard/operations | Live data contract, role-based controls | PLANNED |
| 501-11 | Independent consultation | Reviewer dispatch/ACK/reports/reconciliation | PENDING |
| 501-12 | Design gate package | Final minutes, ADR, plan, journal, approval | BLOCKED — reviews pending |
## Trình tự
1. READ → TRACE: khảo sát source, cấu trúc, contract và ownership hiện hữu.
2. ANALYZE: xác định trùng lặp, rủi ro, hardware fit, provider constraints, privacy và cost.
3. CONSULT: gửi brief theo vai trò; chỉ ghi nhận dispatch/ACK khi có bằng chứng thực tế.
4. DECIDE: so sánh build-vs-adopt; lập ADR cho các quyết định trọng yếu; ghi rõ dissent và residual risks.
5. BUILD GATE: chỉ mở khi điều kiện thiết kế đạt và Vinh phê duyệt riêng. Phê duyệt thiết kế không đồng nghĩa cho phép chi tiền/bật billing/deploy.
## Phân công dự kiến
Vinh: Product Owner/authority. Xu: coordinator/architecture synthesis. Cla: technical. Ka: security/privacy. Qw: QE. Go: hardware/cost feasibility. Vibe: adversarial review. Kha: provider/Work 23. Qc: implementation feasibility, no code. Gem: Agent UX/operation. Chưa có bằng chứng các reviewer đã nhận việc.
## Zero-cost constraints
Ngân sách hiện tại: 0 đồng. Không paid API/subscription, không bật billing/payment, không tạo cloud resources có khả năng bill, không tạo account/token/key, không tải model weights hoặc cài runtime trong giai đoạn thiết kế.
## Acceptance criteria
- Agent identity tách biệt model identity; đổi model không đổi Agent ID/role/session/permissions.
- Global policy allow/deny theo Agent/task/provider/model/data class.
- Paid provider bị chặn server-side; hết quota free không fallback paid.
- Local-first và free-cloud fallback minh bạch, có lý do và audit.
- Registry có version, capability, license, provenance và verification timestamp.
- Arena có independent first pass, challenge phase, rubric và evidence; không suy diễn đồng thuận là sự thật.
- Secrets không xuất hiện trong Git/docs/source/log/UI payload.
- Không thay thế Core/Gateway/Agent Runtime.
- Live dashboard chỉ hiển thị dữ liệu có nguồn; còn lại NOT VERIFIED.
- Mọi gate có evidence; không tự đánh dấu PASS.
## Hiện trạng
Sandbox Work 501 đã tạo. Hồ sơ thiết kế đang được lập. GitHub sync chỉ được đánh dấu DONE sau khi xác minh commit và fetch/readback. PC parity chưa xác minh. BUILD chưa được phép.