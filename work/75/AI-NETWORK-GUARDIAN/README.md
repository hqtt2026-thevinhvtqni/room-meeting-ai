# Work 75 — AI-NETWORK-GUARDIAN

**Sản phẩm:** Ứng dụng quản lý hạ tầng mạng có AI tham gia  
**Nền tảng:** Mobile App + PC Dashboard  
**Trạng thái:** ACTIVE / DESIGN BASELINE / NOT RELEASED  
**Chuẩn quy trình:** Work 70 — ROOM-HOP Product Lifecycle & Work Dashboard

## Mục tiêu
Xây dựng một sản phẩm quản lý hạ tầng mạng nội bộ, bắt đầu từ router và LAN văn phòng. Người quản trị theo dõi trên điện thoại hoặc PC; AI hỗ trợ phân tích, giải thích bất thường và đề xuất xử lý.

## Nguyên tắc sản phẩm
- Một backend, một mô hình dữ liệu và một bộ nghiệp vụ dùng chung cho Mobile và PC.
- PC Dashboard là giao diện quản trị đầy đủ; Mobile App ưu tiên theo dõi, cảnh báo và thao tác nhanh.
- AI là trợ lý phân tích và tư vấn, không phải quyền điều khiển hạ tầng mặc định.
- Local-first; ưu tiên xử lý và lưu trữ trong mạng nội bộ.
- Giai đoạn đầu chỉ đọc (read-only) router/mạng; không tự đổi cấu hình, không tự khắc phục.
- Mọi dữ liệu hiển thị phải có nguồn, thời điểm thu thập và trạng thái tin cậy.

## Trạng thái
Xem [Dashboard](DASHBOARD/README.md), [Manifest](00_ROOT/DOC-001_BAN-TUYEN-NGON_WORK-MANIFEST.md), [Roadmap](04_PLAN/DOC-010_KE-HOACH-TRIEN-KHAI_IMPLEMENTATION-ROADMAP.md).

> GitHub bootstrap snapshot. Việc đồng bộ đầy đủ với Work Sandbox 8030 chưa được xác minh; xem Nhật ký thi công.
