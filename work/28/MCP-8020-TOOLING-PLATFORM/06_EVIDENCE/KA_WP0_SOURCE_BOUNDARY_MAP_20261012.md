# WORK 28 — WP0 SOURCE / BOUNDARY DISCOVERY
Date: 2026-10-12 (+07)
Prepared by: Ka (CSA), independent technical coordinator
Work status: ACTIVE / NOT LOCKED
Scope: read-only inspection of GitHub repository source through the connected GitHub integration plus ROOM-HOP architecture/context. No repository files were modified.

## 1. Snapshot identity and limits
- Repository: `hqtt2026-thevinhvtqni/room-meeting-ai` (private).
- Default branch reported by repository metadata: `main`.
- Most recent commit returned by commit search at inspection time: `d7c90d9d31062d389810808e43dfdd19d7711b75` — “feat(work13): add W12 execution host bridge and W14 E2E”, authored 2026-10-09T21:51:11Z.
- Important limit: this is a GitHub source snapshot. The deployed PC process, current local HEAD, running MCP :8020 registry, Core :8000 runtime routes and live W13 process identity were NOT queried by these GitHub file reads. Do not treat the GitHub snapshot as proof of deployed runtime identity.

## 2. Source map (paths and blob SHA)
| Boundary | Source path | Blob SHA | Observation |
|---|---|---|---|
| MCP entrypoint | `room_hop_mcp/__main__.py` | `43adaa746f8e51a6ecce762a7b01694d0411d105` | Constructs MeetingManager → MeetingService → adapter; stdio server. |
| MCP public adapter | `room_hop_mcp/adapter/server.py` | `f34b4eebc847dac31feb7c9161c2d8bded812991` | Registers list_meetings/get_meeting/get_transcript/add_paste_to_meeting. No execution tool is registered in this adapter source. |
| Core application service | `core/meeting_service.py` | `0b80a81663c1be328c41878a6762d16d95378aab` | MeetingService delegates to MeetingManager; public read DTOs and transcript operations. No execution dispatch method shown in inspected source. |
| Alternate HTTP execution handler | `execution_host/server.py` | `45aec57525b5d55bb63544b7bd7fd23062e06151` | POST /execute parses caller JSON into WorkContext/ExecutionRequest and calls host. No request authentication visible in this handler. |
| Alternate execution host | `execution_host/host.py` | `977b5bc5072eaf0a3ad054aecd22491483d621b1` | Starts subprocess; writes evidence, validates context and command. Must not be exposed to MCP before security review. |
| Alternate execution policy | `execution_host/security.py` | `4aa20fbc9c5939c49c85222916dc28fb8dd8075b` | Allowlisted executable names but permits Python `-c`; command allowlisting does not isolate arbitrary Python. |
| Alternate execution request/result | `execution_host/models.py` | `2488b7c95cf3784fc26eaf677044fe5ab0866420` | WorkContext includes caller-supplied `authorized: bool`; server deserializes it directly. This is not a trustworthy authorization principal. |
| WEE authority | `wee/authority.py` | `31375a230005e224a22039d80bda0dda3433203c` | CanonicalWorkAuthority reads a specific Work binding; it does not discover/guess ambient target. |
| WEE context/evidence | `wee/models.py` | `bc5831c2178be3937c7ddb600169b27981034c1a` | WorkContext binds Work/repository/branch/expected_head/entrypoint/evidence root; EvidenceStore writes execution-scoped files. |
| WEE lifecycle | `wee/controller.py` | `fb2cbd2dc309f2816c1bd71579feb4363f2e2ddc` | Current controller explicitly returns TEST BLOCKED because adapter must execute bound entrypoint; does not establish live test execution by itself. |
| WEE host contract | `wee/bridge/contracts.py` | `3834c7cf10621d083625ab89fa969b7a97524590` | Typed ExecutionResult and host protocol. |
| WEE local host | `wee/bridge/local_host.py` | `bc6406b8c933d6d72f3fb520a575820141fd849c` | Local host calls subprocess directly without OS-level isolation in this inspected file. Not acceptable as arbitrary-AI-code isolation proof. |
| WEE real host | `wee/bridge/real_host.py` | `0f9b37af2f49cda63a050a86ff63bfd91f9f4c76` | RealExecutionHost requires enabled=True, but invokes subprocess.run with inherited environment and no visible OS sandbox; bounded timeout/kill-tree controls are not visible in this method. |
| W13 adapter | `wee_work13_adapter.py` | `73cfda2167219c5b6fbf6719e6066ed230dfa52c` | Adapter delegates to RealExecutionHost (provider_type W12_REAL_EXECUTION_HOST); this is the candidate canonical seam, but integration/reachability is not proven. |
| W12/W13 integration test | `tests/test_work13_wee_integration.py` | `f3c204f1763cefd79c63dd40173d56f3715d0cf6` | Unit/integration test constructs authority and adapter locally; does not prove MCP :8020 → Core :8000 live routing. |
| Execution host tests | `tests/test_execution_host.py` | `183cba2959db9d9fb00751055efdeddd09c14a64` | Tests the alternate execution_host, not the live MCP execution path. |

## 3. Boundary conclusions
1. Observed public MCP adapter is MeetingService-backed and exposes only meeting/read/recording tools. No Python/execution tool appears in the inspected adapter source.
2. Inspected Core MeetingService is not an execution authorization router. The actual Core :8000 execution route/principal binding is not present in the reviewed source set; mark BLOCKED, do not invent one.
3. WEE/W13 has an authority/context/evidence seam worth investigating further, but current evidence only proves source-level classes and local test design. It does not prove the process is deployed, reachable, authorized, or safe for untrusted AI Python.
4. Do not wire MCP directly to `execution_host/server.py`; the handler accepts caller-serialized `authorized` and has no visible authentication. Do not use `execution_host/host.py` as a shortcut/second host.
5. `wee/bridge/real_host.py` currently uses subprocess with inherited environment and lacks visible OS-level sandbox controls in the inspected method. Python is effectively arbitrary code; command ID/validator alone cannot make it safe.
6. WEE LifecycleController currently stops at TEST BLOCKED (“execution adapter must run the bound entrypoint”). This is honest but means the full loop is not complete.
7. Sandbox file API does not expose a principal argument in its public tool schemas; connector/Core authorization may exist outside those schemas, but cross-Work enforcement must be demonstrated with negative tests. Sandbox evidence artifacts are writable by the same broad file tools, so review/evidence integrity is not guaranteed by the Sandbox surface alone.

## 4. Required next source evidence (still BLOCKED)
- Actual deployed/local commit SHA for the PC process listening on :8020 and :8000.
- Live MCP `tools/list` output and exact server startup command/config.
- Actual Core :8000 execution route, middleware, authenticated principal source, WorkContext resolver and authorization decision trace.
- Actual W13 runtime process identity/build hash and authenticated transport, if present.
- OS-level isolation proof: filesystem boundary, no host secrets, network restrictions, resource limits and process-tree cleanup.
- Protected evidence writer/readback that agents cannot overwrite/delete.
- Live negative tests proving unauthorized Work and spoofed `authorized=true` cannot execute.

## 5. WP0 verdict
- GitHub source inspection: DONE for the paths listed above.
- Deployed runtime/Core source alignment: BLOCKED.
- Execution integration approval: NO-GO.
- Safe next step: harden the pure contract/tests in this Work Sandbox and prepare a precise integration contract; do not register or enable `python_run`.
