# HQTT AI Role Catalog v1.0
## Danh mục vai trò AI dùng chung cho HQTT AI / ROOM-HOP

- Work sở hữu chuẩn: Work 50 — HQTT AI Product Delivery Standard (APDS)
- Người quyết định/phê duyệt: Vinh
- Điều phối: Xu (AI-01)
- Ngày lập: 2026-10-21 (UTC+07:00)
- Trạng thái: PROPOSED — đề xuất, chưa có hiệu lực bắt buộc toàn HQTT
- Phiên bản: 1.0

## 1. Mục đích

Chuẩn hóa danh mục vị trí chuyên môn AI dùng chung. Mỗi sản phẩm/Work chọn các vai trò phù hợp theo phạm vi, rủi ro và quy mô; không bắt buộc tạo một AI riêng cho mỗi vai trò. Danh mục vai trò không đồng nghĩa đã có nhân sự AI đủ năng lực hoặc đã phân công thực tế.

## 2. Danh mục vai trò chuẩn

| Role ID | Vai trò | Trách nhiệm chính | Đầu ra tối thiểu |
|---|---|---|---|
| ROLE-CEO-PO | CEO / Product Owner (chủ sản phẩm) | Tầm nhìn, giá trị, phạm vi, ưu tiên, quyết định sản phẩm | Product Charter, ưu tiên, quyết định |
| ROLE-LEAD | Team Lead (trưởng nhóm) | Điều phối, chia việc, quản lý phụ thuộc và tổng hợp | Kế hoạch nhóm, phân công, báo cáo |
| ROLE-ARCH | System / Solution Architect (kiến trúc sư hệ thống/giải pháp) | Kiến trúc, ranh giới module, hợp đồng, khả năng mở rộng | Sơ đồ kiến trúc, ADR, hợp đồng |
| ROLE-DESIGN | Product / UX-UI Design (thiết kế sản phẩm/giao diện) | Nghiên cứu người dùng, luồng thao tác, thiết kế giao diện | User flows, wireframes, design spec |
| ROLE-FE | Frontend Engineer (kỹ sư giao diện) | Giao diện, trạng thái, tích hợp API và accessibility | Mã nguồn giao diện, kiểm thử |
| ROLE-BE | Backend Engineer (kỹ sư phía máy chủ) | API, nghiệp vụ, dữ liệu, tích hợp, phân quyền | API/service, schema, test |
| ROLE-QA | QA / QE (đảm bảo chất lượng/kỹ thuật chất lượng) | Chiến lược test, xác minh tiêu chí, hồi quy và báo lỗi | Test plan, kết quả, evidence, defect list |
| ROLE-DEVOPS | DevOps / SRE (triển khai/vận hành độ tin cậy) | CI/CD, môi trường, giám sát, backup, khôi phục | Pipeline, runbook, monitoring/recovery evidence |
| ROLE-ANALYTICS | Data / Product Analytics (phân tích dữ liệu/sản phẩm) | KPI, đo lường, chất lượng dữ liệu và phân tích kết quả | Metric definitions, dashboard/analysis |
| ROLE-LEGAL | Legal / Compliance (pháp lý/tuân thủ) | Giấy phép, quyền dữ liệu, riêng tư và yêu cầu tuân thủ | Compliance checklist, risk notes |
| ROLE-FINANCE | Finance / Accounting (tài chính/kế toán) | Ngân sách, chi phí model/API/hạ tầng và dự báo | Cost model, budget, variance report |
| ROLE-AUDIT | Independent Auditor (kiểm toán độc lập) | Kiểm tra truy vết, quy trình, bằng chứng và tính trung thực trạng thái | Audit report, findings, evidence links |
| ROLE-SECURITY | Security Engineer (kỹ sư bảo mật) | Threat modeling, phân quyền, kiểm thử bảo mật và xử lý rủi ro | Threat model, security findings |
| ROLE-DATA | Data Engineer / Steward (kỹ sư/quản trị dữ liệu) | Nguồn gốc, chất lượng, lưu giữ, xóa, backup và quyền sử dụng dữ liệu | Data contract, lineage, governance records |
| ROLE-AI-EVAL | AI Evaluation Engineer (kỹ sư đánh giá AI) | Bộ dữ liệu đánh giá, tiêu chí chất lượng, đo độ ổn định/ảo giác | Eval plan, dataset spec, result report |
| ROLE-RELEASE-OPS | Release / Operations Owner (phụ trách phát hành/vận hành) | Go/no-go theo phê duyệt, triển khai, rollback và bàn giao | Release checklist, runbook, handoff |
| ROLE-DOCS | Technical Writer / Knowledge Owner (tài liệu/tri thức) | Tài liệu người dùng, kỹ thuật, quyết định và nhật ký | User guide, technical docs, changelog |

## 3. Quy tắc phân công

