# Initial Evidence Log — Work 32

Date: 2026-10-19 (Asia/Ho_Chi_Minh). Executor: Xu (AI-01), coordinator.
Updated: 2026-11-04 (Asia/Ho_Chi_Minh). Executor: Vibe agent, on Vinh's instruction "đọc nhật ký và triển khai tiếp".

## Phase A — Survey evidence
- Reviewed available ROOM-HOP architecture context and repository metadata read-only.
- Created Work 32 Sandbox through MCP :8020 and wrote design/acceptance documentation.
- Created GitHub branch `work/32-ci-cd-room-hop-python-no-docker` from the then-current main head `cc3100c835ad87ac9670a2ba38dc2c2dfae63755`.
- No PC changes, CI activation, live-service changes or deployment.

## Mirror verification (completed 2026-11-04)
- Mirror verified via GitHub content read-back: all 11 documented files readable and match the README manifest.
- GitHub head of Work branch at verification: `8098d1a7d00d68858442b7fac72ba70a1a0a46f8` (docs(work32): mirror CI/CD design documentation).
- Current main head rechecked: `d7266eb9bfedfc534fc87d56548e47841bb583b9` (differs from the branch base — merge/backport must be re-planned before any integration).
- File count read-back: 11 files + README confirmed.
- Prior blocker (sandbox_read returns empty object): worked around by reading mirror content directly from GitHub; blocker stands for the MCP endpoint itself, not for this Work.

## Survey findings (baseline)
- requirements.txt: pyyaml>=6.0, pytest>=7.0, python-dotenv>=1.0.0, groq>=0.11.0.
- pytest.ini: pythonpath=. ; norecursedirs excludes tests/legacy.
- No .github/workflows directory existed on the Work branch (verified via API); zero Actions runs on this branch before Phase B.

## Phase B — Minimal CI pilot (authorized by Vinh on 2026-11-04)
- Added `.github/workflows/work32-ci-pilot.yml` on the Work branch only.
- Scope: push/PR/workflow_dispatch limited to `work/32-ci-cd-room-hop-python-no-docker`; permissions contents:read; timeout 15 min; no Docker, no secrets, no deploy.
- Gates wired: G0 source/environment record; G1 pip install + compileall syntax gate; G2 pytest tests/ (isolated, no network); G4 toolchain versions; G6 evidence artifacts (junit + pip freeze, 14-day retention).
- Gates G3/G5 intentionally NOT RUN in this phase (BLOCKED by design, per ACCEPTANCE_PLAN Phase C prerequisites).
- First run disposition: recorded after the workflow's first execution (see Actions run URL).
