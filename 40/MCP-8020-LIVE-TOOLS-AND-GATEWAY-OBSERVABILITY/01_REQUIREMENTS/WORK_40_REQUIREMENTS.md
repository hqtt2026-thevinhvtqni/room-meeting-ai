# Work 40 — Requirements and Verification Plan

## User goal
Understand port 8020: its exposed MCP tools and which tools are actually operating.

## Required inventory fields
- Tool name
- Description/purpose
- Input schema
- Read-only, recording/write, or authority-changing behavior
- Immediate handler / downstream dependency when traceable
- Invocation attempted?
- Result classification: PASS / FAIL / BLOCKED / NOT TESTED
- Timestamp and evidence reference
- Error text or response summary

## Verification sequence
1. READ — inspect existing Work 28 evidence and ROOM-HOP runtime contract.
2. TRACE — establish live endpoint, transport, `tools/list`, and tool dispatch path.
3. ANALYZE — compare listed tools with actually callable tools and dependencies.
4. VERIFY — run safe read-only calls, capturing exact outputs/errors.
5. DECIDE — classify findings with evidence; do not infer live health from static files.
6. HANDOFF — provide a concise inventory, blockers, and approved next actions.

## Safety constraints
- Initial phase is read-only.
- Do not call write/delete/meeting lifecycle operations just to test availability.
- Do not change PC or GitHub.
- If the available connector does not expose a needed diagnostic, record BLOCKED and name the missing evidence instead of fabricating it.

## Initial baseline (2026-10-19)
- ROOM-HOP context returned status=ok and identifies MCP :8020 as the AI/agent boundary into ROOM-HOP; Core :8000 is the single source of truth.
- Sandbox work inventory returned 42 works before Work 40 creation; Work 40 was then created successfully through the Sandbox API with identity `xu`.
- This baseline does NOT yet prove the actual PC process, live port binding, live `tools/list` contents, or health of every tool.
