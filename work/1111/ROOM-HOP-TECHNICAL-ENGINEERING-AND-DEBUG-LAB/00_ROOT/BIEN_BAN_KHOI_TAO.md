# BB-1111-001 — BIÊN BẢN KHỞI TẠO WORK 1111
**Tên:** ROOM-HOP Technical Engineering & Debug Lab  
**Mã Work:** 1111 · **Ngày:** 2026-11-08  
**Trạng thái:** ACTIVE — INITIALIZED

## 1. Mục đích
Phòng kỹ thuật dùng chung cho Xu và các AI được ROOM-HOP đăng ký để đọc, truy vết, phân tích, đề xuất, xây dựng và kiểm thử ROOM-HOP.

## 2. Phạm vi
Khảo sát kiến trúc, source, runtime, MCP, Sandbox, GitHub, CI/CD và môi trường chạy; xử lý lỗi theo READ → TRACE → ANALYZE → DECIDE → BUILD → VERIFY → HANDOFF; phối hợp AI kỹ thuật, review độc lập và bàn giao bằng chứng.

## 3. Ranh giới
- Work kỹ thuật đặc thù, không phải Work sản phẩm/kinh doanh.
- Sandbox là không gian làm việc trực tiếp cho AI; GitHub vẫn là nguồn chuẩn của source.
- Không tự ý ghi đè source chuẩn, commit/push hoặc thay đổi Work khác ngoài phạm vi được giao.
- Không kết luận PASS khi thiếu bằng chứng.
- Mỗi hồ sơ có một vị trí chuẩn, không nhân bản tài liệu.
- W70 là chuẩn vòng đời/quản trị Work; W0000 là chuẩn quản trị công ty. W1111 kế thừa nguyên tắc phù hợp, không sao chép bộ máy Work sản phẩm.

## 4. Quy tắc phối hợp
AI phải đọc hồ sơ, registry và nhật ký trước khi hỏi; tự truy tìm dữ kiện đã có trong hệ thống. Chỉ hỏi người dùng khi thiếu điều kiện không thể tự xác minh hoặc cần quyết định thuộc thẩm quyền người dùng.

## 5. Bằng chứng khởi tạo
MCP 8030 trả status=ok, identity_id=xu, authorization=ALLOW: xu is a registered ROOM HOP member.
