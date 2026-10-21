# WORK 28 — CONTINUATION PLAN: MCP-8020-TOOLING-PLATFORM
Version: 1.0
Date: 2026-10-22
Status: ACTIVE
Authority: Vinh
Coordinator: Xu
Execution model: Coder implements; Tester independently verifies; Xu coordinates and reports.
Branch: work/28-mcp-tooling-platform
Scope: Complete and integrate Work 28 tooling incrementally. Do not wait for Work 28 closure.

## 1. Objective

Reconcile the v54 catalog (54 designed tools) with the tools actually registered and callable on MCP :8030; integrate only real implementations; test each change with observable evidence. Keep MCP :8020 available to existing AI clients until migration to :8030 is explicitly verified and approved.

## 2. Verified baseline versus claims

Evidence supplied in the handoff/context:
- MCP :8030 sandbox_read smoke test: PASS, 17 tools reported by the user's current test.
- Work 28 v54 handoff dated 2026-10-21 documents a 54-tool catalog, RoomProvider (10 tools), SandboxProvider (14 file-operation tools), V54Service validation, ExecutionGateway protocol semantics, and tests.
- The v54 handoff explicitly marks live registration, 7 execution tools, 6 computer tools, 17 browser/OCR tools, and contract-version unification as incomplete or blocked by dependencies.

Important distinction: 54 is the catalog design count, not proof that 54 tools are registered or functional on :8030. The observed 17-tool result must be re-collected with raw tools/list output and names/schemas before it is treated as the current runtime inventory.

## 3. Non-negotiable boundaries

1. Preserve MCP :8020 and its current consumers; do not shut it down during this work.
2. Develop MCP :8030 at the already-established endpoint: https://admin-pc.tail7d6101.ts.net/build/mcp. Do not invent or silently change endpoint paths.
3. Preserve the working sandbox_read() implementation and its behavior. Do not re-open already-passed sandbox_read testing unless new evidence shows a regression.
4. No fake handlers, placeholder PASS responses, mock data represented as live Core data, or catalog status promotion without implementation and evidence.
5. Sandbox is a separate execution environment. Never install, run, or copy Core :8000 into Sandbox. Do not bypass Core for execution.
6. Enforce Sandbox root containment, symlink rejection, work isolation, fail-closed authorization, and append-only evidence rules already defined by Work 28.
7. Keep this plan within Work 28. Do not expand into unrelated Works or redesign the architecture.
8. Report DONE / PASS / DECISION / BLOCKED distinctly. A unit test using a mock proves only the tested contract semantics, not live integration.

## 4. Work packages and order

### WP0 — Inventory and baseline (Coder + Tester)
- Capture exact :8030 process/launch configuration and endpoint.
- Call MCP tools/list and save raw response, tool count, exact names, input schemas, and timestamp.
- Map each runtime tool to v54 catalog entry, provider/handler, and status.
- Compare the 17-tool test result with tools/list; investigate only discrepancies that block accurate inventory.
- Do not modify runtime behavior in this package.

Acceptance: inventory artifact is reproducible and every runtime tool is classified as catalog match, legacy/non-catalog, duplicate, or unexplained. No count-only report.

### WP1 — Integrate already-implemented ROOM and Sandbox/file tools
- Inspect existing providers and server adapter before editing.
- Register only handlers that are implemented and satisfy their schemas.
- ROOM tools must use the approved real Core/service path when their semantics require live ROOM data. In-memory RoomProvider state must be labelled as such and must not be presented as live Core state.
- Sandbox/file tools must use the existing SandboxService/provider and preserve containment and authorization protections.
- Keep sandbox_read() unchanged unless a demonstrated integration conflict requires a minimal reviewed fix.
- Do not promote execution, computer, browser, or OCR tools to IMPLEMENTED merely to increase the count.

Acceptance: tool names and schemas match catalog; each newly registered tool has a successful safe invocation and a negative/invalid-input test; runtime tools/list and smoke tests pass.

### WP2 — Core and execution dependency gate
- Inspect the authenticated Core :8000 route and the approved W12/W13 runtime contracts as dependencies; do not modify Core inside Sandbox.
- Keep BlockedExecutionClient as the default until live route, authenticated identity handling, canonical runtime, and OS isolation evidence are available.
- Only after the dependency gate passes, implement CoreExecutionClient for submit, get_status, get_result, cancel, collect_artifact, generate_evidence, and create_handoff.
- Route execution through Core and the approved runtime only. Never wire MCP directly to execution_host/server.py; do not create a parallel execution host.
- Cross-work reads must remain indistinguishable NOT_FOUND.
- Update catalog statuses only after implementation and CI evidence.

Acceptance: authenticated live integration tests prove each method's behavior and failure modes; no mock-only evidence is accepted as live PASS.

### WP3 — Computer / Browser / OCR dependencies
- Treat the six computer tools and seventeen browser/OCR tools as BLOCKED until the relevant approved Work 14 runtimes and provider contracts are available.
- Review the published schemas and runtime interfaces; implement provider adapters only against approved interfaces.
- Do not create fake browser actions, screenshots, OCR output, or computer-use success responses.
- Enable tool registration/status only when provider implementation and safe live tests exist.

