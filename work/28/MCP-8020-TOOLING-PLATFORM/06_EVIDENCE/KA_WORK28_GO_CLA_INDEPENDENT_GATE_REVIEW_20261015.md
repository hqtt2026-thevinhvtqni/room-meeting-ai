# KA — Work 28 Independent Gate Review Request
Date: 2026-10-15 (+07)
Work: MCP-8020-TOOLING-PLATFORM
Purpose: One consolidated review gate for Go and Cla after Nu's single source-lifecycle remediation package.
Authority: Vinh is final gate authority. Ka coordinates. Nu owns implementation. Go owns independent reproducibility/evidence review. Cla owns independent security/trust-boundary review.
Policy: Sandbox-only. Do not access or modify PC. Do not run collector. Do not transfer/import source. Do not restart or alter live services. No claim of task dispatch/acknowledgement unless the task inbox proves it.

## Package under review
- 04_CODE/pc_readonly_source_collector.py
- 04_CODE/source_snapshot_contract.py
- 04_CODE/source_snapshot_import_verifier.py
- 05_TEST/test_source_snapshot_contract.py
- 05_TEST/test_source_snapshot_import_verifier.py
- 06_EVIDENCE/NU_WORK28_COMPLETE_SOURCE_LIFECYCLE_REMEDIATION_REPORT_20261015.md
- 06_EVIDENCE/NU_FINDING_REMEDIATION_F1_F3_F7_F8_20261015_0840.md
- 06_EVIDENCE/NU_STATIC_REVIEW_SOURCE_TRANSFER_20261015_0834.md

## Go — independent reproducibility/evidence review
1. Check that test discovery paths/imports and the documented canonical command are internally coherent.
2. Review whether positive, negative, boundary, and failure cases actually exercise the production draft contracts/verifier rather than duplicated fixture logic.
3. Check result-state semantics: no in-memory verification may be described as imported, authenticated, or PASS.
4. If and only if an approved isolated runner is available, run the documented test command and preserve exact interpreter/version, OS, command, stdout, stderr, exit code, test count, skipped/errors, and artifact hashes. If no approved runner exists, mark execution NOT RUN / BLOCKED and do not improvise evidence.
5. Return a finding matrix with PASS / FAIL / BLOCKED / NOT VERIFIED, precise file/test references, reproduction steps, and limitations. Do not modify Nu's files during review.

## Cla — independent security review
1. Review F1: parent-component traversal, symlink/junction/reparse handling, no-follow behavior, file identity/size/mtime checks, TOCTOU windows, snapshot immutability and platform-specific gaps.
2. Review F3: source identity, channel/issuer authentication, receipt authenticity, nonce freshness/replay protection, binding to archive hash, canonical manifest hash, Work ID and timestamp.
3. Review F7: output-directory lifecycle, cleanup, archive determinism, ZIP bomb/compression ratio, exact entry set, streaming verification, and the fact that no extraction/atomic commit exists.
4. Review F8: fixed Git argv, shell=False, timeouts/output bounds, environment/config/hooks/fsmonitor/network side effects, and remaining platform risks.
5. Explicitly separate local hash integrity from provenance authenticity. Do not infer trust from manifest labels or receipt shape checks.
6. Return a finding matrix with PASS / FAIL / BLOCKED / NOT VERIFIED, exploit/race scenarios, required evidence, and release implications. Do not modify Nu's files during review.

## Consolidation and acceptance
- Go and Cla review independently and do not rely on each other's conclusion.
- Ka will reconcile disagreements and preserve unresolved blockers.
- No finding closes from readback alone.
- F1 remains BLOCKED until required race/reparse tests and frozen snapshot evidence exist.
- F3 remains BLOCKED until a trusted transfer channel, issuer authentication and replay protection are demonstrated.
- F7/F8 remain DESIGN-READY / NOT VERIFIED until approved execution evidence exists.
- Source snapshot remains NOT IMPORTED; E2E-Automatic remains BLOCKED; release remains NO-GO.
- No PC access/modification, collector run, source transfer/import, live-service change, or release is authorized by this review request.
- This document is persisted coordination guidance only. It is not proof of dispatch, acknowledgement, execution, or approval.
