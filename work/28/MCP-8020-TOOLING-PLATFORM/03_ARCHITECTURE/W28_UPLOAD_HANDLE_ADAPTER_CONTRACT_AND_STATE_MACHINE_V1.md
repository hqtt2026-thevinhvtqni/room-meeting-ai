# W28 Upload Handle Adapter Contract & State Machine — V1

**Date:** 2026-11-27 (UTC+07:00)  
**Owner:** Ka — delegated W28 implementation/architecture owner  
**Status:** DESIGN ONLY — NOT IMPLEMENTED / NOT ACCEPTED  
**Branch:** `ka/w28-f01-handle-backend-20261127-r5`  
**Canonical base:** `3271896052962ce188994e07ac687a429f8048de`

## 1. Decision and non-goals

The current `SandboxBinaryUploadService` remains pathname-based. The Linux handle filesystem module is a primitive prototype and is not an adapter for the service. F01 remains BLOCKED.

The remediation is one coherent filesystem boundary used by initialization, startup reconciliation, begin, chunk, digest/readback, finalize/recovery, abort/cleanup and per-upload cross-process locking. No security-sensitive path operation may bypass it.

This document does not authorize merge, rebase, MCP registration, deployment, live upload, Execution Gate opening or release. Windows upload remains unavailable and MUST fail closed until a native handle-relative backend is implemented and independently verified. No pathname fallback is permitted.

## 2. Trust and ownership model

- The configured Sandbox root is opened once as a trusted directory handle by walking from the filesystem root without following symlinks/reparse points. The service retains ownership of this root handle for its lifetime.
- A request obtains a Core-issued grant before any filesystem mutation. The grant binds principal, session, canonical Work, Sandbox Work mapping/version, destination, capability, limits, expiry and revocation epoch.
- The adapter accepts only validated relative components. It never accepts an arbitrary absolute destination from the request or ledger as an authority to escape the pinned Sandbox root.
- A Work handle is opened relative to the pinned Sandbox root. Every nested directory is opened relative to its pinned parent; every file is opened relative to its pinned parent. No `resolve()`, `Path.exists()`, `Path.is_symlink()`, pathname `open()`, pathname `link()`, pathname `unlink()`, or pathname directory enumeration is permitted in the upload service's security boundary.
- Ledger paths are descriptive/audit metadata only. Recovery reconstructs a relative path from validated session fields and Core mapping; it does not trust persisted absolute path strings as authority.
- Handles are scoped and deterministically closed. The adapter must make descriptor ownership explicit and reject use-after-close.

## 3. Required adapter contract

The service depends on a protocol equivalent to the following. Names are conceptual; implementation may refine types without weakening guarantees.

| API | Required guarantee |
|---|---|
| `open_sandbox_root(configured_root)` | Pin root without following symlinks/reparse points; fail closed if guarantee unavailable |
| `open_work(root_handle, work_id, create=False)` | Open/create exactly one validated Work directory relative to root |
| `open_directory(parent_handle, components, create=False)` | Traverse every component relative to retained parent handles; reject symlink/reparse/non-directory |
| `open_regular_file(parent_handle, leaf, mode)` | No-follow open; verify regular-file type from the opened handle |
| `create_exclusive_file(parent_handle, leaf)` | Atomic exclusive create; return pinned read/write file handle |
| `read_at(file_handle, offset, length)` / `write_at(...)` / `truncate(...)` | Operate only on the pinned file object; enforce bounds; write durability as specified |
| `digest(file_handle)` / `stat_file(file_handle)` | Return size/digest/type from the opened object, not a re-resolved name |
| `enumerate_directory(directory_handle)` | Enumerate entries anchored to the pinned directory; each entry must be safely opened before acting on it |
| `publish_no_replace(staging_file_handle, staging_parent_handle, staging_leaf, destination_parent_handle, destination_leaf)` | Atomically publish the exact pinned staging object without replacing an existing destination; prove source identity at the publication primitive |
| `unlink_if_same_object(parent_handle, leaf, expected_identity)` | Remove only the expected entry/object; never unlink a replacement substituted after inspection |
| `fsync_file(file_handle)` / `fsync_directory(directory_handle)` | Expose required durability barriers and report unsupported/error as failure |
| `acquire_upload_lock(staging_directory_handle, lock_leaf)` | Cross-process lock anchored beneath pinned directory; lock identity is bound to upload ID and safely released |
| `close(handle)` | Idempotent ownership-safe close; no descriptor reuse/double-close |

