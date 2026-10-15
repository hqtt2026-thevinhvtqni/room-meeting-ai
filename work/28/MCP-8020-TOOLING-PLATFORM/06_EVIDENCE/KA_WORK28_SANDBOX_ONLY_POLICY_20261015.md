# KA — WORK 28 SANDBOX-ONLY EXECUTION POLICY
Date: 2026-10-15
Authority: Vinh
Status: ACTIVE

## Binding rule
All Work 28 implementation, source files, tests, evidence, decisions, minutes, and work journal updates must be written directly into Sandbox Work 28 through the authorized Room Hop MCP tools.

## PC boundary
- Do not use the PC repository as a development workspace.
- Do not modify PC source, install the collector, run the collector, create a source ZIP on PC, restart services, or alter the live MCP registry as part of this Work 28 build.
- PC is not the destination for in-progress artifacts.
- Any future transfer from Work 28 back to PC is permitted only after independent review, E2E-Automatic evidence, and Vinh's explicit approval.

## Source-intake boundary
The canonical PC source tree is not currently available as file contents through the exposed MCP tools. get_room_structure gives paths, not source bytes. Sandbox text-file write is not a directory/archive import mechanism.
Therefore:
1. Do not fabricate a second implementation to replace missing canonical source.
2. Continue only with source-independent contracts, test plans, audit specs, and evidence records that can be honestly created in Work 28.
3. Keep canonical-source-dependent implementation and end-to-end integration BLOCKED until a supported, authorized read-only transfer/import route is available.
4. If Nu proposes a route, review its actual capability and security boundary first; do not execute PC-side collection by assumption.
5. Verify every Sandbox write by reading the exact file back. Record persistence/readback only; do not claim test PASS unless tests actually ran.

## Current status
- Sandbox-only policy: recorded here.
- Source tree imported into Work 28: NO / BLOCKED.
- PC collector: draft exists as a Work 28 artifact only; NOT approved, NOT installed, NOT executed.
- E2E-Automatic against canonical live implementation: BLOCKED pending source intake and authorized runner.
- Release: NO-GO.

This policy supersedes any ambiguous interpretation that Work 28 work should be carried out on the PC.
