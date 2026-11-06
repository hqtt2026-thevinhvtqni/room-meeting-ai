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
