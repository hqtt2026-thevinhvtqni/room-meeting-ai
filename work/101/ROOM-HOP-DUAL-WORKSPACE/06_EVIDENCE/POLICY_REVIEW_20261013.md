# Work 101 — Policy Review (Static Review Only)

Date: 2026-10-13
Review type: source inspection and test coverage review; NOT runtime execution.

## Issues found and corrected
1. The denylist previously excluded the entire `06_EVIDENCE/` tree, which would prevent syncing the Work's own evidence documents. The policy now permits text evidence files while still rejecting logs and runtime/generated files by extension/name.
2. Snapshot validation now rejects case-insensitive path collisions, protecting Windows workspaces from two Git paths that alias on common Windows filesystems.
3. Snapshots may carry the baseline revision they were collected against. A mismatch produces `STALE_BASE` and no transfer plan.
4. A pure `build_sync_plan` function now emits deterministic direction-specific file lists and a SHA-256 diff digest. It is DRY_RUN only, rejects `main`/`master`, checks permitted path roots, and produces no transfer paths for conflicts or stale bases.
5. A guarded PowerShell test runner was prepared for the first PC session; it checks the repository, exact branch, and required files before running tests, then writes an evidence record.

## Current boundaries
- The policy module is pure: no filesystem writes, credentials, network calls, Core/MCP calls or GitHub writes.
- The plan builder does not execute a transfer and is not an adapter.
- Symlink/realpath containment, atomic write strategy, provider-specific revisions, Core authorization, audit persistence, and restart/recovery still require adapter design and runtime verification.
- The Python unit tests have not been run in a trusted execution environment yet. Adding a GitHub Actions workflow requests a branch-scoped hosted test run, but PASS must not be claimed until a real run result is observed.
- No merge or release. All Work changes remain on `work/101-room-hop-dual-workspace`; `main` is untouched.
