# WORK 10 — WINDOWS LOCAL LAUNCHER CI EVIDENCE — RUN 157

- Document ID: W10-LOCAL-LAUNCHER-CI-EVIDENCE-20261122-RUN157
- Workflow: Work 10 Cross-Platform Verification
- Run ID: `44964503556`; Run #157
- Exact tested commit: `af915dec86f3ff633163bc8d775ec435fa992643`
- Branch: `work/10-computer-agent-mirror`
- URL: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44964503556
- Conclusion: SUCCESS — Windows Server 2022 and Ubuntu 24.04 jobs both passed.

## Windows Server 2022
- Job ID: `137030366624`
- PowerShell AST parser: START and STOP scripts both PASS.
- Local launcher smoke: PASS — starts API on loopback :8787 and Dashboard on :3010, health reports Work ID 10, Dashboard returns HTTP 200, STOP script verifies and stops only its recorded processes.
- Regression suites:
  - Contract: 60 PASS
  - Safety: 45 PASS
  - HTTP API: 52 PASS
  - Process containment: 2 PASS
  - Host operations: 14 PASS
  - V8 validator: 16 PASS
  - Dashboard static: 17 PASS
  - Dashboard live E2E: 7 PASS
  - Windows launcher contract: **11 PASS**
- Total: **224 PASS / 0 FAIL / 0 SKIP**
- Real Chromium API/runtime E2E: PASS
- Artifact ID: `14730956155`; size 36,791 bytes
- ZIP SHA-256: `4ebb98efe20ec6d2b0e6dcafb927ebe1bb89eb35f7092a3e3eb8f1a8e70fcc97`

## Ubuntu 24.04
- Job ID: `137030366887`
- Regression suites:
  - Contract: 60 PASS
  - Safety: 41 PASS
  - HTTP API: 52 PASS
  - Process containment: 2 PASS
  - Host operations: 12 PASS
  - V8 validator: 16 PASS
  - Dashboard static: 17 PASS
  - Dashboard live E2E: 7 PASS
  - Windows launcher contract: **11 PASS**
- Total: **218 PASS / 0 FAIL / 2 expected SKIP**
- Real Chromium API/runtime E2E: PASS
- Artifact ID: `14730652401`; size 42,919 bytes
- ZIP SHA-256: `7e3ef0b7ed8f52aa5b748dabab90febc8ec371441d198a3b7100798abdf0507d`

## Launcher behavior verified

- Python 3.12 and free loopback ports 8787/3010 are checked.
- Writes and PowerShell roots are disabled by default.
- A per-session bearer token is generated and passed only to child API process environment; it is not written to the session JSON.
- API and Dashboard start on loopback; port 3000 is untouched.
- Health must identify Work ID 10 and Dashboard must return HTTP 200 before the launcher reports success.
- Session JSON stores only process IDs/start times/root/ports, not the token.
- STOP refuses to terminate while an execution is active and verifies command line + process start time before stopping the recorded processes.
- The Windows CI smoke used `-NoClipboard -NoOpenBrowser`; clipboard copy and opening the default browser are intentionally skipped in the noninteractive runner. The normal local mode performs those two actions.

## Limitations

- Hosted Windows Server 2022 is not the Owner's physical Windows 10 PC.
- The local launcher smoke verifies service start/health/HTTP/stop in CI, but physical Windows 10 ACLs, Python installation, Chrome profile, clipboard and user session behavior still require local acceptance.
- Production V8 HMAC key/pins remain operator-provisioned.
- Linux process-group containment remains LIMITED_NOT_CGROUP_V2.
- ROOM-HOP W24/W112/W14/W113 runtime integration remains open.

## Disposition

- PowerShell syntax: PASS on Windows Server 2022.
- Local start/stop launcher smoke: PASS on Windows Server 2022.
- Launcher safety contract: 11 PASS on both OS runners.
- Full hosted regression: Windows 224 PASS; Ubuntu 218 PASS + 2 expected SKIP.
- Work 10: ACTIVE — NOT RELEASED.

**KÝ: Co | AI-07 / End-to-End Architecture & Implementation Lead**
