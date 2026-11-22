# WORK 10 — OWNER HANDOVER PACKAGE / ACCEPTANCE CHECKPOINT

- Document ID: W10-HANDOVER-PACKAGE-20261122-01
- Work: 10 — COMPUTER-AGENT
- Owner: Vinh — Project Owner / Final Acceptance Authority
- Implementer: Co — AI-07 / End-to-End Architecture & Implementation Lead
- Date-Time: 2026-11-22 06:31 (UTC+07:00)
- Status: HANDOVER PACKAGE PREPARED — OWNER ACCEPTANCE PENDING
- Authority: Owner delegation `06_EVIDENCE/W10_OWNER_DELEGATION_AND_IMPLEMENTATION_AUTHORIZATION_20261122_01.md`
- Canonical repository: `hqtt2026-thevinhvtqni/room-meeting-ai`
- Canonical Work branch: `work/10-computer-agent-mirror`
- Sandbox Work ID: `10`; root `COMPUTER-AGENT/`

## 1. Purpose and delivered capability

Work 10 delivers a local Computer Agent service intended to operate within explicitly configured PC boundaries:

1. **Browser automation:** navigate, observe, click, type, key press, scroll, wait, extract, screenshot, download and verify post-conditions through the browser Action/Workflow contracts.
2. **PC filesystem:** list directories, read files and optionally write files within explicit allowlisted roots. Writes are disabled by default and require explicit overwrite for existing files.
3. **Pytest:** execute a fixed `python -m pytest -q` command against explicitly allowlisted test paths; arbitrary command flags/shell are not exposed.
4. **PowerShell:** run an existing approved `.ps1` file only, on Windows, within an explicit script root. Inline PowerShell or generic shell execution is not exposed.
5. **Acceptance evidence validation:** validate V8 manifests, recompute semantic state and category/outcome rules, verify fixture/artifact hashes and runner/source pins, then issue an HMAC-signed attestation when trusted configuration is valid.

Host operations use `POST /agent/host/execute`; browser workflows use `POST /agent/execute`. Both share authentication, Origin checks, execution admission, parent deadline and ProcessSupervisor containment.

## 2. Architecture delivered

- `04_CODE/agent_api.py`: loopback HTTP API, bearer authentication, exact Origin allow-list, request size/content validation and single-owner admission.
- `04_CODE/process_supervisor.py`: parent-owned process lifecycle, OS containment, correlation/protocol validation, timeout and cleanup verification, durable run journal and owner lease.
- `04_CODE/execution_worker.py`: inert child worker; application modules and adapters are imported only after parent containment is established and the start gate is released.
- `04_CODE/agent_runtime.py` + `browser_adapter.py`: browser action lifecycle and post-condition verification.
- `04_CODE/host_operations.py`: explicit host capability allow-list for filesystem, pytest, PowerShell and manifest validation.
- `04_CODE/acceptance_validator.py`: V8 schema/semantic validator and signed attestation.
- `08_DASHBOARD/`: operational live-health/browser-workflow UI. It is not a persistent task-history UI and currently does not expose a full host-operation control panel.
- `05_TEST/HOST_E2E_RUNBOOK.md`: local Windows operator procedure.

Three contracts remain LOCKED and unchanged:
- `03_ARCHITECTURE/ACTION_CONTRACT.md`
- `03_ARCHITECTURE/WORKFLOW_CONTRACT.md`
- `03_ARCHITECTURE/SAFETY_POLICY.md`

The separate `PC_HOST_CAPABILITY_CONTRACT.md` adds host operations without changing browser Action types.

## 3. Verified evidence

### Cross-platform CI

