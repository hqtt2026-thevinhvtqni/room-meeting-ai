# WORK 70 — DECISION LOG

Date: 2026-10-30
Maintainer: Xu / AI-01
Final authority: Vinh

| Decision ID | Decision | Rationale | Status |
|---|---|---|---|
| D70-001 | Canonical top-level structure is 00_ROOT, 01_DISCOVER, 02_DEFINE, 03_ARCHITECT, 04_PLAN, 05_BUILD, 06_VERIFY, 06_EVIDENCE, 07_ACCEPT, 08_RELEASE, 09_OPERATE and DASHBOARD. | Separates lifecycle phases from cross-phase evidence and Dashboard. | ACTIVE STANDARD v1.1 |
| D70-002 | 05_BUILD has nine fixed child folders: 00_ROOT, 01_ORIGINAL, 02_EXTENSION, 03_ARCHITECTURE, 04_CODE, 05_TEST, 06_EVIDENCE, 07_RELEASE and 10_AI_DEBUG_HANDOFF. | Preserves the approved engineering navigation layout. | ACTIVE STANDARD v1.1 |
| D70-003 | Work Package records are planned at Work level; 05_BUILD maps WPs to engineering areas and source artifacts. | Keeps planning authority outside the build mapping layer. | ACTIVE STANDARD v1.2 |
| D70-004 | Top-level 06_EVIDENCE is the cross-phase canonical evidence index; 05_BUILD/06_EVIDENCE is staging only. | Prevents duplicate evidence authority. | ACTIVE STANDARD v1.2 |
| D70-005 | Core is authoritative; Dashboard is read-only; local PRODUCT_STATUS.json is a snapshot. | Prevents a second source of truth and false live claims. | ACTIVE STANDARD |
| D70-006 | Existing Meeting.save_artifact is not reused as generic Work storage/export. | The inspected method is Meeting-scoped and tied to Meeting completion; reviewed HTTP router exposes Meeting routes only. | DECIDED — GAP DOCUMENTED |
| D70-007 | Storage/export initial design targets JSON, CSV and Markdown metadata/indexes; PDF/ZIP deferred. | Keeps first implementation bounded and testable. | DESIGN ONLY |
| D70-008 | GitHub main stores Work 70 lifecycle/root/Dashboard; work/70/05-build stores only the 05_BUILD subtree. | Keeps branch scope explicit and avoids duplicating the whole Work. | ACTIVE SYNC CONTRACT |
| D70-009 | Adopt a common AI Project Intake & Execution Standard and one intake report template for all AI participants. | Prevents inconsistent project discovery, evidence handling, status reporting and handoffs. | ACTIVE STANDARD v1.0 — adopted by Vinh on 2026-10-30 |
| D70-010 | Every Work document has stable STT/Document ID, priority P0-P3 and explicit reading order/dependencies in DOCUMENT_REGISTER.md. | Makes document discovery deterministic. | ACTIVE STANDARD v1.0 — adopted by Vinh on 2026-10-30 |
| D70-011 | Every Work uses four coordinated records: BIÊN BẢN, KẾ HOẠCH, BẢN VẼ/MÔ HÌNH when needed, and NHẬT KÝ THI CÔNG. | Creates one shared operating record set and prevents AI-specific documentation patterns. | ACTIVE STANDARD v1.0 — adopted by Vinh on 2026-10-30 |
| D70-012 | Work root owns canonical Work records and approved originals; 05_BUILD is a mapping/engineering coordination layer and does not own canonical originals or product source. | Eliminates duplicate authority and confusion between the Work lifecycle tree and build subtree. | ACTIVE STANDARD v1.0 — adopted by Vinh on 2026-10-30 |
| D70-013 | Each mapped artifact must identify its canonical source path/URI and exact version/commit; 05_BUILD copies are temporary and non-canonical. | Prevents stale or ambiguous references and accidental promotion of working copies. | ACTIVE STANDARD v1.0 — adopted by Vinh on 2026-10-30 |
| D70-014 | All Work documents use Vietnamese-first bilingual titles and the canonical DOC-NNN_VIETNAMESE_ENGLISH filename pattern; stable DOC IDs, ASCII filenames and controlled legacy renames are mandatory. | Makes documents readable to Vietnamese users and consistently discoverable by AI/tools without breaking existing links. | ACTIVE STANDARD v1.0 — adopted 2026-10-30 |
| D70-015 | Official records use a controlled document-type code (BB, QD, LENH, PL, KH, YC, TK, QT, HD, BC, BM, HS, TB, CV) separate from the stable DOC-ID; issue codes follow TYPE-WORKID-YYYYMMDD-NNN and are recorded in a register. | Separates document identity from operational classification and prevents ambiguous or duplicate official records. | ACTIVE STANDARD v1.0 — adopted 2026-10-30 |

Material changes to product scope, authority, security policy, recurring cost, canonical schema or release require Vinh's decision. Routine reversible implementation decisions remain with Xu within approved scope.
