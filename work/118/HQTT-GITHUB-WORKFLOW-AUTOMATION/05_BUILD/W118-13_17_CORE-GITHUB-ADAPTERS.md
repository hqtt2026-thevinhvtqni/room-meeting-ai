# W118-13..17 — Core / GitHub adapter implementation

- **Architecture:** TD-118-012 v1.2
- **Status:** CONTRACT BUILD — RUNTIME INTEGRATION BLOCKED BY EXISTING SERVICE PORTS
- **Implementation branch:** `work/118-auto-e2e-v2`
- **Date:** 2026-11-21

## 1. Ownership correction

Inspection of W102 DOC-012 and W12 Execution Bridge showed that Core :8000 is the sole runtime Task/Assignment/Event authority; W102 owns Agent Loop policy; W14 is the sole integrated execution owner; W12/W13 are absorbed internal foundations. W52 is a DRAFT interoperability reference. W118 therefore does not own a runtime Task DB, dispatcher, durable event queue, Event Bus, Execution Host, Git Gateway or CI engine.

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
- W14 owns the integrated execution path; W12/W13 are absorbed internal modules.
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
- W14 canonical source/API/runtime parity and Work Authority/ExecutionHostBridge are not verified.
- No production webhook secret/TLS endpoint, live GitHub Issue create/readback, task-scoped push, Core event persistence or full runtime E2E has been run.
- Sandbox MCP in this session exposes file operations only; tests are executed by GitHub Actions.

**Disposition:** stateless adapter contracts only. Runtime integration is BLOCKED until the existing owning services expose their approved ports. W118 remains ACTIVE — NOT ACCEPTED — NOT RELEASED.


## Exact-head CI verification — 2026-11-21

- Tested feature branch SHA: `5f02a9eafbf68eb0bcfca2942733882dab9cc5bf`.
- Push run [#44882420198](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44882420198): SUCCESS — **94 tests PASS / 0.209s**.
- PR run [#44882422288](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44882422288): SUCCESS.
- Artifact ID `14697683781`; SHA-256 `a2703f70b4a250197b14a84bb5408cef18f2917266f542c7850a54c70e098abc`.
- Source binding result for the aggregate feature branch: `UNBOUND_LEGACY_BRANCH` (expected; no Task inference).
- This proves adapter/workflow contract tests only. Core API, W102 identity/Assignment, W14 integrated execution, Core event persistence and full runtime E2E remain NOT VERIFIED.


## Ownership correction — 2026-11-22

W14 is the sole product/delivery owner for the integrated execution, GitHub Gateway and CI path. W12/W13 are absorbed internal foundations only. W118 must consume W14's approved Work Authority/ExecutionHostBridge contract; W118-TASK-015 is BLOCKED until W14 source/runtime evidence is verified. No direct W12/W13 product integration or parallel host is allowed.


## P1 remediation — Core Issue identity and lease validation boundary (2026-11-23)

### P1-118-01 — implemented in the W118 adapter

- The marker lookup scans every required Issue page (100/page) up to the configured bound, excludes Pull Requests, and collects all matching Task markers before any mutation.
- Zero marker matches: create is allowed only when the Core projection has no persisted issue_id.
- Exactly one marker match: if Core has issue_id, its integer must equal the matched GitHub Issue number before PATCH/readback; otherwise fail closed.
- More than one marker match: raise IssueLookupDuplicate; no POST/PATCH.
- A persisted Core issue_id with no matching marker Issue, or a different Issue number, is rejected; no replacement Issue is created.
- Reaching the page ceiling while the final page is full raises IssueLookupIncomplete; no mutation is attempted because scan completeness is unproven.
- Pull Requests carrying the marker are excluded from Issue identity matching.
- Regression coverage includes zero/one/multiple matches, persisted-ID match/mismatch/not-found, cross-page scan and cross-page duplicate, PR exclusion, and incomplete pagination.

### P1-118-02 — fail-closed integration port; authoritative validation remains BLOCKED

GitHubIssueAdapter now accepts an optional lease_validator(lease_id, CoreTaskProjection) -> bool integration callback. No callback, false result, exception, or non-boolean success rejects the operation before any GitHub API request. W118 does not implement a local lease authority or infer validity from a non-empty string.

This callback is only an adapter seam and unit-test injection point. It is not a Core API/schema, cryptographic verifier, or proof of authority. The test harness uses a deterministic stub solely to exercise adapter behavior. No production Core validator is supplied or enabled.

Before production mirror writes can be enabled, the Core owner must publish and expose an authenticated validation contract that establishes: issuer/principal, Work and Task binding, permitted operation/resource scope, audience, expiry, revocation/current status, authentication/signature method, and concurrency/lease exclusivity semantics. W118 must then consume that owner-approved port and prove positive, negative, expired, revoked, wrong-Task, wrong-Work, wrong-audience and replay/concurrency cases against the real Core service. Until then P1-118-02 remains BLOCKED and live mirror writes are not authorized.

No Core, W102, W14, W70 or W33 source/service was modified. No W118-local lock, database, queue, dispatcher or authority was introduced.
