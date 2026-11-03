# W32-EVIDENCE-001 — GitHub Actions CI Pilot Results

- Document Number: W32-EVIDENCE-001
- Priority: P1
- Work: 32 — CI-CD-ROOM-HOP-PYTHON-NO-DOCKER
- Owner: Ka — CSA / architecture
- Date-Time: 2026-11-03 09:20 UTC+07:00
- Status: CI PILOT EXECUTED — BLOCKED BY ONE EXISTING CONTRACT FAILURE

## 1. Source identity

- Repository: hqtt2026-thevinhvtqni/room-meeting-ai
- Branch: work/32-ci-cd-python-ci-v2
- Tested HEAD: b7e683dc5fa5ee165c9c12d9a7ee64a34a115550
- Base main SHA: 9e4002cbd93a6b92684b17623d79a1adda161d37
- Compare: branch ahead of main, behind 0; only .github/workflows/ci.yml and requirements.txt changed.
- Workflow: .github/workflows/ci.yml
- Run ID: 41565286414
- Run URL: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41565286414
- Runner: GitHub-hosted Ubuntu 26.04; Python 3.12.
- Permissions: contents: read. No secrets or production endpoints are used.

## 2. Results

- Repository fetch without submodule recursion: PASS.
- Python setup: PASS.
- Install requirements + pip check: PASS.
- compileall core agents: PASS.
- Test suite: 201 passed, 1 failed in 3.76s.
- Artifact: room-hop-ci-evidence; artifact ID 13197759403; SHA-256 6229212163804e1a691a873026ed3b13ad67dd7e627811f109c26dedfeccc111; retention until 2026-11-17.
- Overall CI: FAIL / BLOCKED. Do not report CI PASS.

## 3. Confirmed failure

Test: tests/test_message_v1.py::test_t8_existing_mcp_tools_no_regression.

Expected by test: six MCP tools including join_meeting and start_meeting.
Actual in room_hop_mcp/adapter/server.py: four registered tools — add_paste_to_meeting, get_meeting, get_transcript, list_meetings. join_meeting and start_meeting are not registered.

This is an existing MCP public-boundary contract mismatch, not a CI runner/dependency error. The CI work must not modify Core or MCP server behavior merely to turn the check green. Preserve this test as a release gate until the API contract owner reconciles intended MCP tools and tests.

## 4. Dependency corrections evidenced by CI

- requests was imported by core/connectors.py and core/intent_router.py but absent from requirements.txt. Added requests>=2.31.0.
- MCP server imports mcp; the T8 test imports mcp.types. Added mcp==1.28.1 (matching the known project runtime).
- HTTP adapter imports FastAPI; HTTP tests use TestClient/httpx. Added fastapi>=0.115.0 and httpx>=0.27.0.
- These dependency additions are on the Work 32 feature branch only; main is unchanged.

## 5. Checkout issue and mitigation

The first Actions attempt failed in actions/checkout post-cleanup because the repository tree contains a gitlink named room-meeting-ai but no valid .gitmodules mapping. Do not rewrite repository submodule structure as part of Work 32. The workflow now fetches the exact triggering SHA with git init/fetch/checkout and does not recurse submodules. This step passes in subsequent runs.

## 6. Tests intentionally not in this CI gate

- tests/test_browser_agent_adapter_e2e.py: requires localhost:8787 and external HTTP.
- tests/test_integration.py: starts MCP stdio integration process; requires isolated process/service fixtures.
- tests/test_work13_wee_integration.py: Windows-specific python.exe and host adapter assumptions; not portable to Ubuntu as written.
- tests/test_f4_resource_limits.py: file documents that some tests are expected to fail pending F4 implementation; not a general CI gate.
- tests/legacy/*: historical legacy governance tests excluded by pytest.ini.
- No test has been deleted or silently marked passing.

## 7. Next actions

1. Keep current CI red until the MCP tools contract mismatch is resolved by an explicit architecture/API decision; do not bypass T8.
2. Review whether MCP lifecycle tools are intended public API or the test is stale; update code or test only after that contract is established.
3. Add integration/E2E jobs only after service isolation, process cleanup, and platform assumptions are explicit.
4. Add branch protection and required status checks after verifying repository administration access and a stable green gate.
5. CD/VPS remains NOT STARTED; no secrets, SSH or deployment credentials have been configured or used.

## 8. Disposition

CI workflow operational: PASS.
Runner + dependency + compile: PASS.
Bounded offline regression: 201 PASS / 1 FAIL.
CI gate: BLOCKED.
CD/VPS: NOT STARTED.
Production release: NOT AUTHORIZED.


## Correction Addendum — artifact binding (2026-11-03 09:22 UTC+07:00)

The artifact ID originally referenced in section 2 (13197759403) belongs to the earlier 37-test run `41565074858`, not the expanded 201-pass/1-fail run. The authoritative artifact for run `41565286414` at SHA `b7e683dc5fa5ee165c9c12d9a7ee64a34a115550` is:

- Artifact ID: `13199005568`
- Name: `room-hop-ci-evidence`
- SHA-256: `c1c9666271021cd430e4eceb39a991bf6b2d68d6c047b39177bf041bbc46887e`
- Expiry: 2026-11-17T02:19:05Z

Use this artifact as the source of truth for the expanded test result.
