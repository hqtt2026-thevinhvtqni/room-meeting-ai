# DOC-065 — WP1 CONTRACT COMPATIBILITY MAPPING (DRAFT)
- Work: 102 — AI-AGENT-LOOP-PRODUCTION-READINESS
- Date: 2026-11-12 (UTC+07:00)
- Prepared by: Vi | CODER
- Governing architecture: DOC-012
- Source baseline: W51 WorkContract; W52 task/event schemas and Contracts ports; W102 agent_loop_contract.py
- Status: DRAFT / SOURCE-CONTRACT READ ONLY / CORE MAPPING NOT VERIFIED / NOT APPROVED

## 1. Purpose and safety boundary
This document compares visible Sandbox contract definitions to prepare a single normalized Work 102 integration contract. It does not promote Work 52 draft schema to Core, create a new task store, or authorize source edits. The actual Core :8000 task schema, event schema, authorization payload, transaction semantics and owner approval are unavailable in this inspection; all Core field mappings below remain NOT_VERIFIED until Core owner read-back and approval.

## 2. Source contracts inspected
- W51: CODER-TESTER-HQTT-AI/04_CODE/a2a_ct/contract.py — WorkContract schema work51/v1.
- W52: ROOM-UNIVERSAL-AI-COMMUNICATION-ORCHESTRATION/03_ARCHITECTURE/a2a-task.schema.json — draft room.a2a.task/0.1.
- W52: a2a-event.schema.json — draft room.a2a.event/0.1.
- W52: 04_CODE/room_a2a/contracts.py — schema validation plus CorePort, AuthorityPort, HostPort, RpcPort interface proposals.
- W102: 05_BUILD/04_CODE/agent_loop_contract.py — policy/reference dataclasses ToolIntent, ToolObservation, LoopState, LoopBudget, Decision; module explicitly says it does not execute tools, call providers, grant authority or persist checkpoints.

## 3. Field-level compatibility matrix
| Concern | Work 51 source | Work 52 source | Work 102 source | Proposed normalized treatment | Core status |
|---|---|---|---|---|---|
| Task identity | contract_id | task_id | run_id | One Core-owned task_id; retain contract_id/run_id only as scoped correlation/reference identifiers if Core owner confirms | NOT_VERIFIED |
| Correlation | Not a required WorkContract field | correlation_id | ToolObservation.correlation_id | Use Core-owned correlation identifier; never generate a competing canonical one | NOT_VERIFIED |
| Work scope | Implicit in Work/run setup | work_id, workspace_scope | ToolIntent.work_id, LoopState.work_id | Map to canonical WorkContext and scoped paths owned by Core/authority | NOT_VERIFIED |
| Requester / assignee | created_by string (default vinh) | requested_by, assigned_agent.identity/adapter | external identity_verified input to authorize_intent | Treat all payload identities as claims; resolve/authenticate through Work 01/02/22 and Core | NOT_VERIFIED |
| Role | Coder/Tester view methods | role enum PLANNER/CODER/TESTER/REVIEWER | policy layer has no authenticated role field | Role must be derived from authenticated assignment/authority, not trusted from model-supplied role | NOT_VERIFIED |
| Objective / instruction | objective, function_signature, artifact_filename | input.instruction, context_refs, artifacts | ToolIntent.target/capability/tool_name | Normalize as task instruction plus typed input/artifact refs; avoid overloading target | NOT_VERIFIED |
| Candidate artifacts | solution_bodies and artifact_filename | input.artifacts with path + sha256 | ToolObservation.result/evidence_refs | Immutable artifact ref with path, SHA-256, version and provenance; owner must define canonical storage | NOT_VERIFIED |
| Acceptance oracle | acceptance_programs in tester_brief only | acceptance_checks embedded in task schema | no acceptance-program field | Split protected tester-only acceptance payload from Coder-visible task view; never expose W51 acceptance_programs to Coder. W52 shared task envelope must be projected/redacted per role before dispatch | NOT_VERIFIED |
| Output contract | function_signature and artifact_filename | output_schema | ToolObservation.result mapping | Typed output schema validated at adapter boundary; no remote schema resolution unless explicitly approved | NOT_VERIFIED |
| Retry ancestry | max_fix_rounds | parent_task_id, retry_of, constraints.max_retries | retries_for_current_step, max_retries_per_step | Preserve parent/retry lineage in Core; map repair budget separately from transport retry budget | NOT_VERIFIED |
| Budgets / deadlines | max_fix_rounds, sandbox_timeout_s | timeout_seconds, queue_timeout_seconds, max_retries | LoopBudget max_steps, max_retries_per_step, deadline_epoch_s, max_estimated_cost | Distinguish Work102 locked max_repairs=2/max_test_runs=3 from provider/transport retry and wall-clock/cost budgets | NOT_VERIFIED |
| Idempotency | Not present | constraints.idempotency_key; CorePort.create proposes atomic dedupe | ToolIntent.idempotency_key optional | Required stable key for side effects/retries; Core owner must confirm persistence and conflict semantics | NOT_VERIFIED |
| Tool permissions / approvals | Not present | tool_permissions, approval_policy | requires_human_approval, approval_present | Work28 typed tool contract + Core authority; W102 only consumes decision, does not grant it | NOT_VERIFIED |
| Execution state | W51 states/pipeline result | task state in events | RunStatus READY/RUNNING/SUCCEEDED/FAILED/BLOCKED/CANCELLED/BUDGET_EXHAUSTED | Map to existing Core task state only after owner confirmation; do not equate with acceptance verdict | NOT_VERIFIED |
| Event identity/order | Evidence log, not shared canonical event sequence | event_id, task_id, seq, ts, producer, provenance | ToolObservation correlation_id/evidence_refs | Core owns sequence, persistence and atomic state/event transaction; W52 event is design input only | NOT_VERIFIED |
| Acceptance verdict | Tester emits PASS/FAIL/BLOCKED with evidence | VERDICT_RECORDED event type; candidate refs | no first-class acceptance verdict type | Separate verdict enum PASS/FAIL/BLOCKED/NOT_RUN tied to immutable candidate hash and independent tester/reviewer | NOT_VERIFIED |
| Cancellation | Sandbox timeout behavior | CANCEL_REQUESTED event; HostPort.stop(task_id) -> bool | RunStatus.CANCELLED | Request != confirmation; Core state may become CANCELLED only after W14 Host confirms descendants stopped | NOT_VERIFIED |
| Evidence provenance | Evidence report/hash records | event provenance + raw_sha256; artifact sha256 | evidence_refs tuple | Store run_id, actor identity, timestamp, command, runtime, exit code, raw logs, candidate hash and read-back reference in canonical evidence registry | NOT_VERIFIED |

