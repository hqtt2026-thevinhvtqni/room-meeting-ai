# Xu Plan — Work 28 team execution
- **Plan timestamp:** 2026-10-16 20:13 ICT (UTC+07:00)
- **Plan owner:** Xu — Plan / Planner, Chief Strategy Architect (CSA)
- **Decision authority:** Vinh — Work Owner / Decision Authority
- **Team flow:** Xu Plan → Vi Coder → An Tester → Ka Review
- **Repository:** `hqtt2026-thevinhvtqni/room-meeting-ai`
- **Branch:** `work/28-mcp-tooling-platform`
- **Status at plan time:** Work 28 ACTIVE / NOT RELEASED; live registration and full E2E BLOCKED / NOT PROVEN.

## 1. Source-trace baseline
Xu read from the Work 28 branch:
- `04_CODE/runtime_tools_v1.py` — SHA `5bba7ffc83ad9f28a9a2e64566f713b56c09b0df`
- `04_CODE/sandbox_tools_v1.py` — SHA `6682a4812b199dc1d1384d5eee28866c9b7ba459`
- `04_CODE/github_tools_v1.py` — SHA `c0a29e4a9f27144ed31e59bf4c535bad88506861`
- `04_CODE/mcp_tool_registration_v1.py` — SHA `6fa703050c23402cc9961be0a04234f20bf4ef01`
- `05_TEST/test_mcp_tool_registration_v1.py` — SHA `d73b99932cda5b9813a91909d54c65fd9398db34`
- `.github/workflows/work28-mcp-tooling.yml` — Python 3.12 unit-test workflow.

Finding: a helper registers 13 named tools on an injected MCP object, but this source trace alone does not prove the helper is called by the actual MCP :8020 startup or that those tools appear in the live registry. A FakeMCP unit test is not live registration evidence. Xu must not guess startup/provider wiring.

## 2. Execution lanes and ordered handoffs

### Lane 0 — Xu Plan / Planner (current)
1. Keep the team-role amendment and issue links in the Work 28 minute/journal.
2. Establish exact current source entrypoint for the existing MCP :8020 and trace its imports/startup, trusted provider construction, Core route and configuration using repository evidence.
3. Define the integration patch and testable acceptance gates. No duplicate server/runtime; Core remains authorization authority.
4. Handoff a written plan to Vi with exact source files, contracts, constraints and expected evidence.

### Lane 1 — Vi Coder / Implementer
1. Trace and report the exact existing MCP startup entrypoint and trusted provider bindings. If not present in branch or not authorized, stop and record the precise missing dependency; do not invent it.
2. Integrate the existing adapters into that MCP instance only, using trusted Core/Sandbox/GitHub providers and existing dependency injection.
3. Preserve all existing tools. Avoid arbitrary shell/Python, caller-supplied identity, Core bypass, duplicate services and writes to protected Work 13/PC/live registry.
4. Add/update focused tests for startup registration, all 13 stable tool names, provider-missing fail-closed behavior, authorization boundaries and regressions.
5. Commit only to the Work 28 branch; record commit SHA, files changed, test command and known blockers in Work 28.

### Lane 2 — An Tester / Verification
1. Read Vi's commit and test plan before execution.
2. Run the authorized Python 3.12 unit/regression suite and any approved integration tests.
3. Obtain raw live MCP :8020 `tools/list` from an authorized probe; compare exact names to contract and existing-tool baseline.
4. Run authorized end-to-end checks: MCP request → Core authorization/WorkContext → approved capability/runtime → bounded output/evidence/readback.
5. Save command, timestamp, revision, exit code, stdout/stderr, test inventory, pass/fail/skip, log location/SHA-256 and readback. If a runner or live probe is unavailable, record the exact error and mark BLOCKED / NOT PROVEN.

### Lane 3 — Ka Review / Independent Reviewer
1. Review Vi's diff and An's report against registry, tool contracts, test plan and security constraints.
2. Independently verify tool registration and E2E evidence; distinguish helper/unit tests from live behavior.
3. Record per-gate PASS/FAIL/BLOCKED, evidence links and residual risk. Do not accept a claim without an inspectable artifact.

### Lane 4 — Xu final acceptance / handoff
1. Read back the commit, test report, live tool snapshot, logs/hash and Ka review from Work 28.
2. Resolve contradictions or send a specific fix/retest task back through Work 28 records.
3. Approve only if all required gates pass; otherwise maintain BLOCKED / NOT PROVEN.
4. Do not merge to `main` or release until acceptance is recorded.

## 3. Acceptance gates
- **G1 Source/startup:** exact existing MCP :8020 startup entrypoint and provider construction traced; no duplicate service.
- **G2 Registration:** all 13 expected tools appear in the actual live `tools/list`; existing tools preserved.
- **G3 Core security:** trusted principal/WorkContext, Core authorization, ownership checks, timeout/resource bounds and fail-closed behavior proven.
- **G4 Sandbox:** Work isolation, relative path validation, payload bounds, write policy and readback/hash proven.
- **G5 GitHub:** authenticated provider; read/search/branch/write behavior; protected default branch; expected blob SHA; commit SHA and readback.
- **G6 Tests:** test suite tied to exact commit with exit code, full inventory and logs.
- **G7 E2E:** real authorized request traverses MCP → Core → capability/runtime and returns verified output/evidence.
- **G8 Review:** Ka records independent decision and residual risks.
- **G9 Handoff:** Xu records final acceptance and state.

## 4. Current blockers and honest status
- Xu has not independently re-probed live MCP :8020 in this plan.
- Co's earlier HTTP 200 and Sandbox readback remain reported, not independently reproduced here.
- `runtime_run_tests` and `github_read_file` were reported absent from the live tool list; this needs a fresh raw snapshot.
- Current source trace does not identify/verify the actual startup wiring; Vi must resolve that from evidence.
- No new test run or full E2E PASS is claimed by this plan.

## 5. Team records
- Vi Coder: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/issues/12
- Ka Review: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/issues/13
- Xu Plan / acceptance: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/issues/14
- An Tester: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/issues/15
- Team minute: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/blob/work/28-mcp-tooling-platform/work/28/MCP-8020-TOOLING-PLATFORM/06_EVIDENCE/BIEN_BAN_THONG_NHAT_KHONG_THI_CONG_QUA_CHAT_20261016_2007ICT.md
- Journal: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/blob/work/28-mcp-tooling-platform/work/28/MCP-8020-TOOLING-PLATFORM/06_EVIDENCE/NHAT_KY_THI_CONG.md

**Decision:** Execute only through Work 28 records using Xu Plan → Vi Coder → An Tester → Ka Review. Work 28 remains ACTIVE / NOT RELEASED until the acceptance gates have evidence.
