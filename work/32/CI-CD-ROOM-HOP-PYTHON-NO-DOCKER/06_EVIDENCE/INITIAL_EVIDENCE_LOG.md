# Initial Evidence Log — Work 32

Date: 2026-10-19 (Asia/Ho_Chi_Minh). Executor: Xu (AI-01), coordinator.
Updated: 2026-11-04 (Asia/Ho_Chi_Minh). Executor: Vibe agent, on Vinh's instruction "đọc nhật ký và triển khai tiếp" then "OK thực hiện và ghi nhật ký".

## Phase A — Survey evidence
- Reviewed available ROOM-HOP architecture context and repository metadata read-only.
- Created Work 32 Sandbox through MCP :8020 and wrote design/acceptance documentation.
- Created GitHub branch `work/32-ci-cd-room-hop-python-no-docker` from the then-current main head `cc3100c835ad87ac9670a2ba38dc2c2dfae63755`.
- No PC changes, live-service changes or deployment.

## Mirror verification (completed 2026-11-04)
- Mirror verified via GitHub content read-back: all 11 documented files readable and match the README manifest.
- GitHub head of Work branch at verification: `8098d1a7d00d68858442b7fac72ba70a1a0a46f8`.
- Current main head rechecked: `d7266eb9bfedfc534fc87d56548e47841bb583b9` (differs from branch base — merge/backport must be re-planned before integration).
- File count read-back: 11 files + README confirmed.
- Prior blocker (sandbox_read returns empty object): worked around by reading mirror content directly from GitHub; blocker stands for the MCP endpoint itself.

## Survey findings (baseline)
- requirements.txt (as surveyed): pyyaml>=6.0, pytest>=7.0, python-dotenv>=1.0.0, groq>=0.11.0.
- pytest.ini: pythonpath=. ; norecursedirs excludes tests/legacy.
- No .github/workflows existed on the Work branch before Phase B; zero Actions runs on this branch.

## Phase B — Minimal CI pilot (authorized by Vinh on 2026-11-04)
Workflow: `.github/workflows/work32-ci-pilot.yml` — scoped to the Work branch only; permissions contents:read + issues:write; no Docker, no secrets, no deploy. G3/G5 files (live-service/e2e) excluded from G2 by design.

### Run history (evidence-first dispositions)
| Run | Commit | G1 compileall | G2 unit tests | G6 evidence | Disposition |
|---|---|---|---|---|---|
| [#1](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41786211574) | 39e6191 | PASS | FAIL | artifacts only | Repair 1/3: G2 scope was too broad (whole tests/ incl. e2e/integration files) |
| [#2](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41786558557) | d54626e | PASS | FAIL | FAIL (issue lookup via search index) | Repair 2/3: evidence publish step fixed to deterministic lookup |
| [#3](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41786658982) | fd93d3e | PASS | FAIL (exit 2, 5 collection errors) | PASS → issue #39 | Root cause found (see G4 finding) |
| #4 | (this commit) | — | — | — | Repair 3/3: requirements.txt fix, verdict pending |

### G4 finding (root cause of G2 failure, evidenced by run #3 log in issue #39)
- Undeclared dependencies: code imports `requests` (core/connectors.py:21, core/intent_router.py:25), `mcp` (tests/test_mcp_server.py via `from mcp import types`; room_hop_mcp), `fastapi`, `uvicorn` — none declared in requirements.txt.
- Verified via GitHub code search before adding: requests (5 files), mcp (import + from-imports), fastapi (import + from-imports), uvicorn (1 file).
- Fix (repair 3/3): added requests>=2.31, fastapi>=0.110, uvicorn>=0.29, mcp>=1.0 to requirements.txt with a G4-finding comment.

### Evidence channels
- Canonical tracking issue: [#39 "Work 32 CI Evidence Log"](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/issues/39) — per-run summary + pytest log tail, auto-posted by the workflow.
- Issue #38 was a duplicate created by run #2's partially-failing publish step; commented and closed as duplicate on 2026-11-04.
- Artifacts (junit, pytest log, pip freeze) retained 14 days per run.
- CI job logs require repo admin to download via API; the issue channel is therefore the readable by default.

### Repair loop status
Repairs used: 3 of 3 (attempt 1 = G2 scope, attempt 2 = evidence channel, attempt 3 = dependency declaration). Per doctrine, if run #4 does not reach G2 PASS, the loop is exhausted and the Work enters BLOCKED for human review of remaining test failures.
