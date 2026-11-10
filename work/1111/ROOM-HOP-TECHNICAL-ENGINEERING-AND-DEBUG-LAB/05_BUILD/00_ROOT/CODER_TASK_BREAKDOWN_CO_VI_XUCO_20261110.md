# W1111 — Three-Coder Execution Plan (Co / Vi / Xuco)

- Date: 2026-11-10 (UTC+7)
- Coordinator / technical integrator: Xu
- Execution team: **Co, Vi, Xuco only**
- Work: 1111 — ROOM-HOP Technical Engineering & Debug Lab
- Parent workstream: W1111-T07 — ROOM-HOP authorization boundary & protected mutation remediation
- Governing decision: W32 DOC-117 — W32 Scoped Execution Boundary
- Current gate: PREPARATION / TASK ALLOCATION; protected execution remains DENIED until the exact task tuple, source revision, environment and authorization are valid.
- Canonical journal: `00_ROOT/DOC-003_NHAT-KY-THI-CONG_WORK-EXECUTION-LOG.md`
- Task board: `05_BUILD/00_ROOT/AI_TASK_BOARD.md`
- Technical tracker: `02_EXTENSION/ROOM_HOP_SECURITY_BOUNDARY_TRACE_AND_REMEDIATION_20261110.md`

## 1. Operating decision

Xu decomposes the shared technical problem into three non-overlapping implementation packages. Only Co, Vi and Xuco are in the active coder roster for this workstream. No additional reviewer, QA agent, architect or other AI is assigned. Xu owns architecture integration, dependency resolution, task acceptance and the final technical decision.

The three packages form one delivery:

1. **Co — Trusted Identity & Authorization Core:** establish the trusted principal and scoped authorization/grant contract.
2. **Xuco — Enforcement Gateway & Sandbox Boundary:** enforce that contract at the real server-side mutation entrypoints and close bypass routes.
3. **Vi — Execution Host & Result Integrity:** enforce the same scoped grant at execution time and guarantee truthful result propagation/evidence.

Do not implement three competing authorization systems. Co owns the canonical contract and policy decision interface; Xuco and Vi consume that interface.

## 2. Task summary

| Task | Owner | Package | Priority | Dependencies | Current state |
|---|---|---|---|---|---|
| W1111-T07-CO | Co | Trusted identity, scoped grant, policy decision and durable audit core | P0 | Xu architecture contract; exact source revision | READY — ACK REQUIRED |
| W1111-T07-XUCO | Xuco | Gateway/MCP/Sandbox enforcement, protected mutation choke point and bypass closure | P0 | Co contract/API; runtime topology trace | READY — ACK REQUIRED |
| W1111-T07-VI | Vi | Execution Host grant validation, isolated execution and result/evidence integrity | P0 | Co grant contract; Xuco boundary contract; Host source/revision | READY — ACK REQUIRED |

No task is IN_PROGRESS until the named coder acknowledges in DOC-003 with exact identity, task ID, starting commit SHA, branch, scope and intended output. Task allocation is not proof of agent availability or runtime access.

## 3. Detailed task — W1111-T07-CO

**Owner:** Co  
**Role:** Coder — trusted identity and authorization core  
**Priority:** P0  
**Primary outcome:** one reusable, fail-closed authorization contract that downstream enforcement points can call.

### Scope
1. Trace existing identity/authentication, member registry, agent profile, Work manifest, Assignment/Task and grant code. Compare the relevant W01/W02/W28/W99/W32 implementations; identify canonical candidates and duplicates.
2. Define a typed authorization context containing:
   - trusted authenticated principal and authentication provenance;
   - Work ID and canonical manifest/state revision;
   - exact active Assignment and Task, owner, ACK, status and revocation;
   - repository, ref/branch, exact commit SHA and normalized resource/path;
   - explicit action allowlist;
   - named execution environment;
   - issued-at, expiry, policy version, gate snapshot, correlation/idempotency ID.
3. Define one policy decision interface with explicit ALLOW/DENY and machine-readable reason codes. Missing, stale, mismatched or unverifiable fields must DENY.
4. Implement short-lived, unforgeable/scoped grants or capabilities; store only verifiable token digests where appropriate; support expiry and revocation.
5. Persist authorization decisions and audit events durably. Audit persistence failure must fail closed for protected effects.
6. Add schema validation and focused tests for missing principal, invalid assignment, wrong Work, wrong path/action, stale SHA, expiry, revocation and audit-store failure.
7. Document the stable API and migration adapter for Xuco and Vi. Avoid breaking existing callers silently.

### Explicit non-scope
- Do not mount middleware or edit Gateway/MCP/Sandbox handlers; Xuco owns that.
- Do not edit Execution Host process/runner code; Vi owns that.
- Do not create a second policy engine or treat a client-supplied identity header/YAML name as authentication.
- Do not weaken DOC-117 to make existing flows pass.

