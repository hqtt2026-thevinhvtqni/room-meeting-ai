# W28 Staging Directory Threat Model & Linux Capability Matrix — V1

**Date:** 2026-11-27 (UTC+07:00)  
**Owner:** Ka — delegated W28 implementation / architecture owner  
**Status:** REVIEW DESIGN — NOT IMPLEMENTED / NOT ACCEPTED  
**Branch:** `ka/w28-f01-handle-backend-20261127-r5`  
**Canonical base:** `3271896052962ce188994e07ac687a429f8048de`

## 1. Purpose and decision

This document addresses the unresolved cleanup threat after descriptor-based publication: Linux does not provide a general unlink-by-open-file-descriptor operation. It defines when a staging directory can be treated as a trusted namespace and when upload must remain blocked.

**Decision:** no current evidence proves that the deployed Sandbox staging directory has the required ownership, ACL, mount and process-isolation properties. Therefore this document does not authorize enabling staging cleanup or Linux upload. F01 remains BLOCKED.

## 2. Assets and security invariants

Assets:
- Pinned Sandbox root and Work directory handles.
- Upload staging file object and its file identity.
- Final destination namespace and file object.
- Upload ledger state, quota reservation, digest and receipt.
- Cross-process lock and recovery evidence.

Invariants:
1. Only the exact staging object created for the upload may be published.
2. No operation may follow a symlink or reparse point outside the pinned hierarchy.
3. Cleanup must never unlink a replacement object occupying the staging leaf.
4. A final destination must never be overwritten or removed because a later ledger transaction failed.
5. Uncertainty in publication, cleanup, identity or durability leaves the session FINALIZING/BLOCKED; it must not be converted to COMPLETED or ABORTED.
6. No pathname fallback is allowed.

## 3. Threat actors and trust boundary

### In-scope
- Untrusted remote upload caller controlling request fields, relative destination, upload timing, chunk ordering and retries.
- Concurrent independent upload requests and service instances.
- Other OS identities that can attempt to mutate Sandbox directories if permissions/ACLs accidentally grant access.
- Symlink/reparse/hard-link substitution, path traversal, pre-created destination, crash/restart and filesystem error.
- Process termination at every filesystem/ledger durability boundary.

### Explicitly outside the filesystem guarantee
- A malicious process running with the same effective OS identity and equivalent filesystem privileges as the upload service.
- Host root/administrator, kernel compromise, malicious storage firmware, or an operator with authority to rewrite the Sandbox tree.

These exclusions are not assumptions to leave undocumented: deployment must ensure untrusted workloads do not execute under the upload service identity and do not receive its directory handles or writable mounts. If that separation cannot be demonstrated, the staging namespace is not trusted and upload remains disabled.

## 4. Required staging namespace boundary

A trusted staging directory is acceptable only if all conditions are proven in the actual runtime:

1. It is created beneath a pinned Work directory using descriptor-relative `mkdirat` semantics and a fixed service-owned name.
2. It is owned by the dedicated upload-service UID and has restrictive mode (normally 0700); effective ACLs grant write/rename/unlink only to that service identity and explicitly approved administrators.
3. Parent Work directory permissions/ACLs prevent untrusted identities from renaming or replacing the staging directory entry.
4. No untrusted process shares the service UID, supplementary groups, writable mount namespace, or inherited directory/file descriptors.
5. The directory is not writable through a shared host bind mount, sidecar, container volume, sync client, or other service identity.
6. The service validates ownership, mode, ACL and mount identity from opened handles at startup and before accepting uploads; inability to inspect a required property is a hard failure.
7. The service never relaxes these permissions for convenience and never changes ownership based on request data.
8. Service restart preserves the same trust boundary; reconciliation reopens the directory without following links and revalidates it.

Mode 0700 alone is insufficient if another process shares the service UID, if ACLs grant additional access, if the parent can be replaced, or if privileged actors are in scope. A sticky bit is not a substitute for a private service-owned directory.

### Cleanup rule

If the trusted namespace proof is satisfied and maintained for the full upload lifecycle, the service may unlink the staging leaf relative to its pinned staging-directory FD, because no untrusted actor within the declared threat model can replace that leaf. It must still verify expected identity immediately before unlink for detection, fsync the staging directory after unlink, and treat any mismatch as an incident.

If any namespace condition is absent or unverifiable, the service MUST NOT unlink by leaf name. It must preserve the entry and mark cleanup as QUARANTINED/BLOCKED for privileged reconciliation. A pre-unlink inode comparison does not repair a hostile-writer TOCTOU race.

## 5. Linux publication capability matrix

The following are required runtime observations, not assumptions. Every row must be measured inside the exact service process identity, container/mount namespace and target filesystem.

