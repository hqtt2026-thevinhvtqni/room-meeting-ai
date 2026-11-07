# SỔ QUYẾT ĐỊNH WORK 70 / WORK 70 DECISION LOG
- **STT / Document ID:** DOC-006
- **Priority / Mức ưu tiên:** P0
- **Read order / Thứ tự đọc:** 6
- **Depends on / Phụ thuộc:** DOC-001
- **Status / Trạng thái:** ACTIVE — CANONICAL DECISION RECORD
- **Version / Phiên bản:** 1.1
- **Updated / Cập nhật:** 2026-10-31
- **Maintainer / Quản lý:** Xu / AI-01
- **Final authority / Thẩm quyền cuối cùng:** Vinh

## 1. Mục đích
Ghi nhận các quyết định có tính ràng buộc đối với Work 70, lý do, phạm vi và trạng thái. Đây là nguồn chuẩn duy nhất cho quyết định Work-wide. Không sửa/xóa quyết định lịch sử; đính chính hoặc thay đổi bằng quyết định mới có liên kết tới quyết định trước.

## 2. Decision Log

| Decision ID | Decision / Quyết định | Rationale / Lý do | Status / Trạng thái |
|---|---|---|---|
| D70-001 | Cấu trúc cấp Work gồm 00_ROOT, 01_DISCOVER, 02_DEFINE, 03_ARCHITECT, 04_PLAN, 05_BUILD, 06_VERIFY, 06_EVIDENCE, 07_ACCEPT, 08_RELEASE, 09_OPERATE và DASHBOARD. | Tách các pha vòng đời, kho bằng chứng xuyên pha và Dashboard. | ACTIVE STANDARD v1.1 |
| D70-002 | 05_BUILD có chín thư mục con cố định: 00_ROOT, 01_ORIGINAL, 02_EXTENSION, 03_ARCHITECTURE, 04_CODE, 05_TEST, 06_EVIDENCE, 07_RELEASE và 10_AI_DEBUG_HANDOFF. | Giữ cấu trúc điều hướng kỹ thuật đã thống nhất cho Work 70. | ACTIVE STANDARD v1.1 |
| D70-003 | Hồ sơ Work Package được lập ở cấp Work; 05_BUILD ánh xạ WP tới khu vực kỹ thuật và hiện vật nguồn. | Giữ quyền lập kế hoạch ở cấp Work, không biến Build thành nguồn kế hoạch thứ hai. | ACTIVE STANDARD v1.2 |
| D70-004 | 06_EVIDENCE cấp Work là chỉ mục bằng chứng chuẩn xuyên pha; 05_BUILD/06_EVIDENCE chỉ là nơi tập kết bằng chứng Build. | Ngăn trùng lặp quyền sở hữu bằng chứng. | ACTIVE STANDARD v1.2 |
| D70-005 | Core là nguồn dữ liệu có thẩm quyền; Dashboard chỉ đọc; PRODUCT_STATUS.json cục bộ chỉ là ảnh chụp trạng thái. | Ngăn hình thành nguồn dữ liệu thứ hai và tuyên bố trạng thái trực tiếp không có căn cứ. | ACTIVE STANDARD |
| D70-006 | Không tái sử dụng Meeting.save_artifact làm cơ chế lưu trữ/xuất dữ liệu Work tổng quát. | Hàm hiện tại thuộc phạm vi Meeting và gắn với hoàn tất Meeting; router HTTP đã rà soát chỉ công khai các route Meeting. | DECIDED — GAP DOCUMENTED |
| D70-007 | Thiết kế lưu trữ/xuất dữ liệu giai đoạn đầu tập trung JSON, CSV và Markdown cho metadata/chỉ mục; PDF/ZIP để giai đoạn sau. | Giữ phạm vi triển khai đầu tiên đủ nhỏ và có thể kiểm thử. | DESIGN ONLY |
| D70-008 | GitHub main lưu vòng đời, tài liệu gốc và Dashboard của Work 70; nhánh work/70/05-build chỉ lưu cây 05_BUILD. | Phân định phạm vi nhánh, tránh nhân bản toàn bộ Work. | ACTIVE SYNC CONTRACT |
| D70-009 | Áp dụng chung AI Project Intake & Execution Standard và một mẫu báo cáo tiếp nhận cho tất cả AI tham gia. | Ngăn khác biệt trong khám phá dự án, quản lý bằng chứng, báo cáo trạng thái và bàn giao. | ACTIVE STANDARD v1.0 — adopted by Vinh on 2026-10-30 |
| D70-010 | Mọi tài liệu Work có STT/Document ID ổn định, mức ưu tiên P0-P3 và thứ tự đọc/phụ thuộc rõ ràng trong Document Register. | Giúp AI và con người tra cứu tài liệu theo trình tự nhất quán. | ACTIVE STANDARD v1.0 — adopted by Vinh on 2026-10-30 |
| D70-011 | Mỗi Work sử dụng bốn hồ sơ phối hợp: BIÊN BẢN, KẾ HOẠCH, BẢN VẼ/MÔ HÌNH khi cần và NHẬT KÝ THI CÔNG. | Tạo bộ hồ sơ vận hành chung, tránh mỗi AI tự đặt cách ghi chép riêng. | ACTIVE STANDARD v1.0 — adopted by Vinh on 2026-10-30 |
| D70-012 | Work root sở hữu hồ sơ Work chuẩn và tài liệu gốc đã duyệt; 05_BUILD chỉ là lớp ánh xạ/điều phối kỹ thuật, không sở hữu tài liệu gốc hoặc mã nguồn sản phẩm chuẩn. | Loại bỏ nhiều nguồn chuẩn và nhầm lẫn giữa cây vòng đời Work với vùng Build. | ACTIVE STANDARD v1.0 — adopted by Vinh on 2026-10-30 |
| D70-013 | Mỗi hiện vật được ánh xạ phải chỉ rõ đường dẫn/URI nguồn chuẩn và phiên bản/commit chính xác; bản sao trong 05_BUILD chỉ là bản tạm, không có thẩm quyền. | Ngăn tham chiếu lỗi thời hoặc mơ hồ và tránh vô tình biến bản làm việc thành nguồn chuẩn. | ACTIVE STANDARD v1.0 — adopted by Vinh on 2026-10-30 |
| D70-014 | All Work documents use Vietnamese-first bilingual titles and the canonical DOC-NNN_VIETNAMESE_ENGLISH filename pattern; stable DOC IDs, ASCII filenames and controlled legacy renames are mandatory. | Makes documents readable to Vietnamese users and consistently discoverable by AI/tools without breaking existing links. | ACTIVE STANDARD v1.0 — adopted 2026-10-30 |
| D70-015 | Official records use a controlled document-type code (BB, QD, LENH, PL, KH, YC, TK, QT, HD, BC, BM, HS, TB, CV) separate from the stable DOC-ID; issue codes follow TYPE-WORKID-YYYYMMDD-NNN and are recorded in a register. | Separates document identity from operational classification and prevents ambiguous or duplicate official records. | ACTIVE STANDARD v1.0 — adopted 2026-10-30 |
| D70-016 | Sandbox relative paths are rooted at the Work 70 root without a `work/70/` prefix; GitHub repository paths retain the `work/70/` prefix. The accidental nested Sandbox tree is non-canonical and must not be used. | Prevents two competing Sandbox roots and false-positive synchronization checks. | ACTIVE PATH CONTRACT v1.0 — 2026-10-30 |