### Deliverables
- Scoped branch and PR (after exact base SHA and authorization are recorded).
- Authorization context/schema and decision API.
- Grant issue/validate/revoke implementation.
- Durable audit implementation and failure behavior.
- Unit/contract tests and raw test output.
- Integration contract consumed by Xuco and Vi.
- DOC-003 journal entry with files, methods, exact SHA, tests and unresolved risks.

### Acceptance criteria
- Same valid tuple produces deterministic ALLOW; every required negative case produces DENY.
- No client-controlled field can elevate principal or scope.
- Grant cannot be replayed for another Work, Task, path, action, commit or environment.
- Expiry/revocation take effect on subsequent validation.
- Audit persistence failure prevents protected action.
- Contract tests are consumable by Xuco and Vi; no mock-only claim is represented as runtime PASS.

## 4. Detailed task — W1111-T07-XUCO

**Owner:** Xuco  
**Role:** Coder — Gateway/MCP/Sandbox enforcement  
**Priority:** P0  
**Primary outcome:** every protected mutation request passes through one trusted, server-side enforcement choke point; no direct route bypasses it.

### Scope
1. Trace the actual request path from external/client entry through proxy, Gateway :8040, MCP :8030 and SandboxService to every mutation handler. Record all direct/internal routes and alternate entrypoints.
2. Identify the actual deployed route and module entrypoint separately from source prototypes. If runtime topology cannot be observed, report BLOCKED with the exact missing evidence; do not infer deployment from source.
3. Integrate Co's trusted authorization decision API at the lowest common server-side mutation boundary and at any separately reachable protected route.
4. Enforce explicit action mapping for read/create-draft/write-assigned-file/append/delete/execute/CI-dispatch; default unknown actions to DENY.
5. Normalize and validate repository-relative paths. Reject traversal, symlink escape, wildcard expansion and path alias bypass.
6. Strip or ignore caller-supplied identity/authority headers. Principal must arrive only through the trusted authentication adapter/context.
7. Revalidate the grant and exact source/resource immediately before mutation/commit. Do not rely on an earlier route-level check alone.
8. Ensure every allowed/denied protected mutation emits a durable audit event through Co's interface. Audit failure must stop the mutation.
9. Add route-level tests for direct MCP calls, Gateway calls, internal service calls, bypass attempts, path traversal, stale grant, revoked grant and audit failure.

### Explicit non-scope
- Do not implement an independent identity registry, grant issuer or second policy engine; Co owns it.
- Do not change Execution Host execution semantics; Vi owns them.
- Do not expose a new permissive generic Sandbox write API.
- Do not claim all routes are protected until the complete mutation call-site inventory and tests prove it.

### Deliverables
- Route/topology and mutation-call-site map with exact source references.
- Scoped branch and PR after authorization.
- Gateway/MCP/Sandbox enforcement adapter using Co's API.
- Bypass closure and route-level regression tests.
- Test evidence for positive and negative paths.
- DOC-003 journal entry and handoff contract for Vi.

### Acceptance criteria
- All enumerated protected mutation routes invoke the same server-side policy contract.
- No reachable alternate path can mutate protected resources without authorization.
- Caller-supplied identity headers cannot change the authenticated principal.
- Wrong Work/Task/path/action/SHA/environment, expired/revoked grant and malformed path are denied.
- Audit-store failure prevents mutation.
- Source-level tests pass; live route PASS is withheld until exact deployed runtime is identified and tested.

## 5. Detailed task — W1111-T07-VI

**Owner:** Vi  
**Role:** Coder — Execution Host and result integrity  
**Priority:** P0  
**Primary outcome:** Execution Host :8031 runs only an explicitly authorized, scoped task and reports the true outcome without false aggregate PASS.

### Scope
1. Trace Execution Host :8031 startup, process entrypoint, request schema, command dispatch, workspace selection, subprocess lifecycle, timeout/cancel handling, result aggregation and evidence persistence.
2. Consume Co's grant validation contract; require the exact Work/Assignment/Task, repository/ref/SHA, allowed command/test and named isolated environment.
3. Bind execution to a dedicated workspace and exact checkout revision. Reject arbitrary shell/command, path escape, cross-Work workspace and unapproved environment.
4. Revalidate authorization immediately before process start and before any protected write/commit/effect.
5. Correct nested test/result aggregation so any child failure, timeout, cancellation, missing result or malformed output cannot be converted into aggregate PASS.
6. Preserve exit code, stdout/stderr, per-step status, timeout/cancel state, artifact paths and source revision. No success default when evidence is missing.
7. Persist execution evidence with task ID, grant/correlation ID, environment identity, command/test allowlist, start/end time and exact commit SHA.
8. Add tests for valid named test, wrong grant, wrong SHA, wrong Work, command not allowlisted, path escape, timeout, child failure, missing child result, malformed result and evidence persistence failure.

