# WORK 10 — COMPUTER AGENT

Work ID: 10
Name: COMPUTER-AGENT

## Decision 2026-10-04
Build from specification instead of porting the original HTML. Existing HTML is retained as reference/mock only.

## Specification Lock (2026-10-04) — unchanged
1. **ACTION_CONTRACT.md** — LOCKED — click ≠ type | Unknown → REJECT | Observable result required
2. **WORKFLOW_CONTRACT.md** — LOCKED — PLANNED → RUNNING → VERIFYING → PASS/FAIL/BLOCKED
3. **SAFETY_POLICY.md** — LOCKED — retry/timeout limits, destructive allow, boundary for screenshot/extract/download
4. **OFFLINE_TEST_MATRIX.md** — revised 2026-10-27 to match enforced behaviour

## Remediation 2026-10-27 (gates 0–4)

| Gate | Scope | Status |
|---|---|---|
| 0 | Canonical source identified and compared (repo `hqtt2026-thevinhvtqni/Computer-Agent`) | **DONE (read-only)** — `work/10-computer-agent-mirror` never existed; canonical is `main` @ `b8520f2d`. 12/26 shared files byte-identical, 14 differ = the remediation set. Evidence: `06_EVIDENCE/CANONICAL_VERIFICATION_2026-10-27.md` |
| 1 | Safety Policy enforced in code; false-PASS paths closed; negative tests | **DONE (offline)** |
| 2 | `browser_e2e_target.html` added; contract/action mismatches fixed; adapter closed in `finally`; HTTP tests | **DONE (offline)** — real Chromium run still required |
| 3 | Dashboard sends `actions` + `verification`, renders status/evidence from the runtime | **DONE (code)** — not yet verified in a real browser |
| 4 | Suite runner + JSON evidence in `06_EVIDENCE` | **DONE (offline)** — CI on canonical + host E2E outstanding |

### Gate 0 facts (verified against GitHub, 2026-10-27)
- Branches: `main` = `b8520f2dab13b56ed2b0e97160d80256ebe9e7af` (2026-10-21T22:50:18Z), `work-10-sandbox-handoff-20261006` = `4138a03`, `work-10-computer-agent-2713f` = `a754d388` (a different React/TS project, not this runtime). No tags.
- `main`'s tree (`a94f45d7`) equals the handoff branch's tree — `main` is only a promotion of it.
- The commits `SYNC_POLICY.md` v1.0 cited (`0958c72…` on main, `c3a465e`) do not exist in any ref.
- Canonical `04_CODE` has no `SafetyPolicy` (models.py 73 lines); running it reproduces the false PASS: no verification block → PASS, `checks: []` → PASS, and verification scans all evidence rather than the final observation.
- Canonical already contains `05_TEST/browser_e2e_target.html`, `05_TEST/e2e_real_browser.py`, the CI workflow and `requirements.txt` — the earlier "missing target HTML" finding was true of the Sandbox copy, not of `main`.
- Canonical `test_p0_p5.py` runs 35 PASS / 0 FAIL; it is not compatible with the stricter proposal (a workflow without `verification` is now BLOCKED).

### What was enforced in code
- `models.py`: `SafetyPolicy` (retry ≤2, backoff ≥500 ms, action/wait/observation/workflow timeouts, destructive allow, path + domain boundary) and required-field rules for `wait`, `scroll`, `extract`.
- `agent_runtime.py`: pre-flight policy review before the adapter starts; per-action retry with transient-only classification; thread-based timeout enforcement; workflow deadline; policy violations → BLOCKED with the rule name in evidence.
- `verify()`: verification block is mandatory and must be non-empty; checks read the **final** observation by default (`scope: "final"`, opt-in `scope: "any"`).
- `agent_api.py`: adapter factory (testable), adapter always closed in `finally`, request validation, server-side-only destructive permission.
- Evidence entries now carry `action_id`, `work_id`, ISO-8601 UTC `timestamp`, `attempts`, `timeout_seconds`, `duration_ms`, `destructive`; `TaskResult` carries `started_at`/`finished_at`/`policy`.

### Verification actually run
- `python 05_TEST/run_all_tests.py` → 3 suites, **101 checks passed, 0 failed**, host Chromium E2E `NOT RUN`; evidence written to `06_EVIDENCE/offline-test-evidence.json`.
- The same suite also passes on a clean clone of canonical `main` with the proposal applied (proposal branch `work/10-computer-agent-mirror-proposal`, 21 files, +2321/−659).
- Witness is the offline/HTTP scope only. No Chromium, no integrated ROOM-HOP E2E, no real-browser dashboard check.

## Evidence rule
No fake PASS. P3/P5 may only be recorded PASS after a real run on a host with Chromium/Playwright and evidence present in `06_EVIDENCE`.

## Current status
SOURCE: canonical identified = `main` @ `b8520f2d`; Sandbox = canonical + unmerged remediation proposal
SPECIFICATION: LOCKED
SAFETY POLICY: LOCKED + ENFORCED IN CODE (negative tests pass)
VERIFICATION RULE: PASS requires a confirmed post-condition
OFFLINE + HTTP TESTS: 101/101 PASS (this sandbox)
CI RE-VERIFY: PENDING (proposal branch not pushed)
HOST E2E: NOT YET VERIFIED
DASHBOARD P4: IMPLEMENTED, NOT BROWSER-VERIFIED
RELEASE: NOT READY

## Next gate
1. Review the proposal patch and open a branch + PR off `main`; run CI on it.
2. Run `python 05_TEST/e2e_real_browser.py` on a host with Chromium; commit the JSON + PNG evidence.
3. Open the dashboard against a running API once; only then mark P4 verified.
4. Qe review, then release decision.


## Structure addendum — 2026-10-28 (Xu)
- Added the Work structure standard at `00_ROOT/WORK_STRUCTURE_STANDARD.md`.
- Added Work-specific dashboard preview at `09_DASHBOARD_PREVIEW/`; preview data is visibly labelled sample-only and must not be treated as live verification.
- Added AI debug handoff lifecycle at `10_AI_DEBUG_HANDOFF/` with inbox, review, patch candidates, validation, and decisions.
- Preserved the existing operational dashboard `08_DASHBOARD/` and generic root `preview/`; neither was overwritten.
- Copied Cla CTO's complete available Sandbox debug package into immutable intake folder `10_AI_DEBUG_HANDOFF/00_INBOX/CLA_CTO/20261028_run01/`: DEBUG_REPORT.md, RUN_LOGS.md, proposed_patch.diff, test_prevention_timeout_boundary.py, desktop.ini. The package is proposal-only; no production source changed.
- Verification: all writes returned status=ok; readback verification pending.
- Work status remains ACTIVE / VERIFICATION PENDING / NOT RELEASED. No commit/push/merge/release.


