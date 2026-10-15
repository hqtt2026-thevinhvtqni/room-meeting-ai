# Ka — Work 28 source intake hardening checkpoint
Date: 2026-10-15 (+07)
Scope: Sandbox-only contract/verifier design. No PC access, no collector execution, no archive transfer, no extraction.

## Input review
Read back and reviewed Nu report:
`06_EVIDENCE/NU_STATIC_REVIEW_SOURCE_TRANSFER_20261015_0834.md`
Disposition accepted: REVIEWED / PARTIAL POSITIVE; collector NO-GO; transfer BLOCKED; E2E BLOCKED.

## Sandbox changes persisted
1. `04_CODE/source_snapshot_contract.py`
   - Contract schema version advanced to 0.1.1.
   - Added hard policy ceilings for max files, per-file bytes, total bytes and path length; custom limits cannot exceed ceilings and booleans are not accepted as integers.
   - Added bounds and safe-string validation for `status_short` and `excluded_paths`.
   - Rejects unknown top-level fields.
   - Rejects empty included-file snapshots.
   - Maintains explicit disclaimer: structure/hash-shape checks do not authenticate source provenance.
2. `05_TEST/test_source_snapshot_contract.py`
   - Updated fixture schema version.
   - Added regression cases for unknown fields, hard-limit values, empty snapshots, metadata control characters and metadata bounds.
3. `04_CODE/source_snapshot_import_verifier.py`
   - Added an in-memory verifier draft: checks archive digest before ZIP parsing; validates manifest; rejects duplicate/directory/unexpected ZIP entries; enforces entry-count, compressed archive, per-file and total limits; recomputes per-file byte counts and SHA-256.
   - It does not extract or write files. Success label is `VERIFIED_IN_MEMORY_NOT_IMPORTED`.
   - It explicitly does not authenticate collector identity/provenance.
4. `05_TEST/test_source_snapshot_import_verifier.py`
   - Added fixtures/tests for a valid archive, archive hash mismatch, per-file hash mismatch, extra ZIP entry, duplicate entry, traversal path and corrupt archive.
5. `04_CODE/pc_readonly_source_collector.py`
   - Updated draft schema marker to 0.1.1 only to align its manifest with the contract. This is not collector approval and does not resolve Nu's filesystem race, metadata bounds, output-directory, stream-hashing or provenance findings.

## Evidence status
- Sandbox writes: returned status `ok` for the five artefact writes/updates.
- Code readback: contract, test and collector were read to prepare changes; verifier was read back before its hardening edit.
- **Tests: NOT RUN.** Current MCP Sandbox surface supports text file read/write/append but no authorized isolated code runner was established in this turn. Do not claim syntax, unit-test, ZIP behavior or integration PASS.
- No source snapshot imported; no transfer receipt; no canonical source audit; no PC action.

## Remaining blockers
- Nu F1: filesystem race/reparse safety remains unresolved; collector remains NO-GO.
- Nu F3: provenance authenticity and approved source/transfer identity remain unresolved.
- Nu F7/F8: output directory/symlink guard, cleanup/determinism, streaming archive hash and Git optional-lock/fsmonitor hardening remain unresolved.
- Import verifier is a draft, not a production importer. It verifies in-memory consistency only, not provenance; it does not safely extract to a destination, enforce filesystem no-follow semantics, create an immutable receipt or atomically commit an import.
- Need an actual authorized archive transfer/import route. Current MCP 8020 tools do not provide archive upload/import.
- Need executable, approved test runner and raw stdout/stderr, exit code, environment/version and artifact hashes before any test PASS.
- E2E-Automatic remains BLOCKED until canonical source is transferred, verified and a runner/security gate is approved.

## Gate decision
```
CONTRACT HARDENING: WRITTEN / NOT TESTED
IN-MEMORY IMPORT VERIFIER: DRAFT / NOT TESTED
COLLECTOR RUN: NO-GO
PC EXECUTION: NOT RUN
SOURCE TRANSFER: BLOCKED
SOURCE SNAPSHOT: NOT IMPORTED
E2E-AUTOMATIC: BLOCKED
PC DEVELOPMENT/TRANSFER: PROHIBITED
RELEASE: NO-GO
```
