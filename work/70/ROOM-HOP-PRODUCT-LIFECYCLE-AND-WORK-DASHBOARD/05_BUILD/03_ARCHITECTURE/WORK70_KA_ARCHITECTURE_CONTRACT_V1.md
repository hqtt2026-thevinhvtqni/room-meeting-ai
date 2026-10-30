# WORK 70 — WP70-KA — ARCHITECTURE RUNTIME & CONTRACT V1

Date: 2026-10-31
Owner: Ka / AI-02
Role: CSA / Architecture & Independent Review
Status: DRAFT — SOURCE RECONCILIATION OPEN; NOT APPROVED FOR IMPLEMENTATION

## 1. Scope
Deliver the architecture contract among Lifecycle Engine, Core Work API, and read-only Dashboard. This document does not authorize changes to Core, Co's Engine implementation, or Vi's Dashboard/Adapter. Canonical state names, routes, permissions, thresholds, and schemas remain governed by existing source documents and owner decisions.

## 2. Runtime boundaries
- Lifecycle Engine: evaluates transition legality against the canonical state machine and guards; it does not grant caller identity or bypass Core authorization.
- Core Work API: authenticated application boundary; authorizes actor, loads authoritative Work state, invokes transition evaluation, commits accepted changes, and exposes read projections.
- Dashboard: read-only consumer of Core projections. It cannot decide authoritative state, write storage, invoke Engine directly, or promote a gate based on UI logic.
- Persistence: authoritative state is accessed only behind the approved service boundary.
- Audit/events: trace committed actions; they are not independent authorization or state authority.

## 3. Command and read paths
Command: Client -> Core API -> authentication/authorization -> load Work + version -> validate idempotency and expected version -> Engine guard evaluation -> persist state and audit -> durable event/outbox -> response.

Read: Dashboard -> authorized Core read API -> Work projection with state, phase/gate distinction, version, timestamps, evidence references, verification and freshness metadata.

Rejected commands must not mutate authoritative state. Dashboard must display unknown/not-verified/stale distinctly and must not optimistically report a committed transition.

## 4. Logical command contract
Request fields:
- work_id: stable Work identifier.
- command_id: idempotency key.
- expected_version: optimistic concurrency precondition.
- target_state: requested destination, constrained by canonical state machine.
- reason: rationale where policy requires it.
- evidence_refs: immutable evidence identifiers required by applicable guards.
- actor identity: derived from authenticated principal, never trusted from caller text.

Accepted result: command_id, work_id, accepted outcome, previous/current state, new version, transition ID, timestamp, audit reference.

Rejected result: rejected outcome, stable reason code, current state/version where safe, and explicit no-mutation semantics.

Candidate reason codes for contract mapping: UNAUTHENTICATED, FORBIDDEN, WORK_NOT_FOUND, INVALID_TRANSITION, GUARD_NOT_SATISFIED, EVIDENCE_REQUIRED, VERSION_CONFLICT, IDEMPOTENCY_CONFLICT, VALIDATION_ERROR. These are proposals, not approved API literals.

## 5. Mandatory invariants
1. Authorization and all transition guards pass before mutation.
2. A rejected command leaves authoritative state and version unchanged.
3. Same command ID and same payload has at most one committed effect; retry returns its recorded outcome.
4. Same command ID with a different payload is rejected.
5. Concurrent commands using one expected version cannot both commit.
6. State and audit commit atomically, or through an explicitly documented recoverable consistency mechanism.
7. Event delivery is assumed at-least-once unless proven otherwise; consumers deduplicate on stable event/transition identity.
8. Dashboard is read-only and cannot bypass Core.
9. Missing evidence, failed reads, or unavailable dependencies remain unknown/not verified, never PASS by default.

## 6. Failure and concurrency behavior
- Invalid edge or failed guard: reject, no mutation.
- Stale expected version: conflict, return current version when safe.
- Duplicate exact request: return original outcome, no duplicate transition.
- Idempotency key reused with changed payload: reject conflict.
- Persistence failure: no accepted result and no partial state/audit write.
- Event transport outage: retain event durably for retry; expose pending delivery where relevant.
- Stale read projection: disclose version/as-of or freshness; do not claim current.
- Unauthorized actor: reject before mutation; security audit follows existing policy.

## 7. Audit/event minimum
Candidate attributes: event_id, transition_id, work_id, command_id, authenticated_actor_id, from_state, to_state, aggregate_version, occurred_at, reason, evidence_refs, correlation_id, schema_version. Audit history is append-only; corrections are additional records.

## 8. Dashboard projection minimum
Candidate fields: work_id, display_name, lifecycle_state, phase, gate_status, aggregate_version, updated_at, last_transition, evidence_summary, verification_status, data_freshness. Lifecycle state, lifecycle gate, integration gate, and verification result must remain separate concepts.

## 9. Independent verification matrix
- LC-01: valid authorized transition -> exactly one committed transition and audit.
- LC-02: illegal edge -> reject; state/version unchanged.
- LC-03: required evidence absent -> reject; state/version unchanged.
- LC-04: unauthorized actor -> reject; no mutation.
- LC-05: same command and payload replay -> same outcome; one effect.
- LC-06: same command ID, changed payload -> idempotency conflict.
- LC-07: concurrent requests on same version -> at most one commit.
- LC-08: persistence failure -> no partial state/audit commit.
- LC-09: event transport unavailable -> durable recoverable event.
- LC-10: Dashboard mutation/bypass attempt -> no supported write path; server denies.
- LC-11: stale projection -> freshness/version disclosed.
- LC-12: missing evidence/dependency -> unknown or not verified, never PASS.

Every test must define fixture, independent oracle, request/response, authoritative before/after state, and reproducible evidence.

## 10. Decisions still requiring reconciliation
- Canonical state labels and allowed edges from the current state machine.
- Gate taxonomy and gate ownership.
- Existing Core route, auth/permission model, transaction/version strategy.
- Synchronous versus asynchronous command semantics.
- Existing event schema, delivery/replay/retention guarantees.
- Evidence reference and immutable storage contract.
- Dashboard projection freshness, pagination, filtering.
- Existing implementations that already satisfy any proposed behavior.

No new lifecycle state, gate, route, permission, threshold, or API schema is approved by this draft. Existing source contracts take precedence.

## 11. Acceptance criteria
- Reconcile this draft against current architecture, state machine, gate matrix, assignment contract, and decision log.
- Record exact source references for each adopted contract.
- Xu and relevant owners confirm ownership boundaries and unresolved decisions.
- API/event names align with actual Core conventions before implementation.
- QE independently verifies rejection, retry, race, audit, and Dashboard read-only behavior.
- Unresolved matters remain OPEN/BLOCKED; this draft is not a PASS.

Prepared by: Ka / AI-02
Title: CSA / Architecture & Independent Review
Signature: [KÝ: KA / AI-02 | CSA / ARCHITECTURE & INDEPENDENT REVIEW]
