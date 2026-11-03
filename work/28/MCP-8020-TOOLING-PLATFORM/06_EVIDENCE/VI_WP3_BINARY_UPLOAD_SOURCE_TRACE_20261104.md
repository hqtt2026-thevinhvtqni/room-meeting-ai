# WORK 28 — WP3 BINARY UPLOAD SOURCE TRACE

**Evidence ID:** VI-WP3-F01-TRACE-20261104  
**Execution time:** 2026-11-04 04:09:53 UTC+07:00  
**Role:** VI | CODER  
**Signature:** [KÝ: VI | CODER]  
**Branch:** `work/28-mcp-tooling-platform`

## 1. Scope
Trace the canonical branch implementation and contracts relevant to W28-WP3-F01 `sandbox_upload_file` before modifying code. This is a source-level audit, not runtime proof.

## 2. Canonical source observations

| File | Blob SHA | Verified observation |
|---|---|---|
| `work/28/MCP-8020-TOOLING-PLATFORM/04_CODE/mcp8020_sandbox_tools_v54.py` | `9108d6bd8739f6c74be3ca483aa9c02520a385c9` | `SandboxProvider.sandbox_write()` accepts `content: str` and encodes UTF-8 before writing. `sandbox_read()` decodes requested bytes as UTF-8 and raises DECODE_ERROR on binary ranges. Writes are direct; no upload staging/chunk/finalize path exists in this module. |
| `.../04_CODE/mcp8020_catalog_v54.py` | `e51251f33ca8beb0d181cc8abdcb95875101faf1` | Catalog exposes `sandbox_read`, `sandbox_write`, `sandbox_append`, metadata and other file operations; no `sandbox_upload_file` spec is present. Existing write schema takes a string content field. |
| `.../04_CODE/sandbox_tools_v1.py` | `6682a4812b199dc1d1384d5eee28866c9b7ba459` | Provider protocol and handler accept `content: str`; write is capped at 64 KiB UTF-8. No binary payload or chunk-upload API exists in this adapter. |
| `.../04_CODE/mcp_tool_registration_v1.py` | `b9f306c9e4765117af517be578139faabe8bab01` | Registered v1 sandbox methods include search/stat/read_range/write; no binary upload method is registered. |
| `.../04_CODE/mcp8020_core_authority_authorizer_v1.py` | `1d8013eb2dfa281ac922638ac45d7d4fff00c005` | Core authorizer is explicitly staged and not wired into MCP registration or the v54 catalog. It validates canonical Core Work IDs and server-side credential identity/Work membership when invoked. |
| `.../04_CODE/mcp8020_core_execution_session_v1.py` | `f95160e245ee11cc8c5abc641ca8f1b736970346` | Core grant session is staged and not wired into MCP registration/v54 catalog; its documented purpose is execution grant lifecycle, not a demonstrated Sandbox upload authorization path. |
| `.../04_CODE/mcp8020_service_v54.py` | `5c420b6fb85b85fee8f3fddfd9f504f021c2cae8` | v54 service validates catalog arguments and dispatches to provider methods. The inspected service constructor has no injected Core authorizer or trusted caller context for Sandbox file operations. |

## 3. Security and implementation gap

The approved Architecture Decision V2 requires binary upload to be Work-authorized, bounded, staged, SHA-256 verified, atomically promoted and auditable. The current traced implementation does not yet establish those requirements. In particular:

1. Text-only UTF-8 conversion prevents byte-preserving binary upload/readback.
2. No registered upload tool or streaming/chunk contract is present.
3. No demonstrated Core-authorized identity + Work-scope check is wired into the v54 Sandbox dispatch path. Caller-supplied identity fields must not be treated as credentials.
4. No bounded upload session, per-file/per-Work quota, temporary staging, atomic promotion, checksum-verified readback or failure cleanup path exists in the traced upload surface.
5. Existing `realpath` containment is useful baseline protection but is not by itself proof of race-resistant symlink handling during a staged upload/atomic promotion.

## 4. Safe implementation decision

Do not add a public upload handler directly to the current v54 provider until a trusted Core authorization context is injected and validated server-side. The implementation slice must define a contract that binds the upload session to authenticated identity, canonical Work ID, normalized destination, maximum bytes, expiry and correlation ID. Use bounded chunks with strict base64 validation (or a transport-native byte stream), incremental byte count and SHA-256; stage outside the final path; reject traversal/symlink escape and unauthorized overwrite; atomically promote only after final size/hash verification; and append audit evidence. Failure, cancellation, expiry and concurrent-session cleanup must be tested. The registered schema, handler, provider and deployed runtime tool list must remain in parity.

GitHub publication remains a separate controlled operation from Sandbox upload.

## 5. Test matrix required before acceptance

- Zero-byte file and binary bytes containing invalid UTF-8 sequences.
- ZIP round-trip with exact byte count and SHA-256 parity.
- Small, maximum-size and over-limit payloads; per-Work quota exhaustion.
- Chunk ordering, duplicate chunk, missing chunk, interrupted transfer, cancellation and expired session.
- Traversal, absolute path, drive path, symlink escape and symlink swap/race.
- Existing destination with overwrite omitted/false; authorized overwrite only under explicit policy.
- Atomic promotion: no partial final file visible; cleanup of temporary artifacts after every failure.
- Concurrent uploads to same and different destinations; audit correlation and no cross-Work leakage.
- Missing/invalid Core credential, wrong Work membership, revoked/expired authorization and caller-supplied identity spoofing all fail closed before filesystem side effects.

## 6. Status

**WP3-F01:** SOURCE GAP CONFIRMED / IMPLEMENTATION NOT STARTED / CORE AUTHORIZATION INTEGRATION BLOCKER.  
This report does not claim runtime deployment, live upload, binary fidelity, checksum parity, or test PASS.
