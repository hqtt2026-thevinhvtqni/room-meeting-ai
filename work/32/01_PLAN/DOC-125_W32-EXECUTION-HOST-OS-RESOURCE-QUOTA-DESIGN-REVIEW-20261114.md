# DOC-125 — W32 EXECUTION HOST OS RESOURCE QUOTA DESIGN REVIEW

- **Work:** 32 — CI/CD
- **Document ID:** DOC-125
- **Type:** Design proposal / independent review request
- **Status:** PROPOSED — NOT APPROVED — NO IMPLEMENTATION AUTHORIZED
- **Date:** 2026-11-14
- **Owner:** Xu / AI-01 (architecture and acceptance)
- **Review requested from:** Ka / AI-02 (security architecture), Cla / AI-03 (CTO implementation review)
- **Related:** DOC-117, DOC-123, DOC-124, DOC-035 / W32-LOG-20261114-130

## 1. Problem statement

DOC-123 H1 item 4 requires hard bounds for runtime, memory, CPU, process count and workspace. Current source evidence confirms runtime timeout, combined stdout/stderr cap, workspace containment and process-tree termination attempts. The audited Work32 Execution Host path does not yet show OS-enforced per-run memory, CPU or process-count quotas.

This proposal is limited to the missing OS resource boundary. It does not authorize protected execution, a new service/port, a new authority owner, changes to the Core grant contract, or any PC runtime repair.

## 2. Existing source baseline

- Core remains the sole grant authority; Execution Host remains the enforcement/execution point.
- Core validates grant status, expiry and revocation under its lock; Host persists run-start before process spawn and performs a second online validation immediately before spawn.
- `execution_host/process_control.py` currently enforces timeout/output bounds and attempts process-tree termination. On Windows it uses `taskkill /T /F`; this is cleanup, not a quota mechanism.
- Windows test evidence from Run #508 is hosted Windows evidence, not proof of ADMIN-PC runtime identity or behavior.
- Exact audited source blobs and method are recorded in DOC-035 W32-LOG-20261114-130.

## 3. Design constraints

1. Quotas must be enforced by the operating system, not only by polling or Python-level estimates.
2. A protected process must not execute before its resource container/limits are successfully applied.
3. If quota creation, assignment, verification or cleanup fails, execution must fail closed before the test command can run.
4. Child processes must inherit the same resource boundary; timeout, cancellation and host shutdown must not leave descendants running.
5. Resource policy values must come from the Core-authorized Work policy / grant binding, not caller-controlled request fields.
6. Limits must be observable in the Run Record/evidence: configured values, enforcement mechanism, assignment result and termination result.
7. No widening of command allowlist, network egress, workspace scope, grant lifetime or identity authority.

## 4. Candidate approaches for independent review

### Option A — Windows Job Object as the enforcement container (preferred candidate, not approved)

Investigate a Job Object configured with:
- per-process or job memory ceiling;
- CPU rate control / hard cap;
- active process limit;
- kill-on-job-close;
- explicit assignment verification and deterministic teardown.

Critical design question: ensure the child cannot begin executing before Job Object assignment. Review whether the implementation requires suspended process creation followed by assignment and resume, or another race-free Windows API pattern. A post-spawn assignment with an execution window is not acceptable without a proven no-effect barrier.

### Option B — OS-specific resource backend abstraction

Define a narrow internal interface (e.g. create container, assign process, verify limits, terminate tree, close container), with:
- Windows Job Object implementation;
- Linux implementation only if protected execution is supported there, using a suitable kernel-enforced mechanism;
- unsupported platforms deny protected execution rather than silently running without quotas.

Do not add Docker; the Work32 PC hardware constraint and no-Docker decision remain in force.

### Option C — Defer protected execution until a supported backend exists

If a race-free and testable quota backend cannot be implemented safely, retain DENY for protected execution. This is a valid fail-closed disposition and is preferable to a best-effort quota.

## 5. Required review questions for Ka and Cla

1. Does Option A provide enforceable CPU, memory and process-count limits for the full descendant tree? Identify API flags and edge cases.
2. How will process creation be held before assignment to eliminate the pre-assignment execution race?
3. What happens if Job Object creation, assignment, limit configuration or query fails? Is denial guaranteed before user code starts?
4. How are nested/host-managed Job Objects, process breakaway, child inheritance and handle lifetime handled on supported Windows versions?
5. Which quota values should be policy-controlled, and what safe initial values are appropriate for this Work's current pytest workload? Provide evidence-based recommendations; do not guess a final value.
6. Is a Linux backend required for this Work's protected execution path? If yes, identify the exact kernel mechanism and test environment; if not, explicitly deny protected execution on Linux.
7. What deterministic tests prove memory exhaustion, CPU cap, process-count overflow, child inheritance, timeout, cancellation, no orphan process and fail-closed assignment failure?
8. What independent evidence is required before H1 can be marked PASS?

## 6. Proposed test matrix (not yet executed)

- Process starts only after successful resource-container assignment.
- Assignment failure: command side-effect marker remains absent; result is BLOCKED.
- Memory limit: child attempts to exceed the configured ceiling; host remains alive; run is contained and recorded.
- CPU limit: sustained CPU workload is constrained by the configured quota; measurement and tolerance are documented.
- Process-count limit: descendant creation beyond the cap is rejected or contained; no process escapes.
- Descendant inherits the same Job Object / resource boundary.
- Timeout and cancellation terminate the full tree; no orphan marker appears after the observation window.
- Job Object handle close and host shutdown clean up all descendants.
- Host restart, Core unavailable, malformed policy, unsupported OS and quota telemetry failure all fail closed.
- Existing output cap, workspace/source binding, grant expiry/revocation, Run Record and evidence persistence tests remain green.

## 7. Approval gates

- Ka returns a security review with threat model, Windows API semantics, failure modes and recommended option.
- Cla returns an implementation feasibility review, race analysis, testability and platform support recommendation.
- Xu reconciles both reviews into the canonical DOC-034 Biên bản / DOC-006 decision log as appropriate.
- No code change begins until the review is reconciled and the Biên bản/decision is finalized.
- After approval, implementation must occur on a dedicated remediation branch, with exact-SHA CI and independent security/QE retest.
- Protected execution remains DENIED until H1/H2 gates are fully evidenced and Vinh explicitly approves the separate acceptance/release decision.

## 8. Current disposition

