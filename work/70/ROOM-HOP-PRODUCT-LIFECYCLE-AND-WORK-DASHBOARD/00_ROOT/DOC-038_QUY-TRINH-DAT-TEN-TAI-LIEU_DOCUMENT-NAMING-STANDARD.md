# QUY TRÌNH ĐẶT TÊN TÀI LIỆU / DOCUMENT NAMING STANDARD
- **STT / Document ID:** DOC-038
- **Priority / Mức ưu tiên:** P0 — BẮT BUỘC TRƯỚC
- **Read order / Thứ tự đọc:** 8
- **Depends on / Phụ thuộc:** DOC-001; DOC-002; DOC-003; DOC-033
- **Status / Trạng thái:** ACTIVE
- **Version / Updated:** 1.0 / 2026-10-30
- **Owner / Phụ trách:** Xu / AI-01
- **Authority / Thẩm quyền:** Vinh

## 1. Mục đích / Purpose
Chuẩn hóa tên của mọi tài liệu, hồ sơ, bản vẽ, mô hình, biểu mẫu và tài liệu bàn giao trong tất cả ROOM-HOP Works. Tên phải dễ đọc với con người, dễ nhận diện với AI và tương thích Windows, Git, GitHub, Sandbox.

Standardize names for every document, record, drawing, model, template and handoff artifact across ROOM-HOP Works. Names must be human-readable, AI-discoverable and compatible with Windows, Git, GitHub and Sandbox.

## 2. Nguyên tắc bắt buộc / Mandatory principles
1. Tiếng Việt trước, tiếng Anh sau trong tên hiển thị và tên file.
2. Mỗi tài liệu chính thức có một DOC ID duy nhất, ổn định, không tái sử dụng.
3. DOC ID, Priority P0–P3 và Read order là ba trường riêng biệt.
4. Tên file dùng ASCII không dấu; chỉ dùng chữ A–Z, số 0–9, gạch dưới và gạch nối; không khoảng trắng.
5. Tên ngắn, có nghĩa, mô tả đúng loại và chủ đề; cấm tên mơ hồ như FINAL, NEW, FIXED, LATEST, COPY.
6. Tên file chuẩn không đổi theo mỗi lần cập nhật. Phiên bản nằm trong metadata và lịch sử Git.
7. Một tài liệu chỉ có một đường dẫn chuẩn được khai báo trong Document Register.
8. Không tự ý đổi tên tài liệu cũ; phải có kế hoạch cập nhật toàn bộ liên kết và kiểm chứng.

## 3. Mẫu tên file chuẩn / Canonical filename pattern
DOC-NNN_TEN-TIENG-VIET-KHONG-DAU_ENGLISH-DOCUMENT-NAME.ext

- DOC-NNN: mã tài liệu ổn định, ví dụ DOC-038.
- TEN-TIENG-VIET-KHONG-DAU: tiếng Việt viết hoa, bỏ dấu, các từ nối bằng gạch ngang.
- ENGLISH-DOCUMENT-NAME: cụm tiếng Anh tương đương, viết hoa, nối bằng gạch ngang.
- ext: phần mở rộng đúng loại file như md, pdf, docx, xlsx, drawio, svg, json.

Ví dụ:
- DOC-034_BIEN-BAN_HOP-MINUTES.md
- DOC-035_NHAT-KY-THI-CONG_WORK-EXECUTION-LOG.md
- DOC-038_QUY-TRINH-DAT-TEN-TAI-LIEU_DOCUMENT-NAMING-STANDARD.md
- DOC-041_KIEN-TRUC-HE-THONG_SYSTEM-ARCHITECTURE.drawio
- DOC-042_MO-HINH-DU-LIEU_DATA-MODEL.svg
- DOC-043_KE-HOACH-KIEM-THU_TEST-PLAN.xlsx

Không cần lặp Work ID trong tên file khi file đã nằm trong thư mục Work riêng. Khi xuất file ra ngoài Work và có nguy cơ trùng tên, thêm Work ID theo quy tắc cấp mã đã khai báo.

## 4. Tiêu đề và metadata / Internal title and metadata
Tiêu đề đầu tài liệu theo mẫu:
# TÊN TÀI LIỆU TIẾNG VIỆT / ENGLISH DOCUMENT TITLE

Ngay dưới tiêu đề phải có:
- STT / Document ID
- Priority / Mức ưu tiên
- Read order / Thứ tự đọc
- Depends on / Phụ thuộc
- Status / Trạng thái
- Version / Phiên bản
- Updated / Ngày cập nhật

Với JSON, YAML hoặc schema, không chèn metadata làm sai cú pháp; khai báo trong schema hoặc Document Register. Với bản vẽ/mô hình nhị phân, metadata nằm trong title block, trang thông tin hoặc sidecar manifest được đăng ký.

## 5. Quy tắc theo loại tài liệu / Naming by artifact type
| Loại / Type | Quy tắc tên / Naming pattern |
|---|---|
| Biên bản / Minutes | DOC-NNN_BIEN-BAN_CHU-DE_MINUTES_TOPIC |
| Kế hoạch / Plan | DOC-NNN_KE-HOACH_CHU-DE_PLAN_TOPIC |
| Nhật ký thi công / Execution log | DOC-NNN_NHAT-KY-THI-CONG_PHAM-VI_WORK-EXECUTION-LOG_SCOPE |
| Bản vẽ kiến trúc / Architecture drawing | DOC-NNN_BAN-VE-KIEN-TRUC_CHU-DE_ARCHITECTURE-TOPIC |
| Mô hình dữ liệu / Data model | DOC-NNN_MO-HINH-DU-LIEU_CHU-DE_DATA-MODEL-TOPIC |
| Yêu cầu / Requirements | DOC-NNN_YEU-CAU-SAN-PHAM_PRODUCT-REQUIREMENTS |
| Kiểm thử / Test | DOC-NNN_KE-HOACH-KIEM-THU_TEST-PLAN |
| Báo cáo / Report | DOC-NNN_BAO-CAO_CHU-DE_REPORT_TOPIC |

