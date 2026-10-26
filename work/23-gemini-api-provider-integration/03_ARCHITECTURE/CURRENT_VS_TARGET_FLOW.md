# Current vs Target Flow — Work 23
Date: 2026-10-10
Status: TARGET DOCUMENTED; CURRENT RUNTIME NOT VERIFIED

## Target flow
Agent/AI → MCP :8020 → Core :8000 → Gemini Provider Adapter → Gemini API.

Core :8000 remains the single source of truth. Agent/frontend must not call Gemini directly to bypass policy, authorization, audit or usage metering.

## Related document flow
Gemini response → Core/MCP-controlled workflow → Work 05 Google Workspace Docs/Drive Adapter → Google Docs/Drive. Work 05 uses OAuth credentials; Work 23 uses Gemini API credentials. They are not interchangeable.

## Current evidence
The adapter source exists in Work 23 Sandbox. Its REAL_API branch currently raises NotImplementedError. No evidence proves that the adapter is wired into Core, MCP :8020, or a running ROOM-HOP request path.

## Gaps
1. Inspect the authorized repository/branch and locate the provider seam.
2. Implement behind the existing contract without modifying out-of-scope Core/MCP sources.
3. Verify mock request flow and collect boundary logs.
4. Run real API E2E only with authorized credentials, access and cost.