All adapter failures are typed and fail closed. The service must not catch an adapter failure and retry the same operation using a pathname.

## 4. Publication primitive — explicit unresolved proof obligation

The current prototype's `os.link(source_name, destination_name, src_dir_fd=..., dst_dir_fd=...)` pins the parent directories but resolves the source by leaf name at call time. An attacker able to replace the staging directory entry can cause the link to publish a different object than the already-open staging file.

Therefore the current `promote_no_replace()` is NOT ACCEPTED as a proof of exact-source publication.

An implementation is acceptable only if it uses a platform primitive that atomically publishes the object identified by the retained staging file handle and enforces destination no-replace. On Linux, evaluate `linkat(AT_EMPTY_PATH)` or an equivalently proven primitive, including required capability/filesystem constraints. If the runtime/API cannot provide exact-handle publication, the adapter MUST return `ATOMIC_HANDLE_PUBLICATION_UNAVAILABLE` and the upload must remain blocked. A pathname-based hard-link plus post-hoc inode check is not sufficient because an unintended object could be transiently published.

After publication, verify destination identity against the pinned source handle (device/inode or platform file ID) and verify bytes by reading the destination handle. Destination cleanup after a failure must be conditional on the exact identity created by this operation; never blindly unlink the destination name.

## 5. Upload state machine and ordering

| Durable state | Allowed operation | Filesystem action | Ledger action | Recovery rule |
|---|---|---|---|---|
| none | begin | create exclusive staging object; fsync staging file and staging directory | atomically reserve quota + insert UPLOADING row | orphan created before ledger commit is quarantined, never silently adopted |
| UPLOADING | chunk | lock; verify pinned staging identity; write exact offset; fsync file | insert chunk receipt/update cursor in one transaction | if bytes reached disk but receipt did not, retry may rewrite same cursor under lock |
| UPLOADING | finalize | lock; verify exact byte coverage and digest using pinned file handle | transition UPLOADING→FINALIZING with expected digest | FINALIZING is durable intent; never abort/delete its only source |
| FINALIZING | publish/recover | publish exact staging object no-replace; fsync destination parent; read back destination handle; verify size/digest | transition FINALIZING→COMPLETED and release quota | if destination is exact verified object, complete; if staging is exact verified object and destination absent, retry publication; otherwise BLOCKED |
| UPLOADING | abort | lock; unlink staging only if identity matches ledger-bound pinned object; fsync parent | transition UPLOADING→ABORTED and release quota | cleanup uncertainty remains BLOCKED; do not claim aborted |
| COMPLETED | readback | open destination relative to pinned parent, verify regular file and receipt | no state mutation | mismatch is integrity incident; never delete/replace automatically |
| ABORTED | cleanup check | inspect only through pinned staging directory | no state mutation | unexpected object is quarantined/BLOCKED |

### Critical ordering rules

1. Begin: create staging → fsync staging file → fsync staging directory → commit ledger reservation/session. If ledger commit fails, remove only the exact created staging object; if cleanup cannot be proven, persist/report orphan quarantine.
2. Chunk: durable bytes first, then durable chunk receipt. The cross-process lock serializes filesystem and ledger cursor changes. A crash between the two permits idempotent rewrite of the same range only.
3. Finalize: verify complete byte coverage and digest → commit FINALIZING intent → atomic exact-object no-replace publication → fsync destination directory → destination-handle readback and digest → remove staging name only if same object (or account for same inode link semantics) → fsync staging directory → commit COMPLETED receipt/quota release.
4. Never delete a verified final destination merely because the COMPLETED ledger transaction failed. Keep FINALIZING and recover by inspecting exact object identity and digest. The prior rollback pattern that unlinks final after ledger failure is prohibited.
5. If publication succeeded but readback or cleanup fails, retain FINALIZING and all evidence needed for recovery. Do not convert uncertainty into ABORTED or COMPLETED.
6. Directory creation and rename/link durability must include parent-directory fsync at every newly created/published/deleted entry boundary.

