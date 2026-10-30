# WORK MANIFEST — WORK 70
- Work ID: 70
- Work Name: ROOM-HOP-PRODUCT-LIFECYCLE-AND-WORK-DASHBOARD
- Product: ROOM-HOP Work Master Standard & Per-Work Dashboard
- Standard version: 1.1
- Work status: ACTIVE / DESIGN BASELINE
- Created: 2026-10-30
- Product Owner / Final Authority: Vinh
- Lifecycle Orchestrator: Xu (AI-01)
- Sandbox: Work 70 via MCP 8030
- GitHub repository: hqtt2026-thevinhvtqni/room-meeting-ai
- Build branch: work/70/05-build (scope: 05_BUILD subtree only)
- Scope: reusable Work lifecycle, WP model, evidence/gates, dashboard reference, storage/export design and future migration standard.

## Canonical top-level directory set
00_ROOT, 01_DISCOVER, 02_DEFINE, 03_ARCHITECT, 04_PLAN, 05_BUILD, 06_VERIFY, 06_EVIDENCE, 07_ACCEPT, 08_RELEASE, 09_OPERATE, DASHBOARD.

## Canonical 05_BUILD child directory set
00_ROOT, 01_ORIGINAL, 02_EXTENSION, 03_ARCHITECTURE, 04_CODE, 05_TEST, 06_EVIDENCE, 07_RELEASE, 10_AI_DEBUG_HANDOFF.

These nine build directories are the approved engineering workspace layout. They are not additional lifecycle phases and must remain nested under 05_BUILD.

## Authority and invariants
1. Vinh is Product Owner and final authority.
2. Xu coordinates end-to-end work and makes routine decisions within approved scope.
3. Core is the intended authoritative system for identity, authorization, lifecycle state and canonical evidence metadata.
4. Dashboard is read-only.
5. Work Packages are records in 05_BUILD/00_ROOT/BUILD_REGISTER.md, validated by WORK_PACKAGE.schema.json; they reference build areas and artifacts.
6. Top-level 06_EVIDENCE is the cross-phase evidence index; 05_BUILD/06_EVIDENCE is build-specific evidence staging.
7. No evidence, no PASS. Unknown is not PASS. File creation is not product verification.
8. No migration of other Works is included in this Work's current scope.

## Current truth
- Current lifecycle phase: 03_ARCHITECT (design baseline; exit gate not passed).
- Core integration: NOT VERIFIED.
- Dashboard: local snapshot prototype; browser E2E NOT VERIFIED.
- Storage/export: DESIGN ONLY; no backend implementation verified.
- Independent QE: PENDING.
- Acceptance: PENDING.
- Release: NOT RELEASED.

## Mandatory AI operating standard
- All AI participants must follow `00_ROOT/AI_PROJECT_INTAKE_STANDARD.md` v1.0 before material changes.
- Use `00_ROOT/PROJECT_INTAKE_REPORT_TEMPLATE.md` for a consistent intake report.
- Work-specific instructions may add constraints but may not weaken the shared evidence, authority and status rules.
