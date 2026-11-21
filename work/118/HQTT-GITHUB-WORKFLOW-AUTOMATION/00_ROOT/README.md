# W118 — HQTT GitHub Workflow Automation

**Selected architecture:** A — Sandbox initiates; GitHub controls versioning.  
**Status:** ACTIVE — BUILD / VERIFY — NOT ACCEPTED — NOT RELEASED.  
**Implementation branch:** `work/118-auto-e2e-v2`; PR #67 remains unmerged.

## 1. Purpose

Build two connected workflows:
1. **Plan → Core Task → W102 Agent Loop → W12/W13 Execute → Verify → Owner Accept → Close.**
2. **Sandbox → W12/W13 → GitHub Branch/Commit/Push → GitHub Actions CI → W118 stateless adapter → Core Event → W102/W12 recovery.**

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
- W12/W13 execution host and CIAdapter are not exposed/configured in this session.
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
| W12/W13 execution/CI | **BLOCKED — host/adapter availability** |
| W70 Dashboard | **BLOCKED — schema/owner approval** |
| Full runtime E2E / Vinh acceptance | Not run |

No rebase, merge to main, release or branch-protection change is authorized by this Work state.
