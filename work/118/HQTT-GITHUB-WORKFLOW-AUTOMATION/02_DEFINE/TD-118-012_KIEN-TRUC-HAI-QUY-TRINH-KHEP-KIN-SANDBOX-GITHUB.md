# TD-118-012 — KIẾN TRÚC HAI QUY TRÌNH KHÉP KÍN SANDBOX–GITHUB

- **Work:** W118 — HQTT GitHub Workflow Automation
- **Document ID:** TD-118-012
- **Version:** 1.3
- **English name:** Sandbox–GitHub Dual Closed-Loop Architecture
- **Selected option:** A — Sandbox initiates; GitHub controls versioning.
- **Status:** OWNER-DIRECTED BUILD BASELINE — implementation may proceed within existing Work ownership and permission boundaries.
- **Authority:** Vinh (Product Owner); Xu coordinates technical implementation.
- **Date:** 2026-11-21 (UTC+07:00)
- **Scope:** Plan-to-Task orchestration and Sandbox–GitHub source/CI loop; ownership, states, permissions, data/event contracts, errors, tests and gates.
- **Git source:** `hqtt2026-thevinhvtqni/room-meeting-ai`, branch `work/118-auto-e2e-v2`.
- **Related baselines:** W70 DOC-056 §9 / DOC-093 model; W102 DOC-012 consolidated architecture; W14 integrated execution contract; W14 W12/W13 absorption record; W16 Workflow Engine architecture; W52 A2A contract v0.1 (DRAFT); W112 DOC-001 (DRAFT_NOT_APPROVED).

> **Important:** Vinh has instructed Xu to build without waiting for multi-agent review. This document is the owner-directed implementation baseline, not independent QE approval, product acceptance, merge authorization or release authorization. No Work-owned Core/Agent/Execution/CI service may be duplicated by W118.

---

## 1. Architecture decision and system ownership

### 1.1 Selected option A

**Sandbox/ROOM-HOP khởi phát và điều phối kế hoạch; GitHub kiểm soát phiên bản mã nguồn, Issue/PR và CI.** Core :8000 remains the single runtime Task/Assignment/Event authority. W118 supplies GitHub-specific adapters and workflow evidence; it does not become a second orchestrator/runtime.

### 1.2 Existing Work ownership — mandatory reuse

| System / Work | Canonical responsibility | W118 integration boundary |
|---|---|---|
| **W70 — Work Lifecycle & Dashboard** | Work/WP lifecycle, Work-specific planning Task Register model, canonical Work Dashboard and evidence projection policy | W118 keeps its own planning register using DOC-093 model; Dashboard projection is read-only and requires W70 schema/owner approval |
| **Core :8000** | Sole canonical runtime Task identity/state, Assignment state, event persistence/sequence and authorization decisions | W118 consumes Core Task snapshots and submits normalized event intents through an approved Core port; no local Task DB or event store |
| **W102 — Agent Loop** | Agent Loop policy, role/capability routing, task execution governance and cross-role orchestration | W118 emits handoff/ACK/review observations; W102/Core decides eligibility, assignment, ACK and state |
| **W52 — A2A communication** | Provider-neutral communication/task-event contract reference; current contract is DRAFT | W118 maps GitHub events into an approved Core/W102 event adapter; do not treat draft schema as a live runtime |
| **W14 — Autonomous E2E Builder** | Sole product/delivery owner for integrated Work Authority, ExecutionHostBridge, GitHub Gateway and CI path | W118 consumes W14-approved contracts; W12/W13 are absorbed internal foundations only |
| **W12/W13 — absorbed foundations** | Historical WEE lifecycle/Execution Host contracts and modules owned internally by W14 | Not independent product owners; W118 must integrate through W14 only |
| **W01/W02/W22 + Core** | Identity, authentication, authorization and principal binding | W118 never treats GitHub login, label, comment or role-map text as a verified ROOM-HOP principal |
| **W16 — Workflow Engine** | Deterministic workflow engine architecture | Design reference/future integration; do not assume production runtime is available |
| **GitHub** | Version-controlled source, branches, commits, Issues, PRs, reviews, GitHub Actions runs and artifacts | Version/CI authority; Issue is a collaboration mirror of Core Task, not the runtime Task authority |

**W118 must not build or own:** a second Task database/registry, Agent Registry, dispatcher, durable event queue, Event Bus, execution host, Git Gateway, CI engine or cross-Work workflow engine.

### 1.3 W118 components

W118 owns only:
1. Work-specific planning Task Register for W118's own implementation tasks.
2. Read-only Core Task snapshot normalizer / GitHub Issue projection adapter.
3. GitHub source-binding validator (branch, commit trailers, Issue ID and exact SHA).
4. Stateless GitHub webhook signature/envelope verifier.
5. Stateless GitHub event-to-Core event-intent adapter.
6. GitHub Actions workflow contract tests and immutable CI evidence metadata.
7. Work-specific integration map, journal and acceptance/test evidence.

### 1.4 Non-negotiable principles

1. **Core runtime authority:** Core :8000 is the only canonical runtime Task/Assignment/Event store.
2. **Work plan ≠ runtime Task:** W118 `TASK_REGISTER.json` tracks W118 project/WP work; it is not a substitute for Core runtime Tasks.
3. **W102 owns Agent policy:** W118 never selects or dispatches an Agent independently.
4. **W14 owns integrated execution:** W12/W13 are absorbed internal foundations; W118 uses only W14's canonical Work Authority and ExecutionHostBridge. W118 never runs code through a parallel execution host or Git Gateway.
5. **GitHub owns source history:** exact branch, commit SHA, PR and CI run are read from GitHub.
6. **Issue is a mirror:** GitHub Issue labels/comments/Assignees never become Task or Assignment authority.
7. **Observation ≠ transition:** push, CI, Issue close and review events are evidence observations; Core/W102 alone decides state changes.
8. **No local event queue:** W118 verifies and normalizes delivery, then forwards to Core. Core owns deduplication, sequence, persistence and reconciliation.
9. **Fail closed:** unknown identity, schema, source binding, permission or Core mapping means REJECTED/BLOCKED/DEFERRED; never infer.
10. **No silent write-back:** every mirror/update has exact Core revision, GitHub readback and evidence.

---

## 2. Two connected closed-loop workflows

### 2.1 Workflow A — Plan → Core Task → Agent Loop → Verify → Close

`Work Plan (Sandbox) → W118 Work Task Register → Core Task Create/Read → GitHub Issue Mirror → W102 Policy / Core Assignment → Verified Agent ACK → W14 ExecutionHostBridge (using absorbed W12/W13 modules) → Core Task/Event Update → QE/Owner Acceptance → GitHub Issue Mirror Update → W70 Dashboard`

| Step | Owner | Action | Authoritative record |
|---|---|---|---|
| A1 Plan | Vinh / Work Owner | Define outcome, scope, WP, dependencies, AC and risk in Sandbox | W118 Work Plan / Task Register |
| A2 Task preparation | Xu / Planner | Break down Work WP into actionable project tasks; prepare Core task request | W118 plan artifact; not runtime Task state |
| A3 Runtime Task creation | Core :8000 | Create canonical Task, assign task ID/correlation and validate request | Core Task record |
| A4 Issue mirror | W118 GitHub adapter | Project normalized Core Task snapshot to GitHub Issue; stable Task marker; exact readback | GitHub Issue mirror + Core source revision |
| A5 Agent selection | W102 + Core + Identity | Verify principal, capability, availability, trust and least-privilege policy | Core/W102 assignment decision |
| A6 Dispatch / ACK | W102 + W52 + Core | Dispatch to verified principal; bind ACK to Task/Assignment/dispatch; reject replay | Core Assignment/Event |
| A7 Execution | W14 | Execute task through canonical W14 Work Authority/ExecutionHostBridge; record command, source revision and output | W14 execution record / GitHub commit |
| A8 Progress / blocker | Core + W102 | Persist progress, blocker, retry/reassignment and state | Core Task/Event |
| A9 Verification | QE / Verifier | Verify deliverable against AC and exact source SHA | Core/W102 verification evidence |
| A10 Owner acceptance | Vinh | Accept/reject exact deliverable and revision | Core acceptance event + Work Journal |
| A11 Close mirror | W118 adapter | Update/close GitHub Issue only after Core says Task is complete; readback | GitHub Issue mirror |
| A12 Dashboard | W70 | Read-only projection of approved Work/Task/evidence fields | W70 Dashboard |

