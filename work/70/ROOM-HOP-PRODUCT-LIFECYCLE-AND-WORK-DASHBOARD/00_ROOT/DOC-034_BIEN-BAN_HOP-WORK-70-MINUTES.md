# WORK 70 — BIÊN BẢN
- **STT / Document ID:** DOC-034
- **Priority:** P2
- **Read order:** 31
- **Depends on:** DOC-001; DOC-006; DOC-033
- **Status:** ACTIVE
- **Version / Updated:** 1.0 / 2026-10-30

## Quy định sử dụng
- Đây là sổ biên bản thống nhất của Work 70; mỗi phiên họp/thống nhất có một mã biên bản duy nhất.
- Ghi ngày giờ, người/AI tham gia, vấn đề, ý kiến chính, kết luận, quyết định liên quan, người chịu trách nhiệm và hành động tiếp theo.
- Quyết định có tính ràng buộc phải được ghi thêm vào DOC-006_SO-QUYET-DINH_DECISION-LOG.md; biên bản tham chiếu Decision ID, không tạo một nguồn quyết định thứ hai.
- Không ghi ý kiến chưa được thống nhất thành quyết định.
- Không sửa âm thầm biên bản đã chốt; đính chính bằng mục bổ sung có ngày giờ và lý do.

## Danh mục biên bản

**Lưu ý mã lịch sử:** `BB-70-001` là mã tham chiếu lịch sử được ghi trước khi DOC-039 có hiệu lực; không phải mã phát hành theo cấu trúc mới. Không chuyển đổi hoặc cấp lại mã này hồi tố. Biên bản mới áp dụng cấu trúc tại DOC-039 và được đăng ký trong DOC-040.

### BB-70-001 — Thống nhất bộ hồ sơ Work và ranh giới Work / 05_BUILD
- **Ngày:** 2026-10-30
- **Chủ trì:** Vinh
- **Điều phối/ghi biên bản:** Xu / AI-01
- **Thành phần khác:** Chưa ghi nhận tham gia độc lập.
- **Nội dung thống nhất:**
  1. Mỗi Work sử dụng ba hồ sơ điều hành bắt buộc: Biên bản, Kế hoạch, Nhật ký thi công.
  2. Bản vẽ/mô hình sản phẩm là hồ sơ thứ tư, áp dụng khi sản phẩm cần mô tả trực quan hoặc kỹ thuật.
  3. STT và thứ tự đọc tuân theo Document Register; AI không tự ý đánh lại hoặc đổi thứ tự.
  4. Không tự ý tạo tài liệu độc lập trùng nội dung; cập nhật hồ sơ chuẩn hoặc xin phê duyệt khi thật sự cần tài liệu mới.
  5. Work root quản lý hồ sơ gốc/chính thức; 05_BUILD là tầng ánh xạ và điều phối thi công, không phải nơi sở hữu bản gốc.
  6. Mỗi ánh xạ phải chỉ rõ nguồn chuẩn và phiên bản/commit chính xác.
  7. Không xóa, di chuyển hoặc ghi đè các file 05_BUILD hiện hữu trước khi kiểm kê và phân loại.
- **Quyết định liên quan:** D70-011, D70-012, D70-013.
- **Trạng thái:** RECORDED / ACTIVE STANDARD.
- **Hành động tiếp theo:** Xu hoàn thiện quy tắc lưu trữ, tạo mapping register, phân loại nội dung 05_BUILD và xác minh đồng bộ.



### BB-W70-20261107-001 — Biên bản điều chỉnh và khóa nguyên tắc quản lý văn bản Work 70
- **Ngày:** 2026-11-07 (giờ Việt Nam)
- **Chủ trì / thẩm quyền:** Vinh
- **Điều phối / ghi biên bản:** Xu / AI-01
- **Thành phần khác:** Không ghi nhận tham gia độc lập trong phiên này.
- **Căn cứ:** Chỉ thị trực tiếp của Vinh trong phiên làm việc ngày 2026-11-07; DOC-001; DOC-033; DOC-034; DOC-038; DOC-039; DOC-040; DOC-055; DOC-056.
- **Nội dung điều chỉnh và thống nhất:**
  1. Trong một Work, mỗi văn bản lưu hành chính thức chỉ có **một DOC-ID, một mã văn bản đúng một loại, một đường dẫn chuẩn và một bản nội dung canonical**. Không tạo thêm bản song song, sổ phụ, register khác, tên file tự đặt hoặc nguồn dữ liệu mới chỉ để thuận tiện cho AI.
  2. Mã loại văn bản phải lấy từ danh mục đã được quy định tại DOC-039; mã cấp/phát hành phải được kiểm tra và ghi vào DOC-040. Không tự đặt loại, tiền tố, số hoặc quy tắc đánh số mới.
  3. DOC-055 là sổ duy nhất quản lý DOC-ID và đường dẫn chuẩn. DOC-040 là sổ duy nhất cấp mã văn bản nghiệp vụ. Hai sổ có phạm vi khác nhau, không thay thế và không nhân bản nhau.
  4. DOC-034 là sổ biên bản duy nhất; DOC-035 là nhật ký thi công duy nhất; Kế hoạch và bản vẽ/mô hình tiếp tục dùng đúng hồ sơ canonical đã khai báo tại DOC-033/DOC-001. Mọi cập nhật phải ghi vào hồ sơ hiện hữu, không tạo hồ sơ cạnh tranh.
  5. Tài liệu kỹ thuật bắt buộc của phần mềm (README, schema, source, config, generated/runtime file) chỉ được tồn tại theo yêu cầu kỹ thuật và phải được phân loại/ánh xạ; không được giả danh văn bản lưu hành, không được tự cấp DOC-ID hoặc mã loại khi không thuộc danh mục.
  6. Tài liệu cũ, alias, bản staging hoặc bản sao chỉ được giữ theo trạng thái và thời hạn/mapping được quản lý; không được coi là nguồn có thẩm quyền. Không xóa dữ liệu lịch sử/canonical nếu chưa kiểm kê, kiểm tra tham chiếu, bảo toàn lịch sử và xác minh theo DOC-056.
  7. Khi AI gặp tài liệu trùng số, trùng loại, khác nội dung hoặc không xác định được nguồn chuẩn, phải dừng sử dụng bản mơ hồ, báo Xu, ghi BLOCKED/UNKNOWN và truy về DOC-001/DOC-055/DOC-039/DOC-040; tuyệt đối không tự chọn hoặc tự tạo nguồn mới.
  8. Không đánh số lặp ở cùng cấp cho thư mục, đề mục hoặc danh mục. Một số thứ tự chỉ được dùng một lần trong cùng phạm vi/cấp; nếu là mã định danh thì tuân theo sổ cấp mã tương ứng.
  9. AI phải kiểm tra hồ sơ hiện hữu trước khi tạo tài liệu; mặc định cập nhật văn bản canonical. Chỉ tạo văn bản mới khi thực sự thuộc loại được phép, chưa có văn bản tương đương, đã được cấp DOC-ID/mã hợp lệ và đăng ký đúng sổ.
- **Quyết định liên quan:** D70-020.
- **Trạng thái:** RECORDED — chỉ thị của Vinh; áp dụng ngay như nguyên tắc điều hành trong Work 70. Không tự tuyên bố toàn bộ cây tài liệu đã được chuẩn hóa.
- **Hành động:** Xu duy trì một nguồn canonical cho mỗi hồ sơ; rà soát và hợp nhất alias/trùng lặp theo DOC-056; cập nhật validator/CI để chặn DOC-ID, mã văn bản, canonical path và số mục trùng; ghi mọi thao tác vào DOC-035.
