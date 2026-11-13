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
