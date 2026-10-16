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


## 6. MASTER EXECUTION BLUEPRINT — E2E AUTO (amendment 2026-10-16 21:18 ICT)

**Purpose:** This file is the persistent, single team-readable execution plan for Work 28. All assigned AI must read this plan, the current journal, the relevant issue, and the current source/evidence before acting. This plan is not proof that any gate has passed. Implementation/test/review results must be recorded separately with evidence.

### 6.1 End-state product behavior
The target product is a bounded autonomous execution loop, not only a tool registry or a dashboard:
1. Receive a task from an authorized source (Inbox/task assignment or an explicitly approved request).
2. Load the Work identity, scope, dependencies, current state, previous decisions, known blockers and acceptance criteria from canonical records.
3. Trace relevant source/runtime/provider paths before deciding or editing.
4. Produce a small execution plan with allowed actions, required approvals, test plan, stop conditions and evidence destinations.
5. Check identity, WorkContext, authorization and capability before each consequential action through Core.
6. Execute via existing MCP :8020 → Core :8000 → authorized capability/runtime; record each action and result.
7. Validate output with tests and observable state; preserve raw logs and immutable revision references.
8. If a bounded, reversible fix is authorized, analyze the failure, make the smallest change, rerun affected tests and regression tests. Never retry indefinitely.
9. Escalate when approval, missing provider, unsafe action, ambiguous ownership, isolation failure, repeated failure or insufficient evidence prevents safe continuation.
10. Have An verify, Ka independently review, and Xu accept or return a specific evidence-linked fix.
11. Produce a handoff with status, commit/revision, tests, evidence links, unresolved risks and next owner.

### 6.2 Inbox, Proposal, Task and wake-up lifecycle
These are separate concepts and must not be conflated:
- **Message:** communication record; it is not automatically a task.
- **Proposal:** a proposed action/decision; it is not authorization until accepted by the correct authority.
- **Task / Inbox item:** an actionable unit with task ID, target AI identity, Work ID, status, scope, acceptance criteria, owner, timestamps and evidence links.
- **Wake-up / dispatch:** mechanism that prompts an AI/runtime to inspect or claim eligible work. A read-inbox tool does not prove wake-up works.
- **Execution record:** actual action/result evidence; it is not implied by an accepted Proposal or a task status change.

Required state transition must be explicit and auditable, for example:
message/proposal → authority decision → task created/updated → task assigned to AI identity → dispatch or AI pull → authorized execution → verification → result message + evidence → closed/blocked.
The team must discover the existing implementation first. Do not create a duplicate Inbox, Proposal service, queue, Core or runtime. If the current canonical source does not evidence a stage, record the exact gap as BLOCKED and propose the smallest compatible change for approval.

Required negative tests include: rejected proposal cannot execute; unapproved privileged action cannot execute; wrong AI identity cannot claim a task; wrong Work cannot read/write it; duplicate dispatch cannot cause duplicate consequential execution; stale/closed task cannot be rerun without a new authorized transition; missing provider/auth fails closed; runtime timeout/resource cap stops execution; result cannot be marked PASS without verifiable evidence.

### 6.3 Source of truth and no-repeat protocol
Before asking Vinh or another AI to repeat information:
1. Read this master plan and current Work 28 journal.
2. Read the relevant issue/comments and the latest linked artifacts.
3. Inspect current branch/source/commit and existing test/evidence records.
4. Compare against recorded decisions and unresolved blockers.
5. Ask only if a genuinely missing decision is required, state exactly what was searched and why the answer changes implementation.
6. Record any new decision once in the journal and update the plan/issue links; do not create competing copies of the same decision.

For each handoff, include: named owner + role, exact task, source paths/revision, constraints, acceptance criteria, required evidence path, dependencies, stop condition, and next owner. Each AI should continue from the latest verified record rather than restart discovery or ask the user for already-recorded context.

