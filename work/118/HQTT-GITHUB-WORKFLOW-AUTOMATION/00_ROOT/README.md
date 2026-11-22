# W118 — HQTT GitHub Workflow Automation

**Selected architecture:** A — Sandbox initiates; GitHub controls versioning.  
**Status:** ACTIVE — VERIFYING — NOT ACCEPTED — NOT RELEASED.  
**Implementation branch:** `work/118-auto-e2e-v2-clean`; [PR #68](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/pull/68) is OPEN / UNMERGED. PR #67 is superseded history.

## 1. Purpose

Build two connected workflows:
1. **Plan → Core Task → W102 Agent Loop → W14 Execute → Verify → Owner Accept → Close.**
2. **Sandbox → W14 → GitHub Branch/Commit/Push → GitHub Actions CI → W118 stateless adapter → Core Event → W102/W14 recovery.**

W118 owns GitHub-specific adapters and evidence only. It does not create another runtime Task database, Agent Registry, dispatcher, event queue/Event Bus, Execution Host, Git Gateway or CI engine.

## 2. Canonical ownership

- **W118 Task Register:** Work-specific planning tasks for W118, modeled on W70 DOC-093; not runtime Core Task state.
- **Core :8000:** sole canonical runtime Task/Assignment/Event authority.
- **W102:** Agent Loop policy, identity/capability routing and Assignment decisions.
- **W52:** provider-neutral communication contract reference (DRAFT).
- **W14:** sole product/delivery owner for integrated Work Authority, ExecutionHostBridge, GitHub Gateway and CI path.
- **W12/W13:** absorbed internal foundations under W14; not independent W118 integration owners.
- **W70:** Work lifecycle, Evidence Register and read-only Dashboard projection.
- **GitHub:** source/version, Issues/PRs, branches/commits, Actions runs and artifacts.

## 3. Official W118 documents

- [TD-118-012 — Dual closed-loop architecture v1.3](../02_DEFINE/TD-118-012_KIEN-TRUC-HAI-QUY-TRINH-KHEP-KIN-SANDBOX-GITHUB.md)
- [TASK_REGISTER.json — W118 Work planning register](../04_PLAN/TASK_REGISTER.json)
- [TASK_REGISTER.schema.json — Work planning schema](../04_PLAN/TASK_REGISTER.schema.json)
- [W118-13..17 — Core/GitHub adapter implementation](../05_BUILD/W118-13_17_CORE-GITHUB-ADAPTERS.md)
- [W118-13..17 — Core/GitHub adapter test matrix](../06_TEST/W118-13_17-CORE-GITHUB-ADAPTER-TEST-MATRIX.md)
- [KH-118-001 — Implementation plan](../04_PLAN/KH-118-001_KE-HOACH-TRIEN-KHAI.md)
- [Canonical Work Journal](../EVIDENCE/NHAT-KY-THI-CONG.md)

## 4. W118 adapter code

- `scripts/w118/core_task_adapter.py` — read-only Core Task snapshot normalization using an explicit Core-owner field map.
- `scripts/w118/github_issue_adapter.py` — Core Task to GitHub Issue mirror, requiring Core per-Task lock lease and exact readback.
- `scripts/w118/source_binding.py` — Task branch/commit/Issue/exact-SHA validation.
- `scripts/w118/github_webhook_verifier.py` — stateless HMAC-SHA256 and GitHub delivery envelope verification.
- `scripts/w118/github_event_adapter.py` — stateless push/CI/Issue event-to-Core intent mapping.
- `.github/workflows/w118-workflow-automation.yml` — CI contract and observation-only jobs.

The previous local SQLite TaskRegistry, durable webhook inbox, event reconciler and GitHub-login authorization scripts were removed. Core owns runtime state and event persistence.

## 5. GitHub observation policy

- `w118-handoff` label = handoff request only.
- `ACKED-...` comment = unverified ACK claim only; Core/W102 must verify principal.
- PR review event = review observation only; Core/W102 verifies reviewer authority.
- Push and CI = source/evidence observations only.
- No GitHub label/comment/Assignee/review directly changes Core Task or Assignment state.
- CI PASS is not Task DONE, Assignment ACCEPTED, merge or release.

## 6. Current implementation boundaries

**Runtime integration blocked**

- Core Task read API/schema/approved field map and per-Task lock are not exposed to W118.
- Core Event ingress/deduplication port is not exposed.
- W102 verified Agent identity/Assignment route is not available in current evidence.
- W14 canonical source/API/runtime parity and Work Authority/ExecutionHostBridge are not verified.
- No production webhook secret/TLS route, live Issue API round-trip, task-scoped push or full runtime E2E has been executed.
- Sandbox MCP in this session exposes file operations only; GitHub Actions executes the contract tests.

## 7. Current gates

| Gate | Status |
|---|---|
| Architecture / ownership alignment | **BASELINE SET BY VINH** |
| Core Task projection adapter | Contract tests; Core API field map pending |
| GitHub Issue mirror | Contract tests; live Core/GitHub lock and API pending |
| Source binding | Contract tests; task-scoped live push pending |
| Webhook/event adapter | Contract tests; Core event port pending |
| W102 identity/Assignment | **BLOCKED — Core/W102 integration** |
| W14 execution/GitHub/CI | **BLOCKED — host/adapter availability** |
| W70 Dashboard | **BLOCKED — schema/owner approval** |
| Full runtime E2E / Vinh acceptance | Not run |

No rebase, merge to main, release or branch-protection change is authorized by this Work state.


## Current autonomous build snapshot — 2026-11-22

- **Canonical PR:** [#68 — isolated W118 build](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/pull/68), branch `work/118-auto-e2e-v2-clean`, based on current Main with 1 commit ahead / 0 behind at isolation.
- **Exact-head CI:** Run [#44948921625](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44948921625), 94/94 contract tests PASS; artifact 14724581468. Event-specific jobs were skipped; runtime E2E is not claimed.
- **PR #67:** retained unmerged as superseded history because its branch contained unrelated Work changes and extensive divergence. Do not use it for integration.
- **Sandbox 04_CODE:** synchronized to the stateless Core/GitHub adapter implementation from PR #68. TD-118-012 v1.2 is controlling: no W118 Task DB, webhook inbox, durable event queue, Agent Registry, dispatcher, Execution Host, Git Gateway or CI engine.
- **Task Register:** Sandbox is operational source; GitHub is versioned mirror. Owner-directed build authorization is recorded without fabricating Agent identity, Assignment or ACK.
- **State:** ACTIVE — BUILD / VERIFY — NOT ACCEPTED — NOT RELEASED.


## Latest mainline synchronization — 2026-11-22

- Main HEAD: `792bdd71e5345949e0c1f26ff9f95a8513dfa7d5`.
- Active branch: `work/118-auto-e2e-v2-clean`; latest source commit at this update: `3bdde3221426a96db8c812185ee780283326ca4f`.
- Compare: 12 commits ahead / 0 behind; all 45 changed paths are W118-only.
- Latest completed validation: Run #44949848909, parent SHA `7ae56f961ec6908abc1060d321389b6d71d301cf`, 94 tests PASS; artifact 14724958058. The subsequent status-only commit does not change code; exact latest-head revalidation remains requested.


## Current handoff — 2026-11-22

- **PR #68:** READY FOR REVIEW / OPEN / UNMERGED; branch `work/118-auto-e2e-v2-clean`; based on Main `792bdd71e5345949e0c1f26ff9f95a8513dfa7d5`; 13 ahead / 0 behind; 45 changed paths, all W118-only.
- **Last exact tested code/documentation baseline:** SHA `052689084fba6f548df5c44637f652735628ad83`; Run #44949913071 SUCCESS; 94 tests PASS; artifact 14724444908.
- **PR #67:** CLOSED / UNMERGED / superseded; history preserved.
- **Sandbox parity:** Task Register/schema byte-identical; stateless code mirror aligned to TD-118-012 v1.2; retired local SQLite Task/event files absent.
- **Acceptance:** Xu independent review pending; Vinh product acceptance pending; no merge or release.


## Architecture ownership correction — 2026-11-22

W14 is the sole product/delivery owner for the integrated execution path. W12 and W13 are absorbed internal foundations, not independent product owners or direct W118 integration targets. W118 must consume W14's approved Work Authority and ExecutionHostBridge contract. W14 source parity and full runtime E2E remain NOT VERIFIED; W118-TASK-015 remains BLOCKED. No W12/W13 source modification or parallel host/Gateway is permitted.


## W14 dependency confirmation — 2026-11-22

W118-TASK-015 is now explicitly blocked on W14's canonical Work Authority/ExecutionHostBridge source and runtime contract. W12/W13 are absorbed internal foundations only. The Task Register/test contract update is at commit `4470b555914894c4ad5a6cb98743dc6637a179a1`; exact-head validation is required before review handoff.


## Current W14-aligned review handoff — 2026-11-22

- W14 is the sole integrated execution/product owner; W12/W13 are absorbed internal foundations only.
- W118-TASK-015 remains BLOCKED until W14's canonical source, Work Authority/ExecutionHostBridge contract and live runtime are verified.
- Exact tested code SHA `4470b555914894c4ad5a6cb98743dc6637a179a1`; Run #44950893033 SUCCESS; 95 tests PASS; artifact 14725229117.
- PR #68 READY FOR REVIEW / OPEN / UNMERGED; 20 ahead / 0 behind; 45 changed paths W118-only. PR #67 CLOSED / UNMERGED / superseded.
- Runtime event jobs were skipped; no full runtime E2E or acceptance is claimed.


## W70 governance and current test baseline — 2026-11-22

W70 DOC-093 is DRAFT_NOT_APPROVED and is used only as a structural reference. W118's planning register is not runtime authority; Core :8000 owns runtime Task/Assignment/Event. W14 is the sole integrated execution owner; W12/W13 are absorbed. Exact source SHA `dbdd71d6758abfdf614a59dce2fe5f081cb6a454` passed 95 tests in Run #44951313523; artifact 14724769218. W14 source/runtime and W70 schema/owner ACK remain BLOCKED.


## Current exact-head handoff — 2026-11-22

PR #68 is READY FOR REVIEW / OPEN / UNMERGED. Exact tested head `076a74d8f19e6ca63ac45ff2150910122316c049` passed 95 tests in Run #44951562713 (artifact 14725821955). W14 is the sole integrated execution owner; W12/W13 are absorbed. W14 source/runtime remains unverified. W70 DOC-093 is DRAFT_NOT_APPROVED. Xu independent review and Vinh product acceptance remain pending.


## Current status overlay — 2026-11-22 (UTC+07:00)

- Canonical candidate: PR #68, branch `work/118-auto-e2e-v2-clean`, head `c64bd6f9cb6ab4fa72cf1bbfbabfb7257a254bd1`. PR #67 is superseded.
- Latest exact-head contract CI: [Run #880](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44993439504), validate SUCCESS; raw log confirms 95 tests in 0.293s. Artifact ID `14742494287`, SHA-256 `babe4cfffd72135e70c8623df161404ef5036dd4461d1319d43ce4eeaf9c596c`.
- Run #880 skipped Task-to-Issue push binding and handoff/ACK/review observation jobs. Contract CI is not Runtime Auto E2E.
- Main comparison: DIVERGED 59 ahead / 2 behind; two Main-side commits are W092-only. No rebase or merge performed.
- P1-118-01 OPEN / NEEDS CHANGES; P1-118-02 BLOCKED; W118-TASK-015 W14 dependency BLOCKED; Runtime Auto E2E NOT VERIFIED; Xu review PENDING; Vinh acceptance NOT ACCEPTED.
- Current Xu review routing overlay: [RR-118-001](../EVIDENCE/RR-118-001_CURRENT-XU-REVIEW-ROUTING.md). Historical XR/release/handoff snapshots still reference PR #67; use RR-118-001 to route the active review to PR #68. Gate criteria are unchanged.
- No B-118-010, Main merge or release. W118 remains ACTIVE — NOT ACCEPTED — NOT RELEASED.


## 2026-11-22 — Exact-head CI #884 and current branch refresh

- **Priority:** 01 / P0 — Exact-revision evidence and review-routing freshness.
- **Name / Title:** Ka — CSA / Delegated Technical Lead, Work 118.
- **Date-Time:** 2026-11-22 (UTC+07:00).
- **Canonical candidate:** PR #68, branch `work/118-auto-e2e-v2-clean`, exact current HEAD `b30165802f8078ccc51cd97874c4b820dcace554`; PR #67 remains superseded history.
- **PR state:** OPEN / UNMERGED. Latest PR metadata snapshot identifies #68 as the only active W118 candidate.
- **Exact-head CI:** Run [#884](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44994563080), run ID `44994563080`, event `pull_request`, tested PR head exactly `b30165802f8078ccc51cd97874c4b820dcace554`. Validate job `137122681513` COMPLETED / SUCCESS; raw log confirms **95 tests in 0.292s — OK**.
- **Artifact:** `w118-run-evidence-44994563080-1`, ID `14743596579`, size 684 bytes, SHA-256 `336cb874be65790a2fa3ccc5c7a795d9f3b7e02f28adf244bae882f1c1398d74`. Upload log digest matches GitHub artifact metadata; artifact is not expired. Payload has not been independently downloaded/parsed.
- **Coverage limits:** Task-to-Issue push source-binding step and `handoff-request-capture`, `ack-claim-capture`, `review-observation-capture` jobs were SKIPPED. Evidence artifact reports `SOURCE_BINDING_STATUS=NOT_RUN`. CI #884 is contract/unit evidence only; it does not prove live push binding, handoff, authenticated ACK, review lifecycle, Core lease authenticity or Runtime Auto E2E.
- **Current compare:** `main...work/118-auto-e2e-v2-clean` is DIVERGED **63 ahead / 2 behind**, merge base `792bdd71e5345949e0c1f26ff9f95a8513dfa7d5`, Main tip `554f02e2e9ac9aedc43d875d7a212b35c94525e7`. Compare returns 45 changed paths, all within W118; the two Main-side commits are recorded as W092-only in the existing path audit. This is not a merge simulation or authorization. No rebase, merge or force-push performed.
- **Outstanding gates:** P1-118-01 OPEN / NEEDS CHANGES (duplicate Issue marker and persisted Core `task.issue_id` binding); P1-118-02 BLOCKED (Core-issued lease authenticity / Task binding / expiry / revocation contract and runtime proof); W118-TASK-015 BLOCKED (W14 canonical Work Authority/ExecutionHostBridge, server-side grant and ACK-before-side-effect evidence); Runtime Auto E2E NOT VERIFIED; Xu independent review PENDING; Vinh product acceptance NOT ACCEPTED.
- **Review routing:** RR-118-001 and root README/STATUS refreshed to point to current HEAD and Run #884. Historical XR-118-001, release gate and handoff retain their original PR #67 snapshots; RR-118-001 remains an overlay and does not amend, waive or replace their acceptance criteria.
- **Disposition:** W118 ACTIVE — NOT ACCEPTED — NOT RELEASED. B-118-010 PREPARED / NOT APPLIED. No Main merge, release, permission/secret change or external Work mutation.
- **Next permitted action:** Continue evidence and review preparation under the existing freeze. Xu must review the current PR #68 and close the independent test cycle; external Core/W14 owners must supply their authoritative contracts and runtime evidence. Do not change implementation/workflow, apply B-118-010, merge Main or release without the applicable approvals.


## Latest authoritative refresh — 2026-11-22 (after journal Entry 049)

- Canonical candidate: PR #68 / `work/118-auto-e2e-v2-clean`, exact branch HEAD `7d7454b702efcf56030bf7a3b0788b0db03d122d`; PR #67 remains superseded.
- Exact-head CI: Run [#888](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44995190536), exact head `7d7454b702efcf56030bf7a3b0788b0db03d122d`, validate SUCCESS; raw log **95 tests in 0.318s — OK**. Artifact ID `14743572748`, SHA-256 `3239cc165b7b35d31365d8c4bcb98480b91afe07f733e6d992485fcc1c00cbf9`; metadata/upload digest match, not expired, payload not independently parsed.
- CI #888 skipped Task-to-Issue push source binding and handoff/ACK/review-observation jobs; `SOURCE_BINDING_STATUS=NOT_RUN`. Contract/unit evidence only; no Runtime Auto E2E claim.
- Current compare: DIVERGED **69 ahead / 2 behind**, merge base `792bdd71e5345949e0c1f26ff9f95a8513dfa7d5`, Main `554f02e2e9ac9aedc43d875d7a212b35c94525e7`, 46 changed paths, all W118. No rebase/merge/force-push.
- Latest review readback: 0 formal reviews / 0 inline threads. Xu review PENDING; Vinh acceptance NOT ACCEPTED.
- P1-118-01 OPEN / NEEDS CHANGES; P1-118-02 BLOCKED; W118-TASK-015 W14 dependency BLOCKED; Runtime Auto E2E NOT VERIFIED.
- Entry 049 revalidated the duplicate Issue marker / Core `task.issue_id` binding gap and non-empty-string-only lease check at exact branch HEAD. No implementation change under freeze.
- W118 ACTIVE — NOT ACCEPTED — NOT RELEASED. B-118-010 PREPARED / NOT APPLIED. No Main merge or release.