| Run | Scope | Windows Server 2022 | Ubuntu 24.04 | Result |
|---|---|---:|---:|---|
| #45 | API + ProcessSupervisor + real Chromium E2E | 144 PASS | 140 PASS + 1 SKIP | PASS |
| #49 | Filesystem + pytest + PowerShell host API | 170 PASS | 164 PASS + 2 SKIP | PASS |
| #52 | Full six-suite regression + V8 validator + Chromium | 189 PASS | 183 PASS + 2 SKIP | PASS |
| #53 | Same after V8 category/policy hardening | 189 PASS | 183 PASS + 2 SKIP | PASS |
| #67 | Dashboard HTML synchronized + static contract suite included | 189 PASS | 183 PASS + 2 SKIP | PASS; initial assertion count display was corrected in a follow-up |
| #69 | Dashboard assertion count correction + full static Dashboard suite | 206 PASS | 200 PASS + 2 SKIP | PASS; 17 Dashboard assertions on each OS |
| #104 | Standalone Dashboard moved to port 3010 | 206 PASS | 200 PASS + 2 SKIP | PASS; preserves shared :3000 ingress |
| #105 | POSIX cleanup polling remediation | 206 PASS | 200 PASS + 2 SKIP | PASS |
| #106 | POSIX cleanup three-cycle descendant stress | 206 PASS | 200 PASS + 2 SKIP | PASS; three-cycle test passed |
| #135 | Live Dashboard/API health + consent smoke | 213 PASS | 207 PASS + 2 SKIP | PASS; 7 live UI assertions per OS |
| #157 | Local launcher PowerShell syntax + start/stop smoke | 224 PASS | 218 PASS + 2 SKIP | PASS; Windows AST + API/Dashboard start/stop smoke |
| #180 | Final launcher token-isolation + HTTP regression | 226 PASS | 220 PASS + 2 SKIP | PASS; 13 launcher checks, Windows AST and start/stop smoke |
| #195 | Latest canonical branch HEAD documentation/evidence sync | 226 PASS | 220 PASS + 2 SKIP | PASS; code unchanged from Run #180 |

Evidence files:
- `06_EVIDENCE/W10_API_PROCESS_E2E_EVIDENCE_20261122_RUN45.md`
- `06_EVIDENCE/W10_HOST_CAPABILITIES_CI_EVIDENCE_20261122_RUN49.md`
- `06_EVIDENCE/W10_CROSS_PLATFORM_CI_EVIDENCE_20261122_RUN52.md`
- `06_EVIDENCE/W10_CROSS_PLATFORM_CI_EVIDENCE_20261122_RUN53.md`
- `06_EVIDENCE/W10_CROSS_PLATFORM_CI_EVIDENCE_20261122_RUN69.md`
- `06_EVIDENCE/W10_CROSS_PLATFORM_CI_EVIDENCE_20261122_RUN104.md`
- `06_EVIDENCE/W10_POSIX_CLEANUP_REMEDIATION_CI_20261122_RUN99_105_106.md`
- `06_EVIDENCE/W10_LIVE_DASHBOARD_API_EVIDENCE_20261122_RUN135.md`
- `06_EVIDENCE/W10_LOCAL_LAUNCHER_CI_EVIDENCE_20261122_RUN157.md`
- `06_EVIDENCE/W10_LOCAL_LAUNCHER_HTTP_CI_EVIDENCE_20261122_RUN180.md`
- `06_EVIDENCE/W10_GITHUB_ACTIONS_CI_EVIDENCE_20261122_RUN195.md`

Runs #52, #53, #69, #104, #105 and #106 each execute 16 V8 validator checks successfully on both OS runners. Run #53 tests the additional category catalog, policy ID/version/schema version and category outcome/lease/owner allow-list validation. Run #69 adds 17 Dashboard static assertions per OS. Run #104 verifies Work 10's standalone UI on port 3010. Runs #105/#106 remediate and stress-test the Linux limited process-group cleanup race first seen in Run #99.

### What hosted CI proves

- Windows Job Object worker/descendant containment on hosted Windows Server 2022.
- API-integrated real Chromium E2E and post-condition verification.
- Host filesystem read/list/write controls, pytest command boundary and Windows allowlisted PowerShell script execution.
- V8 semantic validator behavior, negative cases and HMAC attestation under a test-only CI key.
- Linux process-group containment in a LIMITED profile.

CI evidence is commit-specific. It does not prove local Windows 10 startup, ACLs, Chrome user profile, local PowerShell path behavior or ROOM-HOP PC Bridge integration.

## 4. Current acceptance gates

