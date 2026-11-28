# Work 32 — Python Test Runtime for Sandbox (Supplemental Plan v1.0)

**Date:** 2026-10-24 (Asia/Ho_Chi_Minh)  
**Owner / final authority:** Vinh  
**Coordinator:** Xu (AI-01)  
**Status:** PLAN RECORDED; BUILD IN PROGRESS; EXECUTION VERIFICATION BLOCKED  
**Scope:** Provide repeatable Python/pytest execution for ROOM-HOP Tester without depending on Vinh's PC and without requiring Docker.  
**Relationship:** Supplements the existing Work 32 CI/CD survey/architecture; reuses Work 12 execution-environment and Work 27 sandbox-runtime concepts where compatible. It does not replace those Works.

## 1. Problem statement

Tester failures can be caused by missing Python/pytest, undeclared dependencies, incompatible runtime versions, unavailable command execution, or tests that are not collected. These must be distinguished from product-code failures. A missing runtime is not a test PASS and must not automatically be attributed to Coder.

## 2. Architecture decision

1. Work Sandbox remains the workspace for task files and evidence.
2. Python tests must execute only in a dedicated, restricted execution worker / Execution Host boundary, not inside Core :8000, MCP service processes, or the general ROOM host process.
3. Do not assume that a virtual environment alone is a security boundary. Project tests execute arbitrary project code; worker isolation, restricted OS identity, workspace confinement, timeouts, resource limits, and default-deny network policy must be enforced by the host.
4. Docker is not a requirement. A dedicated low-privilege OS worker with a per-task virtual environment is an acceptable first implementation only if isolation and cleanup controls are verified. If the existing Execution Host cannot guarantee those controls, keep execution BLOCKED and use GitHub Actions as a separate remote runner after approval.
5. Use declared dependencies (pyproject.toml or explicit requirements file), pin or constrain versions, record Python/pip/pytest versions, and preserve install/test logs.
6. Never run arbitrary shell strings. Pass an argument vector to the process runner; restrict executable and arguments to policy-approved operations.
7. No Core :8000 installation, no Core 2, no live-service mutation, no deployment, no merge/push by AI. Sandbox files are not automatically authoritative on GitHub.

## 3. Task breakdown

| Task | Owner | Output | Acceptance criteria | Dependency |
|---|---|---|---|---|
| W32-PT-01 Baseline execution capability | Xu + runtime owner | Evidence for available Execution Host command API, Python versions, OS identity, workspace mapping, timeout and isolation controls | Actual capability and limits documented from tool/API evidence; no inference from file access | None |
| W32-PT-02 Runtime contract | Xu / architecture | Input/output schema and status semantics | Includes source SHA, task ID, environment fingerprint, command argv, timestamps, exit code, logs, counts, evidence paths | PT-01 |
| W32-PT-03 Safe environment preparation | Coder | Worker-side venv preparation module | Uses declared dependencies; no shell; timeouts; logs; fail-closed when policy/isolation unavailable | PT-01, PT-02 |
| W32-PT-04 Pytest execution adapter | Coder | Test runner module | Executes python -m pytest; stores stdout/stderr, JUnit XML, exit code and collection result; exit code 5 / zero collected tests cannot PASS | PT-02, PT-03 |
| W32-PT-05 Environment error classification | Coder | Classifier + state mapping | Separates ENV_BLOCKED, COLLECTION_FAILED, TEST_FAILED, TEST_PASSED, TIMEOUT, POLICY_BLOCKED | PT-02, PT-04 |
| W32-PT-06 Unit tests for runner | Tester | Tests for validation, argv safety, status mapping, missing pytest, no tests, failure, timeout, malformed reports | Test cases are executable and results/logs are preserved; until runtime exists, status remains PENDING EVIDENCE | PT-03..05 |
| W32-PT-07 Execution Host integration | Runtime owner + Coder | Adapter behind existing Execution Host contract | No new endpoint on Core :8000; identity and authorization checked; task/workspace scope enforced | PT-01..06 |
| W32-PT-08 End-to-end vertical slice | Coder + Tester + Ka | One synthetic Python project tested end-to-end | Successful case and seeded failing case both produce truthful evidence; restart/timeout path verified | PT-07 |
| W32-PT-09 Hardening | Ka / security reviewer | Threat model and hardening evidence | Low privilege, workspace confinement, no secrets inherited, resource/time limits, cleanup, network policy tested | PT-07 |
| W32-PT-10 CI fallback and handoff | Xu + Tester | GitHub Actions fallback design and handoff | Runner selection documented; no CI activation until authorization; no automatic merge/deploy | PT-08, PT-09 |

