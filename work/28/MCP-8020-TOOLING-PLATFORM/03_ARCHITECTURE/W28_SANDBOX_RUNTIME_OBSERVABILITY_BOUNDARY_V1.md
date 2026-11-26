# W28 Sandbox Runtime Observability Boundary — V1

**Date:** 2026-11-27 (UTC+07:00)  
**Owner:** Ka — delegated W28 implementation / architecture owner  
**Status:** EVIDENCE LIMITATION / READ-ONLY AUDIT — NOT RUNTIME ACCEPTANCE  
**Branch:** `ka/w28-f01-handle-backend-20261127-r5`

## 1. Question

Can the currently available ROOM HOP MCP 8030 Sandbox tools establish the effective OS identity, Linux capabilities, mount namespace, filesystem type, ACLs and directory ownership of the process that would execute the W28 binary upload service?

## 2. Tools actually available and exercised

The available MCP 8030 Sandbox surface exposes:
- Work discovery/listing.
- Listing files and directories in a Work Sandbox.
- Reading, creating, writing, appending and deleting text files.

This review exercised:
- Sandbox Work discovery (77 Works returned).
- Listing Work `28`, which exposes the existing Work28 Sandbox project tree.
- Read attempts for common Work 28 root manifest/readme paths; those paths returned FileNotFound and no runtime metadata.
- No shell, process-inspection, stat/fstat, getfacl, findmnt, mountinfo, /proc, capability, syscall or arbitrary Python execution action is exposed by the available MCP 8030 tool surface.

## 3. What this evidence proves — and does not prove

It proves that the connector can discover Work sandboxes and inspect their virtual file entries/content.

It does NOT prove:
- The host OS or kernel of the upload-service process.
- The effective UID/GID, supplementary groups or Linux capabilities.
- The process's mount namespace, mount flags, filesystem type or device IDs.
- Ownership/mode/ACL of the actual host Sandbox root and staging directories.
- Whether another process shares the service UID or inherited directory handles.
- Whether `linkat(AT_EMPTY_PATH)` is permitted in the target process.
- Whether directory fsync, hard links or required publication semantics work on the target filesystem.

A Work Sandbox file listing is not an OS-level process or filesystem inspection. File metadata and directory names in the virtual Work namespace must not be treated as host security evidence.

## 4. Safe conclusion

The currently available MCP 8030 Sandbox interface is insufficient for the requested runtime capability matrix. No attempt was made to infer host properties from the connector's own execution environment, and no write/delete/execute probe was run against the actual service host.

Therefore:
- Runtime identity/capability/filesystem evidence remains **NOT OBSERVED**.
- The actual service staging namespace trust boundary remains **UNPROVEN**.
- F01 remains BLOCKED; upload remains fail-closed.
- Do not use MCP 8020 sandbox_read: it is outside the authorized W28 operational path and is not a substitute for approved host diagnostics.
- To proceed, an authorized read-only diagnostic must run inside the exact upload-service process/container context and return the evidence fields listed in the Threat Model document. If no approved execution path exists, record the blocker and do not simulate the evidence.

## 5. Required diagnostic evidence (read-only)

An authorized operator or approved host diagnostic must capture:
1. Process identity: PID, executable/service identity, UID, GID, supplementary groups.
2. Linux capabilities: effective, permitted, inheritable, bounding and ambient sets; user namespace context.
3. Kernel/runtime: kernel release, architecture, Python version and syscall wrapper version.
4. Filesystem/mount: mount namespace ID, mountinfo entry, filesystem type, mount flags, device and mount IDs for Sandbox root, Work and staging.
5. Namespace permissions: owner, mode, effective ACLs and parent-directory permissions, captured through opened handles where possible.
6. Isolation: whether untrusted workloads share service UID, groups, writable mounts or inherited handles.
7. Publication probe: exact syscall result/errno and source/destination file identity in a disposable isolated directory, only after separate authorization.

Do not collect secrets, environment variables, tokens or unrelated process command-line data. No mutation or capability elevation is part of this read-only diagnostic.

**Disposition:** MCP 8030 file Sandbox is NOT a host runtime introspection channel. Runtime matrix cannot be completed from current tools. F01 BLOCKED / Execution Gate CLOSED / NOT RELEASED.
