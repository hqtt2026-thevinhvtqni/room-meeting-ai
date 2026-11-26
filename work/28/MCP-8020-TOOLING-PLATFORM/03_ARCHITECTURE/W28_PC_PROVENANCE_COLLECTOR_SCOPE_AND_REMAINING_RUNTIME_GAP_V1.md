# W28 PC Provenance Collector Scope & Remaining Runtime Gap — V1

**Date:** 2026-11-27 (UTC+07:00)  
**Owner:** Ka — delegated W28 implementation / architecture owner  
**Status:** EXISTING PC EVIDENCE PATH FOUND / CURRENT RUN NOT AVAILABLE  
**Branch:** `ka/w28-f01-handle-backend-20261127-r5`

## 1. Discovery and correction

A read-only audit of Work 28 Sandbox inventory found existing approved artifacts:
- `06_EVIDENCE/PC_READONLY_LIVE_PROVENANCE_COLLECTOR_20261123.md`
- `06_EVIDENCE/PC_READONLY_LIVE_PROVENANCE_COLLECTOR_20261123.ps1`
- `06_EVIDENCE/VI_LIVE_PROVENANCE_ANALYSIS_20261123.md`

Therefore, the previous conclusion must be stated precisely: MCP 8030 itself has no host-inspection or command-execution action, but a documented PC-side, read-only collector exists. The collector requires execution by an operator on the Windows PC; Ka cannot run it through the currently exposed MCP 8030 tools.

## 2. Existing collector scope

The script is designed to:
- Read local Git branch, HEAD and short dirty-tree status.
- Enumerate listeners on ports 8000, 8001, 8030 and 8031 with PID, executable, parent PID, creation time and parsed Python module name.
- Hash selected local source files.
- Perform MCP initialize and `tools/list` only against the recorded endpoint `https://admin-pc.tail7d6101.ts.net/build/mcp`.
- Avoid tools/call, port 8020, process restart, repository writes, credentials and full process command lines.
- Write evidence under `%TEMP%\W28_LIVE_PROVENANCE_<timestamp>`.

This is PC listener/source provenance, not an upload-service filesystem capability probe.

## 3. Existing prior evidence (2026-11-23)

The recorded VI analysis reports:
- PC checkout branch `main`, HEAD `05db862cd2ff01cd288cf64cf0be5a9aa05ee816`, dirty.
- Listeners: 8000 PID 2884 (`room_hop_mcp.http_main`), 8030 PID 7160 (`room_hop_mcp.mcp_build_http_main`), 8031 PID 18540 (`execution_host.server`).
- Remote endpoint initialize/tools/list succeeded with 17 tools.
- Local listener module-file hashes were recorded, but do not prove bytes loaded in memory or endpoint-to-PID mapping.
- Canonical Work28 deployed-source alignment, Core authority runtime, and runtime integration remained unverified.

These are historical user-supplied collector observations, not current state.

## 4. What the collector does not establish

It does not capture:
- Effective Windows token SID/privileges, process integrity level, ACLs on the actual Sandbox root/staging directories.
- Exact file identity/handle semantics or safe no-replace publication.
- Linux UID/GID/capabilities, kernel, mount namespace or filesystem behavior.
- Whether the upload service is running in a distinct process/container/runtime from the listed listeners.
- Runtime upload/readback E2E or exact bytes/SHA-256 roundtrip.

It therefore cannot close F01. The 2026-11-23 output must not be treated as current or as proof of filesystem safety.

## 5. Minimal next evidence request

The existing collector may be rerun on the PC only if the operator confirms that the repository path and recorded endpoint are still the intended target. Return only:
1. `summary.txt`
2. `mcp_tools_list_raw.txt`, if created
3. Exact evidence folder timestamp

Do not return environment variables, .env files, credentials, authorization headers, full process command lines or unrelated process data.

After readback, separately determine whether the upload service process and its actual Sandbox path can be identified. Any filesystem ACL/handle/capability probe requires a separately reviewed read-only or disposable-lab procedure; do not add it to this collector or run mutations implicitly.

## 6. Disposition

- Existing PC provenance collector: FOUND / documented.
- Current collector run: NOT AVAILABLE in this session.
- Prior 2026-11-23 evidence: HISTORICAL / NOT CURRENT.
- Actual upload runtime filesystem security evidence: NOT OBSERVED.
- F01 BLOCKED; F02 PARTIAL / NOT VERIFIED; F03/F04 BLOCKED.
- Execution Gate CLOSED / NOT RELEASED.