### 6.4 Security and authority invariants
- Canonical flow: AI → MCP :8020 → Core :8000 → approved capability/runtime → output/evidence.
- Core is the authorization and canonical state authority. No bypass or duplicate Core/runtime.
- No arbitrary shell/Python execution, identity supplied by untrusted caller, privilege self-escalation, cross-Work access, or unapproved live configuration changes.
- Sandbox and GitHub access are provider-backed and scope-limited; validate path, branch, ownership, payload size and write permissions.
- Human approval is required where policy marks the action as privileged, destructive, external, security-sensitive or release-affecting.
- Bounded retries only; stop and record BLOCKED on unsafe ambiguity, unavailable trusted provider, failed isolation or missing approval.
- Do not touch protected Work 13, PC services or live MCP registry without explicit authorization and a reviewed change plan.
- No merge to main or release until G1–G9 pass and Xu records acceptance.

### 6.5 Required E2E evidence bundle
For each run, store an evidence bundle under Work 28 with:
- run ID, timestamp (ICT), initiating AI identity, task/Work IDs and authorization decision;
- source commit/revision and configuration/provider identity (secrets excluded);
- exact request/tool calls and relevant correlation IDs;
- raw command/test invocation, exit code, stdout/stderr, test counts and skip/fail inventory;
- runtime outcome and bounded resource/time details where available;
- before/after state, readback, relevant hashes and GitHub commit/blob SHA when applicable;
- failure/fix/retry chain, with each attempt identifiable;
- An's test verdict, Ka's independent review, Xu's final decision;
- links from journal and issue, plus explicit residual risks.
Redact secrets and personal data. A summary or screenshot alone is insufficient when raw machine-readable evidence is available.

### 6.6 Work 28 implementation order
1. **Trace (Vi):** identify the actual running MCP :8020 startup entrypoint, provider construction, Core route and current tool baseline. Publish source paths/revisions and blockers.
2. **Integrate (Vi):** register the existing 13-tool adapter set into the existing server only if the trusted wiring is evidenced; preserve pre-existing tools; fail closed if required providers are missing.
3. **Contract/tests (Vi + An):** cover stable tool names, provider wiring, authorization, Work isolation, bounded inputs/resources, Inbox/Proposal lifecycle, duplicate/stale tasks, error paths and regression.
4. **Live registration (An):** capture actual live tools/list, compare expected names and baseline, save raw output and timestamp.
5. **E2E (An):** demonstrate one approved test task traversing MCP → Core → authorized runtime/capability → observable output and readback, tied to a specific commit.
6. **Self-repair (Vi, bounded):** fix only reproducible defects in scope; every fix gets targeted and regression reruns; stop after the configured retry cap or at any authority/security boundary.
7. **Independent review (Ka):** inspect diff, test artifacts, negative tests, runtime evidence, Inbox/Proposal transitions and residual risk.
8. **Acceptance (Xu):** read back all evidence and decide PASS/FAIL/BLOCKED for G1–G9.
9. **Handoff:** update journal and issue with exact status, artifact links, next owner and explicit statement whether release is permitted.

### 6.7 Definition of done
Work 28 is DONE/RELEASE-ELIGIBLE only when all applicable G1–G9 gates pass with inspectable evidence tied to the exact accepted revision; the live MCP registry preserves existing tools and exposes the approved tools; one real E2E run proves the authorized path; security/negative tests pass; Ka review is independent; Xu's acceptance is recorded. Otherwise status remains ACTIVE / NOT RELEASED, with each incomplete gate marked BLOCKED or FAIL and a concrete owner/next action.

### 6.8 Current status at amendment time
This amendment records the plan only. It does not change runtime state and does not certify implementation, Inbox/wake-up behavior, live registration, test execution or E2E. The last known source audit still does not prove actual startup wiring or live tool registration. Vi must resolve that first from repository evidence; An must prove runtime behavior; Ka must review independently.
