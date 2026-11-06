# DOC-003 — Sổ quyết định / Decision Log

## DEC-75-001 — Product scope: Mobile + PC + AI
- Date: 2026-11-06
- Decision: Work 75 is a network infrastructure management application for Mobile and PC with AI participation.
- Architecture: one shared backend, data model, authorization model and business logic; two client experiences.
- PC: full administration, topology, device inventory, incidents, audit and configuration views.
- Mobile: monitoring, notifications, incident details and AI-assisted explanation.
- AI: analyze, explain and recommend; human remains the authority for network-impacting actions.
- Status: DECISION RECORDED; implementation pending.

## DEC-75-002 — Local-first and read-only initial release
- Decision: collect network/router data passively; no router configuration writes or autonomous remediation in initial release.
- Reason: protect office network availability and preserve auditability.
- Status: DECISION RECORDED.

## DEC-75-003 — Git layout
- Decision: store Work 75 under work/75/AI-NETWORK-GUARDIAN/ in the existing main repository, following Work 70; no separate Work branch.
- Status: APPLIED to this GitHub baseline.
