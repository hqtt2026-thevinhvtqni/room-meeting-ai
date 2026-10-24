# Work 104 — AI Usage & Evidence Tracking Architecture (Proposed)

Status: PROPOSED; implementation not yet verified.

## Target flow
AI/provider adapter or supported API hook → ROOM-HOP instrumentation → normalized event envelope → durable usage/evidence ledger → query/report contract → dashboard and audit reports.

MCP :8030 remains the Sandbox/build-zone interface. Core :8000 remains the single source of truth and must never be installed inside Sandbox. Inspect existing paths before selecting an integration point; do not assume all AI clients can or should use one proxy.

## Capture layers
- Provider/API: provider/model, provider request ID, provider-reported token categories, finish status, billing metadata when exposed.
- ROOM/MCP: AI identity, Work/task/room, tool name, redacted arguments metadata, result status, duration, error class, artifact references.
- Verification: test run ID, environment fingerprint, pass/fail/blocked, independent reviewer, evidence URI/hash, commit/artifact reference.
- Cost calculator: provider + model + effective date + token category + pricing source/version; preserve inputs and mark estimates.

## Proposed event envelope
event_id (unique/idempotent), occurred_at, ingested_at, event_type; ai_id, ai_role, provider, model; work_id, task_id, room_id, trace_id, parent_event_id; provider_request_id, tool_name, status, latency_ms; usage_source (provider_reported/gateway_observed/estimated/unavailable); input_tokens, output_tokens, cached_input_tokens, reasoning_tokens, other_usage_json; cost_amount, cost_currency, pricing_version, cost_status (actual/estimated/unavailable); artifact_refs, evidence_refs, content_hash, redaction_status, metadata_json.

Missing values stay null with an explicit status; never fabricate zeroes.

## Storage and reporting
Select persistence after discovery. PostgreSQL is a candidate for normalized operational records; ClickHouse is deferred until measured scale justifies it. Existing ROOM UI or a compatible reporting layer can consume the contract; Grafana is optional. Preserve event-level lineage so aggregates can be recomputed.

## Reliability
Stable idempotency keys; bounded queue/outbox if needed; retry/backoff and dead-letter visibility; instrumentation health and dropped-event metrics; no completeness claim without reconciliation; distinguish billed retries from duplicate logging.

## Security and privacy
Never log keys/tokens/secrets. Redact sensitive tool arguments; default to metadata, hashes and artifact references. Apply role-based access, retention and audit logs. Training/RAG export is a separately reviewed data product.

## Metrics
Usage/cost by AI/provider/model/Work/task/room/date; actual vs estimated vs unavailable; task cycle time; retry/error rate; tool-call success; cost per independently accepted task; evidence coverage/test outcomes; A2A handoff time where timestamps exist. Do not rank performance from token volume alone.

## Integration decision gate
Map agent runtime, provider adapters, API calls, MCP 8030, Core :8000, transcripts, evidence storage, and usage-discard points (including adapters that discard provider usage). Choose the smallest integration point that provides adequate coverage. LiteLLM/custom FastAPI is optional and must be justified by evidence.
