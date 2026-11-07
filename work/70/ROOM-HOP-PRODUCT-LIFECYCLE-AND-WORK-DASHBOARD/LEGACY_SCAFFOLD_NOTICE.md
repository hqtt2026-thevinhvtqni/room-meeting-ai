# LEGACY SCAFFOLD NOTICE — WORK 70
- **STT / Document ID:** DOC-029
- **Priority:** P3
- **Read order:** 36
- **Depends on:** DOC-001
- **Status:** ACTIVE
- **Version / Updated:** 1.0 / 2026-10-30


This notice supersedes earlier scaffold guidance that incorrectly prohibited all nested folders under 05_BUILD.

## Canonical structure
- Legacy top-level structure notice (superseded for evidence path by DOC-001 v1.5): 00_ROOT, 01_DISCOVER, 02_DEFINE, 03_ARCHITECT, 04_PLAN, 05_BUILD, 06_VERIFY, EVIDENCE, 07_ACCEPT, 08_RELEASE, 09_OPERATE and DASHBOARD.
- 05_BUILD has exactly nine approved child folders: 00_ROOT, 01_ORIGINAL, 02_EXTENSION, 03_ARCHITECTURE, 04_CODE, 05_TEST, 06_EVIDENCE, 07_RELEASE and 10_AI_DEBUG_HANDOFF.
- These build folders are fixed work areas, not per-WP trees or a second lifecycle.
- Work Packages are records in 05_BUILD/00_ROOT/BUILD_REGISTER.md and are validated by WORK_PACKAGE.schema.json.

Any earlier assistant-authored proposal to create a different WORK_PACKAGES/TEMPLATE folder hierarchy is superseded and must not be populated. Empty non-canonical directory entries or operating-system metadata files are cleanup items only; do not treat them as product structure. This notice does not claim the filesystem has been fully cleaned.


**2026-11-07 correction:** the canonical top-level cross-phase evidence directory is `EVIDENCE/`. `06_VERIFY/` remains phase verification. `05_BUILD/06_EVIDENCE/` remains a build staging area. The old top-level `06_EVIDENCE/` is not a canonical folder and is retained only for controlled compatibility during migration.