## Verification semantics addendum — 2026-11-17 (Ka)
- Authority remains the LOCKED Workflow Contract §3.4: when the verification block is omitted, Runtime enters VERIFYING and performs the minimum observation-exists check. Omission is not equivalent to a caller-supplied empty block.
- An explicitly supplied empty or malformed verification block is rejected as BLOCKED before the adapter starts.
- The minimum check passes only with a non-empty fresh post-action observation. An unavailable/empty observation, timeout, or a terminal final `close` action is BLOCKED; the runtime must not lazily reopen a closed browser to manufacture an observation.
- This supersedes older explanatory statements in this manifest and the 2026-10-27 matrix that said a missing verification block itself is BLOCKED. Those statements remain historical records, not current runtime semantics.
- Sandbox implementation and tests were statically written/read back on 2026-11-17; latest Python tests have NOT RUN. Historical 101/101 results do not certify this revision.
- Overall remains ACTIVE — NOT RELEASED; G0/G3 remain blocked pending exact candidate parity and Windows execution evidence.


## Addendum — P1 HTTP transport boundary (2026-11-17)
The local Agent API now has a Sandbox implementation for bearer authentication, exact Origin allow-listing, restricted CORS preflight, JSON-only execute requests, and a 1 MiB request-body cap. Dashboard token entry is operator-controlled and memory-only. This is a source-level remediation only: HTTP regression tests, browser CSRF validation, and exact-origin Dashboard integration remain NOT RUN until a supported execution host is available. Do not treat this addendum as release authorization. Work 10 remains ACTIVE — NOT RELEASED.


## Current execution status superseding historical gate tables — 2026-11-17

The 2026-10-27 gate table and 101/101 offline result above are historical evidence only. They do not certify the current Sandbox source revision. For current provenance, apply SYNC_POLICY v1.2 and the 2026-11-17 Candidate source parity report; do not rely on the older repository/branch summary above as current source identity.

| Gate | Current disposition | Evidence / missing proof |
|---|---|---|
| G0 — provenance/source parity | BLOCKED | Candidate branch work/10-computer-workforce-p0-candidate at d7cd86e25d012efd4d1cef70cf7acd5f34003248 was inspected read-only; Candidate has not received Sandbox fixes. |
| G1 — runtime safety | BLOCKED | Verification-default and timeout/path changes are statically present; current Python suite NOT RUN. A timed-out worker is not forcibly cancelled; retries are suppressed, API keeps a process-wide execution lease, rejects cross-request dispatch with 409, and defers adapter.close() until worker exit. Runtime now serializes adapter start/actions/verification/close on one dedicated daemon owner thread, but Playwright behavior has not been host-tested and a permanently stuck worker still holds the lease indefinitely; process-level recovery and host execution evidence remain required. |
| G2 — HTTP transport | BLOCKED pending tests | New v1.3.0 bearer/Origin/CORS/body-limit controls and process-wide execution lease and regression tests written; execution NOT RUN. Historical 7/7 covers only its former scope. |
| G3 — artifact boundary | BLOCKED | Screenshot containment and download-to-Evidence implementation/tests present; Windows drive, UNC, junction/symlink and direct-adapter tests NOT RUN. |
| G4 — Chromium | PARTIAL / historical scenario only | Prior 14-step owner-reported E2E is not bound to current Sandbox or Candidate exact HEAD. |
| G5 — Desktop | NOT VERIFIED | No current host execution evidence. |
| G6 — Workforce lifecycle | NOT VERIFIED | No end-to-end lifecycle evidence. |
| G7 — orchestration | NOT VERIFIED | No multi-task orchestration evidence. |
| G8 — multi-agent | NOT VERIFIED | No independent multi-agent execution evidence. |
| G9 — evidence/audit | PARTIAL | Static evidence and journals updated; durable runtime evidence for current source NOT RUN. |
| G10 — ROOM-HOP integration | NOT VERIFIED | No current integrated transcript/API execution evidence. |
| G11 — production/release authorization | BLOCKED_AUTH | No release authorization. |

**Current overall status: ACTIVE — NOT RELEASED.** Sandbox static remediation may continue, but no release gate is promoted without exact-source execution evidence and source-governance approval. No GitHub write, commit, push, PR, merge or release was performed.


## Addendum — P0 cross-request timeout containment (2026-11-17)
Sandbox API v1.3.0 now serializes execute requests with a process-wide non-blocking lease. When Runtime reports a timed-out worker, the API retains that lease, returns BLOCKED, rejects subsequent execute requests with 409 execution_busy, and defers adapter.close() until the timed-out worker exits. Runtime classifies ActionTimeout as BLOCKED and retains the worker reference for the host. HTTP regression tests model request A timing out, request B being rejected without adapter construction, cleanup after worker termination, and later recovery. Test helpers now treat a returned boolean False as FAIL rather than silently printing PASS.

This is a source-level containment measure, not cancellation. It does not prove Playwright sync API thread-affinity, process crash recovery, or safety if a worker never terminates. Tests remain NOT RUN. G1 remains BLOCKED.


## Addendum — API pre-adapter validation (2026-11-17)
Agent API v1.3.0 now validates the verification block before acquiring the execution lease or constructing an adapter; explicit empty/malformed checks return 409 BLOCKED without starting a browser. Chunked Transfer-Encoding is rejected rather than leaving an unbounded/unread body on the request stream. HTTP negative regression cases were added. All remain NOT RUN pending a host test.


## Addendum — dedicated adapter owner thread (2026-11-17)
Runtime now routes adapter start, every action, final observation and close through one dedicated daemon owner thread. This removes the prior design's per-action thread switching at source level and aligns with Playwright Sync API thread affinity. HTTP cleanup waits for a timed-out Future and queues close on that same owner thread before releasing the process-wide lease. A fake-adapter regression captures thread IDs across start, timed-out action and deferred close. This is not a Playwright host PASS; the worker remains non-cancellable and a permanently stuck call holds the lease. G1 remains BLOCKED pending host execution and recovery validation.


