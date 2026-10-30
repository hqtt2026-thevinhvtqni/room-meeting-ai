# DASHBOARD — BẢNG ĐIỀU KHIỂN RIÊNG CHO TỪNG WORK

## Mục đích
Mỗi Work có một Dashboard để theo dõi vòng đời, gate, WP, blockers, risks, decisions, evidence và độ mới dữ liệu.

## Thành phần
- index.html: giao diện chỉ đọc.
- PRODUCT_STATUS.json: bản dữ liệu trạng thái cục bộ hiện tại.
- PRODUCT_STATUS.schema.json: hợp đồng kiểm tra cấu trúc dữ liệu.

## Nguồn dữ liệu
- core_live: chỉ dùng khi response đến từ Core thật, đã xác thực và kiểm tra quyền.
- core_cached: cache do Core phát hành, kèm revision/generated_at/freshness.
- local_snapshot: bản chụp trong Sandbox/Work; không phải dữ liệu trực tiếp.
- sample: dữ liệu minh họa.
Nếu tải dữ liệu lỗi, Dashboard hiển thị UNKNOWN. Không fallback sang dữ liệu giả.

## Hiển thị
Dashboard trình bày giai đoạn hiện tại, 9 phase/gate, owner, WP owner/reviewer, blockers, risks, decisions, evidence references, source mode và freshness. Trạng thái tiến độ không thay thế gate.

## Chạy thử
Chạy static HTTP server trong thư mục DASHBOARD, ví dụ `python -m http.server 8080`, rồi mở `http://localhost:8080`. Không mở bằng file:// nếu trình duyệt chặn fetch JSON.

## Giới hạn hiện tại
Dashboard đang đọc PRODUCT_STATUS.json cục bộ. Core API, đăng nhập/phân quyền, live refresh, lưu trữ bền vững, upload và export backend chưa được xác minh/triển khai. Không có nút giả để tuyên bố lưu/xuất file. G0 và các gate lifecycle vẫn chờ kiểm chứng.
