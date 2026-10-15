# Work 28 — Source Snapshot Intake Contract v0.1.0

Date: 2026-10-15
Status: IMPLEMENTED IN SANDBOX (pure contract + regression test source); NOT EXECUTED; NOT A COLLECTOR OR TRANSFER BRIDGE.

## Purpose
Define a fail-closed validation boundary for a read-only source snapshot manifest before any future import. This closes only the manifest-contract design/code slice. It does not read PC files, create an archive, upload bytes, authenticate the collector, verify archive contents, or prove the claimed Git provenance.

## Artifacts
- 04_CODE/source_snapshot_contract.py
- 05_TEST/test_source_snapshot_contract.py

## Contract
- Schema version is exactly 0.1.0.
- Required provenance: collector version, UTC timestamp, repository root, branch, Git HEAD, explicit dirty flag, complete git status --short records, included/excluded path lists.
- Every included file entry must contain exactly relative path, integer size_bytes, and lowercase SHA-256.
- Duplicate paths are rejected. Counts and byte totals must match entries; boolean values do not count as integers for byte/count fields.
- Default limits: 20,000 files; 8 MiB per file; 128 MiB total; 512 characters per path. These are manifest acceptance limits, not proof that a collector enforces its own resource usage.
- Relative paths must fall under a caller-supplied explicit allowlist; traversal, absolute/drive/backslash paths, selected Unicode ambiguity, secret/credential paths, runtime DB/logs, common cache/build directories, Windows reserved device names, and selected unsafe characters are rejected.
- A clean snapshot must have an empty status list; a dirty snapshot must preserve a non-empty status list.
- Stable canonical JSON bytes and a SHA-256 helper are provided.

## Security and trust limits
1. A valid manifest is still untrusted input. Hash fields can be fabricated unless computed by an approved collector over the actual bytes.
2. The archive hash is shape-checked only; this module does not receive or hash an archive.
3. Per-file hashes are shape-checked only; this module does not open or hash the source files.
4. Allowlist entries must be configuration-controlled by the approved collector/integrator, not caller-selected.
5. This contract does not prevent symlink/reparse-point traversal during collection. Collector must open files safely, reject links/reparse points, resolve each file under the canonical repository root, and avoid TOCTOU races.
6. Do not collect secrets, .env*, credentials, private keys/certificates, runtime DB/state, private-data logs, caches, or generated output unless separately reviewed and explicitly allowlisted.
7. No PC source writes, listener restarts, registry mutation, arbitrary execution, or release operations are part of this slice.

## Required tests
Regression tests cover valid manifest, missing fields, allowlist denial, traversal/absolute/drive paths, secret/runtime exclusions, duplicate paths, malformed hash, mismatched byte total, boolean-as-integer rejection, dirty-state preservation, file-count limit, canonical JSON determinism, and SHA-256 known vector.

## Validation status
- File writes to Work 28 Sandbox: DONE (write operation returned status ok).
- Independent readback of both new files: pending in this record; must be done before considering artifact persistence verified.
- Test execution: NOT RUN — no approved execution tool is exposed in this session. Do not claim tests pass.
- PC collector implementation: NOT STARTED.
- Archive transfer/import: BLOCKED — authorized capability absent.
- Canonical source audit / live E2E: BLOCKED pending source snapshot and approved runner.

## Next slice
1. Read back both artifacts and inspect exact content.
2. Have Go independently review the contract/test source; Cla perform a threat-model review, especially allowlist authority, symlink/reparse-point safety, manifest authenticity, and archive hash binding.
3. In an authorized PC-side environment, implement a read-only collector that computes hashes from actual bytes and emits deterministic archive + manifest; do not modify the repo or running MCP service.
4. Use an authorized archive import route to Work 28. After extraction, recompute all per-file hashes and compare with manifest; verify archive hash before extraction.
5. Only after verified import begin canonical implementation source audit and E2E-Automatic.