**OPEN DESIGN GAP:** memory quota, CPU quota and process-count quota are NOT IMPLEMENTED / NOT VERIFIED in the audited Work32 execution path.

**NO IMPLEMENTATION AUTHORIZED.** This document is a review request, not an approval or a claim that the candidate design is safe.


---

## 9. KA / AI-02 INDEPENDENT CSA REVIEW — RECEIVED 2026-11-14

- **Reviewer:** Ka / AI-02, Chief Security Architect (CSA)
- **Review mode:** READ-ONLY; report supplied in the Work32 conversation by the user.
- **Claimed reference branch:** work/32-main-integration-remediation-20261113
- **Reported inspected commit:** 066e0a19f924806a71b1d0bbc971887e5c5d2c50
- **Code changes / PR / commit by reviewer:** NONE
- **Protected execution:** NOT RUN
- **Evidence qualification:** Xu has received the review report. The report's source observations and blob identifiers are recorded as reviewer-reported evidence; Xu has not independently re-fetched every cited source file or reproduced the Windows API tests in this entry.

### 9.1 Reviewer conclusion

- **Current resource-isolation implementation:** REJECT.
- **Candidate Windows Job Object architecture:** APPROVE WITH CONDITIONS.
- **Protected execution:** retain DENIED.
- **Implementation authorization:** NOT GRANTED.

### 9.2 Main findings reported by Ka

1. Existing execution paths use ordinary subprocess.Popen process creation and do not demonstrate a suspended-create / Job Object assignment / verification / resume barrier.
2. Existing timeout and taskkill /T /F behavior is cleanup, not OS-enforced memory, CPU-rate or active-process quota.
3. Grant validation and command/workspace/source bindings are separate from OS resource isolation; authorization does not establish resource containment.
4. Windows Job Objects are a viable candidate for job memory limits, CPU rate control, active process limits, descendant ownership and kill-on-job-close, subject to implementation and platform-specific verification.
5. Required launch sequence: create Job → configure all limits → query/verify limits → create process suspended → assign to Job → verify membership → resume. Any failure must terminate/deny; no fallback to ordinary Popen.
6. Job Object is not a complete security sandbox. It does not by itself reduce the Host account's filesystem, network, service or token privileges. A restricted workload identity and separate access-control policy remain necessary.
7. Nested Job constraints, breakaway flags, WMI process creation, handle lifetime and host-crash cleanup require explicit treatment and tests.

### 9.3 Reported security findings

- CSA-125-01: memory quota absent — Critical.
- CSA-125-02: CPU hard cap absent — High.
- CSA-125-03: active process limit absent — High.
- CSA-125-04: process can start before resource boundary — Critical.
- CSA-125-05: no demonstrated Job ownership for descendants — Critical.
- CSA-125-06: no demonstrated kill-on-job-close behavior — High.
- CSA-125-07: child-process escape paths require explicit control — High.
- CSA-125-08: workload privilege isolation not demonstrated — High.
- CSA-125-09: quota telemetry/provenance not demonstrated — Medium.

### 9.4 Required acceptance evidence

Ka requests negative tests for every pre-execution failure; memory, CPU and process-count enforcement; child/grandchild inheritance; parent exit; timeout/cancellation; host crash and kill-on-close; breakaway/WMI paths; nested Job assignment; unsupported OS; malformed policy; grant expiry/revocation; Run Record persistence; and restricted workload identity. Windows evidence must come from the actual supported execution environment, not only hosted CI.

### 9.5 Xu disposition

This review supports retaining DOC-125 as a proposal and protected execution as DENIED. It does not approve implementation. Xu will reconcile Ka's findings with Cla's independent feasibility review before drafting the canonical DOC-034 decision. The source review is not treated as independent runtime verification.


## 10. CLA / AI-03 CTO FEASIBILITY REVIEW — RECEIVED IN SANDBOX 2026-11-14; SYNCED TO GITHUB

- **Reviewer:** Cla / AI-03 (Claude), CTO implementation and testability review.
- **Canonical review evidence:** work/32/06_EVIDENCE/W32-EVIDENCE-CLA-06-DOC125-RESOURCE-QUOTA-CTO-REVIEW-20261114.md.
- **Mode:** READ-ONLY; no code, PR, commit or protected execution by reviewer.
- **Conclusion:** IMPLEMENTABLE WITH CONDITIONS.
- **Evidence limitation:** Cla explicitly states that its session could not independently read GitHub source files; it relied on DOC-035 / prior review records for source descriptions. Therefore its source-level statements are secondary, not an independent line-by-line source audit.

### 10.1 Proposed implementation

- Narrow ResourceBackend interface with Windows Job Object implementation and UnsupportedBackend that always denies protected execution.
- Configure and query back all limits; create the workload process suspended; assign to Job; verify membership and process state; perform the second online Core validation; only then resume.
- On any failure: terminate/close resources, return BLOCKED, and never fall back to ordinary Popen.
- Use Job memory limit, CPU hard-cap, active-process limit and kill-on-job-close; keep taskkill only as secondary cleanup.
- Use ctypes without Docker or global OS configuration changes. Linux protected execution should be DENY unless a separately verified kernel-enforced backend exists.

### 10.2 Cla's conditions and unresolved decisions

1. Xu must line-trace the source at the exact candidate SHA; Cla did not independently inspect GitHub source in its session.
2. Xu must decide platform backend/Linux denial and test-double injection, policy source/Host ceiling, orphan handling, incomplete/torn journal behavior, Host cancellation path, and JSONL versus SQLite requirement.
3. Probe nested Job behavior, CPU rate control and optional JOB_LIST on an environment matching ADMIN-PC before relying on them.
4. Determine quota values from measured workload baselines; do not guess. Cla proposes repeated baseline measurements and a conservative percentile-based margin.
5. H1 cannot pass without exact self-hosted ADMIN-PC evidence; hosted Windows is not a substitute.
6. Run Record still needs separate-process contention, crash after durable run_started, restart/hash-chain verification and no-false-PASS tests.

### 10.3 Technical cautions from Cla

- Memory limits concern committed memory, not necessarily working set/RSS; exceeding the limit may cause allocation failure rather than an automatic kill.
- CPU hard cap throttles; CPU-time limit is a distinct policy.
- ActiveProcessLimit behavior on overflow must be measured.
- A suspended process may remain as a non-running orphan if Host dies before assignment in the simpler A1 sequence; cleanup and host-crash behavior require a dedicated harness/test. Cla also identifies JOB_LIST as a stronger candidate requiring platform probing.
- Nested Job assignment failure must fail closed; do not break away from a parent Job to force success.

