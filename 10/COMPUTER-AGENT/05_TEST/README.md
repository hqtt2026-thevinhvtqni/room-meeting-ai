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


## Local launcher / shutdown scripts — 2026-11-22

- `START_WORK10_LOCAL.ps1`: validates Python 3.12 and loopback ports 8787/3010, keeps writes and PowerShell roots disabled, generates a per-session bearer token, starts the Agent API and standalone Dashboard on loopback, checks health/Work ID 10, records process IDs without storing the token, copies the token to clipboard and opens the Dashboard. It never binds port 3000.
- `STOP_WORK10_LOCAL.ps1`: refuses to stop while an execution is active; validates process command line and start time against the session record before stopping only the two Work 10 processes.
- Run `./05_TEST/START_WORK10_LOCAL.ps1` after dependencies are installed, or add `-InstallDependencies` to install requirements and Chromium. Stop with `./05_TEST/STOP_WORK10_LOCAL.ps1`.
- The launcher does not configure production V8 HMAC trust, enable writes or enable PowerShell. Those remain explicit operator actions.
- `test_windows_launcher_contract.py` has 10 static safety assertions; GitHub Windows CI also parses both PowerShell files with the PowerShell AST parser.
