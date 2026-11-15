# DOC-066 — WP1 OWNER-CONTRACT TRACE AND LIFECYCLE ALIGNMENT

- Work: 102 — AI-AGENT-LOOP-PRODUCTION-READINESS
- Date: 2026-11-15 (UTC+07:00)
- Prepared by: Vi | CODER
- Governing architecture: DOC-012
- Related plan: DOC-013 WP1
- Related mapping: DOC-065
- Status: TRACE UPDATED / DESIGN ONLY / WP1 BLOCKED / NOT APPROVED

## 1. Purpose and boundary

This record advances WP1 by reconciling the W51/W52/W102 contract mapping against the currently read W70 lifecycle standards, W112 cross-Work design baseline, and component-owner evidence workspaces W37/W38/W39/W14.

This is a documentation and read-only source-trace action. It does not authorize source/runtime changes, Core or Host writes, new endpoints, task-store creation, dispatch, test execution, merge, deployment or release.

## 2. Additional sources read in this pass

| Source | Observed fact | Evidence class / limitation |
|---|---|---|
| W70 DOC-005 v1.2 — Work State Machine | Defines Work, phase, gate and WP lifecycle; requires server-side identity/permission, expected state/version, evidence, idempotency and fail-closed transitions. Dashboard/adapters cannot write authoritative state. | Owner standard read from Sandbox; does not prove live Core implementation. |
| W70 DOC-042 v1.0 + addenda | Defines end-to-end orchestration, assignment contract, evidence requirements, separate issue/source-map/Work Entry/assignment/acceptance states, and three-stage preparation/authorization/acceptance readiness. | Owner standard read from Sandbox; does not prove API enforcement. |
| W70 DOC-043 v1.0 + addenda | Role declaration is not authentication; identity, capability, permission, ACK and reviewer independence must be verified for each participation. | Governance standard; no live identity endpoint attested in this pass. |
| W70 DOC-044 v1.0 + addenda | Assignment must bind task/WP, source revision, permission, deliverables, acceptance, evidence, G0–G5 and explicit execution authorization. | Template/standard; no W102 assignment authorization granted by this read. |
| W112 DOC-001 v1.0 + v1.1 draft | W70 owns its lifecycle records; W52 owns A2A orchestration; W14 owns Host; W37/38/39 are investigation workspaces; W112 owns cross-Work definitions only. Runtime API, event transport, evidence store, leases and auth enforcement remain NOT VERIFIED. | DRAFT / NOT APPROVED FOR RUNTIME ENFORCEMENT. |
| W37 Core scope + mirror rule | W37 is an evidence/documentation workspace, not a second Core. Core routes, DTOs, transactions, persistence and auth are explicitly still to be verified. | Sandbox owner documentation; not live Core attestation. |
| W38 requirements + mirror role | W38 is an isolated investigation workspace for :8040; process, routes, auth, downstream path and health must be established from evidence. | Sandbox owner documentation; live Gateway remains NOT VERIFIED. |
| W39 mirror role | W39 is an isolated investigation workspace for :8030; tool inventory and live behavior need authorized evidence. | Sandbox owner documentation; does not prove dispatch or Core authority. |
| W14 restoration addendum 2 | W14 is the execution-host owner; historical 2026-10-12 PC attestation is not current full E2E/security/release proof. | Historical evidence; current HostPort open/stop/cancel contract not verified here. |

## 3. Lifecycle alignment — no state-machine flattening

The normalized model must preserve these distinct layers:

1. **Work/WP lifecycle:** apply the W70 governance semantics and the Work's approved lifecycle records. A WP being READY or DONE is not a runtime API claim.
2. **Assignment lifecycle:** DRAFT / READY / IN_PROGRESS / IN_REVIEW / BLOCKED / DONE / CANCELLED, with G0–G5, explicit bounded authorization, attributable recipient ACK and read-back as required by W70.
3. **W52 A2A transport/task lifecycle:** retain as a provider-neutral design candidate only until W52 owner approval and a real transport/consumer contract are verified. It must not silently become the Core task state.
4. **W102 Agent Loop execution state:** READY / RUNNING / SUCCEEDED / FAILED / BLOCKED / CANCELLED / BUDGET_EXHAUSTED remains a local execution-policy vocabulary. It must not overwrite authoritative Work/assignment state.
5. **Acceptance verdict:** PASS / FAIL / BLOCKED / NOT_RUN is independent of task state and execution status, and must bind to an immutable candidate hash plus independent tester/reviewer evidence.
6. **Host process state:** timeout or cancellation request is not cancellation confirmation. W14 must confirm descendant-process stop before any authoritative CANCELLED outcome is asserted.

No implicit conversion is permitted between these dimensions. Any future adapter mapping must be explicit, versioned, reversible and tested for lossy/ambiguous values.

## 4. Contract ownership and normalized treatment