### 10.4 Xu disposition

Cla's feasibility review supports further design work, not immediate implementation. DOC-125 remains PROPOSED / NOT APPROVED. Xu will reconcile Ka's security conditions and Cla's implementation conditions into one DOC-034 decision. Protected execution remains DENIED; no implementation, PC action, main integration or release is authorized by this review.


## 11. XU EXACT-SHA SOURCE TRACE AND DESIGN RECONCILIATION

Xu independently fetched the current remediation-branch source blobs: process_control.py 9f5eeddbbcb32152b19321ac59563e2729a3303c; host.py 977b5bc5072eaf0a3ad054aecd22491483d621b1; granted_host.py 1c5c05f9204510b98775069ed8378d8ac2c69e3f; server.py 14d1d764730540330b7bf1d0f3b83b2c03df6a2c; core_authority_client.py adc36577a94efdd5c46d64c30065993d5cd02b3b; tests/test_execution_host.py 183cba2959db9d9fb00751055efdeddd09c14a64; tests/test_execution_host_grants.py c70ed4bee8a098aae27fcf921e0570bde95bf1f7; core/execution_authority.py dd9becadd56a1df4c3f306de317b2f70f2b3b1db; tests/test_execution_authority.py 6503bf7b5ffb87ee0ab8721044149fb0ebedc52f. The protected GrantedExecutionHost path calls run_bounded(); Windows process creation uses Popen + CREATE_NEW_PROCESS_GROUP, not CREATE_SUSPENDED. The generic ExecutionHost path in host.py also uses ordinary Popen. Neither path currently demonstrates Job Object containment before user code. GrantedExecutionHost's online grant checks and run_started persistence are authorization/audit controls, not resource isolation. Core uses JSONL + OS file lock; DOC-123's SQLite wording needs explicit resolution. See W32-LOG-20261114-134 and W32-DECISION-20261114-08. Design direction approved with conditions only; product implementation not authorized; protected execution DENIED.


---

## 12. XU D1/D3 WINDOWS API DESIGN SPIKE SPECIFICATION — 2026-11-14

- **Status:** DESIGN SPECIFICATION ONLY; NO PRODUCT CODE; NO RUNTIME EXECUTION.
- **Target environment:** Windows 10 Pro, build 19045 (ADMIN-PC baseline recorded in project context).
- **Scope:** resolve D1 (creation-time Job assignment) and D3 (cancellation/descendant lifecycle) sufficiently to define an isolated proof-of-concept. This section does not authorize execution of a user workload.

### 12.1 D1 decision — creation-time Job assignment is the preferred candidate

**Preferred candidate for the bounded spike: `PROC_THREAD_ATTRIBUTE_JOB_LIST` with `STARTUPINFOEX` and `EXTENDED_STARTUPINFO_PRESENT`.**

Reasons:
1. Microsoft documents `PROC_THREAD_ATTRIBUTE_JOB_LIST` as supported on Windows 10 and newer. It lets the creator provide the Job handles to which the child process is assigned during process creation.
2. Creation-time assignment removes the interval in which a newly created, runnable process exists outside the per-run Job.
3. The supported target build (Windows 10 Pro 19045) is within the documented OS generation, but that does **not** prove the exact API call, host nesting state, security descriptor, or runtime behavior on ADMIN-PC. Those require the isolated spike and later exact-environment evidence.
4. The attribute list and its backing Job-handle array must remain valid until the process-creation call has completed and the attribute list is destroyed. Handle ownership and cleanup must be explicit.

**Required launch sequence for the spike:**
1. Validate the Core-authorized grant and resource-profile binding; reject absent, malformed, unknown or digest-mismatched policy.
2. Create a private, unnamed per-run Job Object with a restrictive security descriptor; do not expose a name that unrelated processes can open.
3. Configure all supported limits before process creation: job commit-memory ceiling, CPU hard-cap, active-process ceiling, and `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`. Do not enable either breakaway flag.
4. Query the Job configuration back and compare every effective field with the intended policy. Any mismatch is BLOCKED.
5. Inspect the Host's existing Job membership. If a parent Job exists, determine whether the required nested hierarchy is valid and whether effective parent limits permit the child policy. Do not attempt a breakaway or weaken a parent policy. Unknown or incompatible nesting => DENY.
6. Build the extended startup attribute list with the Job handle(s) in valid parent-to-child order. Create the process using `CreateProcessW` + `STARTUPINFOEX` + `EXTENDED_STARTUPINFO_PRESENT` and the Job-list attribute. Do not use `CREATE_BREAKAWAY_FROM_JOB`.
7. Before allowing the workload to proceed, verify the returned process handle with `IsProcessInJob` for the expected per-run Job, query the Job limits again, and verify the process is alive and the Job membership is present.
8. Perform the final online Core grant/policy revalidation. Only after every previous check and the final revalidation succeeds may the Host mark the run as started/executable and allow the workload to proceed. The exact durable audit ordering must preserve the existing no-false-PASS rule.
9. Close thread/process/attribute-list resources deterministically. Keep the Job handle owned by the Host run supervisor until all descendants are verified terminated.

**No production fallback:** `CREATE_SUSPENDED` + `AssignProcessToJobObject` is retained only as a comparison case in the isolated spike. It is **not** an automatic fallback for production. It has a Host-crash window after process creation and before assignment; a suspended process can be left outside the Job. If the creation-time Job-list path is unavailable, rejected by nested-job constraints, or cannot be verified, protected execution remains DENIED.

### 12.2 Hostile and edge-case conditions

