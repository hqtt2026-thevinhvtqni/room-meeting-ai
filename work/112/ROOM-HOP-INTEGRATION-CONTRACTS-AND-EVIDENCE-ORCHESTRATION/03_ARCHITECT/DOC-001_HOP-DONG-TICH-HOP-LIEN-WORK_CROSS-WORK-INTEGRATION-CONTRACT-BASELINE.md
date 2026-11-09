# DOC-001 — HỢP ĐỒNG TÍCH HỢP LIÊN WORK / CROSS-WORK INTEGRATION CONTRACT BASELINE

- Document ID: DOC-001
- Work: 112 — ROOM-HOP-INTEGRATION-CONTRACTS-AND-EVIDENCE-ORCHESTRATION
- Version: 1.0
- Status: DRAFT — DESIGN BASELINE; NOT APPROVED FOR RUNTIME ENFORCEMENT
- Owner: Xu / xu
- Authority: Vinh
- Date: 2026-11-09
- Canonical path: 03_ARCHITECT/DOC-001_HOP-DONG-TICH-HOP-LIEN-WORK_CROSS-WORK-INTEGRATION-CONTRACT-BASELINE.md
- Governing source: W70 DOC-095; W70 DOC-056; W70 DOC-093/DOC-094; W112 Integration Charter.

## 1. Purpose and non-duplication rule

Define the minimum contracts by which existing ROOM-HOP Works exchange identity, assignments, lifecycle events, dependencies, artifacts and verification evidence. W112 owns the cross-Work contract definitions and integration verification plan only. It does not become a second lifecycle engine, task register, event bus, evidence store, communication orchestrator, CI engine or runtime.

## 2. Authority and source-of-truth map

| Domain | Authority / source of truth | W112 responsibility |
|---|---|---|
| Work lifecycle, phase, WP, Product Task, gates, decisions | W70 canonical records; Dashboard is read-only projection | Consume stable IDs and publish cross-Work compatibility rules; never override status |
| Agent identity, roster and permission | W0000 governance registry + enforced identity/authorization source | Require identity references and authorization evidence; never invent identity or permission |
| Agent capability / skills | W21 owner records | Require capability reference where assignment depends on it; do not own skills |
| Workflow execution | W16, subject to verified owner contract | Define adapter boundary and lifecycle correlation only |
| CI and test execution | W32 | Correlate run IDs, source revision, result and artifact references |
| Evidence storage / file exchange | W33 | Define evidence metadata and retrieval contract; do not create a competing evidence store |
| AI communication / orchestration | W52 | Define message/receipt correlation; do not duplicate communication runtime |
| Execution host / autonomous E2E | W14 | Consume execution and artifact references; do not own host runtime |
| Core / Gateway / Build MCP | W37/W38/W39 investigation and ownership records; runtime ownership remains NOT VERIFIED until proven | Require source/service owner and verified endpoint contract before integration claims |
| Technical investigation | W1111 | Consume signed findings and reproducible evidence; no duplicate debug lab |

A Work name, Sandbox folder, branch name or directory snapshot alone is not proof of deployable source ownership.

## 3. Three-level task correlation

W70's three-level model remains authoritative for W70 products:
- Tier 1 — Product Task: one aggregate task per product.
- Tier 2 — Phase Task: one task per product per lifecycle phase; exactly one primary/answerable owner, contributors, and a distinct checking role where applicable.
- Tier 3 — Agent Task: executable assignment owned by one accountable role/identity, with ACK, scope, dependencies, deliverable, evidence and next action.

Cross-Work links use stable identifiers (work_id, product_task_id, phase_task_id, agent_task_id). W112 may correlate IDs across Works but must not copy task state into a second authoritative register. For non-W70 Works, use that Work's own approved task model; do not impose W70 identifiers or silently translate statuses.

## 4. Canonical contract set

### 4.1 Work and identity reference
Required fields: work_id, work_revision (commit SHA or immutable version), owner_identity_id, authority_ref, canonical_source_ref. Identity must resolve against the approved identity registry. Unknown or ambiguous identity => DENY/BLOCKED, not fallback identity.

### 4.2 Assignment and receipt
Required fields: assignment_id, work_id, task_id, assignee_identity_id, accountable_role, scope, permission_ref, capability_ref, dependency_refs, issued_at, expires_at (when bounded), assignment_status, ack_ref.
Assignment lifecycle: PROPOSED → DISPATCHED → ACKNOWLEDGED → IN_PROGRESS → SUBMITTED → ACCEPTED or REJECTED; BLOCKED and CANCELLED are explicit terminal/exception paths. Dispatch is not ACK. Artifact delivery is not ACK. ACK must be attributable to the receiving identity and assignment ID.

### 4.3 Event envelope
Every cross-Work event must carry:
- event_id (globally unique), event_type, schema_version
- occurred_at (UTC ISO-8601), recorded_at, actor_identity_id
- work_id, task_id and optional product_task_id / phase_task_id
- correlation_id, causation_id, idempotency_key
- source_revision, producer, payload_ref
- delivery_attempt, trace_ref, and authorization_ref where applicable.

Consumers must be idempotent. Duplicate event_id or idempotency_key must not create duplicate state transitions or evidence records. Ordering is not assumed across producers; causation and aggregate version are used to detect stale/out-of-order events.

