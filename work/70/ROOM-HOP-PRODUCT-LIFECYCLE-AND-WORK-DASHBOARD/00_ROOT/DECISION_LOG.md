# WORK 70 — DECISION LOG

Date: 2026-10-30
Maintainer: Xu / AI-01
Final authority: Vinh

| Decision ID | Decision | Rationale | Status |
|---|---|---|---|
| D70-001 | Canonical top-level structure is 00_ROOT, 01_DISCOVER, 02_DEFINE, 03_ARCHITECT, 04_PLAN, 05_BUILD, 06_VERIFY, 06_EVIDENCE, 07_ACCEPT, 08_RELEASE, 09_OPERATE and DASHBOARD. | Separates the nine lifecycle phases from cross-phase evidence and the Dashboard. | ACTIVE STANDARD v1.1 |
| D70-002 | 05_BUILD has exactly nine fixed child folders: 00_ROOT, 01_ORIGINAL, 02_EXTENSION, 03_ARCHITECTURE, 04_CODE, 05_TEST, 06_EVIDENCE, 07_RELEASE and 10_AI_DEBUG_HANDOFF. | Preserves the engineering workspace structure explicitly requested for Work 70. | ACTIVE STANDARD v1.1 |
| D70-003 | WPs are machine-readable records in BUILD_REGISTER.json; Markdown is the human-readable mirror. | Enables schema validation without introducing one folder tree per WP. | ACTIVE STANDARD v1.0 |
| D70-004 | Top-level 06_EVIDENCE is the cross-phase index; 05_BUILD/06_EVIDENCE is build evidence staging. | Prevents mixing all lifecycle evidence with implementation-only artifacts. | ACTIVE STANDARD v1.0 |
| D70-005 | Core is authoritative; Dashboard is read-only; local PRODUCT_STATUS.json is a snapshot. | Prevents a second source of truth and false live claims. | ACTIVE STANDARD |
| D70-006 | Existing Meeting.save_artifact is not reused as generic Work storage/export. | The inspected method is Meeting-scoped and tied to Meeting completion; the HTTP router exposes Meeting routes only. | DECIDED — GAP DOCUMENTED |
| D70-007 | Storage/export initial design targets JSON, CSV and Markdown metadata/indexes; PDF/ZIP deferred. | Keeps first implementation bounded and testable. | DESIGN ONLY |
| D70-008 | GitHub main stores Work 70 lifecycle/root/Dashboard; work/70/05-build stores only the 05_BUILD subtree. | Keeps the branch scope explicit and avoids duplicating the whole Work as a child branch. | ACTIVE SYNC CONTRACT |

Changes to product scope, authority, security policy, material cost or release require Vinh's decision. Routine structural and implementation decisions remain with Xu within approved scope.

| D70-009 | Adopt a common AI Project Intake & Execution Standard and one intake report template for all AI participants. | Prevents inconsistent project discovery, evidence handling, status reporting and handoffs across AI models. | ACTIVE STANDARD v1.0 — adopted by Vinh on 2026-10-30 |
| D70-010 | Every Work document must have a stable STT/Document ID, priority P0-P3 and explicit reading order/dependencies in DOCUMENT_REGISTER.md. | Makes document discovery deterministic and prevents each AI from choosing a different reading sequence. | ACTIVE STANDARD v1.0 — adopted by Vinh on 2026-10-30 |
