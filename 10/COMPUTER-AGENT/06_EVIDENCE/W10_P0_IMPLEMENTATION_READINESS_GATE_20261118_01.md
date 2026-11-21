# WORK 10 — P0 IMPLEMENTATION READINESS GATE

- Document: W10-P0-IMPLEMENTATION-READINESS-20261118-01
- Priority: P0 — Runtime safety / supervised process isolation
- Work: 10 — COMPUTER-AGENT
- Sandbox ID: 10
- Name: Ka
- Title: Delivery / Technical Coordinator
- Date-Time: 2026-11-18 02:00 (UTC+07:00)
- Status: STATIC REVIEW COMPLETE — IMPLEMENTATION BLOCKED BY EXECUTION ENVIRONMENT
- Related: W10-P0-PROCESS-ISOLATION-DESIGN-20261117-01; W10-P0-PROCESS-ISOLATION-REVIEW-20261117-01; W10-P0-PROTOCOL-ADMISSION-20261117-01

## 1. Purpose

Determine whether Work 10 can safely move from the completed P0 process-isolation design into implementation. This is a read-only readiness review. It does not authorize a contract change, source edit, Candidate synchronization, GitHub write, commit, push, PR, merge or release.

## 2. Governing instructions re-read

- 00_ROOT/WORK_MANIFEST.md
- 00_ROOT/SYNC_POLICY.md v1.2
- 00_ROOT/WORK_STRUCTURE_STANDARD.md v1.0
- 03_ARCHITECTURE/WORKFLOW_CONTRACT.md — LOCKED
- 03_ARCHITECTURE/ACTION_CONTRACT.md — LOCKED
- 03_ARCHITECTURE/SAFETY_POLICY.md — LOCKED
- 10_AI_DEBUG_HANDOFF/00_INBOX/VI_P0_REMEDIATION_IMPLEMENTATION_TASK_20261116.md

The Vi P0 task explicitly states that the available Sandbox interface supports file read/write/list only, exposes no code execution/test-runner action, and prohibits edits to 04_CODE or 05_TEST until a verified execution environment is available. The current MCP 8030 tool inventory still exposes Sandbox read-probe, list, create/write/append/delete and ROOM context operations; it does not expose a Sandbox terminal, Python execution or test runner.

## 3. Current source boundary confirmed

Read-only probes succeeded for:
- 04_CODE/agent_api.py
- 04_CODE/agent_runtime.py
- 04_CODE/models.py
- 05_TEST/test_http.py
- 05_TEST/test_fake_adapter.py
- 05_TEST/run_all_tests.py

Static source confirms the interim containment currently implemented in Sandbox:
- one process-local execution lock;
- one dedicated adapter-owner thread per Runtime;
- timeout Future retained without cancellation/retry;
- deferred adapter close after timed-out Future completion;
- request B rejected with HTTP 409 while request A's timed-out worker remains active.

These are source findings only. No Python or HTTP test was executed in this review.

## 4. Readiness decision

**Do not begin source implementation through the current file-only MCP interface.**

Reasons:
1. The explicit Vi implementation task forbids editing runtime/test source before a verified execution environment exists.
2. No execution action is available in the current MCP 8030 tool inventory; a successful read/write probe cannot substitute for executing Python or tests.
3. The process-isolation design introduces OS process ownership, Windows Job Object behavior, suspended process creation, child protocol parsing, and process-tree exit confirmation. An unexecuted implementation would create a high-risk false sense of recovery.
4. The timeout mapping remains a proposed interpretation: Safety Policy §3 states action timeout = FAIL, while uncertain workflow outcome must remain BLOCKED. The three LOCKED contracts must not be silently changed.
5. G0 source parity remains BLOCKED. Sandbox is a working/diagnostic mirror, not the canonical source; no synchronization or promotion is authorized.

## 5. Implementation prerequisites and sequence

Implementation may start only in a verified execution environment and after the timeout result semantics are resolved through the project authority.

