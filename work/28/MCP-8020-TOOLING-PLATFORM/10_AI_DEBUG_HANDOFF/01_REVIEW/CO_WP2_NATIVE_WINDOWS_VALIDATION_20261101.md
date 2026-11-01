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


## Follow-up: suspended-spawn order regression tests (2026-11-01 23:43 UTC+7)

Two deterministic regression tests were added to the focused candidate test file:
1. Assert the exact sequence `CREATE_SUSPENDED` → `AssignProcessToJobObject` → `ResumeThread`.
2. Assert that Job Object assignment failure aborts the suspended process and never calls the resume function.

GitHub commit: `13fb5878c206436c8c164cd4e1c5a221e04a2f37`.

Validation:
- Focused Ubuntu WP2 run [41327747250](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41327747250): **4 passed in 0.38s**.
- Native Windows candidate job in the same run: **13 passed in 1.28s** on Windows Server 2022 / CPython 3.12.10.
- Work28 general CI run [41327747396](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41327747396): **3/3 jobs successful** (Linux lifecycle, Windows lifecycle, unit/regression).

These results verify mocked ordering/fail-closed behavior and real Windows Job Object/process-tree lifecycle in the hosted runner. They still do not prove adversarial scheduling race closure, live Execution Host deployment, or OS sandbox isolation. No production/live MCP changes, PR merge, or gate opening occurred.


## Native pre-assignment execution check (2026-11-01 23:46 UTC+7)

Added a native Windows test that launches a real child whose first instruction writes a marker file. The test observes the actual candidate assign and resume calls and asserts:
- marker absent before Job Object assignment;
- Job Object assignment succeeds;
- marker remains absent immediately before resume;
- marker appears after successful resume.

GitHub commit: `b1b6d207dd7a134c398eff342ab5db34319710e6`.

Validation:
- WP2 run [41327946366](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41327946366): Ubuntu focused tests **4 passed, 1 skipped**; native Windows candidate suite **18 passed in 1.34s**.
- Work28 general CI run [41327946426](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41327946426): all 3 jobs successful (Linux lifecycle, Windows lifecycle, unit/regression).

This provides direct hosted-Windows evidence that the child did not execute before successful Job Object assignment and only executed after resume. It is not an adversarial scheduler stress proof and does not prove live Execution Host deployment or OS sandbox isolation. Production/live MCP source remains untouched; execution gate remains CLOSED.
