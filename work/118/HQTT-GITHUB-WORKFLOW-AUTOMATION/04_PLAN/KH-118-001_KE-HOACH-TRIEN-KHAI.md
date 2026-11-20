# KH-118-001 — KẾ HOẠCH TRIỂN KHAI WORK 118

## Mục tiêu
Thiết kế và kiểm chứng có kiểm soát cơ chế điều phối GitHub → ROOM-HOP → CI → review → Work evidence.

| WP | Hạng mục | Đầu ra | Trạng thái |
|---|---|---|---|
| W118-01 | Kiểm kê hiện trạng GitHub và Work 70 | Danh mục workflow, events, quyền, CI, API, gaps | DONE 2026-11-20 — [EVIDENCE/W118-01_GITHUB_DISCOVERY_20261120.md](../EVIDENCE/W118-01_GITHUB_DISCOVERY_20261120.md); gap chính: 0/8 cơ chế event-driven tồn tại; BLOCKED phụ: secrets/webhook cấp repo cần Vinh xác nhận |
| W118-02 | Chuẩn hóa Issue/Branch/Commit/PR | Quy ước và templates | DRAFT 2026-11-20 — [QC-118-002](../02_DEFINE/QC-118-002_QUY-UOC-ISSUE-BRANCH-COMMIT-PR.md); templates chỉ tạo sau G3 |
| W118-03 | Thiết kế CI và evidence contract | Ma trận jobs, artifacts, SHA, logs, exit code | DRAFT 2026-11-20 — [TD-118-004](../02_DEFINE/TD-118-004_THIET-KE-CI-EVIDENCE-CONTRACT.md); cần extension schema v1.2 |
| W118-04 | Thiết kế event orchestration | Event → actor → action → permission → result | DRAFT 2026-11-20 — [TD-118-005](../02_DEFINE/TD-118-005_THIET-KE-EVENT-ORCHESTRATION.md); ACK magic-token |
| W118-05 | Thiết kế failure/retry/idempotency | State machine và giới hạn retry | DRAFT 2026-11-20 — [TD-118-006](../02_DEFINE/TD-118-006_THIET-KE-FAILURE-RETRY-IDEMPOTENCY.md) |
| W118-06 | Thiết kế review/acceptance/merge gates | Gate matrix và quyền phê duyệt | DRAFT 2026-11-20 — [TD-118-007](../02_DEFINE/TD-118-007_THIET-KE-GATE-MATRIX.md) |
| W118-07 | Thiết kế audit journal/dashboard | Data contract và provenance | DRAFT 2026-11-20 — [TD-118-008](../02_DEFINE/TD-118-008_THIET-KE-AUDIT-DASHBOARD-CONTRACT.md) |
| W118-08 | Phản biện và chốt kiến trúc | Biên bản kiến trúc được duyệt | IN PROGRESS — DC-118-003 + TD-118-004..008 đủ bộ hồ sơ chờ Ka review / Xu tổng hợp / Vinh ACK |
| W118-09 | Pilot có giới hạn | CI/event flow chạy thật trong phạm vi thử nghiệm | RUNTIME VERIFIED 2026-11-20 — run #2 SUCCESS 6s + bot comment bằng chứng trên Issue #65; trình Xu nghiệm thu (G4/G5) |

## Cổng kiểm soát
- G0: xác nhận hiện trạng và phạm vi.
- G1: yêu cầu và state machine được xác định.
- G2: kiến trúc, bảo mật, quyền và evidence contract được phản biện.
- G3: Vinh phê duyệt trước BUILD — APPROVED 2026-11-20 by explicit owner delegation to Ka for Auto E2E build; security and acceptance gates remain mandatory.
- G4: pilot end-to-end có bằng chứng thật.
- G5: nghiệm thu độc lập trước khi mở rộng.

## Quy tắc thực hiện
- Không triển khai trước G3.
- Không coi trạng thái CI xanh là nghiệm thu sản phẩm.
- Không merge tự động trong pilot.
- Không ghi PASS nếu thiếu run URL, commit SHA, logs và kết quả thực tế.
- Mọi blocker phải nêu: vấn đề / bằng chứng đã thử / nút thắt / phương án / điều kiện còn thiếu.


## Amendment — BUILD authorization and Auto E2E v2 (2026-11-20)

Vinh has explicitly delegated technical decisions and implementation of the Auto E2E system to Ka through the acceptance handoff. Xu and Vinh retain acceptance authority; Ka must not self-accept or self-release.

