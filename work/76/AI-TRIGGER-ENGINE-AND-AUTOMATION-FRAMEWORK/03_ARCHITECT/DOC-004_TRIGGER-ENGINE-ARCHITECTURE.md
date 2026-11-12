# DOC-004 — TRIGGER ENGINE ARCHITECTURE / KIẾN TRÚC HỆ THỐNG

## Design principle
Trigger là một policy-bound event-to-action definition, không phải shell command tùy ý. Tách biệt rõ: Event (sự kiện), Condition (điều kiện), Decision (quyết định), Authorization (quyền), Dispatch (giao việc), Action (hành động) và Evidence (bằng chứng).

## Logical components
1. Trigger Registry: versioned definitions, owner, Work scope, status and policy reference.
2. Event Gateway: authenticated intake, schema validation, signature verification, replay protection and normalization.
3. Scheduler: time-based events, timezone-aware schedules and missed-run policy.
4. Event Bus/Queue: durable delivery, partitioning, back-pressure and dead-letter handling (technology TBD).
5. Condition Evaluator: deterministic typed expression evaluator; no arbitrary code execution.
6. Policy/Authorization Adapter: authoritative principal, role, assignment, scope, gate and approval checks from Core.
7. Trigger Orchestrator: idempotency, cooldown, rate limits, retry budget, state machine and correlation.
8. AI Dispatcher: dispatch only through a verified transport contract; record receipt and ACK separately.
9. Action Executor: allow-listed action handlers with explicit permission and human approval where required.
10. Audit/Evidence Store: immutable or tamper-evident execution record, payload digest and evidence references.
11. Dashboard API/Projection: read-only aggregated view.

## Event processing sequence
Receive → Authenticate Source → Validate Schema → Normalize → Deduplicate → Load Trigger Version → Evaluate Condition → Evaluate Policy → Require Approval if applicable → Enqueue/Dispatch → Await Receipt/ACK → Execute approved action → Persist outcome/evidence → Update read-only projection.

## Trigger lifecycle
DRAFT → VALIDATING → READY → ACTIVE → PAUSED / DISABLED.
Execution lifecycle: RECEIVED → VALIDATED → EVALUATED → SUPPRESSED or AUTHORIZED → QUEUED → DISPATCHED → ACKNOWLEDGED → SUCCEEDED / FAILED / EXPIRED.
Each transition is audited. State transition is not inferred from a dashboard display.

## Trigger definition contract (draft)
- trigger_id, name, description, version
- trigger_type: TIME | EVENT | CONDITION | MANUAL | COMPOSITE
- owner_principal, work_id, wp_id, scope
- source: provider, event_type, authentication_profile, schema_version
- condition: typed expression tree, threshold, window, timezone
- action: allow-listed action_type and parameters schema
- target: AI identity or service identity resolved by trusted registry
- policy_ref, approval_mode, cooldown_seconds, rate_limit
- retry_policy, idempotency_key_template, expires_at
- status, created_at, updated_at, created_by

## Security boundaries
- Event data is untrusted input, never an instruction to change policy.
- No direct execution of arbitrary shell, SQL, Python, PowerShell or dynamic code from a Trigger definition.
- Secrets are referenced by managed secret IDs; never embedded in config or logs.
- Every action is checked at execution time, not only at Trigger creation.
- Kill switch can stop new intake/dispatch and must not erase audit history.
- Fail closed for protected mutations if Core authorization or audit persistence is unavailable.

## Deployment architecture
Initial target: local-first ROOM-HOP service, with adapters to Core and 8030 Build MCP only where contracts and ownership are verified. Do not treat MCP 8030 as a production event bus or scheduler without a separate capacity/security assessment.

## Unresolved architecture decisions
Queue/broker, persistent store, scheduler library, API routes, auth contract, dispatch protocol, retention, SLO and HA topology require discovery and ADR approval. This document is a design baseline, not implementation evidence.


## Co contract proposal — interface baseline (DRAFT / NOT APPROVED)
This appendix is a proposed logical contract to make implementation and independent review deterministic. It does not select a broker, database, scheduler, HTTP route, cryptographic scheme or dispatch transport. Those remain open until authoritative Core/ROOM-HOP contracts are inspected and the relevant architecture owner approves an ADR.

### A. Normalized event envelope
Required logical fields:
- `event_id`: stable source event identifier; uniqueness is scoped by `source_id`.
- `source_id`, `event_type`, `schema_version`: source identity and versioned event contract.
- `occurred_at`, `received_at`: RFC 3339 timestamps with explicit UTC offset; preserve original source timestamp and normalized UTC instant separately.
- `work_id`, `scope`: tenant/work boundary; must be resolved from trusted source registration, not copied blindly from payload.
- `correlation_id`: trace identifier propagated through evaluation, authorization and dispatch.
- `payload`: schema-validated data object; treat every string and nested value as untrusted data.
- `payload_digest`: digest of canonical payload bytes for audit/replay correlation.
- `auth_context_ref`: reference to verified source-authentication result; never store raw secret material in the event.
Validation order: authenticate source → enforce body/size limits → validate schema/version → validate timestamp/replay window → resolve trusted Work scope → canonicalize/digest → deduplicate → persist accepted/rejected audit outcome. Rejection must not dispatch an action.

