# TD-118-008 — AUDIT JOURNAL & DASHBOARD DATA CONTRACT (W118-07)

- **Work:** W118
- **Ngày:** 2026-11-20
- **Trạng thái:** DRAFT — chờ phản biện.

## 1. Nguyên tắc một nguồn sự thật
- Nhật ký thi công của Work (EVIDENCE/NHAT-KY-*.md) do người/AI ghi khi làm việc; bot KHÔNG ghi đè nội dung người đã viết.
- Evidence register JSON (mẫu Work 70) là nguồn dữ liệu có cấu trúc duy nhất mà bot được phép ghi, và chỉ ở state RECORDED, không bao giờ VERIFIED.
- Dashboard của Work 70 chỉ là read-only projection từ evidence register; W118 không tạo file trạng thái trùng lặp nào.

## 2. Data contract bot ghi vào register
Mỗi run CI ghi 1 row với: evidence_id là "ci-<run_id>-<attempt>"; work_id suy từ path thay đổi (mẫu "work/<so>/..."); state luôn RECORDED; ci_* fields lấy từ context GitHub (đổ vào sau khi schema v1.2 được ACK); source_commit là github.sha; limitations ghi cố định "CI PASS không thay thế nghiệm thu".

## 3. Reconciliation định kỳ
- Workflow định kỳ (cron hoặc workflow_dispatch, bật sau G5) đối soát: (a) số run trong khoảng thời gian so với số evidence row mới, lệch thì liệt kê run thiếu; (b) row RECORDED quá 14 ngày chưa được review thì nhắc lại; (c) kết quả đối soát đăng vào issue audit của W118, không ghi trực tiếp Dashboard.

## 4. Audit log của các mutation bot
- Mỗi mutation bot (insert/update evidence row, tạo issue, gán label) phải có evidence row OPERATION tương ứng hoặc trích output vào diagnostics issue.
- Bot chỉ append/update entry của chính nó; không sửa dòng lịch sử trong hồ sơ người ghi (bài học append-only từ Work 28).

## 5. Giới hạn
- W118 không dựng dashboard riêng. Khi cần hiển thị trạng thái W118, dùng view đọc từ register; Work 70 chưa hỗ trợ thì liệt kê trong nhật ký W118 cho đến khi Work 70 mở rộng.
