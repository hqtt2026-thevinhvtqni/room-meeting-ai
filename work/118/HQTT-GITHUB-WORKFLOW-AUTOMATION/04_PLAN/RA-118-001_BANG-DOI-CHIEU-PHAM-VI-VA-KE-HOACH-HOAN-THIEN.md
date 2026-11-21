# RA-118-001 — BẢNG ĐỐI CHIẾU PHẠM VI W118 VÀ KẾ HOẠCH HOÀN THIỆN

- **Work:** W118 — HQTT GitHub Workflow Automation
- **Priority:** P0
- **Read order:** 12
- **Name:** Ka / AI-02
- **Title:** CSA / W118 Build Owner (được Vinh ủy quyền)
- **Date-Time:** 2026-11-21 10:15 +07:00
- **State:** DRAFT FOR XU INDEPENDENT REVIEW — không phải nghiệm thu
- **Scope:** Issue #65; không tạo Work mới; không merge/rebase/release.

## 1. Kết luận điều hành

W118 có hai tầng mục tiêu phải nghiệm thu riêng:

1. **Auto E2E / workflow automation:** xử lý một số GitHub events, xác thực ACK/reviewer, chạy CI contract tests, lưu artifact và tạo/cập nhật diagnostics Issue.
2. **HQTT Work Management end-to-end:** quản lý vòng đời nhiệm vụ từ Issue → phân loại → chọn/dispatch AI → ACK → thực thi/progress → Branch/Commit/Push → CI feedback → Work Journal/Evidence → Dashboard.

W118-10 hiện chủ yếu xây tầng 1. Tầng 2 chưa được triển khai hoặc chưa có bằng chứng đủ để xác nhận. Vì vậy W118 tổng thể chưa hoàn thành. CI xanh không thay thế xác minh runtime, quản lý công việc hay nghiệm thu.

## 2. Nguồn đối chiếu và snapshot

### 2.1 Nguồn đã đọc

- GitHub Issue #65 — mục tiêu, phạm vi, nguyên tắc và tiêu chí hoàn thành.
- W118 README — chuỗi Issue → Assignment → Branch → Commit/Push → CI → Failure/Review → Acceptance → Merge → Journal/Dashboard.
- KH-118-001 — W118-01..12; W118-10 Auto E2E v2, W118-11 runtime event E2E, W118-12 acceptance handoff.
- TD-118-005 — event orchestration, handoff label và ACK role-map.
- TD-118-008 — Evidence Register là nguồn dữ liệu cấu trúc; Dashboard Work 70 là read-only projection; schema extension cần Work 70 ACK.
- Workflow, role-map, scripts, test matrix, PR #67 và CI run exact-head.

### 2.2 Snapshot GitHub — 2026-11-21 10:15 +07:00