| Contract concern | W51 / W52 / W102 candidate | Owner-aligned treatment | Current disposition |
|---|---|---|---|
| Canonical Work/WP/gate state | W52 task state; W102 RunStatus | Consume the Work's approved lifecycle authority; W70 standards define governance semantics. Do not create a parallel state store. | Semantics documented; live persistence/API NOT VERIFIED. |
| Assignment / recipient ACK | W52 requested_by / assigned_agent / ACK proposals | Identity and permission must be server-derived; assignment and ACK must be attributable to exact identity + assignment + source revision. | W112/W70 design only; runtime endpoint NOT VERIFIED. |
| Event sequence / idempotency | W52 event_id/seq/idempotency proposals | Owner must identify canonical event authority, aggregate version and transaction boundary. | NOT DECIDED / NOT VERIFIED. |
| Provider identity and capability | W52 adapter/provider; W51 roles | Work 20/21 own provider bindings; W0000 identity reference plus enforced authority must resolve actual principal and capability. | Owner contract and live binding NOT VERIFIED. |
| Tool permission | W52 tool_permissions; W102 ToolIntent | Work 28 typed tool contract + authoritative authorization; W102 consumes a decision, does not grant it. | NOT VERIFIED. |
| Candidate artifact / provenance | W51 artifacts; W52 artifacts; W102 observations | Immutable path/ref + SHA-256 + version + producer + exact source revision; storage owner must be identified. | Mapping defined; canonical storage contract NOT VERIFIED. |
| Tester-only acceptance oracle | W51 tester_brief / acceptance_programs; W52 shared acceptance_checks | Role-scoped projection or separate protected tester payload; Coder must never receive tester oracle. | Required design constraint; compatibility test NOT RUN. |
| Execution / cancellation | W52 HostPort; W102 run state | W14 Host owns process lifecycle, isolation, stop confirmation and host-observed evidence. | Current HostPort binding NOT VERIFIED. |
| Evidence | W51 reports; W52 provenance; W102 evidence_refs | Use existing canonical evidence owner; no parallel evidence store. Preserve RECORDED vs VERIFIED and MOCK/SNAPSHOT/SANDBOX/LIVE classes. | W112 design draft; live storage contract NOT VERIFIED. |

## 5. Core/Authority evidence blocker

The owner evidence reviewed in this pass does not establish an approved, live Core task/assignment/event API or a production authority service boundary. W37 itself states that its workspace is not Core and that source/runtime verification remains open. W112 DOC-001 explicitly leaves the authoritative runtime API for assignment/ACK and cross-Work auth enforcement unresolved.

Separate W28 Core Execution Authority source findings are recorded in the existing DOC-065 addenda and remain branch/source-level findings, not proof of integration into canonical Core :8000. They identify unresolved protocol mismatch, local grant fallback, caller-asserted authorization, atomicity, persistence/recovery and host enforcement concerns. This pass did not execute those tests or call the live service.

A GitHub default-branch code search for generic task/assignment symbols returned no direct result for the exact search terms used; this is a scoped search observation only and MUST NOT be represented as proof that no such API exists anywhere in the repository or runtime.

Therefore:
- Do not add task/assignment/event fields to Core by assumption.
- Do not implement a W102 task store, dispatcher, queue, event bus, authorization authority or Host.
- Do not wire W52 draft ports to guessed endpoints.
- Do not mark WP1 complete until the accountable owners provide exact approved schemas, source revision, runtime boundary, identity/permission semantics, transaction/idempotency behavior and read-back evidence.

## 6. WP1 exit gate — exact evidence still required

| ID | Required evidence | Owner | State |
|---|---|---|---|
| WP1-E01 | Named accountable Core implementation owner and canonical :8000 service/persistence path, pinned to source SHA | Core / Xu to locate owner | BLOCKED |
| WP1-E02 | Approved Core Work/task/assignment/event schema and legal state transitions, or explicit decision that an existing owner API is authoritative | Core + W70 | NOT VERIFIED |
| WP1-E03 | Authenticated principal, role, assignment, permission and ACK contract; server-side enforcement evidence | W0000 / W01 / W02 / Core | NOT VERIFIED |
| WP1-E04 | Aggregate version/CAS, idempotency, event ordering and atomic transaction semantics | Core | NOT VERIFIED |
| WP1-E05 | Canonical artifact/evidence storage contract and retention/access model | W33 + Core | NOT VERIFIED |
| WP1-E06 | W52 owner-approved A2A contract version and adapter compatibility evidence | W52 | NOT APPROVED / NOT VERIFIED |
| WP1-E07 | W14 HostPort open/execute/stop/cancel and host-observed result contract pinned to current source/runtime | W14 | NOT VERIFIED |
| WP1-E08 | Cross-owner compatibility review and decision recorded in W112/W70; no duplicated runtime or state authority | Xu + component owners + W70 | NOT RUN |