## Addendum — AN independent V7 review received (2026-11-19)

Recorded by Co on 2026-11-22 04:49 (UTC+07:00): the independent review is COMPLETE, not pending. Source: `10_AI_DEBUG_HANDOFF/03_VALIDATION/AN_P0_DESIGN_REVIEW_RESULT_20261119_07.md`.

An's static adversarial review leaves AN-V7-F01 through AN-V7-F04 OPEN/BLOCKED: caller-authored consistency flags are not trusted proof; PASS must exclude UNKNOWN lease/owner states using category-aware semantics; category-disallowed outcomes and forged flags need explicit negative cases; and schema/semantic validator execution evidence is absent. AN-V6-F01..F03 are NOT READY TO CLOSE; F04 remains PARTIAL/BLOCKED. P0 implementation remains BLOCKED / NOT AUTHORIZED and release remains NOT AUTHORIZED. Next: Ka/Co revise the design and negative catalogue, then request An re-review; any executable validator task remains separate from P0 runtime implementation and requires an approved execution host.


## Addendum — V8 P0 design response prepared (2026-11-22 04:49 UTC+07:00)
Co prepared `06_EVIDENCE/W10_P0_ACCEPTANCE_INTEGRITY_AMENDMENT_20261122_08.md` in response to An's AN-V7-F01..F04 findings and created the independent review task `10_AI_DEBUG_HANDOFF/03_VALIDATION/AN_P0_DESIGN_REVIEW_TASK_20261122_08.md`. Both are design/handoff artifacts only. V8 proposes trusted-runner validator provenance, recomputed consistency checks, non-UNKNOWN lease/owner states for PASS, a versioned category/outcome policy and expanded negative cases. An review is requested but not yet acknowledged. No V8 schema, validator, runtime source, tests, configuration or LOCKED contracts were changed. P0 remains BLOCKED / NOT AUTHORIZED; Work 10 ACTIVE — NOT RELEASED.


## Addendum — GitHub Actions Run 26 evidence (2026-11-22)
GitHub Actions workflow `Work 10 Real Browser E2E` completed SUCCESS for exact commit `cd423e5fe304775162b74577523457150fa3a016` on `work/10-computer-agent-mirror`. Job `real-browser` passed syntax check, offline contract tests (log: `Offline contract tests: ALL PASSED`) and real Chromium E2E (result `status: PASS`, state trace PLANNED → RUNNING → VERIFYING → PASS). Evidence: `06_EVIDENCE/W10_GITHUB_ACTIONS_CI_EVIDENCE_20261122_RUN26.md`; run ID 44953668873; artifact ID 14726835944; artifact SHA-256 `1f02e24c6e475692d758908a8125000b2c10225f792de1643d6c4ea1cddd6d99`. This certifies the GitHub branch source at that exact commit on Ubuntu 24.04 only. It does not certify divergent Sandbox source, Windows PC execution, P0 process isolation, V7/V8 validator or ROOM-HOP integration. Work 10 remains ACTIVE — NOT RELEASED.


## Owner delegation and implementation authority — 2026-11-22
- Owner Vinh delegated Co to continue Work 10 through implementation, verification, reconciliation and handover for acceptance; see `06_EVIDENCE/W10_OWNER_DELEGATION_AND_IMPLEMENTATION_AUTHORIZATION_20261122_01.md`.
- An V8 review/ACK is not a prerequisite and is removed from the critical path. Historical An findings remain immutable evidence and are not represented as reviewed/closed.
- P0 implementation is now OWNER-AUTHORIZED within this scope. This authorization does not make implementation or host tests PASS.
- F-15 is interpreted conservatively under the existing locked Safety Policy §3: single-action timeout => ActionResult failure; workflow deadline => TaskResult BLOCKED; uncertain continuing side effects => BLOCKED with execution lease held until containment/cleanup proof; TaskResult FAIL only after known termination/failure.
- Three contracts remain LOCKED and read-only. No main merge, production deployment or release without separate Owner acceptance.
- Execution target: Linux + Windows GitHub Actions with retained evidence; local physical PC remains separately unverified unless directly exercised.


## Current execution status superseding historical gate summaries — 2026-11-22 05:40 (UTC+07:00)

**Owner authorization:** `06_EVIDENCE/W10_OWNER_DELEGATION_AND_IMPLEMENTATION_AUTHORIZATION_20261122_01.md` records Vinh's explicit delegation to Co to continue implementation through evidence-backed handover. An V8 review/ACK is not a prerequisite. Historical V7/V8 reports remain immutable.

**Implemented and verified on GitHub branch `work/10-computer-agent-mirror`:**
- Agent API now delegates each workflow to an isolated `execution_worker.py` process managed by `ProcessSupervisor`.
- Windows worker is created atomically inside a named Job Object through `CreateProcessW` + `PROC_THREAD_ATTRIBUTE_JOB_LIST`; Job Object uses KILL_ON_JOB_CLOSE; parent owns deadline and verifies active-process count reaches zero before releasing request admission.
- HostOwnerLease provides an exclusive OS file lock and monotonic owner generation; per-run JSON journals persist owner generation, containment locator, PID and state transitions; startup recovery is fail-closed when identity/containment cannot be reconciled.
- Timeout semantics implement F-15 conservatively: ActionResult fail + outcome_uncertain; enclosing TaskResult BLOCKED; forced cleanup never becomes PASS.
- CI #45 (run ID `44957836070`, commit `bba3c18fab5b81f02177d002b91eeee0b9db87d5`) passed on Windows Server 2022 and Ubuntu 24.04. Both real Chromium E2E scenarios ran through HTTP API + ProcessSupervisor and passed. Evidence: `06_EVIDENCE/W10_API_PROCESS_E2E_EVIDENCE_20261122_RUN45.md`.