- PR #67: OPEN, draft=false, merged=false; formal review submissions = 0; inline review threads = 0.
- Feature HEAD: b694abe80d2c9f86871f7303543dd234da2bd205.
- Main HEAD: 61939922098a6f8e8b3d0c5fe34511c3e57aa838.
- Merge base: cf2537e07bfd71d5823bd98f8673b3ab5644fcdc.
- Compare: **278 ahead / 84 behind — DIVERGED**. Không rebase/merge trong đợt đối chiếu.
- Exact-head PR validation: [Run #44860083377](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44860083377), tested SHA khớp feature HEAD; validate SUCCESS.
- Artifact: w118-run-evidence-44860083377-1, ID 14689611980, SHA-256 8cf8ad90845070b4ccc38e5a019dd8f159d5077b44945a2cd46cecebdee4a382, chưa hết hạn tại readback.
- Trong run này, handoff, ack-verification, acceptance-review, controlled-failure và controlled-failure-dispatch đều SKIPPED. Đây là CI contract evidence, không phải runtime event E2E.

## 3. Bảng đối chiếu yêu cầu — triển khai — bằng chứng

| Lớp | Yêu cầu W118 | Đã triển khai / bằng chứng | Thiết kế nhưng chưa hoàn thiện | Chưa có hoặc chưa chứng minh | Kết luận |
|---|---|---|---|---|---|
| Issue Management | Issue có Work, mục tiêu, scope, priority, owner/AI, acceptance, risk và liên kết | Issue #65 tồn tại; label w118-handoff; workflow comment ghi nhận label event và chống duplicate | TD-118-005 có handoff event; README mô tả Issue → Assignment | Chưa có bằng chứng template/validator chuẩn hóa đủ trường; chưa chứng minh phân loại Work/priority; Issue #65 không có assignee | PARTIAL |
| AI Assignment | Chọn AI theo role/capability/availability; dispatch; lưu owner | Role-map schema 1.1 deny-by-default; ACK authorization parser; tách owner/reviewer | TD-118-005 mô tả ACK theo role-map; unit fixtures có mapped/unmapped actor | Role-map hiện chỉ có 2 login Owner Vinh, ack_roles rỗng; chưa có executor registry, capability, availability, queue, dispatch, assignment record hoặc reassignment policy | NOT IMPLEMENTED / BLOCKED |
| ACK | AI thực sự nhận việc bằng danh tính xác minh | Workflow kiểm tra ACKED-role + Issue; yêu cầu label w118-handoff; có OPERATION artifact và label w118-acked nếu được phép | Contract tests cho allow/deny/duplicate và provenance | Event runtime exact branch chưa chạy; không có executor login trong role-map để chứng minh positive production ACK | CONTRACT PARTIAL; RUNTIME NOT VERIFIED |
| Execution Tracking | Biết AI nhận, bắt đầu, đang làm, hoàn tất, bị kẹt; timeout/heartbeat/reassign | Có handoff/ACK markers và event evidence builder | Có khái niệm handoff/ACK và failure diagnostics | Chưa thấy state machine STARTED/IN_PROGRESS/COMPLETED/BLOCKED, heartbeat/lease, progress update, timeout/stale assignment hoặc recovery/reassignment | NOT IMPLEMENTED |
| Branch / Commit / Push | Liên kết Issue ↔ Branch ↔ Commit ↔ Push | Push/PR triggers có path filters; CI evidence lưu actor, ref, source/tested SHA, PR metadata khi có PR | README nêu lifecycle; KH-118-001 có W118-02 QC draft | Chưa có cơ chế bắt buộc/kiểm tra Issue key trong branch/commit; push evidence không có Issue binding khi push độc lập; chưa có liên kết Issue–branch–commit hoặc cập nhật trạng thái Issue theo push | PARTIAL |
| CI execution | Chạy CI cho thay đổi thuộc phạm vi | Validate chạy thật; exact-head run #44860083377 SUCCESS; artifact tồn tại | Failure diagnostics workflow theo workflow_run và idempotency key | Exact-head run chỉ có validate SUCCESS; năm event jobs SKIPPED; chưa chứng minh trigger/coverage đầy đủ theo Issue/Work | PARTIAL — CONTRACT CI PASS |
| CI FAIL feedback | Tạo/cập nhật diagnostics, giao đúng tác nhân, retry có giới hạn | Diagnostics planner có key workflow ID + SHA; unit/contract test chống duplicate kể cả Issue đóng; nội dung diagnostics ghi Fix owner UNASSIGNED | Retry tối đa 2 lần có actor approval được mô tả | Runtime workflow_run chưa xác minh; diagnostics không tự phân công owner/AI; chưa dispatch nhiệm vụ sửa lỗi về đúng tác nhân | PARTIAL — RUNTIME NOT VERIFIED |
| CI PASS feedback | Cập nhật trạng thái task/Work và chuyển review | Artifact ghi CI_CONTRACT / RECORDED, tách khỏi OPERATION | TD-118-008 đề xuất Evidence Register row và reconciliation | Chưa có CI PASS → task state transition; chưa có review task tự động được tạo/assigned theo policy; chưa cập nhật Work status | NOT IMPLEMENTED |
| Work Journal / Evidence | Audit actor, action, provenance, result, immutable history | Có journal append-only và artifact CI/OPERATION | TD-118-008 quy định evidence contract | Tự động đồng bộ artifacts vào canonical Work Evidence Register chưa được phép/chưa có schema ACK; artifact không tự động là Work journal row | PARTIAL |
| Work Dashboard | Một nơi xem task, assignee, ACK, progress, CI, blocker, evidence | TD-118-008 xác định Dashboard Work 70 là read-only projection | Contract dự kiến dùng Evidence Register làm nguồn dữ liệu | Chưa có tích hợp Assignment/Execution lifecycle; schema extension và projection chưa được xác minh/ACK; chưa có bằng chứng Dashboard hiển thị các trạng thái này | NOT IMPLEMENTED / BLOCKED |

## 4. Ranh giới bắt buộc

1. GitHub Assignee ≠ AI ACK. Assignee chỉ là chỉ định; ACK cần actor identity, role, Issue và nguồn phát sinh được xác minh.
2. ACK ≠ Started. Nhận việc và bắt đầu thực thi là hai sự kiện riêng.
3. Push ≠ Issue linkage. Phải ràng buộc Issue/Work ID trong branch/commit/PR và kiểm tra tại CI.
4. CI PASS ≠ Work complete. CI là tín hiệu chất lượng, không tự đóng task/Work.
5. Artifact ≠ Dashboard update. Artifact không tự động cập nhật Evidence Register hoặc Dashboard.
6. Review ≠ Acceptance ≠ Merge ≠ Release. Xu giữ review độc lập; Vinh giữ nghiệm thu cuối và quyết định release.
7. No guessed identities. Không tự thêm login Xu, Go, Ka, Vi, An hoặc Agent khác khi chưa xác minh danh tính/quyền.
8. Work 70 remains source of truth. Không tạo Dashboard thứ hai, không sửa schema/register Work 70 khi chưa có phê duyệt.

## 5. Kế hoạch hoàn thiện đề xuất trong chính W118

Các gói dưới đây là đề xuất để Xu phản biện; chưa phải quyết định kiến trúc cuối cùng và chưa mở implementation cho phần cần contract mới.

| Thứ tự | Gói đề xuất | Đầu ra bắt buộc | Điều kiện đóng |
|---|---|---|---|
| P0 / 1 | W118-13 — Issue & Task Contract | Template/validator; Work ID, priority, scope, acceptance, capability requirement; canonical state model | Xu review state/transition; Issue round-trip tests |
| P0 / 2 | W118-14 — Agent Registry & Assignment | Agent principal registry; role/capability; availability/health; deterministic matching; assignment record; dispatch receipt; reassignment/lease policy | Tests candidate selection, no capability, offline, duplicate dispatch, unauthorized assignment |
| P0 / 3 | W118-15 — ACK & Execution Lifecycle | Tách ASSIGNED, DISPATCHED, ACKED, STARTED, IN_PROGRESS, BLOCKED, COMPLETED, CANCELLED/EXPIRED; heartbeat/progress; timeout/recovery | Positive/negative runtime E2E, stale lease, crash-window, spoof, concurrency, audit |
| P0 / 4 | W118-16 — Issue–Branch–Commit–Push Binding | Branch/commit convention; parser/validator; liên kết Issue/PR/SHA; push event cập nhật execution record | Missing/invalid/multiple Issue binding tests; exact-SHA push E2E |
| P0 / 5 | W118-17 — CI Feedback & Failure Routing | CI PASS/FAIL callback; task-state update theo policy; diagnostics gắn assignment; retry cap; owner approval | CI PASS/FAIL thật; dedup; đúng Issue/Agent; không retry vô hạn |
| P0 / 6 | W118-18 — Work 70 Evidence & Dashboard Projection | Mapping OPERATION/CI_CONTRACT vào Evidence Register theo schema được duyệt; read-only dashboard view | Work 70 schema owner ACK; data parity; stale/missing evidence reconciliation; Dashboard readback |
| P0 / 7 | W118-19 — Full Lifecycle Acceptance | E2E toàn chuỗi; fault injection; security/permission matrix; runbook; acceptance bundle | Go / AI-06 QE độc lập theo D70-026; Xu technical/security review; Vinh product acceptance |

### Trình tự

- **Gate A — Xu review:** phản biện scope, state machine, trust boundary, identity/dispatch model, Work 70 boundary và tiêu chí đo lường. Không tự coi đề xuất đã được phê duyệt.
- **Gate B — Contract approval:** chốt schema, event contract, authority, idempotency, retry, evidence và dashboard projection.
- **Gate C — Implementation:** xây theo thứ tự W118-13 → W118-18 trên branch riêng; giữ nguyên main, không merge/release.
- **Gate D — QE / adversarial verification:** Go / AI-06 là default QE/QA theo D70-026; cần xác minh login và dispatch/access riêng, không suy ra từ vai trò.
- **Gate E — Xu review và Vinh acceptance:** Xu review độc lập trên exact SHA; Vinh quyết định nghiệm thu sản phẩm.
- **Gate F — Runtime integration:** chỉ thực hiện khi có quyền/ủy quyền cần thiết; runtime test không đồng nghĩa release.

## 6. Tiêu chí nghiệm thu W118 tổng thể

- Tạo/chuẩn hóa Issue và xác định Work/priority/acceptance.
- Chọn AI theo capability + role + availability; assignment độc lập với GitHub Assignee.
- Chỉ ghi ACK khi actor AI thực sự xác thực; DISPATCHED, ACKED và STARTED có bằng chứng riêng.
- Theo dõi progress, heartbeat, completion, blocked, timeout và recovery.
- Mỗi branch/commit/push liên kết đúng Issue/Work; CI xác minh liên kết và ghi exact SHA.
- CI PASS/FAIL cập nhật đúng task lifecycle; FAIL giao nhiệm vụ sửa lỗi đúng tác nhân, có retry cap.
- Journal/Evidence Register/Dashboard dùng cùng nguồn dữ liệu, provenance và trạng thái; Dashboard là read-only projection.
- Duplicate, spoof, unauthorized, race, lost event, stale lease, missing evidence và crash-window có kiểm thử.
- Xu independent review PASS; Vinh product acceptance PASS; release là quyết định riêng.

## 7. Open blockers

- Executor AI GitHub identities và runtime dispatch route: chưa xác minh.
- Xu / Go GitHub identities và permission: chưa xác minh.
- Work 70 Evidence Register schema extension: chưa có bằng chứng ACK.
- Exact-head runtime event jobs: SKIPPED trong run #44860083377.
- PR branch diverged 278/84; không rebase/merge mù.
- Không tạo Work mới; không thay đổi Work 70 schema; không thêm secrets/permissions; không merge/release trong đợt này.

## 8. Hồ sơ lập đối chiếu

- **Name:** Ka / AI-02
- **Title:** CSA / W118 Build Owner (delegated)
- **Date-Time:** 2026-11-21 10:15 +07:00
- **Action:** Đối chiếu Issue #65, README, KH-118-001, TD-118-005/008, role-map, workflow, test matrix, PR #67 và exact-head CI.
- **Result:** W118-10 Auto E2E mới chứng minh một phần automation; Assignment, Execution Tracking, Issue–Push binding, CI feedback và Dashboard integration còn thiếu hoặc chưa chứng minh.
- **Disposition:** DRAFT FOR XU REVIEW; không tuyên bố PASS tổng thể; không merge/rebase/release.
