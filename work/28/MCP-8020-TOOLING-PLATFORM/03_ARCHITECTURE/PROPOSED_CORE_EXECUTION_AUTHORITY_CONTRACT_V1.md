# Core Execution Authority & Agent-to-Computer Integration Contract — V1.3

- Work: W28 — MCP Tooling Platform
- Contract ID: AD-W28-20261123-002 / Core Execution Authority Contract V1.3
- Revision date: 2026-11-23
- Decision authority: Vinh
- Architecture decision owner: Xu (under Vinh's explicit delegation dated 2026-11-23)
- Status: **ARCHITECTURE BASELINE DECIDED — IMPLEMENTATION NOT APPROVED BY THIS DOCUMENT ALONE; NOT DEPLOYED; NOT WIRED; NOT RELEASED**
- Supersedes: proposed V1.2 only for the authority split and integration boundaries described here. V1.2 historical evidence remains preserved.

## 1. Purpose and scope

This contract defines the single authorized Agent-to-Computer path for ROOM-HOP. It resolves the W28/W52/W14/W70 ownership overlap while preserving one Core authority and one canonical Execution Host product.

It is an architecture and interface contract. It does not assert that any endpoint, service, Agent identity, queue, HostPort transport, Computer provider, or deployment currently exists or is operational.

## 2. Normative ownership and state boundaries

### 2.1 W70 — Work control plane
W70 owns Work, Work Package (WP), Gate, and Work lifecycle state. It decides whether the Work/Gate permits a requested operation. Work lifecycle MUST NOT be collapsed into Agent task state or Host run state.

### 2.2 Core :8000 — sole authority and durable system of record
The existing Core :8000 remains the only ROOM-HOP authority boundary. Core is accountable for:
- authenticating and enrolling service/Agent principals, including credential status, capability and revocation;
- evaluating Work policy and Gate eligibility using authoritative W70 state or its verified policy interface;
- issuing, validating, expiring and revoking narrowly scoped execution grants;
- enforcing identity, Work, assignment, task, action, provider/Host, source snapshot, environment and expiry bindings;
- maintaining the authoritative append-only task/authorization/run evidence ledger and invariant enforcement;
- deduplicating idempotent commands and atomically appending ordered, correlated events.

This contract does not create Core 2, an independent grant service, or a parallel authority. Any execution-authority capability must be implemented as an additive, governed extension of the existing Core authority. Existing meeting API compatibility must be preserved.

### 2.3 W52 — Agent orchestration and delivery protocol
W52 owns provider-neutral Agent-to-Agent orchestration:
- task/assignment/event contracts and versioning;
- capability negotiation and recipient selection;
- dispatch, delivery receipts, authenticated recipient ACK/NACK;
- Agent/task state-machine semantics and transition protocol;
- transport adapters, retry/cancel/timeout/recovery semantics and event cursor delivery.

Core remains the authoritative durable ledger and policy/invariant enforcement point. W52 MUST NOT mint grants, self-authorize, claim ACK from task creation/session intake, or maintain a competing authoritative task ledger. W52 owns orchestration semantics, not execution authority.

### 2.4 W14 — sole Execution Host product and side-effect boundary
W14 is the sole product/delivery/release owner for the consolidated Execution Host. W12 and W13 are absorbed internal foundations/historical provenance, not separate active Host products. W14 MUST:
- authenticate the calling service and validate a live Core-issued grant server-side before any side effect;
- bind every Host run to the exact Work, task, assignment, Agent principal, grant, provider, action, source snapshot, environment and correlation IDs;
- enforce process-tree containment before untrusted code starts, OS isolation, quotas, timeout, cancellation and descendant cleanup;
- persist correlated Host run observations and immutable evidence references;
- expose the HostPort capabilities required by W52, or explicitly declare a capability unsupported. A one-shot HTTP endpoint is not proof of a bidirectional HostPort implementation.

No second Execution Host is permitted. The canonical W14 source branch, release SHA and deployment identity must be reconciled before source edits or runtime claims.

### 2.5 W10 — Computer provider candidate only
W10 COMPUTER-AGENT is a provider candidate, not the task recipient Agent and not an authorization boundary. W10 remains **LOCKED / NO CHANGE**. Its API MUST NOT be called directly as a ROOM-HOP execution path. Any future provider invocation must be mediated by W14 after Core authorization and W52 recipient ACK requirements are satisfied.

### 2.6 W092 and W113 — read-only projections
W092 and W113 consume authoritative, correlated events and project task/run status. They MUST NOT synthesize runtime transitions, infer ACK, infer Agent identity from an organization roster, or turn mock/UI states into runtime evidence.

## 3. Canonical identities and correlated records

Every real execution attempt must carry stable identifiers:
- `work_id`, `wp_id` and current Gate/policy version;
- `task_id`, `assignment_id`, `idempotency_key`, `correlation_id`;
- authenticated `agent_principal_id` and runtime instance/build identity;
- `grant_id`, `host_id`, `provider_id`, `run_id`;
- source repository, branch, commit/tree digest and immutable input snapshot;
- action/capability scope, environment, created/expiry timestamps and event sequence.

A human-readable Agent name, model name, chat session, browser session, or roster entry is not an authenticated runtime identity.

## 4. Required lifecycle and authority flow

1. **Work eligibility:** W70 exposes the authoritative Work/WP/Gate decision. Core checks that the requested operation is eligible.
2. **Assignment:** W52 creates an idempotent assignment for one enrolled Agent principal, with exact task, capability and source snapshot references.
3. **Dispatch:** W52 delivers the assignment using an authenticated transport and records delivery attempt/receipt. Delivery is not ACK.
4. **Recipient ACK:** the actual Agent runtime emits an authenticated ACK/NACK bound to assignment_id, task_id, agent_principal_id, runtime identity and correlation_id. Core verifies the principal and persists the event. Session intake or a task-created response is never ACK.
5. **Grant:** after authenticated ACK and policy approval, Core issues a short-lived, least-privilege grant bound to the exact Work, WP/Gate, task, assignment, Agent principal, Host, provider, actions, source snapshot, environment and expiry. Revoke/expiry must be checked online by W14 before every side-effect boundary.
6. **Host run:** W14 validates the grant and recipient binding server-side, establishes containment and records the run before invoking an allowed provider. No caller-supplied `authorized: true` Boolean is trusted.
7. **Provider result:** provider observations/actions/results are returned through W14 and bound to the same run/task/correlation IDs. Unsupported capabilities fail closed.
8. **Events and projection:** Core durably appends authoritative events; W52 transports/subscribes to them; W092/W113 render the source state and provenance.
9. **Terminal state:** W52 defines task terminal semantics; Core persists and validates the transition. W14 run outcome remains a separate state correlated to the task. A provider-reported success is not automatically Work acceptance PASS.

Minimum visible task lifecycle: `QUEUED → ASSIGNED → DISPATCHED → ACKNOWLEDGED → RUNNING → VERIFYING → SUCCEEDED | FAILED | BLOCKED | CANCELLED | TIMED_OUT`. Delivery-attempt and Host-run states remain separate dimensions. State names may be versioned by W52, but transitions must be explicit, validated and durably recorded.

## 5. Security invariants

- **INV-1 — Single authority:** Core :8000 is the sole authority; no MCP, Agent, W52 adapter, W14 Host or UI self-authorizes.
- **INV-2 — Authenticated identity:** service and Agent principals are enrolled, credential-backed, revocable and runtime-verifiable. No identity from request body or display name.
- **INV-3 — Recipient-bound ACK:** only an authenticated event from the assigned runtime satisfies ACK; replay, wrong task, wrong assignment or wrong principal is rejected.
- **INV-4 — Least-privilege grant:** grant binds all fields in §3 and is short-lived, online-checkable, revocable and non-transferable.
- **INV-5 — Host enforcement:** W14 checks grant and ACK binding server-side before any side effect; no trusted caller Boolean or client-generated WorkContext.
- **INV-6 — Durable authoritative records:** task, assignment, ACK, grant, run and evidence references survive restart; history is append-only and queryable by immutable ID.
- **INV-7 — Idempotency and ordering:** duplicate dispatch/commands cannot create duplicate side effects; event sequence compare-and-append prevents stale or out-of-order transitions.
- **INV-8 — Containment:** process-tree containment is established before untrusted execution; OS isolation, quotas, timeout, cancellation and cleanup are independently evidenced.
- **INV-9 — Fail closed:** unknown identity, missing ACK, wrong scope, stale source, expired/revoked grant, unavailable Core, unavailable Host, unsupported capability, missing evidence or event-integrity failure blocks execution.
- **INV-10 — No legacy bypass:** historical quarantined Runtime MCP :8020 is DO NOT USE. No probe, restart, activation, modification or traffic to that listener.

## 6. Required interface capabilities

### Core authority interface
The exact transport and route names are implementation decisions. The interface must support:
- authenticate/enroll/resolve/revoke Agent and service principals;
- evaluate Work/Gate policy;
- issue, inspect, validate and revoke scoped grants;
- append assignment/ACK/task/run/evidence events atomically with sequence and idempotency checks;
- query authoritative state by immutable IDs and event cursor.

### W52 orchestration interface
The contract must support:
- create/assign/dispatch with idempotency and correlation;
- receive and authenticate recipient ACK/NACK;
- stream ordered events with cursor/resume;
- retry, cancel, timeout, dead-letter/recovery and duplicate suppression;
- negotiate capabilities and report unsupported actions without fallback to arbitrary execution.

Durable outbox/queue ownership and retry boundaries must be explicitly implemented and tested; in-memory/session-only delivery is insufficient for production lifecycle claims.

### W14 HostPort interface
The W14 adapter must support the required bidirectional request/notify/receive/respond/close semantics, or a documented capability profile that accurately limits W52. It must include cancellation and prove that stop/close returns only after all descendant processes are confirmed exited. A one-shot POST /execute alone does not satisfy the full HostPort contract.

## 7. Mandatory gates before real Agent-to-Computer E2E

- **G0 — Source provenance:** exact canonical Core and W14 repositories, branches, HEAD SHAs, file hashes, release mapping and deployed build/process identities reconciled.
- **G1 — Identity:** one non-production Agent principal enrolled with protected credential, attestation/runtime identity, capability declaration and revocation test.
- **G2 — W52 dispatch/ACK:** authenticated dispatch and recipient ACK/NACK, durable outbox, idempotency, event cursor and recovery tests.
- **G3 — Core authority:** scoped grant issue/validate/revoke, Gate check, append-only ledger and restart persistence tests.
- **G4 — W14 Host:** grant validation before side effect, recipient/task binding, process containment-before-spawn, OS isolation, resource limits, timeout/cancel and correlated run record.
- **G5 — Provider:** provider contract, capability negotiation and read-only harmless Computer test behind W14; W10 remains locked and unchanged.
- **G6 — Projection:** W092 renders actual source events with timestamps, actor, IDs, reason, evidence references and stale/disconnected/unknown states.
- **G7 — Independent E2E and negative/recovery:** QE independently observes a real non-production Agent lifecycle and verifies evidence from Core→W52→W14→provider→event ledger→W092.

Required negative/recovery cases include unknown/revoked Agent, bad credential, missing or forged ACK, duplicate dispatch, replay, wrong Work/task/assignment/action/provider/source, expired/revoked grant, Core/Host unavailable, PC offline if PC transport is used, provider crash, descendant process, restart/recovery, event gap, cancellation, timeout and idempotent retry.

A task reaching SUCCEEDED is not a Work acceptance PASS. Acceptance requires complete traceability, independent QE evidence and the applicable Work Gate.

## 8. Explicit non-claims and release boundary

### 8.1 Existing Core V1.2 candidate — reuse evidence, not canonical implementation
A read-only GitHub source reconciliation on 2026-11-23 found:
- Current `main` HEAD `0902cd26518673aa078bb4c7c7899e1e4a95656a` contains `CORE_EXECUTION_AUTHORITY_V1_2_DEPLOYMENT.md` (blob `ce130f1f9a95daeaafff75ef37eacd4dffc797e2`) describing five execution-grant routes.
- The same `main` source has `room_hop_mcp/core_http_main.py` blob `8dd6bb5ea500026d932ca52eb6079c980d722ab0`, whose `build_app()` returns `create_http_app(service)`; its `room_hop_mcp/adapter/http_server.py` blob `54cb3ecbce2e6b13083f31c14f0c1f0738f1457d` does not mount the execution-authority router. Main does not contain `core/execution_authority.py` or `room_hop_mcp/adapter/execution_authority_http.py` at the inspected paths. This is a static source finding; no endpoint was called.
- PR #48 / branch `work/w1111-core-execution-authority-v1-2` contains reusable candidate modules (Core authority blob `163b126178b67c6e0a3f68ba33eaf7b9e6d91503`, HTTP adapter blob `48e05c0f5d8121e35ba9bea01ebd8f338529073c`) and historical CI claims. PR remains OPEN/DRAFT/NOT MERGED, has no submitted reviews or inline review threads in the inspected GitHub response, and the branch comparison against current main is DIVERGED (157 ahead / 986 behind at this inspection).
- A source-level defect is present in candidate `ExecutionAuthority.record_run()`: it validates that submitted `source_sha256` is well-formed but does not compare it with the immutable source SHA bound to the issued grant/work policy. The candidate test explicitly submits `b`×64 when the policy is `a`×64 and expects HTTP 200. This contradicts exact-source binding and is a release blocker.
- PR #48 also bundles W12/W13 host code and historical deployment assumptions. Because W14 is now the sole consolidated Host owner, the PR must not be merged wholesale or treated as W14 canonical source. Any reusable Core module must be selectively reconciled, fixed, re-tested on a fresh current-main branch and reviewed; no parallel Core may be created.

Disposition: Core V1.2 is a reusable but defective, unmerged candidate — NOT current-main implementation, NOT deployed proof, NOT release-approved. The current Core source and candidate are separate provenance objects.


- This V1.3 contract is an architecture baseline only. It does not prove implementation, deployment, service health, Agent enrollment, ACK, HostPort compatibility, browser/Computer execution or E2E.
- Existing Core identity/meeting components are not presumed to implement execution grants or an authoritative task ledger.
- Existing W14/W13 endpoints or historical attestations are not presumed to be the current canonical deployed Host until source/release provenance is reconciled.
- W52 A2A v0.1 remains a draft until upgraded, implemented, independently reviewed and tested against this contract.
- W10 remains LOCKED / NO CHANGE. No direct W10 API invocation is authorized by this document.
- No PR merge, main-branch change, endpoint activation, service deployment, production routing or release is authorized by this contract.
- W28 remains ACTIVE / INTEGRATION BLOCKED / NOT RELEASED until its own release gates are independently satisfied.
- W092 remains PARTIAL / NOT ACCEPTED until a real Agent identity, authenticated ACK, real runtime trace and independent verification are evidenced.

## 9. Supersession and change control

This V1.3 supersedes the V1.2 wording that identified W13/W12 as the sole active Execution Host and assigned an undifferentiated task-lifecycle authority to Core. W13/W12 are historical/internal foundations absorbed by W14. Core authority and durable state, W52 orchestration semantics, and W70 Work lifecycle are separate but correlated responsibilities.

Any implementation must reconcile against this contract and the current canonical source SHAs. Changes to authority ownership, Host boundary, W10 lock, or security invariants require a new recorded architecture decision.