1. Danh mục trên là danh mục vai trò chuẩn, không phải danh sách AI đã được xác thực hoặc đã sẵn sàng.
2. Mỗi Work phải lập ma trận phân công theo Role ID, AI ID/tên nhà cung cấp, người chịu trách nhiệm, người phối hợp, deliverables, acceptance criteria, quyền hạn, phụ thuộc và trạng thái.
3. Có thể kiêm nhiệm khi năng lực và quyền hạn phù hợp; ghi rõ kiêm nhiệm. Không được tạo xung đột tự kiểm tra: người viết code không tự là bằng chứng duy nhất để xác nhận chất lượng; người xây dựng không tự phê duyệt phát hành rủi ro cao.
4. Với sản phẩm nhỏ, vai trò không áp dụng có thể đánh dấu N/A kèm lý do. Vai trò bảo mật, dữ liệu, pháp lý và tài chính được kích hoạt theo rủi ro, dữ liệu và mô hình kinh doanh.
5. CEO/Product Owner, kiến trúc, QA/QE, bảo mật, kiểm toán và approver là các trách nhiệm khác nhau; không suy ra quyền phê duyệt chỉ từ chức danh.
6. Nhà cung cấp/model là thuộc tính của AI, không phải vai trò. Một provider có thể đảm nhiệm nhiều vai trò; một vai trò có thể cần nhiều AI.
7. Không cấp quyền truy cập công cụ/dữ liệu rộng hơn yêu cầu nhiệm vụ (least privilege).

## 4. Ma trận phân công theo từng sản phẩm

Dùng mẫu bảng sau trong hồ sơ sản phẩm hoặc Work:

| Role ID | Bắt buộc? | AI ID / Provider | Người chịu trách nhiệm | Người review/test | Đầu ra | Tiêu chí nghiệm thu | Quyền hạn | Trạng thái | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| ROLE-ARCH | Có/Không | Chưa phân công | Chưa phân công | Chưa phân công | Kiến trúc + hợp đồng | Review được, phụ thuộc/rủi ro ghi rõ | Đề xuất, không tự phê duyệt ngoài quyền | OPEN | Chưa có |
| ROLE-BE | Có/Không | Chưa phân công | Chưa phân công | ROLE-QA/Reviewer | Code/API/test | Test và review có bằng chứng | Theo phạm vi được giao | OPEN | Chưa có |
| ROLE-QA | Có/Không | Chưa phân công | Chưa phân công | Reviewer độc lập khi khả thi | Test plan/result | Có kết quả, môi trường, lệnh và artifact | Không tự sửa kết quả để tạo PASS | OPEN | Chưa có |
| ROLE-SECURITY | Theo rủi ro | Chưa phân công | Chưa phân công | Reviewer phù hợp | Threat model/findings | Rủi ro và cách xử lý được ghi nhận | Không tự chấp thuận ngoại lệ rủi ro cao | OPEN | Chưa có |
| ROLE-RELEASE-OPS | Có với Production | Chưa phân công | Chưa phân công | Approver có thẩm quyền | Release/handoff | Có go/no-go, rollback và bằng chứng | Thực thi theo phê duyệt | OPEN | Chưa có |

Các hàng trên là ví dụ mẫu, phải thay bằng vai trò thực tế theo sản phẩm; không phải phân công đã hoàn tất.

## 5. Trạng thái và bằng chứng

- NOT_ASSIGNED: chưa phân công.
- PLANNED: đã phân công trong kế hoạch, chưa bắt đầu.
- IN_PROGRESS: đang thực hiện.
- BLOCKED: bị chặn bởi phụ thuộc hoặc điều kiện.
- DONE: đầu ra đã được tạo.
- PASS: tiêu chí cụ thể được kiểm tra và có bằng chứng đạt.
- FAIL: kiểm tra không đạt.
- NOT_APPLICABLE: không áp dụng, phải có lý do.
- UNVERIFIED: chưa có đủ bằng chứng để kết luận.

Mỗi bản ghi công việc phải ghi AI/người thực hiện, Role ID, ngày giờ UTC+07:00, Work/Task ID, đầu ra, reviewer, kết quả và link/ID bằng chứng khi có. Không suy diễn PASS từ lời báo cáo, commit hoặc việc tệp tồn tại.

## 6. Tích hợp với APDS và dashboard

- APDS: ma trận vai trò thuộc hồ sơ governance/delivery plan của mỗi sản phẩm.
- Work: ghi vai trò chịu trách nhiệm cho từng deliverable và tiêu chí nghiệm thu.
- Dashboard: hiển thị vai trò, AI phụ trách, trạng thái, phụ thuộc, deadline nếu có, reviewer và evidence; phân biệt trạng thái báo cáo với trạng thái đã xác minh.
- Nguồn chuẩn: Work 50 quản lý danh mục; mỗi sản phẩm lưu ma trận phân công theo phiên bản danh mục. Không nhân bản định nghĩa vai trò độc lập ở từng Work.
- Hiệu lực: chỉ chuyển từ PROPOSED sang APPROVED sau quyết định rõ ràng của Vinh và cập nhật nhật ký/quyết định.

## 7. Nhật ký

- 2026-10-21 (UTC+07:00) — Xu (AI-01), điều phối Work 50: tạo bản đề xuất danh mục vai trò AI theo thống nhất với Vinh; chưa áp dụng bắt buộc toàn HQTT; chưa đồng bộ Sandbox do kết nối MCP đang lỗi.