**Owner-directed build exception:** Vinh may directly instruct Xu to work in the current conversation. W118 records that as a project-level execution authorization in its Work plan. It does not create a fake Core Assignment, Agent principal or ACK. Agent-runtime work still requires Core/W102 identity and Assignment verification.

### 2.2 Workflow B — Sandbox → WEE → GitHub → CI → Core → Sandbox

`Core-authorized Task → W14 Work Authority / ExecutionHostBridge → GitHub Gateway → Branch → Code/Test → Commit/Push → GitHub Actions CI → W118 Stateless Webhook Verify/Normalize → Core Event Port → W102/Core Decision → W14 bounded repair/review integration → Owner Acceptance`

| Step | Owner | Action | Authority / evidence |
|---|---|---|---|
| B1 Authorization | Core/W102 | Confirm Task and Assignment are authorized for execution | Core Task/Assignment snapshot |
| B2 Work Authority | W14 + W118 | Consume W14-authorized repository, branch, base SHA, workspace, test entrypoint and policy refs | W14 Work Authority + W118 projection |
| B3 Source sync | W14 (absorbed W12 Gateway) | Resolve repo/branch/head and sync exact base SHA | GitHub ref/commit |
| B4 Build/test | W14 (absorbed W12/W13 modules) | Execute code/tests in the canonical authorized host | W14 execution ID, logs, test result |
| B5 Commit/push | W14 (absorbed GitHub Gateway) | Enforce branch ownership, source binding, exact SHA and permission | GitHub commit/ref |
| B6 CI | GitHub Actions / W14 integration | Run allowlisted workflow and capture run ID, attempt, conclusion, head SHA and artifact digest | GitHub Actions |
| B7 Webhook verify | W118 | Verify HMAC, repository allowlist, event allowlist, delivery UUID and payload digest | Stateless verified envelope |
| B8 Event normalize | W118 | Match event to Core Task snapshot/source binding; produce event intent only | Core Event Intent DTO |
| B9 Persist/reconcile | Core :8000 | Deduplicate, assign event ID/sequence, persist, reconcile out-of-order events and decide state | Core event store |
| B10 Repair/review | W102/W14 | Route failure to authorized repair; bounded policy; open/update PR | Core + GitHub |
| B11 Acceptance | QE / Vinh | Independent verification and explicit Owner acceptance | Core/Work Journal |
| B12 Mirror sync | W118 | Update Issue from latest Core snapshot; verify exact readback | GitHub Issue mirror |

**Critical boundary:** W118 webhook code does not persist an inbox or queue. If Core's event port is unavailable, the adapter returns a structured unavailable/deferred result; GitHub redelivery or Core reconciliation owns recovery. No local W118 queue is created.

---

## 3. State model and status matrices

### 3.1 W118 Work planning Task Register

W118's `04_PLAN/TASK_REGISTER.json` is the Work-specific planning register modeled on W70 DOC-093. It tracks the implementation tasks of Work 118 only.

| Field | Purpose |
|---|---|
| `task_id`, `wp_id`, `phase` | Work-scoped project planning identity |
| `status` | Work plan status: PLANNED/READY/IN_PROGRESS/BLOCKED/IN_REVIEW/DONE/CANCELLED |
| `execution_mode` | OWNER_DIRECTED_BUILD or CORE_AGENT_TASK; project-level authorization mode, not runtime Assignment state |
| `owner_directive_ref` | Required for Owner-directed build tasks |
| `assigned_identity` | Optional planned identity only; never proof of runtime identity |
| `core_task_id`, `correlation_id` | Null until Core creates and returns the runtime Task mapping |
| `evidence_refs`, `next_action`, `blockers` | Project evidence and next step |

The Work planning status is not copied into Core by assumption. Core runtime state remains authoritative for actual Agent execution.

### 3.2 Core runtime Task / Assignment status

- Core :8000 owns runtime Task status and Assignment status.
- W102 owns Agent Loop policy and transition decisions.
- W52 A2A v0.1 and W112 DOC-001 are design references only while their status remains DRAFT.
- W118 consumes a normalized Core Task projection and never implements a second transition engine.

| Core runtime domain | Known compatibility vocabulary | W118 behavior |
|---|---|---|
| Task | PLANNED, READY, IN_PROGRESS, BLOCKED, IN_REVIEW, DONE, CANCELLED | Read-only projection; no local transition |
| Assignment | PROPOSED, DISPATCHED, ACKNOWLEDGED, IN_PROGRESS, SUBMITTED, ACCEPTED, REJECTED, BLOCKED, CANCELLED | Read-only projection; no local Assignment store |
| Event | Core-assigned event ID, sequence, timestamp, task/correlation binding | W118 submits event intent; Core assigns ID/sequence and persists |

### 3.3 GitHub source/CI observations

| GitHub signal | W118 output | Changes Core Task/Assignment? |
|---|---|---:|
| Issue created/updated | Issue mirror readback | No |
| `w118-handoff` label | HANDOFF_REQUESTED observation | No |
| `ACKED-...` comment | ACK_CLAIM_OBSERVED | No; Core identity service must verify |
| Push on aggregate/legacy branch | UNBOUND_LEGACY_BRANCH | No |
| Task-scoped push with exact binding | GITHUB_PUSH evidence intent | No |
| CI queued/running | Telemetry only | No |
| CI success/failure | GITHUB_ACTIONS_CI_RUN evidence intent | No |
| Issue closed | GITHUB_ISSUE_STATE_OBSERVED | No; Core decides |
| PR review submitted | GITHUB_REVIEW_OBSERVED | No; Core/W102 verifies reviewer authority |
| PR merged/release published | Source lifecycle observation | No |

CI PASS is not Task DONE, Assignment ACCEPTED, review approval or release authorization.

---

## 4. Permission and trust boundaries

| Principal / system | Allowed | Not allowed |
|---|---|---|
| Vinh — Product Owner | Approve plan/scope, explicit acceptance, authorize merge/release | No silent or inferred acceptance |
| Xu — Orchestrator | Coordinate W118 work, build adapters, request Core/W14 actions within exposed permissions | Cannot mint Agent identity, bypass Core authorization, merge/release |
| Core :8000 | Canonical Task/Assignment/Event state, authorization decisions and event persistence | No competing W118 runtime state store |
| W102 Agent Loop | Select/route/verify Agent according to policy | No W118 override |
| W14 | Sole owner of authorized code/test execution and GitHub operations through its integrated host/Gateway; W12/W13 are absorbed internal modules | No W118 parallel execution host |
| GitHub Actions | Run repository CI and capture source/test evidence with job-scoped permissions | No Task acceptance or Agent identity authority |
| W118 GitHub adapter | Issue mirror, source-binding validation, webhook verification, event normalization | No Task DB, dispatcher, event queue, Git Gateway or CI engine |
| W70 Dashboard | Read-only projection | No write-back to Task/Core state |

Security rules:
- Use Core/W01/W02/W22 verified principal mapping. GitHub login alone is not a ROOM-HOP principal.
- GitHub Assignee, label, comment or review state is not verified Agent ACK or acceptance.
- GitHub Actions permissions are read-only by default; Issue write is limited to request/observation comments. No `contents: write`, branch-protection bypass, secrets write, merge or release permission for W118 observation jobs.
- Secrets are runtime configuration only; never write tokens/webhook secrets into Task Register, journal or source.
- Webhook verification uses HMAC-SHA256, exact repository allowlist, event allowlist, UUID delivery ID, bounded body size and constant-time digest comparison.
- Core owns event deduplication/replay policy and durable persistence; W118 has no inbox database.

---

## 5. Data contracts

### 5.1 Core Task projection DTO (not a Core schema)

The actual Core API schema and field names must be supplied by the Core owner. W118 does not guess them. `core_task_adapter.py` requires an explicit approved field map and normalizes a read-only projection with:

