# WORK 10 — CROSS-PLATFORM VERIFICATION EVIDENCE — RUN 104

- Document ID: W10-CROSS-PLATFORM-CI-EVIDENCE-20261122-RUN104
- Workflow: Work 10 Cross-Platform Verification
- Run ID: `44963124942`; Run #104
- Exact tested commit: `ee6b6cf06643fc92aac1572290e5b3918b481ade`
- Branch: `work/10-computer-agent-mirror`
- URL: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44963124942
- Conclusion: SUCCESS — Ubuntu 24.04 and Windows Server 2022 matrix jobs both passed.

## Ubuntu 24.04
- Job ID: `137026106941`
- Suites: contract 60 PASS; safety 41 PASS; HTTP API 52 PASS; containment 2 PASS; host operations 12 PASS; V8 validator 16 PASS; Dashboard static contract 17 PASS.
- Total: **200 PASS / 0 FAIL / 2 SKIP**
- Real Chromium E2E: PASS
- Artifact ID: `14729759048`; size 41,283 bytes
- ZIP SHA-256: `d3ecf4849ca7b98c0624b165f1b488564617f9e43fdbb5a90f0a45edec587029`

## Windows Server 2022
- Job ID: `137026107561`
- Suites: contract 60 PASS; safety 45 PASS; HTTP API 52 PASS; containment 2 PASS; host operations 14 PASS; V8 validator 16 PASS; Dashboard static contract 17 PASS.
- Total: **206 PASS / 0 FAIL / 0 SKIP**
- Real Chromium E2E: PASS
- Artifact ID: `14729409940`; size 35,163 bytes
- ZIP SHA-256: `5fe5ababa06291bd1b4dde3eef1574bde1f182781db435bc4e46306225c2ea6e`

## What this run verifies

This run is the first full cross-platform regression after Work 10's standalone Dashboard development origin was moved from port 3000 to port 3010. The default allowed Origin, HTTP test fixtures, standalone Dashboard README, code README and host runbook all use `http://127.0.0.1:3010`. This prevents Work 10's standalone test UI from competing with W113's shared Dashboard ingress on port 3000.

All seven regression suites passed on both OS runners. The API, host operations, V8 validator and Dashboard static contract were all exercised; real Chromium E2E also passed.

## Limitations

- Hosted Windows Server 2022 is not the Owner's physical Windows 10 PC.
- Run #104 tested the port-3010 change but preceded the subsequent POSIX process-group cleanup polling/stress-test patch; Run #105/#106 are the follow-up validation for that patch.
- Linux process-group containment remains LIMITED_NOT_CGROUP_V2.
- Production HMAC key provisioning and ROOM-HOP Core/PC Bridge/Dashboard integration remain open.
- Dashboard contract checks are static UI assertions; live Work 10 Dashboard/API interaction on the Owner PC is not proven.

## Disposition

- Port 3010 standalone Dashboard change: **PASS — RUN 104**.
- Cross-platform regression: **PASS — RUN 104**.
- Owner physical PC acceptance: **NOT RUN**.
- Work 10: **ACTIVE — NOT RELEASED**.

**KÝ: Co | AI-07 / End-to-End Architecture & Implementation Lead**