## 4. Blocking compatibility findings
1. **Acceptance confidentiality mismatch:** W51 deliberately separates coder_brief() from tester_brief(). W52 task schema includes acceptance_checks in the common task object. A single shared task object must not be passed unchanged to Coder; role-scoped projection or a separate protected acceptance payload is mandatory.
2. **Identity trust mismatch:** W52 schema includes requested_by, assigned_agent.identity and role, but its AuthorityPort documentation says claimed role from model input is never trusted. Core/Authority must resolve the authenticated actor and assignment independently.
3. **Retry-budget ambiguity:** W51 max_fix_rounds, W52 max_retries, and W102 max_retries_per_step are different counters. Do not merge them into one field or permit any to override the locked W102 repair/test budget.
4. **State/verdict ambiguity:** W52 task event states and W102 RunStatus describe execution/workflow progress; neither alone means acceptance PASS. Preserve distinct task state, execution status and acceptance verdict.
5. **Idempotency ownership:** W52 CorePort describes atomic dedupe/CAS as a proposed Core behavior; it is not evidence that live Core currently supports it. Verify actual Core contract before implementing an adapter.
6. **Cancellation ownership:** W52 HostPort.stop proposal and W102 local CANCELLED enum do not prove process termination. W14 must provide authoritative stop confirmation.
7. **Tool authority:** W52 tool_permissions and W102 ToolIntent are not substitutes for Work28 tool registry or Core authorization.

## 5. Proposed single normalized Work 102 view (design only)
- Core-owned envelope: task_id, correlation_id, work_id, authenticated requester/assignee references, canonical state/version/sequence, timestamps and idempotency identity — exact field names await Core owner.
- Role-scoped views: Coder view contains instruction, permitted context, constraints and output contract only; Tester view adds protected acceptance criteria; Reviewer view receives immutable candidate and complete test/evidence bundle.
- Typed execution intent: tool name, target, capability, scoped work root, approval requirement and idempotency key, validated against Work28 and canonical authority.
- Observation: normalized result/error classification, duration, correlation reference and immutable evidence references.
- Acceptance record: candidate SHA-256, independent actor, verdict, test run identity, evidence references and timestamp.
- Event envelope: Core-owned event ID/sequence/state transition and producer provenance; W52 draft event schema remains a reference until Core approves mapping.

