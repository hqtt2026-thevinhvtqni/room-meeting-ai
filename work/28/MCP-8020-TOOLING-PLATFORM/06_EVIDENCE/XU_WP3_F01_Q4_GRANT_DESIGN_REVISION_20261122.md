# WORK 28 — WP3-F01 Q4 UPLOAD CAPABILITY-GRANT DESIGN REVISION

**Design ID:** XU-W28-WP3-F01-Q4-DESIGN-20261122-001  
**Owner:** Xu — Work 28 coordinator / technical decision owner  
**Purpose:** Revised technical proposal addressing Ka's Q4 security review dated 2026-11-15  
**Status:** **PROPOSED FOR INDEPENDENT REVIEW — NOT APPROVED — IMPLEMENTATION NOT AUTHORIZED**  
**Scope:** W28-WP3-F01 binary Sandbox upload capability only  
**Authority boundary:** Core :8000 remains the sole authorization authority; Sandbox provider remains a constrained storage executor.

## 1. Why this revision exists

The existing v1/v54 Sandbox adapters accept UTF-8 text, not arbitrary binary payloads. The current tool registration does not expose a binary upload session. Xu's 2026-11-13 decision selected trusted server-side caller context, dynamic Core Work-to-Sandbox mapping and a begin/chunk/finalize protocol, but left Q4 capability-grant semantics unapproved. Ka's 2026-11-15 review rejected Q4 because the design did not fully bind principal, Work mapping, capability, path scope, quota, TTL, revocation, replay/idempotency, atomicity and durable audit.

This revision makes those fields and state transitions explicit. It is a design proposal only. It does not claim that Core currently exposes these operations, that the required transactional store exists, or that any upload code is implemented.

## 2. Security invariants

1. **Core is authoritative.** Only Core may issue, validate, attenuate or revoke an upload capability. The MCP service and Sandbox provider cannot self-authorize.
2. **Trusted caller context is out-of-band.** Principal/session identity comes from authenticated server-side transport context. Tool arguments, caller-supplied identity IDs, Work IDs or booleans are never authentication evidence.
3. **No local fallback.** Missing Core route, timeout, malformed response, unknown policy version, stale mapping or unavailable revocation state means DENY/BLOCKED before filesystem side effects.
4. **Grant is least privilege.** One grant binds one principal/session, one canonical Work, one server-owned Sandbox mapping, one capability, a finite operation set, a bounded destination scope and immutable resource ceilings.
5. **Re-check every operation.** Begin, every chunk, finalize and abort/cleanup must validate the same grant/session binding and current revocation/expiry state. A check performed only at begin is insufficient.
6. **No implicit overwrite.** Default behavior is DENY if the destination exists. Replace requires a separate capability and a destination-version/hash precondition.
7. **No partial success.** A partial upload is never visible as a final artifact. Unknown cleanup, failed audit, checksum mismatch or failed readback is BLOCKED/FAIL, never PASS.
8. **No authority expansion.** This upload grant is not an execution grant and cannot authorize commands, Python execution, arbitrary filesystem access or GitHub publication.

## 3. Proposed versioned grant envelope

The following is a logical contract, not an instruction to accept caller-supplied JSON. Core constructs the envelope from authenticated session state and server-side policy. The opaque bearer token (if used by the approved transport) is separate from the non-secret metadata and must never be logged.

```json
{
  "schema": "w28.sandbox-upload-grant.v2",
  "grant_id": "opaque-core-grant-id",
  "grant_version": 2,
  "issuer": "core-service-identity",
  "audience": "approved-build-sandbox-service-identity",
  "subject": {
    "principal_id": "server-resolved-principal",
    "session_id": "server-resolved-session"
  },
  "work_binding": {
    "canonical_work_id": "W28",
    "sandbox_work_id": "28",
    "mapping_id": "core-issued-mapping-id",
    "mapping_version": 1
  },
  "capability": "sandbox.file.upload",
  "operations": ["begin", "chunk", "finalize", "abort"],
  "path_scope": {
    "mode": "exact",
    "normalized_path": "06_EVIDENCE/source-bundle.zip",
    "canonicalizer_version": 1
  },
  "limits": {
    "max_file_bytes": 104857600,
    "max_reserved_work_bytes": 524288000,
    "max_active_uploads": 2,
    "max_chunk_bytes": 1048576,
    "max_chunks": 256
  },
  "overwrite": {
    "allowed": false,
    "replace_capability": null,
    "expected_destination_version": null
  },
  "lifecycle": {
    "issued_at": "Core timestamp",
    "not_before": "Core timestamp",
    "expires_at": "Core timestamp",
    "revocation_epoch": 0,
    "nonce": "unique-single-grant-value"
  },
  "policy_version": "Core policy revision"
}
```

### 3.1 Mandatory validation

