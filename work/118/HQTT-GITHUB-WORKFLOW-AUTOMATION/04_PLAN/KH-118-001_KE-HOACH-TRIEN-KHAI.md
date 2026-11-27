# KH-118-001 — KẾ HOẠCH TRIỂN KHAI W118

- **Work:** W118 — HQTT GitHub Workflow Automation
- **Version:** 1.2
- **Architecture:** TD-118-012 v1.2
- **Selected option:** A — Sandbox initiates; GitHub controls versioning
- **Status:** OWNER-DIRECTED BUILD PLAN — ACTIVE
- **Owner:** Vinh
- **Coordinator:** Xu / AI-01
- **Date:** 2026-11-21

## 1. Objective

Build two connected closed loops:
1. Plan → Core Task → W102 Agent Loop → W12/W13 Execute → Verify → Owner Accept → Close.
2. Sandbox → W12/W13 → GitHub Branch/Commit/Push → GitHub Actions CI → W118 stateless adapter → Core Event → W102/W12 recovery.

W118 builds GitHub-specific adapters only. It must reuse Core :8000, W102, W12/W13, W70 and existing identity/event services.

## 2. Ownership boundaries

| Owner | Responsibility |
|---|---|
| W118 Work Task Register | W118 implementation plan/WP progress only; not runtime Task state |
| Core :8000 | Sole canonical runtime Task/Assignment/Event authority |
| W102 | Agent Loop policy, selection, dispatch/ACK decisions |
| W01/W02/W22 + Core | Verified principal, authentication and authorization |
| W12/W13 | WEE, execution host, Git/GitHub Gateway and CIAdapter |
| W52 | A2A contract reference (DRAFT) |
| W70 | Work lifecycle, Evidence Register and read-only Dashboard |
| GitHub | Version/source history, Issues/PRs, branch/commit and Actions CI |

W118 must not create a local Task DB, Agent Registry, dispatcher, durable event queue/Event Bus, Execution Host, Git Gateway or CI engine.

## 3. Work Package plan

| WP | Scope | Status | Deliverable / gate |
|---|---|---|---|
| W118-13 | Core Task projection adapter | IN_PROGRESS | Read-only Core snapshot DTO with explicit Core-owner field map; no local Task persistence. Blocked on Core API schema/port. |
| W118-14 | W102/Core identity and Assignment integration | BLOCKED | Handoff/ACK claims forwarded to Core/W102; no local Agent Registry or dispatcher. Blocked on verified principal and Core/W102 port. |
| W118-15 | W12/W13 execution bridge integration | BLOCKED | W118 Work Authority mapped to W12 WEE/GitHub Gateway/CIAdapter and W13 Host. Blocked on host/adapter availability. |
| W118-16 | Core Task → GitHub Issue mirror and source binding | IN_PROGRESS | Core projection → Issue create/update/readback under Core lock; task branch/commit/push exact binding. Live Core lock/API and task-scoped push pending. |
| W118-17 | Stateless webhook verifier and Core event adapter | IN_PROGRESS | HMAC verification and push/CI/Issue event intent normalization; no local inbox/event store. Core Event ingress pending. |
| W118-18 | W70 Evidence Register/Dashboard projection | BLOCKED | Read-only schema mapping after W70 owner/schema ACK. No W70 schema changes. |
| W118-19 | Full lifecycle runtime E2E and acceptance | PLANNED | One non-sensitive pilot from Sandbox Plan to Vinh acceptance; requires W118-13..18 gates. |

## 4. Current code scope

- `scripts/w118/core_task_adapter.py` — read-only Core Task snapshot normalization using explicit field map.
- `scripts/w118/github_issue_adapter.py` — Core Task Issue mirror, Core lock lease required, paginated lookup and exact readback.
- `scripts/w118/source_binding.py` — Task branch/commit/Issue/exact-SHA validator.
- `scripts/w118/github_webhook_verifier.py` — stateless HMAC-SHA256 and delivery envelope verification.
- `scripts/w118/github_event_adapter.py` — stateless GitHub event-to-Core event intent mapping.
- `.github/workflows/w118-workflow-automation.yml` — CI contract; handoff request, ACK claim and PR review observation only.
- Tests: Core projection, Issue mirror, source binding, webhook verifier, event adapter, Task Register contract and workflow contract.

Removed/superseded from W118 implementation path:
- SQLite TaskRegistry / local Task lifecycle store.
- Durable webhook inbox and local event reconciler.
- GitHub-login authorization scripts for Agent ACK/review acceptance.
These duplicated Core/W102/W12 ownership and are not part of the approved architecture.

## 5. Build and verification sequence

1. Finish stateless adapter tests and observation-only GitHub workflow contract.
2. Run exact-head GitHub Actions CI; inspect test summary, run ID, tested SHA and artifact digest.
3. Obtain actual Core Task API schema, explicit field map, per-Task lock lease and Event ingress from Core owner.
4. Integrate W102 identity/Assignment policy; verify one real runtime principal.
5. Obtain W12/W13 Work Authority schema, execution host and GitHub Gateway/CIAdapter route.
6. Obtain W70 read-only Evidence Register/Dashboard mapping approval.
7. Run one non-sensitive full runtime E2E; collect independent QE evidence.
8. Submit exact revision and evidence to Vinh for acceptance.

## 6. Test and evidence requirements

Each test record must include test ID, environment, source SHA, actor/principal, input, method/command, expected/actual result, GitHub run ID/attempt, artifact URL/digest, PASS/FAIL/BLOCKED and next step.

Contract tests are not runtime E2E. CI PASS does not imply Task DONE, Assignment ACCEPTED, product acceptance, merge or release.

## 7. Blockers

| Blocker | Owner | Release condition |
|---|---|---|
| Core Task API schema/field map unavailable | Core :8000 owner | Approved API schema and read port |
| Core lock and Event ingress unavailable | Core :8000 owner | Lock lease + idempotent event append/readback |
| No verified Agent principal/Assignment port | W102 + W01/W02/W22 + Core | Positive/negative identity and ACK tests |
| W12/W13 host/CI adapter not exposed | W12/W13 owner | Real execution ID, logs, GitHub ref and CI evidence |
| W70 projection schema approval pending | W70 owner | Written schema/owner ACK |
| Runtime E2E not run | Xu/QE/Vinh | All prior blockers resolved |

## 8. Governance

- Vinh authorized Xu to proceed with build without waiting for multi-agent review.
- This plan does not authorize permission escalation, branch protection bypass, merge, release or product acceptance.
- PR #67 remains open/unmerged; no rebase or merge to main.
- W118 remains ACTIVE — BUILD / VERIFY — NOT ACCEPTED — NOT RELEASED.
