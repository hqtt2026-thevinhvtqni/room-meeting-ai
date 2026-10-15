# Nu — Remediation disposition for F1, F3, F7, F8
Date: 2026-10-15 (+07)
Work: 28 / MCP-8020-TOOLING-PLATFORM
Scope: Sandbox design/source review only; collector **not run**; no PC access or modification
Status: **REMEDIATION SPECIFIED / VERIFICATION BLOCKED**

## F1 — filesystem race, symlink/reparse and TOCTOU
### Action required in collector source
- Keep the repository root canonical and reject a symlink/reparse repository root.
- Before opening each selected file, reject symlink/reparse state for the file and every parent component between repository root and file.
- Open read-only with `O_NOFOLLOW` where supported; never follow a selected file link.
- Compare pre-open path identity with the opened descriptor (`st_dev`, `st_ino` where available, size and mtime) and compare descriptor identity/size/mtime again after reading.
- Preserve the existing containment checks before and after read.
- Prefer a frozen/read-only source snapshot for any approved collection. A pathname-based reader cannot honestly claim immunity to a hostile concurrent tree; the import gate must retain this limitation.
### Verification gate
F1 is **NOT PASS** until disposable tests cover symlink/reparse rejection, file replacement during read, parent-component replacement where testable, and byte/metadata mismatch. No PC run is authorized in this slice.

## F3 — provenance is reported, not authenticated
### Boundary decision
- `repo_root`, branch, HEAD, dirty state and hashes are observations made by a local process; they are not authentication.
- A structurally valid manifest must be labeled `UNAUTHENTICATED_LOCAL_OBSERVATION` unless an approved source channel supplies an external authenticated receipt.
- Import must require a separate transfer receipt binding: approved source identity/channel, collection timestamp, archive hash, manifest hash and destination Work. Caller-supplied manifest fields alone cannot satisfy this gate.
- Public GitHub revision, copied metadata, or a self-declared identity must not substitute for the canonical PC source.
### Verification gate
F3 remains **BLOCKED** until an approved read-only transfer channel provides and preserves the external receipt. No collector execution is needed or permitted to claim F3 resolved.

## F7 — output directory and archive handling
### Required collector hardening
- Require an output directory that is outside the repository, is not a symlink/reparse point, and is new or empty before collection.
- Refuse pre-existing archive/manifest names and clean partial outputs on all failure paths.
- Keep sorted ZIP entry order and normalized timestamps.
- Hash the archive by streaming from disk rather than loading the complete archive into memory.
- Import verification must reject extra/missing/duplicate ZIP entries and recompute extracted file hashes.
### Verification gate
F7 is **DESIGN-READY / NOT VERIFIED** until isolated fixture tests cover non-empty output rejection, symlink/reparse output rejection, deterministic entry metadata, archive hash, and partial-output cleanup.

## F8 — minimize Git side effects and nondeterminism
### Required collector hardening
- Use `git --no-optional-locks -c core.fsmonitor=false` for read-only metadata queries, with `shell=False`, fixed argv and timeout.
- Do not invoke hooks, arbitrary commands or network operations.
- Record only branch/HEAD/status evidence; do not expose environment variables, credentials or full command lines.
### Verification gate
F8 is **DESIGN-READY / NOT VERIFIED** until an isolated test/inspection confirms the exact argv and that source files remain unchanged. No PC execution is permitted under the current Sandbox-only policy.

## Safe next slice in Work 28
1. Apply the source-only hardening above to the collector/contract and add fixture tests in Sandbox.
2. Add a pure import-verifier contract for archive-before-extract and post-extract hash reconciliation.
3. Read back every changed file; run only if an approved Sandbox runner becomes available. Until then classify tests as NOT RUN.
4. Keep F3 and source intake blocked until an authorized transfer capability and external receipt exist.

## Current decision
- F1: BLOCKED pending race-safe implementation and tests.
- F3: BLOCKED by missing authenticated source/transfer channel; not solvable by a local manifest alone.
- F7: DESIGN-READY / NOT VERIFIED.
- F8: DESIGN-READY / NOT VERIFIED.
- Collector: **NOT RUN**.
- PC: **NOT ACCESSED / NOT MODIFIED**.
- Source snapshot: **NOT IMPORTED**.
- E2E-Automatic: **BLOCKED**.
