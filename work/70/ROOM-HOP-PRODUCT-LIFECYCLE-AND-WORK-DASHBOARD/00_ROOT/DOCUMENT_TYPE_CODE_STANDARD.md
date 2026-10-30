# QUY CHUẨN MÃ LOẠI VĂN BẢN / DOCUMENT TYPE CODE STANDARD
- **STT / Document ID:** DOC-039
- **Priority / Mức ưu tiên:** P0 — BẮT BUỘC TRƯỚC
- **Read order / Thứ tự đọc:** 9
- **Depends on / Phụ thuộc:** DOC-001; DOC-006; DOC-033; DOC-034; DOC-038
- **Status / Trạng thái:** ACTIVE
- **Version / Updated:** 1.0 / 2026-10-30
- **Owner / Phụ trách:** Xu / AI-01
- **Authority / Thẩm quyền:** Vinh

## 1. Mục đích / Purpose
Thiết lập hệ mã thống nhất để phân loại, cấp số, tra cứu, liên kết và lưu vết văn bản chính thức trong mọi ROOM-HOP Work. Áp dụng cho biên bản, quyết định, lệnh/chỉ thị, phụ lục và các hồ sơ nghiệp vụ liên quan.

## 2. Hai lớp mã bắt buộc phải phân biệt
1. DOC-ID (DOC-NNN): định danh tài liệu trong Document Register. DOC-ID duy nhất, ổn định, không tái sử dụng; dùng quản lý vòng đời và đường dẫn tài liệu.
2. Mã văn bản nghiệp vụ: mã phân loại + Work ID + ngày phát hành + số thứ tự. Mã này nhận diện một văn bản/hồ sơ phát hành cụ thể.

Hai mã không thay thế nhau. Tài liệu chính thức có DOC-ID phải có mã loại văn bản khi thuộc một loại trong danh mục tại mục 3. Tài liệu kỹ thuật hoặc tài liệu tham khảo không nhất thiết có mã văn bản nghiệp vụ.

## 3. Danh mục mã loại văn bản chuẩn
| Mã | Loại văn bản | Phạm vi sử dụng |
|---|---|---|
| BB | Biên bản | Biên bản họp, làm việc, nghiệm thu, bàn giao |
| QD | Quyết định | Quyết định đã được người có thẩm quyền phê duyệt |
| LENH | Lệnh / Chỉ thị | Yêu cầu điều hành có tính bắt buộc, xác định người thực hiện và thời hạn/phạm vi |
| PL | Phụ lục | Tài liệu bổ sung, đính kèm và dẫn chiếu văn bản gốc |
| KH | Kế hoạch | Kế hoạch công việc, triển khai, kiểm thử, di chuyển |
| YC | Yêu cầu | Yêu cầu sản phẩm, nghiệp vụ, kỹ thuật hoặc thay đổi |
| TK | Thiết kế | Kiến trúc, thiết kế hệ thống, bản vẽ, mô hình |
| QT | Quy trình / Quy chuẩn | Quy định cách thức thực hiện hoặc tiêu chuẩn bắt buộc |
| HD | Hướng dẫn | Hướng dẫn thao tác, vận hành hoặc sử dụng |
| BC | Báo cáo | Báo cáo phân tích, tiến độ, kiểm tra, tổng kết |
| BM | Biểu mẫu | Mẫu trống để ghi nhận dữ liệu hoặc kết quả |
| HS | Hồ sơ | Bộ hồ sơ tổng hợp nhiều văn bản/tài liệu có liên kết |
| TB | Thông báo | Thông tin chính thức, không mặc nhiên tạo quyền phê duyệt hay mệnh lệnh |
| CV | Công văn / Trao đổi chính thức | Văn bản trao đổi chính thức với bên ngoài hoặc đơn vị khác |

Không tự tạo mã viết tắt mới. Nếu loại văn bản chưa có, đề xuất mã và chỉ áp dụng sau khi Vinh phê duyệt, cập nhật quy chuẩn và danh mục mã.

## 4. Cấu trúc mã văn bản / Document code format
Mẫu chuẩn:

    MA-WORKID-YYYYMMDD-NNN

Trong đó:
- MA: mã loại tại mục 3.
- WORKID: mã Work, ví dụ W70.
- YYYYMMDD: ngày phát hành theo giờ Việt Nam.
- NNN: số thứ tự 3 chữ số, cấp tuần tự riêng cho từng mã loại trong từng Work và từng ngày; bắt đầu từ 001.

Ví dụ:
- BB-W70-20261030-001
- QD-W70-20261030-001
- LENH-W70-20261030-001
- PL-W70-20261030-001

Mỗi tổ hợp mã loại + Work + ngày có bộ đếm riêng. Không cấp trùng, không tái sử dụng số đã cấp, kể cả khi văn bản bị hủy hoặc thu hồi. Số đã cấp phải được ghi vào sổ đăng ký văn bản.

