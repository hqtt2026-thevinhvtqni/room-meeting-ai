# WORK INSTANTIATION & MIGRATION STANDARD — V1.2
- **STT / Document ID:** DOC-012
- **Priority:** P1
- **Read order:** 13
- **Depends on:** DOC-003; DOC-009; DOC-033
- **Status:** ACTIVE
- **Version / Updated:** 1.2 / 2026-10-30

## A. Create a new Work
1. Allocate a unique Work ID through the authorized Work Registry.
2. Instantiate exactly the canonical top-level structure from the Work Manifest.
3. Instantiate the nine fixed 05_BUILD child directories exactly; these are mapping/engineering coordination areas, not source roots.
4. Set product name, owner, authority, scope, standard version and canonical source repository/path.
5. Create the Work Manifest, Document Register and the four coordinated records: Biên bản, Kế hoạch, Nhật ký thi công, and Bản vẽ/Mô hình when needed. Use the canonical paths defined by the Work's documentation/storage standard; do not create duplicate records.
6. Define lifecycle gates, risks, dependencies and measurable acceptance criteria.
7. Record the canonical Work Package plan in 04_PLAN. The 05_BUILD mapping register links each WP to build areas, canonical source files, exact versions and evidence references. Do not treat a 05_BUILD Build Register copy as the authoritative plan.
8. Store cross-phase evidence references in top-level 06_EVIDENCE. 05_BUILD/06_EVIDENCE may stage temporary build evidence before canonical registration.
9. Confirm permissions, evidence paths, source ownership and auditability before execution.
10. Verify GitHub/Sandbox synchronization for every governed write; write success alone is not PASS.

## B. Migrate an existing Work
Inventory → backup/checksum → source mapping → target mapping → duplicate/conflict analysis → dry run → independent review → owner approval → controlled migration → reconciliation → verification → rollback window → closeout.

Preserve IDs, commits, records, timestamps, decisions, evidence and links. Do not delete source data until reconciliation and retention approval are complete.

## C. Prohibited shortcuts
- No extra top-level directories or unapproved 05_BUILD children.
- No per-WP folder trees that duplicate the fixed build workspace.
- No bulk migration based only on folder names.
- No overwrite of unknown files.
- No silent renumbering or ID changes.
- No fabricated historical status/evidence.
- No release/PASS based on successful file creation alone.
- No canonical original or source file stored only in 05_BUILD.
- No self-created standalone documents that duplicate an existing official record.
