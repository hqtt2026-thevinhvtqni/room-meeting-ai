# W05 REAL WORK 001 — DECISION

STATUS: NEED_DECISION / PARTIAL — technical direction selected; production authority unresolved.
OWNER / AGENT: Manus Orchestrator
TIMESTAMP: 2026-10-05T02:40:00+07:00
INPUT: Evidence gate and synthesized proposals.
ACTION: Select bounded implementation decisions without claiming Vinh approval.
DECISIONS:
D1 Core-first; Docs human-readable projection.
D2 Core DB authority + minimal Drive appProperties; no shadow DB.
D3 Hybrid OAuth/service-account model under Core policy; least privilege.
D4 Dedicated Shared Drive preferred; My Drive only explicit exceptions.
D5 Controlled section updates; append-only events; gated full update.
D6 Core per-resource serialization + requiredRevisionId; bounded retries.
D7 changes.list + watch hint + periodic reconciliation.
D8 reject stale ambiguous writes; bounded re-read/re-plan; allow-listed auto-merge only.
VINH_GATE: approve production Core authority, Workspace ownership/Shared Drive, credentials/scopes/domain-wide delegation, human-edit intake, full-update capability, conflict auto-merge allow-list, webhook/freshness SLA, migration, backup/retention, and deployment of real :8020/:8000 services. No Vinh approval was inferred.
EVIDENCE: 04–07 and official Google URLs.
NEXT: Build only the local/mock vertical slice; do not perform external mutations.