Với biên bản hoặc nhật ký định kỳ, có thể thêm ngày ISO YYYY-MM-DD ở cuối phần chủ đề. Ngày không thay thế DOC ID. Evidence dùng Evidence ID riêng nếu hệ thống đã định nghĩa loại ID đó. Source code tuân theo quy ước ngôn ngữ/framework và được quản lý như Artifact, không ép dùng DOC prefix.

## 6. Phiên bản và trạng thái / Versioning and status
- Phiên bản tài liệu đang hoạt động nằm trong metadata, ví dụ Version 1.2.
- Bản xuất hoặc lưu trữ bất biến có thể thêm hậu tố v1.2_YYYYMMDD trước phần mở rộng.
- Không dùng final, final2, new, latest hoặc copy để thay cho quản lý phiên bản.
- Cập nhật cùng một tài liệu thì giữ DOC ID; tài liệu độc lập mới phải cấp DOC ID mới.
- Tài liệu SUPERSEDED phải chỉ rõ tài liệu thay thế và không tiếp tục được dùng làm nguồn hiện hành.

## 7. Quy trình tạo tài liệu mới / New document workflow
1. Tra Document Register để tìm tài liệu tương đương; ưu tiên cập nhật tài liệu chuẩn hiện có.
2. Xác định loại tài liệu, mục đích, chủ sở hữu và thư mục chuẩn.
3. Cấp DOC ID tiếp theo chưa sử dụng; không đoán số, không tái sử dụng ID.
4. Đặt tên tiếng Việt trước, tiếng Anh sau theo mẫu.
5. Thêm tiêu đề song ngữ và metadata bắt buộc.
6. Đăng ký Priority, Read order, path, dependencies, status và mục đích trong Document Register.
7. Cập nhật liên kết liên quan trong Manifest, kế hoạch, biên bản hoặc mapping.
8. Ghi nhận việc tạo/cập nhật trong Nhật ký thi công.
9. Đọc lại từ GitHub và Sandbox; đối chiếu nội dung và đường dẫn.
10. Chỉ báo PASS khi có đủ bằng chứng kiểm tra.

## 8. Đổi tên tài liệu hiện hữu / Legacy rename workflow
Không đổi tên hàng loạt ngay khi ban hành chuẩn. Mỗi đợt đổi tên phải:
1. Lập bảng đường dẫn cũ → đường dẫn mới.
2. Kiểm tra DOC ID, nội dung, lịch sử, nhánh và tất cả tham chiếu.
3. Có backup/commit khôi phục được.
4. Cập nhật Document Register, Manifest, liên kết nội bộ, script, Dashboard và mapping.
5. Đổi tên theo cách giữ lịch sử Git khi có thể.
6. Đọc lại đường dẫn mới và xác nhận không còn tham chiếu hỏng.
7. Ghi biên bản, nhật ký, bằng chứng; yêu cầu QE độc lập kiểm tra.
8. Không xóa bản cũ nếu chưa chứng minh đường dẫn mới đầy đủ và chính xác.

## 9. Ngoại lệ / Exemptions
- Tên file bắt buộc bởi framework, package manager, hệ điều hành hoặc giao thức: giữ nguyên để bảo đảm tương thích và ghi chú trong Register.
- Source code, file lock, migration ID, build asset: theo quy ước kỹ thuật riêng.
- File nhận từ bên ngoài: giữ bản gốc bất biến; bản làm việc phải ghi nguồn.
- File tạm: đánh dấu TEMP, ghi phạm vi và nguồn; không coi là tài liệu chuẩn nếu chưa được đăng ký.

## 10. Kiểm tra tuân thủ / Compliance checklist
- Có DOC ID duy nhất, ổn định.
- Tiếng Việt đứng trước tiếng Anh.
- Filename ASCII, không dấu, không khoảng trắng.
- Đúng mẫu DOC-NNN_TEN-VIET_ENGLISH-NAME.ext.
- Có tiêu đề song ngữ và metadata bắt buộc.
- Có một đường dẫn chuẩn trong Document Register.
- Priority và Read order khai báo riêng.
- Đã kiểm tra trùng lặp, phụ thuộc và liên kết.
- Đã xác minh nội dung sau đồng bộ.

Không đạt điều kiện bắt buộc thì trạng thái DRAFT hoặc NOT VERIFIED; không được tuyên bố PASS.

## 11. Quyền thay đổi / Change authority
Vinh là thẩm quyền cuối cùng đối với chuẩn đặt tên. Xu duy trì và triển khai các thay đổi thường lệ trong phạm vi đã thống nhất. Mọi ngoại lệ phải có lý do, phạm vi, người duyệt và thời hạn rà soát.

**English summary:** Use Vietnamese-first bilingual titles and filenames, stable DOC IDs, ASCII filenames, one canonical path per document, metadata-based versioning and controlled legacy renames.