- **Nested Job:** Windows 8+ supports nested Jobs, but a valid hierarchy and parent limits still govern assignment. Probe the actual Host membership and assignment result. Never escape a parent Job to force assignment.
- **Breakaway:** do not set `JOB_OBJECT_LIMIT_BREAKAWAY_OK`, `JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK`, or `CREATE_BREAKAWAY_FROM_JOB`. Verify descendants remain in the per-run Job.
- **WMI / Task Scheduler / SCM:** Job Object inheritance does not cover every process-creation mechanism. Microsoft specifically documents that children created through `Win32_Process.Create` are not associated with the Job by default. A Job Object is therefore not a complete sandbox. The workload identity must not have privileges to create out-of-band processes through WMI, Task Scheduler, service control or other brokers. If that privilege boundary is not established and tested, protected execution remains DENIED.
- **Handle ownership:** Job handles must be non-inheritable, private to the Host supervisor, absent from the workload's inherited handle list, and not duplicated to unrelated processes. `KILL_ON_JOB_CLOSE` acts when the last Job handle closes; leaked/duplicated handles can defeat the expected close behavior. Explicitly call `TerminateJobObject` during cancellation/failure and then verify termination; kill-on-close is the crash backstop, not the only cleanup action.
- **Host crash:** creation-time Job assignment avoids the unassigned suspended-child window. The spike must still verify that process termination/Host crash closes the final Job handle and that all members are terminated. A separate watchdog/helper must not be introduced without a new architecture decision.
- **Restricted identity:** use a non-admin workload identity with explicit filesystem/workspace access and denied credential, service, WMI and network privileges as appropriate. Job Object limits do not remove inherited Host token permissions.
- **Resource semantics:** Job memory limit is committed-memory accounting, not a promise to cap working set/RSS; allocation may fail when the limit is reached. CPU rate hard-cap throttles CPU share and is distinct from a total CPU-time budget. Active-process overflow behavior must be measured. No numeric quota is approved in this specification.

### 12.3 D3 run and cancellation state machine

`POLICY_VALIDATED → JOB_CREATED → LIMITS_CONFIGURED → LIMITS_QUERIED_BACK → PROCESS_CREATED_IN_JOB → MEMBERSHIP_VERIFIED → CORE_REVALIDATED → RUNNING → (COMPLETED | CANCELLING | ROOT_EXITED_WITH_DESCENDANTS) → JOB_EMPTY_VERIFIED → RUN_RECORD_FINALIZED`

Rules:
1. A single Host run supervisor owns the process handle, primary thread handle, Job handle, cancellation signal and finalization lock for that run.
2. Cancellation, timeout, output overflow, Host shutdown and policy-revocation handling enter one idempotent termination path. Repeated cancellation requests must not race finalization or produce duplicate terminal records.
3. The termination path calls `TerminateJobObject` with a non-success termination status, waits for the Job to become signaled, and queries Job accounting until `ActiveProcesses == 0`. A root process exit alone is never proof that descendants have ended.
4. If the root exits while descendants remain, terminate the entire Job. The result is not a clean PASS; classify as CANCELLED/FAILED according to the trigger and record the orphan-prevention action.
5. If Job termination cannot be confirmed within the bounded cleanup deadline, record BLOCKED / INDETERMINATE, retain diagnostic evidence and prevent the Host from accepting another protected run until the containment state is resolved. Never claim zero descendants based only on taskkill output or root exit.
6. On normal completion, require the Job to be signaled and active-process count to be zero before recording a clean terminal result.
7. On Host process termination, the last Job handle must close and `KILL_ON_JOB_CLOSE` must terminate members. The spike must test both graceful Host shutdown and forced Host termination.
8. Run Record write failure, torn record, failed Job query, failed wait, or contradictory process accounting => INDETERMINATE/BLOCKED, never PASS. Do not silently truncate or repair an append-only journal.
9. Run finalization is exactly-once at the logical level: terminal status and evidence references are durable before the run is exposed as complete to callers.

### 12.4 Isolated proof-of-concept test matrix (specification; not executed)

| ID | Test | Required observation | Failure disposition |
|---|---|---|---|
| D1-01 | Create process with Job-list attribute | Process is in the intended Job before any workload side effect | BLOCKED |
| D1-02 | Invalid/unsupported attribute or Job handle | No workload side-effect marker; no ordinary-Popen fallback | DENY |
| D1-03 | Parent Job / nested Job compatibility | Valid hierarchy only; effective limits are no weaker than policy | DENY on ambiguity/failure |
| D1-04 | Job limit configure/query mismatch | Process is not created; queried fields and policy digest retained | BLOCKED |
| D1-05 | Host crash around process creation | No uncontained runnable or suspended orphan remains | BLOCKED |
| D1-06 | Breakaway attempt by child/grandchild | Descendant remains in Job or operation is denied; no escape | BLOCKED |
| D1-07 | WMI `Win32_Process.Create` attempt | Restricted identity cannot create an out-of-Job process | DENY protected execution if privilege remains |
| D3-01 | Explicit cancellation | Entire Job terminates; Job signaled; ActiveProcesses=0 | BLOCKED if not verified |
| D3-02 | Timeout / output overflow | Same full-tree termination and zero-process verification | BLOCKED if not verified |
| D3-03 | Root exits while child/grandchild remains | Supervisor detects nonzero active count and terminates Job | Never PASS |
| D3-04 | Graceful Host shutdown | All active Jobs terminated and handles closed | BLOCKED if not verified |
| D3-05 | Forced Host termination | Last-handle close triggers kill-on-close; no surviving member | BLOCKED if not verified |
| D3-06 | Duplicate/reused Job handle attempt | Workload cannot inherit/open/duplicate the supervisor handle | DENY if handle isolation fails |
| D3-07 | Repeated/racing cancel requests | One terminal record; no double-finalization or leaked process | BLOCKED on inconsistency |
| D3-08 | Job wait/query failure | Result remains INDETERMINATE; no clean completion | BLOCKED |
| D3-09 | Run Record failure/torn write | No false PASS; evidence preserved; restart fails closed | BLOCKED |
| D3-10 | CPU/memory/process-count enforcement | OS query/accounting confirms configured enforcement and measured behavior | NOT PASS until measured |

### 12.5 Acceptance evidence required from the spike

- Exact Windows edition/build and process identity; exact source revision and test harness hash.
- API calls, flags, structure sizes, return codes and captured `GetLastError` values for every positive and negative path.
- Before/after Job configuration query; `IsProcessInJob` results; Job accounting snapshots; wait/signaled result.
- Process tree identity/PIDs and proof of zero active descendants after cancellation, root exit, graceful shutdown and forced Host termination.
- Side-effect marker proving no user workload ran on every pre-execution failure path.
- Evidence that WMI/service/task-scheduler broker creation is unavailable to the restricted workload identity, or a clear BLOCKED disposition.
- No guessed resource values; baseline measurements must precede any quota selection.
- Independent review by Ka (security) and Cla (implementation feasibility), followed by independent QE on the actual supported Windows environment.