| WP | Hạng mục | Đầu ra | Trạng thái |
|---|---|---|---|
| W118-10 | Auto E2E v2 implementation | Role authorization, event handlers, failure diagnostics, CI evidence artifact, contract tests and runtime matrix | BUILD IN PROGRESS on `work/118-auto-e2e-v2` |
| W118-11 | Real GitHub event E2E | Handoff, ACK allow/deny, duplicate delivery and failure diagnostics runtime evidence | PENDING controlled deployment after Xu review |
| W118-12 | Acceptance and release handoff | Independent Xu review, Vinh final acceptance, release evidence bundle | PENDING |

**G3:** owner BUILD authorization recorded. This does not authorize auto-merge, release, secrets/branch-protection changes or modifications to Work 70's evidence schema.

**Current CI:** Run `44746143577` SUCCESS; 26 unit/contract tests passed. This is contract-level evidence only, not full runtime E2E.

**Current blockers:** verified GitHub login for Xu; executor identity mappings for Ka/Vi/An (no guesses); Work 70 approval for any Evidence Register schema extension; actual diagnostics runtime after listener deployment.


## Review handoff update — 2026-11-20

- Active build branch: `work/118-auto-e2e-v2`, 46 commits ahead / 0 behind main at PR creation.
- Draft PR: [#67](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/pull/67), open and mergeable; awaiting Xu independent review and Vinh final acceptance.
- Latest CI: Run `44747085807` SUCCESS, 30 tests passed; artifact ID `14632579474`.
- PR #66 remains unmerged and is preserved as the earlier pilot history; do not merge it as the implementation branch.
- Real issue/comment and workflow_run runtime E2E is the next implementation/verification gate after the reviewed integration is authorized.


## Security verification update — 2026-11-20

Principal-level self-review hardening is implemented and verified by [Run #44747589539](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44747589539): 32 tests PASS; evidence artifact ID `14634211524`. This closes the identified same-owner multi-login bypass at unit/contract level. Runtime review event and Xu identity mapping remain pending; no acceptance or merge state is inferred.


## Latest CI / PR state — 2026-11-20

- [Run #44747797589](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44747797589): SUCCESS, 32 tests passed, artifact ID `14634046784`.
- PR #67 is OPEN / DRAFT / mergeable=true; branch `work/118-auto-e2e-v2` is 65 ahead / 0 behind main.
- Same-principal cross-account self-review denial is implemented and tested.
- Xu's independent review and Vinh's final acceptance are still pending. Real issue/comment and diagnostics runtime tests remain after approved default-branch integration.


## Xu review package update — 2026-11-20

- Added P0 review checklist `XR-118-001` with 12 ordered gates covering design, identity, ACK, self-review, idempotency, failure/retry, controlled fault injection, least privilege, evidence, cross-Work boundary, runtime E2E and release.
- Latest completed CI [Run #44748049548](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44748049548): SUCCESS, 36 tests passed; artifact ID `14633817327`.
- PR #67 remains DRAFT for Xu independent review. Vinh final acceptance and main integration remain pending.


## Event automation verification update — 2026-11-20

- [Run #44748965030](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44748965030): SUCCESS; 44 tests passed; artifact ID `14634556693`.
- Authorized ACK applies `w118-acked` only after role authorization; handoff/ACK/review event artifacts remain RECORDED and outside Work 70 register.
- PR checklist notifier is isolated in `pull_request_target` and does not checkout/execute PR code. The normal pull_request job stays read-only.
- PR #67 remains DRAFT, 89 commits ahead / 0 behind main. Xu independent review and Vinh final acceptance are pending.


## Latest provenance verification — 2026-11-20

- Run [#44749396083](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44749396083) SUCCESS; 45 tests passed; artifact ID `14635085374`.
- Run evidence binds source commit and tested commit separately, plus actor, repository, ref, run URL and PR metadata.
- Failure diagnostics now subscribes to the W118 PR checklist workflow as well as W118, W300 and Work 70, without self-listening.
- PR #67 remains DRAFT, mergeable, 102 ahead / 0 behind main. Runtime event E2E, Xu review and Vinh acceptance remain pending.


## Staged gate clarification — 2026-11-20

To test the workflow_run listener on real GitHub events, the workflow must be present on the default branch. The gate is split: Xu design/security review → Vinh explicit non-release integration authorization → Ka runtime E2E → Xu runtime evidence review → Vinh final product acceptance → separate release decision. Merge alone does not set ACCEPTED/RELEASED. No integration is performed without the explicit Vinh authorization at Stage B.


## Xu review readiness — 2026-11-20

- Latest CI [Run #44749959595](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44749959595): SUCCESS; 45 tests passed; artifact ID `14635085964`.
- PR #67 is 116 ahead / 0 behind main, OPEN / DRAFT / mergeable; 30 files changed.
- Stage A (Xu independent design/security review) is ready. Stage B (Vinh non-release integration authorization) is not yet granted. Runtime tests remain pending integration; no final acceptance/release is claimed.


## Stage A handoff — 2026-11-20

PR #67 is OPEN / READY FOR REVIEW / mergeable=true. Latest CI Run #44750129069 SUCCESS, 45 tests passed, artifact ID `14634847057`. Xu's independent design/security review is requested. Vinh's explicit Stage B non-release integration authorization is still pending. Ka has not merged or released the Work.


## Final pre-review CI — 2026-11-20

Run [#44750267341](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44750267341) SUCCESS; 45 tests passed; artifact ID `14634727841`. PR #67 is OPEN / READY FOR REVIEW / mergeable=true; 123 commits ahead / 0 behind main. No Xu review has been submitted yet; no Vinh integration authorization or merge has occurred.


## Latest ready-for-review validation — 2026-11-20

Run [#44750417015](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44750417015) SUCCESS; 45 tests passed; artifact ID `14635330750`. PR #67 remains READY FOR REVIEW, 126 ahead / 0 behind main. Xu Stage A review and Vinh Stage B non-release integration authorization are pending; no merge or release.


## P0 remediation — review policy provenance (2026-11-20 21:39 UTC+07:00)

- **Finding:** the `pull_request_review` job used unqualified checkout; the event ref can be the PR merge ref, so PR-controlled role-map/authorization files could influence reviewer authorization.
- **Decision:** Ka treats this as P0 and fixes before Xu review handoff is considered technically ready.
- **Implementation:** checkout is pinned to `${{ github.event.repository.default_branch }}`; `persist-credentials: false`; regression test T10-19 asserts both controls.
- **Commits:** workflow `032f56d1fae57a53380327ffc02dc151f313408f`; regression test `a5c4c52ef660c60e98c480f5bc63bfaf26e81d1e`; test matrix `5d11e4b99696ebe07990b468449ae492df71484e`; implementation note `8c9f5a8ce62083028a590865979575314483e41a`.
- **CI:** PR run `44755364888` is IN_PROGRESS at this log update; no PASS is claimed.
- **Next:** inspect job result and test count; if PASS, continue full workflow security audit and refresh PR review package. Runtime event E2E still requires Xu review and separate Vinh non-release integration authorization.


## P0 remediation verification — 2026-11-20

- Run [#44755364888](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44755364888): validate SUCCESS; 46 tests PASS in 0.234s.
- T10-19 trusted review-policy provenance regression PASS.
- Artifact ID `14636718273`; SHA-256 `c5b8d9a860c111079304579d74213ff516fe1016952bd74756aac4719b670689`.
- Event-specific jobs were skipped; runtime event E2E remains PENDING. Xu review and Vinh Stage B non-release integration authorization remain outstanding.


## P0 remediation — ACK Work-scope boundary (2026-11-20)

- **Finding:** ACK authorization previously validated actor, role and Issue number binding but did not require the Issue itself to be a W118 handoff. A mapped executor could therefore cause a W118 ACK label on an unrelated repository Issue.
- **Decision:** fail closed unless the source Issue carries `w118-handoff` and is not a PR.
- **Implementation:** ACK job event condition now enforces both constraints; regression test T10-20 added.
- **Commits:** workflow `d43c21d327b1e93722ff2fb1861c458f04cb7517`; test `6db3296e663b27008d9269cd191ac2edea990b6f`; matrix `57aca3ee00497283b2f19e9beebc999a968b6c63`; implementation note `fd02875638c07590620f635c9fd7a12c8fb9ee4f`.
- **CI:** awaiting PR synchronize validation; no PASS claimed for T10-20 yet.
- **Next:** verify CI and continue event-scope/security audit. Runtime E2E remains gated by Xu review and Vinh Stage B authorization.


## ACK Work-scope remediation verification — 2026-11-20

- Run [#44755648230](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44755648230): validate SUCCESS; 47 tests PASS in 0.319s.
- T10-20 PASS: ACK job requires `w118-handoff` label and rejects PR events.
- Artifact ID `14637735820`; SHA-256 `c4ec772682b4a967d903ded718af9ed806f3c37af614394d486e7b746ecbd79c`.
- Event-specific jobs remain SKIPPED on PR synchronize; runtime event E2E remains PENDING.


## P0 remediation — independent-review authority separation (2026-11-20)

- **Finding:** the review event used `can_accept`, conflating Vinh's final product acceptance authority with Xu's independent review authority.
- **Decision:** add separate `can_independently_review` permission; review authorization must not rely on `can_accept`. Owner logins retain final acceptance permission and are explicitly denied independent-review permission. Xu remains unmapped until identity confirmation.
- **Implementation:** role-map schema validation, authorizer, review CLI and tests updated; XR-118-001 gate 16 added.
- **CI:** Run [#44755930029](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44755930029) SUCCESS; 47 tests PASS in 0.229s; artifact ID `14637227755`.
- **Intermediate CI:** Run #44755893780 failed during sequential refactor because the function rename reached the source before the two test imports were updated; final test commit corrected both imports and Run #44755930029 passed. No unresolved test failure is hidden.
- **Runtime:** real review event and verified Xu identity remain BLOCKED/PENDING; no runtime PASS.


## Role-map schema 1.1 verification — 2026-11-20

- Run [#44756198541](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44756198541): validate SUCCESS; 48 tests PASS in 0.321s.
- Role map schema 1.1 requires `can_independently_review`; missing-field rejection T10-22 PASS.
- Artifact ID `14638126091`; SHA-256 `681be1785735281a936d774f0de422c973fc9dc48871c53262d10c26dfe1fabf`.
- Event-specific jobs remain SKIPPED; runtime E2E remains PENDING.


## P0 remediation — review event evidence provenance (2026-11-20)

- **Finding:** after pinning review authorization to the trusted default branch, the event evidence still used `github.sha` (PR merge/event SHA) as `source_commit`, which did not identify the policy revision actually used.
- **Decision:** evidence must distinguish policy source commit from PR/event revisions.
- **Implementation:** resolve checked-out policy SHA; set it as `source_commit`; record event SHA, PR head SHA and PR base SHA in artifact details; add T10-23 contract test and XR checklist gate 17.
- **CI:** regression test committed; validation pending. No PASS claim.
- **Next:** verify CI and inspect resulting run artifact schema. Runtime review event remains pending default-branch integration.


## Review evidence provenance verification — 2026-11-20

- Run [#44756410351](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44756410351): validate SUCCESS; 49 tests PASS in 0.207s.
- T10-23 PASS: review evidence binds the trusted policy commit separately from event, PR head and PR base SHAs.
- Artifact ID `14638351674`; SHA-256 `c13688e45484886f302aac1046464587c821a098488259f447442409b0b51a9a`.
- Event-specific jobs remain SKIPPED; runtime review event E2E remains PENDING.


## P0 remediation — direct fault-injection dispatch authorization (2026-11-20)

- **Finding:** owner-only issue-comment dispatch could be bypassed by a repository writer directly invoking `workflow_dispatch` with `failure_injection=controlled`.
- **Decision:** authorize the actor again inside the controlled-failure job using the trusted default-branch role map; do not rely solely on the upstream dispatcher.
- **Implementation:** direct dispatch job checks out default-branch policy, validates `github.actor` with `controlled_test_authorization.py`, and executes exit code 17 only when authorization output is true. Added T10-24 and XR checklist gate 18.
- **CI:** regression test committed; validation pending. No PASS claim.
- **Next:** verify CI and retain fail-closed behavior for unknown actors.


## Direct fault-injection authorization verification — 2026-11-20

- Run [#44757234204](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44757234204): validate SUCCESS; 50 tests PASS in 0.201s.
- T10-24 PASS: direct workflow_dispatch requires a trusted default-branch actor authorization result before failure injection.
- Artifact ID `14638571210`; SHA-256 `0dd1c6dc177ea53d6f64e231b7367e36dbce348b374b36c73c69abf8df4274a8`.
- Runtime propagation of the actor from the owner-comment dispatcher remains unverified until the controlled workflow is executed after approved integration.


## P1 remediation — diagnostics idempotency across closure (2026-11-20)

- **Finding:** diagnostics queried only open `w118-blocked` Issues; a repeated failure with the same workflow ID + SHA after closure could create a duplicate.
- **Decision:** idempotency key must remain unique across Issue state changes.
- **Implementation:** query all Issue states; reuse and reopen the existing Issue when a new run attempt arrives; add T10-25 and XR checklist gate 19.
- **CI:** regression test committed; validation pending. No PASS claim.


## Diagnostics idempotency across closure verification — 2026-11-20

- Run [#44758004387](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44758004387): validate SUCCESS; 52 tests PASS in 0.394s.
- T10-25 PASS: closed diagnostic Issue is found by the stable workflow ID + commit SHA key; workflow reopens/updates rather than creating a duplicate.
- Artifact ID `14640485869`; SHA-256 `b029bddc43da57df2b0199b1dde40987fbe096ed82dda23f2f4571fa5f2ec949`.
- Intermediate Run #44757920850 failed due to an over-specific contract assertion; assertion corrected and final run passed.
- Actual workflow_run failure event remains pending controlled runtime execution.
