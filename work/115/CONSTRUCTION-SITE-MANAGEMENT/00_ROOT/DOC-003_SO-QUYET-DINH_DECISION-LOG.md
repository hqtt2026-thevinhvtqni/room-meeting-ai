# SỔ QUYẾT ĐỊNH WORK 115 / WORK DECISION LOG
- **STT / Document ID:** DOC-003
- **Priority:** P0
- **Read order:** 3
- **Depends on:** DOC-001
- **Status:** ACTIVE
- **Version / Updated:** 0.2 / 2026-11-12
- **Authority:** Vinh

| Decision ID | Date | Decision / status | Rationale / boundary | Authority |
|---|---|---|---|---|
| D115-001 | 2026-11-12 | Initialize a new Work for the construction-site web app; use Work 70 Standard 1.2 as governing template. | User explicitly requested a new Work, Git synchronization and execution journaling. Product is for the user's uncle; field workers report from construction sites to a manager's web dashboard. | Vinh |
| D115-002 | 2026-11-12 | Keep initial phase at 01_DISCOVER; do not start product BUILD. | User-facing workflows, business context, acceptance, data/security and hosting needs are not yet sufficiently defined. | Xu within delegated routine scope; owner retains final authority |
| D115-003 | 2026-11-12 | GitHub main is the canonical Work documentation location for this initial scaffold; product source repository remains unassigned. | Avoid conflating Work governance repository with future product source repository. | Xu within delegated routine scope |
| D115-004 | 2026-11-12 | Initial Sandbox creation/parity was BLOCKED while ROOM-HOP 8030 was unavailable. | Historical decision at initial GitHub scaffold; superseded by D115-005 after successful 8030 recovery. | Xu |\n| D115-005 | 2026-11-12 | Adopt the current Work 70 baseline Standard 1.3 and DOC-096; create Sandbox Work 115 only after inventory collision check. | W70 DOC-001 v1.5 identifies Standard 1.3 and DOC-096 as mandatory AI session/journal control. Sandbox inventory returned 63 Works and no Work ID 115; creation was authorized for registered identity `xu`. | Xu within delegated routine scope |

| D115-006 | 2026-11-12 | Conditionally adopt a Rule-first, AI-assisted architecture principle for evaluation: deterministic application rules and database state remain authoritative; optional Student assistance and exceptional Teacher escalation may be assessed later; human approval controls consequential outcomes. | Design baseline only, not final product scope or technology approval. W115 remains focused on field reporting and project management. QS/estimating is excluded from current MVP. No model/provider/version, fine-tuning, GPU rental, paid API, real-data training or BUILD is authorized. Apply privacy, project isolation, provenance, audit, uncertainty/abstention, fallback and cost controls before any implementation. | Xu within delegated reversible design scope; Vinh retains final product approval |
| D115-007 | 2026-11-12 | Set the primary business workflow as site foreman (quản công) reporting construction progress to the contractor (nhà thầu); allow optional, explicitly granted project-scoped investor (chủ đầu tư) access as an extension. | User-confirmed business direction. Foreman is the primary reporting actor and contractor the primary recipient. Investor access is optional, read-only by default and limited to explicitly shared project information. Direct worker reporting, detailed review authority, report cadence and exact field visibility remain open discovery items. No BUILD authorization. | Vinh — confirmed product direction; detailed permissions remain subject to discovery |

| D115-008 | 2026-11-12 | Add construction-material operations to discovery and add a project-scoped Storekeeper role to record material receipts. | User-confirmed direction: the foreman needs construction-material workflows and a storekeeper is added for warehouse receipt entry. Material requests, issues, approvals, adjustments, multi-warehouse behavior and investor visibility remain discovery items. Scope is operational stock movement only; no full ERP/procurement/accounting approval and no BUILD authorization. | Vinh — confirmed role/scope direction; detailed workflows remain subject to discovery |
