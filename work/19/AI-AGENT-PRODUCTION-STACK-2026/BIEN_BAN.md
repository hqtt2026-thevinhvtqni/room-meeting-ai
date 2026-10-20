# BIÊN BẢN — WORK 19

## Thông tin
- Work ID: 19
- Tên: CẤU TRÚC HỌC TẬP — AI AGENT PRODUCTION STACK 2026
- Chủ sở hữu / người quyết định: Vinh
- Điều phối: Xu (AI-01)
- Thời điểm ghi nhận: 2026-10-20, UTC+07:00

## Phạm vi
Xây dựng lộ trình học tập và kiểm chứng Production Readiness cho hệ thống AI Agent, lấy ROOM-HOP làm kiến trúc đối chiếu. Phạm vi hiện tại là tài liệu, bản đồ kiến trúc và kế hoạch kiểm chứng; không tự động mở rộng sang cài đặt framework hoặc thay đổi dịch vụ đang chạy.

## Quyết định và quy tắc
1. Dùng cấu trúc Work riêng dưới work/19/AI-AGENT-PRODUCTION-STACK-2026/, cùng mô hình work/NN/... của các Work khác.
2. Dùng branch work/19-ai-agent-production-stack-2026; không merge vào main trong nhiệm vụ đồng bộ này.
3. Phân biệt DONE (đã thực hiện) với PASS (đã kiểm chứng). Không tuyên bố Production-ready nếu chưa có bằng chứng E2E và tiêu chí nghiệm thu.
4. Core :8000 là nguồn truth; Dashboard :3000 chỉ render.
5. Cần đối chiếu nội dung GitHub với Sandbox sau khi đường đọc Sandbox hoạt động tin cậy; không tuyên bố đồng bộ byte-for-byte trước khi đối chiếu.
6. Mọi hoạt động quan trọng phải ghi người/AI, chức danh, thời điểm UTC+07:00, kết quả, bằng chứng và bước tiếp theo.

## Trạng thái
- DONE: tạo branch làm việc trên GitHub.
- DONE: tạo bản mirror có cấu trúc cho tài liệu học tập và kế hoạch dựa trên thông tin khả dụng trong phiên.
- CHƯA XÁC MINH: nội dung GitHub có trùng từng byte với các file Sandbox hay không.
- BLOCKED: nghiệm thu toàn bộ Work 19; chưa thực hiện G0–G7.