Sequence:
1. Preserve the LOCKED contracts byte-for-byte; record their hashes before and after implementation.
2. Implement and unit-test the strict Parent–Child protocol parser/serializer independently of browser startup.
3. Implement single-host admission and startup/shutdown ownership; test duplicate parent, abandoned owner and fail-closed recovery.
4. Implement child launch containment: Windows child created suspended, assigned to a dedicated Job Object, then resumed; assignment failure must prevent execution.
5. Move the complete adapter/browser lifecycle into the child; do not share Playwright objects across processes.
6. Implement parent-owned monotonic deadline, bounded stdout/stderr draining, strict response correlation and state-trace/final-observation validation.
7. On timeout/crash/protocol error, return BLOCKED when outcome is uncertain; terminate the complete child process tree and confirm exit before releasing admission.
8. Add deterministic protocol/admission tests, then fake-child lifecycle tests, then exact Windows Job Object/Chromium descendant tests.
9. Run the complete offline/HTTP suite and real Chromium E2E on the exact resulting source; record raw logs, timestamps and SHA-256.
10. Perform independent review and exact-source parity reconciliation. No Candidate/GitHub write is implied by this sequence.

## 6. Open decisions / non-negotiable safety rules

- Timeout mapping proposal is NOT APPROVED. Do not edit LOCKED Safety Policy or alter ActionResult/TaskResult semantics by assumption.
- Initial Windows mutex proposal is scoped to the same interactive logon session; do not claim cross-session exclusion.
- A process-local lock is not a multi-parent singleton.
- Killing only the Python child PID is insufficient; all owned browser/driver descendants must be proven exited.
- Never release the execution lease on HTTP response completion alone.
- Never auto-retry an action with uncertain side-effect completion.
- Never accept child status PASS without validating correlation, process identity/exit, legal state trace, VERIFYING, fresh final observation, all required checks and cleanup outcome.
- No source change, test result or gate promotion is inferred from static read-back.

## 7. Verification performed in this review

- MCP 8030 Sandbox list and read-probe: PASS for the paths listed above.
- Work 10 manifest and P0 design read-back: PASS.
- Python syntax/tests: NOT RUN.
- HTTP regression tests: NOT RUN.
- Playwright/Chromium: NOT RUN.
- Windows Job Object / mutex / process-tree tests: NOT RUN.
- POSIX process-group tests: NOT RUN.
- Candidate/canonical source parity: NOT re-established in this review; G0 remains BLOCKED.
- GitHub writes / commit / push / PR / merge / release: NOT PERFORMED.

## 8. Gate disposition

- P0 design and static readiness review: STATIC REVIEW COMPLETE.
- P0 process-isolation implementation: BLOCKED — verified execution environment unavailable.
- Timeout semantics: PENDING AUTHORITY DECISION.
- G0 provenance/source parity: BLOCKED.
- G1 runtime safety: BLOCKED.
- G2 HTTP transport: BLOCKED pending exact-source tests.
- G3 artifact boundary: BLOCKED pending Windows path tests.
- G4 Chromium: NOT VERIFIED against current Sandbox source.
- G5–G8: NOT VERIFIED.
- G9 evidence/audit: PARTIAL.
- G10 ROOM-HOP integration: NOT VERIFIED.
- G11 release: BLOCKED_AUTH.

**Overall Work 10: ACTIVE — NOT RELEASED.**

No PC action is requested at this checkpoint. A verified execution host will be required before runtime source implementation and host-dependent validation can proceed.


## Owner-authorized implementation and updated execution evidence — 2026-11-22

This addendum supersedes the historical disposition above that implementation was blocked solely because a verified execution host was unavailable. Vinh's owner authorization is recorded in `06_EVIDENCE/W10_OWNER_DELEGATION_AND_IMPLEMENTATION_AUTHORIZATION_20261122_01.md`; it explicitly delegates implementation to Co and removes An V8 review as a prerequisite. The historical static review remains unchanged.

Implementation now exists in `04_CODE/process_supervisor.py`, `04_CODE/execution_worker.py` and `04_CODE/agent_api.py`. Windows uses atomic Job Object assignment at process creation; Linux uses a limited process-group profile and fails closed by default. Host owner lease, owner generation, durable per-run journal, parent deadline and containment-empty verification are implemented.