## 6. Startup reconciliation and orphan policy

- Reconciliation runs before accepting new upload operations and uses only pinned root/Work/staging handles.
- Enumerate every Work directory under the pinned root, not only Works represented in the ledger.
- For each durable session, safely open and classify staging/final entries; verify regular-file type, object identity where recorded, byte count and digest. Never follow symlinks/reparse points.
- Unknown staging entries, identity mismatches, unexpected final entries, unreadable directories, missing parents and unsupported handle operations produce BLOCKED/quarantine records.
- Reconciliation must not delete unknown entries or infer a successful state from file existence alone.
- Quota rebuild is derived from durable ledger states only after filesystem reconciliation has classified each session; unresolved sessions remain reserved/blocked according to a documented conservative policy.
- Crash/fault-injection tests cover every boundary before and after each fsync and ledger commit.

## 7. Locking and concurrency

- Per-upload lock is created/opened relative to the pinned staging directory, with no-follow and regular-file validation.
- Lock key is derived from validated upload ID; lock file cannot be redirected by a replaced parent path.
- All chunk/finalize/recovery/abort paths acquire the same cross-process lock before re-reading the ledger row and obtaining a fresh Core grant.
- Lock acquisition failure, lock identity mismatch or uncertain release blocks the operation.
- Tests include independent service instances/processes, concurrent chunk/finalize/abort, lock entry replacement, process crash while holding lock, and restart recovery.

## 8. Platform acceptance gates

### Linux
- Directory-FD traversal with `O_DIRECTORY|O_NOFOLLOW`; file open with `O_NOFOLLOW`; fstat regular-file checks; pwrite/pread/ftruncate; file and directory fsync.
- Exact-source atomic no-replace publication must be proven for the actual filesystem and runtime. If not supported, upload remains unavailable.
- Adversarial tests replace Sandbox root, Work root, nested parent, staging directory and staging leaf at controlled barriers.

### Windows
- No current backend exists. Required design must use native handles, open reparse points without traversing them, validate file IDs/reparse tags from handles, retain ancestor handles, and perform child creation/open relative to trusted parent handles (e.g. a reviewed `NtCreateFile` RootDirectory design or equivalent).
- Atomic exact-handle no-replace publication and directory durability semantics must be documented and tested on supported Windows filesystems.
- Until all conditions pass, constructor/operation returns a stable fail-closed unsupported-platform error. No `Path` fallback and no claim of Windows upload support.

## 9. Required adversarial test matrix

1. Swap Sandbox root after validation and during initialization.
2. Swap Work root after grant validation and between directory open steps.
3. Replace nested destination parent with symlink/reparse point.
4. Replace `.upload-staging` directory and staging leaf before create/open/write/digest/publish/cleanup.
5. Replace staging leaf after its handle is opened; prove published object is still the opened object or operation blocks without publishing.
6. Pre-create destination; verify no-replace and no overwrite.
7. Replace destination around publication/readback/cleanup; ensure cleanup never removes an unrelated object.
8. Inject crashes after staging create, each chunk write, chunk receipt, FINALIZING commit, publication, destination fsync, readback, staging unlink and COMPLETED commit.
9. Inject SQLite failures at begin, chunk receipt, FINALIZING and COMPLETED transitions.
10. Replace lock leaf/parent and race independent service processes.
11. Exercise symlink, hardlink, mount boundary, cross-Work escape, permission denial, unsupported fs primitive and directory fsync failure.
12. Run equivalent Windows reparse-point/file-ID/handle-relative tests before Windows support can be enabled.