WP1 can exit only when the mapping is approved by the accountable owners and compatibility tests are specified against the exact approved contract. No test is run in this pass.

## 7. Decision and next bounded actions

- Keep DOC-065 as the field-level draft; this DOC-066 is its owner/lifecycle evidence supplement.
- Ask Xu to obtain named Core owner + approved Core contract/source/runtime evidence (WP1-E01..E04).
- Ask W52 owner to confirm the exact A2A version and protected tester-payload projection (WP1-E06).
- Ask W14 owner to supply current HostPort contract and stop/cancel evidence (WP1-E07).
- Ask W33/Core to confirm evidence storage authority (WP1-E05).
- After those owner responses, revise DOC-065 once, create compatibility fixtures/tests only from approved schemas, and request independent review. Do not repeat discovery reads absent new evidence.

## 8. Change-control record

- Read-only inspection of W70/W112/W37/W38/W39/W14 records and scoped GitHub code search.
- No source code, tests, runtime, Work 51/52/112/37/38/39/14 files, Core, Gateway, Host, main branch or release artifacts were modified.
- No dispatch, provider invocation, process execution or live endpoint probe was performed.
- Status remains WP0 PARTIAL; WP1 BLOCKED / DESIGN ONLY; WP2–WP7 NOT RUN / NOT VERIFIED; Work 102 NOT ACCEPTED / NOT RELEASED.

[KÝ: VI | CODER]

## 9. Work Entry and assignment-readiness reconciliation — 2026-11-15

### 9.1 Governing policy read-back
W70 DOC-057 (ACTIVE — POLICY APPROVED / ENFORCEMENT IMPLEMENTATION REQUIRED) requires separate G0–G5 evidence for each participant + Work + assignment. It explicitly permits read-only discovery, evidence collection and draft remediation planning before PASS, but does not authorize product/source changes. Technical enforcement remains NOT VERIFIED until real execution-path negative/positive tests exist.

W70 DOC-044 requires instantiated assignments to bind a Task ID, WP, exact source baseline, scope/permissions, deliverables, acceptance, participant Work Entry G0–G5, explicit authorization, ACK and read-back. A DRAFT assignment is not permission.

### 9.2 Register status limitations
- W70 DOC-093 is DRAFT_NOT_APPROVED; its task assignments and role labels cannot be treated as approved dispatch/authorization records for Work 102.
- W112 DOC-003 and DOC-004 are also DRAFT_NOT_APPROVED; their proposed tasks and agent roles do not prove dispatch, ACK or permission.
- W70 DOC-069 is a Work Entry record for Xu in Work 70, not a transferable Work Entry PASS for Vi or Work 102.
- Work 102 DOC-004 remains a lifecycle gate matrix with G0–G5 not independently evidenced as PASS for the current Vi + WP1 assignment. Historical 2026-10-15 Xu read receipt is historical and does not establish current participant entry or runtime enforcement.
- Therefore no existing record authorizes Vi or any other participant to perform protected WP1 implementation or test execution in this pass.

### 9.3 Allowed and prohibited next actions
**Allowed now:** continue read-only owner/source discovery; prepare bounded contract mapping, evidence requests and draft test designs; update Work 102 documentation/journal/register with read-back.

**Not authorized:** Core/Gateway/Host source edits; runtime/API changes; provider dispatch; protected test execution; task-store/queue/dispatcher creation; state transitions to READY/IN_PROGRESS/DONE; acceptance or release.

### 9.4 Exact readiness closure
Before any protected implementation/test assignment:
1. Xu/authorized owner must instantiate an assignment under the approved Work 102 task/assignment source of truth (not a draft register), with one accountable owner and independent checker.
2. Vi's identity/session, capability, source access and exact assignment scope must be evidenced for this Work and source revision.
3. G0–G5 must be evaluated separately with exact paths/versions and authorized evaluator; G5 must include dependencies, risk, rollback/stop condition and acceptance route.
4. An explicit execution authorization must name allowed actions/paths, source baseline, environment, expiry and revocation conditions; preparation readiness alone is insufficient.
5. Vi must ACK the exact assignment; the ACK must be recorded and read back before IN_PROGRESS.
6. Any independent reviewer/QE must be separately identity/capability/independence verified before review is counted.
7. If no authoritative assignment store or enforcement route is available, remain PREPARATION_READY/BLOCKED and do not infer permission from Sandbox/GitHub access.

### 9.5 Reconciled status
- WP1 design/source trace: UPDATED.
- Work Entry for Vi + WP1: NOT ESTABLISHED / NOT PASS.
- Execution authorization: NOT REQUESTED / NOT GRANTED.
- Assignment ACK: NOT ISSUED.
- Protected implementation and tests: NOT RUN.
- WP1: BLOCKED / DESIGN ONLY.
- Work 102: ACTIVE / NOT ACCEPTED / NOT RELEASED.


[KÝ: VI | CODER]
