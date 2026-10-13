# Work 101 — PC Integration Gate (Prepared; NOT RUN)

This checklist is for the first time Vinh is back at the PC. Do not infer a PASS from this document.

## Before running
1. Fetch/pull branch `work/101-room-hop-dual-workspace` explicitly; do not checkout or merge into `main`.
2. Open repository root `hqtt2026-thevinhvtqni/room-meeting-ai`.
3. Run `work/101/ROOM-HOP-DUAL-WORKSPACE/05_TEST/run_work101_tests.ps1` from the repository root in PowerShell.
4. Inspect the generated `06_EVIDENCE/LOCAL_UNIT_TEST_*.txt`; confirm branch, HEAD, Python version, exit code and test output.
5. Commit/push test evidence only on the dedicated Work 101 branch after review. Do not include unrelated PC changes.

## Still required after unit tests
- Verify Work 24 bridge contract and actual route/identity; verify Work 27 runner contract and sandbox isolation; verify Work 28 live MCP registry and authorization; reconcile Work 14 lifecycle conflict against source-of-truth evidence.
- Run policy tests, contract tests, path traversal/symlink tests, Windows case-collision tests and approval replay tests.
- Verify Sandbox ↔ GitHub round trip on a disposable, allowlisted fixture file in both directions; read back destination and compare SHA-256.
- Test simultaneous divergent edits: operation must stop as `CONFLICT_PENDING`, with no writes on either side.
- Test stale base, retry/idempotency, network/auth failure, restart/recovery and protected branch denial.
- Verify Dashboard in a real browser; its live status must be sourced from authorized Core/MCP reads, never static placeholder data.
- Capture operation IDs, base/source/destination revisions, digests, timestamps, test logs and runtime identity in `06_EVIDENCE/`.

## Release gates
No routine sync write until policy review, unit tests and target contracts are verified. No integration, merge or release until Vinh explicitly approves the exact operation ID, diff digest, destination branch and base revision.
