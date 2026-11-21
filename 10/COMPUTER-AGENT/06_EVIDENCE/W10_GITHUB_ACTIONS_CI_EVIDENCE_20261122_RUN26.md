# WORK 10 — GITHUB ACTIONS CI EVIDENCE — RUN 26

- Record: W10-CI-20261122-RUN26
- Work: 10 — COMPUTER-AGENT
- Workflow: Work 10 Real Browser E2E
- Run: [44953668873](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44953668873)
- Run number: 26
- Job ID: 136996928129 (`real-browser`)
- Tested commit: `cd423e5fe304775162b74577523457150fa3a016`
- Branch: `work/10-computer-agent-mirror`
- Start: 2026-11-22 04:51:09 (UTC+07:00)
- Completed: 2026-11-22 04:51:58 (UTC+07:00)
- Runner: Ubuntu 24.04.5 LTS
- Python: 3.12.16
- Playwright: 1.55.0
- Overall conclusion: SUCCESS

## Step results
All reported job steps completed successfully:
1. Checkout exact tested commit.
2. Setup Python 3.12.
3. Install dependencies and Chromium.
4. Syntax check.
5. Offline contract tests — log states `Offline contract tests: ALL PASSED`.
6. Real Chromium E2E — JSON result reports `status: PASS`, state trace `PLANNED → RUNNING → VERIFYING → PASS`.
7. Browser scenario observed title `Work 10 Browser E2E Target`, submitted result `SUBMITTED: Work 10 REAL E2E`, extracted the result, captured screenshot and exercised download.
8. Evidence artifact upload completed.

## Retained artifact
- Artifact: `work10-real-browser-evidence`
- Artifact ID: `14726835944`
- Size: 19,182 bytes
- SHA-256: `1f02e24c6e475692d758908a8125000b2c10225f792de1643d6c4ea1cddd6d99`
- [Open workflow run and artifact](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44953668873)

## Scope and limitations
This run validates the GitHub canonical branch's code at the exact commit above, on an Ubuntu GitHub-hosted runner. It is evidence for the branch's existing offline contract suite and real Chromium browser workflow only.

It does NOT validate:
- Sandbox's divergent v1.3.0 source files;
- Windows PC filesystem access or PowerShell execution;
- Windows Job Object / process-tree containment;
- the V7/V8 JSON Schema or semantic validator;
- integrated ROOM-HOP MCP → PC execution;
- Dashboard integration or release readiness.

The post-job cleanup emitted a submodule warning (`No url found for submodule path 'room-meeting-ai' in .gitmodules`) after the test and artifact-upload steps had completed. The workflow run's overall conclusion remained SUCCESS. Track the warning separately; do not reinterpret it as a failed test.

## Disposition
- GitHub branch offline/syntax/browser CI at the tested commit: **PASS**.
- Sandbox exact-source parity: **BLOCKED**.
- Windows/PC execution: **NOT VERIFIED**.
- P0 process isolation: **BLOCKED**.
- Work 10 release: **NOT AUTHORIZED**.

KÝ: Co | AI-07
