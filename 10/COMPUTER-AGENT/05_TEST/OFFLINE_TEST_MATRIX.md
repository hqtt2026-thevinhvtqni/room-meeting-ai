# WORK 10 — OFFLINE TEST MATRIX

**Status:** Historical baseline 2026-10-27; current Sandbox revision updated 2026-11-17 — tests NOT RUN after latest edits
**Owner:** Work 10 — COMPUTER-AGENT
**Runners:** `python 05_TEST/run_all_tests.py` (all suites) or each file directly

## 1. Scope

Things that must be testable **without Chromium / Playwright / a real browser**.
Current rule alignment (2026-11-17):
1. Workflow Contract §3.4: omitted verification invokes a minimum observation check; it is not an automatic PASS.
2. An explicitly supplied empty/malformed verification block is BLOCKED.
3. Explicit post-conditions are evaluated on the final action observation by default.
4. If minimum verification cannot obtain a non-empty observation, or the final action closed the adapter, result is BLOCKED.
5. Historical 2026-10-27 run counts below do not verify the 2026-11-17 Sandbox edits.

## 2. Categories

Legend: `PASS` = implemented and green in the last local run.

### 2.1 Action Contract — `test_p0_p5.py`

| Test case | Expected | Status |
|---|---|---|
| Known action types accepted | parse OK | PASS |
| Unknown action type | REJECT (`ActionValidationError`) | PASS |
| click without target | REJECT | PASS |
| type without value / target | REJECT | PASS |
| navigate without value | REJECT | PASS |
| key_press without value | REJECT | PASS |
| wait without value / non-numeric | REJECT | PASS |
| scroll non-numeric amount | REJECT | PASS |

### 2.2 Click / Type separation

| Test case | Expected | Status |
|---|---|---|
| Explicit click action | semantic = click | PASS |
| Explicit type action | semantic = type | PASS |
| type cannot fake click | semantic stays type | PASS |
| Mixed sequence click → type | order preserved | PASS |

### 2.3 Workflow state machine

| Test case | Expected | Status |
|---|---|---|
| PLANNED → RUNNING → VERIFYING → PASS | allowed | PASS |
| VERIFYING → FAIL on failed check | allowed | PASS |
| RUNNING → PASS (skip VERIFYING) | FORBIDDEN | PASS |
| Action success → auto PASS | FORBIDDEN | PASS |
| Verification omitted | Run minimum observation check; PASS only when non-empty observation exists | NOT RUN (latest revision) |

### 2.4 Verification logic

| Test case | Expected | Status |
|---|---|---|
| All checks pass | PASS | PASS |
| One check fails | FAIL | PASS |
| Explicit empty `checks` list | **BLOCKED** (`verification_invalid`) | NOT RUN (latest revision) |
| Check without `contains` | BLOCKED | PASS |
| Check without `field` | BLOCKED | PASS |
| Unknown `scope` value | BLOCKED | PASS |
| Early observation only | FAIL (final observation is what counts) | PASS |
| `scope: "any"` explicitly requested | PASS when any step matches | PASS |

### 2.5 Evidence completeness

| Test case | Expected | Status |
|---|---|---|
| One entry per action | required | PASS |
| `action_id`, `work_id`, ISO-8601 UTC `timestamp` | required | PASS |
| `attempts`, `timeout_seconds`, `duration_ms` | required | PASS |
| Observation present | required | PASS |
| Verification result recorded | required | PASS |
| `TaskResult.started_at` / `finished_at` | required | PASS |

### 2.6 API / payload validation

| Test case | Expected | Status |
|---|---|---|
| Invalid action type | `ActionValidationError` | PASS |
| `observe` / `close` need no fields | accepted | PASS |
| `wait` with numeric value | accepted | PASS |
| `scroll` with value | accepted | PASS |
| `extract` with object schema | accepted | PASS |

### 2.7 Failure handling

| Test case | Expected | Status |
|---|---|---|
| Permanent adapter exception | FAIL, message preserved, 1 attempt | PASS |
| Transient (timeout/network) | retried, then PASS | PASS |
| Retry count / backoff | 2 retries, ≥500 ms | PASS |

### 2.8 Safety Policy enforcement — `test_safety_policy.py`

| Test case | Expected | Status |
|---|---|---|
| Unknown action in a workflow | BLOCKED, browser not started | PASS |
| Destructive action without allow | BLOCKED, browser not started | PASS |
| Destructive action with explicit allow | PASS | PASS |
| Action flagged `destructive` | BLOCKED | PASS |
| screenshot path outside Work | BLOCKED | PASS |
| screenshot path inside `06_EVIDENCE` / work_root | PASS | PASS |
| Path escaping work_root | BLOCKED | PASS |
| navigate outside allowed domains | BLOCKED | PASS |
| wait over the 120 s cap | BLOCKED | PASS |
| Action timeout | FAIL after retries, budget respected | PASS |
| Workflow timeout | BLOCKED | PASS |
| Retry exhaustion / no infinite retry | FAIL, bounded attempts | PASS |
| Explicit empty / malformed verification | BLOCKED | NOT RUN (latest revision) |
| Omitted verification with unavailable/empty observation | BLOCKED | NOT RUN (latest revision) |
| Final action is close (must not reopen adapter to verify) | BLOCKED | NOT RUN (latest revision) |

