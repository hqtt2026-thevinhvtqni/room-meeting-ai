# F01-W28-20261126-001 — HANDLE-ANCHORED FILESYSTEM REMEDIATION DESIGN

**Document ID:** F01-W28-20261126-001  
**Priority / read order:** P0 / 1  
**Name:** Ka  
**Title:** Delegated Work 28 Operational Owner / Remediation Lead  
**Date-Time:** 2026-11-26 20:xx +07 (Asia/Ho_Chi_Minh)  
**Status:** DESIGN BASELINE — NOT IMPLEMENTED / NOT APPROVED FOR RELEASE  
**Scope:** WP3 binary upload F01 only

## 1. Evidence and threat

PR #81 exact candidate SHA `305305bc7a9c84b144743890375ed971a618d11e` contains the deterministic regression `test_begin_rejects_parent_swap_after_validation`. Workflow #513 reproduced the vulnerability on both native Linux and Windows:
- Linux job `139721601541`: failure because `UploadError` was not raised.
- Windows job `139721601602`: same failure.
- Unit/regression job `139721601414`: 375 tests, one failure from the same regression.

The baseline performs pathname validation and later separate pathname operations. Relevant attack surfaces include Work-root creation, destination parent creation, staging creation, chunk file open/write, startup reconciliation, finalizing recovery, final promotion, readback, cleanup and abort. A single safe check in `begin()` is insufficient; all file operations in the lifecycle must share the same containment model.

## 2. Non-negotiable invariants

1. No filesystem operation may trust a prior pathname-only `resolve()`, `is_symlink()`, `exists()` or `stat()` check as proof of containment.
2. Resolve and hold a trusted Sandbox-root directory handle; all Work and descendant traversal must be anchored to it.
3. Every traversed component must be opened without following symlinks/reparse points. Verify the opened object is a directory where required.
4. Keep the relevant parent handles alive through create/open/read/write/promote/unlink. A path replacement after handle acquisition must not redirect the operation.
5. Final promotion must be atomic no-replace, relative to verified parent handles. Readback and cleanup must operate on the same verified objects/handles.
6. If the platform cannot provide the required primitive or invariant, fail closed before mutating the filesystem. Never fall back to pathname-only operations.
7. Work identity and destination authorization continue to come from Core; this design does not create a local authority or change the grant contract.

## 3. Linux backend

Use directory file descriptors and descriptor-relative operations:
- Open the configured Sandbox root once with `O_DIRECTORY | O_CLOEXEC | O_NOFOLLOW`; retain the descriptor for service lifetime.
- Open/create Work directories relative to the root descriptor. Use `openat` semantics with `O_DIRECTORY | O_NOFOLLOW | O_CLOEXEC`; after creation, reopen and validate the handle.
- Traverse destination parents one segment at a time, retaining each required parent descriptor; reject symlinks and non-directories.
- Create staging directory and staging file relative to the Work/staging directory descriptors with `mkdirat` / `openat`, `O_CREAT | O_EXCL | O_NOFOLLOW`.
- Chunk writes use the already-open staging file descriptor (or securely reopen relative to a pinned staging directory); use `pwrite`/offset-safe writes and `fsync`.
- Promote with descriptor-relative no-replace semantics (`linkat` or a supported `renameat2(RENAME_NOREPLACE)` path); reject if the primitive is unavailable.
- Readback, unlink and cleanup use descriptors/dirfds; fsync affected files and directories where durability requires it.
- Do not persist absolute path strings as authority. Persist logical Work ID + normalized relative destination + opaque staging leaf; derive and re-open through the safe backend after restart.

## 4. Windows backend

Python pathname APIs alone are not sufficient. Implement a native handle backend:
- Open Sandbox root and each descendant directory using `CreateFileW` with directory semantics, `FILE_FLAG_OPEN_REPARSE_POINT`, and sharing flags that prevent delete/rename replacement while the handle is relied upon.
- Query handle metadata (file attributes/reparse tag and stable file identity) and reject any reparse point or non-directory component.
- Hold root, Work, destination-parent and staging-parent handles throughout each operation so a concurrent rename/replacement cannot redirect the operation.
- Create/open files relative to the validated directory handle using a native handle-relative primitive (e.g. carefully reviewed `NtCreateFile` with `RootDirectory`) or a demonstrated equivalent that preserves the parent-handle invariant.
- Use a no-replace promotion primitive and verify destination identity/readback through the resulting handle. Do not use a check-then-`os.link`/path rename fallback.
- If native handle-relative creation or atomic no-replace semantics cannot be established and tested on supported Windows versions, the Windows backend must return a typed fail-closed error before any upload mutation. Windows functional support remains BLOCKED.

## 5. Lifecycle coverage matrix

| Operation | Required safe primitive | Adversarial verification |
|---|---|---|
| Work root open/create | Root dirfd / root handle + no-follow child open | Work-root replacement, symlink/reparse point |
| Destination parent | Segment-by-segment anchored traversal | Parent swap at each depth, traversal and cross-Work |
| Staging create | Relative exclusive no-follow create | Staging-dir swap and pre-created symlink |
| Chunk write | Pinned file handle / pwrite | Replace staging path during write; verify original inode/handle only |
| Startup reconciliation | Safe traversal + handle reads/truncate | Swap Work/staging/final during scan and recovery |
| Finalize/recovery | Pinned staging/final parents; atomic no-replace | Parent swap, destination race, reparse-point injection |
| Readback | Read exact promoted handle/object | Replace pathname after promotion; verify object identity |
| Abort/cleanup | Relative unlink under pinned parent | Swap staging parent before unlink |

## 6. Test requirements

- Deterministic race hooks at the boundary after acquiring a directory handle and before the next operation; assert an attacker-controlled replacement cannot redirect writes outside the original Work directory.
- Linux: symlinked Work root, nested symlink, parent replacement, cross-Work escape, staging replacement, final destination race and concurrent rename tests.
- Windows: directory reparse point/junction, parent rename/replacement, nested reparse point, staging/final replacement, handle sharing/rename denial, and atomic no-replace race tests on native Windows runners.
- Tests must assert both the denial/result and filesystem side effects (outside directory remains untouched; no unauthorized final object).
- Run the full upload suite on native Linux and Windows at the exact PR head. No skipped platform suite may be counted as a pass for functional support.
- Independent An QA and a separately assigned security reviewer must review the final exact-SHA evidence.

## 7. Implementation order

1. Introduce a small internal filesystem backend interface with explicit open-root, open-work, open-parent, create-staging, open-staging, read/write, promote-no-replace, readback and unlink methods.
2. Implement and test Linux backend with dirfd operations.
3. Implement Windows native handle backend and prove reparse-point and rename invariants. Until then, Windows mutation is fail-closed and Work 28 remains blocked.
4. Refactor begin/chunk/finalize/recovery/reconciliation/abort to use only the backend. Remove pathname-only mutation/read operations from the upload service.
5. Add the full adversarial matrix and rerun exact-SHA CI.
6. Obtain independent QA and security dispositions; only then reconsider F01 status.

## 8. Explicit exclusions

- This is not approval of Xu's proposed Core upload contract; F03 remains independently blocked.
- This does not register an MCP :8030 tool or prove a deployed raw-byte transport; F04 remains blocked.
- This does not close durability/recovery gaps; F02 remains partial / not verified.
- No live Sandbox upload, merge, registration, deployment, Execution Gate opening or release is authorized.

**Decision:** Treat the path-based upload engine as unsafe. Replace the filesystem access layer end-to-end; do not patch isolated path checks.  
**Signed:** Ka — Delegated Work 28 Operational Owner / Remediation Lead
