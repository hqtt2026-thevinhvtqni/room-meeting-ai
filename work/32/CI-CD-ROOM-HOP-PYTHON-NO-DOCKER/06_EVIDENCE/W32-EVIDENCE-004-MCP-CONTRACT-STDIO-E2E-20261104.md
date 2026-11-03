# W32-EVIDENCE-004 — MCP Contract Reconciliation and Stdio E2E

- Document Number: W32-EVIDENCE-004
- Priority: P1
- Author: Ka — CSA / Architecture & Backend Owner (delegated)
- Date-Time: 2026-11-04 (hour/minute not captured; not inferred)
- Status: SOURCE CONTRACT RESOLVED; RUNTIME VALIDATION PENDING

## Evidence
- T8 failed because it expected six MCP tools while the adapter exposed four.
- Git history shows MCP Public Boundary V1 started with three tools in commit `73a454b4a806a47a738ab323b50ce4154a65d6b6`; `add_paste_to_meeting` was added as the fourth tool in commit `d9b0a1a5baea1498a940e8d4652c9e875915c05a`.
- Message v1.0 commit `a799106199976334ef740c80f566f801fb00c667` added T8 expecting six tools, but the Integration client itself describes four locked tools while incorrectly requiring `join_meeting`.
- `API_CONTRACT.md` puts join/start lifecycle actions on Core HTTP routes, not MCP Public V1.

## Changes committed on Work branch
- MCP adapter forwards optional `identity_id` into `MeetingService.add_paste`.
- T8 now asserts the four-tool Public V1 inventory and validates legacy and identified paste transcript metadata.
- Integration client requires only the four locked tools and no longer exposes unsupported MCP `join_meeting`.
- Added `tests/test_ci_mcp_stdio_e2e.py`, which launches the actual MCP stdio subprocess, checks exact tool inventory, list/get, legacy paste, identified paste, and transcript readback.
- Added the stdio E2E test to `.github/workflows/ci.yml`.

## Commit references
- Adapter: `9adce9b54e4c9a9394472c959d1e56cf25911169`
- T8: `b070c59d18f17b0b194caf6b36818aa8a482af53`
- Integration client: `f692dbd0fcc01d4507bb0f57a47745119164abb4`
- Stdio E2E test: `15503d0794d77e6a20d7594e3556c3dd2721f410`
- Workflow: `5309f89984e5ab61d85c22e404babec88ace5995`

## CI status
- Run `41718470071` at final SHA `5309f89984e5ab61d85c22e404babec88ace5995`: QUEUED/PENDING at report creation.
- No validation PASS is claimed for the updated code until the exact SHA run completes.
- Previous run `41718406486` is intermediate SHA and is not accepted as validation of the final changes.

## Branch safety
- Main HEAD observed: `4d2788158b08a48c39abf3d9c74c57314eea3ff4`.
- Work branch compare: 48 ahead / 31 behind; merge base `9e4002cbd93a6b92684b17623d79a1adda161d37`.
- No merge, rebase, cherry-pick, main update, deployment, secrets, or production mutation.
- Overall Work 32: ACTIVE — NOT RELEASED.