### 12.6 D1/D3 disposition

- **D1:** design recommendation is creation-time `PROC_THREAD_ATTRIBUTE_JOB_LIST`; Windows 10 build 19045 is within the documented support generation. Runtime proof on ADMIN-PC remains NOT RUN / NOT VERIFIED. Suspended-create/assign is not an approved production fallback.
- **D3:** lifecycle and cancellation contract defined above; implementation and runtime evidence remain NOT RUN.
- **Authorization:** this is a design/test specification only. It does not authorize product code, local PC execution, self-hosted runner dispatch, protected workload execution, service changes, PR/main integration or release.
- **D1 status:** DESIGN SPECIFIED / RUNTIME NOT VERIFIED.
- **D3 status:** CONTRACT SPECIFIED / RUNTIME NOT VERIFIED.

### 12.7 External API references consulted

- Microsoft Learn — Job Objects: https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects
- Microsoft Learn — UpdateProcThreadAttribute / `PROC_THREAD_ATTRIBUTE_JOB_LIST`: https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-updateprocthreadattribute
- Microsoft Learn — Nested Jobs: https://learn.microsoft.com/en-us/windows/win32/procthread/nested-jobs
- Microsoft Learn — JOBOBJECT_BASIC_LIMIT_INFORMATION: https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_limit_information

These references establish documented API semantics only; they are not evidence that the API has been exercised successfully on ADMIN-PC.


### 12.8 Current document-status clarification

The metadata and dispositions in Sections 1–10 preserve the proposal/review history as it stood when those entries were written. The later controlling decision is **W32-DECISION-20261114-08 in DOC-006 and Biên bản W32-20261114-08 in DOC-034**: the **design direction is APPROVED WITH CONDITIONS**, while **product implementation remains NOT AUTHORIZED** and **protected execution remains DENIED**. Sections 11–12 are the current Xu trace/specification addenda and do not override the authorization boundary in DOC-006/DOC-034.


---

## 13. XU D2 CORE RESOURCE-PROFILE CONTRACT — DESIGN PROPOSAL

- **Status:** DESIGN PROPOSAL; NOT IMPLEMENTED; NOT AUTHORIZED FOR PRODUCT SCHEMA CHANGE.
- **Source baseline:** exact Core source blob `core/execution_authority.py` = `dd9becadd56a1df4c3f306de317b2f70f2b3b1db`; Host validation client blob = `adc36577a94efdd5c46d64c30065993d5cd02b3b`; Granted Host blob = `1c5c05f9204510b98775069ed8378d8ac2c69e3f`.
- **Finding:** current Core Work policy requires `max_timeout_seconds` but does not validate or bind an OS resource profile. Grant issuance copies `max_timeout_seconds` and `policy_version`; it does not currently carry memory, CPU hard-cap or active-process policy. Host `validate_grant()` returns the stored grant fields, so there is no resource profile for Host to enforce today.

### 13.1 Ownership and trust model

1. **Core owns policy.** The authoritative Work policy contains a versioned resource profile. The profile is not supplied by the agent, caller, HTTP request or workload.
2. **Grant binds a snapshot.** At issuance, Core validates the Work profile and copies the normalized profile plus its canonical SHA-256 digest into the immutable grant record. The grant token therefore authorizes one Work/assignment/task/host/source/environment and one exact resource profile.
3. **Validation returns the bound profile.** Core's online grant validation returns the profile, profile ID/version and digest with the rest of the grant binding. Missing or malformed profile fields are an authorization failure, not a request to use defaults.
4. **Host has a local hard ceiling.** The Host loads an operator-controlled, service-owned ceiling at startup. It is not accepted from the execution request, environment supplied by the caller, or workload. Missing/invalid ceiling => Host DENY.
5. **Effective limits are the stricter values.** For each upper-bound dimension, effective limit = `min(Core-authorized profile, Host hard ceiling)`. Host cannot raise a Core limit; Core cannot exceed the Host ceiling. Timeout is likewise the minimum of grant-authorized timeout and Host maximum.
6. **No profile downgrade.** Unknown schema/profile, stale version, digest mismatch, unsupported enforcement capability or policy change since grant issuance => DENY. No legacy/no-profile compatibility fallback for protected execution.

### 13.2 Proposed canonical profile shape

The following is a contract sketch, not an implemented API schema:

```json
{
  "schema": "room-hop.resource-profile/v1",
  "profile_id": "work32-pytest",
  "profile_version": 1,
  "memory_limit_bytes": 0,
  "cpu_rate_x100": 0,
  "active_process_limit": 0,
  "runtime_limit_seconds": 0
}
```

Field semantics:
- `memory_limit_bytes`: positive integer for Job-wide committed-memory ceiling; not RSS/working-set bytes.
- `cpu_rate_x100`: integer 1..10000; Windows Job Object hard-cap rate expressed as percentage × 100 (for example, 2000 means 20%). The profile must explicitly request hard-cap mode; weight-based scheduling is not an equivalent control.
- `active_process_limit`: positive integer for the maximum simultaneous processes in the Job, including descendants.
- `runtime_limit_seconds`: positive integer; must not exceed the Work policy's existing maximum timeout and the Host ceiling.
- `profile_id`: stable, Work-policy-owned identifier; not a caller-selected string.
- `profile_version`: positive integer, incremented whenever any effective profile field changes.
- The example's zero values are placeholders and MUST NOT be accepted as runnable limits. No quota values are selected in this design.

### 13.3 Digest and validation rules

- Core canonicalizes the profile using the existing canonical JSON convention (UTF-8, sorted keys, compact separators, no NaN/Infinity) and calculates SHA-256 over the complete normalized profile object.
- Grant stores `resource_profile`, `resource_profile_id`, `resource_profile_version`, and `resource_profile_sha256`. Digest is recomputed at every Core/Host trust boundary and compared in constant-time where appropriate.
- Core validates exact keys and types; booleans are rejected where integers are required; all numeric fields must be positive and within documented OS/API ranges; CPU rate must be 1..10000.
- Host verifies schema, digest, Work/Grant binding, supported backend and local hard ceiling before creating a Job.
- Core validation must reject a grant if the current authoritative Work profile no longer matches the profile digest/version bound at issuance, unless a future explicit policy permits grandfathering. Default disposition is stale-policy DENY.
- The agent request schema must not accept resource-profile values. Unknown quota fields supplied by a caller must be ignored only if the current API contract explicitly allows unknown fields; preferred future behavior is reject unknown fields to avoid ambiguous authority. In all cases, caller-supplied quotas never affect the grant.
- Profile change requires a new version and digest; existing grants with an old digest are denied or revoked. No in-place reinterpretation.

