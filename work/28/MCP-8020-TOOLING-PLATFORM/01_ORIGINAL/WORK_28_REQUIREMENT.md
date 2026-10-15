# WORK 28 — ORIGINAL REQUIREMENT

## Goal
Create a dedicated project to build tools for MCP :8020, enabling AI members to work more effectively through the canonical ROOM-HOP boundary.

## Scope
- Inventory current MCP :8020 tools, contracts, permissions, and known gaps.
- Define a tool registry and typed input/output contracts.
- Provide Work-scoped operations for listing, reading, writing, searching, and validating artifacts where the server authorizes them.
- Define execution-tool interfaces that delegate to the canonical Core/W12/W13 path; do not add an arbitrary-shell bypass.
- Standardize run/task IDs, error/status semantics, audit evidence, and readback verification.
- Add contract, authorization, failure-mode, and E2E tests.
- Document tool onboarding/versioning/deprecation and compatibility.

## Non-goals
- Do not create Core 2 or bypass Core :8000.
- Do not allow AI to access Workspace/database directly.
- Do not duplicate W12/W13 Execution Host, W14 browser/build providers, or W24 PC Source Bridge.
- Do not expose unrestricted shell, host filesystem, credentials, or network access.
- Do not mark unexecuted tests PASS.

## Required flow
AI member -> MCP :8020 -> Core :8000 authorization/application service -> authorized capability (Sandbox / W12-W13 / W24) -> result + evidence -> MCP response.

## Working rule
Keep this Work ACTIVE and unlocked until real acceptance evidence exists. If a capability is not available from this session, record BLOCKED and the precise missing dependency rather than inventing an endpoint or claiming live integration.
