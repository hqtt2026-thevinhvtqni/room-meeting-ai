# Work 28 — Co consolidated WP2 fail-closed candidate

- **Owner:** Co — Coder / AI Build Assistant
- **Date/time:** 2026-11-01 23:35 UTC+7
- **Scope:** Isolated Sandbox/GitHub branch candidate only; no production source, live MCP, main branch, PR merge, or execution gate changed.

## Change
Merged Ka's independently reviewed WP2 fail-closed corrections into Co's suspended-spawn candidate:
1. `_wait_job_drained()` returns `False` and records `job_member_count_unavailable_fail_closed` when Job Object membership cannot be queried. Unknown membership is not treated as drained.
2. `ManagedProcess.members_count()` preserves `None` when an attached Windows Job Object membership query is unavailable; it no longer falls back to leader-only liveness and falsely reports zero after leader exit.
3. The focused regression test loads the exact isolated Co candidate by file path, avoiding accidental import of the repository's production `execution_host` package.

## Sandbox evidence
- Candidate source, focused test and this report were written/read back through MCP 8030.
- Nhật ký thi công Work 28 was appended with the implementation and test status.

## GitHub synchronization
- Repository: `hqtt2026-thevinhvtqni/room-meeting-ai`
- Branch: `work/28-mcp-tooling-platform`
- Commit: `1064fbd76183df72e1d8018db2aa3ba01ee295f2`
- Synchronized: candidate `process_job.py`, focused pytest file, this evidence report, and workflow `.github/workflows/work28-wp2-fail-closed-pytest.yml`.
- All four files were independently fetched from GitHub at the new commit and their blob SHAs verified.
- Branch ref update used expected previous SHA `1499fc88b35484e370a5209e65bd36df3efca628`; GitHub confirmed success.

## GitHub test results
- Focused pytest workflow, final commit: **2 passed in 0.35s**, exit code 0. Run: [41327090595](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41327090595).
- The first attempt at commit `1499fc88` failed during collection because the test imported the repository's production package rather than the isolated candidate. The test loader was corrected to import the exact candidate file; the rerun above passed.
- Existing Work 28 CI on final commit: **3/3 jobs successful** (Linux lifecycle, Windows lifecycle, unit/regression). Run: [41327090671](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41327090671).

## Limits / gate
- Focused pytest validates two fail-closed branches using mocked Job Object query failures. It does not prove native Windows Job Object membership, suspended-spawn race closure, child-process containment, or OS sandbox isolation.
- Existing Work 28 CI passing is not proof that this isolated candidate is deployed or wired into the live Execution Host.
- Production/live MCP integration: NOT APPLIED.
- Native Windows containment / OS isolation: NOT VERIFIED by the focused candidate tests.
- Execution gate remains CLOSED. WP2 remains BLOCKED pending native Windows process-tree containment evidence and independent review. No E2E or release PASS is claimed.
