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
| #67 | Dashboard HTML synchronized + static contract suite included | 189 PASS | 183 PASS + 2 SKIP | PASS; dashboard assertion count reporting was corrected in a follow-up |
| #69 | Dashboard assertion count correction | Pending | Pending | IN PROGRESS at handover preparation |

Evidence files:
- `06_EVIDENCE/W10_API_PROCESS_E2E_EVIDENCE_20261122_RUN45.md`
- `06_EVIDENCE/W10_HOST_CAPABILITIES_CI_EVIDENCE_20261122_RUN49.md`
- `06_EVIDENCE/W10_CROSS_PLATFORM_CI_EVIDENCE_20261122_RUN52.md`
- `06_EVIDENCE/W10_CROSS_PLATFORM_CI_EVIDENCE_20261122_RUN53.md`

Run #52 and #53 each execute 16 V8 validator checks successfully on both OS runners. Run #53 tests the additional category catalog, policy ID/version/schema version and category outcome/lease/owner allow-list validation.

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

Follow `05_TEST/HOST_E2E_RUNBOOK.md` on the physical Windows 10 PC. The minimum required evidence is:

- exact Git commit and source/schema/policy SHA-256 values;
- Python/Playwright/Chrome and Windows build inventory;
- `python 05_TEST/run_all_tests.py` full output and generated evidence JSON;
- `python 05_TEST/e2e_real_browser.py` result JSON + screenshot;
- local API health response and approved Dashboard workflow response;
- host `list_directory`, `read_file`, `run_pytest` and (only if explicitly enabled) `write_file` / approved PowerShell script evidence;
- ProcessSupervisor run journal and Windows containment-empty proof;
- V8 attestation + signature verification result, with key redacted;
- local root allow-lists and service-account/ACL disposition.

This session has no direct local PowerShell/desktop executor, so these steps are documented but not claimed as executed.

## 7. Synchronization disposition

- Canonical branch contains the current Work 10 source, test suite, core contracts, PC Host Capability Contract, operational Dashboard and current runbooks.
- The 30 source/test/architecture/config files independently sampled in the current reconciliation pass were exact-match between Sandbox and GitHub after the updates; all three LOCKED contracts are exact-match.
- Current inventory: Sandbox has 156 files under `COMPUTER-AGENT/`; GitHub branch has 59; 59 paths are shared and 97 are Sandbox-only. The Sandbox-only set includes historical/debug records, original/reference files, preview/sample data, generated evidence/lock files and Python cache files. Their KEEP/SANDBOX-ONLY dispositions must be recorded in the final inventory reconciliation; do not bulk-copy caches, locks, preview samples or unreviewed debug packages into the canonical branch.
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

**Full inventory reconciliation:** IN PROGRESS.

**Owner acceptance / release:** PENDING / NOT AUTHORIZED.

Work 10 remains **ACTIVE — NOT RELEASED**. This document is a handover package, not an acceptance certificate.

**KÝ: Co | AI-07 / End-to-End Architecture & Implementation Lead**
