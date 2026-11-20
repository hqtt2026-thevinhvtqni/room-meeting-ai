# Ma trận vai trò và quyền AI / AI Role & Permission Matrix
- **STT / Document ID:** DOC-043
- **Priority:** P0
- **Read order:** 43
- **Depends on:** DOC-002; DOC-004; DOC-005; DOC-042
- **Status:** ACTIVE / CONTROLLED REGISTER
- **Version / Updated:** 1.0 / 2026-10-30

## 1. Nguyên tắc
Danh sách AI chỉ là khai báo vai trò. Không chứng minh agent đang hoạt động, đã kết nối, có quyền truy cập hoặc đã thực hiện công việc. Mỗi lần tham gia phải xác minh danh tính, capability và quyền trên đúng Work/WP.

## 2. Ma trận vai trò mặc định
| Role | Trách nhiệm | Quyền mặc định | Không được tự phê duyệt |
|---|---|---|---|
| AI-01 Xu — Orchestrator/CEO | Intake, phân rã WP, điều phối, quyết định thường nhật trong scope, tổng hợp và handoff | Đọc hồ sơ; tạo assignment; sửa tài liệu trong scope; gọi adapter được cấp quyền | Acceptance cuối, release, policy/security, destructive migration |
| AI-02 Ka — CSA/Architecture reviewer | Phản biện kiến trúc, hợp đồng, rủi ro và khả năng mở rộng | Read/review; đề xuất ADR | Tự merge hoặc tự duyệt thiết kế do mình là tác giả |
| AI-03 Cla — CTO/Code-Debug | Phân tích lỗi, đề xuất/sửa code khi được giao | Chỉ repository/path/branch được cấp | Tự xác nhận QE độc lập |
| AI-04 Kha — Strategy/Product | Phân tích sản phẩm, yêu cầu, trade-off | Read/recommend; draft requirements | Thay đổi mục tiêu/scope đã duyệt |
| AI-05 Qw — Member (QE/QA role superseded) | Thành viên AI-05 Qw được giữ trong stable roster; vai trò QE/QA mặc định đã được chuyển sang AI-06 Go theo D70-026 | Chỉ capability/quyền được xác minh và cấp riêng theo assignment | Không tự nhận QE/QA mặc định; không suy diễn quyền truy cập |
| AI-06 Go — CFO/Cost Analyst + QE/QA | CFO/Cost Analyst và QE/QA mặc định duy nhất trên toàn bộ Work; chịu trách nhiệm kiểm thử độc lập, review, phân loại defect, xác minh evidence, đồng thời phân tích chi phí, ngân sách và hiệu quả | Read/test; ghi kết quả QE/QA; đọc cost data được cấp và đề xuất | Sửa kết quả để biến FAIL thành PASS; tự accept/release; phê duyệt chi phí/đăng ký dịch vụ mới |
| AI-07 Co — Coder Assistant | Hỗ trợ code/debug theo WP | Quyền giới hạn theo assignment | Merge/release/accept |
| AI-08 Qc — Qwen Coder | Thực thi code/UI/backend theo assignment và capability thực tế | GitHub/repository nếu đã kết nối và được cấp | Không được giả định có MCP/Sandbox; không QE độc lập |
| La — Dola AI | Adapter hỗ trợ theo nhiệm vụ được xác minh | Chỉ quyền được kiểm tra thực tế | Không suy diễn model/backend/capability chưa xác minh |
| An — Human Tester | Kiểm thử thao tác và nghiệm thu kỹ thuật được phân công | Test environment và evidence capture | Không thay quyền Product Owner |

## 3. Kiểm tra capability trước khi giao
Với mỗi agent/adapter, ghi:
- AI/adapter ID, provider/product, model/version nếu có bằng chứng.
- Kênh truy cập thật: ChatGPT, GitHub, MCP, Sandbox, local runtime, connector.
- Phép thử capability cụ thể và kết quả quan sát.
- Permission scope, read/write/execute, Work/repository/path.
- Giới hạn, quota/chi phí, dữ liệu được phép truy cập.
- Ngày xác minh, người xác minh, evidence ref.
Nếu chưa thử: UNKNOWN / NOT VERIFIED. Không dùng nhãn “connected” chỉ dựa trên cấu hình.

## 4. Quy tắc reviewer độc lập
- Reviewer không phải tác giả chính của deliverable được review.
- QE phải có quyền đọc source và chạy test nhưng không cần quyền sửa authoritative status.
- Gate evaluator/authority là vai trò riêng; kết quả review chỉ là đầu vào cho quyết định gate.
- Khi thiếu reviewer độc lập, ghi BLOCKED hoặc yêu cầu reviewer khác; không tự review thay.