### 2.9 HTTP API — `test_http.py`

| Test case | Expected | Status |
|---|---|---|
| `GET /health` | 200 with service, version, policy | PASS |
| Unknown path | 404 | PASS |
| Empty task | 400 | PASS |
| Unknown action | 400 `invalid_action` | PASS |
| Valid workflow | 200 PASS + state trace + evidence | PASS |
| Failing post-condition | 409 FAIL | PASS |
| Omitted verification | 200 PASS only when minimum observation succeeds | NOT RUN (latest revision) |
| Explicit empty verification | 409 BLOCKED | NOT RUN (latest revision) |
| Destructive action | 409 BLOCKED | PASS |
| Adapter lifecycle | `close` on success and on failure | PASS |

## 3. How to run

```bash
cd COMPUTER-AGENT
python 05_TEST/run_all_tests.py          # all suites + JSON evidence
python 05_TEST/test_p0_p5.py             # contracts only
python 05_TEST/test_safety_policy.py     # policy negatives
python 05_TEST/test_http.py              # HTTP API (needs a free port)
```

The HTTP suite runs the real `04_CODE/agent_api.py` with
`COMPUTER_AGENT_ADAPTER_MODULE=test_fake_adapter:FakeAdapter`, so no browser is
started. `test_fake_adapter.py` is a test double, never shipped behaviour.

## 4. Not covered offline

- Chromium launch / real navigate, click, type, scroll, download
- Screenshot and extract against a real DOM
- Dashboard behaviour in a real browser
- Integrated ROOM-HOP E2E

→ stay `READY / HOST RUN REQUIRED`. Never record PASS for them here.

## 5. Definition of Done (offline) — HISTORICAL BASELINE MET; CURRENT REVISION PENDING

- [x] Every case above has executable test code
- [x] Runs without Chromium
- [x] Contract + policy enforced in code, not only in documents
- [x] Runner writes `06_EVIDENCE/offline-test-evidence.json` with per-suite results and source hashes


## 6. Current Sandbox v1.3.0 addendum — 2026-11-17 (NOT RUN)

The historical PASS rows above describe the prior baseline only. A later review found that several check helpers treated a callback returning boolean False as PASS because they only caught exceptions. The helper was corrected in test_p0_p5.py, test_safety_policy.py and test_http.py; the latest revision has not been executed, so historical counts such as 101/101 are not accepted as current evidence.

New NOT RUN cases:
- Bearer token missing/invalid, hostile/missing Origin, preflight method/header restrictions, non-JSON, chunked transfer encoding, non-object JSON, oversized body.
- Explicit verification schema rejected before adapter construction.
- Cross-request timeout: request A times out; request B receives 409 execution_busy without adapter construction; close deferred until worker exit; later request admitted.
- Adapter thread ownership: fake adapter records start/action/deferred-close thread IDs and asserts they are identical.
- False-returning assertion callbacks fail the suite.
- Windows drive/UNC/backslash traversal and symlink escape. Unsupported host capabilities must be reported as SKIP, not PASS.
- Source hashes include Dashboard, Work manifest, architecture, release and AI handoff documentation.

No current test result is claimed by this addendum. Run the current test runner on the exact source revision and retain the generated JSON evidence.


## Cross-platform process-supervisor + real-browser API evidence — 2026-11-22

Source: GitHub Actions run #45, commit `bba3c18fab5b81f02177d002b91eeee0b9db87d5`.

| Suite / gate | Windows Server 2022 | Ubuntu 24.04 | Interpretation |
|---|---:|---:|---|
| Contract tests | 60 PASS | 60 PASS | Current branch commit |
| Safety negative tests | 45 PASS | 41 PASS + 1 SKIP | Skip is Windows-only case |
| HTTP API | 37 PASS | 37 PASS | Auth/origin/body/admission + isolated worker |
| Process containment / owner lease | 2 PASS | 2 PASS | Windows Job Object; Linux process-group LIMITED |
| Real Chromium E2E via HTTP API | PASS | PASS | 13 actions, 15 evidence entries, final verification PASS |
| Containment empty | true | true | Parent checked before releasing request lease |
| Forced cleanup on successful E2E | false | false | No unexpected descendant required forced kill |

Windows Job Object assurance: `OS_JOB_OBJECT_ATOMIC_JOB_LIST` using `PROC_THREAD_ATTRIBUTE_JOB_LIST` at process creation and `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`. Linux assurance: `LIMITED_NOT_CGROUP_V2`; no production cgroup claim.

The run proves hosted runner behavior only. Physical Windows 10 PC validation, V8 semantic validator, file-system/PowerShell/pytest capability API, ROOM-HOP bridge integration and final source parity remain open.


## PC host capability test coverage — 2026-11-22 (CI pending)

A new suite, test_host_operations.py, covers allowlisted directory listing, file read/hash, traversal rejection, explicit write/read-back/overwrite, pytest execution, disabled-by-default writes, symlink escape and Windows-only PowerShell execution. HTTP API tests exercise the same operations through POST /agent/host/execute and ProcessSupervisor. These tests are written but have not yet been run in the next CI commit. No PASS is claimed yet.