| Gate | Status | Remaining work |
|---|---|---|
| Browser API + Workflow verification | PASS on hosted CI | Physical Windows 10 live smoke test |
| HTTP auth / Origin / request boundary | PASS on hosted CI | Local browser/API check on Owner PC |
| Windows Job Object containment | PASS on hosted Windows Server 2022 | Verify on physical Windows 10 PC |
| Filesystem / pytest / PowerShell host API | PASS on hosted CI | Local allowlist/ACL/service-account acceptance |
| V8 semantic validator | PASS on hosted CI (16 tests per OS) | Provision production HMAC key and pinned hashes on Owner PC; verify attestation locally |
| Dashboard static contract | Run #67 PASS; assertion count fix in Run #69 pending | Confirm Run #69 and live Dashboard/API workflow on Owner PC |
| Linux production containment | BLOCKED / NOT IMPLEMENTED | Implement cgroup-v2 profile and deterministic delegated-cgroup fixture |
| ROOM-HOP Dashboard / PC Bridge E2E | OPEN | Connect Work 10 API to approved ROOM-HOP PC Bridge/Dashboard integration and capture end-to-end evidence |
| Full Sandbox↔GitHub path parity | PARTIAL / RECONCILIATION IN PROGRESS | Finish file-by-file dispositions for Sandbox-only archival/reference/generated files |
| Release | NOT AUTHORIZED | Owner's final acceptance and separate release approval |

## 5. Security and operating constraints

1. Keep API bound to loopback; do not expose port 8787 publicly or via port forwarding/reverse proxy.
2. Use a fresh bearer token per local session; do not store it in source, URL, chat, logs, browser storage or screenshots.
3. `COMPUTER_AGENT_HOST_ALLOWED_ROOTS` controls direct host path selection. `COMPUTER_AGENT_HOST_WRITABLE_ROOTS` and `COMPUTER_AGENT_HOST_POWERSHELL_ROOTS` default empty.
4. Approved pytest tests and PowerShell scripts execute with the agent service account's privileges. Path allow-lists are not an OS sandbox for code inside those approved scripts/tests. Use a low-privilege service account and only trusted scripts/tests.
5. The V8 CI key is TEST-ONLY. Generate a new production key on the Owner PC; configure validator/schema/policy SHA-256 pins and key ID. Never copy the CI key.
6. If a timeout leaves side-effect completion uncertain, the result is BLOCKED and the execution lease must remain held until containment is confirmed empty.
7. Linux process-group mode is not cgroup-v2 and must not be represented as hardened Linux production containment.
8. No generic shell or arbitrary inline PowerShell endpoint exists.

## 6. Local acceptance procedure for Owner PC

Follow `05_TEST/HOST_E2E_RUNBOOK.md` on the physical Windows 10 PC. The local operator scripts are now ready:

