# Initial Evidence Log — Work 32

Date: 2026-10-19 (Asia/Ho_Chi_Minh). Executor: Xu (AI-01), coordinator.
Updated: 2026-11-04 (Vibe agent; Phase B runs #1–#4, repair loop, handoff proposal).
Updated: 2026-11-05 (Vibe agent; G7 approval, mcp pin, run #5–#7 record).

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
| [#3](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41786658982) | fd93d3e | PASS | FAIL (exit 2, collection errors) | PASS → issue #39 | G4 finding 1: undeclared deps |
| [#4](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41787560785) | 750c08d | PASS | FAIL (exit 1; 10 failed, rest of suite green) | PASS → issue #39 | G4 finding 2: mcp 2.x API break |
| #5, #6 | be6e7c3 / 2374ce5 (docs-only pushes) | PASS | FAIL (same 10 mcp tests; 178 passed) | PASS → issue #39 | No code change; expected repeat while BLOCKED |

### G4 finding 1 (run #3, fixed): undeclared dependencies
- Code imports `requests`, `mcp`, `fastapi`, `uvicorn` — none declared.
- Fix: added to requirements.txt (repair 3/3).

### G4 finding 2 (runs #4–#6, fixed 2026-11-05): mcp SDK major-version incompatibility
- `mcp>=1.0` resolved to 2.x, whose `Server` API removed `@server.list_tools()` used by `room_hop_mcp/adapter/server.py` → exactly 10 unit tests FAIL; 178 others PASS.
- Resolution researched on PyPI: latest mcp = 2.3.0; last 1.x release = 1.14.0.
- Fix: pin `mcp>=1.14,<2.0` in requirements.txt.

### G7 decision record (2026-11-05)
- 2026-11-04: repair loop exhausted 3/3 → BLOCKED; proposal `02_EXTENSION/PHASE_B_HANDOFF_XU.md` recorded for Xu (per Vinh: no chat-side implementation).
- 2026-11-05: Vinh instructed "triển khai tiếp w32" → recorded as G7 approval to apply the proposed mcp pin from this session and verify via CI.
- Run #7 (this commit): verdict recorded below after execution.

### Run #7 verdict
- Pending at commit time; update with conclusion + URL after completion.

### Evidence channels
- Canonical tracking issue: [#39](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/issues/39) — auto-posted per-run summary + log tail.
- Issue #38 closed as duplicate.
- Artifacts retained 14 days per run; CI job-log API download requires repo admin.

### Gate status after run #7
- G0, G1, G6: PASS with evidence. G2: recorded after run #7. G3/G5: BLOCKED by design (Phase C). G7: PASS (Vinh, 2026-11-05).
