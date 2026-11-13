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
