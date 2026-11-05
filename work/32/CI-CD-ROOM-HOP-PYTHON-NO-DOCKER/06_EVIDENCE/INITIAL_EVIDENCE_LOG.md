# Initial Evidence Log — Work 32

Date: 2026-10-19 (Asia/Ho_Chi_Minh). Executor: Xu (AI-01), coordinator.
Updated: 2026-11-04 (Vibe agent; Phase B runs #1–#4, repair loop, handoff proposal).
Updated: 2026-11-05 (Vibe agent; G7 approval, mcp pin, run #5–#7 verdicts + product-drift finding).

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
| [#4](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41787560785) | 750c08d | PASS | FAIL (exit 1; 10 failed) | PASS → issue #39 | G4 finding 2: mcp 2.x API break |
| #5, #6 | be6e7c3 / 2374ce5 (docs-only pushes) | PASS | FAIL (same 10 mcp tests; 178 passed) | PASS → issue #39 | No code change; expected repeat |
| [#7](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41941796297) | 95495b9 | PASS | **FAIL (exit 1; 3 failed, 185 passed)** | PASS → issue #39 | mcp pin effective (10→3); remaining = product-drift finding (below) |

### G4 finding 1 (fixed 2026-11-04): undeclared dependencies
- Code imports `requests`, `mcp`, `fastapi`, `uvicorn` — none declared. Fixed via requirements.txt.

### G4 finding 2 (fixed 2026-11-05): mcp SDK major-version incompatibility
- `mcp>=1.0` resolved to 2.x (removed `@server.list_tools()`); pinned to `mcp>=1.14,<2.0` after G7 approval.
- Effect: 10 failing tests → 3 failing tests (185 passed).

### Product-drift finding (run #7 — G5 scope, OPEN — requires Coder under approval, NOT a CI defect)
1. `tests/test_message_v1.py::test_t8_existing_mcp_tools_no_regression`: `room_hop_mcp/adapter/server.py` registers only 4 tools (`add_paste_to_meeting`, `get_meeting`, `get_transcript`, `list_meetings`); the frozen contract ("6 tools KHÔNG đổi, KHÔNG thêm add_message") requires also `join_meeting` and `start_meeting`.
2. `tests/test_f4_resource_limits.py` (2 tests): `add_paste` inputSchema is `{'type': 'string'}` without `maxLength`; F4 policy contract requires `maxLength == 1048576`.
- These are product/test-contract mismatches in the source under test — outside the CI pilot's repair scope. Candidate paths: (a) Coder restores the 2 missing tool registrations + `maxLength` in server.py after Vinh's approval; or (b) Reviewer/QE confirms whether main head `d7266eb…` already carries the fix (branch divergence from base `cc3100c…` is a plausible cause and must be checked first).

### G7 decision record
- 2026-11-05: Vinh instructed "triển khai tiếp w32" → recorded as approval to apply the proposed mcp pin from this session and verify via CI (executed, run #7).

### Evidence channels
- Canonical tracking issue: [#39](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/issues/39) — auto-posted per-run summary + log tail.
- Issue #38 closed as duplicate. Artifacts retained 14 days per run; CI job-log API download requires repo admin.

### Gate status (after run #7)
- G0, G1, G6: PASS with evidence. G7: PASS (Vinh, 2026-11-05).
- G2: FAIL — remaining 3 failures are product-drift (see finding above); CI-side work complete.
- G3/G5: BLOCKED by design (Phase C).
- Next: Vinh decides product-repair path (Coder scope) or main-head reconciliation first.
