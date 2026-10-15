# Nu — Static review: source collector and transfer design
Date: 2026-10-15 (+07)
Work: 28 / MCP-8020-TOOLING-PLATFORM
Scope: static review only; no collector execution, no PC access, no source transfer, no E2E
Disposition: **REVIEWED / NOT APPROVED TO RUN**

## Reviewed artifacts
- `04_CODE/pc_readonly_source_collector.py`
- `04_CODE/source_snapshot_contract.py`
- `05_TEST/test_source_snapshot_contract.py`
- `06_EVIDENCE/KA_SOURCE_SNAPSHOT_INTAKE_CONTRACT_20261015.md`
- `06_EVIDENCE/KA_WORK28_SANDBOX_ONLY_POLICY_20261015.md`

## Positive controls observed
1. Collector uses `subprocess.run` with an argument list, `shell=False`, fixed Git subcommands, timeout and captured output.
2. Source selection is allowlisted to `room_hop_mcp`, `core`, `integration`, `tests` plus selected root manifests; secrets, credentials, keys, databases, logs, caches, build output and common virtual-environment paths are excluded.
3. Symlinks/reparse points are rejected during enumeration and file reads; repository containment is checked before and after read; `O_NOFOLLOW` is used where available.
4. File count, per-file bytes, total bytes and output path separation are bounded.
5. Zip entries are sorted, timestamps are normalized and archive content is created from selected bytes; manifest includes HEAD, branch, dirty flag, status records, file hashes, totals and archive hash.
6. Pure manifest contract is explicitly documented as structural validation only; it does not claim to authenticate provenance or verify archive contents.
7. Current tests cover malformed manifest fields, traversal/secret paths, duplicate files, hash shape, size/count consistency, dirty-state consistency, canonical JSON and a SHA-256 vector.

## Findings and required disposition
### F1 — HIGH: filesystem race/reparse safety is not proven for a hostile or changing tree
`safe_read()` resolves/checks the path, checks link state, then opens by pathname. Parent-directory replacement or a reparse/symlink race between checks and open is not fully eliminated; `O_NOFOLLOW` protects the final component only on platforms that provide it. The second resolve check detects some escapes after the read but cannot prove the bytes came from the intended immutable tree.
**Required:** collect from a read-only/frozen source snapshot where possible, or use component-wise directory-handle/openat-style no-follow traversal and explicit file identity checks. Add a disposable race/reparse test where the approved runner supports it. Until then: BLOCKED for hostile-tree assurance.

### F2 — HIGH: archive/hash claims are not independently bound at import
The collector computes hashes over bytes it reads and writes a zip, but the Work-side design currently has no implemented archive-import route or verifier that hashes the received archive before extraction and recomputes every extracted file hash afterward.
**Required:** import gate must verify archive SHA-256 before extraction, validate manifest, extract into a new destination, recompute every file hash/size/path, reject extra/missing/duplicate entries, and preserve the original manifest/archive hash. Until that route exists: SOURCE_SNAPSHOT_IMPORTED cannot be returned.

### F3 — MEDIUM: collector provenance is reported, not authenticated
`--repo` accepts any local Git working tree and the manifest records caller-observable path/HEAD/status. A valid manifest can be fabricated by a caller or by a different repository. This is correctly acknowledged by the contract, but the overall transfer design must bind collection to an approved operator/channel and preserve an external transfer receipt.
**Required:** approved source channel/identity and immutable transfer receipt; do not treat manifest validity as PC provenance proof.

### F4 — MEDIUM: configured limits have no hard upper bounds in `SnapshotLimits`
`SnapshotLimits` checks positive integers but allows an integrator to configure arbitrarily large values. The collector constants are bounded, but the contract can be invoked with larger limits.
**Required:** add hard maxima or make limits immutable policy constants; add tests for bool, zero, negative and over-hard-maximum values.

### F5 — MEDIUM: manifest validation permits ambiguous/unbounded metadata
`validate_manifest()` checks types for `status_short` and `excluded_paths` but does not bound list length/string length or reject control/newline characters in each item. It also allows unknown top-level fields. This can create parser/logging ambiguity and resource pressure.
**Required:** bound metadata counts/lengths, validate safe strings, and choose/document strict unknown-field rejection or explicit forward-compatible extension rules.

### F6 — MEDIUM: empty snapshot is accepted by the contract
The collector rejects zero selected files, but `validate_manifest()` accepts `included_files=[]`, `file_count=0`, `total_bytes=0`. A source snapshot gate should reject empty input unless an explicit empty-snapshot mode is intended.
**Required:** require at least one included file for this Work 28 intake contract and add a regression test.

### F7 — MEDIUM: output directory and deterministic archive handling need stronger checks
The collector rejects an output path inside the repository and refuses existing archive/manifest names, but does not require the output directory to be empty or reject an existing symlink/reparse-point output path. Archive hashing reads the full archive into memory after writing.
**Required:** require a new/empty non-link output directory, stream archive hashing, and add failure-cleanup tests.

### F8 — LOW: Git read-only invocation should disable optional hooks/state refresh
The collector uses `git status --short --untracked-files=all` without the documented `--no-optional-locks` / `core.fsmonitor=false` hardening. It does not write source files, but an approved collector should minimize repository side effects and nondeterminism.
**Required:** use `git --no-optional-locks -c core.fsmonitor=false ...` for status/rev queries where compatible; record command semantics without secrets.

### F9 — LOW: test coverage is contract-only, not collector/import coverage
`test_source_snapshot_contract.py` does not execute or test the collector, zip layout, archive hash, cleanup, symlink/reparse behavior, file mutation detection, output separation, or post-import recomputation. This is acceptable for a pure contract slice but not for source intake approval.
**Required:** add isolated tests for collector behavior using a disposable fixture tree, then separately test the Work-side import verifier. Do not run on PC under current Sandbox-only policy.

## Transfer design decision
- Static contract/draft quality: **PARTIAL POSITIVE**.
- Source collector run authorization: **NO-GO at this stage**.
- PC source collection: **NOT RUN**.
- Archive transfer/import capability: **BLOCKED / absent from current MCP 8020 tools**.
- Canonical source snapshot: **NOT IMPORTED**.
- E2E-Automatic: **BLOCKED**.
- PC modification/restart/registry mutation: **NOT PERFORMED**.

## Smallest next safe slice in Sandbox
1. Harden the pure contract for hard caps, bounded metadata and non-empty snapshot.
2. Add tests for those rules without touching PC.
3. Specify/import-verifier contract for archive-before-extract and per-file readback hashing.
4. Obtain an actual authorized transfer route. Only after the route is approved and the received bytes are verified may the status change to `SOURCE_SNAPSHOT_IMPORTED`.
5. Start E2E-Automatic only after source import verification; separate contract, collector/import, service, connector and live-PC evidence.

## Final review status
**BLOCKED — NOT APPROVED TO RUN COLLECTOR.** This review is static only and does not claim source provenance, transfer success, test PASS, or E2E PASS.
