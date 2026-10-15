# KA → NU: SINGLE CONSOLIDATED DELIVERY MANDATE — WORK 28
Date: 2026-10-15 (+07)
Work: 28 — MCP-8020-TOOLING-PLATFORM
Priority: P0 — one integrated delivery, no piecemeal handoffs
Execution boundary: Sandbox-only. PC access/modification, collector execution, source transfer/import, live service changes and release remain prohibited unless Vinh separately approves.

## Mission
Nu owns one complete, coherent remediation package for the source snapshot lifecycle: collector safety, manifest contract, archive verification, provenance/receipt design, import transaction/reconciliation, and tests/evidence. Do not wait for Ka to issue separate tasks for F1/F3/F7/F8. Implement as much as safely possible in the Work 28 Sandbox, test only through an approved isolated runner, and clearly identify any remaining environmental blocker.

## Canonical artefacts to inspect and reconcile
- `04_CODE/pc_readonly_source_collector.py`
- `04_CODE/source_snapshot_contract.py`
- `05_TEST/test_source_snapshot_contract.py`
- `04_CODE/source_snapshot_import_verifier.py`
- `05_TEST/test_source_snapshot_import_verifier.py`
- Nu's prior reviews and remediation reports under `06_EVIDENCE/`
Do not create a second competing implementation. Update these artefacts coherently or explain why a safe change cannot be made.

## Work package A — F1 filesystem race safety
1. Design and implement a race-resistant read-only source collection strategy appropriate to Windows and the supported test platform.
2. Validate every parent component; reject symlinks, junctions and reparse points; avoid following links during open.
3. Where supported, open with no-follow semantics and compare descriptor/file identity plus size/mtime before and after reading; fail closed if guarantees are unavailable.
4. Use a frozen/read-only source snapshot or an explicitly documented consistent-snapshot method. Do not claim an atomic snapshot from ordinary path checks alone.
5. Add adversarial tests for parent-link replacement, file replacement between validation/open, junction/reparse cases where testable, changed size/mtime, and cleanup after failure.
6. State platform limitations and what cannot be proven in the current environment.

## Work package B — F3 provenance and transfer trust
1. Treat a locally generated manifest as `UNAUTHENTICATED_LOCAL_OBSERVATION`, never as proof of source identity.
2. Define a transfer receipt that binds: trusted source identity, approved channel/session, archive SHA-256, canonical manifest SHA-256, destination Work ID, transfer timestamp/nonce and verifier result.
3. Define who attests each field and how receipt integrity is established; do not use self-asserted manifest fields as independent authentication.
4. If the existing MCP surface has no upload/import route or trusted receipt issuer, record the exact blocker and propose the smallest authorized protocol/tool addition. Do not fabricate a receipt or simulate an import.
5. Add negative tests for mismatched archive/manifest/Work ID, replayed nonce, missing signer/issuer, and untrusted source claims where implementable.

## Work package C — F7 output/archive lifecycle
1. Require a newly created, empty, non-link output directory outside the repository and prove containment; reject pre-existing, linked, reparse and ambiguous paths.
2. Stream archive hashing and bound both compressed archive size and total uncompressed content; reject duplicate entries, path traversal, unexpected entries and zip bombs using conservative limits.
3. Make ZIP/manifest generation deterministic where feasible; specify stable ordering, timestamps, permissions and compression settings. Test reproducibility.
4. Guarantee cleanup of partial output on any failure without deleting unrelated/pre-existing files.
5. Implement post-collection and post-import reconciliation: expected vs actual paths, counts, byte totals and per-file hashes; fail closed on extra/missing/duplicate files.
6. Add failure-injection tests for write failure, hash mismatch, truncated archive, extraction failure and cleanup.

## Work package D — F8 Git command isolation
1. Use fixed argv lists, shell=False, explicit timeout, bounded stdout/stderr and validated repository root.
2. Apply `--no-optional-locks` and `-c core.fsmonitor=false` to Git calls; prevent hooks/config/env from causing writes, network or execution to the extent technically possible.
3. Sanitize relevant environment variables; define a controlled working directory; do not invoke arbitrary repository scripts/hooks.
4. Document the limit: Git flags alone do not guarantee no network or arbitrary side effects if command/config/environment scope is incomplete.
5. Add tests using a fake Git executable/controlled subprocess harness to assert argv, environment, timeout, output bounds and fail-closed behavior. Do not run Git collection on the PC.