Each test records exact OS/kernel/filesystem, Python/runtime version, source SHA, command, raw output and whether the platform primitive is supported. No test result transfers across a changed code SHA.

## 10. Implementation sequence and exit criteria

1. Freeze this contract and review every primitive's security proof obligations.
2. Implement a service-facing adapter protocol plus Linux backend, including exact-handle no-replace publication or fail-closed unsupported behavior.
3. Add adapter unit tests and adversarial race/fault-injection tests before integrating service paths.
4. Refactor the service so all nine lifecycle boundaries use the adapter; remove security-boundary pathname operations and absolute paths as authority.
5. Rework ledger schema/identity metadata and crash recovery only where needed; preserve append-only audit.
6. Run focused tests, full Work28 suite and exact-SHA Linux CI; keep Windows upload fail-closed until native implementation exists.
7. Obtain independent security review and independent QA on the exact final SHA.
8. Only after all findings are closed may PR status/acceptance be reconsidered. This document itself is design evidence only.

**Current disposition:** F01 BLOCKED; F02 PARTIAL / NOT VERIFIED; F03 BLOCKED; F04 BLOCKED; PR #85 DRAFT / UNMERGED; Execution Gate CLOSED; Work28 ACTIVE / INTEGRATION BLOCKED / NOT RELEASED.


### 4.1 Linux `linkat(AT_EMPTY_PATH)` feasibility — review result (not runtime-verified)

Linux `linkat(oldfd, "", newdirfd, newleaf, AT_EMPTY_PATH)` is the candidate because the source is named by an already-open file descriptor rather than by a mutable staging leaf. When the kernel accepts this operation, the destination hard link refers to the object held by that descriptor; destination creation is no-replace because an existing destination entry causes the link operation to fail with `EEXIST`.

This is a **conditional candidate, not an unconditional portable solution**:

- `AT_EMPTY_PATH` is Linux-specific and requires the relevant GNU feature definitions at the C interface.
- The documented `AT_EMPTY_PATH` route requires `CAP_DAC_READ_SEARCH`; ordinary service processes must not assume they possess this capability. Capability availability must be checked in the actual service execution context, not inferred from root in a developer shell.
- The source and destination must be on the same filesystem for a hard link. Cross-device failure is a hard failure, not a reason to copy bytes or fall back to a pathname rename.
- The target filesystem must support hard links and the required durability semantics. The exact kernel, mount, filesystem and security policy must be part of the acceptance record.
- The operation must be exercised using the actual Python/runtime binding or a narrowly reviewed syscall wrapper. A feature flag or presence of a constant does not prove that the kernel call is available or authorized.
- A `/proc/self/fd/N` + `AT_SYMLINK_FOLLOW` route is a separate candidate only; it depends on procfs and must receive its own threat analysis and adversarial tests. It is not an automatic fallback.

**Important limitation:** exact-handle publication solves source-object selection, but does not by itself make deletion of the staging directory entry safe. Linux has no general unlink-by-open-file-descriptor primitive. If an attacker can replace the staging leaf, a later `unlinkat(staging_dir_fd, staging_leaf)` can delete the replacement. The design must therefore either (a) establish and test an explicit directory ownership/permission boundary that prevents untrusted replacement for the entire upload lifecycle, or (b) retain the extra staging link and quarantine/reconcile it without unsafe unlink. A pre-unlink `fstatat`/inode comparison followed by `unlinkat` is still TOCTOU and is not an acceptable proof.

**Disposition:** do not implement publication or staging cleanup based only on the API name. First run a capability/filesystem matrix in the actual target service identity, prove exact source identity and destination no-replace, and separately prove staging-name cleanup safety. If any proof is unavailable, return `ATOMIC_HANDLE_PUBLICATION_UNAVAILABLE` / cleanup-blocked and retain FINALIZING; never silently downgrade to pathname operations.