- `work_id`, `task_id`, `correlation_id`
- `title`, `instruction`, `status`, `source_revision`
- `acceptance_checks[]`
- optional `wp_id`, `priority`, `scope_in[]`, `scope_out[]`
- optional `assigned_identity`, `issue_id`, `source_bindings[]`

This DTO is a W118 adapter interface, not a new canonical Task model. No writes to Core occur in this normalizer.

### 5.2 GitHub Issue mirror contract

- Stable marker: `<!-- room-hop-core-task:<task_id> -->`.
- Issue title/body are derived from the normalized Core snapshot and include `source_revision`.
- Issue labels are display projections only; no label can independently transition Core state.
- Mirror operation requires a Core-issued per-Task lock lease to prevent concurrent create races.
- Adapter scans paginated Issues, excludes Pull Requests, creates or updates one matching Issue, then exact-readbacks number/title/body.
- Result includes `issue_id`, `issue_url`, `correlation_id`, `core_source_revision`, `readback_verified`.
- No GitHub Assignee mutation, Issue close, merge or release from this adapter.

### 5.3 Source binding contract

Task-scoped branch:
`work/<work_id>/task-<task_id>`

Every commit in the push must include exactly one each:
`Work-ID: W###`
`Task-ID: W###-TASK-###`
`Issue: #<positive_issue_number>`

Validation requirements:
- repository allowlist matches;
- branch Work ID equals Task ID prefix;
- full 40-character commit SHA;
- push `after` equals `head_commit.id` and appears in commits;
- no force push or branch deletion;
- all commit trailers bind to the same Work/Task/Issue;
- Issue ID matches the Core Task's verified Issue link.

Legacy aggregate branches return `UNBOUND_LEGACY_BRANCH`; never guess a Task.

### 5.4 Stateless GitHub webhook envelope

Inputs: raw body bytes, `X-Hub-Signature-256`, `X-GitHub-Delivery`, `X-GitHub-Event`, expected repository and receive timestamp.

Verifier output:
- delivery UUID, event type, repository, received_at;
- parsed payload and SHA-256 digest;
- signature_verified=true;
- persistence_owner=ROOM_HOP_CORE_EVENT_PATH.

No SQLite inbox, local queue, sequence number or event persistence.

### 5.5 Core Event Intent DTO

W118 emits an intent, not a persisted Core event:

```json
{
  "task_id": "W118-TASK-016",
  "correlation_id": "corr-from-core",
  "type": "EVIDENCE_LINKED",
  "producer": {
    "kind": "adapter",
    "identity": "github-webhook",
    "adapter": "w118-github-event-adapter"
  },
  "payload": {
    "kind": "GITHUB_ACTIONS_CI_RUN",
    "repository": "owner/repo",
    "branch": "work/W118/task-W118-TASK-016",
    "head_sha": "<exact-40-char-sha>",
    "run_id": 12345,
    "conclusion": "success",
    "state_effect": "EVIDENCE_ONLY_NO_TASK_OR_ASSIGNMENT_TRANSITION"
  },
  "provenance": {
    "source": "adapter_synthesized",
    "native_ref": "<github-delivery-uuid>",
    "raw_sha256": "sha256:<payload-digest>"
  }
}
```

Core adds canonical `event_id`, `seq`, `ts`, persists the event and decides any Task/Assignment transition. W118 never assigns sequence or writes a local event ledger.

### 5.6 CI workflow_run binding

- Allowlist exact workflow name: `W118 Auto E2E Validation`.
- Require completed run, exact branch, full head SHA and positive run ID.
- Core Task snapshot must contain a prior source binding for the exact branch/head SHA/Issue ID.
- If CI arrives before the corresponding push evidence, return `DEFERRED`; Core reconciliation/redelivery handles ordering. No local queue.
- Success/failure is evidence only; no automatic Task/Assignment transition.

### 5.7 Data ownership matrix

| Data | Canonical owner | W118 role |
|---|---|---|
| W118 implementation plan/WP tasks | Sandbox W118 Task Register | Maintain project planning artifact |
| Runtime Task/Assignment/Event | Core :8000 | Read snapshot; submit normalized event intents |
| Agent identity/capability/authorization | W01/W02/W22 + Core/W102 | Consume verified decision only |
| Agent Loop policy/dispatch | W102 + Core/W52 path | No duplicate dispatcher |
| Execution run/logs | W14 | Supply Work Authority and consume evidence |
| Branch/commit/PR/review | GitHub | Validate and mirror metadata |
| CI run/artifact | GitHub Actions / W14 integration | Normalize evidence only |
| Work Journal | Canonical W118 Journal | Append build/check/test evidence |
| Work Evidence Register/Dashboard | W70 | Read-only mapping after owner/schema approval |

---

## 6. Event catalog

| GitHub event / signal | W118 result | Core action |
|---|---|---|
| `issues.labeled:w118-handoff` | HANDOFF_REQUESTED observation | Core/W102 decides whether to create Assignment |
| `issue_comment:ACKED-...` | ACK_CLAIM_OBSERVED with GitHub actor/comment ID | Core identity service verifies principal; no ACK inferred |
| `push` | GITHUB_PUSH evidence intent if exact binding passes | Core deduplicates and appends evidence |
| `workflow_run` | GITHUB_ACTIONS_CI_RUN evidence intent if exact SHA matches | Core appends CI evidence; no Task state inferred |
| `issues.closed/reopened` | GITHUB_ISSUE_STATE_OBSERVED | Core decides if mirror is consistent; Issue close is not Task DONE |
| `pull_request_review.submitted` | GITHUB_REVIEW_OBSERVED | Core/W102 verifies reviewer principal/authority |
| `pull_request.opened/synchronize/closed` | PR source observation | Core/W14 decides review/merge state |

Core-originated Task/Assignment events are not re-created by W118. All normalized event intents include native GitHub delivery reference and raw payload digest.

---

## 7. Errors and recovery policy

| Error | W118 result | Recovery owner |
|---|---|---|
| Invalid HMAC / missing signature | REJECTED (401-equivalent) | GitHub webhook sender/security |
| Wrong repository / event not allowlisted | REJECTED / UNHANDLED | Repository policy |
| Malformed payload / body too large | REJECTED | Sender/configuration |
| Core Task snapshot or field map unavailable | BLOCKED; no Issue mirror or event | Core owner |
| Core-issued Task lock missing | BLOCKED; no Issue create | Core adapter |
| Issue lookup pagination incomplete | BLOCKED; do not create possible duplicate | GitHub adapter retry after API recovery |
| Aggregate branch / no Task binding | UNBOUND; no event intent | Work Owner / source policy |
| Work/Task/Issue mismatch | REJECTED | Core/W14 source binding |
| CI before matching push | DEFERRED; no local queue | Core reconciliation / GitHub redelivery |
| CI workflow not allowlisted | REJECTED | Workflow policy owner |
| Core event port unavailable | SERVICE_UNAVAILABLE; no local persistence | Core service / GitHub redelivery |
| GitHub 403/429/5xx | Structured error; respect Retry-After/backoff at caller | GitHub API caller |
| W14 canonical execution path unavailable | BLOCKED; do not execute locally | W14 owner |
| W70 schema/owner ACK missing | BLOCKED projection; no W70 write | W70 owner |
| Merge/release not authorized | DENIED; repository unchanged | Vinh |

W118 does not implement a durable retry queue, dead-letter queue or event store. Those belong to Core infrastructure. Duplicate delivery is deduplicated by Core after successful forwarding; adapter functions remain stateless and safe to retry.

---

## 8. Test plan

### 8.1 Unit / contract tests owned by W118

| Test group | Required cases |
|---|---|
| Core Task projection | explicit field map, missing path, invalid types, duplicate AC, exact source revision |
| Issue mirror | stable marker, Core authority text, create/update/readback, pagination, PR exclusion, lock required, no assignee/state mutation |
| Source binding | task branch, all commit trailers, exact SHA, force push, delete, mismatch, legacy aggregate branch |
| Webhook verifier | HMAC valid/invalid, UUID, event/repository allowlist, body limit, malformed JSON, timestamp |
| Event adapter | push bound/unbound/mismatch, CI exact SHA, CI-before-push DEFERRED, workflow allowlist, issue/review observation only |
| Workflow contract | SHA-pinned Actions, least privilege, handoff request only, ACK claim only, review observation only, CI evidence classification |
| Security | GitHub actor is not Core principal, comments/labels never mutate Core state, no local DB/queue |