## 5. Quy tắc liên kết văn bản
- Phụ lục PL phải ghi rõ mã văn bản gốc, tên văn bản gốc và quan hệ (đính kèm/bổ sung/sửa đổi).
- Quyết định QD phải ghi người/quyền phê duyệt, phạm vi, hiệu lực và căn cứ.
- Lệnh LENH phải ghi người ban hành, người/đơn vị nhận lệnh, nội dung yêu cầu, phạm vi, hạn hoàn thành và điều kiện xác nhận kết quả.
- Biên bản BB ghi thành phần, thời gian, nội dung, kết luận, ý kiến khác biệt và người xác nhận. Biên bản không tự động trở thành quyết định nếu không có nội dung phê duyệt hợp lệ.
- Báo cáo BC phải chỉ rõ kỳ báo cáo, nguồn dữ liệu và thời điểm chốt.
- Một văn bản có thể tham chiếu nhiều văn bản khác; không nhúng mã của văn bản cha vào mã con để tránh phụ thuộc cấu trúc.

## 6. DOC-ID, mã văn bản và tên file
Đối với văn bản phát hành chính thức, tên file theo mẫu:

    DOC-NNN_MA-VAN-BAN_TEN-VIET-KHONG-DAU_ENGLISH-NAME.ext

Ví dụ:
- DOC-034_BB-BIEN-BAN_HOP-WORK-70_WORK-70-MEETING-MINUTES.md
- DOC-040_QD-QUYET-DINH_PHE-DUYET-QUY-CHUAN_APPROVAL-DECISION.md
- DOC-041_PL-PHU-LUC_DANH-MUC-MA-VAN-BAN_DOCUMENT-CODE-APPENDIX.md

Tên file vẫn phải tuân thủ DOC-038: tiếng Việt trước, tiếng Anh sau, ASCII không dấu. Mã văn bản nghiệp vụ phải xuất hiện trong phần đầu nội dung và metadata. Với tài liệu chưa phát hành hoặc tài liệu kỹ thuật không thuộc danh mục, dùng quy tắc DOC-038 mà không tự gắn mã loại.

## 7. Sổ đăng ký và cấp mã
Mỗi Work duy trì một Sổ đăng ký văn bản do Document Register hoặc sổ con được đăng ký quản lý. Tối thiểu gồm:
- Mã văn bản; DOC-ID; loại; tiêu đề.
- Ngày phát hành; người soạn; người ban hành/phê duyệt.
- Văn bản liên quan/văn bản gốc; trạng thái.
- Đường dẫn chuẩn; phiên bản; bằng chứng phát hành/duyệt.

Quy trình cấp mã:
1. Xác định đây có phải văn bản chính thức thuộc danh mục không.
2. Kiểm tra sổ đăng ký để tránh trùng mã.
3. Cấp DOC-ID mới nếu là tài liệu mới và cấp mã văn bản theo đúng loại.
4. Ghi mã ở đầu tài liệu, tên file, metadata và sổ đăng ký.
5. Kiểm tra thẩm quyền, xác nhận, liên kết phụ lục và trạng thái.
6. Ghi nhận phát hành/cập nhật trong biên bản hoặc nhật ký thi công.
7. Đọc lại từ GitHub/Sandbox và xác minh liên kết trước khi báo PASS.

## 8. Trạng thái và sửa đổi
- DRAFT: dự thảo, chưa phát hành; không được trình bày như văn bản có hiệu lực.
- ISSUED: đã phát hành hợp lệ.
- EFFECTIVE: đang có hiệu lực, nếu loại văn bản có hiệu lực áp dụng.
- SUPERSEDED: đã bị văn bản mới thay thế.
- REVOKED: bị thu hồi/hủy theo thẩm quyền.
- ARCHIVED: lưu trữ, không còn dùng vận hành.

Mã đã phát hành là bất biến. Văn bản sửa đổi/thay thế được cấp mã mới và phải dẫn chiếu mã cũ. Không sửa nội dung lịch sử của văn bản đã phát hành; đính chính bằng văn bản mới hoặc phụ lục đúng thẩm quyền.

## 9. Nguyên tắc thẩm quyền
Mã số chỉ phân loại và nhận diện, không tự tạo thẩm quyền hoặc hiệu lực pháp lý. Một quyết định/lệnh chỉ được coi là đã ban hành khi có đúng chủ thể có thẩm quyền, quy trình phê duyệt và bằng chứng xác nhận theo quy định của Work/tổ chức. AI được đề xuất và chuẩn bị dự thảo; không tự nhận quyền phê duyệt thay Vinh hoặc chủ thể được ủy quyền.

## 10. Kiểm tra tuân thủ
- Mã đúng cấu trúc, đúng loại, đúng Work ID và ngày phát hành.
- Không trùng hoặc tái sử dụng số.
- Có DOC-ID và một đường dẫn chuẩn nếu là tài liệu đăng ký.
- Có người soạn và người ban hành/phê duyệt phù hợp.
- Phụ lục có liên kết văn bản gốc.
- Trạng thái phản ánh đúng tình trạng phát hành.
- Sổ đăng ký và nội dung file khớp nhau.

Không đủ bằng chứng về phê duyệt/phát hành thì phải ghi DRAFT hoặc NOT VERIFIED, không gắn ISSUED/EFFECTIVE và không tuyên bố PASS.

## 11. Quyền thay đổi
Vinh là thẩm quyền cuối cùng đối với danh mục mã và quy chuẩn. Xu quản lý sổ mã, cấp mã tuần tự trong phạm vi đã được phê duyệt và ghi vết mọi thay đổi.

**English summary:** Keep stable DOC IDs separate from operational document codes. Use controlled type prefixes such as BB, QD, LENH and PL, followed by Work ID, issue date and a per-type sequence number.
