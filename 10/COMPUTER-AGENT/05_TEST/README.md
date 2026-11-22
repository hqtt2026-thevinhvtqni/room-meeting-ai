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
- `test_windows_launcher_contract.py` has 13 static safety assertions; GitHub Windows CI also parses both PowerShell files with the PowerShell AST parser.


## Recommended Windows operator commands

Run from the Work 10 root in a normal, non-elevated PowerShell session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\05_TEST\START_WORK10_LOCAL.ps1 -PythonPath .\.venv\Scripts\python.exe
```

If dependencies are not installed yet, use `-InstallDependencies` once. Paste the copied token into the Dashboard password field. To stop safely:

```powershell
.\05_TEST\STOP_WORK10_LOCAL.ps1
```

The execution-policy change is process-scoped only and does not persist to the user's account or machine.


## One-command physical Windows 10 acceptance runner — 2026-11-22

`RUN_WORK10_ACCEPTANCE.ps1` is the single-command Owner PC acceptance runner. It requires Windows 10 client + Python 3.12, records OS/Python/Playwright/Chromium/Git identity, hashes accepted source/tests/contracts/schemas, parses the START/STOP scripts, performs the noninteractive launcher start/health/Dashboard/stop smoke, runs `run_all_tests.py` and `e2e_real_browser.py`, and writes a timestamped JSON report plus full logs under `06_EVIDENCE/`.

Run from the Work 10 root:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
./05_TEST/RUN_WORK10_ACCEPTANCE.ps1 -PythonPath ./.venv/Scripts/python.exe
```

Add `-InstallDependencies` if requirements/Chromium are not installed. The report stores only whether a production V8 HMAC key is configured, never the key value. It leaves `release_gate=OPEN`; passing local tests is not final Owner acceptance. It does not enable writes or PowerShell roots. Do not run it while the interactive START_WORK10_LOCAL session is active.


## Acceptance runner contract extension — 2026-11-22

The Windows launcher contract suite now contains 18 static assertions: 13 prior launcher/stop checks plus 5 checks for the one-command Owner acceptance runner. GitHub Windows CI PowerShell AST parsing now includes `RUN_WORK10_ACCEPTANCE.ps1`. The new runner is intended for the physical Windows 10 PC; hosted Windows Server 2022 CI parses its syntax but does not execute it because the runner enforces a Windows 10 client profile. Full CI verification of this latest change is pending.


## Production V8 trust field clarification — 2026-11-22

The acceptance JSON field `production_v8_hmac_env_present` is only a presence check for the environment variable. It does not validate key format, key ID, schema/policy pins, HMAC signature or trust-chain correctness. `production_v8_trust_validation` is explicitly `NOT_RUN`. The secret value is never recorded. Production trust provisioning/validation remains a separate owner-controlled gate.
