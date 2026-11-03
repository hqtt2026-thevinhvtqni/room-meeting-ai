# WORK 28 — WP3 BINARY UPLOAD AUTHORIZATION CONTRACT PROPOSAL

**Proposal ID:** VI-WP3-F01-AUTH-CONTRACT-20261104  
**Execution time:** 2026-11-04 04:09:53 UTC+07:00  
**Role:** VI | CODER  
**Signature:** [KÝ: VI | CODER]  
**Branch:** `work/28-mcp-tooling-platform`  
**Status:** PROPOSAL ONLY — NOT AN APPROVED ARCHITECTURE CHANGE

## 1. Why a contract gate is required

The WP3 source trace shows the existing v54 service dispatches tool arguments directly to a Sandbox provider, while the Core authorizer module explicitly states it is staged and not wired into MCP registration/v54. The server adapter currently calls the service with only tool name and arguments. A caller-supplied identity_id or work_id cannot be treated as authentication evidence.

There is also an identifier mismatch: Core authorizer accepts canonical `W<number>` IDs, while the Sandbox provider currently accepts generic Work IDs such as `28`. A server-owned mapping between Core Work ID `W28` and the Sandbox's internal Work key must be explicit and auditable; do not normalize caller input by guesswork.

## 2. Proposed trust boundary

1. The MCP transport/server obtains authenticated principal context from a trusted server-side source (for example, a verified transport session or pinned service credential). The client must not pass credentials or identity claims inside tool arguments.
2. A trusted context resolver, injected into the server adapter, returns an opaque caller context. The adapter passes it out-of-band to the service; it is never serialized into tool output or logged.
3. The service invokes the Core authority authorizer before any Sandbox side effect. Authorization must bind authenticated identity, canonical Core Work ID, capability `sandbox_upload_file`, normalized destination scope, and policy decision.
4. Only after authorization does a server-owned mapping resolve Core Work ID to the provider's internal Sandbox key. Mapping failure is BLOCKED.
5. The provider receives a narrow authorized upload context/capability, not an arbitrary caller-supplied identity string. Missing context, Core outage, denial, expiry or revocation fails closed before staging or writing.

## 3. Proposed upload protocol

Use a bounded, server-side upload session to avoid a single unbounded JSON/base64 request:

- **Begin:** authenticated Work scope, normalized destination, expected total byte count, expected SHA-256, chunk size/count limits, expiry, correlation ID and overwrite policy. Return opaque upload ID.
- **Chunk:** upload ID, monotonic chunk index/offset, bounded base64 bytes, per-chunk length/hash. Reject duplicate, missing, reordered, oversized or out-of-scope chunks.
- **Finalize:** require complete contiguous byte coverage; verify total byte count and final SHA-256; revalidate authorization; promote atomically; perform independent readback; append audit record; then return final status and checksum.
- **Abort/expiry:** remove temporary content and session state; never leave a partial final destination. Cleanup is idempotent and audited.

The external capability may be presented as one documented `sandbox_upload_file` streaming contract backed by begin/chunk/finalize operations, or as separately registered versioned tools. The catalog, schemas, handlers, provider and runtime tools/list must agree. Do not register a placeholder.

## 4. Filesystem invariants

- Work-root and destination containment must be revalidated at every operation, including symlink components and the final promotion point.
- Temporary staging must be inside a controlled same-filesystem staging area inaccessible as a final artifact.
- Default no-overwrite. If overwrite is ever supported, it must be an explicit Core-authorized capability and use a race-safe atomic replace policy.
- Quotas and size limits apply before accepting data and again during chunk accumulation.
- SHA-256 is calculated over exact bytes, not UTF-8 text. Readback independently checks byte count and digest.
- Audit includes upload/correlation ID, identity reference (non-secret), Core Work ID, internal Work mapping reference, destination, size, digest, timestamps, result and failure reason. Never log credentials or file contents.

## 5. Required contract tests

- No authenticated context, invalid credential, unauthorized Work, wrong capability, revoked/expired context, Core unavailable and spoofed caller identity: deny before filesystem side effect.
- W28 → internal Sandbox mapping succeeds only for an explicit registered mapping; unknown/mismatched mapping fails closed.
- Binary payload containing invalid UTF-8, zero bytes, ZIP, exact size/SHA-256 round trip.
- Chunk ordering, duplication, gaps, truncation, over-limit, oversized chunks, cancellation, expiry, retry and concurrent sessions.
- Traversal, absolute/drive paths, symlink escape/swap, unauthorized overwrite, quota exhaustion and atomic promotion failure.
- Readback mismatch, disk-full/write failure, interrupted transfer and cleanup failure; final destination remains absent or previous authorized version remains intact.

## 6. Decisions required before implementation

- Confirm the trusted MCP transport/session source for authenticated principal context; do not infer it from MCP tool arguments.
- Confirm the authoritative mapping between Core Work IDs (`W28`) and provider Sandbox IDs (`28`).
- Confirm whether the service should expose one streaming `sandbox_upload_file` contract or three explicit begin/chunk/finalize tools.
- Confirm Core capability-grant semantics for file upload, including destination scope, quota and overwrite authority.

**Conclusion:** This proposal identifies the minimum secure integration contract. It does not claim that the current server has the required trusted context, that an upload tool exists, or that binary transfer works. Implementation remains blocked on verified Core caller context and Work-ID mapping.