### 8.2 Integration tests — pending system ports

1. Core Task snapshot API returns approved schema/revision and field map.
2. Core per-Task lock lease controls Issue mirror concurrency.
3. W118 Issue adapter creates/updates one GitHub Issue and Core stores returned Issue reference.
4. Core event port accepts normalized event intent, assigns event ID/sequence and deduplicates delivery.
5. W102 verifies Agent principal and handles assignment/ACK; W118 never sets ACK.
6. W14 executes a controlled task branch through its canonical Work Authority/ExecutionHostBridge, pushes exact SHA and triggers GitHub Actions.
7. CI workflow_run event is verified, bound to Core source evidence and appended by Core.
8. W70 read-only projection matches canonical source fields after schema/owner approval.

### 8.3 Runtime E2E acceptance

A single non-sensitive pilot must prove:
`Sandbox Plan → Core Task → GitHub Issue → W102 Assignment/verified ACK → W14 executes → task-scoped Branch/Commit/Push → GitHub CI → W118 webhook/event adapter → Core event persistence → QE review → Vinh acceptance → Issue mirror sync`

Evidence must include exact Task ID, Assignment ID, actor principal, correlation ID, branch, commit SHA, PR ID, CI run ID/attempt, artifact digest, event IDs and Owner acceptance reference.

**Current limitation:** Sandbox MCP in this session exposes file operations only; W14's current manifest reports full product E2E NOT VERIFIED and current canonical GitHub source/runtime parity NOT VERIFIED. Therefore no runtime E2E is claimed.

---

## 9. Gate matrix and current state

| Gate | PASS condition | Current state |
|---|---|---|
| G-A Ownership/contract | Core/W102/W14 ownership and approved Core projection/event ports | DESIGN ALIGNED; Core API field map/port NOT PROVIDED |
| G-B Agent identity/assignment | Core/W102 verifies a real Agent principal and dispatch/ACK | BLOCKED — no verified runtime Agent principal in current evidence |
| G-C Execution | W14 canonical host executes controlled Task | BLOCKED — W14 source/API/runtime not verified |
| G-D GitHub Issue adapter | Core snapshot → Issue create/update/readback under Core lock | CONTRACT TESTS; live Core/API operation pending |
| G-E Source binding | Task branch/commit/push exact Work/Task/Issue/SHA | CONTRACT TESTS; task-scoped live push pending |
| G-F Webhook/event adapter | HMAC verification + event intent accepted by Core | VERIFIER/ADAPTER CONTRACT; Core event port pending |
| G-G CI | Exact SHA workflow_run evidence reconciled by Core/W12 | GitHub Actions CI contract exists; W14 integration/real callback pending |
| G-H W70 projection | Owner-approved read-only schema mapping and parity | BLOCKED — W70 owner/schema ACK pending |
| G-I Security/reliability | identity, replay, duplicate, out-of-order, rate-limit, permission and crash-window integration tests | UNIT/CONTRACT PARTIAL; runtime tests pending |
| G-J Product acceptance | Independent QE and Vinh accept exact revision | NOT STARTED |

No gate can be inferred from another. CI PASS does not substitute for identity, runtime E2E, QE or Owner acceptance.

---

## 10. Implementation sequence

| Order | Work Package | W118 deliverable | Dependency / gate |
|---|---|---|---|
| WP-A1 | Core Task Projection Adapter | Read-only Core snapshot normalizer and field-map contract | Core owner provides actual API schema/port |
| WP-A2 | GitHub Issue Mirror | Stable marker, Core lock lease, create/update/readback | WP-A1 |
| WP-B1 | Source Binding | Branch/commit/push validator with exact SHA | W14 absorbed GitHub Gateway contract |
| WP-B2 | Webhook Verifier + Event Adapter | Stateless HMAC verifier and Core event intent mapper | Core event port + approved Core projection |
| WP-B3 | W14 Integration | Work Authority, ExecutionHostBridge, GitHub Gateway/CI binding | W14 source and runtime contract exposed |
| WP-C1 | W102/W52/Core Assignment Integration | Handoff/ACK claim observations routed to Core/W102 | Verified identity and approved runtime port |
| WP-C2 | W70 Evidence Projection | Read-only mapping to approved Evidence Register/Dashboard | W70 owner/schema ACK |
| WP-X | Full Runtime E2E | End-to-end pilot and evidence pack | All prerequisite gates PASS |

No WP may introduce a second runtime Task database, Agent dispatcher, event bus, execution host or CI engine.

---

## 11. Explicit non-goals / prohibited shortcuts

- Do not implement a W118 SQLite Task Registry or any other local runtime Task database.
- Do not implement a durable W118 webhook inbox, event queue or event bus.
- Do not select/dispatch Agents from GitHub labels or Assignee fields.
- Do not treat GitHub comment ACK as verified Core Assignment ACK.
- Do not treat GitHub review approval as Core acceptance.
- Do not let CI PASS/FAIL mutate Task or Assignment status.
- Do not implement a new Git Gateway, Execution Host or CI engine; reuse W14's integrated path; W12/W13 are absorbed internal foundations.
- Do not modify W70 schema or dashboard without owner approval.
- Do not rebase/merge PR #67, merge to main, release or change branch protection without Vinh's explicit authorization.

---

## 12. Version and build status

