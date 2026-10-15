# KA — Work 28 P0 Source Trace (read-only)
Date: 2026-10-15 UTC+07
Owner: Ka CSA / Work 28 Coordinator
Authority: Vinh
Status: SOURCE TRACE PARTIAL / BUILD BLOCKED AT DEPLOYED-SOURCE BINDING

## Scope actually inspected
1. Work 28 assignment: `MCP-8020-TOOLING-PLATFORM/06_EVIDENCE/KA_WORK28_NEXT_EXECUTION_ASSIGNMENT_20261015.md`.
2. Work 28 cross-work inventory, gap decision and registry design in Sandbox.
3. Read-only ROOM-HOP source tree and architecture from the connected ROOM-HOP connector.
4. GitHub-connected private repository `hqtt2026-thevinhvtqni/room-meeting-ai`, branch `main`, source files:
   - `room_hop_mcp/__main__.py` (Git blob SHA reported by GitHub contents API: `43adaa746f8e51a6ecce762a7b01694d0411d105`)
   - `room_hop_mcp/adapter/server.py` (Git blob SHA reported by GitHub contents API: `f34b4eebc847dac31feb7c9161c2d8bded812991`)
   - `room_hop_mcp/adapter/http_server.py` (read source; not runtime-attested)
   - `core/meeting_service.py` (read source; not runtime-attested)

## Findings grounded in source
### MCP registration in repository main
The inspected `room_hop_mcp/adapter/server.py` registers only four tools through its `list_tools()` handler:
- `list_meetings`
- `get_meeting`
- `get_transcript`
- `add_paste_to_meeting`

Its `call_tool()` handler dispatches those same four names to `MeetingService`. The source inspected does not register `sandbox_search`, `sandbox_stat`, `sandbox_read_range`, or `capability_discover`.

This is evidence about the inspected GitHub `main` source only. It is NOT proof of the currently loaded PC listener on :8020.

### Core/Sandbox API trace
- `core/meeting_service.py` is a meeting-domain application service. The inspected methods cover meeting list/read/transcript/lifecycle/recording. No Work-artifact search, file stat, bounded range read, or MCP registry-discovery method was found in this file.
- `room_hop_mcp/adapter/http_server.py` routes meeting HTTP operations through `MeetingService`; its inspected code does not expose the four P0 Work-artifact/registry capabilities.
- The connected ROOM-HOP context identifies Sandbox as a separate AI BUILD ZONE and MAIN SOURCE as read-only for AI build operations.
- The connected tool surface exposes 18 operations, including Sandbox operations, but that is a different surface from the four tools registered by the inspected GitHub-main MCP adapter.
- A lookup for `room_hop_mcp/sandbox_service.py` on repository `main` returned 404. Therefore the Sandbox connector implementation seen in this session has not been tied to this GitHub-main source path.

## P0 decisions
| Capability | Repository-main source result | Decision |
|---|---|---|
| `sandbox_search` | Not present in inspected MCP registration or `MeetingService`; actual connected Sandbox backend source not bound to this revision | DESIGN GAP CONFIRMED IN INSPECTED FILES; live implementation target UNVERIFIED |
| `sandbox_stat` | Same | DESIGN GAP CONFIRMED IN INSPECTED FILES; live implementation target UNVERIFIED |
| `sandbox_read_range` | Same | DESIGN GAP CONFIRMED IN INSPECTED FILES; live implementation target UNVERIFIED |
| `capability_discover` | Actual MCP `list_tools()` exists in inspected adapter, but no separate discovery tool; adapter's own list is the canonical mechanism within that server | Do NOT add a duplicate discovery wrapper until deployed listener/source identity is established |

## Why implementation is not started in canonical source
The inspected repository-main adapter does not match the 18-operation connected ROOM-HOP connector surface, and neither is bound to the PC :8020 listener PID/source revision. The approved tooling available in this session can read/write Work Sandbox artifacts and fetch repository source, but cannot edit the PC working tree or prove which file the live listener loaded. Writing P0 code into Work 28 Sandbox would create another unregistered implementation, not a working MCP tool; that would violate the no-duplicate/no-false-PASS rule.

## Required one-shot PC evidence to unblock build and E2E
From the PC owner/runtime, provide read-only evidence:
1. exact listener command/module and working directory for PID bound to 127.0.0.1:8020;
2. deployed Git HEAD/branch and clean/dirty status;
3. exact loaded MCP entrypoint/registration source paths and SHA-256 for entrypoint + relevant adapter/Sandbox service files;
4. raw JSON-RPC `initialize` and `tools/list` response from that same endpoint, with timestamp and endpoint identity;
5. the actual Core :8000 authorization route/policy used for Work-scoped reads.

Do not include secrets, environment values, or unrestricted command output. Do not restart or mutate the live service.

## Test and gate status
- Source inspection: DONE for the files listed above.
- Unit tests: NOT RUN in this execution; no test runner was invoked.
- Security-negative tests: NOT RUN.
- Connector-level Sandbox reads: observed callable, but not evidence for new P0 tools.
- Live PC :8020 registry: BLOCKED / UNVERIFIED.
- MCP -> Core -> authorized capability -> readback E2E: BLOCKED / NOT RUN.
- Work 28: ACTIVE / NOT LOCKED.
- Release: NO-GO.

## Signature
Ka — CSA / Work 28 Coordinator (textual signature; not cryptographic).