### Explicit non-scope
- Do not implement identity/grant issuance; Co owns it.
- Do not implement Gateway/MCP/Sandbox route authorization; Xuco owns it.
- Do not enable general-purpose remote shell or arbitrary code execution.
- Do not claim live :8031 is verified without deployed build/process attestation.

### Deliverables
- Execution Host source/runtime path map and contract gaps.
- Scoped branch and PR after authorization.
- Grant-validation integration and named-command execution guard.
- Correct result propagation and evidence schema.
- Unit/contract/integration tests with raw outputs.
- DOC-003 journal entry with exact source SHA, environment, commands and test outcomes.

### Acceptance criteria
- No execution without valid grant, matching task and exact source SHA.
- Only explicitly named commands/tests run in the authorized isolated environment.
- Any child failure/timeout/cancel/missing or malformed result => non-PASS aggregate status.
- Evidence is durable and bound to the exact task/grant/SHA/environment.
- Evidence persistence failure prevents a false success response.
- Live runtime status remains NOT VERIFIED until attested and tested.

## 6. Shared integration contract and dependency order

1. Xu publishes the architecture contract and exact action semantics; Co implements the canonical API.
2. Xuco and Vi consume Co's contract. They must not fork or reinterpret the authorization schema.
3. Co publishes versioned schema/API and contract tests.
4. Xuco integrates at all mutation choke points and reports the route coverage matrix.
5. Vi integrates at Execution Host and reports the command/result/evidence matrix.
6. Xu performs cross-package review, checks no duplicate policy logic exists, and reconciles all test/evidence results.
7. Only after source review and exact revision mapping may the authorized live verification plan be executed.

## 7. Shared coding rules

- Start with DOC-001, DOC-004, DOC-005, DOC-006, DOC-007, this plan, the security tracker and the latest DOC-003 entries.
- Each coder claims only their task in DOC-003. Record exact AI identity, branch, base commit SHA, task scope, intended files and deliverables.
- One task = one scoped branch = one PR. Never push application/security source directly to main.
- No overlapping ownership: Co owns authorization core; Xuco owns Gateway/MCP/Sandbox enforcement; Vi owns Execution Host and result integrity.
- Do not change another coder's files without Xu reassigning the task and recording the handoff.
- Every test record includes timestamp (UTC+7), command/method, environment, repository/ref/commit SHA, raw output/artifact, PASS/FAIL/BLOCKED/NOT RUN and next step.
- No fabricated ACK, test result, runtime attestation or PASS.
- If blocked, record: problem / attempts and evidence / bottleneck / options / exact missing condition.
- Keep the work focused on the three packages. Do not open additional AI workstreams.

## 8. Authorization and release boundary

This plan allocates work; it does not itself authorize protected execution. Until the exact assignment, source SHA, target resource, action, environment and grant are approved under DOC-117:

- READ / TRACE / ANALYZE / DESIGN may proceed within the available access.
- Code mutation to protected security/runtime components, CI dispatch, PC/runner execution, merge, deployment and release remain DENIED.
- A coder must not bypass the gate by writing through generic MCP file tools or by self-asserting identity.
- Xu must record a separate READY / EXECUTION_AUTHORIZED decision bound to the exact tuple before protected effects.
- Vinh remains the final authority for the security policy and release approval.

## 9. Definition of done for W1111-T07

- Co, Xuco and Vi deliver their separate PRs and complete journal/evidence entries.
- Xu verifies all three consume one authorization contract and have no conflicting ownership.
- All positive and negative tests pass on the exact candidate commit.
- Actual Gateway/MCP/Sandbox/Execution Host runtime paths are attested and tested; source-only checks are not called runtime PASS.
- Durable audit and evidence readback succeeds.
- No bypass path remains in the enumerated protected surface.
- Final state is recorded as PASS, FAIL or BLOCKED with exact residual risks; never infer release from merged code alone.


## End-to-end task ownership addendum — D70-022 (2026-11-10)
After the named coder has acknowledged the exact task and the required scoped authorization is valid, the coder owns the complete package through implementation, focused tests, in-scope defect repair/retry, evidence capture, journal update and handoff. The coder must not stop after a single code change or ask for step-by-step instructions when the remaining steps are defined by the acceptance criteria. Xu coordinates dependencies and integrates the three packages; routine progress is recorded in DOC-003, not repeatedly sent as chat updates. Notify Xu only for material milestone, final handoff or a genuine blocker. Initial ACK and DOC-117 authorization requirements are unchanged; this addendum does not authorize protected source mutation by itself.
