# W118-13..17 — Core / GitHub adapter implementation

- **Architecture:** TD-118-012 v1.2
- **Status:** CONTRACT BUILD — RUNTIME INTEGRATION BLOCKED BY EXISTING SERVICE PORTS
- **Implementation branch:** `work/118-auto-e2e-v2`
- **Date:** 2026-11-21

## 1. Ownership correction

Inspection of W102 DOC-012 and W12 Execution Bridge showed that Core :8000 is the sole runtime Task/Assignment/Event authority; W102 owns Agent Loop policy; W12/W13 own execution, Git/GitHub Gateway and CIAdapter. W52 is a DRAFT interoperability reference. W118 therefore does not own a runtime Task DB, dispatcher, durable event queue, Event Bus, Execution Host, Git Gateway or CI engine.

The earlier W118-local SQLite TaskRegistry, webhook inbox and event reconciler were removed from the implementation path. W118 now builds stateless adapters only.

## 2. Current adapter modules

| Module | Responsibility | Persistence / state mutation |
|---|---|---|
| `scripts/w118/core_task_adapter.py` | Normalize an approved Core Task snapshot using an explicit Core-owner field map; build a read-only GitHub Issue projection | None; read-only DTO |
| `scripts/w118/github_issue_adapter.py` | Create/update one Issue from Core snapshot, require Core per-Task lock lease, paginate lookup and exact readback | GitHub Issue mirror only; no Core state |
| `scripts/w118/source_binding.py` | Validate Task branch, commit trailers, Work/Task/Issue binding and exact SHA | None |
| `scripts/w118/github_webhook_verifier.py` | Stateless HMAC-SHA256, delivery UUID, event/repository allowlist, payload-size and JSON validation | No inbox/queue/database |
| `scripts/w118/github_event_adapter.py` | Normalize verified push/CI/Issue events into Core event-intent DTOs; CI-before-push returns DEFERRED | No event ID/sequence assignment; no persistence |
| `.github/workflows/w118-workflow-automation.yml` | CI contract tests; handoff request, ACK claim and PR review observation capture | Does not assign Agent, verify ACK or accept Task |

## 3. Core boundaries

- Core :8000 owns Task identity/status, Assignment status, event IDs/sequence, idempotency and persistence.
- W102 owns Agent selection/dispatch policy and identity/permission decisions.
- W01/W02/W22 + Core provide verified principals.
- W12/W13 own execution host, GitHub Gateway and CIAdapter.
- W70 owns Work Dashboard/Evidence Register schema and read-only projection policy.
- GitHub login, Issue Assignee, label, comment or review state is not a verified ROOM-HOP principal or Task transition.

## 4. Issue mirror contract

- Marker: `<!-- room-hop-core-task:<task_id> -->`.
- Body is derived from normalized Core Task snapshot and includes Core source revision and acceptance checks.
- Mirror requires a Core-issued lock lease; W118 does not create its own lock database.
- Lookup is paginated; PRs are excluded; exact readback verifies Issue number/title/body.
- No GitHub Assignee mutation, Issue close, merge or release.

## 5. Webhook and event contract

- Webhook verifier checks `X-Hub-Signature-256`, `X-GitHub-Delivery`, `X-GitHub-Event`, repository allowlist, JSON and body limit.
- Event adapter emits a Core Event Intent containing `task_id`, `correlation_id`, type, producer, payload and provenance.
- Core adds canonical `event_id`, `seq`, `ts`, persists and decides state.
- Push/CI events are evidence only. CI PASS/FAIL never sets Task DONE or Assignment ACCEPTED.
- CI arriving before matching Core push evidence returns DEFERRED; Core reconciliation/redelivery handles ordering. No local W118 queue.

## 6. GitHub Actions observation jobs

- `handoff-request-capture`: captures `w118-handoff` as a request only; does not create Assignment.
- `ack-claim-capture`: captures an `ACKED-...` comment as an unverified claim; does not add `w118-acked` or transition Assignment.
- `review-observation-capture`: records GitHub review metadata; does not authorize acceptance, merge or release.
- Workflow default permissions remain read-only; Issue write is scoped to observation comments.

## 7. Test modules

- `test_core_task_adapter.py`
- `test_github_issue_adapter.py`
- `test_source_binding.py`
- `test_github_webhook_verifier.py`
- `test_github_event_adapter.py`
- `test_task_register_contract.py`
- `test_workflow_contract.py`

Legacy duplicate tests/modules `task_lifecycle.py`, `webhook_inbox.py`, `event_reconciler.py` and their tests have been removed.

## 8. Runtime gaps

- Core Task read API, actual schema and approved field map are not exposed to W118.
- Core per-Task lock and Core event ingress are not exposed.
- W102 Agent identity/Assignment API and a verified runtime principal are not available in current evidence.
- W12/W13 execution host and CIAdapter are not exposed/configured in this session.
- No production webhook secret/TLS endpoint, live GitHub Issue create/readback, task-scoped push, Core event persistence or full runtime E2E has been run.
- Sandbox MCP in this session exposes file operations only; tests are executed by GitHub Actions.

**Disposition:** stateless adapter contracts only. Runtime integration is BLOCKED until the existing owning services expose their approved ports. W118 remains ACTIVE — NOT ACCEPTED — NOT RELEASED.
