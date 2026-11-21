# WORK 10 — TESTS

Executable contract tests are in test_p0_p5.py.

P0: API/action/verification contract.
P1: browser adapter capability contract.
P2: runtime order + evidence.
P3: integrated real-browser E2E.
P4: dashboard/API integration.
P5: release smoke test.

Real-browser tests must be run on the machine with Chromium/Playwright installed. This workspace records the scripts and evidence; it does not fabricate execution results.


## Dashboard live UI/API smoke test — 2026-11-22

`test_dashboard_live_e2e.py` starts the local Agent API on loopback port 8787 and the standalone Work 10 Dashboard on loopback port 3010. It uses Playwright to verify:
1. cross-origin live health fetch succeeds;
2. health identifies Work ID 10;
3. Execute remains disabled until explicit consent;
4. valid health + token + consent enables Execute;
5. Clear removes the in-memory token;
6. Clear resets consent and disables Execute.

This smoke test does not click Execute and does not run a real workflow. The separate `e2e_real_browser.py` suite verifies the API/runtime browser workflow. Port 3000 remains reserved for W113's shared Dashboard ingress.
