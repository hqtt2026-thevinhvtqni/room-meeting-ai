# BIÊN BẢN — WORK 50

## Thông tin
- Work ID: 50
- Tên: HQTT AI Product Delivery Standard (APDS)
- Chủ sở hữu / người quyết định cuối cùng: Vinh
- Điều phối / quản lý kế hoạch: Xu (AI-01)
- Người thực hiện ghi hồ sơ: Xu (AI-01), CEO / AI Core của LAB
- Ngày ghi nhận: 2026-10-20 (UTC+07:00)
- Trạng thái: DECISION RECORDED — chờ nghiệm thu và phê duyệt tiêu chuẩn

## Bối cảnh
HQTT cần một chuẩn chung để quy hoạch và phát triển sản phẩm CNTT/AI theo vòng đời đầy đủ, tránh mỗi Work tự định nghĩa quy trình, vai trò, trạng thái và bằng chứng khác nhau.

## Phạm vi
APDS bao phủ: quản trị sản phẩm, khám phá bài toán, yêu cầu, kiến trúc, kỹ thuật AI, kế hoạch giao hàng, phát triển, QA/kiểm thử, bảo mật, phát hành, vận hành, bằng chứng và bàn giao.

APDS là tiêu chuẩn quản lý và tiêu chí; bản thân Work 50 không tự động triển khai code hoặc thay đổi các dịch vụ hiện hữu.

## Quyết định được ghi nhận
1. Tạo Work riêng mã 50: HQTT AI Product Delivery Standard (APDS).
2. Work 50 sở hữu tiêu chuẩn, phiên bản và quá trình đánh giá tiêu chuẩn.
3. Work 19, Work 21 và các Work sản phẩm khác là Work áp dụng tiêu chuẩn trong phạm vi phù hợp; không chuyển quyền sở hữu APDS sang các Work đó.
4. Không được coi APDS là tiêu chuẩn đã phê duyệt toàn HQTT cho đến khi Vinh ra quyết định rõ ràng.
5. Không ghi PASS nếu thiếu bằng chứng đáp ứng tiêu chí nghiệm thu.
6. Giữ thay đổi trên branch `work/50-ai-product-delivery-standard`; không sửa/merge vào `main` trong bước khởi tạo này.
7. Phải duy trì đúng ba hồ sơ điều hành chính thức: biên bản, kế hoạch thi công và nhật ký chung; không tạo các bản cạnh tranh.
8. Phải tạo/đối chiếu Sandbox khi dịch vụ sẵn sàng. Tại thời điểm ghi biên bản, lệnh liệt kê Work Sandbox trả lỗi kết nối nên trạng thái Sandbox là CHƯA XÁC MINH.

## Quyết định chưa đưa ra
- Chưa phê duyệt APDS v1.0 làm quy định bắt buộc toàn HQTT.
- Chưa chốt ngưỡng định lượng chung cho độ chính xác AI, độ trễ, chi phí hoặc độ tin cậy. Các ngưỡng phải được xác định theo rủi ro, use case và dữ liệu đánh giá của từng sản phẩm.
- Chưa xác nhận Work 50 đã đồng bộ với Sandbox.
- Chưa xác nhận sản phẩm mẫu nào sẽ dùng để thử nghiệm.

## Bước tiếp theo
Khôi phục kết nối Sandbox → đối chiếu hồ sơ → đánh giá checklist → chạy thử trên sản phẩm mẫu → trình Vinh phê duyệt.

## Bổ sung quyết định — 2026-10-21 (UTC+07:00)

### Thống nhất nguyên tắc dự phòng MCP
- Khi MCP lỗi nhưng GitHub hoạt động, Xu tiếp tục các đầu việc có thể thực hiện an toàn trực tiếp trên branch Work; ghi nhận commit, bằng chứng và phần bị chặn bởi Sandbox.
- Khi MCP phục hồi, phải đọc và đối chiếu trạng thái GitHub/Sandbox trước khi đồng bộ; phát hiện và xử lý xung đột trước khi ghi; đọc lại hai phía sau đồng bộ.
- Không coi MCP lỗi là bằng chứng rằng mọi dịch vụ ROOM-HOP đều lỗi; xác định phạm vi ảnh hưởng theo bằng chứng.
- Không tuyên bố Sandbox đã đồng bộ cho đến khi có bằng chứng đọc lại và so sánh thành công.

### Danh mục vai trò AI
- Đã tạo đề xuất 01_STANDARD/AI_ROLE_CATALOG_v1.0.md với 17 vai trò chuẩn.
- APDS được bổ sung tham chiếu tới danh mục, ma trận phân công và quy trình dự phòng MCP.
- Trạng thái vẫn PROPOSED; chưa áp dụng bắt buộc toàn HQTT cho đến khi Vinh phê duyệt.