### 13.4 Host ceiling and effective policy

- Host ceiling is loaded once from a trusted service-owned configuration source with restrictive filesystem ACLs and a recorded configuration digest/version.
- Host ceiling contains the same four numeric ceilings and backend capability requirements; it is not exposed in public request parameters.
- The effective Job configuration is computed and recorded before process creation. It includes source profile ID/version/digest, Host ceiling version/digest, effective memory bytes, effective CPU rate, effective process count and effective timeout.
- Query-back of the actual Job Object must equal the effective values. If Windows rounds, ignores or rejects a value, the backend must fail closed rather than silently accept a different limit.
- The Work's existing workspace path/source binding remains a separate filesystem boundary; Job Object is not a disk quota. Any disk-usage quota requirement must be specified and enforced separately, not represented as a Job memory field.

### 13.5 D2 disposition

- **Design recommendation:** Core-owned immutable resource profile + digest in the grant; Host-owned local hard ceiling; strict minimum for every limit; missing/stale/mismatched policy => DENY.
- **Current implementation:** profile schema absent from audited Core and Host source; D2 is NOT IMPLEMENTED / NOT VERIFIED.
- **Authorization:** no Core schema change, Host source change or product test change is authorized by this design proposal.

---

## 14. XU D4/D5 RUN-RECORD AND PERSISTENCE CONTRACT — DESIGN PROPOSAL

### 14.1 D4 — crash/recovery and no-false-PASS contract

The current audited Core implementation uses append-only JSONL events with SHA-256 hash chaining, flush/fsync and an OS file lock. The following behavior is required regardless of the final store:

1. A durable `run_started` event is written before any workload process is created. The grant is consumed at this point.
2. A run with `run_started` and no durable terminal event after restart is `INDETERMINATE`; it is never inferred PASS from exit code, missing process, timeout or Host disappearance.
3. An indeterminate run's grant remains consumed. Re-execution requires a newly issued grant and a separately authorized retry decision.
4. A clean PASS requires all of: process exit code 0; Job signaled; Job active-process count 0; output and runtime bounds satisfied; resource profile and Job query-back verified; source/workspace bindings still valid; durable terminal record accepted by Core.
5. A failure before process creation records a terminal BLOCKED/FAILED result if the store is healthy. If the store is unavailable or the write outcome is ambiguous, status remains INDETERMINATE and no workload starts (pre-start) or no PASS is reported (post-start).
6. A partial/torn/corrupt append is not silently truncated, skipped or auto-repaired. Startup detects corruption and fails closed, preserving the original bytes for investigation.
7. Separate-process contention must be tested with independent Core processes sharing the same store, not only threads or multiple objects in one process.
8. Completion submission must be idempotent by `run_id` and canonical completion digest: an exact duplicate returns the already committed result; a different payload for the same run ID is rejected as a conflict. A transport timeout after commit must not force a second logical completion or create contradictory events.
9. Terminal status must not be returned to the caller as complete until the terminal record is durably committed and readback/chain validation succeeds.

**Required D4 tests:** crash after durable run_started before spawn; crash after spawn before completion; Core restart with incomplete run; Host restart; two independent Core processes contending; lock timeout; torn final line; hash tampering; duplicate identical completion; conflicting duplicate completion; store full/permission denied; and no-false-PASS assertions for every case.

### 14.2 D5 — resolve DOC-123 persistence wording

DOC-123 H1 item 7 explicitly calls for “multi-process lock/SQLite timeout/recovery and append-only Run Record consistency.” The audited source is currently JSONL + OS file lock, not SQLite. To avoid silently treating the current implementation as satisfying an explicit directive, the design disposition is:

- **Acceptance target:** SQLite-backed transactional Run Record is the required target unless DOC-123 is formally amended by the decision owner to remove or replace the SQLite requirement.
- **Current JSONL store:** historical/current implementation only; it does not by itself satisfy the SQLite portion of DOC-123. No automatic migration or dual-write is authorized.
- **Proposed SQLite contract:** one local Core-owned database; WAL mode where supported by the deployment filesystem; `synchronous=FULL`; bounded `busy_timeout`; `BEGIN IMMEDIATE` for state transitions; append-only events table with monotonically increasing sequence, previous hash and event hash; unique run IDs and enforced legal transitions; update/delete protection for event history; transactionally commit grant consumption and run-start/terminal transitions.
- **Integrity:** canonical event serialization and hash chain remain required even with SQLite. Database integrity check and application-level chain validation run on startup/recovery; corruption fails closed.
- **Concurrency:** independent Core processes must serialize state transitions through SQLite transactions; lock timeout returns structured BLOCKED/503 and must not bypass the store.
- **Crash semantics:** SQLite transaction atomicity must ensure a grant/run transition is either fully committed or absent; a committed run_started without completion remains INDETERMINATE and grant-consumed.
- **Deployment constraints:** database must reside on a supported local filesystem, not an unverified network share. WAL behavior, backup/restore, disk-full and process-crash recovery must be tested on the actual deployment filesystem.
- **Migration:** preserve the original JSONL file read-only; design a one-time verified importer with source hash, event count, grant/run counts, hash-chain validation and rollback plan. Do not dual-write or delete the old file until a separately approved migration and reconciliation plan passes.

### 14.3 D4/D5 disposition

- D4 contract specified; process-level/crash/restart/idempotency evidence NOT RUN.
- D5 resolved as a design interpretation of DOC-123: SQLite is the acceptance target; JSONL remains current source implementation and is not silently treated as compliant.
- Product persistence changes and migration remain NOT AUTHORIZED. Ka/Cla review and separate implementation authorization are required.

---

## 15. XU D6 RESOURCE-BASELINE MEASUREMENT PLAN — NO QUOTA VALUES SELECTED

### 15.1 Measurement objective

Derive defensible memory, CPU and active-process ceilings from the actual supported Work32 workload and Host overhead. No numeric limits are selected from guesswork or hosted-runner-only observations.

