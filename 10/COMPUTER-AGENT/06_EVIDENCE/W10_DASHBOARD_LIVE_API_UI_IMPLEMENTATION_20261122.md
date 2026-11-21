# WORK 10 — DASHBOARD LIVE API UI IMPLEMENTATION

- Work: 10 — COMPUTER-AGENT
- Date-Time: 2026-11-22 05:25 (UTC+07:00)
- Scope: operational UI only; no Agent API/runtime, LOCKED contract, preview data, or release changes.
- Files: `08_DASHBOARD/index.html`, `08_DASHBOARD/README.md`, `05_TEST/test_dashboard_contract.py`, `05_TEST/TEST_PLAN.md`.

## Candidate changes

- Replaced the sample-filled operational form with blank actions/verification fields and an explicit confirmation before a real browser workflow can be submitted.
- The page checks `/health` every 15 seconds and only enables Execute when the API identifies as `computer-agent`, reports `work_id=10`, is fresh, and is not busy. It displays the service/version, execution lease and effective destructive-action flag.
- The page sends the operator token only as a Bearer Authorization header; it does not persist it. It displays the API's status, trace, checks, per-action evidence, verification observation and raw response. Timeout is treated as uncertain and is not automatically retried.
- The runtime `verify` evidence record carries the final observation; the UI uses that record before falling back to action observations.
- The current Agent API has no persistent history/read-only task-list endpoint. The page therefore reports current health and the response from the current tab's workflow only; it does not present preview JSON as live data.

## Verification

- Classification: `STATIC`.
- `python3 05_TEST/test_dashboard_contract.py`: **16 assertions PASS**; inline JavaScript `node --check`: **PASS**.
- Test ran on the local candidate copy in the Manus Sandbox. It did not start or call Agent API, launch a browser adapter, or execute any workflow.
- Candidate SHA-256 on the local LF copy: HTML `3a93c6777526af60478a361d9e868336254023345d9696fa7bb2682c58471bab`; README `a0e4a782e0988d06cee29f8a9524450d6412000b474e1fe64a7b334f95e919b7`; test `fefcf1cf24f3ed7e5e93d51f2f3c4d8723768c5c0be784a5bbf2602ad9ca44fa`.
- Work Sandbox readbacks succeeded. Reported byte sizes match the candidates normalized from LF to CRLF: HTML 20,997 bytes, README 4,296 bytes, test 4,482 bytes. SHA-256 of those CRLF-normalized candidate copies: HTML `84aa7708ed18920b62d8206e343fc94d9ff4152a93110f51afeac395a87ecd75`; README `ff94ddd5d4b7224490fa422d55a2705da4b44eb44d5d8f6c67e6a8b65cb07456`; test `b0251b9100d006687f87c5a4f3a24dfd1a1a2cd71d2b25520d74c2e29170a7cc`. The Work Sandbox read tool exposes content/size but not a direct digest; the normalized hashes above are candidate-copy hashes, not a server-computed attestation.
- Static assertions cover Work 10 identity guard, live endpoint references, explicit run confirmation, busy-state guard, required post-condition, correct verification-observation source, token non-persistence, no seeded sample execution, periodic health check, bounded requests, blank action form, and disabled-by-default Execute.

## Disposition

- Dashboard source/runbook/static check: **IMPLEMENTED**.
- Live Dashboard/API integration (P4): **NOT VERIFIED / NOT RUN**.
- Work 10 release: unchanged; this UI change does not authorize release or alter other blocked gates.
- Next: run the documented startup on the supported Windows machine, confirm `CONNECTED · W10`, then execute one approved, low-risk target/workflow and retain the exact API response and browser evidence. Stop and investigate if health is wrong, origin is rejected, or result is uncertain.


## Candidate correction — 2026-11-22 05:26 UTC+07

- Corrected the Execute-button health guard to normalize `work_id` with `String(...)`, so a valid JSON numeric `10` and string `"10"` are treated consistently. Added a dedicated static assertion.
- Re-run on the local candidate copy `/home/ubuntu/w10_dash_rework/08_DASHBOARD/index.html`: **17 assertions PASS**, including inline JavaScript `node --check`. No API, browser adapter, or workflow was invoked.
- Updated local candidate-copy digests (not server attestations): LF SHA-256 — HTML `7a0f91ada2c33ecaa4f6819070bc7b15109f3ce13ddff296173d28d3ccd2602e`, README `a0e4a782e0988d06cee29f8a9524450d6412000b474e1fe64a7b334f95e919b7`, test `e015f27bda0629e761fa2a28e7d52eedc8585a8d2fc8f0ded0aedc694a5d6878`. CRLF-normalized local candidate-copy SHA-256 — HTML `8f837336ccf08df82c1f46cc07433b4d2339ddbc566b635b285f0e79c578b89e`, README `ff94ddd5d4b7224490fa422d55a2705da4b44eb44d5d8f6c67e6a8b65cb07456`, test `1dd62e9e4e22c6df8d545511a1c852462b22c39511b06a2a3f76fcef7ca257c2`. These hashes identify local candidate copies only; the Work Sandbox read API does not return a digest. The Work update used an appended compatibility guard and matching test assertion, so do not interpret the local direct-edit HTML hash as an exact digest of the Work-resident file.
- Work Sandbox updates were made to the Dashboard, static test, Test Plan, and this evidence note. Readback must confirm the appended changes. The Work-resident static test was not executed in Work Sandbox.
- P4 live browser/API integration remains **NOT RUN / NOT VERIFIED**; Work status and release gates are unchanged.