| Gate | Current disposition | Evidence / limitation |
|---|---|---|
| P0 Windows Job Object execution path | PASS on hosted Windows Server 2022 | Atomic Job List worker creation; HTTP + Chromium E2E; 144/144 checks |
| P0 Linux execution path | PASS — LIMITED profile only | POSIX process group; 140 PASS / 1 Windows-only SKIP; not cgroup-v2 |
| P0 V8 semantic acceptance validator | OPEN / NOT IMPLEMENTED | Trusted provenance, category/outcome policy and negative validator suite remain |
| P1 HTTP security boundary | PASS on hosted Windows + Linux CI | Bearer auth, exact Origin, request size/content validation, execution lease |
| Real Chromium E2E through API | PASS on hosted Windows + Linux | 13 actions, 15 evidence entries, screenshots retained in run artifacts |
| Physical Windows 10 PC validation | NOT RUN | Hosted Windows Server is not Owner's PC; PowerShell/ACL/Chrome profile/local install still required |
| File-system / PowerShell / pytest host capabilities | NOT IMPLEMENTED | Current locked Action Contract remains browser-oriented; separate capability contract/API required |
| ROOM-HOP Dashboard / PC Bridge integration | OPEN | No integrated ROOM-HOP end-to-end evidence yet |
| Full Sandbox↔GitHub source parity | NOT YET RECHECKED | Reconcile all accepted source/test/config files and exact hashes after current implementation |
| Main merge / release | NOT AUTHORIZED | Owner retains final acceptance and release authority |

Three LOCKED contracts (`ACTION_CONTRACT.md`, `WORKFLOW_CONTRACT.md`, `SAFETY_POLICY.md`) remain unchanged. Work 10 remains ACTIVE — NOT RELEASED.

**KÝ: Co | AI-07 / End-to-End Architecture & Implementation Lead**


## PC host capabilities — 2026-11-22 05:45 (UTC+07:00)

Co has added a separate, non-Action-Contract host capability surface:
- New architecture contract: 03_ARCHITECTURE/PC_HOST_CAPABILITY_CONTRACT.md.
- New module: 04_CODE/host_operations.py.
- New endpoint: POST /agent/host/execute, delegated to the same ProcessSupervisor worker.
- Operations: list_directory, read_file, write_file (explicit writable roots + read-back/hash), run_pytest (fixed Python module command), run_powershell_script (existing allowlisted .ps1 only; Windows only).
- Default is read-only: writable roots and PowerShell roots are empty unless operator explicitly configures them. No generic shell or inline PowerShell command is exposed.
- New unit/HTTP tests are being added. CI validation is pending; this is not yet a PASS or release acceptance.

API version advanced to 1.5.0 in Sandbox. Three LOCKED contracts remain unchanged. Work 10 remains ACTIVE — NOT RELEASED.

**KÝ: Co | AI-07 / End-to-End Architecture & Implementation Lead**


## PC host capability acceptance update — 2026-11-22 05:52 (UTC+07:00)

GitHub Actions #49 (run ID 44958804750, commit c11319e26bc6578baaf71e664152c259ee0c1e37) proves the separate PC host capability API on hosted CI:
- Windows Server 2022: 170 PASS / 0 FAIL / 0 SKIP; file list/read/write, traversal/symlink rejection, pytest and allowlisted PowerShell .ps1 all PASS.
- Ubuntu 24.04: 164 PASS / 0 FAIL / 2 expected SKIP; file list/read/write, traversal/symlink rejection and pytest PASS; PowerShell correctly blocked on non-Windows.
- Both platforms' real Chromium E2E and ProcessSupervisor tests PASS.
- Detailed evidence: 06_EVIDENCE/W10_HOST_CAPABILITIES_CI_EVIDENCE_20261122_RUN49.md.

| Gate | Current disposition | Boundary |
|---|---|---|
| Browser HTTP API + real Chromium | PASS — hosted Windows/Linux | Not yet ROOM-HOP integrated |
| Windows Job Object worker containment | PASS — hosted Windows Server 2022 | Physical Windows 10 still NOT RUN |
| File-system host operations | PASS — hosted Windows/Linux | Explicit roots; direct API path allow-list only, not OS sandbox |
| Pytest host execution | PASS — hosted Windows/Linux | Fixed command, allowlisted paths, plugin autoload disabled |
| PowerShell host execution | PASS — hosted Windows Server 2022 | Allowlisted .ps1 only; disabled by default |
| Linux cgroup-v2 production containment | OPEN / NOT IMPLEMENTED | Current Linux profile remains LIMITED process group |
| V8 semantic acceptance validator | OPEN / NOT IMPLEMENTED | Trusted runner attestation and negative suite outstanding |
| Physical Windows 10 PC validation | NOT RUN | Local install, ACL, Chrome profile, PowerShell and repo-root tests outstanding |
| ROOM-HOP Dashboard / PC Bridge E2E | OPEN | No integrated evidence yet |
| Full Sandbox↔GitHub source parity | NOT YET RECHECKED | Exact hashes/inventory still required |

Work 10 remains ACTIVE — NOT RELEASED. No main merge or production release is authorized.

**KÝ: Co | AI-07 / End-to-End Architecture & Implementation Lead**


## V8 acceptance validator implementation — 2026-11-22 06:00 (UTC+07:00)

Co has begun implementing the V8 integrity design without waiting for An review, under the Owner's delegation. New artifacts in Sandbox:
- 06_EVIDENCE/W10_P0_ACCEPTANCE_MANIFEST_V8.schema.json — removes caller consistency flags; PASS schema excludes UNKNOWN lease/owner and requires safe final state.
- 06_EVIDENCE/W10_P0_CATEGORY_OUTCOME_POLICY_V8.json — category-specific PASS outcome, lease and owner policy.
- 06_EVIDENCE/W10_P0_VALIDATOR_ATTESTATION_V1.schema.json — signed validator output schema.
- 04_CODE/acceptance_validator.py — JSON Schema + semantic validator; verifies exact state tuple, category outcome, host/source provenance, fixture/artifact bytes and HMAC signature.
- 05_TEST/test_acceptance_validator.py — adversarial tests for forged flags, mismatched states, UNKNOWN states, disallowed outcomes, hash substitution, oracle refs, runner/source forgery, missing key and stale validator pins.
- Host API operation validate_acceptance_manifest is routed through ProcessSupervisor; health reports validator_ready.

Trust boundary: production validator returns BLOCKED unless validator/schema/policy hashes, source commit, key ID and a protected HMAC key are provisioned. CI uses a TEST-ONLY key and cannot be treated as production trust configuration. This implementation is written but has NOT yet passed CI. P0 validator remains OPEN pending execution evidence and local key provisioning.

**KÝ: Co | AI-07 / End-to-End Architecture & Implementation Lead**


