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