## 3. Thẩm quyền và thay đổi quyết định
Các thay đổi trọng yếu về phạm vi sản phẩm, thẩm quyền, chính sách bảo mật, chi phí định kỳ, schema chuẩn hoặc phát hành phải được Vinh quyết định. Xu được tự quyết các thay đổi triển khai thông thường, có thể đảo ngược và nằm trong phạm vi đã duyệt.

## 4. Quy tắc duy trì
1. Không xóa hoặc viết lại quyết định đã ghi nhận.
2. Quyết định thay thế phải có ID mới, nêu rõ ID bị thay thế, lý do, người có thẩm quyền và thời điểm hiệu lực.
3. Trạng thái phải phản ánh bằng chứng; DESIGN ONLY không được diễn giải thành quyết định triển khai hoặc RELEASE.
4. Mọi thay đổi phải cập nhật DOC-035 và Document Register khi có thay đổi metadata/đường dẫn.
5. Alias DECISION_LOG.md chỉ là đường dẫn tương thích; mọi chỉnh sửa thực hiện tại DOC-006.

## 5. Khôi phục lịch sử
Bản ghi D70-001 đến D70-013 được khôi phục từ nội dung GitHub lịch sử tại commit `27ed78444bf4a7ee705b0362e3b9359fc7397b3a`. Các quyết định D70-014 đến D70-016 được khôi phục nguyên văn từ `00_ROOT/DECISION_LOG.md` tại commit `6555a9ab0eaea1130e0e9dc12344595c0299e0a0`. Nội dung quyết định và trạng thái lịch sử được giữ nguyên. Đối chiếu hoàn tất ngày 2026-10-31: DOC-039 v1.2 và DOC-040 v1.4 hiện quy định danh mục đầy đủ 22 mã; 14 mã được liệt kê trong D70-015 đều còn nằm trong danh mục hiện hành, 8 mã bổ sung được chuẩn hóa ở DOC-039. Vì vậy D70-015 được giữ nguyên như quyết định lịch sử về nguyên tắc; DOC-039/DOC-040 là danh mục chi tiết hiện hành. Không có mã lịch sử nào bị xóa hoặc tái diễn giải.