## 4. Status semantics

- PASS: requested tests were collected and executed; required assertions passed; exit code and reports agree.
- TEST_FAILED: tests executed and one or more failed.
- COLLECTION_FAILED: pytest could not collect the intended tests or collected zero when tests were required.
- ENV_BLOCKED: runtime/dependency prerequisites could not be prepared.
- POLICY_BLOCKED: required isolation or authorization was unavailable.
- TIMEOUT: execution exceeded a declared limit and was terminated/contained.
- PENDING EVIDENCE: required evidence has not yet been produced.
- BLOCKED: no safe/authorized execution route exists or a dependency prevents progress.
- NOT RUN: no execution was attempted.

Never turn ENV_BLOCKED, COLLECTION_FAILED, POLICY_BLOCKED, TIMEOUT, or NOT RUN into PASS.

## 5. Build loop

For each Task: prepare environment → validate environment → collect tests → execute tests → store evidence → Tester classifies → Ka independently reviews → Xu updates task queue. On a code failure, allow at most two repair/retest cycles. Environment failures are routed to runtime ownership and do not consume a code-repair attempt unless evidence shows a product-code cause. Other independent Tasks continue while blocked Tasks remain queued.

## 6. Security and architecture guardrails

- Core :8000 remains the single source of truth; never install a runner or project dependencies into Core.
- No execution of untrusted project tests in the MCP process itself.
- No shell=True, no unbounded output, no unlimited runtime, no inherited secrets, no default network access.
- Validate work/task IDs and canonicalize workspace paths; reject path traversal and symlink escape.
- Per-task venv/workspace and cleanup policy; preserve only declared evidence artifacts.
- Do not activate CI or deploy until approval and baseline evidence exist.
- Existing Work 12/27 contracts must be inspected before introducing duplicate APIs.

## 7. Gates

- G0 — Existing runtime contract and policy traced.
- G1 — Runtime contract and classification tests written.
- G2 — Environment preparation and pytest adapter implemented.
- G3 — Worker isolation and timeout/resource policy demonstrated.
- G4 — Synthetic pass/fail/no-tests/environment-blocked cases executed with artifacts.
- G5 — Tester → Ka → Xu end-to-end flow demonstrated.
- G6 — Security review and evidence audit completed.

## 8. Current evidence and limitations

The currently accessible ROOM-HOP 8030 tool catalog exposes Sandbox file read/write/list operations but no direct shell/Python/pytest execution operation. This is evidence only about the currently exposed tool catalog; it does not prove the separate Execution Host :8031 lacks execution capability. PT-01 must verify :8031 before implementation is integrated.

**Current status:** planning and scoped initial source artifacts can be authored in Sandbox; actual execution verification remains BLOCKED until a supported execution tool/endpoint is confirmed. No claim of tests passing is made.

## 9. Findings from Work 12/13/27 contract trace (2026-10-24)

- Work 12 Execution Bridge specifies discover, execute, runtime_info, workspace_info, collect_artifact and cleanup, with exit code/log/evidence/provider metadata.
- Work 27 Execution Contract requires task/workspace/source revision, argv, bounded timeout, resource/network profiles, authenticated requester, structured status and evidence; execution must use a non-root disposable isolated worker.
- Work 27 RuntimeAdapter delegates to Work 13 POST /execute and explicitly avoids creating a second execution host.
- Work 27 cross-work decision log states live E2E is BLOCKED because an authorized executable host is not exposed through the current ROOM-HOP route.
- The inspected Work 12 TestRunner prototype has no explicit timeout in the visible subprocess call; it is not accepted as a production-safe runner by itself.

**W32-PT-01 status:** contract trace is recorded; live :8031 capability/attestation remains BLOCKED.  
**Build started:** a pure-Python structured result classifier and unit tests have been written in Sandbox. Test execution remains NOT RUN.