- **Selected architecture:** A — Sandbox initiates; GitHub controls versioning.
- **W118 role:** GitHub-specific adapters and workflow evidence only.
- **Runtime Task/Assignment/Event authority:** Core :8000.
- **Agent Loop authority:** W102/Core; W52 is a draft communication contract reference.
- **Execution/GitHub/CI bridge:** W14 (with absorbed W12/W13 internal modules).
- **Work planning register:** Sandbox W118 `04_PLAN/TASK_REGISTER.json`.
- **Code authorization:** Vinh has instructed Xu to build without waiting for multi-agent review, within these ownership boundaries.
- **Current implementation status:** stateless Core/GitHub adapters and observation-only workflow contract implemented; exact-head CI 94/94 PASS at `5f02a9eafbf68eb0bcfca2942733882dab9cc5bf` (run #44882420198); no runtime E2E.
- **W118 overall:** ACTIVE — BUILD / VERIFY — NOT ACCEPTED — NOT RELEASED.
- **Git:** branch `work/118-auto-e2e-v2`; PR #67 remains unmerged. No rebase/merge/release performed.
# TD-118-012 — KIẾN TRÚC HAI QUY TRÌNH KHÉP KÍN SANDBOX–GITHUB

- **Work:** W118 — HQTT GitHub Workflow Automation
- **Document ID:** TD-118-012
- **Version:** 1.2
- **English name:** Sandbox–GitHub Dual Closed-Loop Architecture
- **Selected option:** A — Sandbox initiates; GitHub controls versioning.
- **Status:** OWNER-DIRECTED BUILD BASELINE — implementation may proceed within existing Work ownership and permission boundaries.
- **Authority:** Vinh (Product Owner); Xu coordinates technical implementation.
- **Date:** 2026-11-21 (UTC+07:00)
- **Scope:** Plan-to-Task orchestration and Sandbox–GitHub source/CI loop; ownership, states, permissions, data/event contracts, errors, tests and gates.
- **Git source:** `hqtt2026-thevinhvtqni/room-meeting-ai`, branch `work/118-auto-e2e-v2-clean`.
- **Related baselines:** W70 DOC-056 §9 / DOC-093 model; W102 DOC-012 consolidated architecture; W14 integrated execution contract; W14 W12/W13 absorption record; W16 Workflow Engine architecture; W52 A2A contract v0.1 (DRAFT); W112 DOC-001 (DRAFT_NOT_APPROVED).

> **Important:** Vinh has instructed Xu to build without waiting for multi-agent review. This document is the owner-directed implementation baseline, not independent QE approval, product acceptance, merge authorization or release authorization. No Work-owned Core/Agent/Execution/CI service may be duplicated by W118.

---

## 1. Architecture decision and system ownership

### 1.1 Selected option A

**Sandbox/ROOM-HOP khởi phát và điều phối kế hoạch; GitHub kiểm soát phiên bản mã nguồn, Issue/PR và CI.** Core :8000 remains the single runtime Task/Assignment/Event authority. W118 supplies GitHub-specific adapters and workflow evidence; it does not become a second orchestrator/runtime.

### 1.2 Existing Work ownership — mandatory reuse

| System / Work | Canonical responsibility | W118 integration boundary |
|---|---|---|
| **W70 — Work Lifecycle & Dashboard** | Work/WP lifecycle, Work-specific planning Task Register model, canonical Work Dashboard and evidence projection policy | W118 keeps its own planning register using DOC-093 model; Dashboard projection is read-only and requires W70 schema/owner approval |
| **Core :8000** | Sole canonical runtime Task identity/state, Assignment state, event persistence/sequence and authorization decisions | W118 consumes Core Task snapshots and submits normalized event intents through an approved Core port; no local Task DB or event store |
| **W102 — Agent Loop** | Agent Loop policy, role/capability routing, task execution governance and cross-role orchestration | W118 emits handoff/ACK/review observations; W102/Core decides eligibility, assignment, ACK and state |
| **W52 — A2A communication** | Provider-neutral communication/task-event contract reference; current contract is DRAFT | W118 maps GitHub events into an approved Core/W102 event adapter; do not treat draft schema as a live runtime |
| **W14 — Autonomous E2E Builder** | Sole product/delivery owner for integrated Work Authority, ExecutionHostBridge, GitHub Gateway and CI path | W118 consumes W14-approved contracts; W12/W13 are absorbed internal foundations only |
| **W12/W13 — absorbed foundations** | Historical WEE lifecycle/Execution Host contracts and modules owned internally by W14 | Not independent product owners; W118 must integrate through W14 only |
| **W01/W02/W22 + Core** | Identity, authentication, authorization and principal binding | W118 never treats GitHub login, label, comment or role-map text as a verified ROOM-HOP principal |
| **W16 — Workflow Engine** | Deterministic workflow engine architecture | Design reference/future integration; do not assume production runtime is available |
| **GitHub** | Version-controlled source, branches, commits, Issues, PRs, reviews, GitHub Actions runs and artifacts | Version/CI authority; Issue is a collaboration mirror of Core Task, not the runtime Task authority |

**W118 must not build or own:** a second Task database/registry, Agent Registry, dispatcher, durable event queue, Event Bus, execution host, Git Gateway, CI engine or cross-Work workflow engine.

### 1.3 W118 components

W118 owns only:
1. Work-specific planning Task Register for W118's own implementation tasks.
2. Read-only Core Task snapshot normalizer / GitHub Issue projection adapter.
3. GitHub source-binding validator (branch, commit trailers, Issue ID and exact SHA).
4. Stateless GitHub webhook signature/envelope verifier.
5. Stateless GitHub event-to-Core event-intent adapter.
6. GitHub Actions workflow contract tests and immutable CI evidence metadata.
7. Work-specific integration map, journal and acceptance/test evidence.

### 1.4 Non-negotiable principles

1. **Core runtime authority:** Core :8000 is the only canonical runtime Task/Assignment/Event store.
2. **Work plan ≠ runtime Task:** W118 `TASK_REGISTER.json` tracks W118 project/WP work; it is not a substitute for Core runtime Tasks.
3. **W102 owns Agent policy:** W118 never selects or dispatches an Agent independently.
4. **W14 owns integrated execution:** W12/W13 are absorbed internal foundations; W118 uses only W14's canonical Work Authority and ExecutionHostBridge. W118 never runs code through a parallel execution host or Git Gateway.
5. **GitHub owns source history:** exact branch, commit SHA, PR and CI run are read from GitHub.
6. **Issue is a mirror:** GitHub Issue labels/comments/Assignees never become Task or Assignment authority.
7. **Observation ≠ transition:** push, CI, Issue close and review events are evidence observations; Core/W102 alone decides state changes.
8. **No local event queue:** W118 verifies and normalizes delivery, then forwards to Core. Core owns deduplication, sequence, persistence and reconciliation.
9. **Fail closed:** unknown identity, schema, source binding, permission or Core mapping means REJECTED/BLOCKED/DEFERRED; never infer.
10. **No silent write-back:** every mirror/update has exact Core revision, GitHub readback and evidence.

---

## 2. Two connected closed-loop workflows

### 2.1 Workflow A — Plan → Core Task → Agent Loop → Verify → Close

`Work Plan (Sandbox) → W118 Work Task Register → Core Task Create/Read → GitHub Issue Mirror → W102 Policy / Core Assignment → Verified Agent ACK → W14 ExecutionHostBridge (using absorbed W12/W13 modules) → Core Task/Event Update → QE/Owner Acceptance → GitHub Issue Mirror Update → W70 Dashboard`

| Step | Owner | Action | Authoritative record |
|---|---|---|---|
| A1 Plan | Vinh / Work Owner | Define outcome, scope, WP, dependencies, AC and risk in Sandbox | W118 Work Plan / Task Register |
| A2 Task preparation | Xu / Planner | Break down Work WP into actionable project tasks; prepare Core task request | W118 plan artifact; not runtime Task state |
| A3 Runtime Task creation | Core :8000 | Create canonical Task, assign task ID/correlation and validate request | Core Task record |
| A4 Issue mirror | W118 GitHub adapter | Project normalized Core Task snapshot to GitHub Issue; stable Task marker; exact readback | GitHub Issue mirror + Core source revision |
| A5 Agent selection | W102 + Core + Identity | Verify principal, capability, availability, trust and least-privilege policy | Core/W102 assignment decision |
| A6 Dispatch / ACK | W102 + W52 + Core | Dispatch to verified principal; bind ACK to Task/Assignment/dispatch; reject replay | Core Assignment/Event |
| A7 Execution | W14 | Execute task through canonical W14 Work Authority/ExecutionHostBridge; record command, source revision and output | W14 execution record / GitHub commit |
| A8 Progress / blocker | Core + W102 | Persist progress, blocker, retry/reassignment and state | Core Task/Event |
| A9 Verification | QE / Verifier | Verify deliverable against AC and exact source SHA | Core/W102 verification evidence |
| A10 Owner acceptance | Vinh | Accept/reject exact deliverable and revision | Core acceptance event + Work Journal |
| A11 Close mirror | W118 adapter | Update/close GitHub Issue only after Core says Task is complete; readback | GitHub Issue mirror |
| A12 Dashboard | W70 | Read-only projection of approved Work/Task/evidence fields | W70 Dashboard |

**Owner-directed build exception:** Vinh may directly instruct Xu to work in the current conversation. W118 records that as a project-level execution authorization in its Work plan. It does not create a fake Core Assignment, Agent principal or ACK. Agent-runtime work still requires Core/W102 identity and Assignment verification.

### 2.2 Workflow B — Sandbox → WEE → GitHub → CI → Core → Sandbox

`Core-authorized Task → W14 Work Authority / ExecutionHostBridge → GitHub Gateway → Branch → Code/Test → Commit/Push → GitHub Actions CI → W118 Stateless Webhook Verify/Normalize → Core Event Port → W102/Core Decision → W14 bounded repair/review integration → Owner Acceptance`

| Step | Owner | Action | Authority / evidence |
|---|---|---|---|
| B1 Authorization | Core/W102 | Confirm Task and Assignment are authorized for execution | Core Task/Assignment snapshot |
| B2 Work Authority | W14 + W118 | Consume W14-authorized repository, branch, base SHA, workspace, test entrypoint and policy refs | W14 Work Authority + W118 projection |
| B3 Source sync | W14 (absorbed W12 Gateway) | Resolve repo/branch/head and sync exact base SHA | GitHub ref/commit |
| B4 Build/test | W14 (absorbed W12/W13 modules) | Execute code/tests in the canonical authorized host | W14 execution ID, logs, test result |
| B5 Commit/push | W14 (absorbed GitHub Gateway) | Enforce branch ownership, source binding, exact SHA and permission | GitHub commit/ref |
| B6 CI | GitHub Actions / W14 integration | Run allowlisted workflow and capture run ID, attempt, conclusion, head SHA and artifact digest | GitHub Actions |
| B7 Webhook verify | W118 | Verify HMAC, repository allowlist, event allowlist, delivery UUID and payload digest | Stateless verified envelope |
| B8 Event normalize | W118 | Match event to Core Task snapshot/source binding; produce event intent only | Core Event Intent DTO |
| B9 Persist/reconcile | Core :8000 | Deduplicate, assign event ID/sequence, persist, reconcile out-of-order events and decide state | Core event store |
| B10 Repair/review | W102/W14 | Route failure to authorized repair; bounded policy; open/update PR | Core + GitHub |
| B11 Acceptance | QE / Vinh | Independent verification and explicit Owner acceptance | Core/Work Journal |
| B12 Mirror sync | W118 | Update Issue from latest Core snapshot; verify exact readback | GitHub Issue mirror |

**Critical boundary:** W118 webhook code does not persist an inbox or queue. If Core's event port is unavailable, the adapter returns a structured unavailable/deferred result; GitHub redelivery or Core reconciliation owns recovery. No local W118 queue is created.

---

## 3. State model and status matrices

### 3.1 W118 Work planning Task Register

W118's `04_PLAN/TASK_REGISTER.json` is the Work-specific planning register modeled on W70 DOC-093. It tracks the implementation tasks of Work 118 only.

| Field | Purpose |
|---|---|
| `task_id`, `wp_id`, `phase` | Work-scoped project planning identity |
| `status` | Work plan status: PLANNED/READY/IN_PROGRESS/BLOCKED/IN_REVIEW/DONE/CANCELLED |
| `execution_mode` | OWNER_DIRECTED_BUILD or CORE_AGENT_TASK; project-level authorization mode, not runtime Assignment state |
| `owner_directive_ref` | Required for Owner-directed build tasks |
| `assigned_identity` | Optional planned identity only; never proof of runtime identity |
| `core_task_id`, `correlation_id` | Null until Core creates and returns the runtime Task mapping |
| `evidence_refs`, `next_action`, `blockers` | Project evidence and next step |

The Work planning status is not copied into Core by assumption. Core runtime state remains authoritative for actual Agent execution.

### 3.2 Core runtime Task / Assignment status

- Core :8000 owns runtime Task status and Assignment status.
- W102 owns Agent Loop policy and transition decisions.
- W52 A2A v0.1 and W112 DOC-001 are design references only while their status remains DRAFT.
- W118 consumes a normalized Core Task projection and never implements a second transition engine.

| Core runtime domain | Known compatibility vocabulary | W118 behavior |
|---|---|---|
| Task | PLANNED, READY, IN_PROGRESS, BLOCKED, IN_REVIEW, DONE, CANCELLED | Read-only projection; no local transition |
| Assignment | PROPOSED, DISPATCHED, ACKNOWLEDGED, IN_PROGRESS, SUBMITTED, ACCEPTED, REJECTED, BLOCKED, CANCELLED | Read-only projection; no local Assignment store |
| Event | Core-assigned event ID, sequence, timestamp, task/correlation binding | W118 submits event intent; Core assigns ID/sequence and persists |

### 3.3 GitHub source/CI observations

| GitHub signal | W118 output | Changes Core Task/Assignment? |
|---|---|---:|
| Issue created/updated | Issue mirror readback | No |
| `w118-handoff` label | HANDOFF_REQUESTED observation | No |
| `ACKED-...` comment | ACK_CLAIM_OBSERVED | No; Core identity service must verify |
| Push on aggregate/legacy branch | UNBOUND_LEGACY_BRANCH | No |
| Task-scoped push with exact binding | GITHUB_PUSH evidence intent | No |
| CI queued/running | Telemetry only | No |
| CI success/failure | GITHUB_ACTIONS_CI_RUN evidence intent | No |
| Issue closed | GITHUB_ISSUE_STATE_OBSERVED | No; Core decides |
| PR review submitted | GITHUB_REVIEW_OBSERVED | No; Core/W102 verifies reviewer authority |
| PR merged/release published | Source lifecycle observation | No |

CI PASS is not Task DONE, Assignment ACCEPTED, review approval or release authorization.

---

## 4. Permission and trust boundaries

| Principal / system | Allowed | Not allowed |
|---|---|---|
| Vinh — Product Owner | Approve plan/scope, explicit acceptance, authorize merge/release | No silent or inferred acceptance |
| Xu — Orchestrator | Coordinate W118 work, build adapters, request Core/W14 actions within exposed permissions | Cannot mint Agent identity, bypass Core authorization, merge/release |
| Core :8000 | Canonical Task/Assignment/Event state, authorization decisions and event persistence | No competing W118 runtime state store |
| W102 Agent Loop | Select/route/verify Agent according to policy | No W118 override |
| W14 | Sole owner of authorized code/test execution and GitHub operations through its integrated host/Gateway; W12/W13 are absorbed internal modules | No W118 parallel execution host |
| GitHub Actions | Run repository CI and capture source/test evidence with job-scoped permissions | No Task acceptance or Agent identity authority |
| W118 GitHub adapter | Issue mirror, source-binding validation, webhook verification, event normalization | No Task DB, dispatcher, event queue, Git Gateway or CI engine |
| W70 Dashboard | Read-only projection | No write-back to Task/Core state |

Security rules:
- Use Core/W01/W02/W22 verified principal mapping. GitHub login alone is not a ROOM-HOP principal.
- GitHub Assignee, label, comment or review state is not verified Agent ACK or acceptance.
- GitHub Actions permissions are read-only by default; Issue write is limited to request/observation comments. No `contents: write`, branch-protection bypass, secrets write, merge or release permission for W118 observation jobs.
- Secrets are runtime configuration only; never write tokens/webhook secrets into Task Register, journal or source.
- Webhook verification uses HMAC-SHA256, exact repository allowlist, event allowlist, UUID delivery ID, bounded body size and constant-time digest comparison.
- Core owns event deduplication/replay policy and durable persistence; W118 has no inbox database.

---

## 5. Data contracts

### 5.1 Core Task projection DTO (not a Core schema)

The actual Core API schema and field names must be supplied by the Core owner. W118 does not guess them. `core_task_adapter.py` requires an explicit approved field map and normalizes a read-only projection with:

- `work_id`, `task_id`, `correlation_id`
- `title`, `instruction`, `status`, `source_revision`
- `acceptance_checks[]`
- optional `wp_id`, `priority`, `scope_in[]`, `scope_out[]`
- optional `assigned_identity`, `issue_id`, `source_bindings[]`

This DTO is a W118 adapter interface, not a new canonical Task model. No writes to Core occur in this normalizer.

### 5.2 GitHub Issue mirror contract

- Stable marker: `<!-- room-hop-core-task:<task_id> -->`.
- Issue title/body are derived from the normalized Core snapshot and include `source_revision`.
- Issue labels are display projections only; no label can independently transition Core state.
- Mirror operation requires a Core-issued per-Task lock lease to prevent concurrent create races.
- Adapter scans paginated Issues, excludes Pull Requests, creates or updates one matching Issue, then exact-readbacks number/title/body.
- Result includes `issue_id`, `issue_url`, `correlation_id`, `core_source_revision`, `readback_verified`.
- No GitHub Assignee mutation, Issue close, merge or release from this adapter.

### 5.3 Source binding contract

Task-scoped branch:
`work/<work_id>/task-<task_id>`

Every commit in the push must include exactly one each:
`Work-ID: W###`
`Task-ID: W###-TASK-###`
`Issue: #<positive_issue_number>`

Validation requirements:
- repository allowlist matches;
- branch Work ID equals Task ID prefix;
- full 40-character commit SHA;
- push `after` equals `head_commit.id` and appears in commits;
- no force push or branch deletion;
- all commit trailers bind to the same Work/Task/Issue;
- Issue ID matches the Core Task's verified Issue link.

Legacy aggregate branches return `UNBOUND_LEGACY_BRANCH`; never guess a Task.

### 5.4 Stateless GitHub webhook envelope

Inputs: raw body bytes, `X-Hub-Signature-256`, `X-GitHub-Delivery`, `X-GitHub-Event`, expected repository and receive timestamp.

Verifier output:
- delivery UUID, event type, repository, received_at;
- parsed payload and SHA-256 digest;
- signature_verified=true;
- persistence_owner=ROOM_HOP_CORE_EVENT_PATH.

No SQLite inbox, local queue, sequence number or event persistence.

### 5.5 Core Event Intent DTO

W118 emits an intent, not a persisted Core event:

```json
{
  "task_id": "W118-TASK-016",
  "correlation_id": "corr-from-core",
  "type": "EVIDENCE_LINKED",
  "producer": {
    "kind": "adapter",
    "identity": "github-webhook",
    "adapter": "w118-github-event-adapter"
  },
  "payload": {
    "kind": "GITHUB_ACTIONS_CI_RUN",
    "repository": "owner/repo",
    "branch": "work/W118/task-W118-TASK-016",
    "head_sha": "<exact-40-char-sha>",
    "run_id": 12345,
    "conclusion": "success",
    "state_effect": "EVIDENCE_ONLY_NO_TASK_OR_ASSIGNMENT_TRANSITION"
  },
  "provenance": {
    "source": "adapter_synthesized",
    "native_ref": "<github-delivery-uuid>",
    "raw_sha256": "sha256:<payload-digest>"
  }
}
```

Core adds canonical `event_id`, `seq`, `ts`, persists the event and decides any Task/Assignment transition. W118 never assigns sequence or writes a local event ledger.

### 5.6 CI workflow_run binding

- Allowlist exact workflow name: `W118 Auto E2E Validation`.
- Require completed run, exact branch, full head SHA and positive run ID.
- Core Task snapshot must contain a prior source binding for the exact branch/head SHA/Issue ID.
- If CI arrives before the corresponding push evidence, return `DEFERRED`; Core reconciliation/redelivery handles ordering. No local queue.
- Success/failure is evidence only; no automatic Task/Assignment transition.

### 5.7 Data ownership matrix

| Data | Canonical owner | W118 role |
|---|---|---|
| W118 implementation plan/WP tasks | Sandbox W118 Task Register | Maintain project planning artifact |
| Runtime Task/Assignment/Event | Core :8000 | Read snapshot; submit normalized event intents |
| Agent identity/capability/authorization | W01/W02/W22 + Core/W102 | Consume verified decision only |
| Agent Loop policy/dispatch | W102 + Core/W52 path | No duplicate dispatcher |
| Execution run/logs | W14 | Supply Work Authority and consume evidence |
| Branch/commit/PR/review | GitHub | Validate and mirror metadata |
| CI run/artifact | GitHub Actions / W14 integration | Normalize evidence only |
| Work Journal | Canonical W118 Journal | Append build/check/test evidence |
| Work Evidence Register/Dashboard | W70 | Read-only mapping after owner/schema approval |

---

## 6. Event catalog

| GitHub event / signal | W118 result | Core action |
|---|---|---|
| `issues.labeled:w118-handoff` | HANDOFF_REQUESTED observation | Core/W102 decides whether to create Assignment |
| `issue_comment:ACKED-...` | ACK_CLAIM_OBSERVED with GitHub actor/comment ID | Core identity service verifies principal; no ACK inferred |
| `push` | GITHUB_PUSH evidence intent if exact binding passes | Core deduplicates and appends evidence |
| `workflow_run` | GITHUB_ACTIONS_CI_RUN evidence intent if exact SHA matches | Core appends CI evidence; no Task state inferred |
| `issues.closed/reopened` | GITHUB_ISSUE_STATE_OBSERVED | Core decides if mirror is consistent; Issue close is not Task DONE |
| `pull_request_review.submitted` | GITHUB_REVIEW_OBSERVED | Core/W102 verifies reviewer principal/authority |
| `pull_request.opened/synchronize/closed` | PR source observation | Core/W14 decides review/merge state |

Core-originated Task/Assignment events are not re-created by W118. All normalized event intents include native GitHub delivery reference and raw payload digest.

---

## 7. Errors and recovery policy

| Error | W118 result | Recovery owner |
|---|---|---|
| Invalid HMAC / missing signature | REJECTED (401-equivalent) | GitHub webhook sender/security |
| Wrong repository / event not allowlisted | REJECTED / UNHANDLED | Repository policy |
| Malformed payload / body too large | REJECTED | Sender/configuration |
| Core Task snapshot or field map unavailable | BLOCKED; no Issue mirror or event | Core owner |
| Core-issued Task lock missing | BLOCKED; no Issue create | Core adapter |
| Issue lookup pagination incomplete | BLOCKED; do not create possible duplicate | GitHub adapter retry after API recovery |
| Aggregate branch / no Task binding | UNBOUND; no event intent | Work Owner / source policy |
| Work/Task/Issue mismatch | REJECTED | Core/W14 source binding |
| CI before matching push | DEFERRED; no local queue | Core reconciliation / GitHub redelivery |
| CI workflow not allowlisted | REJECTED | Workflow policy owner |
| Core event port unavailable | SERVICE_UNAVAILABLE; no local persistence | Core service / GitHub redelivery |
| GitHub 403/429/5xx | Structured error; respect Retry-After/backoff at caller | GitHub API caller |
| W14 canonical execution path unavailable | BLOCKED; do not execute locally | W14 owner |
| W70 schema/owner ACK missing | BLOCKED projection; no W70 write | W70 owner |
| Merge/release not authorized | DENIED; repository unchanged | Vinh |

W118 does not implement a durable retry queue, dead-letter queue or event store. Those belong to Core infrastructure. Duplicate delivery is deduplicated by Core after successful forwarding; adapter functions remain stateless and safe to retry.

---

## 8. Test plan

### 8.1 Unit / contract tests owned by W118

| Test group | Required cases |
|---|---|
| Core Task projection | explicit field map, missing path, invalid types, duplicate AC, exact source revision |
| Issue mirror | stable marker, Core authority text, create/update/readback, pagination, PR exclusion, lock required, no assignee/state mutation |
| Source binding | task branch, all commit trailers, exact SHA, force push, delete, mismatch, legacy aggregate branch |
| Webhook verifier | HMAC valid/invalid, UUID, event/repository allowlist, body limit, malformed JSON, timestamp |
| Event adapter | push bound/unbound/mismatch, CI exact SHA, CI-before-push DEFERRED, workflow allowlist, issue/review observation only |
| Workflow contract | SHA-pinned Actions, least privilege, handoff request only, ACK claim only, review observation only, CI evidence classification |
| Security | GitHub actor is not Core principal, comments/labels never mutate Core state, no local DB/queue |

### 8.2 Integration tests — pending system ports

1. Core Task snapshot API returns approved schema/revision and field map.
2. Core per-Task lock lease controls Issue mirror concurrency.
3. W118 Issue adapter creates/updates one GitHub Issue and Core stores returned Issue reference.
4. Core event port accepts normalized event intent, assigns event ID/sequence and deduplicates delivery.
5. W102 verifies Agent principal and handles assignment/ACK; W118 never sets ACK.
6. W14 executes a controlled task branch through its canonical Work Authority/ExecutionHostBridge, pushes exact SHA and triggers GitHub Actions.
7. CI workflow_run event is verified, bound to Core source evidence and appended by Core.
8. W70 read-only projection matches canonical source fields after schema/owner approval.

### 8.3 Runtime E2E acceptance

A single non-sensitive pilot must prove:
`Sandbox Plan → Core Task → GitHub Issue → W102 Assignment/verified ACK → W14 executes → task-scoped Branch/Commit/Push → GitHub CI → W118 webhook/event adapter → Core event persistence → QE review → Vinh acceptance → Issue mirror sync`

Evidence must include exact Task ID, Assignment ID, actor principal, correlation ID, branch, commit SHA, PR ID, CI run ID/attempt, artifact digest, event IDs and Owner acceptance reference.

**Current limitation:** Sandbox MCP in this session exposes file operations only; W14's current manifest reports full product E2E NOT VERIFIED and current canonical GitHub source/runtime parity NOT VERIFIED. Therefore no runtime E2E is claimed.

---

## 9. Gate matrix and current state

| Gate | PASS condition | Current state |
|---|---|---|
| G-A Ownership/contract | Core/W102/W14 ownership and approved Core projection/event ports | DESIGN ALIGNED; Core API field map/port NOT PROVIDED |
| G-B Agent identity/assignment | Core/W102 verifies a real Agent principal and dispatch/ACK | BLOCKED — no verified runtime Agent principal in current evidence |
| G-C Execution | W14 canonical host executes controlled Task | BLOCKED — W14 source/API/runtime not verified |
| G-D GitHub Issue adapter | Core snapshot → Issue create/update/readback under Core lock | CONTRACT TESTS; live Core/API operation pending |
| G-E Source binding | Task branch/commit/push exact Work/Task/Issue/SHA | CONTRACT TESTS; task-scoped live push pending |
| G-F Webhook/event adapter | HMAC verification + event intent accepted by Core | VERIFIER/ADAPTER CONTRACT; Core event port pending |
| G-G CI | Exact SHA workflow_run evidence reconciled by Core/W12 | GitHub Actions CI contract exists; W14 integration/real callback pending |
| G-H W70 projection | Owner-approved read-only schema mapping and parity | BLOCKED — W70 owner/schema ACK pending |
| G-I Security/reliability | identity, replay, duplicate, out-of-order, rate-limit, permission and crash-window integration tests | UNIT/CONTRACT PARTIAL; runtime tests pending |
| G-J Product acceptance | Independent QE and Vinh accept exact revision | NOT STARTED |

No gate can be inferred from another. CI PASS does not substitute for identity, runtime E2E, QE or Owner acceptance.

---

## 10. Implementation sequence

| Order | Work Package | W118 deliverable | Dependency / gate |
|---|---|---|---|
| WP-A1 | Core Task Projection Adapter | Read-only Core snapshot normalizer and field-map contract | Core owner provides actual API schema/port |
| WP-A2 | GitHub Issue Mirror | Stable marker, Core lock lease, create/update/readback | WP-A1 |
| WP-B1 | Source Binding | Branch/commit/push validator with exact SHA | W14 absorbed GitHub Gateway contract |
| WP-B2 | Webhook Verifier + Event Adapter | Stateless HMAC verifier and Core event intent mapper | Core event port + approved Core projection |
| WP-B3 | W14 Integration | Work Authority, ExecutionHostBridge, GitHub Gateway/CI binding | W14 source and runtime contract exposed |
| WP-C1 | W102/W52/Core Assignment Integration | Handoff/ACK claim observations routed to Core/W102 | Verified identity and approved runtime port |
| WP-C2 | W70 Evidence Projection | Read-only mapping to approved Evidence Register/Dashboard | W70 owner/schema ACK |
| WP-X | Full Runtime E2E | End-to-end pilot and evidence pack | All prerequisite gates PASS |

No WP may introduce a second runtime Task database, Agent dispatcher, event bus, execution host or CI engine.

---

## 11. Explicit non-goals / prohibited shortcuts

- Do not implement a W118 SQLite Task Registry or any other local runtime Task database.
- Do not implement a durable W118 webhook inbox, event queue or event bus.
- Do not select/dispatch Agents from GitHub labels or Assignee fields.
- Do not treat GitHub comment ACK as verified Core Assignment ACK.
- Do not treat GitHub review approval as Core acceptance.
- Do not let CI PASS/FAIL mutate Task or Assignment status.
- Do not implement a new Git Gateway, Execution Host or CI engine; reuse W14's integrated path; W12/W13 are absorbed internal foundations.
- Do not modify W70 schema or dashboard without owner approval.
- Do not rebase/merge PR #67, merge to main, release or change branch protection without Vinh's explicit authorization.

---

## 12. Version and build status

- **Selected architecture:** A — Sandbox initiates; GitHub controls versioning.
- **W118 role:** GitHub-specific adapters and workflow evidence only.
- **Runtime Task/Assignment/Event authority:** Core :8000.
- **Agent Loop authority:** W102/Core; W52 is a draft communication contract reference.
- **Execution/GitHub/CI bridge:** W14 (with absorbed W12/W13 internal modules).
- **Work planning register:** Sandbox W118 `04_PLAN/TASK_REGISTER.json`.
- **Code authorization:** Vinh has instructed Xu to build without waiting for multi-agent review, within these ownership boundaries.
- **Current implementation status:** stateless Core/GitHub adapters and observation-only workflow contract implemented; exact-head CI 94/94 PASS at `5f02a9eafbf68eb0bcfca2942733882dab9cc5bf` (run #44882420198); no runtime E2E.
- **W118 overall:** ACTIVE — BUILD / VERIFY — NOT ACCEPTED — NOT RELEASED.
- **Git:** branch `work/118-auto-e2e-v2`; PR #67 remains unmerged. No rebase/merge/release performed.


## 13. Current branch and exact-head verification — 2026-11-22

- **Delivery candidate:** PR #68, branch `work/118-auto-e2e-v2-clean`, isolated from current Main; base `43efc145c9f7007284366e8edb4f4805191bb3ad`; head at isolation `c291c29890ad726c1afdfca00f7832662622c19a`; 1 ahead / 0 behind.
- **Scope:** only W118 workflow, adapters, tests and Work 118 documentation are changed. The previous PR #67 branch is superseded due to cross-Work paths and branch divergence; it remains unmerged for historical evidence.
- **Exact-head CI:** PR run #44948921625; validate SUCCESS; 94 tests PASS; artifact 14724581468; digest `9661e45026e42edda828ef6294dbd14d45d811597e324aba4da8d81935c11da4`.
- **Limitation:** event-specific jobs skipped on PR synchronize. No runtime E2E claim; Core/W102/W12/W13/W70 external integration gates remain open.
- **Authority:** Ka executes technical build; Xu independently reviews; Vinh retains final product acceptance and separate release authority.
- **State:** ACTIVE — BUILD / VERIFY — NOT ACCEPTED — NOT RELEASED.


## 14. Amendment v1.3 — W14 is the sole integrated execution owner

**Source evidence:** W12 Work Manifest (COMPLETED / absorbed by W14); W13 Work Manifest (COMPLETED / ABSORBED_BY_W14); W14 Work Manifest (ACTIVE — sole product owner for W12+W13+W14 consolidation); W14 `W12_W13_ABSORPTION_RECORD.md`; W14 `DOC-001_W14_WORK_MANIFEST.md`.

### Binding ownership correction
- **W14** is the sole product/delivery/release owner for the integrated autonomous execution product, Work Authority, ExecutionHostBridge, GitHub Gateway/CI integration and end-to-end acceptance.
- **W12/W13** are absorbed internal foundations and historical source/provenance. They are not independent product owners or direct integration targets for W118.
- **Core :8000** remains sole runtime Task/Assignment/Event authority.
- **W102** owns Agent Loop policy and verified principal/Assignment integration.
- **W70** owns canonical Work lifecycle, Evidence Register and Dashboard projection.
- **W118** owns only Work planning metadata, stateless GitHub-specific adapters, source binding, event normalization and evidence metadata.

### Required W118 integration route
`Sandbox Plan → Core Task → GitHub Issue mirror → W102/Core Assignment → W14 Work Authority → W14 ExecutionHostBridge → absorbed W12/W13 modules → GitHub Gateway/CI → W118 stateless event adapter → Core Event Port → QE/Owner acceptance`.

### Current blocker
W14 is ACTIVE / UNLOCKED, but its manifest says current canonical GitHub source/ref parity is NOT VERIFIED and full product E2E is NOT VERIFIED. W13 bridge evidence records live :8031 E2E as NOT RUN / BLOCKED from the inspected session. W118 must therefore keep W118-TASK-015 BLOCKED until W14 provides its approved source/API/runtime contract and live evidence. Do not modify W12/W13 or create a parallel host/Gateway.

This amendment supersedes earlier ownership-table entries in this document that describe W12/W13 as independent execution owners. Historical source references remain for provenance only.
