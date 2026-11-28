# W05 REAL WORK 001 — SYNTHESIS

STATUS: PASS — evidence-backed synthesis; production decisions remain gated.
OWNER / AGENT: Manus Orchestrator / reducer
TIMESTAMP: 2026-10-05T02:38:52+07:00
INPUT: 8 independent proposals and prior ROOM-HOP architecture.
ACTION: Resolve common direction and preserve conflicts.
RESULT: The coherent design is Core-first: AI/Runner → MCP :8020 → Core :8000 (single source of truth) → Google Workspace adapter. Core owns workflow intent, metadata, audit, idempotency, revision observations, queue state, sync cursors, and conflict policy. Docs/Drive provide readable collaboration, correlation, and external persistence. Conflicts remain explicit: Core authority versus Google document-body state; human edits versus generated content; section update versus auto-merge; Shared Drive versus per-user cursors; hybrid credentials versus least privilege.
EVIDENCE: 04_RESEARCH.md, 05_PROPOSALS.md, prior W05 evidence file, and official URLs.
NEXT: Record decisions and Vinh gates.
