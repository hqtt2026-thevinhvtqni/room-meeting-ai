# TD-118-005 — THIẾT KẾ EVENT ORCHESTRATION (W118-04)

- **Work:** W118
- **Ngày:** 2026-11-20
- **Trạng thái:** DRAFT — chờ phản biện.

## 1. Ma trận sự kiện v1 (GitHub-native, không webhook)
| Sự kiện | Điều kiện | Hành động tự động | Actor chịu trách nhiệm |
|---|---|---|---|
| issue.opened + label handoff | label do người gán | workflow comment hướng dẫn nhận việc mới | Xu tổng hợp |
| issue_comment có magic-token | body đầu chứa "ACKED-<role> <số issue>" | tick nhận việc, ghi evidence row OPERATION | actor AI được mapping |
| pull_request.opened | title có mã Work | auto-gán checklist review độc lập | reviewer chỉ định |
| push trên main chạm path Work | có evidence-write job | ghi evidence row RUNTIME | bot evidence |
| workflow failure | bất kỳ job FAIL | diagnostics issue + label blocked theo TD-118-006 | actor pending |

Trong v1 KHÔNG có hoạt động mutation tự động nào khác; mọi mutation vẫn cần người/AI comment ACK kèm bằng chứng.

## 2. Xác thực nhận việc (trả lời câu hỏi 2 BB-118-001)
- Assignee GitHub chỉ là đề cử. Nhận việc chỉ có hiệu lực khi có comment magic-token ACKED-<ROLE> <so issue> từ chính actor AI (tạo bởi hệ thống của nó, không phải người gõ thay).
- Workflow nhận comment kiểm tra author + so với mapping role cố định trong file cấu hình docs của Work (role → github login), sau đó ghi evidence row OPERATION (state RECORDED). Không khớp thì chỉ cảnh báo, không tick.

## 3. Anti-spoof
- Token ACK chỉ hợp lệ khi comment do chính tác nhân tạo, hoặc được người đúng role trong mapping xác nhận lại ít nhất 1 lần trong cùng Work.
- V1 chọn phương án đơn giản: mapping role-file + người reviewer xác nhận role của GitHub login lần đầu xuất hiện.

## 4. Giới hạn v1
- ROOM-HOP không nghe realtime: state sync chỉ qua evidence register và Dashboard đọc từ đó.
- Event không có label/magic-token bị bỏ qua cố ý (fail-closed).


## Amendment — Auto E2E v2 actor and event policy (2026-11-20)

- Handoff is triggered only by an Issue `labeled` event with `w118-handoff`; the output comment is deduplicated by issue number + label ID + `issue.updated_at` (distinguishes a later remove/re-apply cycle while deduplicating the same event delivery).
- ACK is accepted only when the full comment body matches `ACKED-<role> <issue-number>`, the issue number matches the event, and the GitHub login is active and explicitly mapped to that ACK role.
- A valid GitHub login is not automatically an authorized ROOM-HOP role. Unknown login, inactive account, wrong role or issue mismatch is denied; the workflow records `ACK UNVERIFIED` and makes no assignment/state transition.
- Vinh's two confirmed GitHub logins map to the same owner principal for acceptance only. They have no execution ACK roles.
- Xu's GitHub login and execution-agent logins are not guessed. They remain unconfigured until verified and approved.
- Pull request review events are recorded only for mapped acceptance reviewers who are not the PR author. The workflow does not merge.
- Output comments are deduplicated by source comment/review ID. Bot-generated output does not match the ACK prefix and cannot recurse into ACK handling.


## Amendment — event evidence and PR checklist hardening (2026-11-20)

- Authorized ACK now applies the `w118-acked` Issue label only after actor, role and Issue binding pass. Unauthorized ACK records `ACK UNVERIFIED` and does not mutate Issue state.
- Handoff, ACK and PR review events write a separate immutable OPERATION event artifact bound to source event ID, run ID/attempt, actor, decision and source SHA. State remains RECORDED; no Work 70 register write is performed.
- PR checklist notification is isolated in `w118-pr-review-checklist.yml` using `pull_request_target`, with only `contents: read` and `issues: write`, same-repository PR scope, and no checkout or execution of PR code. It posts one checklist comment per PR head SHA.
- The ordinary `pull_request` validation workflow remains read-only. A failed attempt to comment from pull_request context confirmed the repository token was read-only; the write action was moved to the safe base-context workflow rather than requesting broader token access.
