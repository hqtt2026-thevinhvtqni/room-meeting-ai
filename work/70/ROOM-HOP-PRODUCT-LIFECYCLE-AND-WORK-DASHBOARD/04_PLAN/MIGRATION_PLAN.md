# WORK 70 — EXISTING WORK MIGRATION PLAN
# Kế hoạch chuyển đổi các Work hiện hữu
- **STT / Document ID:** DOC-018
- **Priority:** P2
- **Read order:** 23
- **Depends on:** DOC-012; DOC-033; DOC-036
- **Status:** ACTIVE / DESIGN PLAN — NO MIGRATION EXECUTED
- **Version / Updated:** 1.1 / 2026-10-30

## 1. Scope and guardrails
Each existing Work may be standardized into the nine-phase lifecycle and receive its own Dashboard. Work ID, repository history, branch names, issues, artifacts and evidence references must be preserved. This is a controlled migration plan, not permission to modify other Works. Work 70 is the reference design; no other Work is in scope.

## 2. Per-Work migration sequence
1. INVENTORY — list manifest, folders, branches, issues, artifacts, evidence, owner and current status.
2. CLASSIFY — map content to lifecycle phase, canonical source, 05_BUILD mapping area, evidence or legacy history.
3. MAP — record old_path → canonical_path, old_status → proposed_status and evidence_ref → preserved_ref.
4. DRY RUN — generate a mapping report without writing/deleting/moving source data.
5. REVIEW — owner and independent reviewer inspect mapping, links, permissions, duplicate content and conflicts.
6. BACKUP — create a timestamped snapshot with checksums.
7. APPROVE — obtain explicit approval for that Work and the exact migration batch.
8. MIGRATE — apply logged, idempotent operations in controlled batches.
9. VERIFY — reconcile counts, hashes, links, branch/commit/issue references and status.
10. ACCEPT / ROLLBACK — close only after owner acceptance; rollback on defined triggers.

## 3. Work / 05_BUILD ownership rules
- Work root owns canonical Work records, approved plans, drawings/models, acceptance/release records and the cross-phase evidence index.
- Product source code/tests live only in the source repository/path declared by the Work Manifest or controlled artifact register.
- 05_BUILD is a mapping and engineering coordination layer. It may contain mapping registers, WP-to-build-area links, temporary working copies and technical execution pointers.
- A 05_BUILD file is not canonical merely because it exists in the branch or Sandbox.
- Top-level 06_EVIDENCE is the canonical cross-phase index; 05_BUILD/06_EVIDENCE is temporary staging only.
- Unknown destination → MIGRATION_REVIEW_QUEUE; do not guess.
- Preserve historical evidence references and original timestamps/authors.

## 4. Work 70 05_BUILD transition batch
Initial inventory has identified the following classes; this is classification only, not migration approval:
- Build Register Markdown/JSON and schemas: CANONICAL CANDIDATE; WP plan/schema ownership must be reconciled into Work-level plan/architecture.
- Storage & Export Architecture and Core Capability Gap Assessment: CANONICAL CANDIDATE; reconcile into 03_ARCHITECT or another justified Work-level location.
- Storage & Export Acceptance: CANONICAL CANDIDATE; reconcile into 06_VERIFY.
- AI Participants & Token Usage: LEGACY / REFERENCE; audit accuracy and retention need.
- Work 70 Session Log: LEGACY / HISTORICAL; Work-wide chronological events are summarized in 00_ROOT/NHAT_KY_THI_CONG.md.
- BUILD_MAPPING_REGISTER.md: canonical mapping index for the 05_BUILD layer; not an original artifact.

No source file has been moved, deleted or overwritten in this batch. The exact source inventory and proposed target mapping are recorded in 05_BUILD/00_ROOT/BUILD_MAPPING_REGISTER.md.

### Required next actions
1. Fetch and checksum every candidate from branch work/70/05-build and Sandbox.
2. Compare against any existing Work-root equivalent; record exact duplicate/difference.
3. Decide one canonical target path for each candidate and update Document Register.
4. Prepare backup and rollback evidence.
5. Obtain Vinh's approval for the exact migration batch.
6. Copy/relocate or replace build-branch copies with pointers only after approval.
7. Verify canonical target, mapping link, hashes, GitHub branch and Sandbox readback; independent QE reviews the result.

## 5. Pilot and exclusions
Work 70 is the reference design. Select one pilot only after Work 70 is independently verified and explicitly approved. Work 10/15/28 must not be modified as part of this plan without separate authorization.

## 6. Rollback triggers
Missing/corrupt evidence; lost branch/commit/issue link; wrong Work ID/owner; checksum mismatch; Dashboard/source divergence; inability to restore the prior structure.

## 7. Completion criteria
Inventory baseline, approved mapping, backup checksums, migration log, reconciliation report, unresolved issue list, rollback evidence and explicit acceptance decision. Until all are present, migration is NOT VERIFIED.
