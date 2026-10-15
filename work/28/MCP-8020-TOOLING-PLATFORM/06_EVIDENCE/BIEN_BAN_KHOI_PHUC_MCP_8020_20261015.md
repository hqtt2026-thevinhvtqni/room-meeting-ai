# BIÊN BẢN TIẾP TỤC TRIỂN KHAI — KHÔI PHỤC KẾT NỐI MCP 8020
- Ngày: 2026-10-15
- Work: 28 — MCP Tooling Platform
- Trạng thái: BLOCKED — kết nối công cụ ROOM-HOP từ phiên Xu vẫn trả về `UNAVAILABLE: Connection failed`.
- Bằng chứng đầu vào: người dùng chạy `.\start-dev.ps1`; script báo `[PASS] MCP Meeting started :8020`, nhưng `:8030` báo `[BLOCKED] MCP Build did not listen on :8030`.
- Kiểm tra trực tiếp từ phiên Xu: gọi `get_room_context` và `sandbox_list_works` qua connector đều thất bại với `Connection failed`.
- Kết luận: script báo dịch vụ cục bộ 8020 khởi động, nhưng chưa xác minh được đường kết nối từ phiên Xu tới MCP; không được ghi PASS cho kết nối end-to-end. Lỗi 8030 là vấn đề riêng, chưa có bằng chứng xác định liên quan đến lỗi kết nối 8020.
## Việc cần làm
1. Trên PC, xác minh listener cục bộ: `Test-NetConnection 127.0.0.1 -Port 8020`.
2. Kiểm tra endpoint MCP và giao thức HTTP/SSE (Server-Sent Events — luồng sự kiện từ máy chủ), sau đó kiểm tra Tailscale Funnel/đường truy cập từ xa nếu dùng.
3. Kiểm tra log tiến trình MCP Meeting, cấu hình endpoint và lỗi xác thực/transport; không đưa token hoặc bí mật vào biên bản.
4. Sau khi kết nối phục hồi, đọc lại biên bản này và nhật ký, xác minh thao tác đọc/ghi Work 28 qua MCP.
5. Xử lý MCP Build :8030 theo nhánh riêng; không mở shell tổng quát, không tạo execution host mới, không bỏ qua Core.
## Tiêu chí hoàn tất
- Có bằng chứng listener :8020 hoạt động.
- Phiên Xu gọi được công cụ MCP thật và đọc được dữ liệu Work.
- Ghi biên bản qua MCP thành công và đọc lại xác minh nội dung.
- Trạng thái cuối chỉ PASS khi đủ bằng chứng; nếu chưa thì giữ BLOCKED.