## W10-CI-RUN52-20261122-01 — 2026-11-22 06:10 (UTC+07:00)

Co | AI-07 / End-to-End Architecture & Implementation Lead. Đã kiểm tra GitHub Actions Run #52 (ID `44959557526`), branch `work/10-computer-agent-mirror`, tested commit `843a532d2c08bc4bbd404fcd165ff5d619c130f6`. Cả hai matrix job SUCCESS. Ubuntu 24.04: 183 PASS / 0 FAIL / 2 SKIP; Windows Server 2022: 189 PASS / 0 FAIL / 0 SKIP. Mỗi OS chạy V8 acceptance validator 16 PASS, real Chromium E2E PASS, HTTP API, process containment và host operations suites PASS. Windows evidence xác nhận Job Object profile và 0 active processes after cleanup; Linux vẫn profile LIMITED_NOT_CGROUP_V2. Artifacts: Linux ID `14728674665`, ZIP SHA-256 `2d6338874ff0977c9e47a51e5a21bfbc87b45a159e90a288558b11a070b79b75`; Windows ID `14729430156`, ZIP SHA-256 `7cd16b4fdda217a9d4b1bdcba37b4d30a822891b1ebbd7859ea393d0921099a2`. Run #51 predecessor failed in http_api and acceptance_validator subprocesses; detailed stderr was not present in job summary, so no root cause inferred. Evidence file: `06_EVIDENCE/W10_CROSS_PLATFORM_CI_EVIDENCE_20261122_RUN52.md`. Run #52 does not cover physical Windows 10 PC, production HMAC key provisioning, Linux cgroup-v2, or ROOM-HOP integration.

## W10-SOURCE-PARITY-HARDENING-20261122-01 — 2026-11-22 06:10 (UTC+07:00)

Co đã so sánh 31 tệp source/test/architecture/config hiện có trong Sandbox với nhánh GitHub. ACTION_CONTRACT, WORKFLOW_CONTRACT, SAFETY_POLICY và PC_HOST_CAPABILITY_CONTRACT exact match. Các module runtime/host/process và test chính exact match; phát hiện duy nhất trong nhóm source/test là Sandbox `04_CODE/acceptance_validator.py` có thêm kiểm tra allowlist đầy đủ category + policy_id/version/schema_version + allowed outcome/lease/owner enums so với GitHub. Đã đồng bộ đúng tệp này lên GitHub commit `29daa718509b1c3906527a8cd9358104061e3b85`. Cross-platform CI Run #53 đang chạy trên commit này tại thời điểm ghi. Full inventory/parity chưa chốt; tiếp tục kiểm tra các tệp evidence/docs khác.

## W10-CI-RUN53-PENDING-20261122-01 — 2026-11-22 06:10 (UTC+07:00)

Sau commit `29daa718509b1c3906527a8cd9358104061e3b85`, GitHub Actions Run #53 (ID `44960863874`) được kích hoạt, workflow Cross-Platform Verification. Trạng thái tại thời điểm ghi: IN_PROGRESS. Không ghi nhận PASS trước khi cả Windows và Linux jobs hoàn tất.


## W10-CI-RUN53-20261122-01 — 2026-11-22 06:10 (UTC+07:00)

Co | AI-07 / End-to-End Architecture & Implementation Lead. Run #53 (ID `44960863874`) on exact commit `29daa718509b1c3906527a8cd9358104061e3b85` completed SUCCESS on Ubuntu 24.04 and Windows Server 2022. Ubuntu: 183 PASS / 0 FAIL / 2 SKIP; Windows: 189 PASS / 0 FAIL / 0 SKIP. V8 acceptance validator 16 PASS on each OS; Chromium E2E, syntax, contract, safety, HTTP, containment and host operations PASS. Artifacts: Linux ID `14728729586`, SHA-256 `cca2583aca62d247c43b795205d63837570e451f3f98e87d4558c035cdcd2b26`; Windows ID `14729905280`, SHA-256 `f6254b5e1fb0c5d27b98def8434cb2f59781e5c45fffd0af2e771eff61d780bf`. This run specifically tests the hardened category/policy checks added to Sandbox acceptance_validator.py and mirrored in commit 29daa. Evidence: `06_EVIDENCE/W10_CROSS_PLATFORM_CI_EVIDENCE_20261122_RUN53.md`. Physical Windows 10, production HMAC key, Linux cgroup-v2 and ROOM-HOP integration remain open.

## W10-CURRENT-STATUS-20261122-01 — 2026-11-22 06:10 (UTC+07:00)

Hosted cross-platform implementation is substantially verified: browser API + ProcessSupervisor + Windows Job Object + host file operations + pytest + allowlisted PowerShell + V8 validator pass on hosted Windows/Linux. Remaining release blockers are physical Windows 10 PC installation/ACL/Chrome profile/PowerShell validation; production validator secret/hash provisioning; hardened Linux cgroup-v2 profile; ROOM-HOP Dashboard/PC Bridge integrated E2E; full inventory reconciliation and handover packaging. No main merge/release.


## W10-CI-RUN69-20261122-01 — 2026-11-22 06:31 (UTC+07:00)

Co | AI-07 / End-to-End Architecture & Implementation Lead. GitHub Actions Run #69 (ID `44962226803`), exact commit `d6aa3283dec649e57bd51bc47299e3596f39b8ac`, SUCCESS trên Ubuntu 24.04 và Windows Server 2022. Ubuntu: 200 PASS / 0 FAIL / 2 SKIP; Windows: 206 PASS / 0 FAIL / 0 SKIP. Dashboard static contract: 17 PASS mỗi OS; V8 validator 16 PASS mỗi OS; Real Chromium E2E PASS. Artifacts: Linux ID `14730191774`, SHA-256 `88a725422f3495a82c0dd37242e5c2cf44d5f925763a1523df387dea1873968e`; Windows ID `14730515415`, SHA-256 `1644d1ce85e6d06a38c404a03e15ff7f7063c15ee21fff467c32c97a3f264948`. Evidence: `06_EVIDENCE/W10_CROSS_PLATFORM_CI_EVIDENCE_20261122_RUN69.md`.

## W10-DASHBOARD-REGRESSION-RESOLUTION-20261122-01 — 2026-11-22 06:31 (UTC+07:00)

