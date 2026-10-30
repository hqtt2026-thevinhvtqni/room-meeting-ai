# WORK MANIFEST — WORK 70
- **STT / Document ID:** DOC-001
- **Priority:** P0
- **Read order:** 1
- **Depends on:** NONE
- **Status:** ACTIVE
- **Version / Updated:** 1.4 / 2026-10-30
- Work ID: 70
- Work Name: ROOM-HOP-PRODUCT-LIFECYCLE-AND-WORK-DASHBOARD
- Product: ROOM-HOP Work Master Standard & Per-Work Dashboard
- Standard version: 1.2
- Work status: ACTIVE / DESIGN BASELINE
- Created: 2026-10-30
- Product Owner / Final Authority: Vinh
- Lifecycle Orchestrator: Xu (AI-01)
- Sandbox: Work 70 via MCP 8030
- GitHub repository: hqtt2026-thevinhvtqni/room-meeting-ai
- Build branch: work/70/05-build (scope: 05_BUILD mapping/execution subtree only; not a canonical source repository)
- Canonical product/source repositories: must be declared per Work and artifact in this Manifest or its controlled register; do not infer from the presence of a folder.
- Scope: reusable Work lifecycle, WP model, evidence/gates, dashboard reference, storage/export design and future migration standard.

## Canonical top-level directory set
00_ROOT, 01_DISCOVER, 02_DEFINE, 03_ARCHITECT, 04_PLAN, 05_BUILD, 06_VERIFY, 06_EVIDENCE, 07_ACCEPT, 08_RELEASE, 09_OPERATE, DASHBOARD.

## 05_BUILD role
05_BUILD is a mapping and engineering coordination layer, not the canonical home of original Work documents or product source files. It may contain mapping registers, execution pointers, temporary working copies, build/test coordination metadata and links to canonical artifacts. Each mapping must identify the canonical path/URI and exact version/commit. A file physically present in 05_BUILD is not automatically an original or authoritative source.

## Canonical ownership
- Work governance and official records belong to the relevant lifecycle folders at the Work root.
- Biên bản (minutes/decisions): 00_ROOT and the relevant phase decision record.
- Kế hoạch (plan): 04_PLAN.
- Bản vẽ/mô hình sản phẩm (design/model): 03_ARCHITECT.
- Nhật ký thi công (execution log): 00_ROOT as the Work-wide chronological record; technical detail may be linked from 05_BUILD.
- Product source code and tests belong to the canonical source repository/path explicitly declared for that Work; 05_BUILD only maps to them.
- Cross-phase verified evidence belongs to top-level 06_EVIDENCE. 05_BUILD/06_EVIDENCE may stage temporary build evidence before it is registered canonically.
- Acceptance, release and operations records belong to 07_ACCEPT, 08_RELEASE and 09_OPERATE respectively.

## Canonical 05_BUILD child directory set
00_ROOT, 01_ORIGINAL, 02_EXTENSION, 03_ARCHITECTURE, 04_CODE, 05_TEST, 06_EVIDENCE, 07_RELEASE, 10_AI_DEBUG_HANDOFF.
These are navigation/mapping/execution areas, not independent canonical source roots.

## Authority and invariants
1. Vinh is Product Owner and final authority.
2. Xu coordinates end-to-end work and makes routine decisions within approved scope.
3. Core is the intended authoritative system for identity, authorization, lifecycle state and canonical evidence metadata.
4. Dashboard is read-only.
5. Work Packages are planned/owned at Work level; 05_BUILD may map each WP to engineering areas and source artifacts.
6. Top-level 06_EVIDENCE is the cross-phase evidence index; 05_BUILD/06_EVIDENCE is build-specific staging only.
7. No evidence, no PASS. Unknown is not PASS. File creation is not product verification.
8. No migration of other Works is included in this Work's current scope.
9. No file in 05_BUILD becomes canonical merely by being copied, committed or referenced there.
10. Never delete or silently move legacy files during the transition; classify, map, verify and obtain approval where canonical ownership changes.

## Current truth
- Current lifecycle phase pointer: 01_DISCOVER (PLANNED; G0/G1 NOT_READY; phase not formally started). This supersedes the prior 03_ARCHITECT pointer because predecessor gates are unresolved.
- Core integration: NOT VERIFIED.
- Dashboard: local snapshot prototype; browser E2E NOT VERIFIED.
- 05_BUILD normalization: ACTIVE / MIGRATION NOT VERIFIED; legacy candidates are classified but no source files have been moved or deleted.
- Storage/export: DESIGN ONLY; no backend implementation verified.
- Independent QE: PENDING.
- Acceptance: PENDING.
- Release: NOT RELEASED.

## Document numbering, naming and reading priority
- 00_ROOT/DOC-055_SO-DANG-KY-TAI-LIEU_WORK-70-DOCUMENT-REGISTER.md is the single canonical catalogue for all Work documents. DOCUMENT_REGISTER.md is a temporary compatibility pointer only.
- Every document has a stable STT/Document ID, priority P0-P3 and read order.
- New and updated documents follow DOC-038 and DOC-056: Vietnamese first, English second, ASCII filename, stable DOC ID, one canonical path; no new legacy-style names.
- Official record classification and issuance follow DOC-039 and DOC-040; operational codes are separate from DOC-ID.
- Sandbox relative paths start at ROOM-HOP-PRODUCT-LIFECYCLE-AND-WORK-DASHBOARD/; the repository prefix is not included in Sandbox paths.
- All controlled documents must use DOC-NNN-prefixed canonical filenames. Legacy filenames remain only as temporary aliases during the batch migration defined by DOC-056.
- AI must follow the register's reading sequence and dependencies.

- DOC-055 is the sole document register; DOC-040 is the separate operational document-code register. DOC-056 governs migration and exceptions.

## Mandatory AI operating standard
- All AI participants must follow 00_ROOT/DOC-002_TIEU-CHUAN-TIEP-NHAN-DU-AN_AI-PROJECT-INTAKE-STANDARD.md v1.0 and 00_ROOT/DOC-033_TIEU-CHUAN-TAI-LIEU-VA-LUU-TRU_WORK-DOCUMENTATION-AND-STORAGE-STANDARD.md v1.0 before material changes.
- Use 00_ROOT/PROJECT_INTAKE_REPORT_TEMPLATE.md for a consistent intake report.
- Work-specific instructions may add constraints but may not weaken the shared evidence, authority, storage and status rules.