### 15.2 Workload cohorts

Measure each actual supported command class separately, including:
- deterministic unit/tooling test workload;
- Windows-specific integration / process-tree workload;
- product-artifact or browser/E2E workload only where that command is genuinely in the protected allowlist and its environment is available.

Do not mix hosted Windows results with ADMIN-PC results. Record cold-start and warm-start behavior, serial and approved concurrency modes, and the exact source SHA/environment for each sample.

### 15.3 Required observations

For every run, capture:
- Job-wide committed memory current/peak and configured limit;
- CPU hard-cap configured value, CPU time/accounting and observed throttling;
- active process current/peak, descendant tree and process creation failures;
- wall-clock duration, timeout result and cleanup duration;
- output bytes, workspace size and temporary-file growth;
- Host/Core baseline memory and CPU overhead;
- exact source SHA, command/arguments, Python/runtime versions, OS build, identity, concurrency and test result.

Use Job Object accounting/query APIs for resource values where available. Do not substitute Task Manager working set/RSS for Job committed-memory accounting.

### 15.4 Derivation and review

- Collect repeated samples across the representative workload cohorts; report sample count, p50, p95, maximum, variance and outliers. The measurement plan must state why the sample set is sufficient.
- Choose ceilings with an explicit safety margin and explain the impact of outliers, concurrency and Host overhead. A profile must leave sufficient capacity for the Host/Core and OS; quotas must not endanger the machine.
- Validate memory exhaustion behavior, CPU hard-cap throttling and active-process overflow under controlled conditions. Capture both the OS enforcement result and workload-visible behavior.
- Ka reviews the security implications and denial-of-service envelope; Cla reviews implementation semantics and measurement quality; QE independently reproduces the selected values.
- Any quota adjustment increments profile version and digest. A new profile requires new exact-SHA CI and actual supported-environment verification.

### 15.5 Environment gate and disposition

- Hosted Windows may be used for preliminary harness development but is not a substitute for the supported ADMIN-PC evidence required by H1.
- No local PC measurement or self-hosted runner dispatch is authorized by this design plan. A separate explicit execution authorization and a single bounded PC command/harness will be prepared only after the spike and review gates are complete.
- **D6 status:** MEASUREMENT PLAN SPECIFIED / MEASUREMENTS NOT RUN / NUMERIC QUOTAS NOT SELECTED.
- **H1 resource isolation:** BLOCKED until D1/D3 runtime proof, D2 policy binding, D4/D5 persistence evidence, D6 measured values, privilege boundary and independent QE all pass.


### 12.9 Launch-barrier refinement — creation-time Job assignment PLUS suspended initial thread

To remove ambiguity in the launch sequence, the preferred spike sequence is refined as follows:

1. Use `PROC_THREAD_ATTRIBUTE_JOB_LIST` so the new process is associated with the intended Job during process creation.
2. Also pass `CREATE_SUSPENDED` to `CreateProcessW`. The process is therefore born inside the Job but its primary thread cannot execute workload code.
3. Verify `IsProcessInJob`, query back all effective Job limits, verify the process/thread handles and run bindings, and perform the final online Core revalidation while the primary thread remains suspended.
4. Call `ResumeThread` only after every check succeeds. A return value of `(DWORD)-1`, an unexpected previous suspend count, or any failed verification => call `TerminateJobObject`, wait for Job signaled/ActiveProcesses=0, record BLOCKED and never fall back.
5. Because the process is assigned to the Job at creation, Host crash before `ResumeThread` leaves at most a suspended Job member; last-handle close with `KILL_ON_JOB_CLOSE` must terminate it. The spike must prove this behavior. This is materially safer than create-suspended-outside-Job followed by assignment.
6. `CREATE_SUSPENDED` + later `AssignProcessToJobObject` remains comparison-only. It is not the production fallback because the process exists outside the Job during the assignment interval.

This refinement supersedes any shorter reading of Section 12.1 that might be interpreted as resuming or permitting execution immediately after creation-time assignment without the suspended-thread verification barrier.


---

## 16. BOUNDED WINDOWS API SPIKE — HARNESS ARCHITECTURE AND EXECUTION PROTOCOL

- **Status:** SPECIFICATION ONLY; NOT CODED; NOT EXECUTED; NO PRODUCT IMPLEMENTATION AUTHORIZATION.
- **Authority basis:** DOC-034 / W32-20261114-08 and DOC-006 / W32-DECISION-20261114-08.
- **Purpose:** prove D1 creation-time Job assignment and D3 lifecycle/cleanup using only a benign local probe process. This spike does not execute a Work task, pytest suite, shell command supplied by an agent, or arbitrary user payload.

### 16.1 Isolation and artifact boundary

The spike must be a separate, disposable harness, not imported by Core, Execution Host, Gateway, Workspace or any production service.

Proposed logical components:
1. **Controller:** starts/stops the harness supervisor, captures its PID/exit code, and observes test markers. It must not own or duplicate the per-run Job handle.
2. **Supervisor under test:** creates the unnamed Job Object, configures lifecycle flags, creates the probe process through direct `CreateProcessW`, verifies it, resumes it, cancels it and records API evidence.
3. **Probe executable:** a fixed, reviewed test binary with a small allowlisted set of modes: write a unique marker after start; spawn a child/grandchild using `CreateProcessW`; exit while descendants remain; wait for cancellation. It must not accept arbitrary command strings or load user-supplied scripts.
4. **Evidence collector:** reads only the unique temporary test directory and controller-observed process handles. It must not scan or modify unrelated processes/files.

All output is confined to a newly created per-test temporary directory with restrictive ACLs. Each test uses a unique run ID and marker names. Cleanup is limited to files created by that test. No service, registry, firewall, account, scheduled task, WMI provider, port or machine-wide setting is changed.

### 16.2 API path to be tested

The harness must call the Win32 API directly; wrapping `subprocess.Popen` is not acceptable for this proof.