Run #63 fail được truy nguyên: GitHub Dashboard cũ 1.7 KB không có các live-health/input/evidence hooks trong Sandbox Dashboard 20.5 KB; static contract test phát hiện đúng mismatch. Co đồng bộ Dashboard thật và README lên GitHub, không bỏ hoặc nới test. Run #67 pass sau sync; phát hiện check counter không đếm Dashboard PASS vì output prefix thiếu hai dấu cách. Co sửa test output và Run #69 xác nhận 17 assertions PASS trên cả Windows/Linux. Dashboard static contract PASS; live Dashboard/API integration trên PC Owner vẫn NOT RUN.

## W10-INVENTORY-RECONCILIATION-20261122-02 — 2026-11-22 06:31 (UTC+07:00)

Inventory snapshot hiện tại: Sandbox 156 files trong `COMPUTER-AGENT/`; GitHub branch 62 files; shared 62; Sandbox-only 94; GitHub-only 0. Toàn bộ 62 shared files đang được đối chiếu; 30 source/test/architecture/config files đã exact UTF-8 match trong các lượt kiểm tra độc lập. Ba LOCKED contracts exact match. Sandbox-only còn lại chủ yếu là historical/debug handoff, reference/original, preview/sample, generated runtime evidence/lock và cache files; cần ghi KEEP/SANDBOX-ONLY dispositions, không bulk-sync pycache, locks, preview samples hoặc debug packages không được chấp thuận. Full inventory disposition chưa chốt.


## W10-INVENTORY-COUNT-CORRECTION-20261122-01 — 2026-11-22 06:33 (UTC+07:00)

Co | AI-07. Sau khi tạo và đồng bộ chính tài liệu inventory, số lượng tăng một file ở mỗi phía: Sandbox 158 files; GitHub 65 files; shared 65; Sandbox-only 93; GitHub-only 0; một thư mục `.github/` chỉ ở Sandbox. Bản snapshot trước đó 157/64 là thời điểm trước khi inventory document được thêm. Danh sách 93 file Sandbox-only được phân loại đầy đủ trong `06_EVIDENCE/W10_FULL_PATH_INVENTORY_DISPOSITION_20261122.md`. Các file đó giữ SANDBOX-ONLY theo nhóm generated/transient, reference/preview, historical evidence, debug handoff, superseded handover và transcript.

## W10-HANDOVER-PACKAGE-20261122-01 — 2026-11-22 06:33 (UTC+07:00)

Co đã tạo và đồng bộ `07_RELEASE/W10_HANDOVER_PACKAGE_20261122.md` cùng `07_RELEASE/README.md`. Đây là gói bàn giao cho Owner review, không phải nghiệm thu cuối hay release. Run #69 xác nhận 17 Dashboard static assertions PASS trên mỗi OS; Windows 206 PASS, Ubuntu 200 PASS + 2 SKIP. Các gate còn mở: physical Windows 10, production HMAC key/pins, Linux cgroup-v2, ROOM-HOP PC Bridge integration và Owner acceptance. Không merge main/deploy/release.



## W10-ROOM-HOP-BOUNDARY-AND-PORT-3010-20261122-01 — 2026-11-22 06:35 (UTC+07:00)

Co xác lập ranh giới tích hợp: Work10 là local Computer Agent provider, loopback-only; W24 giữ Core authorization + authenticated PC transport; W112 giữ cross-Work contracts; W14 giữ canonical W12/W13/W14 execution boundary; W113 giữ shared Dashboard ingress port 3000. Work10 standalone Dashboard chuyển sang loopback port 3010, không chiếm port 3000. Không remote expose API, không bypass Core, không thay W14, không sửa các Work khác. Handoff: `06_EVIDENCE/W10_ROOM_HOP_INTEGRATION_BOUNDARY_HANDOFF_20261122.md`. Integration runtime W10↔W24/W14/W113 còn NOT IMPLEMENTED / NOT VERIFIED.

## W10-INVENTORY-COUNT-CORRECTION-20261122-02 — 2026-11-22 06:36 (UTC+07:00)

Sau khi tạo và đồng bộ integration boundary handoff, snapshot mới: Sandbox 159 files; GitHub 66 files; shared 66; Sandbox-only 93; GitHub-only 0. Một thư mục `.github/` chỉ ở Sandbox. 93 Sandbox-only file dispositions không đổi. Inventory report đã được cập nhật.


## W10-CI-RUN104-20261122-01 — 2026-11-22 06:37 (UTC+07:00)

Co | AI-07. GitHub Actions Run #104 (ID `44963124942`) tested commit `ee6b6cf06643fc92aac1572290e5b3918b481ade` and completed SUCCESS on Ubuntu 24.04 and Windows Server 2022. Ubuntu: 200 PASS / 0 FAIL / 2 SKIP; Windows: 206 PASS / 0 FAIL / 0 SKIP. Seven suites passed on both OSes, including Dashboard static 17 PASS and V8 validator 16 PASS; real Chromium E2E PASS. This is the first complete cross-platform run after moving Work10 standalone Dashboard origin to port 3010 (not 3000). Artifacts: Linux ID `14729759048`, SHA-256 `d3ecf4849ca7b98c0624b165f1b488564617f9e43fdbb5a90f0a45edec587029`; Windows ID `14729409940`, SHA-256 `5fe5ababa06291bd1b4dde3eef1574bde1f182781db435bc4e46306225c2ea6e`. Evidence: `06_EVIDENCE/W10_CROSS_PLATFORM_CI_EVIDENCE_20261122_RUN104.md`. Run #104 precedes POSIX cleanup polling/stress-test patch; Run #105/#106 are follow-up checks.



## W10-POSIX-CLEANUP-REMEDIATION-20261122-01 — 2026-11-22 06:37 (UTC+07:00)

Co | AI-07. Run #99 (ID `44963052277`) exposed one intermittent Ubuntu process-containment failure: `process group did not become empty` after the worker leader exited while an orphaned descendant could still be awaiting init reaping. Windows job passed. Co hardened `terminate_posix_process_group` to keep polling group identity until the bounded deadline after SIGKILL, and expanded the POSIX worker/grandchild test to three cycles. Run #105 (ID `44963236229`, commit `e46189f...`) passed both OSes: Ubuntu 200 PASS/0 FAIL/2 SKIP; Windows 206 PASS/0 FAIL/0 SKIP. Run #106 (ID `44963255436`, commit `12992e1...`) passed both OSes with the three-cycle stress test. Real Chromium E2E PASS on both. Evidence: `06_EVIDENCE/W10_POSIX_CLEANUP_REMEDIATION_CI_20261122_RUN99_105_106.md`. This closes the observed intermittent CI failure, not the Linux cgroup-v2 production gate; POSIX remains LIMITED_NOT_CGROUP_V2.