Acceptance: each enabled tool has a real provider, schema validation, safe success test, negative/failure test, and captured evidence. Unavailable dependencies remain explicitly BLOCKED.

### WP4 — Contract version and catalog consistency
- Record the observed CONTRACT_VERSION values (handoff notes 1.0.0 versus 1.3.0 elsewhere) and identify their authoritative source.
- Do not choose or unify a version silently. Xu requests/records the architecture decision; after approval, update the single source of truth and tests together.
- Ensure catalog status, provider registration, schema, and implementation cannot drift unnoticed.

Acceptance: one approved contract version, tests assert it, and the evidence records the decision and changed files.

### WP5 — Verification, evidence, handoff
- Run focused unit/contract tests first, then the relevant integration/smoke suite.
- Test tools/list, schema parity, safe valid calls, invalid inputs, permission boundaries, file containment, and failure envelopes.
- Record command, environment, timestamp, exit code, test counts, relevant output, commit SHA, and CI URL when available.
- Tester reviews independently and reports PASS/FAIL/BLOCKED per acceptance criterion.
- Xu produces a concise handoff and keeps the Work ACTIVE while blocked packages continue in parallel where dependencies permit.

## 5. Role contracts

### Coder
- Read the current branch and handoff before edits; trace call paths before changing code.
- Work in small, reviewable changes on work/28-mcp-tooling-platform.
- Do not edit the running PC process from a remote session unless a supported, authorized path exists. Provide exact local commands when PC-side verification is required.
- Do not claim runtime integration from source changes alone.
- Provide changed-file list, rationale, tests run, outputs, commit SHA, and remaining blockers.

### Tester
- Independently compare catalog, registration, schemas, and handlers.
- Reproduce tests rather than relying on Coder's assertion.
- Distinguish unit/mock tests from live :8030 and live Core/runtime tests.
- Fail closed on missing evidence, fake providers, unexpected tool exposure, permission leaks, or regression to sandbox_read().
- Do not change implementation while reporting test findings unless explicitly assigned a separate fix task.

### Xu — coordinator
- Maintain scope and dependency gates; assign work packages in order.
- Resolve decisions only within delegated authority; escalate architecture decisions that require Vinh's approval.
- Never report PASS without evidence and never imply that GitHub changes altered the PC's running process.

## 6. Required evidence artifacts

Store new artifacts under:
work/28/MCP-8020-TOOLING-PLATFORM/06_EVIDENCE/

Recommended files:
- MCP8030_TOOLS_LIST_BASELINE_20261022.md (actual runtime inventory and raw output reference)
- WORK28_TOOL_CATALOG_PARITY_20261022.md (catalog-to-runtime matrix)
- WORK28_WP1_INTEGRATION_TESTS_20261022.md (test commands, results, evidence)
- WORK28_BLOCKERS_AND_DECISIONS.md (append/update decision and dependency record)
- WORK28_HANDOFF_CONTINUATION_20261022.md (final scope status)

Do not fabricate evidence files containing results that have not been collected. If an artifact cannot be collected remotely, document the exact local command and mark it BLOCKED pending the actual output.

## 7. Overall acceptance and migration gate

Work 28 remains ACTIVE until the enabled-tool inventory, schema/handler parity, safety boundaries, tests, and evidence are reviewed. The 54-tool catalog count alone is not an acceptance criterion.

MCP :8020 may be retired only after all of the following are evidenced and Vinh explicitly approves:
- target AI clients successfully connect to :8030;
- required tools are present with correct schemas and real handlers;
- end-to-end paths through MCP → Core → approved runtime succeed where applicable;
- regression/security tests pass;
- rollback path is documented and verified.

Until then, :8020 remains available.

## 8. Immediate next actions

1. Tester: capture the actual :8030 tools/list names and schemas; compare with the reported 17-tool smoke test.
2. Coder: perform read-only source trace of the :8030 server registration and identify which existing ROOM and Sandbox/file providers can be safely registered now.
3. Coder: implement the smallest WP1 integration increment, preserving sandbox_read().
4. Tester: independently run focused tests and provide exact evidence; mark any PC-side/live-Core checks BLOCKED if output is unavailable.
5. Xu: review the evidence and issue the next bounded work order without waiting for Work 28 closure.

## 9. Initial status

- WP0 runtime inventory: BLOCKED until actual :8030 tools/list output is captured.
- WP1 existing provider integration: READY FOR SOURCE TRACE; runtime PASS not yet established.
- WP2 live execution integration: BLOCKED by authenticated Core/runtime/isolation evidence.
- WP3 computer/browser/OCR: BLOCKED by approved Work 14 runtime/provider dependencies.
- WP4 contract version unification: BLOCKED pending decision on source of truth.
- WP5 final verification: IN PROGRESS as incremental work proceeds.
