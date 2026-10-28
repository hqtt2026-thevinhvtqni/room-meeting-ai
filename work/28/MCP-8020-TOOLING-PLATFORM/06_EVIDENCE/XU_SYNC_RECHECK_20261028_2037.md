# Work 28 — GitHub/Sandbox recheck addendum
Date: 2026-10-28 (UTC+7)
Owner: Xu — AI-01 / CEO coordination
Canonical source: GitHub branch `work/28-mcp-tooling-platform`
Sandbox: MCP 8030, Work ID `28`

## Current observed results

- `sandbox_list(work_id="28")` now returns `status=ok` and enumerates the Work tree. Earlier safety-layer blocks were intermittent; do not infer a persistent outage from those earlier calls.
- `sandbox_read_probe` successfully reads the Work 28 manifest and evidence files.
- `sandbox_read` remains unreliable: a prior same-path probe produced an empty object `{}` while `sandbox_read_probe` returned content. Keep ordinary read tool marked unreliable until its response shape is fixed and regression-tested.
- GitHub branch exists. Compared from `990349fa7619d0a2347b7141eb7d91f9b993bd31`, branch is ahead by 3 commits, behind by 0; those commits are the reconciliation report and the two Xu evidence mirrors. This comparison is only relative to that base, not the total delta from the older `9093fc0` baseline.

## Exact content comparisons completed in this recheck

The following Sandbox paths were read with `sandbox_read_probe` and compared as complete text against the corresponding file on the GitHub branch. All returned `equal=true`:

- `03_ARCHITECTURE/PROPOSED_CORE_EXECUTION_AUTHORITY_CONTRACT_V1.md`
- `04_CODE/mcp8020_core_authority_authorizer_v1.py`
- `04_CODE/mcp8020_w13_core_client_v1.py`
- `04_CODE/mcp8020_core_execution_session_v1.py`
- `05_TEST/test_core_execution_authority_boot_v1.py`
- `05_TEST/test_core_execution_authority_v1.py`
- `05_TEST/test_mcp8020_core_authority_authorizer_v1.py`
- `05_TEST/test_mcp8020_w13_core_client_v1.py`
- `05_TEST/test_w13_bridge_execution_token.py`
- `05_TEST/test_w13_client_live_authority_e2e_v1.py`
- `06_EVIDENCE/XU_INTEGRATION_TRACE_V54_TO_W13_W12_20261025.md`
- `06_EVIDENCE/XU_EXECUTION_TOOL_CONTINUATION_JOURNAL_20261025.md`

Additional check:
- `05_TEST/test_mcp8020_core_execution_session_v1.py` now matches the GitHub branch exactly (9,232 characters; blob SHA `632abd0b5f140bcf249792c9ef1d355af79853a0`). This supersedes the earlier observation of a canonical Sandbox mismatch for this test file.
- `06_EVIDENCE/REPO_SIDE_W13_HANDLER_AUTH_HARDENING_20261025_GITHUB_HEAD_CANDIDATE.md` matches the GitHub canonical evidence file exactly (42,870 characters; blob SHA `aa4aa19ee7c9746ae3cb8f4a2a79d8b02bb8c28f`).
- Canonical Sandbox `06_EVIDENCE/REPO_SIDE_W13_HANDLER_AUTH_HARDENING_20261025.md` remains older/different (19,348 characters vs 42,870 on GitHub). Candidate preserved; canonical not overwritten.

## Limitations and status

- Reading the Sandbox copy of `VIBE_INDEPENDENT_RECONCILIATION_20261026.md` was blocked by the tool safety layer in this pass. The prior reconciliation record documents an earlier successful exact readback for it; this recheck does not re-certify it.
- This was a targeted file-level recheck, not a recursive byte-for-byte comparison of every path in both trees.
- No source was overwritten, no test was executed, and no CI status was inferred from an empty status-check response.
- Work 28 remains `ACTIVE / INTEGRATION BLOCKED / NOT RELEASED`; execution gate remains `CLOSED`.