## W10-CI-RUN105-106-AND-INVENTORY-UPDATE-20261122-01 — 2026-11-22 06:38 (UTC+07:00)

Run #105 and #106 completed SUCCESS on Ubuntu 24.04 and Windows Server 2022. Run #106 included the three-cycle POSIX worker/grandchild cleanup test. Current results: Ubuntu 200 PASS / 0 FAIL / 2 SKIP; Windows 206 PASS / 0 FAIL / 0 SKIP. Run #99's intermittent group-empty check failure is remediated by bounded polling and repeated stress test; Linux remains LIMITED_NOT_CGROUP_V2. Evidence: `06_EVIDENCE/W10_POSIX_CLEANUP_REMEDIATION_CI_20261122_RUN99_105_106.md`.

After adding Run #104 and POSIX remediation evidence to both sides, inventory: Sandbox 161 files; GitHub 68 files; shared 68; Sandbox-only 93; GitHub-only 0; one Sandbox-only `.github/` directory. All 68 shared paths exist; accepted source/test/architecture/config files remain exact-match. 93 Sandbox-only paths retain explicit dispositions in `06_EVIDENCE/W10_FULL_PATH_INVENTORY_DISPOSITION_20261122.md`.



## W10-OWNER-DELEGATION-CURRENT-GATE-20261122-01 — 2026-11-22 06:39 (UTC+07:00)

Owner's direct delegation (22/11/2026 06:10 UTC+07) supersedes the prior V8 review wait state: Co is authorized to continue Work 10 implementation, source/test changes, verification on available hosts, Sandbox/GitHub sync and handover without waiting for An review. An V8 review task is marked WAIVED BY OWNER; no An ACK/review/approval is claimed. P0 implementation may proceed under this delegation but must remain within the three LOCKED contracts. No contract change or release/merge is implied. F-15 TaskResult/Workflow timeout mapping remains OWNER DECISION REQUIRED; the earlier Biên bản wording that attributed a specific F-15 decision to Owner has been corrected in an append-only clarification. Current remaining gates: physical Windows 10, production V8 HMAC key/pins, Linux cgroup-v2, W24/W112/W14/W113 integration disposition and final Owner acceptance.



## W10-OWNER-DELEGATION-AND-P0-STATUS-CORRECTION-20261122-02 — 2026-11-22 06:41 (UTC+07:00)

Owner delegation authorizes Co to proceed with P0 implementation and handover without waiting for An review. The V8 review task is WAIVED BY OWNER; no An review/ACK/approval is claimed. Earlier P0 BLOCKED/NOT AUTHORIZED statements remain historical and are superseded by this direct owner delegation for implementation work. Three LOCKED contracts remain unchanged. F-15 TaskResult/Workflow timeout mapping remains OWNER DECISION REQUIRED; no owner decision was inferred. The previous Biên bản sentence attributing an F-15 mapping to Owner has been corrected.

Current inventory: Sandbox 161 files; GitHub 69; shared 69; Sandbox-only 92; GitHub-only 0; one Sandbox-only `.github/` directory. Updated inventory file lists all 92 Sandbox-only paths and dispositions.


## W10-LIVE-DASHBOARD-API-RUN135-20261122-01 — 2026-11-22 06:42 (UTC+07:00)

Co | AI-07. GitHub Actions Run #135 (ID `44963956538`) tested commit `a3d935066ffa2dbada32bdd7cf1c94599e6463cf` and passed on Ubuntu 24.04 + Windows Server 2022. New `dashboard_live_e2e` Playwright suite starts Agent API :8787 and Work10 standalone Dashboard :3010; verifies live cross-origin health, Work ID 10, Execute consent gate, in-memory token clearing and reset. Seven checks PASS on each OS. Ubuntu: 207 PASS / 0 FAIL / 2 SKIP; Windows: 213 PASS / 0 FAIL / 0 SKIP. Real Chromium API/runtime E2E PASS. Artifacts: Linux ID `14730642888`, SHA-256 `197f37dd1beaab4589a85a2c7f7b76c6b98b3e40a4bbc73f6835648a17c1284d`; Windows ID `14730518600`, SHA-256 `ec8703ec46cd80026bc46ee0df56b700fc0528d922a6c8ae861ef4f64d86a5e1`. Evidence: `06_EVIDENCE/W10_LIVE_DASHBOARD_API_EVIDENCE_20261122_RUN135.md`. The smoke test does not click Execute; local physical Windows 10 acceptance remains NOT RUN.

## W10-INVENTORY-COUNT-CORRECTION-20261122-04 — 2026-11-22 06:42 (UTC+07:00)

After adding `05_TEST/test_dashboard_live_e2e.py` and its Run #135 evidence to both Sandbox and GitHub, current inventory: Sandbox 163 files; GitHub 71 files; shared 71; Sandbox-only 92; GitHub-only 0; one Sandbox-only `.github/` directory.


## W10-LOCAL-LAUNCHER-RUN157-20261122-01 — 2026-11-22 06:45 (UTC+07:00)

Co | AI-07. GitHub Actions Run #157 (ID `44964503556`) completed SUCCESS on Windows Server 2022 and Ubuntu 24.04. Windows PowerShell AST parser passed both local launcher scripts; local launcher smoke started Agent API on loopback :8787 and Dashboard on :3010, verified Work ID 10 health + HTTP 200, then STOP verified process command lines/start times and stopped only its session processes. Windows: 224 PASS / 0 FAIL / 0 SKIP; Ubuntu: 218 PASS / 0 FAIL / 2 expected SKIP. Windows launcher contract: 11 PASS each OS; Dashboard static 17 PASS; Dashboard live E2E 7 PASS; V8 validator 16 PASS; real Chromium E2E PASS. Evidence: `06_EVIDENCE/W10_LOCAL_LAUNCHER_CI_EVIDENCE_20261122_RUN157.md`. CI uses `-NoClipboard -NoOpenBrowser`; physical Windows 10, clipboard/browser launch, ACL and local Chrome profile still require Owner PC acceptance.



