# WORK 10 — CROSS-PLATFORM VERIFICATION EVIDENCE — RUN 69

- Document ID: W10-CROSS-PLATFORM-CI-EVIDENCE-20261122-RUN69
- Workflow: Work 10 Cross-Platform Verification
- Run ID: `44962226803`; Run #69
- Exact tested commit: `d6aa3283dec649e57bd51bc47299e3596f39b8ac`
- Branch: `work/10-computer-agent-mirror`
- URL: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44962226803
- Conclusion: SUCCESS — both matrix jobs completed successfully.

## Ubuntu 24.04
- Job ID: `137023329568`
- Contract: 60 PASS
- Safety: 41 PASS / 2 expected Windows-only SKIP
- HTTP API: 52 PASS
- Process containment: 2 PASS
- Host operations: 12 PASS
- V8 acceptance validator: 16 PASS
- Dashboard static contract: **17 PASS**
- Total: **200 PASS / 0 FAIL / 2 SKIP**
- Real Chromium E2E: PASS
- Artifact ID: `14730191774`; size 41,175 bytes
- ZIP SHA-256: `88a725422f3495a82c0dd37242e5c2cf44d5f925763a1523df387dea1873968e`

## Windows Server 2022
- Job ID: `137023329768`
- Contract: 60 PASS
- Safety: 45 PASS
- HTTP API: 52 PASS
- Process containment: 2 PASS
- Host operations: 14 PASS
- V8 acceptance validator: 16 PASS
- Dashboard static contract: **17 PASS**
- Total: **206 PASS / 0 FAIL / 0 SKIP**
- Real Chromium E2E: PASS
- Artifact ID: `14730515415`; size 35,023 bytes
- ZIP SHA-256: `1644d1ce85e6d06a38c404a03e15ff7f7063c15ee21fff467c32c97a3f264948`

## Dashboard test diagnosis and correction

Run #63 failed because GitHub still contained the obsolete 1.7 KB sample dashboard while Sandbox had the secured 20.5 KB operational dashboard. The static test correctly detected missing live-health/input/evidence hooks. The fix was to synchronize the actual Sandbox Dashboard and its README; the test was not weakened.

Run #67 then passed both OS jobs, but the dashboard test printed `PASS` without the two-space prefix expected by the test runner's check counter, so its check count showed 0 despite process exit 0. Co corrected the output format in commit `d6aa3283dec649e57bd51bc47299e3596f39b8ac`. Run #69 confirms **17 Dashboard static assertions PASS on both OSes**.

## Scope and limitations

- This run proves the exact tested GitHub branch commit on hosted Ubuntu 24.04 and Windows Server 2022.
- Dashboard checks are static HTML/JavaScript contract assertions plus Node syntax validation; they do not start the API or perform a live Dashboard/API browser workflow.
- Real Chromium E2E in this workflow exercises the API/runtime test target; it does not replace the separate local Dashboard interaction on Owner's PC.
- Physical Windows 10 PC, production HMAC key provisioning, Linux cgroup-v2 and ROOM-HOP PC Bridge integration remain open.
- CI HMAC key is TEST-ONLY.

## Disposition

- Cross-platform regression including V8 validator and Dashboard static contract: **PASS — RUN 69**.
- Dashboard static contract: **17 PASS on each OS**.
- Live local Dashboard/API: **NOT RUN on Owner PC**.
- Work 10: **ACTIVE — NOT RELEASED**.

**KÝ: Co | AI-07 / End-to-End Architecture & Implementation Lead**