## 6. Addendum — quyết định D70-017 (2026-11-02)
| Decision ID | Decision / Quyết định | Rationale / Lý do | Status / Trạng thái |
|---|---|---|---|
| D70-017 | Chọn Hybrid AI Dispatch: ROOM-HOP quản lý Work/WP/assignment/quyền/audit/evidence; AI tiếp tục trong conversation/session hiện có qua adapter được xác minh; ưu tiên native permission và manual session handoff, hạn chế API; không tự tạo API cost. | Giữ continuity của phiên AI, tránh phát sinh chi phí không cần thiết, đồng thời đưa giao việc/ACK/tiến độ/kết quả về một luồng có kiểm soát. | DECIDED BY VINH — TARGET ARCHITECTURE; IMPLEMENTATION NOT AUTHORIZED |

Ràng buộc: DOC-064/065 là thiết kế; DOC-066 là kế hoạch. Không suy diễn connector hoạt động, ACK hoặc dispatch tự động. Không tạo API key/phí mới; không mở BUILD khi Work Entry chưa đạt.


## 7. Quyết định D70-018 — Ủy quyền điều phối và hoàn thiện Work 70 (2026-11-02)
| Decision ID | Decision / Quyết định | Rationale / Lý do | Status / Trạng thái |
|---|---|---|---|
| D70-018 | Theo chỉ thị trực tiếp của Vinh ngày 2026-11-02, Xu / AI-01 được toàn quyền điều phối và quyết định các công việc cần thiết để hoàn thiện Work 70 trong phạm vi Work 70; không yêu cầu Vinh duyệt từng bước. Xu được quyết định các thay đổi kế hoạch, tài liệu, phân rã WP/SD và triển khai kỹ thuật thông thường có thể đảo ngược, với điều kiện ghi nhật ký và có bằng chứng. | Giảm thời gian tham gia vận hành của Product Owner, duy trì một đầu mối chịu trách nhiệm đầu-cuối và tránh chờ duyệt các bước tác nghiệp thông thường. | ACTIVE — DELEGATED EXECUTION AUTHORITY |

**Ranh giới bắt buộc:** D70-018 không miễn trừ Work Entry/G0–G5, không tự tạo quyền cho AI khác, không xác nhận ACK, không cho phép giả lập danh tính/ủy quyền, không cho phép phát sinh API cost hoặc secret mới, không cho phép sửa ngoài Work 70, không thay thế độc lập QE, và không cho phép Xu tự nghiệm thu cuối cùng hoặc tự phát hành. Core vẫn là nguồn dữ liệu có thẩm quyền; mọi thay đổi phải fail-closed khi thiếu identity/permission/evidence. Những việc thuộc quyền riêng của Vinh theo chính sách sản phẩm, bảo mật, chi phí định kỳ và phát hành cuối cùng vẫn được bảo lưu.


