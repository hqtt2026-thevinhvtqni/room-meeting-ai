# Work 10 — COMPUTER-AGENT

**Work status: ACTIVE — NOT RELEASED.** This directory is the Work 10 Sandbox mirror and validation workspace, not the canonical release source.

## Authority and source boundary

- Canonical repository: `hqtt2026-thevinhvtqni/room-meeting-ai`.
- Canonical branch: `work/10-computer-agent-mirror`.
- Protected baseline: `0cad66c59560450d68b06e76a659a6c44104e811`.
- Sandbox Work ID: `10`, root: `COMPUTER-AGENT/`.
- Reconcile GitHub and Sandbox file-by-file under `00_ROOT/SYNC_POLICY.md` before any synchronization. Do not overwrite divergent files or locked contracts.
- `ACTION_CONTRACT.md`, `WORKFLOW_CONTRACT.md`, and `SAFETY_POLICY.md` remain LOCKED.
- No Sandbox-only change is canonical or releasable until exact-source parity, independent review, tests, and owner approval are recorded.

## Current implementation status (2026-11-17)

- Runtime verification semantics: omitted verification invokes Workflow Contract §3.4 minimum fresh-observation check; explicit empty/malformed verification is BLOCKED.
- Screenshot/download evidence paths: source-level containment and filename controls added; Windows path execution remains NOT RUN.
- HTTP API: v1.3.0 Sandbox implementation adds bearer authentication, exact Origin allow-list, restricted preflight, JSON/body-size validation, and a process-wide execution lease. A timed-out worker retains the lease and adapter cleanup is deferred until it exits.
- Important residual risk: the timed-out worker is still not forcibly cancelled. The lease prevents a second HTTP workflow from dispatching and prevents premature adapter close. Runtime now owns one dedicated daemon thread for adapter start/actions/verification/close, addressing the Playwright thread-affinity design; this is not yet host-verified. A permanently stuck worker remains unresolved. Process isolation/cooperative cancellation and host validation are still required.
- Dashboard: token is entered by the operator, kept in page memory only, and sent in the Authorization header. Serve it through the exact allow-listed HTTP origin; do not open as `file://`.
- Current Python/HTTP tests and Chromium E2E: NOT RUN against this Sandbox revision. Test helpers were hardened so a returned boolean `False` is counted as FAIL; historical 101-check/7-check results do not certify current files.
- Desktop, Workforce orchestration, multi-agent coordination, and ROOM-HOP Transcript integration: NOT VERIFIED.
- Production/release authorization: BLOCKED_AUTH.

## Local validation (on an approved host)

From the Work 10 root, use a dedicated virtual environment and install `requirements.txt`.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python 05_TEST/run_all_tests.py
```

The test runner writes `06_EVIDENCE/offline-test-evidence.json` with suite output and source hashes. Do not infer test success from static read-back.

## Local API and Dashboard

Follow `04_CODE/README.md` and `08_DASHBOARD/README.md`. Generate a fresh local token on the operator host, keep it out of source/evidence/chat, bind the API to loopback, and serve the Dashboard from its exact configured Origin.

## Release gates

See `00_ROOT/WORK_MANIFEST.md`, `05_TEST/TEST_PLAN.md`, and `07_RELEASE/README.md`. G0 source parity, G1 runtime lifecycle, G2 current HTTP controls, G3 Windows artifact boundary, G4 exact-source browser E2E, G5–G10 product/integration evidence, and G11 release authorization are not accepted.

**No commit, push, PR, merge, tag, production visibility change, or release was performed.**


## Current execution status — 2026-11-22 (supersedes older process-isolation paragraphs above)

The runtime no longer relies only on a thread-owned adapter worker. Each HTTP workflow is delegated to a separate `execution_worker.py` process through `ProcessSupervisor`. On Windows, the worker is created atomically inside a named Job Object using `PROC_THREAD_ATTRIBUTE_JOB_LIST`; KILL_ON_JOB_CLOSE covers worker/browser descendants. The API owner holds an exclusive host lease, persists owner generation and per-run process journals, enforces a parent deadline, and verifies the containment is empty before releasing request admission. If timeout or uncertain cleanup requires forced termination, the TaskResult is BLOCKED, never PASS.

**Verified milestone:** GitHub Actions #45 passed on hosted Windows Server 2022 and Ubuntu 24.04. Real Chromium E2E was submitted through the HTTP API and process supervisor on both platforms. Windows: 144/144 checks; Linux: 140 PASS + 1 Windows-only SKIP. See `06_EVIDENCE/W10_API_PROCESS_E2E_EVIDENCE_20261122_RUN45.md`.

**Important boundaries:** Linux process-group containment is a LIMITED test profile, not cgroup-v2. The hosted Windows runner is not the Owner's physical Windows 10 PC. The V8 semantic acceptance validator, local PC PowerShell/ACL/Chrome profile validation, file-system/PowerShell/pytest host capability API, ROOM-HOP integration and full source parity remain open. The current LOCKED Action Contract is browser-oriented; no unsupported system-command capability is implied.

API version: **1.4.0**. Work 10 remains ACTIVE — NOT RELEASED. No merge to main, deployment or production release is authorized.


## PC host capability API — version 1.5.0 (implementation in progress)

A separate endpoint is being added without changing the LOCKED browser Action Contract:

- POST /agent/host/execute — list_directory, read_file, write_file, run_pytest, run_powershell_script.
- All host operations run inside the same ProcessSupervisor worker containment as browser workflows.
- Allowed roots are configured with COMPUTER_AGENT_HOST_ALLOWED_ROOTS.
- Writes are disabled unless COMPUTER_AGENT_HOST_WRITABLE_ROOTS is explicitly configured.
- PowerShell is disabled unless COMPUTER_AGENT_HOST_POWERSHELL_ROOTS is explicitly configured; only existing .ps1 files are run through -File.
- Pytest uses the fixed command sys.executable -m pytest -q and allowlisted test paths.
- No arbitrary shell, cmd.exe /c or powershell -Command endpoint exists.

This capability API is not yet release-accepted. Its unit/HTTP/Windows PowerShell tests and physical Windows 10 PC validation must pass before it is marked complete.
