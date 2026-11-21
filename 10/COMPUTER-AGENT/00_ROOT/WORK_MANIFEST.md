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
