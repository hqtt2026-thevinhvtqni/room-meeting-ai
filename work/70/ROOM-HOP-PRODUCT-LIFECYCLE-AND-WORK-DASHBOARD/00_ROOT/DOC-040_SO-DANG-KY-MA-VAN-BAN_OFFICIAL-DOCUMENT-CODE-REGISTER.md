# SỔ ĐĂNG KÝ MÃ VĂN BẢN / OFFICIAL DOCUMENT CODE REGISTER
- **STT / Document ID:** DOC-040
- **Priority / Mức ưu tiên:** P0
- **Read order / Thứ tự đọc:** 10
- **Depends on / Phụ thuộc:** DOC-001; DOC-006; DOC-039
- **Status / Trạng thái:** ACTIVE
- **Version / Updated:** 1.2 / 2026-10-30
- **Owner / Phụ trách:** Xu / AI-01
- **Authority / Thẩm quyền:** Vinh

## 1. Mục đích
Sổ duy nhất ghi nhận việc cấp, phát hành, thay thế, thu hồi và lưu trữ mã văn bản nghiệp vụ của Work 70. Quy tắc mã được định nghĩa tại DOC-039; sổ này không thay thế Document Register.

## 2. Trạng thái ban đầu
Chưa có mã nào được phát hành theo cấu trúc mới của DOC-039. Mã lịch sử có định dạng cũ được lưu riêng với trạng thái LEGACY_REFERENCE, không tính là mã mới đã cấp.

## 3. Sổ cấp mã
| STT | Mã văn bản | DOC-ID | Loại | Tiêu đề | Ngày cấp | Người soạn | Người ban hành/phê duyệt | Văn bản liên quan/gốc | Trạng thái | Đường dẫn chuẩn | Bằng chứng |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 001 | BB-70-001 | DOC-034 | BB | Biên bản thống nhất bộ hồ sơ Work và ranh giới Work / 05_BUILD | 2026-10-30 | Xu / AI-01 | Vinh (chủ trì; xác nhận tại phiên làm việc) | D70-011; D70-012; D70-013 | LEGACY_REFERENCE — mã lịch sử, không theo DOC-039 | 00_ROOT/BIEN_BAN.md | Biên bản gốc; không tái cấp mã hồi tố |
| — | — | — | — | Chưa có mã phát hành theo cấu trúc DOC-039 | — | — | — | — | EMPTY | — | — |

## 4. Quy tắc vận hành
1. Kiểm tra mã gần nhất theo đúng loại + Work ID + ngày phát hành trước khi cấp số.
2. Cấp số tiếp theo, không bỏ qua để tái sử dụng và không cấp trùng.
3. Ghi dòng đăng ký trước hoặc đồng thời với thời điểm phát hành; không ghi nhận ngược một mã chưa có bằng chứng.
4. Mã đã cấp không xóa khỏi sổ. Nếu hủy/thu hồi, giữ nguyên dòng và cập nhật trạng thái cùng bằng chứng.
5. Văn bản sửa đổi/thay thế được cấp mã mới; ghi mã văn bản cũ tại cột liên quan.
6. Cập nhật sổ này và Document Register khi thêm DOC-ID/path mới.
7. Chỉ đánh dấu ISSUED khi có bằng chứng ban hành/phê duyệt hợp lệ; nếu thiếu, giữ DRAFT hoặc NOT VERIFIED.

## 5. Kiểm tra định kỳ
- Không trùng mã.
- Mã khớp loại, Work ID, ngày và số thứ tự.
- DOC-ID và đường dẫn tồn tại trong Document Register.
- Văn bản gốc/phụ lục liên kết đúng.
- Trạng thái khớp bằng chứng thực tế.

## 6. Kiểm tra tự động
Mã nguồn kiểm tra sổ:
- `06_VERIFY/validate_official_document_codes.py` — kiểm tra mã trùng, cấu trúc mã mới theo DOC-039, ngày phát hành, loại văn bản, DOC-ID có trong Document Register và bằng chứng đối với trạng thái ISSUED/EFFECTIVE.
- `06_VERIFY/test_official_document_code_validator.py` — bộ kiểm thử các trường hợp hợp lệ, mã lịch sử, mã trùng, định dạng/ngày/số thứ tự sai, DOC-ID không tồn tại và thiếu bằng chứng phát hành.

Lệnh chạy từ Work root:
```bash
python 06_VERIFY/validate_official_document_codes.py
python -m unittest discover -s 06_VERIFY -p "test_official_document_code_validator.py"
```

Công cụ không tự cấp mã, không thay đổi sổ và không thay thế quyền phê duyệt của Vinh. Kết quả kiểm tra hiện tại trong môi trường phát triển: một dòng LEGACY_REFERENCE được nhận diện; không có mã mới được phát hành. Việc chạy lại trên Sandbox/PC và lưu evidence vẫn cần thực hiện trước khi đóng R-10.

**English summary:** This is the single issuance ledger for Work 70 operational document codes. No code is considered issued without supporting approval/issuance evidence.
