# WORK 10 — TEST PLAN

Revised 2026-10-27; addenda through 2026-11-17. Browser items stay unticked until a host run exists. Historical note: existing [x] markers describe the earlier tested baseline only; current Sandbox v1.3.0 execution is NOT RUN.

## P0 Contract (offline — `test_p0_p5.py`, `test_http.py`)
- [x] `/health` returns service identity, version and effective policy
- [x] unsupported action is rejected (400 over HTTP, BLOCKED inside a workflow)
- [x] type and click remain separate action types
- [x] no fake PASS when the adapter is disconnected; omitted verification invokes the Workflow Contract §3.4 minimum final-observation check
- [x] explicit verification blocks must contain non-empty checks evaluated on the final observation; omission is not a caller-supplied empty block
- [x] minimum verification evidence is recorded; unavailable/empty observation cannot PASS; empty/unavailable observation or a terminal close action must yield BLOCKED (never reopen the browser just to verify).
- [ ] Screenshot path interpretation: bare filename defaults to Evidence; nested relative path must explicitly start with `06_EVIDENCE/`; traversal, look-alike Work-relative path, absolute escape and symlink escape are rejected (execution pending).

## P1 Browser (host required)
- [ ] start/close lifecycle
- [ ] navigate
- [ ] observe
- [ ] click
- [ ] type
- [ ] key_press
- [ ] wait
- [ ] extract
- [ ] screenshot
- [ ] download

## P2 Agent loop (offline)
- [x] action sequence executes in order
- [x] failure stops the sequence
- [x] evidence is recorded with action_id / work_id / timestamp / attempts
- [x] post-condition is verified (final observation by default)
- [x] retry bounded, backoff applied, transient-only
- [x] policy refusals decided before the adapter starts

## P3 Integrated E2E (host required — `e2e_real_browser.py`)
Scenario: open the deterministic local target → inspect → identify target →
click → type → submit → observe → verify result → screenshot → download.

- [ ] PASS recorded only with runtime evidence and post-condition verification
- [ ] `06_EVIDENCE/real-browser-e2e-result.json` + `.png` present

## P4 Dashboard (browser required)
- [x] sends `actions` and `verification` with the task
- [x] renders status, state trace, evidence rows, post-condition results and final observation from the API response
- [ ] verified once against a live API in a real browser

## P5 Release (host required)
- [ ] full suite green on the canonical branch
- [ ] host E2E evidence committed
- [ ] release package + manifest in `07_RELEASE`


## P1 — HTTP transport authorization (added 2026-11-17)
- [ ] Missing bearer token returns 401 before adapter construction.
- [ ] Invalid bearer token returns 401 before adapter construction.
- [ ] Missing or unapproved Origin returns 403 for execute requests.
- [ ] Unapproved preflight returns 403; approved preflight permits only POST with Authorization and Content-Type on /agent/execute.
- [ ] Non-JSON request bodies are rejected; chunked Transfer-Encoding is rejected; non-object JSON returns 400; request body over 1 MiB returns 413.
- [ ] Explicit empty/malformed verification is rejected before adapter construction.
- [ ] Unauthorized/hostile requests do not construct or start the browser adapter.
- [ ] Download filenames containing traversal or Windows ADS/invalid characters are reduced/rejected; resulting file path remains inside Work 06_EVIDENCE.
- [ ] Dashboard sends bearer token only in Authorization header; it is not persisted in browser storage or embedded in source.
- [ ] Dashboard origin exactly matches the configured allow-list; opaque `file://` origin is rejected.

Execution status for this Sandbox revision: NOT RUN. Source write/read-back is not runtime validation.

- [ ] A timed-out adapter call must not be retried while its worker may still be active. Current Sandbox change makes timeout terminal (one attempt); worker cancellation/process isolation and safe adapter cleanup remain an open P0 runtime-lifecycle gate.

- [ ] Real-browser E2E must leave the final in-workflow action as the final observation; adapter close occurs in host cleanup after runtime verification, not before the post-condition check.


## P0 — cross-request timeout containment (added 2026-11-17)
- [ ] Request A times out on a slow adapter action and returns BLOCKED.
- [ ] The timed-out worker remains alive; adapter.close() is deferred until worker termination.
- [ ] Request B during that interval returns 409 execution_busy and does not construct/start a second adapter.
- [ ] The process-wide execution lease is released only after deferred adapter cleanup; a later request can execute.
- [ ] A worker that never terminates leaves the API fail-closed; operator recovery procedure is documented.
- [ ] All test check helpers fail when an assertion callback returns boolean False (not only when it raises).
- [ ] Windows drive, UNC and backslash traversal tests execute on Windows; unsupported symlink creation is reported as SKIP, never PASS.

These cases are implemented in the Sandbox test sources but NOT RUN. A passing fake-adapter regression will still not prove Playwright thread-affinity or browser process isolation.

- [ ] Adapter start, every action, final observation and deferred close execute on one dedicated owner thread; fake-adapter thread-ID regression passes, then repeat with real Playwright/Chromium.

- [ ] Fake-adapter regression confirms start, action, final observation and deferred close run on one dedicated owner thread; repeat with real Playwright/Chromium before G1 acceptance.


## P4 Dashboard live-data implementation addendum — 2026-11-22

- [x] STATIC source checks for the operational UI: `05_TEST/test_dashboard_contract.py` — 16 assertions PASS, including JavaScript syntax (`node --check`) on the candidate copy in the Manus Sandbox.
- [ ] Live `/health` connection from a supported browser to the exact Work 10 API revision — NOT RUN.
- [ ] Approved `POST /agent/execute` workflow in a supported browser, with retained response/evidence — NOT RUN.
- The static test is not a browser/API integration result. P4 remains **NOT VERIFIED** until both live checks above are completed on a pinned candidate. API history is not available; the dashboard displays health and the response for the current in-tab workflow only.


