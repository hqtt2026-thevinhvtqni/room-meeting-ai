# HƯỚNG DẪN TIẾNG VIỆT — 9 GIAI ĐOẠN VÒNG ĐỜI SẢN PHẨM
- **STT / Document ID:** DOC-026
- **Priority:** P3
- **Read order:** 30
- **Depends on:** DOC-004; DOC-005; DOC-033; DOC-036
- **Status:** ACTIVE
- **Version / Updated:** 1.1 / 2026-10-30

Tài liệu này diễn giải tiếng Việt theo đúng thứ tự các giai đoạn chuẩn. Tên tiếng Anh được giữ lại để thống nhất mã thư mục, API và trao đổi kỹ thuật.

## 01_DISCOVER — KHÁM PHÁ
**Mục tiêu:** Hiểu đúng vấn đề cần giải quyết trước khi nghĩ đến giải pháp.
- Ai là người dùng/đối tượng chịu ảnh hưởng?
- Vấn đề thực tế là gì, xảy ra trong bối cảnh nào?
- Bằng chứng nào xác nhận vấn đề tồn tại?
- Điều gì là dữ kiện, điều gì mới chỉ là giả định?
- Cơ hội và kết quả mong muốn là gì?

**Đầu ra:** Bản mô tả vấn đề, bối cảnh, nhóm người dùng, bằng chứng nhu cầu, giả thuyết và phạm vi khám phá.

## 02_DEFINE — ĐỊNH NGHĨA
**Mục tiêu:** Chuyển kết quả khám phá thành mục tiêu và yêu cầu rõ ràng, có thể kiểm tra.
- Mục tiêu sản phẩm và chỉ số thành công.
- Phạm vi làm và không làm.
- Yêu cầu chức năng, phi chức năng và ràng buộc.
- Điều kiện nghiệm thu và tiêu chí đo kết quả.
- Những điểm chưa rõ cần quyết định.

**Đầu ra:** Product Brief (bản định nghĩa sản phẩm), danh sách yêu cầu, chỉ số thành công, tiêu chí nghiệm thu và phạm vi được thống nhất.

## 03_ARCHITECT — KIẾN TRÚC
**Mục tiêu:** Thiết kế cách hệ thống hoạt động trước khi lập kế hoạch thi công chi tiết.
- Các thành phần, ranh giới và trách nhiệm.
- Luồng dữ liệu, luồng điều khiển và tích hợp.
- Nguồn dữ liệu chuẩn, quyền truy cập và bảo mật.
- Cách xử lý lỗi, timeout, dữ liệu cũ và phục hồi.
- Rủi ro kỹ thuật, quyết định kiến trúc và phương án thay thế.

**Đầu ra:** Sơ đồ kiến trúc, hợp đồng giao tiếp, mô hình dữ liệu, quyết định kỹ thuật, phân tích rủi ro và yêu cầu bảo mật. Đây cũng là nơi lưu bản vẽ/mô hình sản phẩm đã duyệt.

## 04_PLAN — KẾ HOẠCH
**Mục tiêu:** Chia sản phẩm thành các gói thi công có thể giao việc, theo dõi và nghiệm thu.
- Các mốc và thứ tự triển khai.
- Work Package (WP — gói thi công), người phụ trách và người review.
- Phụ thuộc, nguồn lực, thời hạn và ưu tiên.
- Đầu ra, tiêu chí nghiệm thu và kế hoạch kiểm thử của từng WP.
- Điều kiện mở giai đoạn BUILD.

**Đầu ra:** Roadmap (lộ trình), kế hoạch mốc, danh sách WP, phân công, phụ thuộc và tiêu chí hoàn tất. Kế hoạch chính thức thuộc Work root/04_PLAN.

## 05_BUILD — THI CÔNG
**Mục tiêu:** Xây dựng sản phẩm theo kế hoạch đã được duyệt.