| Dimension | Evidence required | Fail-closed condition |
|---|---|---|
| Kernel/runtime | kernel release, architecture, Python version, syscall/API binding version | unsupported or unrecorded environment |
| Effective identity | UID, GID, supplementary groups, effective/permitted/inheritable/bounding capabilities | identity/capability differs from approved deployment |
| `AT_EMPTY_PATH` | actual syscall invocation using the already-open staging FD | `EPERM`, `EINVAL`, `ENOSYS`, binding unavailable or source identity not exact |
| Capability | prove whether `CAP_DAC_READ_SEARCH` is available and permitted in this process/user namespace | capability absent where required; do not silently elevate |
| Filesystem | source/destination filesystem type, mount ID, device ID, mount flags | cross-device, unknown filesystem, or unsupported hard links |
| Destination no-replace | pre-existing destination and concurrent creation race tests | overwrite or replacement possible |
| Source identity | compare opened source handle file ID with published destination handle file ID | mismatch or identity unavailable |
| Durability | fsync staging file, destination directory, staging directory; injected failures | unsupported/error or undocumented ordering |
| Namespace ownership | owner, mode, ACL, parent permissions, mount exposure, same-UID process inventory | any untrusted writer can mutate staging namespace |
| Recovery | crash after publication and before unlink/ledger commit | recovery cannot distinguish exact object or preserve FINALIZING |

Do not infer capability from running a developer shell as root. Do not add `CAP_DAC_READ_SEARCH` to production merely to make a test pass without a separate least-privilege/security decision. A syscall wrapper must be narrowly scoped, reviewed and tested; a Python constant or feature probe is not proof.

## 6. Adversarial test plan

Run tests in an isolated disposable Sandbox and record exact source SHA, command, raw output, OS/kernel, Python, filesystem/mount, UID/GID/capabilities and ACL state.

A. Namespace isolation:
- Different UID attempts to list, create, rename, unlink or replace staging entries.
- Same-UID helper process attempts the same; expected result documents the explicit trust boundary (if it succeeds, same-UID process is trusted and must not host untrusted code).
- Parent Work directory rename/replacement attempts while service retains its handle.
- ACL/group/mount changes before startup and during service lifetime.
- Restart and reconciliation with directory owner/mode/ACL changed.

B. Publication:
- Open staging FD, replace staging leaf, then invoke candidate exact-FD publication; destination must reference the opened FD object or publication must fail without publishing.
- Pre-create destination and race another creator; no overwrite.
- Force `EPERM`, `EXDEV`, unsupported filesystem, missing procfs (for any separately considered procfs route), fsync errors and short/failed syscall behavior.
- Verify source and destination object identity from handles.

C. Cleanup:
- Replace staging leaf before cleanup from an in-scope identity; operation must be prevented by namespace permissions.
- Attempt replacement from an excluded same-UID helper to document why same-UID execution is within service trust domain.
- Inject failure after destination publication but before staging cleanup; recovery remains FINALIZING and does not delete destination.
- Inject staging directory fsync failure; report cleanup durability uncertain and block completion.

D. Ledger and crash:
- Fail SQLite transitions at begin, chunk receipt, FINALIZING and COMPLETED.
- Crash after each file/directory fsync, publication, readback and cleanup.
- Confirm quota remains reserved conservatively for uncertain sessions and no unknown orphan is silently adopted/deleted.

## 7. Acceptance evidence template

No result is accepted unless it includes:
- Exact commit/source SHA and test artifact.
- Exact target OS/kernel, runtime, filesystem, mount and container namespace.
- Effective UID/GID/groups/capabilities and relevant ACL/ownership/mode evidence.
- Raw syscall result and errno for publication.
- Source/destination file identity evidence from open handles.
- Race/fault-injection outputs and recovery ledger snapshots.
- Independent review of the test harness and threat-boundary assumptions.

## 8. Current disposition and next steps

- The current prototype still publishes by mutable source leaf via `os.link(..., src_dir_fd=...)`; it does not use the pinned staging file FD for publication.
- No target-runtime capability or filesystem experiment has been run as part of this review.
- No evidence currently establishes a private staging namespace in the deployed Sandbox.
- Therefore no adapter integration or upload enablement is authorized by this document.
- Next: identify the actual Sandbox service runtime identity/mount/filesystem configuration, then run the isolated capability and namespace matrix. If that environment cannot be inspected safely, retain fail-closed behavior.

**STATUS:** THREAT MODEL RECORDED / RUNTIME EVIDENCE PENDING / F01 BLOCKED / F02 PARTIAL / F03-F04 BLOCKED / PR #85 DRAFT-UNMERGED / EXECUTION GATE CLOSED / NOT RELEASED.
