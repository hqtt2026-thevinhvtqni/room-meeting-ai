# Xu — Work 28 Sandbox pytest execution-path diagnostic
**Date:** 2026-10-25 (UTC+7)
**Identity:** Xu — AI-01 GPT CEO / Quân sư LAB
**Scope:** Verify MCP 8030 connectivity and determine whether this session can execute Python/pytest inside the Work Sandbox.

## Results
1. **MCP 8030 connectivity: PASS (file-operation surface only).** `sandbox_list_works` returned status=ok and 53 Works; `sandbox_list(work_id='28')` returned status=ok and Work 28 contents; `sandbox_read_probe` read Work 28 test plans successfully.
2. **Work 28 test plan readback: PASS.** `MCP-8020-TOOLING-PLATFORM/05_TEST/WORK_28_TEST_PLAN.md` specifies the canonical local contract command `python -m unittest discover -s 05_TEST -t . -v`. It explicitly says this has not been run by an approved runner in this session. The plan's G3-G6 execution/security/E2E gates remain blocked.
3. **Command/pytest execution via current MCP 8030 surface: BLOCKED.** The live tool inventory exposed 17 tools; available Sandbox operations are read/list/create/write/append/delete and context/meeting operations. There is no `sandbox_run_command`, Python execution, or pytest-run tool exposed to this session. Therefore I cannot truthfully execute pytest inside the Sandbox through this connection.
4. **No execution attempted by substituting another environment.** No tests were run in this session, and no PASS is claimed for Python/pytest, runtime, or E2E. Do not treat Sandbox file readback or historical `__pycache__` files as test evidence.

## Decision
- MCP 8030 file access is restored and verified.
- The specific blocker is the missing authorized command/test execution capability in the current exposed MCP tool surface, not a demonstrated pytest failure.
- Do not bypass the approved execution architecture by invoking an unrelated runner or direct unauthenticated W13 endpoint.
- Required next step: expose/use the approved authenticated RUN_TESTS route through Core -> canonical W12/W13 runtime, with server-derived Work authorization, immutable source/hash binding, bounded timeout/process cleanup, and captured output/evidence. Then run the canonical Work 28 test command with exit code and discovered-test count recorded.

**Status:** MCP file access PASS; pytest execution path BLOCKED / NOT RUN; Work 28 remains ACTIVE / BLOCKED / NOT RELEASED.