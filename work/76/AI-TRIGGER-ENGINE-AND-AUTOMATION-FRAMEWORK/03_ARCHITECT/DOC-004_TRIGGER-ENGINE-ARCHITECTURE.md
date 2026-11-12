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


## H. Cross-Work dependency trace — evidence-backed status (DRAFT / NOT APPROVED)

This section records a bounded read-only comparison of W76's proposed interfaces against existing ROOM-HOP records and source findings. It is not an integration approval and does not assert that a searched-but-unseen component is absent from every repository, branch, deployment or runtime.

| W76 dependency | Existing evidence inspected | Verified fact | W76 disposition |
|---|---|---|---|
| Principal / Work authorization | Work 70 DOC-063, DRAFT / DESIGN ONLY / NOT APPROVED / NOT IMPLEMENTED; DOC-061 source-trace findings recorded in W70 journal | DOC-063 defines server-trusted principal, Work/WP/assignment, action/resource scope, source revision, gate snapshot, expiry/revocation and commit-time revalidation. W70 source-trace record says the inspected Core router exposed Identity/Meeting routes; Work/WP authorization and Evidence Registry routes were not found in that inspected router. | Reuse the security requirements as design constraints only. Actual Core API, owner, route, schema and deployed enforcement remain NOT VERIFIED. No local substitute authority. |
| Execution boundary / tool dispatch | W13/W70/W1111 source-trace records; execution_host/server.py, execution_host/host.py, execution_host/wee_bridge.py findings summarized in W1111 DOC-003 | The inspected main /execute path relied on caller-supplied authorized boolean; no server-side principal/assignment/gate authorization was evidenced in that inspected handler. W28 hardened branch is a separate branch and is not proof of main or deployed PC runtime; shared bearer token and static allow-list limitations were also recorded. | W76 must call a verified server-side authorization boundary before protected action. Do not treat MCP 8030, a caller boolean, shared token, or branch-only code as trusted per-principal dispatch. Actual provider and deployed path remain NOT VERIFIED. |
| Event source / intake authentication | GitHub default-branch indexed code searches: event gateway event envelope schema validation replay idempotency in room-meeting-ai | Search returned no matching indexed files. Search coverage is limited to indexed default-branch content and query terms. | No authoritative event-source registry, webhook signature/key rotation, replay store or intake API was located in this bounded search. Mark NOT LOCATED / DISCOVERY OPEN, not globally absent. |
| Durable queue / outbox | GitHub default-branch indexed code search: scheduler queue outbox dispatch acknowledgement AI dispatcher | Search returned no matching indexed files. | Broker/database/outbox and delivery semantics remain TBD; do not select technology or claim durable delivery. |
| Scheduler / time triggers | Same bounded scheduler/queue search; W76 DOC-004 unresolved ADR list | No authoritative scheduler implementation/owner/contract was identified in the inspected results. | Scheduler library, timezone/DST policy, missed-run policy and leader/HA behavior remain OPEN ADR. |
| AI target identity / receipt / ACK | W70 DOC-063 and W76 DOC-004 proposed dispatch contract | W76 design distinguishes QUEUED/SENT/RECEIVED/ACKNOWLEDGED; inspected cross-Work records do not provide an authoritative W76-compatible target identity resolver plus receiver-issued receipt/ACK contract. | No dispatch success may be inferred from enqueue, HTTP acceptance, tool invocation or local log. Require receiver identity and explicit ACK evidence before recording ACKNOWLEDGED. |
| Audit / evidence persistence | W70 DOC-063; W76 DOC-004 proposed audit minimum | W70 design requires provenance, append-only/tamper-evident audit and atomicity or approved reconciliation; no verified W76-compatible Core persistence contract was found in this bounded inspection. | Audit store, atomicity/outbox, retention, privacy and recovery remain OPEN ADR; protected action fails closed if required audit cannot persist. |

### H.1 Required architecture decisions before implementation-ready
1. Xu/Core owner must identify the authoritative Core principal + Work/WP/assignment + policy/gate read API and its owning repository, branch, route, schema, revision and deployed runtime evidence.
2. Vi/Core owner must map the actual protected mutation and execution endpoints, including caller authentication, principal binding, authorization recheck at commit, audit atomicity and failure behavior.
3. Xu must identify the authoritative event-source registry and scheduler/queue ownership, or explicitly record that these are new components requiring separate ADR and approval.
4. Dispatch owner must provide the target identity resolver, transport, receiver receipt and ACK schema, idempotency and retry semantics, and raw evidence for each state transition.
5. Architecture authority must approve storage/outbox, retention/privacy, SLO and operational ownership before selecting infrastructure.

### H.2 Evidence boundary and status
- This is read-only cross-work discovery plus a documentation update. It is not source inspection of every candidate module and not a runtime topology audit.
- Search results with no matches mean NOT LOCATED in the indexed default-branch search, not proof of nonexistence.
- Work 70 DOC-063 remains DRAFT; its contract is a design reference, not an approved API.
- No W76 implementation, test, CI, runtime, PC Bridge, dispatch, independent QE or release evidence is created by this appendix.
- Status: PROPOSED DEPENDENCY MAP / NOT APPROVED / NOT IMPLEMENTED. WE-G4/G5 and G0/G1 remain unchanged.
