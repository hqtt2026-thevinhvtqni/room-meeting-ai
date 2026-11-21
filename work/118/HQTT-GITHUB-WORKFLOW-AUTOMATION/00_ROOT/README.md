# W118 — HQTT GitHub Workflow Automation

**Selected architecture:** A — Sandbox initiates; GitHub controls versioning.  
**Status:** ACTIVE — BUILD / VERIFY — NOT ACCEPTED — NOT RELEASED.  
**Implementation branch:** `work/118-auto-e2e-v2`; PR #67 remains unmerged.

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
- **W12/W13:** WEE, Git/GitHub Gateway, CIAdapter and Execution Host.
- **W70:** Work lifecycle, Evidence Register and read-only Dashboard projection.
- **GitHub:** source/version, Issues/PRs, branches/commits, Actions runs and artifacts.

## 3. Official W118 documents

- [TD-118-012 — Dual closed-loop architecture v1.2](../02_DEFINE/TD-118-012_KIEN-TRUC-HAI-QUY-TRINH-KHEP-KIN-SANDBOX-GITHUB.md)
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
