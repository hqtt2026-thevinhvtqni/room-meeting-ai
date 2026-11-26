# F01-W28-20261126-002 — Path-Based Lifecycle Audit

**Priority:** P0 / Read order 1 — F01 security blocker  
**Name:** Ka  
**Title:** Delegated Work 28 Operational Owner / Remediation Lead  
**Date-Time:** 2026-11-26 20:xx +07 (Asia/Ho_Chi_Minh)  
**Scope:** Exact PR #82 head `f0c52ae0ceca3edc1708b20f8d67022f576d4774`; source `04_CODE/sandbox_binary_upload_v1.py`; native Linux/Windows upload lifecycle  
**Classification:** Technical audit evidence — NOT implementation, NOT approval

## 1. Executive finding

The current candidate remains path-based throughout the upload lifecycle. The existing `no_symlinks()` helper performs pathname checks and does not pin the checked directory object. An attacker able to replace a checked Work or nested parent directory between validation and later use can redirect subsequent operations. The exact-SHA CI #514 parent-swap regression is therefore a genuine product security failure, not an infrastructure failure.

**F01 status: BLOCKED.** No source remediation is present in this audit.

## 2. Source-level evidence

The following code paths were inspected in the exact PR #82 source:

| Area | Current path-based operations | Security consequence |
|---|---|---|
| Service initialization | `Path(sandbox_root).resolve()`, `mkdir()` | Root is represented as a pathname, not a retained trusted directory handle |
| Work root | `(self.root/work).resolve()`, `p.parent`, `mkdir(parents=True)` | Check/use gap permits Work-root replacement |
| Symlink validation | `target.relative_to(root)`, repeated `root/part`, `is_symlink()` | Checks names at one instant; does not bind later operations to checked objects |
| Startup reconciliation | `exists()`, `is_symlink()`, `iterdir()`, `open(staging)`, `stat()`, `truncate()`, `unlink()` | Recovery and orphan scan can follow replaced path components |
| Begin | `final.exists()`, `staging_dir.mkdir()`, `os.open(staging_path,...)`, exception cleanup `staging.unlink()` | Destination check, staging creation and cleanup are pathname based |
| Chunk | lock path via `os.open(lock_path)`; `open(path,"r+b")` | Lock and data file may resolve through a substituted parent; write is not anchored to trusted directory handles |
| Digest/readback | `open(path,"rb")` | Hash/readback can inspect a different object after path replacement |
| Finalize/recovery | `mkdir(parents=True)`, `os.link(staging,final)`, `open(final)`, `unlink()` | Promotion and cleanup use mutable pathnames; hard-link no-replace alone does not secure parent traversal |
| Abort | `Path(staging_path).unlink()` | Cleanup is not anchored to the validated Work/staging directory |

## 3. Required remediation boundary

A narrow patch to `begin()` is insufficient. One filesystem backend must own all security-sensitive filesystem operations and retain trusted root/ancestor handles for the duration of each operation.

### Linux backend
- Open and retain the trusted Sandbox root directory descriptor.
- Traverse each Work/destination/staging component relative to its parent descriptor using directory-only and no-follow flags; reject symlinks and non-directory components.
- Create staging exclusively relative to the verified staging-directory descriptor.
- Perform chunk read/write, digest, truncate, readback and unlink using the pinned file descriptor.
- Promote with an atomic no-replace primitive relative to retained verified parent descriptors; fsync file and relevant directories where durability requires it.
- Never reconstruct an absolute path and reopen it for a security-sensitive operation.

### Windows backend
- Use native directory/file handles opened with reparse-point-safe semantics.
- Inspect reparse metadata from the opened handle, not from a prior pathname check.
- Retain ancestor handles and prove that subsequent create/open/rename/delete operations are bound to those objects despite concurrent rename/replacement.
- Use a reviewed handle-relative create/promotion primitive (for example, a vetted `NtCreateFile` RootDirectory design or an equivalently proven implementation).
- If a required primitive cannot be implemented and tested, fail closed; do not silently fall back to pathname-only mutation.

## 4. Required adversarial test matrix

Native Linux and native Windows tests must cover:
1. Sandbox root replacement after initial open.
2. Work-root replacement after validation.
3. Nested destination-parent replacement.
4. Staging-directory replacement and staging-file substitution.
5. Parent replacement during chunk write and digest/readback.
6. Parent replacement during finalize, promotion and cleanup.
7. Parent replacement during startup reconciliation and abort.
8. Symlink/reparse-point insertion at every traversed component.
9. Cross-Work and Sandbox-root escape attempts.
10. Existing destination race and atomic no-replace behavior.
11. Process restart at each durable state transition, with no untracked staging mutation.
12. Deterministic barriers/hooks proving the attacker swap occurs between the former check and use points.

Tests must assert that no file is created, modified, read as trusted, promoted or deleted outside the originally opened Sandbox/Work object. No functional security test may be skipped to claim platform acceptance.

## 5. Acceptance criteria

- All filesystem lifecycle methods route through the same handle-anchored backend.
- No security-sensitive operation uses path-based check-then-use.
- Native Linux and Windows adversarial suites pass on the exact candidate SHA.
- Existing upload roundtrip, quota, idempotency, crash-recovery and audit tests remain passing.
- An performs independent QA after implementation is frozen.
- An independent security reviewer reviews the implementation and threat matrix; Ka does not self-certify.
- F02 durability, F03 Core authority contract and F04 MCP transport remain separate gates and must not be implied by F01 closure.

## 6. Evidence and limits

- PR: #82 (OPEN / DRAFT / UNMERGED)
- Exact source SHA: `f0c52ae0ceca3edc1708b20f8d67022f576d4774`
- Workflow #514 / run ID `45764958955`
- Native Windows regression job `139723552234`: FAILURE — parent-swap assertion, `UploadError not raised`
- Native Linux regression job `139723552350`: FAILURE — same assertion
- Unit/regression job `139723552247`: FAILURE — same regression
- Execution Host lifecycle Linux `139723551988` and Windows `139723552246`: SUCCESS (different scope)
- Immutable artifact job `139723755810`: SKIPPED due to required test failures

This audit does not implement a backend, prove a fix, authorize merge, register an MCP tool, deploy, perform live upload, or release Work 28.

**Decision:** retain the regression; do not merge PR #82; implement the full handle-anchored lifecycle before requesting independent QA.

**Signed:** Ka — Delegated Work 28 Operational Owner / Remediation Lead
