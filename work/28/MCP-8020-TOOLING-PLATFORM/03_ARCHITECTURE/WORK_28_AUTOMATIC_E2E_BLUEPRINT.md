# WORK 28 — AUTOMATIC E2E IMPLEMENTATION BLUEPRINT
Revision: 1.2 — 2026-10-12
Owner/coordinator: Ka (CSA), delegated by Vinh
Status: PLAN + CONTRACT IN SANDBOX; live runtime remains BLOCKED
This is not a claim that any test ran.

## A. Required automatic pipeline
The goal is a single approved entry point that can repeatedly run:
DISCOVER -> AUTHORIZE -> SNAPSHOT -> HASH -> DISPATCH -> COLLECT -> VERIFY -> PERSIST -> READBACK -> REPORT.
The pipeline must fail closed at each stage. No manual caller-provided `authorized`, principal, interpreter, shell, cwd, environment or command string.

### Stage 0 — Environment discovery (read-only)
- Capture deployed MCP/Core/runtime build identities and process identities using an approved diagnostic.
- Capture registered MCP tool list and exact source revisions.
- If the deployed identity cannot be tied to inspected source, stop BLOCKED.
- Never start a second host as a fallback.

### Stage 1 — Authorization
- Derive authenticated principal from trusted transport.
- Core resolves the authorized WorkContext and operation server-side.
- Reject spoofed principal, Work mismatch and disallowed operation before snapshot or process creation.
- Status/output/cancel calls re-authorize independently.

### Stage 2 — Immutable snapshot
- Accept only Work-relative entry_path and expected_source_sha256.
- Validate lexically, then enforce real filesystem containment at open time; reject symlinks/reparse points and path races.
- Copy only authorized files to an immutable per-run snapshot; calculate SHA-256 from snapshot.
- Hash mismatch => BLOCKED, zero process creation.

### Stage 3 — Canonical runtime
- Dispatch only to the one approved W12/W13 runtime behind Core.
- Runtime must attest build identity and OS isolation profile.
- Apply server-owned resource caps for wall time, CPU, RAM, PIDs, disk, output and concurrency.
- Deny network/host loopback and host secrets by default; terminate the full process tree on timeout/cancel.
- If isolation cannot be attested, return BLOCKED. Never fall back to a general-purpose shell.

### Stage 4 — Evidence
- Server creates request_id and run_id.
- Capture actual exit code, bounded stdout/stderr refs, source hash, runtime identity, timestamps, test discovery summary and cleanup state.
- Evidence writer stores a protected integrity-checked record inaccessible to Sandbox write/delete.
- Read back evidence through the authorized API and verify integrity before final status.

### Stage 5 — Status calculation
- RUN_TESTS PASS requires exit_code=0, tests_run>=1, failures=0, errors=0, exact snapshot hash, run_id, protected evidence_ref and verified readback.
- RUN_SCRIPT PASS requires exit_code=0, exact snapshot hash, run_id, protected evidence_ref and verified run metadata.
- Any missing/malformed evidence, zero tests, test failures/errors, hash mismatch, runtime mismatch, timeout, or incomplete process cleanup => non-PASS.
- Caller output text and printed JSON never determine status.

### Stage 6 — Mutation loop
For an authorized disposable test Work only:
1. Run baseline and record run_id/hash/evidence.
2. Apply a deliberately small test-only mutation.
3. Run tests and verify FAIL with nonzero exit and evidence.
4. Revert/patch the test mutation through the authorized Work mutation path.
5. Run again and verify PASS with a new run_id, new exact source hash and separate evidence.
6. Verify the baseline, failure and final records are all immutable and cross-linked.
Never mutate MAIN SOURCE or a production Work for this acceptance case.

## B. Required acceptance matrix
| ID | Case | Expected result |
|---|---|---|
| A01 | Authorized Work, valid RUN_TESTS | PASS only with nonzero test count + protected evidence |
| A02 | Missing/forged principal | DENIED before side effects |
| A03 | Spoofed identity_id / authorized=true | caller value ignored; Core principal wins |
| A04 | Cross-Work status/output/cancel | NOT_FOUND or DENIED without leaking existence |
| A05 | Traversal, drive, UNC, ADS, Unicode control/confusable | rejected before file open |
| A06 | Symlink/reparse escape and path race | rejected by filesystem adapter |
| A07 | Source hash mismatch | BLOCKED before execution |
| A08 | Zero discovered tests | FAIL, never PASS |
| A09 | Test failure/error with process exit 0 | FAIL, never PASS |
| A10 | Intentional nonzero process exit | FAIL with actual exit code |
| A11 | Infinite loop / child process | TIMEOUT/CANCELLED only after process-tree cleanup evidence |
| A12 | Secret, host file, loopback and outbound network probe | OS policy denies; no secret value in output |
| A13 | Output/file/concurrency/resource flood | bounded and recorded |
| A14 | Evidence overwrite/delete attempt | denied; integrity/readback remains stable |
| A15 | Runtime absent/stale/unknown identity | BLOCKED; no alternate host fallback |
| A16 | Baseline -> mutation FAIL -> patch -> PASS | distinct run IDs, hashes, verified protected evidence |
| A17 | Status/output/cancel without ownership | denied/not-found and no side effect |
| A18 | malformed tool/runtime response | FAIL/BLOCKED, never PASS |

## C. Owners and proof
- Ka: coordinate implementation, maintain the contract, consolidate evidence and keep gates honest.
- Cla: independent threat-model review, security test matrix and explicit veto/NO-GO findings.
- Go: independent E2E execution through the real deployed MCP entry point after gates are ready; attach raw logs, command, exit code, source/runtime identities and evidence readback.
- Runtime owner: expose existing canonical runtime through an authenticated Core route and supply isolation proof; do not create a parallel execution host.
- Vinh: final approval for enabling execution and closing Work 28.

## D. Current gate state
- Source contract and tests: written/readback verified, not executed by approved runner.
- Deployed PC MCP/Core SHA and registered live tool list: BLOCKED pending read-only PC evidence.
- Auth principal + Core WorkContext execution route: BLOCKED.
- OS isolation/process-tree cleanup/protected evidence: BLOCKED.
- Full automatic E2E: BLOCKED.
- Work 28 remains ACTIVE / NOT LOCKED.