## Work package E — contract and import verifier
1. Reconcile schema/version compatibility across collector, contract, tests, verifier and evidence.
2. Enforce independent hard caps; reject bool-as-int, empty source, unknown fields, malformed/ambiguous paths, oversized metadata and invalid dirty-state claims.
3. Verify archive hash before parsing ZIP; validate canonical manifest; compare exact entry set; reject duplicates, directories, traversal, links/special files and unsupported compression; enforce compressed/uncompressed size and compression-ratio bounds.
4. Recompute each file's size/hash while streaming; never trust manifest claims alone.
5. Separate `VERIFIED_IN_MEMORY_NOT_IMPORTED` from any actual import state. No import PASS without a trusted transfer receipt and post-import readback/hash reconciliation.
6. Do not add filesystem extraction unless its path safety, no-follow semantics, staging, atomic commit/rollback and cleanup are independently designed and tested.

## Work package F — complete automated test suite
Provide tests grouped by F1/F3/F7/F8, contract, ZIP verifier, provenance and lifecycle. Include positive, negative, boundary, race and failure-injection tests. Use deterministic fixtures; do not require PC access, network, real secrets or live service mutation.
Every test report must include exact command, interpreter/version, OS/platform, stdout/stderr, exit code, test count and artifact SHA-256. If no approved runner exists, mark tests NOT RUN and report the runner blocker; do not claim PASS from static review.

## Work package G — integrated evidence and handoff
Deliver one consolidated report:
`06_EVIDENCE/NU_WORK28_COMPLETE_SOURCE_LIFECYCLE_REMEDIATION_REPORT_20261015.md`
and update `06_EVIDENCE/NHAT_KY_THI_CONG.md`.
The report must include:
- exact artefact list and schema versions;
- findings matrix F1/F3/F7/F8 and contract/import states;
- design decisions, threat assumptions and platform limitations;
- test inventory with raw logs/exit codes or explicit NOT RUN;
- per-file SHA-256 and canonical manifest/hash evidence for the Sandbox artefacts (not PC source);
- blockers, residual risks, next gate and explicit no-go actions;
- explicit distinction between source files written, tests executed, source transferred and source imported.

## Acceptance criteria
- One internally consistent versioned package; no stale schema fixture.
- All feasible static/unit/adversarial tests executed only in an approved isolated runner, with reproducible evidence. Any test not run is explicitly BLOCKED/NOT RUN.
- F1/F3/F7/F8 each get a disposition of PASS WITH EVIDENCE, BLOCKED, or DESIGN-READY / NOT VERIFIED, with evidence citations and residual risk.
- No claim that local hashes authenticate provenance.
- No PC execution, no collector run, no source transfer/import, no live service changes.
- No release approval. Keep `SOURCE SNAPSHOT: NOT IMPORTED`, `E2E-AUTOMATIC: BLOCKED`, `RELEASE: NO-GO` until separate approval and evidence.

## Ownership / independent review
- Nu: implementation owner for this single package and report.
- Go: independent test reproducibility reviewer; review after Nu submits the consolidated package, not by issuing incremental micro-tasks.
- Cla: independent security reviewer for F1/F3 and all residual risks; review after Nu submits the consolidated package.
- Ka: coordinate, verify evidence boundaries, consolidate review findings and present the gate to Vinh.
- Vinh: final authority for any action crossing Sandbox boundary.

## Dispatch truthfulness
This mandate is persisted in Work 28 Sandbox. The available MCP surface has not provided a verified task-create/dispatch action in this workflow. Therefore this record is a durable assignment document, NOT proof that Nu has received or acknowledged it. Nu must acknowledge this exact path through the supported Room Hop task/proposal mechanism or report the dispatch blocker. Do not claim assignment delivery/acceptance until there is evidence.

## Current gate
```
NU CONSOLIDATED PACKAGE: ASSIGNED IN WORK DOCUMENT / ACKNOWLEDGEMENT PENDING
COLLECTOR RUN: NO-GO
PC ACCESS/MODIFICATION: PROHIBITED
SOURCE TRANSFER/IMPORT: BLOCKED
SOURCE SNAPSHOT: NOT IMPORTED
E2E-AUTOMATIC: BLOCKED
RELEASE: NO-GO
```
