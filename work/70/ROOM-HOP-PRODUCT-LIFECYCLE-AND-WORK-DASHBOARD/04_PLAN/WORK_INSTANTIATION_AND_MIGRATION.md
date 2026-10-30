# WORK INSTANTIATION & MIGRATION STANDARD — V1.1

## A. Create a new Work
1. Allocate a unique Work ID through the authorized Work Registry.
2. Instantiate exactly the canonical top-level structure from 00_ROOT/WORK_MANIFEST.md.
3. Instantiate the nine fixed 05_BUILD child directories exactly; do not invent additional nested templates.
4. Set product name, owner, authority, scope, standard version and source references.
5. Create the manifest and an explicitly labelled SAMPLE or LOCAL SNAPSHOT dashboard payload.
6. Define lifecycle gates, risks, dependencies and success metrics.
7. Record WPs in 05_BUILD/00_ROOT/BUILD_REGISTER.md and validate against WORK_PACKAGE.schema.json.
8. Store cross-phase evidence references in top-level 06_EVIDENCE; build evidence may be staged in 05_BUILD/06_EVIDENCE.
9. Confirm permissions, evidence paths and auditability before execution.

## B. Migrate an existing Work
inventory → backup/checksum → source mapping → target mapping → duplicate/conflict analysis → dry run → owner approval → migration → reconciliation → verification → rollback window → closeout.
Preserve IDs, commits, records, timestamps, decisions, evidence and links. Do not delete source data until reconciliation and retention approval are complete.

## C. Prohibited shortcuts
- No extra top-level directories or unapproved 05_BUILD children.
- No per-WP folder trees that duplicate the fixed build workspace.
- No bulk migration based only on folder names.
- No overwrite of unknown files.
- No silent renumbering or ID changes.
- No fabricated historical status/evidence.
- No release/PASS based on successful file creation alone.
