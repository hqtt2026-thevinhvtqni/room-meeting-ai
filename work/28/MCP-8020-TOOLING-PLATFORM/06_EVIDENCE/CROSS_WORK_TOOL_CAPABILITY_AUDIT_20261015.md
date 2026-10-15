# Work 28 — Cross-Work Tool Capability Audit
Date: 2026-10-15
Status: SOURCE-INVENTORY COMPLETE / INTEGRATION UNVERIFIED

## Executive finding
Multiple tool-related Works contain source code, contracts, adapters, test plans and evidence artifacts. However, their presence in Sandbox does not prove registration or invocation through the live PC MCP :8020 endpoint. The connected ROOM-HOP session exposes 18 operations; this is not proof of the PC runtime tools/list.

## Work-by-Work inventory
| Work | Capability/source observed | Work 28 integration status |
|---|---|---|
| 01 AI-BUILD-GATEWAY | Gateway identity, authentication, authorization, MCP boundary and Work 99 gate/middleware code/tests. | Candidate entry/policy boundary; live link to MCP :8020 unverified. |
| 02 MCP-UNIFIED-AUTHORIZATION | Authorized boundary, unified authorization gate and tests. | Must be traced/reused; live enforcement by Work 28 unverified. Core remains authority. |
| 05 Google Workspace Docs/Drive | Adapter, provider/connection code and E2E evidence package. | Provider capability candidate; Core route and MCP registration unverified. |
| 08 VSCode-Web | Web editor/workspace files. | UI/client, not itself an MCP tool registry; invocation route unverified. |
| 09 / 091 Browser Agent + Workflow Engine | Browser adapter, workflow engine, runners and historical E2E evidence. | Candidate BUILD/EXECUTE adapter; current readiness and approved runtime link must be verified. |
| 10 Computer Agent | Agent runtime/API/browser adapter plus action/safety contracts and tests. | Candidate client; public MCP exposure unverified. |
| 12 WEE | execute_work WorkContext contract, controller/runtime, bridge, test runner and tests. | Canonical execution contract candidate; real E2E blocked by missing authorized host capability. |
| 13 Execution Host | execution_host adapters, WEE :8031 bridge, tests and evidence. | Canonical host candidate; live PC attestation/route incomplete. Do not duplicate host. |
| 14 Autonomous E2E Builder | Builder/browser workflow and security validator staging v2-v4 with evidence. | Orchestrator/consumer; must use W12/W13; security and live E2E gates remain. |
| 16 Workflow Engine | Workflow engine, contracts and historical run evidence. | Orchestration candidate; current MCP registration/runtime readiness unverified. |
| 20 Create Agent | Agent credential, skill/tool MCP binding, runtime binding and cost contracts. | Contracts/source snapshots exist; actual Core/registry binding unverified. |
| 21 AI Skills | Skill contract, manifest schema and tests. | Skill metadata is not a callable MCP tool; binding unverified. |
| 22 Security & Safety | Security/message contract materials. | Cross-cutting policy input; runtime enforcement unverified. |
| 23 Gemini Provider | Provider adapter, connector factory/smoke tests and recorded test evidence. | Core provider candidate; direct Work 28 MCP exposure unverified. Work 23 evidence is not MCP integration evidence. |
| 24 PC Source/Workspace Bridge | Bounded list/read/search, path containment, audit/hash, diff-before-write design and Core transport seam. | Sole PC source bridge candidate; no real authenticated PC transport/Core route. Tests authored but not run through this Sandbox connector. |
| 26 Camera/Voice | Fail-closed adapter stubs, contracts/tests and source audit. | No public MCP camera/voice/STT/TTS tools found in audit; not registered. |
| 27 Sandbox Execution Runtime | Runtime architecture and execution contract; explicitly avoids competing host/arbitrary shell. | Isolation extension behind W12/W13; callable execution capability unverified. |
| 28 Tooling Platform | tool_contracts.py, tests, registry design, and evidence records. | Contract code exists in Sandbox; proposed registry additions remain draft/not registered. |
| 29 AI Video Studio | Pipeline README and pipeline tests. | Pipeline capability candidate; callable MCP route/provider integration unverified. |
| 89 Xi Mang Nghi Son | Product API schema, E2E plan and implementation/evidence packs. | Product API is not automatically an MCP tool; Work 28/Core mapping unverified. |
| 97 Voice minutes experiment | Work sandbox exists. | Live MCP exposure not established by this audit. |
| 98 ONT Care | Product code/readmes and E2E materials exist in Sandbox. | ONT actions need typed, authorized capabilities; registry integration unverified. |
| 99 Work Index/Gateway | Work registry, AI tools directory and gateway integration baton. | Inventory/coordination source, not proof external AI services are MCP tools. |