## 5. Rà soát quyền
Quyền được cấp tối thiểu theo WP, hết hiệu lực khi WP đóng hoặc bị thu hồi. Mọi thay đổi quyền cần actor, scope, lý do, thời hạn và audit. Không chia sẻ token giữa AI; không lưu secret trong register.

## 6. Participation record
Mỗi lần tham gia ghi AI ID, assignment ID, thời điểm, input/version, action, output refs, test/evidence và trạng thái. Roster không phải participation record. Token usage chỉ ghi khi có dữ liệu đo được; nếu không, UNKNOWN.

## 7. Xung đột vai trò
Nếu cùng agent vừa thực thi vừa review, phải chỉ định reviewer độc lập khác. Nếu không có, kết quả chỉ là self-check, không đủ cho gate PASS.

## 8. Stable identity mapping — Decision D70-024 (2026-11-21)
Theo quyết định trực tiếp của Vinh ghi tại D70-024:
- AI-06 = Go — CFO / Cost Analyst.
- AI-07 = Co — Coder Assistant.
- AI-08 = Qc — Qwen Coder.
- AI-05 = Qw — stable roster identity; vai trò QE/QA mặc định đã được chuyển sang AI-06 theo D70-026.
- AI-06 = Go — CFO/Cost Analyst + QE/QA mặc định duy nhất toàn HQTT.
Mapping này thay thế các mapping lịch sử mâu thuẫn trong DOC-010 v1.1 và DOC-025 v1.3. Không xóa hoặc viết lại lịch sử; các bản cũ được giữ làm evidence lịch sử và không còn là nguồn áp dụng cho stable ID hiện hành.
- AI ID chỉ là stable roster identifier. Không chứng minh provider session, GitHub login, runtime principal, permission, dispatch/ACK hoặc capability thực tế.
- Theo D70-026, AI-06 Go là QE/QA mặc định duy nhất toàn HQTT và đồng thời giữ CFO/Cost Analyst. AI-05 Qw vẫn là thành viên trong stable roster nhưng không còn giữ vai trò QE/QA mặc định.
- Go không tự review deliverable do chính mình thực hiện; khi có xung đột tác giả/thực thi phải chỉ định reviewer độc lập khác.
- Phân công owner/reviewer ở từng Work/WP chỉ xác định trách nhiệm cho deliverable cụ thể, không phải điều kiện phát sinh vai trò mặc định và không thu hẹp vai trò của thành viên còn lại.
- Quyền kỹ thuật GitHub/repository/MCP/Sandbox/runtime, login, token và principal vẫn deny-by-default; cần xác minh và cấp riêng. Vai trò nghiệp vụ QE/QA không tự tạo quyền truy cập hệ thống.


## 9. Vai trò kép Go — Decision D70-025 (2026-11-21) — HISTORICAL / SUPERSEDED BY D70-026
D70-025 từng xác lập Go giữ CFO + QE/QA và Qw tiếp tục QE/QA đồng thời. Theo quyết định mới hơn D70-026, phần “Go và Qw cùng giữ QE/QA mặc định” đã bị thay thế: Go hiện là QE/QA mặc định duy nhất toàn HQTT; Qw không còn vai trò QE/QA mặc định. D70-025 được giữ nguyên làm lịch sử, không còn là authority hiện hành cho phân công QE/QA. Các ranh giới về quyền kỹ thuật, login, token và runtime principal vẫn giữ nguyên.


## 10. Vai trò QE/QA mặc định của Go thay Qw — Decision D70-026 (2026-11-21)
Theo chỉ thị trực tiếp mới nhất của Vinh, AI-06 Go thay AI-05 Qw làm thành viên QE/QA mặc định duy nhất của HQTT, áp dụng toàn bộ Work. Go giữ đồng thời vai trò CFO/Cost Analyst. Qw không còn giữ vai trò QE/QA mặc định trong roster hiện hành. D70-026 supersedes phần vai trò QE/QA đồng thời của Go và Qw tại D70-025; D70-025 vẫn là lịch sử quyết định đã từng có hiệu lực, không xóa hoặc viết lại. D70-024 stable identity mapping vẫn giữ nguyên: AI-05 Qw, AI-06 Go, AI-07 Co, AI-08 Qc. Phân công QE/QA owner/reviewer cụ thể theo Work/WP mặc định thuộc Go, trừ khi Vinh có quyết định mới.

**Ranh giới:** Vai trò nghiệp vụ QE/QA toàn HQTT được giao cho Go; không tự động tạo GitHub login, token, runtime principal, collaborator permission hoặc quyền MCP/Sandbox. Go không tự review deliverable do chính mình thực hiện; phải có reviewer độc lập khác. Không xóa Qw khỏi lịch sử hay stable roster ID AI-05; chỉ thay đổi vai trò hiện hành.
