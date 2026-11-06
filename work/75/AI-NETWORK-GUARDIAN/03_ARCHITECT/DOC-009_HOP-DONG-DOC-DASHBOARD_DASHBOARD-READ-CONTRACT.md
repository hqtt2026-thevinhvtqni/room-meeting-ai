# DOC-009 — Hợp đồng dữ liệu Dashboard / Dashboard Read Contract

## Purpose
PC and Mobile clients render a shared, versioned backend contract. UI must not invent network state.

## Required fields
- schema_version
- generated_at
- source_mode: live | snapshot | demo
- freshness: FRESH | STALE | UNKNOWN
- system_status
- router: identity, vendor/model (if known), reachability, last_seen, source
- devices: device_id, ip, mac (where permitted), hostname, status, last_seen, source
- incidents: id, type, severity, status, observed_at, evidence_refs
- ai_insights: summary, evidence_refs, confidence, recommended_checks, generated_at
- audit: event_id, actor, action, timestamp, result

## Rendering rules
- Unknown values render as UNKNOWN, never as healthy/zero.
- Snapshot/demo data must be visibly labelled and must not be presented as live monitoring.
- Stale data displays its last observation time.
- AI insight without evidence references is not a verified incident finding.
- Clients cannot infer router reachability from API availability.

## Security
No router secrets, passwords, tokens or raw credential material in client payloads or logs. Apply role-based field filtering and audit all privileged reads/actions.
