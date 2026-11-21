# WORK 10 — P0 PROCESS SUPERVISOR IMPLEMENTATION

- Document ID: W10-P0-PROCESS-SUPERVISOR-IMPL-20261122-01
- Name: Co
- Title: AI-07 / End-to-End Architecture & Implementation Lead
- Date-Time: 2026-11-22 05:33 (UTC+07:00)
- Status: IMPLEMENTATION WRITTEN — CI VALIDATION PENDING
- Authority: Owner delegation in `W10_OWNER_DELEGATION_AND_IMPLEMENTATION_AUTHORIZATION_20261122_01.md`.

## 1. Execution architecture

The API process is the sole host owner and request-deadline authority. It does not execute browser actions in its own process. For each workflow it starts one `execution_worker.py` process through `ProcessSupervisor`; the worker creates the adapter and runs `AgentRuntime`.

The worker accepts exactly one bounded JSON request on stdin. It imports runtime/adapter modules only after receiving the parent request. The parent validates the HTTP envelope and verification structure before starting the worker; the worker performs runtime preflight before constructing the adapter.

## 2. Windows containment profile

- A named Windows Job Object is created first with `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`.
- The worker is created through `CreateProcessW` with `PROC_THREAD_ATTRIBUTE_JOB_LIST`; the Job Object membership is established atomically at process creation, before the worker's first instruction.
- `PROC_THREAD_ATTRIBUTE_HANDLE_LIST` restricts inherited handles to the worker's stdin/stdout pipe handles.
- Browser/driver descendants inherit Job Object membership. Closing the API owner's Job Object handle on crash kills the complete contained tree.
- Parent enforces a monotonic workflow deadline, checks Job Object active-process count, terminates the job on timeout/uncertain worker result/remaining descendants, and records whether the job became empty.
- A workflow may be PASS only when no forced termination was needed and the Job Object active-process count is zero. Forced cleanup produces TaskResult BLOCKED even when the tree is subsequently empty.

## 3. Durable host owner and run journal

- `HostOwnerLease` uses an OS file lock to ensure one API owner per Work 10 work root.
- A monotonically increasing `owner_generation` is persisted with owner PID and lifecycle state.
- Every execution has a durable JSON journal under `06_EVIDENCE/process-runs/`, including owner generation, named containment locator, worker PID, and state transitions.
- On new owner acquisition, stale journals are reconciled. Windows recovery opens a still-existing named Job Object and terminates it; if the Job Object is absent but its worker PID is still alive, startup fails closed.
- POSIX recovery does not kill a process group based only on a possibly reused PID; if the old group still exists and identity cannot be proven, startup fails closed.

## 4. Linux profile

The current Linux fallback uses a new POSIX session/process group and verifies/kills descendants in that group. It is explicitly `LIMITED_NOT_CGROUP_V2`. API execution is fail-closed on Linux unless `COMPUTER_AGENT_ALLOW_LIMITED_PROCESS_GROUP=1` is explicitly set. CI sets this only to exercise the limited profile. Production Linux P0 remains BLOCKED until a writable cgroup-v2 fixture, durable cgroup identity and recovery oracle are implemented and tested.

## 5. Timeout semantics (F-15)

- An individual action timeout is represented by ActionResult `status=fail` and `outcome_uncertain=true`.
- The enclosing TaskResult is BLOCKED while the adapter may still be running or the side-effect outcome is unknown.
- Parent terminates the OS containment and verifies it empty before releasing the request lease.
- Whole-workflow deadline is BLOCKED.
- TaskResult FAIL is reserved for a terminated action with a known failure outcome.
- This follows the existing locked Safety Policy; no locked contract is modified.

## 6. Evidence and validation plan

The next cross-platform CI run must prove:
1. API starts and acquires the exclusive owner lease.
2. A normal HTTP workflow returns PASS with `process_supervisor` evidence and verified-empty containment.
3. Windows worker is created atomically inside the named Job Object and real Chromium descendants are contained.
4. Timeout returns BLOCKED, parent forces tree termination, verifies empty containment, and only then releases the request lease.
5. Host owner generation increments; stale journals are reconciled or service startup fails closed.
6. Real-browser E2E is submitted through the HTTP API, not direct in-process AgentRuntime.
7. Three LOCKED contracts remain byte-identical.

## 7. Known limitations

- GitHub-hosted Windows Server 2022 is not the Owner's physical Windows 10 PC. Local PowerShell, ACL, Chrome profile and ROOM-HOP PC bridge remain separate acceptance evidence.
- Linux cgroup-v2 production containment is not implemented.
- Integrated API/process containment has been written but has not yet passed the next CI run at the time of this document.
- Semantic acceptance-manifest validator (schema + trusted provenance + category policy + negative suite) remains a separate open P0 gate.
- Full ROOM-HOP bridge/dashboard integration remains open.

**Disposition:** P0 implementation is in progress. Do not claim P0 PASS or release until exact CI evidence, Windows PC validation, validator suite and integration gates are complete.

**KÝ: Co | AI-07 / End-to-End Architecture & Implementation Lead**
