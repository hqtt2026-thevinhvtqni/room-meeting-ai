# Acceptance Plan — Work 32

## Phase A — Baseline survey (current)
- [ ] Read governing repository and Work rules.
- [ ] Confirm branch/path conventions and source SHA.
- [ ] Inventory Python, dependencies, tests and existing workflows.
- [ ] Identify safe isolated commands and external-service dependencies.
- [ ] Capture baseline evidence without PC/live-service changes.
- Exit: Vinh reviews and approves survey.

## Phase B — Minimal CI pilot (not authorized yet)
- [ ] Add a narrowly scoped Actions workflow on the Work branch.
- [ ] Install declared Python dependencies without Docker.
- [ ] Run compile/import validation and existing unit tests.
- [ ] Publish test summary/logs without secrets.
- [ ] Verify PR behavior and disclose skipped gates.

## Phase C — Integration/E2E (future approval)
- [ ] Isolated fixtures and cleanup.
- [ ] Prove MCP → Core → runtime contract without bypassing Core.
- [ ] Add E2E only with repeatable prerequisites.

## Phase D — Release readiness (future approval)
Manual approval, rollback plan, secret/permission review and post-release evidence. Deployment is outside initial scope. PASS requires evidence; distinguish FAIL, BLOCKED and NOT RUN.