# ĐỀ XUẤT CHUẨN HÓA GÓI CÔNG VIỆC / WORK PACKAGE BASELINE RECONCILIATION PROPOSAL

- **STT / Document ID:** DOC-062
- **Priority:** P0
- **Read order:** 62
- **Depends on:** DOC-001; DOC-004; DOC-005; DOC-006; DOC-011; DOC-036; DOC-042; DOC-043; DOC-044; DOC-054; DOC-055; DOC-057; DOC-061
- **Status:** DRAFT — RECONCILIATION COMPLETE / PRODUCT OWNER APPROVAL PENDING / G4 NOT READY
- **Version / Updated:** 1.0 / 2026-11-01
- **Owner:** Xu / AI-01
- **Authority:** Vinh

## 1. Mục đích và giới hạn

Đối chiếu kế hoạch Work-level DOC-011 với Build Register JSON/Markdown và phân công DOC-054 để tạo một baseline WP duy nhất có thể trình Vinh xem xét.

Đây là đề xuất kế hoạch, không phải quyết định phê duyệt, không phải Work Package Registry đã được triển khai và không cấp quyền BUILD. Không thay đổi trạng thái Manifest, lifecycle gate hoặc quyền hạn của Vinh.

## 2. Thứ bậc nguồn và phát hiện

| Nguồn | Vai trò | Kết luận |
|---|---|---|
| DOC-001 Manifest | Nguồn chuẩn về phạm vi, trạng thái Work và quyền | Current phase pointer = 01_DISCOVER PLANNED; G0/G1 NOT_READY; BUILD chưa được mở |
| DOC-004 / DOC-005 | Gate và state machine | G4 là PLAN → BUILD; không thể PASS khi điều kiện tiền nhiệm và bằng chứng chưa đạt |
| DOC-011 Implementation Roadmap | Kế hoạch Work-level hiện hành | Sáu WP: WP-70-01 đến WP-70-06; đây là nguồn kế hoạch chuẩn hiện tại |
| DOC-036 Build Mapping Register | Ánh xạ và phân loại hiện vật Build | BUILD_REGISTER và schemas là candidate; chưa có canonical target/version |
| DOC-054 Parallel Assignment Order | Phân vai kỹ thuật đề xuất | Assignment ready không chứng minh agent đã ACK hoặc WP READY |
| DOC-055 Document Register | Danh mục tài liệu chuẩn | DOC-053 là Operate Execution Playbook; không phải WP register |
| DOC-061 | Đối chiếu kiến trúc runtime | DRAFT; source reconciliation không đồng nghĩa contract approval |
| 04_PLAN/WORK_PACKAGE_REGISTER.json | Đường dẫn từng được nêu trong addendum DOC-061 | NOT FOUND trong Sandbox tại lần kiểm tra 2026-11-01 |
| 05_BUILD/00_ROOT/BUILD_REGISTER.json | Hồ sơ WP ứng viên | Có 6 records; không được nâng thành canonical plan nếu chưa được phê duyệt và di trú có kiểm soát |

## 3. Baseline sáu WP đề xuất

Giữ nguyên sáu WP ID và mục tiêu cấp cao của DOC-011. Bảng dưới đây chuẩn hóa trách nhiệm và điều kiện; không tự nhận các WP đã READY.

| WP ID | Mục tiêu chuẩn hóa | Accountable owner đề xuất | Reviewer | Trạng thái quan sát từ DOC-011 | Điều kiện tiếp theo |
|---|---|---|---|---|---|
| WP-70-01 | Chuẩn Work, lifecycle, gate, record và state model | Xu / AI-01 | Qw / AI-05 | IN_PROGRESS | Reconcile DOC-001/004/005; independent review; evidence đăng ký |
| WP-70-02 | Work-level WP model, schema và 05_BUILD mapping contract | Xu / AI-01 | Qw / AI-05 | IN_PROGRESS | Chốt canonical WP source/schema, mapping; không dùng Build Register candidate như nguồn chuẩn |
| WP-70-03 | Dashboard read-only, data model, local snapshot và UI states | Xu / AI-01 | Qw / AI-05 | IN_PROGRESS | Schema validation, browser E2E local; phân biệt snapshot/sample/live |
| WP-70-04 | Core read integration discovery và verification | Xu / Core owner TBD | Qw / AI-05 | BLOCKED / NOT VERIFIED | Xác định Core owner, route thật, AuthN/AuthZ, Work scope, freshness và negative tests |
| WP-70-05 | Evidence storage và JSON/CSV/Markdown export | Xu / AI-01 | Qw / AI-05 | DESIGN ONLY | Phê duyệt Core/storage contract, retention, authorization, audit và test plan trước implementation |
| WP-70-06 | Independent verification, acceptance preparation và release readiness | Xu / AI-01 | Qw / AI-05 | PLANNED | Chỉ bắt đầu sau khi các WP phụ thuộc có implementation và evidence kiểm tra được |