- Reject absent/unknown schema versions, unknown issuer/audience, missing fields, type mismatches, duplicate operations, unsupported capability names and non-positive limits.
- Verify the authenticated transport principal and session exactly match the grant subject; never accept a subject override in a tool argument.
- Verify canonical Work ID, Sandbox Work ID, mapping ID and mapping version against a current Core-issued WorkContext. A changed or stale mapping invalidates the grant and all active sessions.
- Verify capability and operation allow-list. An upload grant cannot authorize read, delete, execution, GitHub write or overwrite unless separately granted.
- Normalize the destination with one versioned path canonicalizer. Reject absolute/drive paths, parent traversal, NUL, alternate data streams, ambiguous separators, invalid segments and symlink escape. Re-resolve and revalidate at begin and immediately before promotion.
- The grant's maximums are immutable ceilings. A request may ask for less, never more.

### 3.2 Token and storage handling

- Prefer an opaque, high-entropy Core-issued grant token with server-side validation; do not assume JWT or invent a signing scheme without a Core contract.
- Store only a token digest or opaque reference in durable state. Never persist raw credentials, bearer tokens or file bytes in audit logs.
- Bind grant ID, nonce, audience, principal, Work mapping and policy version to every upload session.
- Core revocation state is authoritative. A local cache may only shorten availability; it may not extend grant validity or override a denial.

## 4. Upload session protocol

The external MCP contract may expose one documented streaming upload capability or separately registered versioned operations. The transport choice must be proven to preserve raw bytes and bounded memory. Do not use JSON UTF-8 conversion or unbounded base64 payloads as a substitute for binary streaming.

### 4.1 begin

Input: destination path, expected total byte count, expected SHA-256, requested chunk size, idempotency key and correlation ID. Principal and Work authority are resolved out-of-band.

Order:
1. Validate trusted caller context and ask Core to authorize the exact Work, capability, destination and requested size.
2. Verify the returned grant envelope and current mapping/revocation version.
3. Atomically reserve per-Work/per-principal quota and active-upload capacity using a durable transactional ledger or equivalent compare-and-swap mechanism.
4. Create a private staging object under a controlled same-filesystem staging root; it must not be visible as a final artifact.
5. Persist the session record and audit BEGIN_ACCEPTED before returning the opaque upload ID.

Duplicate begin with the same idempotency key and identical principal/Work/path/size/digest returns the same session. Reuse with different content or scope is DENIED. If reservation, staging, durable state or audit cannot be confirmed, return BLOCKED and release/clean up what can be proven safe.

### 4.2 chunk

Each chunk binds upload ID, zero-based chunk index, byte offset, exact byte length, chunk SHA-256, idempotency key and raw bytes.

- Require the exact next contiguous index/offset; reject gaps, overlaps, reordered chunks, oversized chunks and content beyond the grant/session byte ceiling.
- Revalidate Core grant, session binding, expiry, revocation epoch and mapping version before every chunk side effect.
- A repeated chunk with the same index, offset, length and digest is idempotent and returns the prior acknowledgement. A repeated index with different bytes/digest is DENIED and raises a replay/security event.
- Persist chunk receipt only after bytes are written and the chunk digest is verified. A crash/restart must recover a truthful session state; incomplete or ambiguous chunks cannot be counted as accepted.
- Quota accounting is reserved atomically at begin and reconciled against actual accepted bytes. Concurrent sessions cannot exceed the grant or Work quota.

### 4.3 finalize

1. Revalidate the active grant, principal/session, Work mapping version, path scope, expiry and revocation state.
2. Transition the session to FINALIZING using an atomic compare-and-swap; concurrent finalize calls must return the same eventual result, not run promotion twice.
3. Require complete contiguous byte coverage from offset 0 to expected size; verify every recorded chunk and recompute full-object SHA-256 over exact bytes.
4. Flush and fsync the staged object and containing directory where supported. Re-resolve the destination and reject symlink/path changes.
5. Promote atomically with a no-replace primitive. If the destination appeared concurrently, return DENIED/CONFLICT; never overwrite implicitly.
6. Independently read back the final object and verify exact byte count and SHA-256.
7. Persist the durable completion/audit record before returning PASS. If audit durability or readback cannot be confirmed, do not return success; remove/quarantine the promoted object according to a recoverable transaction protocol and record BLOCKED if rollback cannot be verified.
8. Release reserved quota exactly once and persist the final session result.

Repeated finalize with the same session/idempotency key returns the stored result. A different finalize request is DENIED.

### 4.4 abort, expiry and revocation

- Abort is allowed only for the bound principal or an explicitly authorized service cleanup identity; it cannot change another Work's session.
- Expiry and Core revocation prevent further chunks/finalize immediately. They trigger idempotent staging cleanup and quota release.
- If cleanup is verified, record ABORTED, EXPIRED or REVOKED. If cleanup is uncertain, retain a BLOCKED tombstone and staging reference for retry; do not report cleanup PASS or free quota optimistically.
- A cleanup worker may retry only within the same Work scope and must record each attempt, evidence and final disposition.

## 5. Session state machine

Allowed states:

- `AUTHORIZED` — Core grant validated; no file bytes accepted.
- `UPLOADING` — quota reserved and one or more verified chunks accepted.
- `FINALIZING` — immutable finalization attempt owns the session transition.
- `COMPLETED` — atomic promotion, independent readback and durable audit all verified.
- `ABORTED` — caller-authorized abort and staging cleanup verified.
- `EXPIRED` — TTL elapsed and cleanup verified.
- `REVOKED` — Core revoked grant and cleanup verified.
- `BLOCKED` — state, audit, cleanup or readback cannot be verified; retry/manual disposition required.

No transition may move BLOCKED to COMPLETED without a fresh authorization check and full integrity verification. No client may set the state directly.

## 6. Atomicity, concurrency and persistence requirements

- Grant issue/revoke, quota reservation/release, session creation, chunk receipt, finalize ownership and audit sequence need durable transactional semantics. An in-memory dictionary or read-then-append JSONL sequence is insufficient for multi-process concurrency.
- Use a unique constraint or atomic idempotency record for (principal, Work, idempotency key); unique chunk identity for (upload ID, index); compare-and-swap for session state transitions.
- A revocation racing with chunk/finalize must be linearized: either the operation is committed before revocation under the defined policy, or the operation is denied. It must never pass a stale pre-check and promote after revocation.
- Quota reservation is atomic across concurrent sessions and released exactly once. Unknown reservation state remains BLOCKED.
- Filesystem promotion and audit are not assumed to share a transaction. The implementation must provide a recoverable commit protocol so no unverified file is reported as complete and no audit failure yields PASS.
- Recovery on service restart must reconcile staging objects, session records, quota reservations and audit sequence. Orphaned staging data remains inaccessible and is cleaned only with verified evidence.

## 7. Durable audit contract

Append-only events must include: event ID, timestamp, correlation ID, upload ID, grant ID, non-secret principal reference, canonical Work ID, Sandbox mapping ID/version, capability, operation, normalized destination reference, expected/actual byte counts, expected/actual SHA-256, chunk index/offset/digest where relevant, quota reservation/release, policy version, decision, outcome and cleanup/readback evidence reference.

Never record credentials, raw grant tokens or file contents. Audit storage failure before a success response means BLOCKED; a success response is forbidden until the completion event is durable and readback is verified.

## 8. Required independent test matrix

The exact implementation SHA must be tested for:

- Missing, forged, expired or mismatched principal/session; wrong audience; invalid token; Core timeout/unavailable/denied; revoked grant.
- Wrong Work, missing/stale mapping, mapping-version change, cross-Work access and spoofed caller identity.
- Wrong capability/operation; exact-path and prefix-scope escape; path canonicalization ambiguity; absolute/drive/parent paths; symlink swap/escape.
- Zero-byte file, invalid UTF-8 binary, ZIP and arbitrary bytes with exact byte-count/SHA-256 round trip.
- Maximum file size, over-limit file/chunk, quota exhaustion and concurrent quota reservations.
- Chunk duplicate, changed-content replay, reorder, gap, overlap, truncation, oversize and interruption.
- Grant expiry/revocation between begin, chunk and finalize; duplicate begin/finalize; timeout retry and idempotency.
- Overwrite denied by default; explicit replace denied without separate capability; stale destination-version/hash precondition denied.
- Disk-full, write failure, checksum mismatch, readback mismatch, audit failure, atomic promotion failure, process crash and cleanup failure.
- Restart recovery: no partial final artifact, no optimistic quota release, no fabricated completion or cleanup PASS.

Mocks/local HTTP may prove component behavior only. They do not prove deployed Core authorization, live Sandbox integration, runtime tools/list parity or production filesystem isolation.

## 9. Open decisions and mandatory review

This revision deliberately does not invent a Core HTTP route or claim that the current Core service supports upload grants. Before implementation:

1. Ka must independently review this exact design revision and disposition every Q4 requirement, including atomic revocation/finalize races and audit failure semantics.
2. The Core owner must identify an existing approved route/contract or approve a separately versioned Core contract. No endpoint may be guessed or created by the Sandbox service.
3. The authoritative Work mapping and mapping-version lifecycle must be proven from Core.
4. The durable transactional quota/session/audit store and crash-recovery strategy must be selected and reviewed.
5. An must independently review the acceptance matrix and later reproduce exact-SHA tests.
6. Xu may record a new decision only after Ka's independent review is available. This document itself grants no implementation authority.

## 10. Current disposition

**Q4 remains NOT APPROVED. WP3-F01 implementation, tool registration, staging, chunk acceptance, promotion and production routing remain BLOCKED.** This design is submitted for independent review only.

Core :8000 remains the sole authorization authority. MCP Build/Verification :8030 remains a supporting build/evidence lane. The historical quarantined runtime is not used. Execution Host :8031 remains the only approved execution boundary. Work 28 remains ACTIVE / INTEGRATION BLOCKED / NOT RELEASED; Execution Gate CLOSED.

**[KÝ: XU | PROPOSED DESIGN — NOT APPROVED]**