### B. Typed condition AST
Proposed node families:
- Literal: `{type: "literal", value, value_type}`.
- Field reference: `{type: "field", path}`, where path is an allow-listed schema path, not arbitrary object traversal.
- Comparison: `{type: "compare", op, left, right}`; operators are a fixed allow-list (EQ, NE, LT, LTE, GT, GTE).
- Boolean: `{type: "and"|"or", operands: [...]}` and `{type: "not", operand: ...}`.
- Presence/membership: explicit `exists` and `in` nodes with exact arity and type rules.
- Time window: explicit window node with a named clock basis, duration/bounds and documented inclusive/exclusive semantics.
Validation must reject unknown keys, missing operands, invalid arity, unsupported operators, type mismatches, excessive depth/node count, and non-finite numeric values. Missing is distinct from explicit null. No `eval`, dynamic imports, executable expressions, user-defined functions, shell or SQL fragments. Evaluation returns a typed result plus stable reason code; malformed AST is INVALID, not a false/true match.

### C. Evaluation and policy decision contracts
Condition result is one of `MATCH`, `NO_MATCH`, `INVALID`, `ERROR`; include trigger/version, event/correlation IDs, evaluator version, evaluated timestamp and reason code. Only MATCH may proceed to policy evaluation.
Policy result is one of `ALLOW`, `DENY`, `REQUIRE_APPROVAL`, `INDETERMINATE`; bind it to principal, action type, resource, Work/WP scope, policy revision, decision timestamp and expiry. `DENY`, `REQUIRE_APPROVAL` without approval, `INDETERMINATE`, stale policy, missing identity or unavailable Core authorization must not dispatch. The authoritative Core API and principal schema remain TBD and must not be simulated locally.

### D. Dispatch and acknowledgement contract
A dispatch request must carry `assignment_id`, `correlation_id`, trusted target identity reference, Work/WP scope, allow-listed action reference, idempotency key, expiry and policy-decision reference. Never infer target identity from event payload.
Track `QUEUED`, `SENT`, `RECEIVED`, `ACKNOWLEDGED`, and terminal outcome as separate facts. A local queue write proves QUEUED only; transport acceptance may prove SENT; receiver evidence is required for RECEIVED; explicit receiver acknowledgement is required for ACKNOWLEDGED. Timeout is UNKNOWN/EXPIRED according to policy, never fabricated ACK. Transport, receipt format, ACK authority and retry semantics remain unresolved until verified against the actual dispatch provider.

### E. Audit record minimum
Append-only logical record: audit_id, event_id, trigger_id/version, correlation_id, actor/principal reference, Work/WP scope, transition, prior/new state, condition result, policy decision reference, dispatch/ACK references, timestamp, reason code, payload digest and evidence references. Redact secrets and private conversation content. Protected action must fail closed when the audit persistence dependency is unavailable. Tamper-evidence mechanism and retention are ADR decisions, not assumed implementation details.

### F. State and concurrency invariants
- At most one ACTIVE version per trigger_id; activation of a new version and retirement of the previous active version must be atomic.
- State changes use an expected version/revision (compare-and-swap or equivalent) to prevent lost updates.
- Pause/disable/kill-switch checks occur immediately before enqueue/dispatch and before protected execution; a previously evaluated MATCH is not authorization to bypass a later pause or revoked policy.
- Idempotency key is stable for the same logical trigger-version/event/action attempt; duplicate intake must not create duplicate side effects.
- Replay defaults to dry-run and cannot bypass current authorization, approval, kill switch or audit requirements.

### G. Open ADRs / owner decisions required
1. Core principal, assignment, Work/WP scope and authorization API contracts.
2. Event source registry, signature algorithm/key rotation, timestamp tolerance and replay retention.
3. Canonical serialization/digest algorithm and payload size/depth limits.
4. Durable queue/broker, database and transaction/outbox strategy.
5. Scheduler ownership/library and daylight-saving/missed-run policy.
6. Dispatch provider, target identity resolution, receipt/ACK schema and retry contract.
7. Audit storage, tamper-evidence, retention and privacy policy.
8. SLO, throughput, rate limits, operational ownership and recovery objectives.

Status of this appendix: PROPOSED ONLY. Xu/architecture review and Vinh authority decision are pending. No ADR is approved by this text; no gate is passed and no implementation is authorized.
