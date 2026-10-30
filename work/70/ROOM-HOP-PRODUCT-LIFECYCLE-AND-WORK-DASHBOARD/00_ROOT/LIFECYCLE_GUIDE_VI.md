# HƯỚNG DẪN TIẾNG VIỆT — 9 GIAI ĐOẠN VÒNG ĐỜI SẢN PHẨM

## 01_DISCOVER — KHÁM PHÁ
Làm rõ người dùng, vấn đề thực tế, bối cảnh, bằng chứng nhu cầu, giả thuyết và phạm vi khám phá.
Đầu ra: problem brief, bằng chứng, cơ hội và giả định.

## 02_DEFINE — ĐỊNH NGHĨA
Chuyển kết quả khám phá thành mục tiêu, phạm vi trong/ngoài, yêu cầu chức năng/phi chức năng, chỉ số thành công và tiêu chí nghiệm thu.
Đầu ra: product brief, requirements và acceptance criteria.

## 03_ARCHITECT — KIẾN TRÚC
Xác định thành phần, ranh giới, luồng dữ liệu/điều khiển, nguồn dữ liệu chuẩn, quyền, bảo mật, lỗi, phục hồi và rủi ro.
Đầu ra: architecture, interface contracts, data model và ADR.

## 04_PLAN — KẾ HOẠCH
Chia sản phẩm thành WP có owner, reviewer, phụ thuộc, đầu ra, tiêu chí nghiệm thu, test plan và nguồn lực.
Đầu ra: roadmap và BUILD_REGISTER.

## 05_BUILD — THI CÔNG
Triển khai theo 9 build areas cố định: 00_ROOT, 01_ORIGINAL, 02_EXTENSION, 03_ARCHITECTURE, 04_CODE, 05_TEST, 06_EVIDENCE, 07_RELEASE, 10_AI_DEBUG_HANDOFF. WP là record quản trị, không tạo lifecycle/folder tree thứ hai.
Đầu ra: code, cấu hình, tài liệu, test và bằng chứng thi công.

## 06_VERIFY — KIỂM CHỨNG
Kiểm tra yêu cầu, tích hợp, bảo mật, lỗi và hồi quy; ghi môi trường, phiên bản, lệnh chạy, log, người kiểm chứng và kết quả.
Đầu ra: verification report, defects và evidence.

## 07_ACCEPT — NGHIỆM THU
Người có thẩm quyền xác nhận tiêu chí, bằng chứng, giới hạn và ngoại lệ.
Đầu ra: ACCEPTED / REJECTED / PENDING kèm actor, timestamp và lý do.

## 08_RELEASE — PHÁT HÀNH
Chuẩn bị version, release notes, cấu hình, quyền, backup, rollback, smoke test và phê duyệt.
Đầu ra: release record và triển khai có kiểm soát.

## 09_OPERATE — VẬN HÀNH
Có owner, monitoring, alert, incident response, backup/restore, bảo trì, chỉ số chất lượng và vòng phản hồi.
Đầu ra: báo cáo vận hành và backlog cải tiến.

## Quy tắc xuyên suốt
1. Không có bằng chứng thì không PASS.
2. Task/WP hoàn tất không đồng nghĩa phase hoàn tất.
3. Dashboard chỉ phản ánh trạng thái, không phê duyệt.
4. UNKNOWN khác FAIL; cả hai đều không phải PASS.
5. Ngoại lệ cần approver, lý do, phạm vi, expiry/review và risk acceptance.
6. Giữ nguyên Work ID, lịch sử, commit và evidence khi migration.