Nguyên tắc:
- 05_BUILD là tầng ánh xạ và điều phối thi công, không phải nơi lưu bản gốc.
- Mapping Register liên kết WP với source repository, file chuẩn, phiên bản/commit và bằng chứng.
- Source code, test source và cấu hình chính thức nằm tại repository/path được khai báo trong Work Manifest.
- Bản sao phục vụ công cụ phải ghi TEMPORARY, nguồn và phiên bản.
- Không tự đánh dấu PASS khi chỉ mới ghi code hoặc tạo file.

**Đầu ra:** Mapping cập nhật, trạng thái thi công, liên kết source, kết quả test và bằng chứng truy xuất được.

## 06_VERIFY — KIỂM CHỨNG
**Mục tiêu:** Chứng minh sản phẩm đáp ứng yêu cầu bằng kiểm tra có thể lặp lại.
- Mỗi yêu cầu có test hoặc bằng chứng tương ứng.
- Test chức năng, tích hợp, bảo mật, lỗi và hồi quy phù hợp.
- Kết quả phải có môi trường, phiên bản, lệnh chạy và log.
- Người kiểm chứng độc lập với người triển khai khi có thể.
- Lỗi còn tồn tại và rủi ro còn lại phải được công khai.

**Đầu ra:** Báo cáo kiểm thử, ma trận truy vết, lỗi, bằng chứng và kết luận PASS/FAIL/BLOCKED có căn cứ.

## 07_ACCEPT — NGHIỆM THU
**Mục tiêu:** Người có thẩm quyền quyết định sản phẩm có đạt điều kiện chấp nhận hay không.
- Tiêu chí nghiệm thu đã thống nhất được đáp ứng.
- Bằng chứng kiểm chứng có thể truy cập và đúng phiên bản.
- Hạn chế, lỗi còn lại và ngoại lệ được công khai.
- Người có thẩm quyền ghi quyết định, thời điểm và lý do.

**Đầu ra:** Biên bản nghiệm thu: ACCEPTED (chấp nhận), REJECTED (từ chối) hoặc PENDING (chờ bổ sung).

## 08_RELEASE — PHÁT HÀNH
**Mục tiêu:** Đưa phiên bản đã nghiệm thu đến môi trường mục tiêu một cách có kiểm soát.
- Phiên bản và ghi chú phát hành.
- Cấu hình, quyền và kiểm tra bảo mật.
- Backup (sao lưu), rollback (quay lui) và runbook (hướng dẫn thao tác).
- Kiểm tra sau phát hành và người chịu trách nhiệm.
- Phê duyệt phát hành.

**Đầu ra:** Bản phát hành có phiên bản, nhật ký triển khai, bằng chứng smoke test và phương án quay lui.

## 09_OPERATE — VẬN HÀNH
**Mục tiêu:** Duy trì sản phẩm ổn định và dùng dữ liệu vận hành để cải tiến.
- Người trực tiếp chịu trách nhiệm vận hành.
- Monitoring (giám sát), alert (cảnh báo) và quy trình incident (sự cố).
- Sao lưu, khôi phục, bảo trì và chỉ số chất lượng dịch vụ.
- Theo dõi lỗi, chi phí, mức sử dụng và phản hồi người dùng.
- Đưa bài học vận hành quay lại DISCOVER/DEFINE cho chu kỳ tiếp theo.

**Đầu ra:** Báo cáo vận hành, sự cố, chỉ số, kế hoạch bảo trì và đề xuất cải tiến.

## Quy tắc xuyên suốt
1. Không có bằng chứng thì không PASS.
2. Hoàn thành task không đồng nghĩa hoàn thành phase.
3. Dashboard chỉ phản ánh trạng thái; không có quyền tự phê duyệt.
4. UNKNOWN (chưa xác định) khác FAIL (không đạt), và cả hai đều không phải PASS.
5. Mọi ngoại lệ phải có người duyệt, lý do, phạm vi và hạn sử dụng.
6. Giữ nguyên Work ID và lịch sử khi chuyển đổi cấu trúc.
7. Không lưu hai bản gốc cạnh tranh giữa Work root và 05_BUILD.