## 6. Required Core-owner confirmation before WP1 exit
1. Actual live Core task schema and event schema (source path/API version + exact field definitions).
2. Authenticated requester/assignee identity and role derivation; authority decision contract and audit trail.
3. Canonical task state machine/version/CAS behavior and event sequence/persistence semantics.
4. Idempotency key scope, duplicate behavior and retry lineage persistence.
5. Canonical WorkContext/workspace path scope and approval/tool permission integration with Work28.
6. Host dispatch/ACK/result correlation and cancellation/descendant-stop confirmation owned by W14.
7. Explicit approval of role-scoped acceptance payload separation.
8. Compatibility test cases against the approved schema; no implementation until approval.

## 7. Gate status
- W51/W52/W102 source contract reads: DONE (read-only).
- Draft field compatibility mapping: RECORDED.
- Acceptance opacity risk: IDENTIFIED; design rule recorded, implementation NOT RUN.
- Actual Core schema mapping: NOT VERIFIED.
- Core owner approval: NOT RECEIVED.
- WP1: BLOCKED / DESIGN DRAFT ONLY — no source edit or Core schema change permitted.

[KÝ: VI | CODER]


## 8. External cross-Work boundary check — W112 (2026-11-12)
A read-only check was made because W112 owns cross-Work contract definitions and integration verification under its current Work manifest:
- W112 Sandbox manifest: ACTIVE — DISCOVER / DEFINE; GitHub main is recorded as source of code truth; Sandbox is the working/verification zone. W112 explicitly excludes rebuilding W52 communication orchestration, W14 execution-host ownership, W37 Core, W38 Gateway, W39 Build MCP and W0000 governance registry.
- W112 DOC-001 §1–§2 assigns cross-Work contract definitions to W112; AI communication/orchestration remains W52; execution host remains W14; identity/roster/permission reference is W0000; Core/Gateway/Build MCP runtime ownership is explicitly NOT VERIFIED until proven through W37/W38/W39 investigation records.
- W112 DOC-001 is DRAFT / NOT APPROVED FOR RUNTIME ENFORCEMENT. Its design baseline cannot be treated as a live schema or authorization grant.
- GitHub main ref was read as a663bd5afda524cb9dc7ca685945ca96c68d664d. Sandbox W112 DOC-001 contains the GitHub main text as an exact prefix, plus later Sandbox-only addenda (including 2026-11-11); exact full-file parity is therefore FALSE. Do not silently promote the Sandbox addendum to GitHub source.
- W112's DOC-001 says non-W70 Works should retain their own approved task model; cross-Work IDs are correlation only and must not duplicate task state. This reinforces the no-second-task-store rule.

### Required architecture reconciliation
1. Work 102 continues to own its internal Agent Loop policy (role sequence, bounded repair, recovery and acceptance predicate), not the cross-Work contract registry or communication transport.
2. W52 remains communication/orchestration component owner; W102 consumes its approved task/event contract through a compatibility adapter/projection, not a copied runtime.
3. W112 is the cross-Work contract design/integration-verification owner, but its baseline is still draft. Do not enforce it until independent review and Vinh approval.
4. W14 remains the execution-host owner. Work 102 cannot claim dispatch, ACK, process-stop or live E2E without W14 evidence.
5. Identity and Core/Gateway/Build MCP ownership must be reconciled against W0000 and W37/W38/W39 records. W102's intended Core source-of-truth principle does not prove the live endpoint or owner is verified.
6. Any eventual normalized Work 102 task/event view must be a consumer projection of approved owner contracts; no independent cross-Work canonical schema or state register.

**Effect on WP1:** The draft mapping remains useful for identifying field overlaps and security risks, but its external contract authority dependency is now explicit: W112 DOC-001 + component-owner approval + verified Core/Authority contract are prerequisites. WP1 remains BLOCKED / DESIGN DRAFT ONLY.



## 9. Owner-source evidence check — Core, Gateway, Build MCP, identity and Host
Read-only owner Work records and current GitHub main source were inspected to determine whether WP1 can map to a real Core task schema.

