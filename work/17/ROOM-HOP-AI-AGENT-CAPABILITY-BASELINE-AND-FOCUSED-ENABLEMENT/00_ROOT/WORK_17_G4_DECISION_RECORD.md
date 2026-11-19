# BIÊN BẢN QUYẾT ĐỊNH G4 — WORK 17 (ĐỀ XUẤT TRÌNH VINH PHÊ DUYỆT)

- Work ID: 17 · Ngày: 2026-11-19 · Người phát biểu: Xu / AI-01 (chuyển nguyên văn bởi Vinh cho Vibe lưu hồ sơ)
- Trạng thái: **G4 CONDITIONAL / MIGRATION NOT AUTHORIZED**

## 1. Nguyên tắc của Xu
Chuẩn hóa cấu trúc không đồng nghĩa ép tất cả Work phải cùng mức hoàn thiện. Work 17 phải tạo ra một chuẩn 71 Work áp dụng được, AI nào cũng hiểu, bằng chứng không thất lạc. Duyệt hướng kiến trúc, chưa bật quyền di trú; AI có năng lực GitHub-side tiếp tục làm việc chuẩn bị, không đứng chờ.

## 2. Quyết định định tính
1. Chấp thuận về nguyên tắc chuẩn layout nested work/<ID>/<WORK-NAME>/ làm chuẩn thống nhất cho GitHub Mirror và Sandbox.
2. Chưa cho phép di trú hàng loạt; Vibe ở chế độ chuẩn bị và kiểm chứng.
3. Điều chỉnh proposal: tách 06_VERIFY và 06_EVIDENCE; sửa số liệu coverage (nested 9/17, flat 8/17); tích hợp deep-scan 7 Work; phân loại theo maturity, không ép Work sơ khai đủ vòng đời; điều kiện parity Sandbox ↔ GitHub trước khi di trú; phân biệt G4 (phê duyệt kiến trúc) với G7 (cho phép thực thi).
4. Kiểm soát xác minh: đọc qua Contents API, đối chiếu blob/commit SHA, xác nhận nội dung thật chứa deep-scan, không dùng raw làm nguồn xác nhận duy nhất.
5. Sau hoàn thiện: cập nhật biên bản và nhật ký; gửi Xu phản biện độc lập; trình Vinh quyết định cuối cùng trước khi di trú.

## 3. Phân công
| Vai | Nhiệm vụ |
|-----|----------|
| Vibe | GitHub: coverage, proposal, biên bản; chuẩn bị di trú |
| Xu | Kiến trúc, parity Sandbox ↔ GitHub, phản biện, nghiệm thu |
| Ka | Nhất quán governance và gate |
| Qw | Kiểm thử độc lập tiêu chí nghiệm thu |
| Vinh | Quyết định cuối cùng cho phép di trú |

## 4. Các việc Vibe đã thực hiện từ quyết định này (commit ghi nhận)
- Coverage v1.1: commit 5eb8c982 (đã sửa số liệu, tách 06_VERIFY/06_EVIDENCE, maturity note).
- Proposal v1.1: commit của kỳ này.
- Biên bản này: commit của kỳ này.
- Tính chất: hồ sơ lưu kết quả của G4 — chờ Vinh duyệt; chưa có lệnh di trú.