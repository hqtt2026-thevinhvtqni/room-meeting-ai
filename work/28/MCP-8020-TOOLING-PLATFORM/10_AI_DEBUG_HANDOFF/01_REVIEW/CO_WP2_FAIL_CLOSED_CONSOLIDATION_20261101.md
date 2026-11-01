# Work 28 — Co consolidated WP2 fail-closed candidate
- **Owner:** Co — Coder / AI Build Assistant
- **Date/time:** 2026-11-01 23:09 UTC+7
- **Scope:** Sandbox-only isolated patch candidate; no production source, live MCP, GitHub branch, PR, or execution gate changed.

## Change made
Merged the exact two fail-closed corrections independently identified by Ka (2026-11-01) into Co's existing suspended-spawn candidate:
1. `_wait_job_drained()` now returns `False` and records `job_member_count_unavailable_fail_closed` when Job Object membership cannot be queried. Unknown membership is not treated as drained.
2. `ManagedProcess.members_count()` preserves `None` when an attached Windows Job Object membership query is unavailable; it no longer falls back to leader-only liveness and falsely reports zero after leader exit.

The rest of the Co suspended-spawn candidate was preserved. Source readback after write returned `status=ok` and the target path.

## Validation status
- **Sandbox write/readback:** PASS for the candidate file only.
- **Static merge scope:** candidate was compared against Ka's isolated review file; differences were confined to the two fail-closed corrections plus explanatory comments.
- **Tests:** NOT RUN. Current MCP 8030 tool inventory exposes Sandbox file operations but no approved Python/pytest execution action.
- **Windows Job Object / child-process containment:** NOT VERIFIED.
- **OS isolation:** NOT VERIFIED.
- **Production/live MCP integration:** NOT APPLIED.
- **GitHub sync:** NOT PERFORMED / NOT VERIFIED.

## Gate
WP2 remains BLOCKED pending execution of the focused fail-closed tests and Windows process-tree tests through the approved canonical runtime. This candidate must not be treated as a production fix or E2E PASS.