## 8. Quyết định D70-019 — Bổ sung kho tri thức công nghệ và năng lực AI (2026-11-07)
| Decision ID | Decision / Quyết định | Rationale / Lý do | Status / Trạng thái |
|---|---|---|---|
| D70-019 | Bổ sung vào Work 70 một lớp quản trị tri thức dùng chung về công nghệ AI, taxonomy, capability registry và liên kết tới các Work ứng dụng; lấy DOC-086 làm kiến trúc baseline. Không tạo Work mới. | Tránh phân tán kiến thức công nghệ; phân biệt họ công nghệ, mô hình, năng lực đã kiểm chứng và ứng dụng thực tế; giúp các Work tái sử dụng tri thức nhưng giữ quyền sở hữu và kiểm thử tại từng Work. | APPROVED BY VINH — KNOWLEDGE ARCHITECTURE BASELINE; REGISTRY IMPLEMENTATION NOT STARTED |

Phạm vi phê duyệt: tài liệu kiến trúc và phân loại tri thức trong Work 70. Không phê duyệt tự động triển khai database/API/UI, phát sinh API cost, tích hợp model/provider, thay đổi Work 75/76/103/26/29, hoặc tuyên bố capability VERIFIED. Mọi năng lực phải có model/version, phương pháp test và evidence; UNKNOWN không phải PASS.


## 9. Quyết định D70-020 — Một định danh, một loại văn bản, một nguồn canonical (2026-11-07)
| Decision ID | Decision / Quyết định | Rationale / Lý do | Status / Trạng thái |
|---|---|---|---|
| D70-020 | Theo chỉ thị trực tiếp của Vinh, mỗi văn bản lưu hành chính thức trong Work chỉ có một DOC-ID, một mã văn bản thuộc đúng một loại đã quy định, một canonical path và một bản nội dung có thẩm quyền. DOC-055 là register duy nhất cho DOC-ID/path; DOC-039 là chuẩn loại văn bản; DOC-040 là sổ cấp mã nghiệp vụ; DOC-034 và DOC-035 lần lượt là sổ biên bản và nhật ký duy nhất. Không tạo nguồn lạ, register song song, tài liệu trùng nội dung hoặc bản sao có thẩm quyền. AI phải dừng và báo Xu khi phát hiện xung đột; không tự chọn hoặc tự phát sinh mã/loại/nguồn. | Ngăn AI mới và người vận hành hiểu nhầm, tránh nhiều nguồn sự thật, trùng số, sai loại và quyết định dựa trên tài liệu không có thẩm quyền. | APPROVED BY VINH — ACTIVE WORK 70 DOCUMENT CONTROL RULE |

**Ranh giới:** Quyết định này củng cố và áp dụng các chuẩn DOC-033/038/039/040/055/056 hiện có; không tạo loại văn bản mới, không tạo register mới, không tự động cho phép xóa lịch sử hoặc tài liệu đang có tham chiếu. Di trú/xóa alias phải theo DOC-056 và có bằng chứng.


## 8. Quyết định D70-021 — Tách tên kho Evidence khỏi số thứ tự phase (2026-11-07)
| Decision ID | Decision / Quyết định | Rationale / Lý do | Status / Trạng thái |
|---|---|---|---|
| D70-021 | Đổi tên thư mục bằng chứng xuyên pha cấp Work từ `06_EVIDENCE/` thành `EVIDENCE/`; giữ `06_VERIFY/` là phase 06; giữ `05_BUILD/06_EVIDENCE/` là staging kỹ thuật. | Tránh hai thư mục cấp Work cùng mang tiền tố 06, giúp AI/con người phân biệt phase 06 với kho evidence xuyên phase, không thay đổi ownership hoặc DOC-ID. | ACTIVE STANDARD — MIGRATION IN PROGRESS; old path non-canonical |

D70-021 supersedes only the top-level folder-name portion of D70-001 and D70-004. It does not change the 05_BUILD child directory set or the canonical evidence ownership rule. New artifacts and references use `EVIDENCE/`; old top-level `06_EVIDENCE/` remains compatibility-only until link reconciliation and QE permit retirement. No historical decision text is rewritten.
