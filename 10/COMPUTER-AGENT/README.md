# Work 10 — COMPUTER-AGENT

**Status: ACTIVE — NOT RELEASED.** Owner Vinh has delegated implementation, verification, Sandbox/GitHub reconciliation and handover preparation to Co. No merge to `main`, deployment or production release is authorized.

## Authority and source

- Repository: `hqtt2026-thevinhvtqni/room-meeting-ai`
- Working/canonical Work 10 branch: `work/10-computer-agent-mirror`
- Sandbox Work ID: `10`; root: `COMPUTER-AGENT/`
- Three browser contracts remain LOCKED and unchanged: `ACTION_CONTRACT.md`, `WORKFLOW_CONTRACT.md`, `SAFETY_POLICY.md`.
- PC Host Capability Contract is a separate additive API contract; it does not add browser Action types or alter the three LOCKED contracts.

## Delivered implementation

- Browser automation API: `POST /agent/execute`; browser adapter and observable workflow verification.
- HTTP security: bearer token, exact Origin allow-list, JSON-only requests, 1 MiB body limit, restricted preflight, loopback binding by default.
- Process isolation: `ProcessSupervisor` launches a separate inert `execution_worker.py`; Windows uses Job Object kill-on-close and atomic process assignment before releasing the start gate. The parent enforces a deadline, validates response correlation and confirms containment empty before releasing the host lease.
- PC host API: `POST /agent/host/execute` with `list_directory`, `read_file`, `write_file`, `run_pytest`, `run_powershell_script` and `validate_acceptance_manifest`.
- Host operations use explicit path/script roots. Writes and PowerShell are disabled by default. There is no generic shell or inline PowerShell command.
- V8 acceptance validator: JSON Schema + semantic category policy + expected/observed tuple comparison + runner/source/hash checks + HMAC-signed attestation. Missing or mismatched trust pins/key fail closed.
- Operational Dashboard: live health and browser workflow UI. Static Dashboard contract test is included in the full suite.

## Verified hosted evidence

- Run #49: hosted Windows Server 2022 and Ubuntu 24.04 host-capability API acceptance; Windows PowerShell included. See `06_EVIDENCE/W10_HOST_CAPABILITIES_CI_EVIDENCE_20261122_RUN49.md`.
- Run #52: Windows 189 PASS / 0 FAIL / 0 SKIP; Ubuntu 183 PASS / 0 FAIL / 2 expected SKIP; both ran real Chromium E2E and 16 V8 validator tests. See `06_EVIDENCE/W10_CROSS_PLATFORM_CI_EVIDENCE_20261122_RUN52.md`.
- Run #53: same cross-platform suite after acceptance-validator category/policy hardening; both OS jobs PASS. See `06_EVIDENCE/W10_CROSS_PLATFORM_CI_EVIDENCE_20261122_RUN53.md`.
- The exact run, commit, job IDs, artifact IDs and SHA-256 digests are retained in those evidence files and in the GitHub Actions run history.

## Remaining acceptance gates

| Gate | Current state | What is still needed |
|---|---|---|
| Hosted browser/API/ProcessSupervisor | PASS | Retain evidence; no further claim beyond tested commits |
| Windows Job Object | PASS on hosted Windows Server 2022 | Physical Windows 10 PC verification |
| Host file operations / pytest / PowerShell | PASS on hosted runners | Local PC roots, ACL and service-account review |
| V8 semantic validator | PASS unit/HTTP suite on hosted runners | Provision production key and pins; verify locally |
| Linux containment | LIMITED / NOT RELEASE-ACCEPTED | Implement and test cgroup-v2 production profile |
| Physical Windows 10 PC | NOT RUN | Local install, startup, ACL, Chrome profile, PowerShell and repo-root tests |
| Dashboard / ROOM-HOP PC Bridge integration | OPEN | End-to-end integrated ROOM-HOP evidence |
| Full Sandbox↔GitHub parity | RECONCILIATION IN PROGRESS | Exact inventory and content/hash readback for every accepted file |
| Release | NOT AUTHORIZED | Owner's final acceptance and separate release decision |

Hosted Windows Server 2022 is not the Owner's physical PC. Linux process-group containment is explicitly limited and is not cgroup-v2. CI uses a test-only HMAC key; it is not production trust material. Path allow-lists constrain direct API selection but are not an OS sandbox for approved pytest/PowerShell code; configure only trusted roots/scripts and use a low-privilege service account.

## Local setup and validation

Use `05_TEST/HOST_E2E_RUNBOOK.md` for the full Windows operator procedure. From the Work 10 root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python 05_TEST/run_all_tests.py
python 05_TEST/e2e_real_browser.py
```

The suite writes logs and `06_EVIDENCE/offline-test-evidence.json`. A hosted CI result does not replace the local Windows 10 run. Keep API tokens and production HMAC keys out of source control, URLs, chat, screenshots and evidence logs.

## Handover and release

- Architecture and host API: `03_ARCHITECTURE/PC_HOST_CAPABILITY_CONTRACT.md`.
- Current implementation map: `04_CODE/README.md`.
- Tests and host procedure: `05_TEST/README.md`, `05_TEST/TEST_PLAN.md`, `05_TEST/HOST_E2E_RUNBOOK.md`.
- Evidence: `06_EVIDENCE/`.
- Handover candidate: `07_RELEASE/W10_HANDOVER_PACKAGE_20261122.md` (to be completed after parity and remaining host/integration gates).

**No false PASS. No physical-PC claim without physical-PC evidence. No main merge, deployment or release without Owner approval.**


## Latest hosted regression — 2026-11-22

GitHub Actions Run #69 passed on hosted Windows Server 2022 and Ubuntu 24.04 after the secured Dashboard and static contract suite were synchronized. Windows: 206 PASS / 0 FAIL / 0 SKIP; Ubuntu: 200 PASS / 0 FAIL / 2 expected SKIP. Dashboard static contract 17 PASS per OS; V8 validator 16 PASS per OS; real Chromium E2E PASS. See `06_EVIDENCE/W10_CROSS_PLATFORM_CI_EVIDENCE_20261122_RUN69.md`.

The current owner handover candidate is `07_RELEASE/W10_HANDOVER_PACKAGE_20261122.md`. Work remains ACTIVE — NOT RELEASED pending physical Windows 10, production V8 trust provisioning, Linux cgroup-v2 disposition, ROOM-HOP integration and final inventory dispositions.