## W10-LAUNCHER-INVENTORY-UPDATE-20261122-01 — 2026-11-22 06:46 (UTC+07:00)

Run #157 confirms PowerShell syntax and Windows local launcher start/stop smoke on hosted Windows Server 2022. Current hosted regression: Windows 224 PASS / 0 FAIL / 0 SKIP; Ubuntu 218 PASS / 0 FAIL / 2 expected SKIP. Local Windows 10 acceptance remains NOT RUN.

After adding START/STOP scripts, launcher contract test and Run #157 evidence to both sides, inventory: Sandbox 167 files; GitHub 75; shared 75; Sandbox-only 92; GitHub-only 0. All 34 accepted source/test/architecture/config/launcher files independently compared exact UTF-8. Updated inventory: `06_EVIDENCE/W10_FULL_PATH_INVENTORY_DISPOSITION_20261122.md`.



## W10-HTTP-OVERSIZE-TEST-REMEDIATION-20261122-01 — 2026-11-22 06:48 (UTC+07:00)

Co | AI-07. Run #169 Windows HTTP API suite stopped after 20 PASS with WinError 10053 while urllib was uploading a 1 MiB+10 byte body. API correctly rejects Content-Length >1 MiB before reading body and returns 413; Windows client could still be sending the payload while server closed the connection. Co changed only test construction to send authenticated headers with oversized Content-Length via http.client without uploading the body. API limit/runtime unchanged. Run #175 (ID `44965429403`, commit `740798d7053061f5c8d0908d4882f8aed13f1a4b`) passed both OSes: Windows 225 PASS / 0 FAIL / 0 SKIP; Ubuntu 219 PASS / 0 FAIL / 2 SKIP; HTTP suite 52 PASS per OS. Evidence: `06_EVIDENCE/W10_HTTP_OVERSIZE_TEST_REMEDIATION_RUN169_175.md`.



## W10-FINAL-LAUNCHER-HTTP-RUN180-20261122-01 — 2026-11-22 06:50 (UTC+07:00)

Co | AI-07. GitHub Actions Run #180 (ID `44965583364`) tested commit `1d64e841b10bf1a68bc3dba2484ff0bcfbd7d415` and passed both OSes. Windows Server 2022: 226 PASS / 0 FAIL / 0 SKIP; Ubuntu 24.04: 220 PASS / 0 FAIL / 2 expected SKIP. Windows PowerShell AST, local launcher start/health/Dashboard/stop smoke, 13 launcher contract assertions, Dashboard static 17, Dashboard live 7, V8 validator 16 and real Chromium API/runtime E2E all PASS. The latest launcher clears the API token from the parent environment before starting the static Dashboard server and cleans its session record on startup failure. The oversized HTTP test now sends an oversized Content-Length without platform-dependent body upload; API still returns 413. Evidence: `06_EVIDENCE/W10_LOCAL_LAUNCHER_HTTP_CI_EVIDENCE_20261122_RUN180.md`. Physical Windows 10 acceptance remains NOT RUN.



## W10-RUN180-INVENTORY-UPDATE-20261122-01 — 2026-11-22 06:51 (UTC+07:00)

Latest hosted regression Run #180: Windows 226 PASS / 0 FAIL / 0 SKIP; Ubuntu 220 PASS / 0 FAIL / 2 expected SKIP. PowerShell AST, local launcher start/stop smoke, 13 launcher checks, Dashboard static/live, V8 validator and real Chromium E2E PASS. Evidence: `06_EVIDENCE/W10_LOCAL_LAUNCHER_HTTP_CI_EVIDENCE_20261122_RUN180.md`.

After mirroring Run #180 evidence, current inventory: Sandbox 169 files; GitHub 77; shared 77; Sandbox-only 92; GitHub-only 0; one Sandbox-only `.github/` directory. All accepted source/test/architecture/config/launcher files are on the canonical branch.



## W10-CANONICAL-HEAD-RUN195-20261122-01 — 2026-11-22 06:52 (UTC+07:00)

Co | AI-07. Latest GitHub Actions Run #195 (ID `44965933111`) tested current branch HEAD `73b51f61b62d3b1664e8d9d0dd54e979eb5640b1` after final Manifest/Journal/inventory sync. Both matrix jobs SUCCESS: Windows 226 PASS / 0 FAIL / 0 SKIP; Ubuntu 220 PASS / 0 FAIL / 2 expected SKIP. Code unchanged from Run #180; this validates the latest docs/evidence HEAD. Evidence: `06_EVIDENCE/W10_GITHUB_ACTIONS_CI_EVIDENCE_20261122_RUN195.md`.



## W10-RUN195-INVENTORY-UPDATE-20261122-01 — 2026-11-22 06:52 (UTC+07:00)

Run #195 is the latest canonical branch HEAD verification and passed on both OSes: Windows 226 PASS / 0 FAIL / 0 SKIP; Ubuntu 220 PASS / 0 FAIL / 2 expected SKIP. Current branch HEAD at time of run: `73b51f61b62d3b1664e8d9d0dd54e979eb5640b1`. Evidence: `06_EVIDENCE/W10_GITHUB_ACTIONS_CI_EVIDENCE_20261122_RUN195.md`.

Current inventory after adding Run #195 evidence: Sandbox 170 files; GitHub 78; shared 78; Sandbox-only 92; GitHub-only 0; one Sandbox-only `.github/` directory. All 92 Sandbox-only files have explicit KEEP dispositions.



## W10-OWNER-PC-ACCEPTANCE-RUNNER-20261122-01 — 2026-11-22 06:53 (UTC+07:00)

Co created and synced `05_TEST/RUN_WORK10_ACCEPTANCE.ps1`, a one-command physical Windows 10 acceptance runner. It requires Windows 10 client + Python 3.12, parses PowerShell launcher scripts, runs noninteractive launcher smoke, full test suite and real Chromium E2E, hashes source/tests/contracts/schemas, and writes a timestamped JSON report + logs. It records only a boolean for production HMAC key presence, never the secret value; it does not enable write/PowerShell roots and leaves release gate OPEN. It has not been run on Owner PC. CI AST validation is pending.

Current inventory: Sandbox 171 files; GitHub 79; shared 79; Sandbox-only 92; GitHub-only 0.

