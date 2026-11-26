# DOC-004 — WORK 33: CLOUD DRIVE PROTOTYPE SOURCE REVIEW GATE

- Date: 2026-11-26 (+07)
- Status: REVIEW GATE / SOURCE NOT AVAILABLE ON GITHUB MAIN / SANDBOX UNAVAILABLE
- Scope: determine whether the Cloud Drive prototype can undergo a trustworthy source-level review and define the next evidence required.
- Repository: hqtt2026-thevinhvtqni/room-meeting-ai, branch main.
- No code changes, test runs, runtime calls, or deployment performed.

## 1. Source availability result

Attempted read-only GitHub fetch on main for the following expected prototype files:
- `02_EXTENSION/cloud_drive/uploads/session_manager.py`
- `02_EXTENSION/cloud_drive/uploads/lifecycle.py`
- `02_EXTENSION/cloud_drive/service/quota_manager.py`
- `02_EXTENSION/cloud_drive/service/upload_service.py`
- `02_EXTENSION/cloud_drive/storage/local.py`
- `02_EXTENSION/cloud_drive/uploads/recovery_inspector.py`
- `02_EXTENSION/cloud_drive/uploads/recovery_planner.py`
- `02_EXTENSION/cloud_drive/service/authorization.py`

All eight fetches returned GitHub 404 NOT_FOUND at the expected Work 33 path on main. This establishes only that these exact paths are not available at the requested ref/path; it does not establish that the files do not exist in Sandbox or at another branch/path.

A single Sandbox list request for Work ID 33 returned UNAVAILABLE / connection failed. The prototype source therefore could not be read from Sandbox in this session.

## 2. Review disposition

- Source-level review: BLOCKED — exact prototype source not accessible.
- Static defect assessment: NOT PERFORMED in this turn.
- Unit/integration tests: NOT RUN.
- Runtime/E2E: NOT RUN.
- Security verification: NOT RUN.
- PASS: none.

Do not infer that previously described prototype behaviors are currently present in a verified source tree until the exact files are read at a known commit or Sandbox revision.

## 3. Required source intake package

When Sandbox access is restored, capture a source manifest before review:
1. Work ID and canonical relative path for each file.
2. Source revision/commit or Sandbox manifest version and file hashes.
3. Exact file contents for implementation and matching tests.
4. Dependency/configuration manifest and supported Python/runtime versions.
5. Existing test command and test output, if previously run, with timestamp and environment.
6. No credentials, personal files or production data.

If the source is promoted to GitHub, preserve the canonical Work 33 folder and commit; do not create duplicate copies under alternate paths.

## 4. Mandatory static review checklist

### Upload protocol and persistence
- Enforce bounded request and part sizes before allocating or writing.
- Validate upload ID, part index, expected count, declared total size and digest format.
- Use server-derived staging paths; reject traversal, symlinks and special files.
- Write each part to a unique temporary file, fsync as supported, atomically publish, then commit metadata.
- On retry, identical bytes are idempotent; changed bytes for an existing part are rejected.
- Completion requires a contiguous part set, total size and whole-object SHA-256 match.
- Never mark AVAILABLE before durable object write and read-back verification.
- Ensure state transitions are compare-and-set with monotonic version/fencing; stale writers cannot finalize.
- Crash windows between filesystem and SQLite operations must have explicit recovery states and deterministic reconciliation.

### Quota correctness
- Reserve quota transactionally before accepting bytes.
- Prevent concurrent requests from oversubscribing a scope.
- Commit used bytes exactly once on successful completion.
- Release reservation exactly once on a proven abort.
- Never release held quota merely because a TTL expired while a writer may still be active.
- Reconcile metadata, actual object bytes, reservations and used bytes.
- Ensure quota database identity and transaction boundaries are explicit.

### Storage and integrity
- Enforce tenant/space scoped object identity; avoid cross-tenant content-dedup existence leaks.
- Distinguish provider ETag from SHA-256.
- Verify stored object size/hash after write and on recovery.
- Ensure atomic replace and durability semantics are documented per adapter.
- Ensure local adapter cannot read/write outside configured root, including symlink races.
- Define provider failure, timeout, partial-write and retry semantics.

### Recovery and audit
- Recovery inspection must be read-only by default.
- Mutations require verified evidence, writer fencing, idempotency, explicit authorization and independent approval.
- Never auto-release quota or finalize ambiguous COMMITTING state.
- Audit events must identify authenticated principal, action, resource, result, correlation ID and policy version without leaking tokens.
- Backup/restore must be independent of primary storage and tested with checksums.

## 5. Required dynamic test matrix (not run)

1. Empty file, one-part file, multi-part file and maximum permitted size.
2. Out-of-order, duplicate-identical, duplicate-different and missing parts.
3. Interrupt before write, during write, after rename and before metadata commit.
4. Concurrent same-part writes and concurrent completion attempts.
5. Stale worker after lease expiry and stale fencing token.
6. Process restart in each nonterminal lifecycle state.
7. Quota race across threads and processes; reserve/commit/release replay.
8. Corrupt part, corrupt final object, missing blob and orphan blob.
9. Symlink/path traversal and permission boundary attacks.
10. Cross-space identical content dedupe and metadata enumeration.
11. Provider unavailable, slow, partial and conflicting read-back.
12. Backup restore to clean target, full checksum and metadata reconciliation.

Each test must record exact source revision, command, environment, expected/actual result, logs/evidence, and independent QE disposition. Do not claim PASS from a test definition alone.

## 6. Next action

Restore Sandbox MCP access or make the exact existing Work 33 prototype source available at its canonical GitHub path. Then perform READ → TRACE → ANALYZE before any code modification. No PC action is requested from Vinh at this point.
