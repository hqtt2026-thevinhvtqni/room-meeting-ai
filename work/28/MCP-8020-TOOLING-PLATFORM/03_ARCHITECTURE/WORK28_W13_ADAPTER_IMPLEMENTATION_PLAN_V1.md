# Work 28 — W13 pinned-snapshot adapter implementation plan v1

- Date: 2026-10-25
- Owner: Xu (AI-01), architecture and integration coordination
- Status: PARTIAL IMPLEMENTATION / NOT WIRED / NOT RELEASED
- Scope: adapt Work 28's narrow execution contract to the existing Work 13 canonical Execution Host. Do not create a second host; do not modify Work 12's frozen contract.

## 1. Evidence-based current state

Static review of the current `main` source found:

- `wee_work13_adapter.py` forwards a caller-supplied command list to `RealExecutionHost.execute()`.
- `wee/bridge/real_host.py` runs `subprocess.run(command, cwd=workspace, ...)` without a timeout argument and does not bind the command to an expected source hash or immutable source snapshot.
- The host's process cleanup terminates tracked services but does not wait for verified process-tree exit.
- `wee/models.py` has Work binding/context fields but no `expected_source_sha256` or immutable snapshot reference.
- Existing `tests/test_work13_wee_integration.py` uses a temporary workspace and executes a Python command; this is local integration coverage, not proof of authenticated Core → HTTP :8031 → approved runtime end-to-end behavior.

These are static source findings. No live host request was sent and no runtime security claim is made.

## 2. Required boundary

The public Work 28 request remains exactly:

- `work_id`
- Work-relative `entry_path`
- `operation`: `RUN_SCRIPT` or `RUN_TESTS`
- `expected_source_sha256`
- optional bounded `timeout_seconds`

Do not accept public `command`, `script`, `argv`, `cwd`, `shell`, `env`, `principal`, or `authorized` fields. Caller identity must come from authenticated server middleware; Work permission must be decided by trusted Core, not a caller-supplied boolean.

## 3. Implementation sequence

1. **Trusted Work resolver** — resolve the requested Work and authenticated caller using canonical Core authority. Deny by default when the caller/Work binding is missing or ambiguous.
2. **Snapshot builder** — resolve `entry_path` beneath the authorized Work root; reject symlink/reparse-point escapes and non-regular files; create a read-only immutable snapshot; calculate SHA-256 over the exact bytes to be executed; compare to `expected_source_sha256` before dispatch.
3. **Narrow W13 operation mapping** — map `RUN_SCRIPT` to the approved interpreter plus the snapshot entry file; map `RUN_TESTS` only to a Work-bound, approved test entrypoint. Never forward a caller-provided command vector. Add enforced timeout and process-tree containment/cleanup to the existing W13 host implementation.
4. **Pinned runtime verification** — obtain runtime identity from trusted deployment configuration/attestation, compare it to the approved identity before dispatch and in the result. Do not treat a returned PID/build hash alone as trusted approval.
5. **Result and evidence binding** — require request ID, run ID, Work ID, snapshot reference, source hash, approved runtime identity, integer exit code, evidence reference, and verified process-tree cleanup. For `RUN_TESTS`, require total > 0 and failed = errors = 0 before PASS.
6. **Negative tests first** — unauthorized caller, cross-Work path, traversal, symlink/reparse escape, changed source after snapshot, hash mismatch, runtime mismatch, timeout, failed child cleanup, missing evidence, nonzero exit, empty test suite, and false/boolean numeric fields must fail closed.
7. **Live authorized E2E** — only after unit tests pass, use a controlled authorized test Work through the canonical Core → existing W13 HTTP :8031 route; prove request-to-evidence identity and exact snapshot hash; verify cleanup after both success and timeout.
8. **Activation gate** — only after all evidence is reviewed may the MCP service and connector guard be changed together. Until then all seven public execution/evidence tools remain `NOT_IMPLEMENTED`.


## 3A. Implementation progress (2026-10-25)

**Implemented and regression-tested in the Work 28 branch:**
- `execution_host/work28_contract.py` — strict request schema plus Work-bound source snapshot creation, exact SHA-256 verification, symlink-component rejection, and read-only snapshot permissions.
- `05_TEST/test_w13_contract_boundary.py` — rejection cases for caller-controlled command/authority/cwd/shell fields, unsafe paths, invalid operation/hash/timeout, Work mismatch, hash mismatch, and symlink paths.
- CI run [40150494323](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/40150494323) passed: 200 tests, 4 skipped.
- Identical staged source file is also present on branch `work/13-execution-host-hardening` for the bounded W13 continuation.

**Still not implemented or verified:**
- Trusted Core caller authentication and authoritative Work-root resolution in the live HTTP handler.
- Execution of the exact snapshot through a constrained runtime entrypoint.
- Independently pinned runtime identity at dispatch and result verification.
- Verified process-tree containment/cleanup, including timeout behavior.
- Authenticated live Core → existing W13 HTTP :8031 end-to-end test and evidence.
- Wiring into the MCP v54 service and connector.

The staged module is intentionally not wired to `/execute`; the current command-oriented route remains incompatible. Its read-only file permissions are defense-in-depth, not OS-enforced immutable storage. CI proves only repository unit/regression tests, not live execution security.

## 4. Acceptance criteria

- No caller-controlled command or authority fields cross the public API.
- No execution occurs before trusted authorization and source-hash verification.
- The exact immutable snapshot whose hash was checked is the one executed.
- The runtime identity matches an independently approved identity.
- Timeouts stop the entire process tree and cleanup is verified, not inferred from a terminate call.
- Results and evidence bind to the same request, run, Work, source hash, snapshot, and runtime.
- CI passes all unit/regression tests; live authorized E2E produces inspectable evidence.
- No new execution host is created; Work 12 remains unchanged.

## 5. Current decision

**BLOCKED for live activation.** Work 28's staged adapter is only a fail-closed policy seam with injected dependencies. Current W13's command-oriented interface is not compatible with the narrow Work 28 contract. Do not wire it directly and do not mark execution tools implemented until the required components and evidence exist.
