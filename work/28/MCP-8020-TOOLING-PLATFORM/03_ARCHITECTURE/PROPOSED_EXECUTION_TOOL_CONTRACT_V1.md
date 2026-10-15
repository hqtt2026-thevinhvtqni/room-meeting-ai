# PROPOSED EXECUTION TOOL CONTRACT V1 — DESIGN ONLY
Date: 2026-10-12 (+07)
Status: DESIGN / NOT REGISTERED / NOT LIVE
Owner: Ka (CSA)
Authority: Vinh
Scope: tool schema and trust boundaries only. This document does not create an endpoint or authorize execution.

## 1. Preconditions — all are hard gates
Do not register or expose execution tools until all are evidenced:
1. The deployed MCP :8020 and Core :8000 revisions are identified by exact SHA.
2. Core provides the actual authenticated principal and resolves WorkContext from server-side authority. Caller-supplied identity_id, authorized=true, paths, repository, branch, workspace, evidence_root or expected_head are never authoritative.
3. A single canonical W12/W13 execution service is identified and reachable through an existing authenticated Core route. Do not wire MCP directly to execution_host/server.py and do not create another host.
4. Runtime enforces OS-level isolation for untrusted Python: dedicated low-privilege identity/container/VM, no host secrets, denied host loopback and outbound network by default, workspace-only writable filesystem, bounded CPU/RAM/PIDs/disk/output/time, and process-tree termination.
5. Run source is copied to an immutable per-run snapshot and hashed before execution. The executed hash must equal expected_source_sha256.
6. Core/runtime writes evidence to an integrity-protected location that normal Sandbox write/delete tools cannot modify.
7. Cla reviews the threat model and negative tests; Go independently runs E2E. A tool schema alone never passes these gates.

## 2. Proposed tool family (names are proposals, not registered tools)
### python_run
Input:
- work_id: string, required
- entry_path: relative path within authorized Work, required
- operation: enum RUN_SCRIPT | RUN_TESTS, required
- expected_source_sha256: lowercase SHA-256 hex, required
- timeout_seconds: integer, 1..300 requested; server applies a stricter policy cap
- request metadata: no caller-selected principal, cwd, interpreter, shell, argv, env, stdin, host path, URL or command string

Trusted server actions:
- Derive principal from authenticated MCP/Core transport.
- Resolve and authorize Work + operation via Core.
- Validate path lexically and enforce canonical filesystem containment, reject symlinks/reparse points at open time.
- Create request_id/run_id server-side.
- Snapshot source into per-run isolated workspace, compute hash, compare to expected hash, otherwise BLOCKED before executing.
- Dispatch to the one canonical W12/W13 runtime only after the OS isolation gate is proven.
- Persist a protected run record and return only bounded/redacted output.

Response:
- request_id, run_id, status, work_id, source_sha256, exit_code, started_at, finished_at, runtime_identity, stdout_ref, stderr_ref, evidence_ref, test_summary, safe blocker
- PASS for execution requires run_id, exit_code=0, exact source hash, non-empty protected evidence_ref, and trusted test summary showing at least one test when operation=RUN_TESTS
- exit_code=0 alone is never enough; zero tests must not pass.

### python_status
Input: run_id only.
- Principal and Work ownership are checked by Core; unauthorized and nonexistent runs return indistinguishable NOT_FOUND.
- QUEUED/RUNNING remain non-terminal; CANCELLED is terminal and distinct from FAIL.

### python_output_read
Input: run_id plus output selector enum STDOUT | STDERR | SUMMARY.
- Must re-authorize principal + Work on every call.
- Returns bounded, redacted content or a protected evidence reference, never arbitrary filesystem paths.

### python_cancel
Input: run_id.
- Must re-authorize principal + Work on every call.
- Cancels the process tree and records cleanup evidence; status CANCELLED only when cleanup is verified.

## 3. Security and lifecycle invariants
- MCP is an adapter; Core :8000 is the sole authorization/WorkContext authority.
- No caller-controlled command text, interpreter, cwd, environment, stdin, free-form argv, shell or arbitrary network destination.
- Approved command labels do not make arbitrary Python safe. OS isolation is mandatory.
- Every run binds request_id, run_id, work_id, principal, source SHA, runtime build identity, exact operation, timestamps, exit code, test summary and protected evidence reference.
- Evidence is append-only or integrity-checked and inaccessible to agent write/delete operations.
- All request sizes, output bytes, concurrency, CPU/RAM/PIDs/disk and wall time have server-side limits.
- Timeout, malformed response, missing evidence, zero tests, source hash mismatch, unknown runtime identity or incomplete cleanup cannot be PASS.

## 4. Required negative acceptance cases
1. Missing/invalid authenticated principal → DENIED before any side effect.
2. Spoofed identity_id or caller-provided authorized=true → ignored; Core principal wins.
3. Work mismatch / cross-Work run_id read → NOT_FOUND or DENIED per public contract, no data leakage.
4. Traversal, absolute, drive, UNC, ADS, symlink/reparse-point escape → INVALID_REQUEST/DENIED before file open.
5. Unicode bidi/invisible/confusable and Windows reserved/trailing dot-space names → rejected.
6. Source changes after request → immutable snapshot runs only; hash mismatch blocks.
7. Python attempts host secret read, host filesystem read/write, network/loopback, subprocess escape → OS policy blocks.
8. Infinite loop / child process tree → TIMEOUT, all descendants reaped, evidence records cleanup.
9. Huge stdout/stderr / huge file / concurrent run flood → hard limits enforced.
10. Test runner reports zero tests or malformed summary → FAIL, never PASS.
11. Caller attempts evidence overwrite/delete → denied; hash/readback remains stable.
12. Runtime down, stale build hash or unknown host → BLOCKED, no fallback host.
13. Intentional nonzero test → FAIL with nonzero exit code.
14. Happy-path smoke and mutation→fail→patch→rerun must each have distinct run IDs, source hashes and readback evidence.

## 5. Integration decision
Current decision remains NO-GO for registering execution tools. This design becomes implementable only after the missing deployed Core route, authenticated principal, canonical runtime reachability and OS isolation are evidenced. Do not invent route names or wire directly to the alternate HTTP execution handler.
