# DOC-119 — Work32 Two-Phase Run Record and Exact-SHA CI Handoff

- **Document Number:** DOC-119
- **Priority:** P0 — execution evidence integrity
- **Work:** 32 — CI/CD
- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-12 00:25 Asia/Ho_Chi_Minh
- **Branch:** work/32-core-owned-execution-authority-20261112
- **Status:** TWO-PHASE RUN RECORD IMPLEMENTED IN SOURCE — EXACT-SHA CI PENDING

## 1. Run Record protocol

Ka selected a two-phase append-only Run Record to prevent a protected process from starting without a durable Core-side intent record:

1. Host validates Grant online and verifies the immutable workspace source SHA.
2. Host asks Core to append run_started with run_id, grant_id, principal, Work, Assignment, Task, Host, exact command, source SHA, environment and start time.
3. Host revalidates the Grant online immediately before process creation. If the Grant was revoked after run_started, no process is spawned.
4. Host executes only the Core-bound pytest entrypoint.
5. Host writes stdout/stderr and a hashed RUN_EVIDENCE.json.
6. Host asks Core to append run_completed with outcome, exit code, evidence digest and completion time.

Each Grant is single-use: Core rejects a second run_started for the same grant_id. Revocation after a recorded start does not erase the start record and does not prevent the Host from recording the completion of that already-started attempt. Revocation does prevent a new run from starting. No cached ALLOW is accepted.

## 2. Source changes

- Core ExecutionAuthority journals run_started and run_completed separately and verifies the state transition.
- Core HTTP exposes POST /works/{work_id}/execution-grants/{grant_id}/runs and POST .../runs/{run_id}/complete.
- Execution Host Core client exposes start_run and complete_run.
- GrantedExecutionHost persists the start record before its final online validation and process effect; it completes the record only after evidence is written.
- Tests cover two-phase persistence, HTTP start/complete, single-use grants, concurrent journal appends, source/evidence path containment and the revocation-before-spawn negative path.
- The WEE adapter's Host HTTP timeout now covers the maximum bounded pytest timeout plus a safety margin, avoiding premature client timeout while the Host is still executing.

## 3. CI handoff

- Push-trigger workflow branch: work/32-main-integration-authority-20261112 (matches work/32-main-integration-* filter).
- Exact source commit before this evidence marker: 3064e7eac51665e0c9f7fe714fd3c625b49002e0.
- Workflow tests include Core authority/store, Core HTTP contract, source snapshot, Host grant enforcement, WEE lifecycle and grant adapter.
- This record itself is documentation-only and must not be mistaken for source-code test evidence.

## 4. Safety and acceptance

- No credentials or live Work policy are committed.
- No Core or Host process has been configured or started.
- No protected command has been executed.
- Run #376 passed the Work32 tooling, 226 unit tests, 112 E2E tests, hosted Windows Browser Adapter and immutable product artifact at its tested merge revision. This is an earlier source snapshot than the subsequent hardening commits; the latest head still requires a new exact-SHA run.
- Independent security review and live exact-runtime positive/negative tests remain required.
- Protected execution remains DENIED; Work32 remains ACTIVE — NOT RELEASED.

## BIÊN BẢN
- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-12 00:25 Asia/Ho_Chi_Minh
- **Decision:** Added a durable run-intent/completion protocol before allowing any protected test execution.

## NHẬT KÝ
- **W32-LOG-20261112-111**
- Recorded the two-phase Run Record protocol and exact-SHA CI handoff.

## 5. P0 completion-contract alignment addendum — 2026-11-13

A source audit found that the Host completion payload included `evidence_persisted` and `evidence_errors`, while the strict HTTP `RunCompleteRequest` schema did not declare them. Because the schema uses `extra="forbid"`, the actual Host completion request could be rejected with HTTP 422 even though direct Core tests passed.

The remediation branch now aligns the full Host → HTTP → Core contract:

- Required lifecycle: `finished_at`, `status`, `exit_code`, `evidence_sha256`.
- Optional execution outcome: `execution_status`.
- Evidence persistence: `evidence_persisted` (bool or null), `evidence_errors` (at most 8 bounded strings).
- Evidence references: `evidence_ref` (bounded to 2048 characters).
- Output digests: optional `stdout_sha256` and `stderr_sha256`, each lowercase SHA-256 hex.
- HTTP schema remains strict: undeclared fields are rejected.

Core now independently validates optional output digests, evidence reference, persistence flag and error list. Inconsistent persistence metadata is rejected: evidence errors require `evidence_persisted=false`; a non-persisted evidence result must be `BLOCKED` and include an error; persisted evidence cannot contain errors.

Regression coverage added:
- HTTP test sends the same evidence metadata shape used by the Host.
- HTTP negative test rejects invalid digest and inconsistent persistence metadata, then accepts a correctly marked BLOCKED completion.
- Core parameterized tests reject malformed stdout/stderr digests, evidence refs, persistence flags and evidence-error lists.

**Validation status:** source and regression tests committed on `work/32-main-integration-remediation-20261113`; full exact-head CI and live Host→Core E2E remain pending. This addendum does not claim PASS.

## BIÊN BẢN — Addendum
- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-13 20:14 Asia/Ho_Chi_Minh
- **Decision:** Align the strict HTTP completion DTO with the actual Host evidence payload and enforce evidence integrity invariants in Core.

## NHẬT KÝ — Addendum
- **W32-LOG-20261113-123**
- Recorded the Host/HTTP/Core completion contract mismatch, source correction and regression coverage.


## 6. Host → Core HTTP end-to-end regression addendum — 2026-11-13

Added `test_granted_host_completes_through_real_core_http_contract` to `tests/test_execution_authority_http.py`.

The test:
1. Creates a temporary Git workspace with the approved repository remote, exact branch and commit SHA.
2. Computes the real workspace source digest and configures a real `ExecutionAuthority`.
3. Issues the grant through the FastAPI Core HTTP route.
4. Constructs the real `CoreAuthorityClient` with an in-process TestClient transport (no fake Host authority client).
5. Executes `GrantedExecutionHost.execute_for_work()`, which performs online grant validation, persists `run_started`, runs the canonical pytest entrypoint, writes evidence and posts the full completion payload through the HTTP route.
6. Reads the append-only Core journal and asserts `run_completed`, `evidence_persisted=true`, empty `evidence_errors`, and valid stdout/stderr SHA-256 digests.

This closes the prior test gap where Core HTTP and Host were tested separately but the actual Host-shaped completion payload was not proven end-to-end through the HTTP boundary.

**Validation:** regression source committed on the remediation branch; exact-head GitHub Actions has not yet completed. No PASS is claimed until the full repository test and Windows lanes finish.

## BIÊN BẢN — Host/Core HTTP E2E Addendum
- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-13 20:18 Asia/Ho_Chi_Minh
- **Priority:** P0 — two-phase Run Record and evidence persistence
- **Decision:** Add a real Host → Core HTTP integration regression to verify the full two-phase completion contract.

## NHẬT KÝ — Host/Core HTTP E2E Addendum
- **W32-LOG-20261113-124**
- Recorded the real Host → Core HTTP completion regression and journal readback assertions.