1. Record OS edition/build, process identity/integrity level, current-process Job membership (`IsProcessInJob(GetCurrentProcess(), NULL, ...)`) and relevant parent-job facts obtainable through documented APIs.
2. Create an unnamed Job Object using `CreateJobObjectW`; retain the only supervisor-owned Job handle. Do not make the handle inheritable, named, duplicated or available to the probe.
3. Configure `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`; set neither breakaway flag. Query the setting back using `QueryInformationJobObject`. Resource quotas are intentionally excluded from this D1/D3-only spike because D2 and D6 have not been approved/measured.
4. Build `STARTUPINFOEXW` and its attribute list. Add `PROC_THREAD_ATTRIBUTE_JOB_LIST` with the intended Job handle(s). Keep the handle array and attribute storage alive until `DeleteProcThreadAttributeList`.
5. Call `CreateProcessW` with an explicit executable path, a fixed argument list, `EXTENDED_STARTUPINFO_PRESENT | CREATE_SUSPENDED`, and no breakaway flag. Prefer `bInheritHandles=FALSE`; if a future test needs pipes, use an explicit `PROC_THREAD_ATTRIBUTE_HANDLE_LIST` containing only the required pipe handles, never the Job handle.
6. While the primary thread is suspended, verify `IsProcessInJob(process_handle, per_run_job_handle)` is TRUE; query back Job limits; verify process/thread handles and expected identity; verify the workload-start marker does not exist; and complete the final authorization/test-fixture check.
7. Call `ResumeThread` exactly once. The expected previous suspend count is 1. A return of `(DWORD)-1`, 0, or any value other than 1 is a failure: terminate the Job, wait for completion, and record BLOCKED. Never retry by launching through Popen.
8. After resume, verify the probe's unique start marker and record the exact API results, error codes and timestamps.
9. On every exit path, close thread/process/attribute resources deterministically. Keep the Job handle until the Job is signaled and accounting confirms zero active processes, or until the explicit Host-crash test transfers observation to the external Controller.

### 16.3 Parent Job / nested Job test is a mandatory D1 gate

Microsoft documents nested Job hierarchies and parent-to-child assignment ordering. It also documents that `IsProcessInJob(..., NULL, ...)` can tell whether a process is in any Job, but does not return a handle to that Job. Therefore the harness must not assume it can enumerate or supply every opaque parent Job handle.

Required cases:
- **P0 — no parent Job:** baseline creation with only the new per-run Job in the Job-list attribute.
- **P1 — known parent Job:** Controller places the Supervisor in a controlled outer Job; the test supplies known Job handles in documented parent-to-child order and verifies the child is in the expected hierarchy.
- **P2 — existing/opaque parent Job:** Supervisor detects it is already in a Job but cannot prove the full parent chain/required assignment semantics. The harness records the API behavior; production disposition remains DENY until the supported launch path is demonstrated safe on the actual Host topology.
- **P3 — incompatible parent limits or nesting:** creation/assignment failure must not cause an alternate launch path; no probe marker may appear.

The spike must determine whether the JOB_LIST attribute used by the actual Host preserves all inherited parent-job constraints and whether the per-run Job is effective under the actual parent chain. A successful `IsProcessInJob` check against the new Job alone is not sufficient proof that every ancestor constraint is preserved.

### 16.4 D3 lifecycle scenarios

- **L1 — normal completion:** probe exits; Supervisor waits on the Job handle and verifies Job signaled plus `ActiveProcesses == 0`.
- **L2 — explicit cancellation:** Supervisor calls `TerminateJobObject`, waits on the Job handle, queries accounting and verifies zero active processes.
- **L3 — root exits, child remains:** probe creates a child/grandchild then exits. Supervisor must detect nonzero active count and terminate the complete Job. Root exit alone is not completion.
- **L4 — graceful Supervisor shutdown:** Supervisor follows the common cancellation path and closes its final Job handle only after recording the outcome.
- **L5 — forced Supervisor termination:** external Controller terminates the Supervisor while a probe is running. The Job handle must not have been inherited or duplicated; `KILL_ON_JOB_CLOSE` must terminate every member. Controller verifies process handles become signaled and no probe descendants remain.
- **L6 — failure before ResumeThread:** Controller kills Supervisor after process creation but before resume. The suspended process must be a member of the Job and must terminate when the final Job handle closes; the workload-start marker must remain absent.
- **L7 — repeated cancellation:** concurrent/repeated cancellation requests result in one logical terminal outcome and no live descendants.
- **L8 — breakaway attempt:** a probe attempts child creation with a breakaway flag. Either creation is denied or the child remains in the Job; any child outside the Job is a hard FAIL.
- **L9 — failed wait/query/termination:** status is BLOCKED/INDETERMINATE; no clean PASS and no next protected run.

### 16.5 Evidence schema and PASS criteria

Each test record must include:
- run ID, test ID, exact harness/probe source and binary SHA-256;
- Windows edition/build, architecture, Supervisor and probe identity/integrity;
- parent Job membership result and known/unknown parent chain disposition;
- API name, flags, input structure values, return value, `GetLastError` when applicable, and monotonic timestamps;
- Job configuration before/after query, `IsProcessInJob` results, process IDs/parent IDs, Job accounting snapshots, wait result and final active-process count;
- marker file presence/absence and hash; Controller-observed Supervisor/probe exit status;
- cleanup result and all remaining test-created process IDs.

A test can PASS only when its own expected behavior is observed and independently verifiable. The overall D1/D3 spike can PASS only if P0–P3 and L1–L9 pass, including the actual supported Host parent-job topology. Any missing observation, ambiguous parent chain, surviving descendant, inherited/duplicated Job handle, marker before ResumeThread, failed query/wait, or evidence loss => BLOCKED/FAIL; no inferred PASS.

### 16.6 Explicit exclusions

This spike does not:
- run pytest, CI commands, shell scripts, agent-provided commands or user workloads;
- set memory, CPU or process-count quotas (D2/D6 remain open);
- claim WMI/Task Scheduler/SCM privilege isolation (separate restricted-identity gate required);
- test or change production Core grant schema, SQLite, JSONL Run Record, Execution Host, Gateway, Workspace or services;
- change PC configuration, start a self-hosted runner, modify main, create a PR, deploy or release.

### 16.7 Required review and execution gate

Before any harness code is created or executed, Xu must prepare a concrete file-level plan and obtain:
- Ka security review of the harness boundary, parent-job behavior, handle ownership and escape cases;
- Cla implementation review of Win32 structure/API correctness, error handling and cleanup;
- explicit separate authorization for harness source creation and, later, execution in a disposable supported Windows environment.

Until those conditions are met, this document is a test protocol only. D1/D3 remain NOT VERIFIED; H1 remains BLOCKED; protected execution remains DENIED.
