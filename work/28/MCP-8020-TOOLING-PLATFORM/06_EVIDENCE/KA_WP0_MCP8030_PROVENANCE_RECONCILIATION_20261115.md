# KA — WP0 MCP :8030 PROVENANCE RECONCILIATION

**Priority:** P0 — source/runtime provenance gate  
**Date:** 2026-11-15 (UTC+07)  
**Reviewer:** Ka — Independent Architecture & Security Review  
**Work:** 28 — MCP Tooling Platform  
**Branch inspected:** `work/28-mcp-tooling-platform`  
**Branch HEAD at inspection:** `9a19d6df9a2a7bb122817d65df90426b48b57116`  
**Disposition:** PARTIAL / BLOCKED — no live deployed MCP :8030 tools/list evidence

## 1. Scope and safety

Reviewed GitHub source and existing Work 28 inventory, and made read-only calls to the connected ROOM-HOP Build MCP surface for context, structure and Work listing. No call was made to the historical MCP :8020 listener. No code or runtime configuration was changed. The known `sandbox_read` defect was not probed. No tests were run in this review.

## 2. Pinned GitHub source evidence

| Artifact | Path | Blob SHA-1 |
|---|---|---|
| Historical 18-tool inventory | `work/28/MCP-8020-TOOLING-PLATFORM/00_GOVERNANCE/MCP8020_18_TOOL_RECONSTRUCTION_BASELINE.md` | `c597b89a74ec743b0b99a1955abe443dc55d04b1` |
| v54 contract catalog | `work/28/MCP-8020-TOOLING-PLATFORM/03_ARCHITECTURE/WORK28_TOOL_CONTRACT_CATALOG_V1_54.md` | `17028408aeb079a3e2b35cc3e87249ddc93b1c7d` |
| v54 catalog source | `work/28/MCP-8020-TOOLING-PLATFORM/04_CODE/mcp8020_catalog_v54.py` | `e51251f33ca8beb0d181cc8abdcb95875101faf1` |
| v54 service | `work/28/MCP-8020-TOOLING-PLATFORM/04_CODE/mcp8020_service_v54.py` | `5c420b6fb85b85fee8f3fddfd9f504f021c2cae8` |
| v54 MCP adapter | `work/28/MCP-8020-TOOLING-PLATFORM/04_CODE/mcp8020_server_v54.py` | `80365761d75fe27a1e8c7677f79c14ae90819c97` |
| Unified 31-tool registry | `work/28/MCP-8020-TOOLING-PLATFORM/04_CODE/mcp8020_unified_registry_v1.py` | `b3b975c7ccc16d76595bdb6fa695a088639a4e2c` |
| Unified server factory | `work/28/MCP-8020-TOOLING-PLATFORM/04_CODE/mcp8020_unified_server_v1.py` | `65ab9cd41da231c97e5094cb6fab0a6b9c3c84cb` |
| Sandbox v54 provider | `work/28/MCP-8020-TOOLING-PLATFORM/04_CODE/mcp8020_sandbox_tools_v54.py` | `9108d6bd8739f6c74be3ca483aa9c02520a385c9` |

## 3. Findings

### WP0-PROV-01 — Three competing registry/catalog generations (HIGH)

The branch contains three different public tool sets with different names and status semantics:

1. The historical baseline records 18 legacy tool names (dated 2026-10-21).
2. The v54 catalog declares 54 tools and labels individual entries IMPLEMENTED or NOT_IMPLEMENTED. Its module docstring explicitly says it is a design/contract catalog and does not claim live registration.
3. The unified registry declares 31 names: 18 legacy + 3 GitHub + 10 extensions. Its module docstring explicitly says it is a prepared contract and does not prove live registration.

The v54 names use forms such as `room_list_meetings`, while the 31-tool registry retains names such as `list_meetings`. They are not schema/name-equivalent registries. The branch does not identify one of these as the current deployed :8030 registry, nor provide a verified migration/version decision that resolves the competing sets.

**Risk:** a client can discover one name/schema set while code/tests/documentation validate another. Counting tools (18/31/54) is not registry parity.

### WP0-PROV-02 — Source factories are not deployment evidence (HIGH)

The v54 MCP adapter states that it does not open a listener; an external HTTP host owns transport and lifecycle. The unified server factory also states it does not open a listener and requires six provider groups to be supplied. These files prove source-level factories exist, not that either factory is used by the currently running Build MCP service.

