# KA — P0 API Trace + Manifest Schema Review
Date: 2026-10-15
Role: Ka / CSA — Work 28
Scope: Steps 1 and 2 requested by Vinh. Static review only; no code/runtime changes.

## Result
- Step 1: PARTIAL. P0 candidates absent from the connected 18-operation surface and from the reviewed Work 28 SandboxOperation enum, but equivalent canonical Core/Sandbox APIs have not been ruled out.
- Step 2: BLOCKED. Canonical Work manifest schema and validator were not verified. No manifest was created for Work 15 or Work 98.

## Evidence
- 03_ARCHITECTURE/MCP_TOOL_REGISTRY_V1.md: DRAFT / NOT REGISTERED IN LIVE MCP. P0 candidates are sandbox_search, sandbox_stat, sandbox_read_range, capability_discover. The 18 connected operations do not prove the PC :8020 registry.
- 06_EVIDENCE/TOOL_GAP_DECISION_20261015.md: requires canonical API duplicate-check before building; capability_discover must query the real registry.
- 06_EVIDENCE/CROSS_WORK_TOOL_CAPABILITY_AUDIT_20261015.md: Work 01 gateway/policy, Work 02 unified authorization, Work 24 sole PC source bridge; live enforcement/transport remains unverified.
- 04_CODE/tool_contracts.py: CONTRACT_VERSION 1.3.0; pure validation/data contracts, no filesystem/network/Core/runtime side effects. SandboxOperation enum contains LIST, READ, CREATE, WRITE, APPEND, DELETE, but no SEARCH, STAT, RANGE_READ or DISCOVER. READ has byte limits but the reviewed request shape has no range parameters. TrustedPrincipal/WorkContext are data contracts, not proof of authentication/authorization.

## Step 1 — API trace matrix
- sandbox_search: not in connected tool names or Work 28 SandboxOperation enum; canonical Core/Sandbox equivalent NOT VERIFIED. Keep candidate; do not implement yet.
- sandbox_stat: same status; equivalent NOT VERIFIED.
- sandbox_read_range: not exposed in connected tool names or request shape; equivalent NOT VERIFIED.
- capability_discover: not exposed in connected tool names; exact PC :8020 tools/list and live registry source NOT VERIFIED. Must not return a static proposed list as runtime truth.

Before implementation, trace Work 01 trusted identity/gateway, Work 02 authorization, canonical Core/Sandbox methods/path containment/limits, and Work 24 authenticated PC transport. Capture exact PC :8020 tools/list only when authorized access is available. This report does not authorize implementation.

## Step 2 — Manifest schema
- Work 15 and Work 98 report manifest_exists=false, while their source trees exist. This is an intake/metadata gap, not missing source.
- Work 21 is described as containing a skill manifest schema. A skill manifest is not automatically the canonical Work Sandbox manifest.
- Required Work manifest fields, versioning, identifier rules and validator were NOT verified. No manifest was created and no schema is labelled canonical.
- Next: Cla/Work 99/Sandbox owner should identify the canonical Work manifest schema and validator. Compare with at least one existing valid manifest, then draft and validate Work 15/98 proposals in Sandbox and read back. Do not invent required fields or overwrite existing records.

## Questions for Cla
1. Confirm whether Work 01/02/Core/Sandbox already expose equivalents for the four P0 candidates.
2. Confirm the canonical Work manifest schema and validator; distinguish it from Work 21's skill manifest.
3. Identify authorized source evidence and runner for negative tests.
4. Preserve Core authorization, Work 24 as sole PC source bridge, no arbitrary shell, no PC collector and no live service mutation.

## Gate
Work 28 ACTIVE / NOT LOCKED. P0 API duplicate-check PARTIAL/OPEN. Manifest schema NOT VERIFIED. PC :8020 tools/list UNVERIFIED. Tests/E2E NOT RUN. Release NO-GO.
