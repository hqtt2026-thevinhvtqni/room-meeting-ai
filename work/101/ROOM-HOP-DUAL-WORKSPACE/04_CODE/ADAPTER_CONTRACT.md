# Work 101 — Runtime Adapter Contract (Design Only)

Status: CONTRACT DRAFT; no adapter implementation is present.

## Purpose
Define the minimum provider contract for Sandbox and GitHub adapters without inventing ROOM-HOP routes or bypassing Core/MCP authorization.

## Provider operations

### 1. `read_target_identity()`
Returns target kind, Work ID, canonical root, repository/branch where applicable, actor identity, permissions and observed revision. Unknown identity or branch blocks planning.

### 2. `read_snapshot(target, permitted_roots, expected_base)`
Returns an immutable manifest containing:
- target ID and kind;
- observed revision and the common base revision used for comparison;
- sorted canonical relative paths under the allowlist;
- SHA-256 digest and byte length for each file;
- captured timestamp and provider identity.

Must not follow symlinks outside the Work root. Reject ambiguous Unicode, case-insensitive path collisions, secrets, runtime databases, logs, caches, OS metadata and generated output. An unavailable or stale revision is BLOCKED, not guessed.

### 3. `read_file(target, path, expected_revision)`
Returns bytes and digest only if the path is allowlisted and the target revision still matches the plan. Verify the returned digest against the snapshot before any transfer.

### 4. `write_file(target, path, content, expected_revision, operation_id, diff_digest, approval)`
Available only after the policy gate and exact approval checks pass. Must use provider-supported compare-and-swap or conditional revision writes. If the provider cannot prevent stale-base overwrite, return BLOCKED. Never write `main`/protected branches. Never accept browser-supplied credentials.

### 5. `verify_write(target, path, expected_digest, resulting_revision)`
Read the destination back and compare SHA-256. A successful API response alone is not destination verification.

## Intentionally absent in v1
- No `delete_file` operation. Baseline-file deletion enters `DELETION_PENDING` and blocks the plan until a separate explicit-resolution design is reviewed.
- No merge, pull-request approval, release, or default-branch mutation.
- No direct AI-to-Drive/backend access.
- No direct write to Core's data store.
- No new MCP tool registration until Work 28's live registry and Core authorization contract are verified.

## Required transfer transaction
1. Capture and validate both snapshots against one exact common base.
2. Build deterministic dry-run plan; bind operation ID, per-path base/source/destination hashes, allowlist, destination branch and base revision in the diff digest.
3. Persist or obtain server-side approval bound to the exact operation/digest/branch/base.
4. Revalidate source and destination revisions immediately before each write.
5. Transfer only permitted PUT actions; fail closed on any partial failure.
6. Read destination back and verify SHA-256.
7. Record every action and failure in an append-only evidence ledger.
8. On partial failure, stop and produce a resumable ledger; do not blindly replay with a changed payload.

## Provider mapping still required
- Sandbox: confirm Work 101 sandbox API semantics, revision/ETag availability, and atomicity.
- GitHub: use the dedicated branch only; confirm branch head SHA before and after writes and per-file blob SHA on read-back.
- ROOM-HOP: confirm the authorized route through MCP :8020 -> Core :8000 -> Workspace :8010 and reuse Work 24/27/28/14 only after live contracts are inspected.

This contract does not authorize or perform any write.
