# BIÊN BẢN — Python Test Runtime cho ROOM-HOP Sandbox

- **Ngày:** 24/10/2026 (Asia/Ho_Chi_Minh)
- **Chủ dự án / quyền quyết định cuối:** Vinh
- **Điều phối:** Xu (AI-01)
- **Phạm vi:** Giải quyết lỗi Tester do thiếu Python, pytest, phụ thuộc dự án hoặc không có đường thực thi lệnh trong Sandbox.
- **Work chủ trì:** Work 32 — CI/CD ROOM-HOP Python, không Docker.
- **Work tích hợp:** Work 12 — Work Execution Environment; Work 27 — Sandbox Execution Runtime VS Code; Work 51 — Coder–Tester.
- **Trạng thái:** DECISION ghi nhận hướng triển khai; SOURCE WRITTEN IN SANDBOX; TEST EXECUTION NOT RUN; live execution BLOCKED.

## 1. Vấn đề

Lỗi kiểm thử thường có thể bắt nguồn từ môi trường thực thi chứ không nhất thiết từ mã nguồn. Thiếu pytest, sai phiên bản Python, phụ thuộc không khai báo, không thu thập được test và không có công cụ chạy lệnh phải được phân loại riêng. Không chấp nhận “Ran 0 tests” hoặc test bị bỏ qua như bằng chứng PASS.

## 2. Quyết định kiến trúc

1. Dùng Work 32 làm nơi quản lý kế hoạch bổ sung và tiêu chí nghiệm thu, vì Work 32 đã có phạm vi CI/CD Python không Docker; không tạo Work trùng lặp.
2. Truy vết hợp đồng Work 12/13/27 trước khi thêm adapter mới; tránh tạo API hoặc runtime song song không cần thiết.
3. Chạy test trong worker/Execution Host có quyền hạn thấp và được cô lập; không chạy mã dự án tùy ý trong Core :8000 hoặc tiến trình MCP.
4. Mỗi Task có môi trường Python độc lập, phụ thuộc khai báo, lệnh chạy cố định theo policy và bằng chứng máy đọc được.
5. Không PASS nếu thiếu test được thu thập, thiếu exit code/log hoặc báo cáo mâu thuẫn.
6. Vòng sửa mã tối đa 2 chu kỳ; lỗi môi trường chuyển cho chủ sở hữu runtime, không đổ mặc định cho Coder.
7. Không bật CI, deploy, sửa Core hoặc ghi đè cấu hình dịch vụ trước khi các cổng kiểm chứng và quyền thực thi được xác minh.

## 3. Nhiệm vụ tiếp theo

Xem 03_ARCHITECTURE/PYTHON_TEST_RUNTIME_PLAN.md để biết W32-PT-01 đến W32-PT-10, phụ thuộc và điều kiện nghiệm thu.

## 4. Bằng chứng và giới hạn hiện tại

- Đã xác nhận Work 32, Work 12, Work 27 và Work 51 tồn tại trong Sandbox.
- Đã truy vết Work 12 Execution Bridge và Work 27 Execution Contract/RuntimeAdapter. Work 27 ghi rõ live E2E bị BLOCKED do chưa có execution capability được ủy quyền qua route ROOM-HOP hiện tại.
- Danh mục công cụ ROOM-HOP 8030 trong phiên hiện tại cho thấy thao tác file Sandbox; không có tool shell/Python/pytest trực tiếp được công bố.
- Đã ghi kế hoạch, biên bản, quyết định tích hợp, classifier và 15 test case vào Sandbox; read-back xác nhận nội dung.
- Chưa thực thi unit test; không có kết quả PASS nào được tuyên bố.
- Chưa xác minh live endpoint/attestation của Execution Host :8031.
- Chưa sửa Core :8000, chưa kích hoạt CI/deploy và chưa ghi thay đổi lên GitHub.

## 5. Quyết định cần giữ

**Không chặn toàn bộ dự án vì một Task không chạy được test.** Ghi ENV_BLOCKED, POLICY_BLOCKED hoặc PENDING EVIDENCE, chuyển việc cho đúng chủ sở hữu và tiếp tục Task độc lập. Ka chỉ xác nhận những gì bằng chứng thực tế hỗ trợ.