### P4 dashboard candidate correction — 2026-11-22 05:26 UTC+07

This note supersedes the earlier 16-assertion count above. The local candidate was amended to normalize `health.work_id` as `String(...)` in the Execute button guard. Re-run result: **17 static assertions PASS**, including `node --check`, on `/home/ubuntu/w10_dash_rework/08_DASHBOARD/index.html` in the Manus Sandbox. This was not executed inside the Work Sandbox and did not contact Agent API or launch a browser. A matching compatibility guard and assertion were appended to the Work Sandbox Dashboard and test source, respectively; Work readback is required and is not an execution result. Live `/health` and approved `/agent/execute` remain **NOT RUN**; P4 remains **NOT VERIFIED**.


## Current execution and process-containment validation — 2026-11-22

**Latest cross-platform evidence:** GitHub Actions run #45 (`44957836070`, commit `bba3c18fab5b81f02177d002b91eeee0b9db87d5`) completed SUCCESS on Windows Server 2022 and Ubuntu 24.04. Both real Chromium E2E scenarios ran through the HTTP API + isolated worker + ProcessSupervisor and returned PASS after 13 actions and 15 evidence entries.

- [x] Windows hosted-runner HTTP API regression — 37/37 PASS.
- [x] Windows hosted-runner process containment / host owner lease — 2/2 PASS; Job Object KILL_ON_JOB_CLOSE + atomic Job List creation.
- [x] Windows hosted-runner real Chromium E2E through HTTP API — PASS; containment empty verified; forced cleanup false.
- [x] Linux hosted-runner HTTP API regression — 37/37 PASS.
- [x] Linux hosted-runner process-group regression — 2/2 PASS; explicitly LIMITED, not cgroup-v2.
- [x] Linux hosted-runner real Chromium E2E through HTTP API — PASS; containment empty verified.
- [ ] Physical Windows 10 PC: PowerShell startup, filesystem boundary, Chrome profile, ACL and process-tree validation — NOT RUN.
- [ ] Linux cgroup-v2 production containment — NOT IMPLEMENTED; production profile remains fail-closed.
- [ ] V8 semantic acceptance-manifest validator + trusted provenance/category policy + negative suite — OPEN.
- [ ] File-system / PowerShell / pytest host capability contract/API — NOT IMPLEMENTED; do not treat browser-only Action Contract as supporting these operations.
- [ ] Integrated ROOM-HOP Dashboard / PC Bridge E2E — OPEN.
- [ ] Full Sandbox/GitHub source parity and final exact-hash reconciliation — NOT YET RECHECKED after current implementation.

No release gate is closed solely by hosted CI. Work 10 remains ACTIVE — NOT RELEASED.


## PC host capability API — implementation validation pending (2026-11-22)

- [ ] list_directory/read_file within allowlisted roots — HTTP integration test added; CI pending.
- [ ] read_file rejects traversal and symlink escape — unit test added; CI pending.
- [ ] write_file disabled without writable roots; explicit root + overwrite flag + read-back SHA-256 — unit/HTTP tests added; CI pending.
- [ ] run_pytest uses fixed sys.executable -m pytest command and allowlisted paths — unit/HTTP tests added; CI pending.
- [ ] run_powershell_script accepts only allowlisted .ps1 files on Windows — Windows unit/HTTP tests added; CI pending.
- [ ] Host operations run inside ProcessSupervisor and include containment evidence — HTTP tests added; CI pending.
- [ ] Physical Windows 10 PC host operations — NOT RUN.

No generic shell or powershell -Command is exposed. This API is separate from the LOCKED browser Action Contract.


## PC host capability CI disposition — 2026-11-22

- [x] list_directory/read_file within allowlisted roots — Windows/Linux HTTP and unit tests PASS.
- [x] read_file rejects traversal and symlink escape — unit tests PASS.
- [x] write_file disabled by default; explicit root + overwrite flag + read-back SHA-256 — unit/HTTP tests PASS.
- [x] run_pytest fixed command, allowlisted paths, no ambient plugin autoload — Windows/Linux PASS.
- [x] run_powershell_script only allowlisted .ps1 via -File — Windows Server 2022 PASS; Linux correctly BLOCKED.
- [x] Host operations include ProcessSupervisor containment evidence — Windows/Linux HTTP tests PASS.
- [ ] Physical Windows 10 PC host operations — NOT RUN; hosted CI is not a substitute.


## V8 semantic acceptance validator — CI validation pending (2026-11-22)

- [ ] V8 schema validates expected/observed state tuples and rejects caller-supplied consistency_check — tests added.
- [ ] Category/outcome policy permits successful negative tests (e.g. SAFETY verdict PASS with observed REJECTED) and rejects disallowed outcomes — tests added.
- [ ] PASS excludes UNKNOWN lease/owner and requires safe final state — tests added.
- [ ] Fixture and artifact bytes are independently SHA-256 checked; oracle refs must point to verified PRESENT artifacts — tests added.
- [ ] Trusted runner/source identity, validator/schema/policy pinned hashes and HMAC-signed attestation — tests added.
- [ ] Missing key or stale hash pin returns BLOCKED, never PASS — tests added.
- [ ] Host API validate_acceptance_manifest runs inside ProcessSupervisor and writes attestation under writable root — HTTP tests added.
- [ ] Production HMAC key + pins provisioned on Owner's Windows 10 PC — NOT RUN.

CI test key is TEST-ONLY and is not production trust material. No V8 PASS is claimed until the next CI run.


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
