# Quy trình điều phối thực thi toàn trình / End-to-End Execution Orchestration
- **STT / Document ID:** DOC-042
- **Priority:** P0
- **Read order:** 42
- **Depends on:** DOC-001; DOC-002; DOC-004; DOC-005; DOC-033; DOC-041
- **Status:** ACTIVE / OPERATING STANDARD
- **Version / Updated:** 1.0 / 2026-10-30

## 1. Mục tiêu
Biến chuẩn vòng đời Work thành quy trình vận hành có thể giao việc, thực thi, kiểm chứng và truy xuất. AI là adapter thực hiện vai trò được cấp quyền; Work lifecycle/Core là nơi quản lý sự thật và quyền hạn.

## 2. Mô hình vận hành
- Vinh: Product Owner và thẩm quyền cuối cùng; quyết định mục tiêu, phạm vi lớn, thay đổi chính sách, nghiệm thu và phát hành.
- Xu / AI-01: Lifecycle Orchestrator; chịu trách nhiệm điều phối đầu-cuối, phân rã WP, giao đúng vai trò, xử lý phụ thuộc, tổng hợp bằng chứng và báo cáo.
- AI/nhân sự thực thi: nhận một WP có phạm vi, nguồn chuẩn, đầu ra, quyền, hạn chế và tiêu chí nghiệm thu.
- Reviewer/QE: độc lập với người làm; kiểm tra kết quả theo tiêu chí và bằng chứng.
- Core: nguồn sự thật dự kiến cho danh tính, quyền, trạng thái, quyết định và metadata bằng chứng khi các API đó được triển khai/xác minh.
- Dashboard: read-only projection; không cấp quyền, không phê duyệt, không tự đổi trạng thái.

## 3. Chu trình bắt buộc
READ → TRACE → ANALYZE → DECIDE → ARCHITECT → PLAN → ASSIGN → BUILD → INTEGRATE → VERIFY → DEBUG → REGRESSION → ACCEPTANCE PREPARATION → HANDOFF.

Mỗi vòng lặp phải tạo ra thay đổi hoặc bằng chứng mới. Không lặp lại thao tác đọc/kiểm tra nếu không có lỗi mới, phiên bản mới hoặc câu hỏi chưa được trả lời.

## 4. Hợp đồng giao việc (Work Assignment Contract)
Mỗi assignment phải có:
1. Work ID và WP ID ổn định.
2. Mục tiêu và phạm vi IN/OUT.
3. AI ID, vai trò, người chịu trách nhiệm và reviewer độc lập.
4. Canonical repository/path, branch, starting commit/version.
5. Đầu vào và tài liệu/ADR bắt buộc.
6. Quyền được phép và hành động bị cấm.
7. Đầu ra cụ thể, định dạng và vị trí lưu.
8. Acceptance criteria có thể kiểm tra.
9. Test/evidence bắt buộc, môi trường và lệnh chạy.
10. Dependencies, blocker, thời hạn nếu có.
11. Cơ chế báo cáo, bàn giao và trạng thái.

Assignment thiếu nguồn chuẩn, quyền, đầu ra hoặc tiêu chí nghiệm thu không được chuyển READY.

## 5. Trạng thái assignment/WP
DRAFT → READY → IN_PROGRESS → IN_REVIEW → DONE.
- BLOCKED có thể áp dụng từ bất kỳ trạng thái đang hoạt động nào.
- Review REJECTED trả về IN_PROGRESS kèm finding cụ thể.
- DONE chỉ khi toàn bộ acceptance criteria được xác minh và evidence được đăng ký.
- CANCELLED cần quyết định của owner và lý do.
- WP DONE không tự động làm phase DONE hoặc gate PASS.

## 6. Quy tắc phân công
- Chọn agent theo năng lực đã được kiểm chứng, quyền truy cập thực tế, loại công việc và chi phí/rủi ro.
- Không suy diễn quyền truy cập từ tên sản phẩm hoặc lời giới thiệu; phải kiểm tra thao tác thật.
- Một WP có đúng một accountable owner; có thể có contributors nhưng phải ghi rõ.
- Người viết code không tự làm reviewer cuối cùng cho cùng thay đổi.
- Nếu agent không truy cập được repository, Sandbox, MCP hoặc môi trường cần thiết, không giao nhiệm vụ phụ thuộc vào quyền đó.
- Ưu tiên tái sử dụng quyền hiện có; không tạo API key/chi phí mới khi chưa có phê duyệt.
- Mọi credential phải qua secret manager/connector được duyệt; không đưa vào prompt, log hoặc tài liệu.

## 7. Quy tắc thực thi và tích hợp
- Kiểm tra trạng thái branch/worktree trước khi sửa.
- Không ghi đè thay đổi của phiên khác; nếu xung đột, dừng và reconcile.
- Chỉ thay đổi file trong scope được giao.
- Commit/PR phải liên kết Work/WP/decision/evidence.
- Tích hợp theo dependency; chạy test tập trung rồi regression phù hợp.
- Ghi rõ NOT RUN, BLOCKED, FAIL, PASS; PASS phải có lệnh, môi trường, phiên bản, exit code và output.
- Không merge, deploy, xóa dữ liệu hoặc thay đổi policy nếu chưa được cấp quyền.

## 8. Hợp đồng bằng chứng
Evidence tối thiểu ghi: Evidence ID; claim/requirement/WP được hỗ trợ; producer; reviewer; timestamp; source URI/path; commit/version/hash; environment/tool version; command/action; result; integrity/provenance; access classification; verification status.
Ảnh chụp màn hình không thay thế log hoặc dữ liệu máy đọc được khi cần xác minh kỹ thuật.

## 9. Xử lý blocker
Báo cáo theo mẫu: vấn đề; bằng chứng và lần thử; nút thắt; ảnh hưởng; lựa chọn; điều kiện còn thiếu; owner cần hành động.
Chỉ escalte khi thiếu thẩm quyền, phụ thuộc bên ngoài, rủi ro bảo mật/quyền riêng tư, thay đổi phá hủy/không đảo ngược, chi phí định kỳ hoặc quyết định được giữ lại cho Vinh.
Không báo blocker chung chung và không retry lặp lại nếu không có dữ kiện mới.

## 10. Quyền quyết định
Xu được tự quyết định các lựa chọn kỹ thuật thường nhật, có thể đảo ngược, nằm trong scope và kiến trúc đã duyệt. Vinh giữ quyền thay đổi mục tiêu/scope trọng yếu, chính sách bảo mật, nguồn sự thật, chi phí đáng kể, migration phá hủy, production release và acceptance cuối cùng.

## 11. Báo cáo/handoff
Mỗi lần bàn giao ghi: AI ID/role; Work/WP; scope; branch/commit đầu-cuối; file đã đọc/sửa; test và kết quả; evidence refs; trạng thái; defect/risk; dependency; owner tiếp theo; sync status.
Kết quả phải phân biệt DESIGN, IMPLEMENTED, EXECUTED, VERIFIED, ACCEPTED, RELEASED.

## 12. Tiêu chí tuân thủ
Không có assignment READY nếu thiếu hợp đồng; không có DONE nếu thiếu acceptance evidence; không có gate PASS nếu thiếu evaluator/authority; không có RELEASED nếu thiếu acceptance và release evidence.