The v54 service fails construction if a tool marked IMPLEMENTED lacks a callable provider handler. It returns NOT_IMPLEMENTED for explicitly disabled catalog entries. This is a useful fail-closed source design, but no exact deployed process/build identity or live tools/list response was captured in this review.

### WP0-PROV-03 — Connected Build MCP reports a limited capability surface, not raw MCP tools/list (MEDIUM)

Read-only calls to the connected Build MCP returned:
- get_room_context: service `room-hop-build`, version `1.0`, rule says Sandbox is the AI BUILD ZONE, Working Source read-only, Sandbox read/write.
- get_room_structure: service `room-hop-build`, version `1.0`, capability names listed: `sandbox_list`, `sandbox_read`, `sandbox_create`, `sandbox_write`, `sandbox_append`, `sandbox_delete`, `sandbox_create_work`, `sandbox_list_works`.
- sandbox_list_works: 66 Works returned.

These are outputs from the connected Build MCP helper calls. They are **not** a raw protocol-level `tools/list` response, do not expose full input schemas, and do not prove that the running service is the Work 28 deployment. The connected client also exposes a set of callable wrapper operations, but wrapper metadata is not a substitute for raw deployed MCP tools/list.

### WP0-PROV-04 — Sandbox Work inventory is not authorization/provenance proof (MEDIUM)

The Build MCP listed 66 Work entries and included Work 28. This proves that the connected Build MCP can enumerate those Sandbox records. It does not prove canonical Core Work identity binding, access-control enforcement per tool, correct Work-to-Sandbox mapping, or that this is the intended Work 28 deployment instance.

### WP0-PROV-05 — Binary upload remains absent from reviewed contracts (HIGH for WP3-F01)

Neither the v54 catalog excerpt/source nor the 31-tool unified registry includes `sandbox_upload_file` or a streaming upload session contract. The sandbox provider source shown is text-oriented for `sandbox_write` and `sandbox_append`. This is consistent with the prior WP3 source trace; it is not evidence of a live deployed upload handler.

## 4. What is and is not proven

**Proven by this review**
- Exact GitHub branch HEAD and the listed source/document blob SHAs were read from the canonical branch.
- Three distinct catalog generations exist in the branch (18, 31, 54) with different names/contracts.
- v54 and unified MCP server source factories explicitly do not own/open the listener.
- Connected Build MCP helper calls report service label/version and an eight-capability structure list, and list 66 Work records.

**Not proven**
- Current raw MCP :8030 `tools/list` names, complete JSON schemas, order or digest.
- Exact live process/deployment identity, executable/source commit, build hash, host/port binding or startup command.
- Source-to-runtime correspondence for v54 or unified registry.
- That the 66 listed Work records are all correctly authorized for the caller.
- Any live `tools/call` parity, safe read/write, or binary upload behavior.

## 5. Required closure evidence

1. Xu/Vi identify the one intended current :8030 deployment and canonical registry version; record why the 18/31/54 generations are current, superseded or archival.
2. Capture a raw protocol-level `tools/list` response from the approved :8030 service, including complete schemas, exact response bytes and SHA-256.
3. Capture deployment identity from the same process/session: service identity, build/source commit, executable or package identity, startup configuration (secrets redacted), host/port and timestamp.
4. Bind the raw `tools/list` digest to the deployment identity and canonical source commit. A separately queried GitHub registry digest is not enough unless the runtime reports the same build/source identity.
5. Run only approved non-destructive representative calls against that identified :8030 instance, with request/response evidence and Core authorization context. Do not probe `sandbox_read` while its known defect remains quarantined.
6. For WP3-F01, continue to require the separate Q4 capability-grant decision and upload contract approval; do not infer upload authorization from existing Sandbox helper access.

## 6. Review decision

**WP0: PARTIAL / BLOCKED.** GitHub source inventory has enough evidence to identify catalog drift and source/runtime uncertainty, but the required live provenance and raw tools/list evidence are absent. G0 remains OPEN. WP3 runtime provenance is NOT VERIFIED. No tool-count or deployment PASS is issued.

**Safety:** Historical MCP :8020 remains DO NOT USE. Execution Gate remains CLOSED. Work 28 remains ACTIVE / INTEGRATION BLOCKED / NOT RELEASED.

**Next owner:** Xu to resolve registry/deployment identity and coordinate an approved read-only raw :8030 tools/list evidence capture; Vi to supply source-to-deployment mapping; An to independently reproduce protocol-level discovery and schema digest once an identified target is provided; Ka to re-review the exact pinned evidence.