## Connected ROOM-HOP tool surface observed in this session
- Meetings (6): list_meetings, get_meeting, get_transcript, join_meeting, start_meeting, add_paste_to_meeting.
- Sandbox (8): sandbox_create_work, sandbox_list_works, sandbox_list, sandbox_read, sandbox_create, sandbox_write, sandbox_append, sandbox_delete.
- Orientation (2): get_room_structure, get_room_context.
- Agent flow (2): get_pending_tasks, submit_proposal.
- Total: 18 operations callable through the connected tool surface. This does not establish the PC MCP :8020 runtime inventory.

## Capability maturity for Work 28
- READ: Sandbox list/read and meeting/context reads are callable here. sandbox_search, sandbox_stat, sandbox_read_range and capability_discover are proposals, not verified live tools.
- BUILD: Sandbox create/write/append/delete are callable here; guarded patch/diff/validation tools are not verified live.
- EXECUTE: execution_submit/status/output_read and python_run are not verified registered. Arbitrary Python/shell stays disabled.
- VERIFY: no live artifact-hash, validator or evidence-collection tool was verified; current evidence relies on file creation/readback and separate reports.
- RELEASE: no release/commit/push tool verified on this connected ROOM-HOP surface.
- CONTROL: meeting and agent task/proposal operations are callable; live gateway/policy enforcement is unverified.

## Integration sequence
1. Capture raw tools/list from the exact PC MCP :8020 endpoint with timestamp, endpoint identity, revision and SHA-256; compare against this connected session surface.
2. Trace Core :8000 authorization and Work 01/02 policy path; MCP must not bypass Core.
3. Add bounded READ capabilities only after source registration, authorization tests and negative security tests.
4. Route execution only through Work 12 -> Work 13 canonical host, with Work 27 isolation and Work 14 as consumer; require real PC attestation and E2E evidence.
5. Integrate Work 24 as the only PC source bridge after authenticated Core/PC transport exists.
6. Integrate Work 05/23/26/29/89/98 capabilities via typed adapters after each has explicit Core-authorized contracts and real tests.
7. Add artifact verification/evidence collection and release gates.

## Decision
Work 28: ACTIVE / NOT LOCKED. Connected-session operations: 18 observed. Live PC MCP :8020 registry count: UNVERIFIED. New registry capabilities: draft only until registration evidence. Python/arbitrary shell: NOT ENABLED. Live MCP -> Core -> capability -> readback E2E: BLOCKED / NOT VERIFIED. Release: NO-GO.

## Addendum — live connector inventory check (2026-10-15)

### What was actually queried in this check
- `sandbox_list_works`: returned `status=ok`, `count=39` Work records. 37 records report `manifest_exists=true`; Work 15 and Work 98 report `manifest_exists=false`.
- `get_room_structure`: returned `status=ok`, source label `MAIN_SOURCE`, `read_only=true`. This is a path tree, not file-content access or proof of a live PC :8020 tools/list.
- `get_room_context`: returned `status=ok`, source label `MAIN_SOURCE`, `read_only=true`; it states Core :8000 is single source of truth, Dashboard :3000 render-only, App Workspace :8010 separate, MCP :8020 agent boundary, Sandbox is build zone separate from MAIN SOURCE.
- Work 28 `sandbox_list` and reads of this audit, `MCP_TOOL_REGISTRY_V1.md`, `TOOL_GAP_DECISION_20261015.md`, and MCP recovery minutes all returned content in this connector call.

### Reconciliation
- This connector path is callable at the time of this check; this does not resolve the earlier Xu-session `Connection failed` report and does not prove PC listener/Funnel or remote transport.
- 39 Work records are discoverable, but this is not a complete source-level audit of all 39 Works. The table above is a focused inventory of tool-related Works. The two missing manifests (15, 98) require separate intake review before their tool needs can be responsibly assessed.
- The connected tool surface remains 18 operations as declared by the current tool definitions. No runtime `tools/list` result from the exact PC :8020 endpoint was obtained in this check.
- Existing proposed P0 remains: `sandbox_search`, `sandbox_stat`, `sandbox_read_range`, `capability_discover`. Before implementation, trace canonical API/source to prevent duplicates; capability discovery must query the real registry, not a static list.
- Execution tools remain blocked until Core authorization and the canonical Work 12 -> Work 13 host path with Work 27 isolation are verified. PC source operations must reuse Work 24, not a second bridge.

### Gate status
Work 28 ACTIVE / NOT LOCKED. Sandbox connector access in this check: PASS. Direct Xu-to-PC MCP 8020 path: NOT VERIFIED. Live PC registry: UNVERIFIED. Execution/E2E: BLOCKED. Release: NO-GO.
