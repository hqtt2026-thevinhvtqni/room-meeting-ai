# Initial Evidence Log — Work 32

Date: 2026-10-19 (Asia/Ho_Chi_Minh). Executor: Xu (AI-01), coordinator.
Updated: 2026-11-04 (Asia/Ho_Chi_Minh). Executor: Vibe agent, on Vinh's instructions "đọc nhật ký và triển khai tiếp" and "OK thực hiện và ghi nhật ký".

## Phase A — Survey evidence
- Reviewed available ROOM-HOP architecture context and repository metadata read-only.
- Created Work 32 Sandbox through MCP :8020 and wrote design/acceptance documentation.
- Created GitHub branch `work/32-ci-cd-room-hop-python-no-docker` from the then-current main head `cc3100c835ad87ac9670a2ba38dc2c2dfae63755`.
- No PC changes, live-service changes or deployment.

## Mirror verification (completed 2026-11-04)
- Mirror verified via GitHub content read-back: all 11 documented files readable and match the README manifest.
- GitHub head of Work branch at verification: `8098d1a7d00d68858442b7fac72ba70a1a0a46f8`.
- Current main head rechecked: `d7266eb9bfedfc534fc87d56548e47841bb583b9` (differs from branch base — merge/backport must be re-planned before integration).
- Prior blocker (sandbox_read returns empty object): worked around by reading mirror content directly from GitHub.

## Survey findings (baseline)
- requirements.txt (as surveyed): pyyaml>=6.0, pytest>=7.0, python-dotenv>=1.0.0, groq>=0.11.0 (main branch carries the same incomplete file).
- pytest.ini: pythonpath=. ; norecursedirs excludes tests/legacy.
- No .github/workflows existed on the Work branch before Phase B.

## Phase B — Minimal CI pilot (authorized by Vinh on 2026-11-04)
Workflow: `.github/workflows/work32-ci-pilot.yml` — Work-branch-only; permissions contents:read + issues:write; no Docker, no secrets, no deploy. G3/G5 files (live-service/e2e) excluded from G2 by design.

### Run history (evidence-first dispositions)
| Run | Commit | G1 | G2 | G6 | Disposition |
|---|---|---|---|---|---|
| [#1](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41786211574) | 39e6191 | PASS | FAIL (scope too broad) | artifacts only | Repair 1/3: G2 scoped to unit tests only |
| [#2](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41786558557) | d54626e | PASS | FAIL | FAIL (issue lookup) | Repair 2/3: deterministic evidence lookup |
| [#3](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41786658982) | fd93d3e | PASS | FAIL (exit 2, collection errors) | PASS → issue #39 | Root cause: undeclared deps |
| [#4](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41787560785) | 750c08d | PASS | FAIL (exit 1, runtime) | PASS → issue #39 | mcp SDK major-version incompatibility |

### G4 finding 1 (run #3): undeclared dependencies
- Code imports `requests` (core/connectors.py:21, core/intent_router.py:25), `mcp` (tests/test_mcp_server.py), `fastapi`, `uvicorn` — none declared.
- Fix (repair 3/3): added requests>=2.31, fastapi>=0.110, uvicorn>=0.29, mcp>=1.0 to requirements.txt.

### G4 finding 2 (run #4): mcp SDK major-version incompatibility (OPEN — human review)
- `mcp>=1.0` resolves to the latest 2.x, whose `Server` API no longer exposes `@server.list_tools()`.
- `room_hop_mcp/adapter/server.py:32` (and its tests) target the 1.x API → 12+ unit tests FAIL with `AttributeError: 'Server' object has no attribute 'list_tools'` (run #4 log tail in issue #39).
- All G2 failures observed in run #4 are this single root cause; collection/import is now clean.
- Candidate fix awaiting Vinh's decision: pin `mcp>=1.0,<2.0` (one-line requirements change).

### Evidence channels
- Canonical tracking issue: [#39](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/issues/39) — auto-posted per-run summary + log tail.
- Issue #38 closed as duplicate (created by run #2's partially-failing publish step).
- Artifacts (junit, pytest log, pip freeze) retained 14 days per run. CI job-log API download requires repo admin; issue #39 is the default-readable channel.

### Repair loop status: EXHAUSTED (3/3) → G7 human review
- Repairs used: 1) G2 scope, 2) evidence channel, 3) dependency declaration.
- Per doctrine, further automated repair (including the mcp pin) requires Vinh's explicit approval. Phase B G2 final disposition: **BLOCKED pending human decision on the mcp version pin**.
- G0, G1, G6: PASS with evidence. G2: FAIL→BLOCKED (single root cause identified). G3/G5: BLOCKED by design (Phase C). G7: pending Vinh.
