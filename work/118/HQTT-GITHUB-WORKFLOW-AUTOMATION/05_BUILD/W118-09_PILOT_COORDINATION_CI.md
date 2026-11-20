# W118-09 — PILOT BUILD: W118 COORDINATION CI (PHẠM VI GIỚI HẠN)

- **Work:** W118 (Issue #65) · **Ngày:** 2026-11-20 (UTC+07)
- **Ủy quyền:** Vinh phê duyệt BUILD trực tiếp trong phiên ("xây đi, chưa cần phản biện; khi xong Xu nghiệm thu OK là được") — G3 được chấp nhận trong phiên.
- **Phạm vi:** tài liệu + 1 workflow CI + 2 template. KHÔNG: branch protection, secrets, webhook, auto-merge, token ngoài GITHUB_TOKEN của CI.

## Đã xây (trên nhánh `work/118-github-workflow-automation`)

1. `.github/workflows/w118-coordination-ci.yml`:
   - Trigger: push/PR theo `work/118/**` + workflow_dispatch (đúng ma trận W118-03, xử lý Gap #2).
   - Job `validate-w118-docs`: validate YAML workflow W118 (PyYAML — nếu thiếu thì ghi limitation, không PASS ảo), kiểm cấu trúc tài liệu W118 bắt buộc, kiểm 7 label state machine trong W118-02, đếm Entry nhật ký; summary trạng thái WP ra step summary.
   - Job `failure-diagnostic` (chỉ khi FAIL và ngoài PR): idempotency theo W118-05 — dedupe theo SHA, trùng thì chỉ comment dùng lại; label `ci-diagnostic`; xử lý Gap #3.
2. `.github/ISSUE_TEMPLATE/work-execution.md` và `.github/PULL_REQUEST_TEMPLATE.md` (theo W118-02 mục 5).

## Kết quả CI thực tế

- Ghi nhận tại Entry 004 của nhật ký thi công (run URL + commit SHA được cập nhật sau khi push).
