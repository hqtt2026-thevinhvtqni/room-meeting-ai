# Work 104 — Request and Scope

## Request
Create a common system for HQTT/ROOM-HOP to attribute AI work and record which AI acted, Work/task/room, provider/model, input/output tokens, cost, latency, tool calls, errors, outputs, and evidence of completion. Use data for cost control, quality analysis, and governed future optimization.

## Outcomes
- Attribute usage/cost to AI and task where evidence exists.
- Trace AI work across PLAN → BUILD → VERIFY.
- Distinguish provider-reported facts, verified facts, estimates, and missing data.
- Calculate cost per independently accepted task without confusing activity with success.
- Support later prompt/RAG improvements; fine-tuning remains separately gated.

## In scope
Multi-provider instrumentation; identifiers ai_id/provider/model/work_id/task_id/room_id/trace_id/request_id; usage ledger and pricing provenance; latency/retries/errors/tool events/artifact and verification links; access control, redaction, retention, auditability; dashboard-ready metrics and repeatable tests.

## Excluded from initial milestone
Billing/settlement, quotas/chargeback, model training pipeline, production-wide proxy migration, ranking workers by token volume alone, and default storage of private prompt/response content when metadata and hashes suffice.

## Principles
1. Evidence First; Necessary and Sufficient Conditions defined before implementation.
2. Provider-neutral core and replaceable adapters.
3. Do not violate protected Core boundaries without approved design.
4. Usage source must be explicit: provider_reported, gateway_observed, estimated, or unavailable.
5. Logging failures must not silently lose events.
6. Idempotency prevents duplicate records on retry.
7. Never log secrets; minimize sensitive content and store full content only when approved.
