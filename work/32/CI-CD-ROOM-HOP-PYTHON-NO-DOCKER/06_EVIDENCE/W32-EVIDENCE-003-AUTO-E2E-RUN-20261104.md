# W32-EVIDENCE-003 — Auto E2E Run 41

- Document Number: W32-EVIDENCE-003
- Priority: P1
- Author: Ka — CSA / Architecture & Backend Owner (delegated)
- Date-Time: 2026-11-04 (hour/minute not captured; not inferred)
- Status: E2E PASS; UNIT FAIL; OVERALL CI FAIL

## Run identity
- Repository: hqtt2026-thevinhvtqni/room-meeting-ai
- Branch: work/32-ci-cd-python-ci-v2
- Commit SHA: 6e56836c3c0b20f39dc59a562e49342c15f0afa4
- Workflow run: 41718006637
- Run URL: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41718006637
- Runner: GitHub-hosted Ubuntu; Python 3.12.15

## Gate results
| Gate | Result | Evidence |
|---|---|---|
| Exact triggering SHA checkout | PASS | Both jobs fetched and checked out exact revision |
| Dependency install + pip check | PASS | Both jobs completed |
| Compile application packages | PASS | Both jobs completed |
| Auto E2E job | PASS | 37 passed, 1 warning, 1.29s |
| Unit job | FAIL | 156 passed, 1 failed, 2.39s |
| Workflow overall | FAIL | Unit job failed; E2E job passed |

## E2E scope executed
- tests/test_e2e.py
- tests/test_execution_host.py
- tests/test_wee_8031_bridge.py
- tests/test_mcp_server.py
- tests/test_http_lifecycle.py
- tests/test_http_recording.py
- tests/test_ci_live_e2e.py
- Live HTTP roundtrip started an actual Uvicorn server on an ephemeral loopback port; both HTTP checks passed.
- E2E artifact ID: 13270472546; name room-hop-ci-evidence-e2e; retained by GitHub Actions.

## Unit failure
- Exact failing test: tests/test_message_v1.py::test_t8_existing_mcp_tools_no_regression
- Result: expected six MCP tools, actual four.
- Expected extras are join_meeting and start_meeting.
- The test fails at the tool-inventory assertion before its subsequent legacy/new paste calls execute.
- Current MCP server source registers four tools. The integration client source has an inconsistent contract: its module prose says four locked tools, while code also declares/uses join_meeting. No authoritative MCP boundary decision was found that authorizes adding start_meeting as a public MCP tool.
- A separate static discrepancy remains: MCP schema advertises optional identity_id, but the handler does not forward it to MeetingService.add_paste. T8 has not reached that assertion because it fails earlier.

## Decision
1. Do not add join_meeting/start_meeting to MCP merely to satisfy the test.
2. Do not rewrite/skip/delete T8.
3. Reconcile the public MCP tool inventory against approved Contract #1 and integration client implementation. Keep any correction isolated to the test/API contract or MCP adapter only after the intended boundary is proven.
4. Then fix and independently test optional identity_id propagation, preserving old two-argument callers.
5. Keep unit and E2E jobs independent. The workflow remains red until both gates pass.
6. No merge to main, branch-protection activation, secrets, deployment, or production mutation.

## Disposition
- Auto E2E pipeline: OPERATIONAL / PASS for the listed scope.
- Unit gate: BLOCKED by unresolved T8 public API contract mismatch.
- Overall CI: FAIL.
- CD / deployment: NOT STARTED.
- Work 32: ACTIVE — NOT RELEASED.
