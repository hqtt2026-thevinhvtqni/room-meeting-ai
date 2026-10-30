# WORK 70 — EXISTING WORK MIGRATION PLAN
# Kế hoạch chuyển đổi các Work hiện hữu

## 1. Scope and guardrails
Each existing Work may be standardized into the nine-phase lifecycle and receive its own Dashboard. Work ID, repository history, branch names, issues, artifacts and evidence references must be preserved. This is a future migration plan, not an instruction to modify other Works.

## 2. Per-Work migration sequence
1. INVENTORY — list manifest, folders, branches, issues, artifacts, evidence, owner and current status.
2. CLASSIFY — map content to lifecycle phase, 05_BUILD build area, evidence, or legacy history.
3. MAP — record old_path → new_path, old_status → proposed_status and evidence_ref → preserved_ref.
4. DRY RUN — generate a mapping report without writing/deleting/moving source data.
5. REVIEW — owner and independent reviewer inspect mapping, links, permissions and conflicts.
6. BACKUP — create a timestamped snapshot with checksums.
7. APPROVE — obtain explicit approval for that Work.
8. MIGRATE — apply logged, idempotent operations in controlled batches.
9. VERIFY — reconcile counts, hashes, links, branch/commit/issue references and status.
10. ACCEPT / ROLLBACK — close only after owner acceptance; rollback on defined triggers.

## 3. Mapping rules
- Work root and Work ID remain unchanged.
- Lifecycle folders are product-management phases.
- The nine fixed 05_BUILD child directories are engineering build areas, not additional lifecycle phases.
- WPs are logical records in 05_BUILD/00_ROOT/BUILD_REGISTER.md; they reference build areas and artifacts, not per-WP folder trees.
- Top-level 06_EVIDENCE is the cross-phase index; 05_BUILD/06_EVIDENCE is build-specific evidence staging.
- Preserve historical evidence references and original timestamps/authors.
- Unknown destination → MIGRATION_REVIEW_QUEUE; do not guess.

## 4. Pilot and exclusions
Work 70 is the reference design. Select one pilot only after Work 70 is independently verified and explicitly approved. Work 10/15/28 must not be modified as part of this plan without separate authorization.

## 5. Rollback triggers
Missing/corrupt evidence; lost branch/commit/issue link; wrong Work ID/owner; checksum mismatch; Dashboard/source divergence; inability to restore the prior structure.

## 6. Completion criteria
Inventory baseline, approved mapping, backup checksums, migration log, reconciliation report, unresolved issue list, rollback evidence and explicit acceptance decision.