### 4.4 Evidence and artifact provenance
Every material result must be traceable to:
- evidence_id, work_id, task_id, event_id / correlation_id
- source repository + branch/ref + commit/blob SHA
- exact artifact path and SHA-256 where a file artifact exists
- method/command, environment, timestamp, exit/result code
- observed output, status, limitation, reviewer identity
- journal reference and acceptance criterion reference.

Evidence state vocabulary: RECORDED (exists, not independently verified), VERIFIED (checks performed and passed within stated scope), REJECTED, MISSING, NOT_RUN, NOT_VERIFIED. RECORDED is never rendered as VERIFIED/PASS. A file's presence or a successful write acknowledgment is not test evidence.

### 4.5 Dependency and state consistency
A dependency is READY only when its required predecessor status and evidence are present in the authoritative owner record. Otherwise use BLOCKED or NOT_VERIFIED with a missing-condition reference. A downstream task cannot become IN_PROGRESS if mandatory dependencies are unresolved unless an explicit, recorded exception exists. W112 reports conflicts; W70 retains lifecycle decision authority.

### 4.6 Error, retry and concurrency
Contract implementations must define timeout, retryable vs non-retryable errors, maximum attempts, backoff, duplicate delivery behavior, lock/lease scope, lease expiry, cancellation, replay and recovery. Retry must reuse the same idempotency key for the same logical operation. Concurrent updates must use aggregate version / compare-and-swap semantics or an equivalent conflict detector. No silent last-write-wins for authoritative status.

## 5. Shared status semantics

- Task status: PLANNED, READY, IN_PROGRESS, BLOCKED, IN_REVIEW, DONE, CANCELLED; NOT_ASSESSED is allowed only for an explicitly unassessed aggregate/projection and must not be mistaken for an executable state.
- Assignment status: PROPOSED, DISPATCHED, ACKNOWLEDGED, IN_PROGRESS, SUBMITTED, ACCEPTED, REJECTED, BLOCKED, CANCELLED.
- Verification status: NOT_RUN, NOT_VERIFIED, RECORDED, PASS, FAIL, BLOCKED.
- Sync status: NOT_MAPPED, NOT_SYNCED, PARTIAL_SYNC, SYNCED, DRIFTED, BLOCKED.
- No implicit status conversion. A status mapping must be explicit, versioned, reversible and documented with loss/ambiguity.

## 6. Integration test levels

S0 ownership and source pin; S1 contract/schema compatibility; S2 component contract tests; S3 end-to-end cross-Work flow; S4 replay, idempotency, concurrency, timeout and recovery; S5 security/negative authorization and independent QE; S6 founder acceptance.

Every test record distinguishes MOCK, SNAPSHOT, SANDBOX and LIVE evidence. A mock or snapshot PASS cannot be promoted to LIVE integration PASS. Every result records exact source SHA, test command/method, raw outcome, artifact, timestamp and reviewer. If no executable integration path is available, status remains NOT_RUN/BLOCKED.

## 7. Compatibility and change control

- Contract changes use semantic versioning: MAJOR for breaking changes, MINOR for backward-compatible additions, PATCH for clarifications/fixes.
- Producers publish schema version and supported consumer range.
- Unknown required fields, unsupported major versions or missing identity/provenance fail closed.
- Deprecation requires an owner, replacement, migration window, consumer inventory and compatibility test.
- W70 approves system-level authority/lifecycle changes; component owners approve their implementation; W112 maintains cross-boundary compatibility findings and test evidence.

## 8. Journal and handoff requirements

Before work: read W70 governing standard, W112 Manifest/Charter/Journal and the target Work's Manifest, decisions, task register and full relevant journal. After work: append timestamp, actor, scope, source revision, method, exact files/commands, result, evidence, limitation and next step. A handoff is complete only when the receiving owner can continue without repeating completed discovery.

## 9. Open design decisions — not silently assumed

1. Canonical event transport and delivery guarantee: NOT DECIDED.
2. Authoritative runtime API for assignment/ACK and state transitions: NOT VERIFIED.
3. Canonical evidence object store and retention policy: NOT VERIFIED.
4. Lock/lease provider and aggregate version enforcement: NOT VERIFIED.
5. Live component endpoint/source ownership for W37/W38/W39: NOT VERIFIED.
6. Cross-Work authentication and authorization enforcement: NOT VERIFIED.

## 10. Acceptance criteria for this design baseline

- Ownership boundaries do not duplicate W70/W32/W33/W52/W16/W14/W37/W38/W39/W0000 responsibilities.
- All contract families above have required fields, lifecycle semantics and failure behavior.
- Task/event/evidence references are correlatable without copying authoritative state.
- Test levels distinguish mock/snapshot/sandbox/live and require source pinning.
- Every unresolved runtime choice is explicitly marked NOT DECIDED / NOT VERIFIED.
- Independent architecture review and Vinh approval are still required before runtime enforcement.

**Current disposition:** DOCUMENT DRAFT WRITTEN; NOT APPROVED; NO RUNTIME IMPLEMENTATION AUTHORIZED; NO INTEGRATION TEST PASS CLAIMED.