**Latest verification:** GitHub Actions run #45 (`44957836070`, commit `bba3c18fab5b81f02177d002b91eeee0b9db87d5`) SUCCESS on hosted Windows Server 2022 and Ubuntu 24.04. Both API-integrated real Chromium E2E tests PASS. Detailed hashes and artifacts are in `06_EVIDENCE/W10_API_PROCESS_E2E_EVIDENCE_20261122_RUN45.md`.

**Still BLOCKED / OPEN:** physical Windows 10 PC execution; Linux cgroup-v2 production profile; V8 semantic acceptance validator and negative suite; file-system/PowerShell/pytest host capability contract/API; integrated ROOM-HOP Dashboard/PC Bridge E2E; full source parity. No contract change, main merge or release is authorized by this addendum.

**KÝ: Co | AI-07 / End-to-End Architecture & Implementation Lead**


## Latest Owner-delegated P0 implementation status — 2026-11-22 06:40 (UTC+07:00)

This addendum supersedes the 2026-11-18 and 2026-11-22 earlier readiness text where it says P0 implementation cannot proceed because no execution host exists or V8 validation has not run. Owner Vinh has directly delegated continued implementation to Co and waived An V8 review as a prerequisite. The task is not an An approval; no An ACK/review is claimed.

### Implemented and hosted-CI verified
- Parent-owned ProcessSupervisor, isolated execution worker, host owner lease, run journal, parent deadline and containment-empty check.
- Windows Job Object kill-on-close / atomic assignment tested on hosted Windows Server 2022.
- Linux limited process-group cleanup, including bounded post-SIGKILL polling and three-cycle worker/grandchild stress; Run #106 passed. This remains LIMITED_NOT_CGROUP_V2.
- HTTP auth, exact Origin, request limits, browser API, host filesystem operations, pytest and allowlisted PowerShell script operation.
- V8 schema + semantic validator + category policy + HMAC attestation; 16 validator tests pass on both OS runners.
- Dashboard static contract: 17 PASS on both OS runners; Work10 standalone UI uses port 3010, leaving shared port 3000 to W113.
- Latest full regression Run #106: Ubuntu 24.04 200 PASS / 0 FAIL / 2 expected SKIP; Windows Server 2022 206 PASS / 0 FAIL / 0 SKIP; real Chromium E2E PASS on both.

### Current gate matrix
| Gate | Current disposition |
|---|---|
| G0 accepted source/test/architecture/config parity | PASS for shared accepted implementation set; 68 shared paths, 93 explicitly Sandbox-only files, 0 GitHub-only |
| G1 browser/API/runtime hosted regression | PASS on hosted Windows/Linux |
| G2 HTTP/auth/Origin/host operations | PASS on hosted Windows/Linux |
| G3 Windows Job Object | PASS on hosted Windows Server 2022; physical Windows 10 NOT RUN |
| G4 real Chromium E2E | PASS on hosted runners; local Owner PC NOT RUN |
| V8 schema/semantic validator | PASS hosted; production HMAC key/pins NOT PROVISIONED |
| Linux hardened containment | BLOCKED — cgroup-v2 not implemented; process-group fallback remains limited |
| G10 ROOM-HOP integration | NOT IMPLEMENTED / NOT VERIFIED; W24/W112/W14/W113 boundaries handed off separately |
| F-15 TaskResult/Workflow timeout mapping | OWNER DECISION REQUIRED; no semantics inferred |
| G11 release | NOT AUTHORIZED; Owner acceptance pending |

### Evidence
- Run #53: V8 policy hardening.
- Run #69: Dashboard static contract.
- Run #104: port 3010 boundary.
- Runs #105/#106: POSIX cleanup remediation and stress.
- Evidence files are linked from the current handover package `07_RELEASE/W10_HANDOVER_PACKAGE_20261122.md`.

**Disposition:** implementation is authorized and substantially delivered; acceptance is partial and release remains blocked by the explicit gates above. Three LOCKED contracts remain unchanged.

**KÝ: Co | AI-07 / End-to-End Architecture & Implementation Lead**
