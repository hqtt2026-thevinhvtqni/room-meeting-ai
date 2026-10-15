# Work 28 — Tool Gap Decision
Date: 2026-10-15
Purpose: Decide what additional MCP tools are actually worth building after considering existing ROOM-HOP capabilities.

## Decision
Do not add tools merely because another Work contains code or because a registry proposal lists them. First reuse and verify existing connected operations. Add only tools that close a concrete workflow gap.

## Build priority
| Priority | Tool/capability | Why needed | Decision |
|---|---|---|---|
| P0 | sandbox_search | Find artifacts across authorized Work paths without listing directories manually. | BUILD after checking whether an equivalent Core/Sandbox search already exists. |
| P0 | sandbox_stat | Check file metadata/existence/size/modified info before reading or writing. | BUILD if not already available from canonical API. |
| P0 | sandbox_read_range | Read bounded file ranges to avoid oversized responses. | BUILD if not already available. |
| P0 | capability_discover | Query the actual registered tool catalog, versions and schemas. | BUILD/EXPOSE only from the real MCP registry; must not return a static proposed list as runtime truth. |
| P1 | sandbox_diff | Compare before/after content for safe review. | Useful, but only after P0 and existing equivalent check. |
| P1 | artifact_verify | Readback + content hash for files written by an operation. | Useful; may initially be a verification workflow using existing readback if no native tool needed. |
| P1 | artifact_validate | Run named, bounded validators from an allowlist, never arbitrary commands. | Needed for automatic E2E after validator registry/security gate exists. |
| P1 | sandbox_patch | Guarded patch with expected-before hash/content. | Defer until diff, authorization and atomic write semantics are proven; existing write/create/append may suffice for simpler edits. |
| P2 | execution_submit/status/output_read | WorkContext-bound execution via Core -> W12/W13, isolated through approved runtime. | Required for AI-run-code workflows, but BLOCKED until identity, Core authorization, PC attestation, isolation and E2E are proven. No arbitrary shell/Python. |
| P2 | evidence_collect | Correlate request/task/run IDs, logs, hashes and evidence references. | Build alongside approved execution path, not as a standalone claim of verification. |
| P3 | pc_source_list/read/search | Controlled access to PC source via Work 24. | Defer until authenticated PC-initiated transport and Core route exist; no second bridge. |
| P3 | runtime_health | Report readiness of Core/MCP/Workspace/W12/W13/W24. | Useful only if it queries real health endpoints and reports unknown/degraded honestly. |

## Do not build yet
- Separate tool wrappers for every Work's functions unless a real user workflow needs them and Core authorization is defined.
- A second browser runner, execution host, PC bridge, or alternate route around Core.
- Unrestricted `python_run`, shell/command-string execution, or generic process-launch tools.
- Static tool-count dashboards that present proposed capabilities as registered runtime tools.
- Direct MCP tools for camera, voice, Gemini, video, ONT or product APIs before provider/device/product authorization and end-to-end contracts are ready.

## Minimal next step
1. Verify the canonical Core/Sandbox API for search, stat, range-read and capability discovery to avoid duplicates.
2. If absent, implement P0 read-only tools with Work-scoped path containment, bounded outputs, Core authorization, negative tests and readback evidence.
3. Independently collect live PC MCP tools/list and compare against the connected session tools.
4. Keep execution capabilities blocked until W12/W13/W27 gates pass.

## Current state
Decision record only; this document does not mean the proposed tools have been implemented or registered. Work 28 remains ACTIVE / NOT LOCKED. Live PC registry is UNVERIFIED. Release remains NO-GO while live E2E is BLOCKED.

## Ka decision — capability gap confirmed (2026-10-15)
Status reconciled against Nu's readback evidence:
- MCP connectivity: PASS
- Work 28 Sandbox read/write: PASS
- PC/Main-Source to Work 28 source transfer capability: MISSING
- Build/E2E: BLOCKED by source intake, not by MCP connection.

### Next implementation slice (design only; do not change PC/live MCP)
Specify a narrowly scoped, read-only source collector/transfer bridge with these gates:
1. Explicit allowlist of repository paths; default-deny everything else.
2. Exclude .env files, credentials/tokens, private keys/certificates, caches, runtime databases/state, logs with private data, and generated artifacts unless specifically approved.
3. Collect repository root, UTC timestamp, branch, HEAD, porcelain dirty/untracked status, included/excluded path list, file size and SHA-256 for every included file.
4. Produce a deterministic archive and SHA-256; preserve relative paths and do not normalize/rewrite source bytes.
5. Transfer only into Work 28 MCP-8020-TOOLING-PLATFORM/04_CODE/source_snapshot/ via an explicitly authorized upload/import capability; verify per-file hashes after readback.
6. Record collector version, command/exit code, manifest hash, archive hash and verification result. Never claim source snapshot imported until destination readback matches.
7. No arbitrary command execution, no source edits, no service restart, no registry mutation, no GitHub-main substitution.
8. After verified import: Nu performs source audit and isolated tests; Go independently reproduces results; Cla reviews security/trust boundaries; Ka reconciles gates. E2E remains blocked until then.

### Current decision
Keep Work 28 ACTIVE / NOT LOCKED; SOURCE_TRANSFER=BLOCKED; BUILD=NOT STARTED; REVIEW=NOT STARTED; E2E=BLOCKED; RELEASE=NO-GO. This is a design decision only and does not imply the transfer route exists or has been implemented.