1. Open a normal, non-elevated PowerShell session at the Work 10 root.
2. Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force` (process scope only; not persistent).
3. Run `./05_TEST/START_WORK10_LOCAL.ps1 -PythonPath ./.venv/Scripts/python.exe` (add `-InstallDependencies` only if dependencies/Chromium are not installed). This starts the local Agent API on loopback :8787 and Dashboard on :3010, checks health, creates a session record without the token, copies the per-session token to clipboard and opens the Dashboard.
4. Paste the token into the Dashboard password field. Confirm Work ID 10 and API health. Do not enable write roots or PowerShell roots for the first acceptance pass.
5. Stop the interactive launcher with `./05_TEST/STOP_WORK10_LOCAL.ps1`. It refuses to stop during active execution and validates process command line + start time.
6. With the interactive launcher stopped, run `python 05_TEST/run_all_tests.py` and `python 05_TEST/e2e_real_browser.py`. The test runner starts its own temporary API/Dashboard instances; do not leave the interactive launcher running because it uses the same ports.
7. Retain the full logs, evidence JSON, browser result JSON + screenshot, Windows build/Python/Playwright/Chrome inventory, ProcessSupervisor journal and Job Object containment-empty proof.
8. Keep writable roots and PowerShell roots disabled unless Owner separately approves exact paths and scripts. Production V8 signature acceptance requires provisioning the production HMAC key and exact pins; never paste the key into chat or commit it.

Required evidence:
- exact Git commit and source/schema/policy SHA-256 values;
- Python/Playwright/Chrome and Windows build inventory;
- full test output and generated evidence JSON;
- local API health + Dashboard health/consent smoke;
- Chromium E2E result JSON + screenshot;
- host `list_directory`, `read_file`, `run_pytest`; (only after explicit approval) `write_file` / approved PowerShell evidence;
- ProcessSupervisor run journal and Windows containment-empty proof;
- V8 attestation + signature verification result with key redacted;
- root allow-lists and service-account/ACL disposition.

This ChatGPT session has no direct local PowerShell/desktop executor; the physical Windows 10 procedure is prepared but NOT RUN here.

## 7. Synchronization disposition

- Canonical branch contains the current Work 10 source, test suite, core contracts, PC Host Capability Contract, operational Dashboard and current runbooks.
- The 30 source/test/architecture/config files independently sampled in the current reconciliation pass were exact-match between Sandbox and GitHub after the updates; all three LOCKED contracts are exact-match.
- Current inventory: Sandbox has 171 files under `COMPUTER-AGENT/`; GitHub branch has 79; 79 paths are shared and 92 are Sandbox-only; GitHub-only paths = 0. The 93 Sandbox-only files have explicit KEEP/SANDBOX-ONLY dispositions in `06_EVIDENCE/W10_FULL_PATH_INVENTORY_DISPOSITION_20261122.md`; they include historical/debug records, original/reference files, preview/sample data, generated evidence/lock files and Python caches. Do not bulk-copy caches, locks, preview samples or unreviewed debug packages into the canonical branch.
- No GitHub-only Work 10 file remains in the inventory snapshot.
- Branch history is preserved; no force push, main merge, deployment or release was performed.

## 8. Owner acceptance checklist

- [ ] Confirm the tested branch/commit is the intended Work 10 candidate.
- [ ] Run the local Windows 10 procedure and inspect raw evidence.
- [ ] Approve the local service account, API token handling, filesystem roots, writable roots and PowerShell roots.
- [ ] Confirm production V8 HMAC key and pin provisioning.
- [ ] Decide whether Linux cgroup-v2 and ROOM-HOP integration are required before release or may be accepted as documented limitations.
- [ ] Review the final inventory reconciliation and open-risk register.
- [ ] Issue a separate written acceptance/release decision.

## 9. Final disposition at handover preparation

**Technical implementation:** substantially delivered and cross-platform hosted-CI verified.

**Physical PC acceptance:** NOT YET VERIFIED.

**Linux cgroup-v2:** NOT IMPLEMENTED.

**ROOM-HOP integrated E2E:** OPEN.

**Full inventory reconciliation:** COMPLETE BY EXPLICIT DISPOSITION — 170 Sandbox files; 78 GitHub files; 78 shared paths; 92 Sandbox-only files itemized; 0 GitHub-only paths.

**Owner acceptance / release:** PENDING / NOT AUTHORIZED.

Work 10 remains **ACTIVE — NOT RELEASED**. This document is a handover package, not an acceptance certificate.

**KÝ: Co | AI-07 / End-to-End Architecture & Implementation Lead**


## 10. Latest Dashboard static regression — 2026-11-22 06:31 (UTC+07:00)

Run #69 (ID `44962226803`) completed SUCCESS after the secured operational Dashboard was synchronized and the test-output counter was corrected. Windows Server 2022: 206 PASS / 0 FAIL / 0 SKIP; Ubuntu 24.04: 200 PASS / 0 FAIL / 2 expected SKIP. Dashboard static contract = 17 PASS on each OS; V8 validator = 16 PASS on each OS; real Chromium E2E = PASS. Evidence: `06_EVIDENCE/W10_CROSS_PLATFORM_CI_EVIDENCE_20261122_RUN69.md`.

Run #69 validates static Dashboard invariants and JavaScript syntax; it does not establish a live Dashboard/API workflow on the Owner's physical PC.


## 11. ROOM-HOP integration and shared Dashboard boundary — 2026-11-22 06:35 (UTC+07:00)

The integration handoff is recorded in `06_EVIDENCE/W10_ROOM_HOP_INTEGRATION_BOUNDARY_HANDOFF_20261122.md`.

- Work 10 remains a local loopback-only Computer Agent provider. Its bearer token and Origin allow-list are not a substitute for ROOM-HOP Core authorization.
- Work 24 owns the shared PC Source Bridge/Core authorization/authenticated PC transport boundary. Its current Core/transport seam is fail-closed and not yet wired to the PC. Work 10 is not remotely exposed or called as a bypass.
- Work 112 owns cross-Work contract definitions and integration verification; its baseline remains DRAFT and not approved for runtime enforcement.
- Work 14 remains sole owner of the W12/W13/W14 autonomous E2E product/execution boundary. W10 ProcessSupervisor is only the containment boundary for W10's own agent.
- Work 113 owns the shared ROOM-HOP Dashboard ingress on port `3000`. Work 10's standalone development/acceptance UI has been moved to loopback port `3010`; it must not create a competing listener on port 3000.
- W10 production Dashboard route mounting, W24 authenticated transport integration and W14 capability consumption are NOT IMPLEMENTED / NOT VERIFIED.
- The port-3010 code/test change was validated by Run #104: Windows 206 PASS and Ubuntu 200 PASS + 2 SKIP; see `06_EVIDENCE/W10_CROSS_PLATFORM_CI_EVIDENCE_20261122_RUN104.md`.


## 12. Latest process-cleanup and port-boundary verification — 2026-11-22 06:37 (UTC+07:00)

- Run #104: 200 PASS / 0 FAIL / 2 SKIP on Ubuntu; 206 PASS / 0 FAIL / 0 SKIP on Windows. Confirms standalone Work 10 Dashboard origin/port 3010.
- Run #99 exposed one intermittent Ubuntu limited process-group cleanup failure. Co changed the cleanup path to poll group identity until its bounded deadline and expanded the POSIX descendant test to three cycles.
- Run #105 passed on both OSes after the cleanup implementation patch.
- Run #106 passed on both OSes with the three-cycle POSIX descendant stress test: Ubuntu 200 PASS / 0 FAIL / 2 SKIP; Windows 206 PASS / 0 FAIL / 0 SKIP.
- Evidence: `06_EVIDENCE/W10_POSIX_CLEANUP_REMEDIATION_CI_20261122_RUN99_105_106.md`.
- Linux remains `LIMITED_NOT_CGROUP_V2`; this closes the observed flaky cleanup test, not the hardened Linux production containment gate.


## 13. Owner delegation, review waiver and F-15 status — 2026-11-22 06:39 (UTC+07:00)

- Owner explicitly delegated Co to continue Work 10 through implementation, evidence, Sandbox/GitHub synchronization and handover without waiting for An's V8 review.
- The V8 review task is marked WAIVED BY OWNER. This is not an An review, ACK or approval; none is claimed.
- P0 implementation is authorized to proceed under the Owner's delegation, within the three existing LOCKED contracts. No contract change, main merge, deployment or release is implied.
- F-15 TaskResult/Workflow timeout mapping remains OWNER DECISION REQUIRED. An earlier Biên bản sentence attributing a specific timeout mapping decision to Owner was corrected in the official record. Co will not infer or modify F-15 semantics.
- Work 10 remains ACTIVE — NOT RELEASED pending physical Windows 10 acceptance, production trust configuration, Linux cgroup-v2 disposition, ROOM-HOP integration decisions and final Owner acceptance.


## 14. Live Dashboard/API smoke verification — 2026-11-22

Run #135 (ID `44963956538`) adds a Playwright live smoke test that starts the Work 10 Agent API on loopback :8787 and the standalone Dashboard on :3010. It verifies cross-origin live health, Work ID 10, Execute disabled before consent, enabled after valid health/token/consent, and Clear removing the in-memory token/resetting consent. Seven assertions passed on each OS. The test does not click Execute; real browser workflow remains covered by the separate API/runtime Chromium E2E suite.

- Ubuntu 24.04: 207 PASS / 0 FAIL / 2 expected SKIP.
- Windows Server 2022: 213 PASS / 0 FAIL / 0 SKIP.
- Evidence: `06_EVIDENCE/W10_LIVE_DASHBOARD_API_EVIDENCE_20261122_RUN135.md`.
- Physical Windows 10 live Dashboard/API acceptance remains NOT RUN.


## 15. Local Windows launcher verification — Run #157

The Work 10 local operator launcher and shutdown scripts are now part of the canonical branch:
- `05_TEST/START_WORK10_LOCAL.ps1` starts the API on loopback :8787 and standalone Dashboard on :3010, generates a per-session token, copies it to clipboard in interactive mode, leaves writes/PowerShell disabled, and writes a session record without the token.
- `05_TEST/STOP_WORK10_LOCAL.ps1` refuses to stop during active execution and verifies process command line + start time before stopping only the recorded processes.
- GitHub Windows Server 2022 CI parsed both PowerShell scripts and ran the noninteractive start/health/Dashboard HTTP/stop smoke successfully.
- Windows launcher contract: 11 PASS on each OS runner.
- Run #157 totals: Windows 224 PASS / 0 FAIL / 0 SKIP; Ubuntu 218 PASS / 0 FAIL / 2 expected SKIP.
- Evidence: `06_EVIDENCE/W10_LOCAL_LAUNCHER_CI_EVIDENCE_20261122_RUN157.md`.

The CI smoke intentionally used `-NoClipboard -NoOpenBrowser`; it does not replace Owner's physical Windows 10 user-session/clipboard/Chrome/ACL acceptance.


## 16. Latest final regression — Run #180

- Windows Server 2022: 226 PASS / 0 FAIL / 0 SKIP.
- Ubuntu 24.04: 220 PASS / 0 FAIL / 2 expected SKIP.
- PowerShell AST, local start/stop smoke, Dashboard static 17 checks, Dashboard live 7 checks, V8 validator 16 checks and real Chromium API/runtime E2E all PASS.
- Windows launcher contract: 13 PASS per OS.
- The API token is now cleared from the parent environment before the static Dashboard process starts; the Dashboard server does not inherit the API bearer token.
- Startup failure cleans up only its own processes and removes the session record.
- The oversized HTTP request test now reliably verifies 413 on both OSes without platform-dependent client-side upload abort.
- Evidence: `06_EVIDENCE/W10_LOCAL_LAUNCHER_HTTP_CI_EVIDENCE_20261122_RUN180.md`.


## 17. Latest canonical branch HEAD — Run #195

Run #195 tested current branch HEAD `73b51f61b62d3b1664e8d9d0dd54e979eb5640b1` after the final Manifest/Journal/inventory sync. Both jobs succeeded: Windows 226 PASS / 0 FAIL / 0 SKIP; Ubuntu 220 PASS / 0 FAIL / 2 expected SKIP. Runtime source/tests were unchanged from Run #180; this confirms the latest documentation/evidence HEAD remains green. Evidence: `06_EVIDENCE/W10_GITHUB_ACTIONS_CI_EVIDENCE_20261122_RUN195.md`.


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


## 18. One-command physical Windows 10 acceptance runner — 2026-11-22

Added `05_TEST/RUN_WORK10_ACCEPTANCE.ps1`. It is gated to a Windows 10 client, validates Python 3.12 and Playwright/Chromium, parses START/STOP PowerShell scripts, runs the noninteractive launcher smoke, executes the complete Python regression suite and real Chromium E2E, hashes accepted source/tests/contracts/schemas, and writes a timestamped JSON report plus full logs under `06_EVIDENCE/`. It records only whether a production V8 HMAC key is configured, never the key value. The report keeps `release_gate=OPEN`; local test PASS is not release acceptance.

Run from Work 10 root:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
./05_TEST/RUN_WORK10_ACCEPTANCE.ps1 -PythonPath ./.venv/Scripts/python.exe
```

Add `-InstallDependencies` if needed. Do not run while the interactive START_WORK10_LOCAL session is active. The runner has not yet been executed on Owner's physical Windows 10 PC; CI PowerShell AST verification is pending.


## Production V8 trust field clarification — 2026-11-22

The acceptance JSON field `production_v8_hmac_env_present` is only a presence check for the environment variable. It does not validate key format, key ID, schema/policy pins, HMAC signature or trust-chain correctness. `production_v8_trust_validation` is explicitly `NOT_RUN`. The secret value is never recorded. Production trust provisioning/validation remains a separate owner-controlled gate.
