# Work 28 — WP2 native Windows candidate validation

**TÊN:** Co  
**CHỨC DANH:** Coder / AI Build Assistant  
**NGÀY:** 2026-11-01  
**GIỜ - PHÚT:** 23:42 (UTC+7)

## Changes made

- Added `execution_host/__init__.py` to the isolated WP2 suspended-spawn candidate so the candidate package can be imported directly during CI.
- Extended `.github/workflows/work28-wp2-fail-closed-pytest.yml` with a `windows-2022` job. It runs the existing process lifecycle/process-tree suite from the candidate directory, causing `execution_host.process_job` to resolve to the isolated candidate, not the production package.
- Existing Ubuntu focused tests remain in place for mocked Job Object query failure cases.

## GitHub commits

- Workflow update: `82518469181a5ad5b7474356d0de914dda931c5a`.
- Candidate package marker: `2997100cc90a90f27be87cab4103adeafc4b9944`.
- Branch: `work/28-mcp-tooling-platform`.

## Executed evidence

- WP2 workflow run [41327587057](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41327587057) completed success, both jobs.
- Native Windows candidate job log: **13 passed in 1.06s**, Windows Server 2022 / CPython 3.12.10. This exercised real Job Object attachment and parent/child process-tree cleanup against the isolated candidate in the hosted Windows runner.
- Latest WP2 workflow run [41327592086](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41327592086) on commit `2997100` completed success, both Ubuntu fail-closed tests and native Windows candidate lifecycle job.
- Work28 general CI run [41327592075](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41327592075) on commit `2997100` completed success, all three jobs: Linux lifecycle, Windows lifecycle and unit/regression.

## Interpretation and limits

This is stronger than the previous mocked-only test: native Windows Job Object attachment and process-tree cleanup have now passed against the isolated candidate on a GitHub-hosted Windows runner. It does **not** prove the suspended-spawn race is closed under adversarial scheduling, that every Windows host policy behaves identically, that the candidate is deployed to the live Execution Host, or that OS sandbox isolation exists.

No production source or live MCP entrypoint was changed. No PR was merged. Execution gate remains CLOSED. Work 28 remains ACTIVE / INTEGRATION BLOCKED / NOT RELEASED. No full E2E or release PASS is claimed.
