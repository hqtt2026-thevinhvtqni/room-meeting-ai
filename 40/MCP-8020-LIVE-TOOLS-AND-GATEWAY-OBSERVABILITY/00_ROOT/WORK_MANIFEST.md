# WORK 40 — MCP :8020 LIVE TOOLS & GATEWAY OBSERVABILITY

- Work ID: 40
- Work name: MCP-8020-LIVE-TOOLS-AND-GATEWAY-OBSERVABILITY
- Owner / decision authority: Vinh
- Coordinator: Xu (AI-01, GPT, CEO / Quân sư LAB — HQTT AI)
- Created: 2026-10-19 (Asia/Ho_Chi_Minh)
- Status: ACTIVE — INITIALIZED; implementation and live verification NOT YET VERIFIED

## Purpose
Create one evidence-based place to inspect the ROOM-HOP MCP gateway on port 8020 and identify which tools are actually exposed and working.

## Scope
1. Identify the live MCP endpoint and its protocol/transport.
2. Retrieve the live `tools/list` result and inventory each tool.
3. Distinguish tools that are merely registered/listed from tools that have been successfully invoked.
4. Test tool behavior with safe, read-only probes first; record request, result, errors, timestamp, and evidence.
5. Trace each tool through MCP :8020 to Core :8000 and any downstream service where evidence permits.
6. Record blockers, ownership, and next steps.

## Out of scope
- No PC configuration or source changes without Vinh's explicit approval.
- No direct filesystem/database access that bypasses Core.
- No writes, deletes, commits, pushes, or lifecycle-changing actions during the initial audit.
- No PASS claim based only on a tool name, source file, or `tools/list` entry.

## Acceptance criteria
- [ ] Live endpoint/transport confirmed from runtime evidence.
- [ ] Full live `tools/list` response captured with timestamp and digest or equivalent immutable evidence.
- [ ] Every listed tool has a record: name, purpose, input schema, read/write impact, dependency path, test status, evidence.
- [ ] Invoked tools are classified PASS / FAIL / BLOCKED / NOT TESTED with exact evidence.
- [ ] At least one safe end-to-end probe traces MCP → Core → expected response, if supported by available tools.
- [ ] Findings and handoff are recorded without overstating confidence.

## Evidence policy
Use DONE / PASS / DECISION / BLOCKED. Keep source-derived claims separate from live-runtime observations. Record actor identity, role, local timestamp, operation, result, and evidence location.
