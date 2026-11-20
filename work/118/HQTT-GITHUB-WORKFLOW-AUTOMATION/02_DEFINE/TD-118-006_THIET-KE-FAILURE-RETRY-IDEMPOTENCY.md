# TD-118-006 — THIẾT KẾ FAILURE / RETRY / IDEMPOTENCY (W118-05)

- **Work:** W118
- **Ngày:** 2026-11-20
- **Trạng thái:** DRAFT — chờ phản biện.

## 1. State machine một đơn việc (issue/PR theo dõi)
Trạng thái: ASSIGNED → ACKED → IN_PROGRESS → CI_PASS | CI_FAIL. CI_PASS → IN_REVIEW → ACCEPTED → MERGED → EVIDENCED → CLOSED. CI_FAIL (trong cap 2 retry) → IN_PROGRESS lại. CI_FAIL vượt cap → BLOCKED → sau can thiệp có người → IN_PROGRESS. Không hoạt động 7 ngày → STALE (nhắc) → BLOCKED nếu tiếp tục.
Mỗi chuyển trạng thái phải có comment/evidence row có timestamp làm bằng chứng; không dùng thuộc tính nội bộ làm bằng chứng.

## 2. Quy tắc retry
- Cap chính: 2 lần chạy lại bởi actor. Lần thứ 3 phải có người phê duyệt hoặc đổi cách tiếp cận.
- Mỗi retry phải có comment "RETRY-<n> <lý do>" và evidence row RUNTIME mới kèm source_commit mới. Không retry lại cùng SHA trừ khi lỗi là flaky infra và được ghi chú rõ.
- Không có automatic retry loop; không scheduled re-trigger.

## 3. Idempotency & chống vòng lặp
- Mọi mutation của bot phải: (a) có evidence_id theo run; (b) kiểm tra tồn tại trước khi ghi, nếu trùng thì cập nhật/thay thế; (c) dùng [skip ci] trong commit nếu là mutation chỉ mang style.
- Bot mutation cap: tối đa 1 commit mutation tự động mỗi run; nếu cần lần 2 thì dừng lại và mở diagnostics issue.
- GITHUB_TOKEN push không trigger workflow — đây là an toàn có sẵn; tuyệt đối KHÔNG dùng PAT cá nhân thay thế vì PAT push sẽ trigger workflow.

## 4. Diagnostics issue
- Tạo khi FAIL với: run URL, SHA, trích output, danh sách job. Gán actor chờ xử lý, gắn label w118-blocked.
- Giới hạn tạo mới: KHÔNG tạo issue mới nếu đã có issue mở cùng (workflow, run-workflow-name, SHA) — kiểm tra bằng search trước khi tạo.

## 5. Không merge tự động
- Dù CI xanh, merge chỉ sau review của actor khác người push (trả lời câu hỏi 5-6 BB-118-001).


## Amendment — Auto E2E v2 diagnostics idempotency (2026-11-20)

- Failure diagnostics runs in a separate workflow, not in the orchestrator workflow. It listens to W118 Auto E2E Validation, the legacy W118 pilot during migration, W300 Dashboard CI and Work 70 Preview Host Tests. It does not listen to itself.
- Diagnostic issue key: `workflow_id + head_sha`. Repeated runs for the same workflow and commit reuse one open `w118-blocked` issue.
- Diagnostic update marker: `run_id + run_attempt`; repeated delivery of the same attempt is ignored, while a new attempt is recorded separately.
- Handoff marker: issue number + GitHub label ID + issue.updated_at (distinguishes a later remove/re-apply cycle while deduplicating the same event delivery). ACK result marker: source comment ID. These markers prevent duplicate comments on event redelivery/re-run.
- Concurrency groups serialize mutations for the same issue/event or workflow/commit key.
- No automatic retry is implemented. Retry remains actor-approved, reasoned and bounded to two attempts under the existing policy.
- Unit tests cover key stability, workflow/SHA separation, existing issue reuse, attempt-specific markers and invalid key rejection. Real workflow_run runtime remains pending deployment.
