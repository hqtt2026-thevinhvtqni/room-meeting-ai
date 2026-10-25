# Work 28 Git Sync / CI Evidence Reconciliation — 2026-10-25

**Owner:** Xu (AI-01, GPT CEO / coordination)  
**Work:** 28 — MCP Tooling Platform  
**Branch:** `work/28-mcp-tooling-platform`  
**Status:** ACTIVE / NOT RELEASED

## Verified GitHub CI evidence

- Workflow run: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/40151686990
- Run ID: `40151686990`
- Job ID: `121044353112`
- Tested commit: `9ef3ddb3a349befb16643a807287a44d3684c9a3`
- Environment: GitHub-hosted `ubuntu-latest`, Python 3.12
- Command: `python -m unittest discover -s 05_TEST -v` from `work/28/MCP-8020-TOOLING-PLATFORM`
- Result in job log: `Ran 201 tests in 0.035s`; `OK (skipped=4)`; test step and job conclusion `success`.

## Scope of the result

This is a PASS for the unit/regression suite at the exact commit and scope above. It does **not** prove pytest execution inside Sandbox, nor live end-to-end execution through MCP 8030 → authenticated Core :8000 → authorized Execution Host :8031.

A cleanup warning also appeared after tests: `fatal: No url found for submodule path 'room-meeting-ai' in .gitmodules`. The workflow still concluded success; track the warning separately.

## Runtime execution boundary — still blocked

The current MCP 8030 tool surface available to this session supports Sandbox file operations but does not expose Python/pytest/command execution. Do not mark Sandbox execution PASS and do not bypass the trusted authorization boundary by direct-connecting MCP to Work 13 / Execution Host.

Before enabling a narrow `RUN_TESTS` capability, verify:
1. Canonical deployed Core source/revision and authenticated route.
2. Server-side identity and per-Work `sandbox:pytest` authorization.
3. Canonical Work path and immutable source snapshot/hash.
4. Approved isolated runtime, filesystem/network restrictions, time/resource limits, and process cleanup.
5. Structured stdout/stderr/exit/test summary bound to run ID, Work ID, source hash, and runtime.
6. Positive and negative live E2E through the authorized route, followed by independent review.

## Next action

Continue the integration from source-of-truth discovery and authenticated Core wiring. Keep Work 28 ACTIVE / NOT RELEASED until Sandbox pytest and live E2E have verifiable evidence.
