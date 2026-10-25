# Work 28 Execution Contract Migration Map
Date: 2026-10-25
Status: DESIGN / NOT LIVE
Branch: work/28-mcp-tooling-platform

## Decision
Keep all seven execution/evidence tools marked NOT_IMPLEMENTED until the canonical Core :8000 -> W12/W13 route, runtime identity, OS isolation, and protected evidence gates are proven. The new Python contract validator is a candidate contract module, not a live authorization or execution boundary.

## Current-to-target mapping

| Current v54 catalog tool | Current input shape | Target contract capability | Required migration |
|---|---|---|---|
| sandbox_run_python | work_id, script, args, timeout_seconds | python_run | Replace inline/script + free-form args with Work-relative entry_path, operation RUN_SCRIPT/RUN_TESTS, and required expected_source_sha256. |
| sandbox_run_command | work_id, command, args, timeout_seconds | None | Do not migrate arbitrary command strings. Remove from the future public contract or keep blocked; no alias that bypasses the Python contract. |
| sandbox_get_execution_status | run_id | python_status | Reauthorize principal + Work on every read; unauthorized and unknown run IDs must not disclose existence. |
| sandbox_get_execution_result | run_id | python_output_read | Target requires a bounded selector (STDOUT, STDERR, SUMMARY) and reauthorization; never accept arbitrary output paths. |
| sandbox_collect_artifact | run_id, artifact_path | Protected evidence/artifact API | Replace caller-selected arbitrary artifact path with server-owned artifact references and integrity metadata. |
| sandbox_generate_evidence | run_id, evidence_type, refs | Protected evidence API | Core/runtime must bind evidence to request/run/source hash/runtime identity/exit/test summary and store it outside agent write/delete control. |
| sandbox_create_handoff | work_id, status, evidence_refs, next_action | Handoff after verified result | Reject caller-asserted PASS unless Core verifies protected evidence; handoff must reference the authoritative run result. |
| No current public cancellation tool | Gateway client protocol has cancel but catalog has no cancel entry | python_cancel | Add only after reauthorization, process-tree termination, cleanup evidence, and distinct CANCELLED terminal state are verified. |

## Necessary conditions before implementation
1. Exact deployed MCP and Core revisions are recorded.
2. Authenticated transport supplies principal; Core derives authorized WorkContext.
3. Existing authenticated Core route reaches the one canonical W12/W13 runtime; no direct MCP-to-host route and no second host.
4. OS isolation and network/host-secret denial are independently evidenced.
5. Immutable per-run snapshot hash matches the caller's expected SHA-256 before execution.
6. Protected evidence cannot be modified by ordinary Sandbox write/delete tools.
7. RUN_TESTS PASS requires a trusted summary with total > 0, failed = 0, errors = 0, exit code 0, exact source hash, runtime identity, and protected evidence reference.
8. Cla threat review and Go independent E2E pass, including negative tests and cleanup verification.

## Current explicit incompatibilities
- The candidate contract requires entry_path and expected_source_sha256; the legacy catalog still accepts script and does not require a source hash.
- The gateway currently forwards the legacy request shape and is not wired to the canonical Core route.
- The service returns NOT_IMPLEMENTED before handler dispatch. Gateway injection alone must not activate catalog entries.
- A validator/unit test in an isolated environment is not evidence of live runtime reachability or OS isolation.

## Release rule
No catalog status flip, no endpoint activation, and no release until every necessary condition above has evidence attached to the exact deployed revisions. Missing/stale runtime identity, absent evidence, source hash mismatch, zero tests, timeout, malformed results, or incomplete process cleanup must never produce PASS.
