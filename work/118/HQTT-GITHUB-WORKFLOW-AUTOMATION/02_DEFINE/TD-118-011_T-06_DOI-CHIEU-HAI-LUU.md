# TD-118-011 — T-06 ĐỐI CHIẾU HAI LUỒNG W118 (PR #66 vs main)

- **Work:** W118
- **Ngày:** 2026-11-20
- **Mục đích:** phục vụ test T-06 trong KT-118-009; bổ sung hồ sơ results, không sửa code trong vòng nghiệm thu.

## 1. So sánh kỹ thuật
| Tiêu chí | main: w118-workflow-automation.yml | PR #66: w118-coordination-ci.yml (head 05b3fe3) |
|---|---|---|
| Kiểu | event orchestration (issues/issue_comment/workflow_run) | docs validation CI (push/PR/dispatch) + diagnostics |
| Chức năng | handoff-brief, ack-verification, ci-failure-diagnostics (W300/W70) | validate YAML syntax, validate docs structure, state summary, failure-diagnostic nội bộ |
| Triggers không chồng lấn? | chỉ phản ứng với issue/comment/CI-fail | chỉ chạy khi file W118 thay đổi hoặc dispatch |
| Idempotency diagnostics | 1 issue theo (workflow, SHA), có label w118-blocked | dedupe theo title có SHA — LƯU Ý: title chứa SHA nên mỗi fail mới sẽ tạo issue mới (không gộp) |
| Hồ sơ tham chiếu | không đụng hồ sơ docs | BẮT BUỘC có 01_DISCOVER/W118-01_... và 02_DEFINE/W118-02_... — các file này CHỈ tồn tại trên nhánh PR, KHÔNG tồn tại trên main |
| Xác thực actor | bắt đầu có (magic-token +); role mapping manual | không liên quan |

## 2. Kết luận đối chiếu (kiểm chứng thực tế cấu trúc)
- Hai luồng KHÔNG chồng lấn chức năng: một bên là event orchestration, một bên là docs-CI. Có thể tách riêng nếu mọi bên đồng ý boundary rõ ràng, mỗi luồng 1 MAINT knowledge.
- RỦI RO MERGE PR #66 nguyên trạng thái: job validate-w118-docs sẽ FAIL vì hai file hồ sơ bắt buộc vắng mặt trên main (đây là lý do run của nó chưa bao giờ được xét trên main).
- CRITICAL: nếu cả hai sống cùng repo, w118-coordination-ci.yml job diagnostics dùng label ci-diagnostic trong khi luồng main dùng w118-blocked — 2 label khác mục đích tương tự => tạo nhiễu. Cần chuẩn hóa 1 label.

## 3. Đề nghị chính thức (để Xu đối chiếu và quyết)
1. Main là canonical cho W118 hồ sơ (đúng nguyên tắc evidence-first đã dùng từ Issue #65).
2. Sau khi vòng kiểm thử độc lập của Xu đóng: PR #66 có thể được chuyển hóa thành đóng-góp riêng: giữ job validate-w118-docs + failure-diagnostic như một CI bổ trợ, nhưng sửa danh sách hồ sơ bắt buộc để khớp tập hồ sơ canonical trên main, hoặc ghi kế hoạch di chuyển (move) các file hồ sơ "song song" nếu muốn dùng thêm chức năng validate.
3. Giữ một label diagnostics duy nhất: w118-blocked. Bỏ ci-diagnostic trong đề nghị merge lại sau.

## 4. Bằng chứng
- Nội dung w118-coordination-ci.yml theo sha 05b3fe3 (kết quả đọc lỗi: "get_file_contents" kết quả kết hợp).
- Base PR #66: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/pull/66 (open, draft: true); head branch work/118-github-workflow-automation.