### 9.1 Core :8000 / Work 37
- Work 37 manifest is ACTIVE, but its 04_CODE directory contains only a desktop.ini placeholder in the observed Sandbox inventory.
- CORE_8000_SCOPE.md explicitly says its baseline comes from ROOM CONTEXT and lists process entrypoint, routers, DTOs, persistence/transactions, state transitions, authentication and authorization as items still to be verified.
- SANDBOX_MIRROR_ROLE_AND_SINGLE_CORE_RULE.md states Work 37 is an evidence/documentation workspace for the one live Core, not a second Core; live behavior and mirror completeness remain NOT VERIFIED.
- Current GitHub main source inspection (read-only, ref a663bd5afda524cb9dc7ca685945ca96c68d664d) fetched core/meeting_service.py, core/meeting_manager.py, core/meeting_log.py and room_hop_mcp/adapter/http_server.py. The inspected HTTP adapter exposes meeting lifecycle/transcript/paste and read-only identity discovery routes; the inspected MeetingService/Manager/Log implement meeting operations and meeting events. No generic agent-task dispatch, assignment ACK, lease/fencing or canonical task-event endpoint was observed in these inspected files.
- Classification: MEETING DOMAIN EXISTS IN INSPECTED SOURCE; GENERIC TASK/ASSIGNMENT/ACK/LEASE API = NOT VERIFIED IN INSPECTED SCOPE. Do not generalize this to repository-wide MISSING and do not treat source inspection as live :8000 runtime proof.

### 9.2 Gateway :8040 / Work 38
- Work 38 manifest says CREATED, technical content not audited, source/runtime audit NOT STARTED, live service UNKNOWN / NOT VERIFIED.
- Therefore no Gateway contract can be bound to W52 RpcPort or W102 dispatch in this pass.

### 9.3 Build MCP :8030 / Work 39
- Work 39 Sandbox manifest is ACTIVE, but the observed Work 39 tree is a small documentation/structure inventory; no verified live tool contract or runtime owner binding was established here.
- The existence of the Build MCP Sandbox tools used for file operations is not proof of a generic task-dispatch service, production Core authority or a W52 RpcPort binding.

### 9.4 Identity / governance / Work 0000
- W112 DOC-001 references W0000 governance registry for identity, roster and permission, but Work 0000 DOC-021 (2026-11-03) states Work 99 server-side entry/dispatch enforcement remains NOT VERIFIED; policy text is not technical authorization proof.
- Work 0000 DOC-016 is a point-in-time GitHub hqtt-ai-platform main snapshot from 2026-11-03, not a current runtime identity/authorization attestation for ROOM-HOP Core.
- W102 must consume identity/authorization decisions from the verified owner path; no identity is accepted from model-provided role or Sandbox metadata alone.

### 9.5 Execution Host / Work 14
- Work 14 manifest identifies Work 14 as sole product/delivery/release owner for W12+W13+W14 consolidation.
- Work 14 records historical W13 PC /health and POST /execute attestation PASS on 2026-10-12, with matching runtime identity. This proves that specific historical W13 host attestation only.
- The same W14 manifest states full W14 UI → canonical W13 → W09.1 → real Chromium → verified artifact/E2E is NOT yet proven; security closure and independent release review remain open.
- Cla's 2026-10-11 report records seven SANDBOX_PASS gates, but explicitly does not claim PC_RUNTIME_PASS and lists AUD-001 through AUD-007 source findings. No current W14 live dispatch/ACK/stop contract was verified in this pass.
- Classification: W13 historical PC host attestation = RECORDED/PASS for that specific run; W14 full product E2E, current HostPort binding, cancellation descendant-stop and independent release = NOT VERIFIED.

## 10. WP1 updated gate decision
- A canonical generic Core task/event schema and live endpoint binding are still NOT VERIFIED.
- The inspected Core HTTP adapter is meeting-focused; this is a scoped observation, not proof of global absence.
- Work 38 Gateway is not audited; Work 39 live dispatch binding is not verified; Work 0000 policy does not prove runtime authorization.
- W14 owns execution host; historical W13 attestation cannot substitute for current HostPort open/stop and full W14 E2E evidence.
- W112 cross-Work contract remains DRAFT / NOT APPROVED and must be reconciled with component owners.
- WP1 remains BLOCKED / DESIGN DRAFT ONLY. Do not implement a parallel Core task store, queue, dispatcher, authorization layer or Execution Host in W102.
