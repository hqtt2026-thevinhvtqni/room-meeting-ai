# Work 50 — HQTT AI Product Delivery Standard (APDS)

- Work ID: 50
- Tên: HQTT AI Product Delivery Standard
- Tên tiếng Việt: Tiêu chuẩn xây dựng và vận hành sản phẩm CNTT/AI
- Chủ sở hữu / người quyết định: Vinh
- Điều phối / quản lý kế hoạch: Xu (AI-01)
- Ngày khởi tạo hồ sơ: 2026-10-20 (UTC+07:00)
- Trạng thái: CREATED — nội dung khởi tạo; chưa được nghiệm thu/phê duyệt áp dụng toàn HQTT
- GitHub branch: `work/50-ai-product-delivery-standard`
- GitHub path: `work/50/AI-PRODUCT-DELIVERY-STANDARD/`
- Sandbox: Work 50 đã được tạo; 10 hồ sơ chính thức đã được ghi và xác minh sự hiện diện qua listing. Đọc lại nội dung Sandbox vẫn BLOCKED vì sandbox_read trả đối tượng rỗng; chưa xác nhận byte-for-byte.

## Mục tiêu

Thiết lập một tiêu chuẩn dùng chung, có bằng chứng kiểm tra được, cho toàn bộ vòng đời sản phẩm CNTT/AI: từ xác định bài toán, yêu cầu, kiến trúc, kế hoạch, phát triển, kiểm thử, phát hành đến vận hành và bàn giao.

## Hồ sơ chính thức của Work

- `BIEN_BAN.md` — biên bản và quyết định đã thống nhất.
- `KE_HOACH_THI_CONG_XU.md` — kế hoạch thi công do Xu quản lý.
- `NHAT_KY_HOP_THI_CONG.md` — nhật ký chung, mọi AI nối tiếp ghi.
- `01_STANDARD/APDS_STANDARD_v1.0.md` — bản tiêu chuẩn đề xuất.
- `02_TEMPLATES/PRODUCT_CHARTER_TEMPLATE.md` — mẫu khởi tạo sản phẩm.
- `03_ACCEPTANCE/APDS_ACCEPTANCE_CHECKLIST.md` — checklist đánh giá Work 50.

## Quan hệ với các Work khác

- Work 19 — AI Agent Production Stack: áp dụng phần phù hợp cho nền tảng Agent; Work 19 không sở hữu APDS.
- Work 21 — AI Skills: áp dụng các phần phù hợp với thiết kế, kiểm thử và bàn giao Skills; không tự đổi phạm vi Work 21.
- Work 33 — ROOM Shared File & Evidence Hub: có thể cung cấp hạ tầng lưu trữ/tìm kiếm bằng chứng; APDS không mặc định rằng mọi tích hợp đã tồn tại hoặc PASS.
- Các Work sản phẩm khác: dùng APDS sau khi tiêu chuẩn được Vinh phê duyệt và có kế hoạch áp dụng tương ứng.

## Quy tắc trạng thái

- DONE: đã thực hiện đầu việc.
- PASS: tiêu chí cụ thể đã được kiểm tra bằng bằng chứng phù hợp.
- FAIL: kiểm tra không đạt.
- BLOCKED: không thể tiếp tục do phụ thuộc/quyền truy cập/điều kiện chưa đáp ứng.
- CHƯA XÁC MINH: chưa có bằng chứng đủ để kết luận.

## Trạng thái hiện tại

- DONE: tạo branch làm việc riêng và khởi tạo hồ sơ Work 50 trên GitHub.
- CHƯA XÁC MINH: Sandbox đã tạo/đồng bộ; chưa kiểm thử nội dung theo một sản phẩm mẫu.
- CHƯA PHÊ DUYỆT: APDS v1.0 chỉ là bản đề xuất, không tự động trở thành quy định bắt buộc toàn HQTT.

## Bước tiếp theo

1. Khôi phục kết nối Sandbox, kiểm tra Work 50 đã tồn tại hay chưa trước khi tạo.
2. Tạo/đối chiếu cùng bộ hồ sơ trong Sandbox; không tuyên bố đồng bộ chính xác khi chưa đọc lại được.
3. Đánh giá checklist nghiệm thu APDS.
4. Chọn một sản phẩm mẫu để thử nghiệm tiêu chuẩn.
5. Trình Vinh quyết định phê duyệt, sửa đổi hoặc từ chối áp dụng toàn HQTT.


## Cập nhật trạng thái Sandbox — 2026-10-21 (UTC+07:00)

- DONE: tạo Work 50 trong ROOM-HOP Sandbox bằng runtime identity đã đăng ký `xu`.
- DONE: ghi 10 hồ sơ cốt lõi từ branch Work 50 sang Sandbox và xác minh các đường dẫn xuất hiện qua listing.
- PARTIAL: content readback chưa xác minh do công cụ sandbox_read trả đối tượng rỗng. Không được coi đây là đồng bộ nội dung hoàn toàn.
- GitHub branch vẫn là nguồn chuẩn của các hồ sơ Work 50 trong giai đoạn đối chiếu; không sửa/merge vào main.