### 3.1 Vai trò thực thi theo DOC-054

- Ka / AI-02: kiến trúc và hợp đồng tích hợp; DOC-061 vẫn DRAFT.
- Co / AI-07: Lifecycle Engine; chỉ triển khai khi có contract được duyệt và authorization hợp lệ.
- Vi: Core route discovery, API Adapter và Dashboard; báo capability gap, không giả lập Core live.
- Qw / AI-05: test strategy và QE độc lập; không tự sửa implementation để làm test PASS.
- Xu / AI-01: chịu trách nhiệm tích hợp, đối soát, điều phối và evidence.
- Các vai trò trên là assignment đề xuất/đã mô tả; ACK của từng AI phải có bằng chứng riêng. Không suy ra đã nhận việc từ DOC-054.

## 4. Dependencies và thứ tự triển khai

1. WP-70-01 là nền tảng governance/state.
2. WP-70-02 phụ thuộc WP-70-01; hoàn thiện canonical plan/mapping.
3. WP-70-03 phụ thuộc WP-70-01; có thể kiểm thử local bằng fixture được gắn nhãn, không được tuyên bố Core live.
4. WP-70-04 phụ thuộc WP-70-03; bị BLOCKED đến khi Core owner và route thật được xác minh.
5. WP-70-05 phụ thuộc WP-70-04; hiện chỉ DESIGN ONLY.
6. WP-70-06 phụ thuộc WP-70-01..05; Qw xác minh độc lập.

Không dùng trạng thái của Build Register candidate để ghi đè trạng thái DOC-011. Không mở các WP implementation chỉ vì đã có phân công.

## 5. G4 readiness assessment

**Kết luận: NOT READY / NOT PASS.**

Lý do:
- Manifest hiện trỏ 01_DISCOVER PLANNED, G0/G1 NOT_READY.
- Chưa có bằng chứng predecessor gates đã hoàn thành.
- DOC-061 chưa được phê duyệt.
- WP plan chưa được Product Owner phê duyệt thành baseline triển khai.
- WP owner/reviewer và dispatch ACK chưa được xác minh cho từng assignment.
- Core contract, implementation source và test evidence còn thiếu.
- Build branch đang diverged; không merge/rebase mù.

DOC-011 hiện là kế hoạch chuẩn đang có hiệu lực, nhưng việc có DOC-011 không tự chứng minh G4 PASS. DOC-062 chỉ đề xuất chuẩn hóa, không thay thế G4 evaluator hoặc quyết định của Vinh.

## 6. Quy tắc trạng thái sau khi baseline được duyệt

- Trước phê duyệt: DOC-062 = DRAFT; WP status trong đề xuất chỉ là trạng thái quan sát/đề xuất, không cấp quyền thực thi.
- Sau phê duyệt kế hoạch: WP chỉ có thể chuyển READY khi assignment đủ source, scope, permission, dependencies, acceptance criteria và evidence plan theo DOC-044/DOC-057.
- IN_PROGRESS chỉ khi có Work Entry PASS và authorization kỹ thuật phù hợp.
- DONE chỉ khi acceptance criteria được kiểm chứng và reviewer độc lập chấp nhận.
- WP DONE không tự động làm phase DONE hoặc lifecycle gate PASS.

## 7. Rủi ro và kiểm soát

| Rủi ro | Kiểm soát |
|---|---|
| Hai WP register cạnh tranh | DOC-011 là plan hiện hành; DOC-062 là đề xuất; Build Register vẫn candidate |
| Nhầm DOC-053 thành WP register | DOC-053 là Operate Playbook; DOC-055 là register tài liệu |
| Nhầm assignment với ACK | Yêu cầu phản hồi/artefact từ chính AI được giao |
| Nhầm mock/snapshot với Core live | Source mode bắt buộc, timestamp/revision và E2E evidence |
| Branch divergence làm mất thay đổi | Không merge/rebase; inventory và reconcile trước |
| Bypass Work Entry/G4 | Chỉ đọc, lập kế hoạch và remediation cho tới khi gate/authorization đạt |

## 8. Handoff / quyết định cần Product Owner

Xu trình Vinh xem xét:
1. Chấp thuận DOC-062 làm baseline WP cấp Work để thay thế phần mô tả sáu dòng hiện tại của DOC-011 sau khi cập nhật có kiểm soát; hoặc yêu cầu chỉnh sửa.
2. Xác nhận ưu tiên và phạm vi sản phẩm nếu có thay đổi so với DOC-011.
3. Không yêu cầu Vinh duyệt các thao tác kỹ thuật thường nhật; Xu tiếp tục chuẩn bị hồ sơ, đối chiếu nguồn và kiểm thử không phá hủy trong phạm vi được phép.

Cho đến khi có quyết định: DOC-062 DRAFT, G4 NOT READY, BUILD implementation NOT AUTHORIZED, RELEASE NOT RELEASED.

---
Prepared by Xu / AI-01 — 2026-11-01.
