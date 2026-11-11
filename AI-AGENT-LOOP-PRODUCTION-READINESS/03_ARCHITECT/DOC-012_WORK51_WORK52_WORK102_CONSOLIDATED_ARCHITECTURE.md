# DOC-012 — WORK 51 / 52 / 102 CONSOLIDATED ARCHITECTURE
- Work: 102 — AI-AGENT-LOOP-PRODUCTION-READINESS
- Version: 1.0
- Date: 2026-11-12 (+07:00)
- Authority: Vinh
- Coordinator: Xu (AI-01)
- Recorder / implementation role: Vi (CODER)
- Status: CONSOLIDATION BASELINE RECORDED / IMPLEMENTATION AND LIVE BINDINGS NOT VERIFIED

## 1. Purpose and governing decision
Work 102 is the sole canonical continuation and integration work for the combined Agent Loop capability. Work 51 and Work 52 remain preserved source/provenance/evidence works. This is a controlled capability consolidation, not a destructive merge and not a declaration that either source Work is complete or production-ready.

The consolidation has four outcomes:
1. Work 102 owns the cross-role Agent Loop and closed-loop acceptance policy.
2. Work 52 contributes the provider-neutral task/event contract and adapter boundary as the preferred interoperability design reference, subject to compatibility mapping and Core approval.
3. Work 51 contributes the proven Coder–Tester vertical-slice behaviors, role-opacity rules, bounded repair, sandbox result handling and evidence requirements.
4. Existing ROOM-HOP owners remain authoritative for Core state, identity/authorization, provider bindings, tools, execution, isolation and test hosting.

No whole runtime is copied into Work 102. No second Core, task database, queue, dispatcher, registry, MCP registry, scheduler or Execution Host is permitted.

## 2. Source Works and evidence truth

### Work 51 — CODER-TESTER-HQTT-AI
Sandbox root: `51/CODER-TESTER-HQTT-AI/`
Canonical source recorded by Work 51: GitHub branch `work/51-hqtt-coder-tester`; Sandbox is documented as a GitHub→Sandbox mirror. The current branch tip/commit was not independently fetched in this consolidation session.

Reusable capabilities:
- WorkContract with separate `coder_brief()` and `tester_brief()`; Coder must not receive acceptance programs.
- Coder and Tester are distinct roles/backends; Tester checks the actual immutable artifact.
- A2A-compatible task/artifact shape and continuation pattern.
- Artifact SHA-256, version, verdict and evidence binding.
- Bounded feedback/repair loop; default maximum two fix rounds.
- Explicit BLOCKED outcomes for transport failure, timeout, missing artifact/verdict, hash mismatch and PASS without evidence.
- Sandbox hardening patterns and tests for negative paths.

Evidence boundary:
- Work 51 EVIDENCE_WORK51 reports a real GitHub Actions run with 43 passed and demo exit 0 on commit `ccbe2985c260c05582a315885d51f6d481cd6910`; artifact upload run is separately recorded. This proves the recorded vertical-slice CI only.
- Work 51 itself says NOT DONE; independent QA, custom seccomp/image digest review and production key management remain open.
- The CI run is historical evidence and is not a fresh Work 102 test or production acceptance.

### Work 52 — ROOM-UNIVERSAL-AI-COMMUNICATION-ORCHESTRATION
Sandbox root: `52/ROOM-UNIVERSAL-AI-COMMUNICATION-ORCHESTRATION/`
Reusable capabilities:
- Provider-neutral internal task/event contract; provider-specific Codex/Qwen/MCP dialects belong behind adapters.
- Closed task schema, versioning, correlation, parent/retry ancestry, scoped paths, capability requirements, idempotency and approval policy.
- Event-sequence model; separate execution state from acceptance verdict.
- Adapter ports: CorePort, AuthorityPort, HostPort and RpcPort; adapters must not bypass those owners.
- Cancellation is not complete until Host confirms process exit; unconfirmed cancellation remains visible.
- Candidate-bound evidence manifest and hash validation.

Evidence boundary:
- Work 52 reconciliation 2026-10-28 reports 29/29 manifest file hashes match Sandbox candidate r2.
- The same report says local checks are coder-recorded and not rerun in that reconciliation; An QA and Ka review were waiting/not verified; Core/Authority and W14 Host integration blocked; native Codex/Qwen invocation and full E2E not run.
- Therefore 29/29 is file-integrity evidence only, not test, provider, Core, Host or release PASS.

### Work 102 — canonical continuation
Work 102 owns common orchestration policy: task lifecycle coordination mapped to Core, role handoff, authorization boundary use, bounded retries/repair, candidate-bound test/review evidence, recovery semantics and end-to-end traceability.
Its existing reference modules and historical 151/151 local tests remain evidence for their exact candidate only. Live Core/Host integration and PC acceptance remain NOT VERIFIED. Current DOC-001 status governs: ACTIVE / STANDARDIZATION IN PROGRESS / NOT ACCEPTED / NOT RELEASED.

## 3. Canonical layered architecture

| Layer | Canonical responsibility | Reuse / implementation rule |
|---|---|---|
| Product authority | Vinh | Approves scope, architecture exceptions and acceptance/release |
| Work coordination | Xu / AI-01 | Plans, dispatch evidence, decisions, journal and handoff |
| Agent Loop policy | Work 102 | Role sequencing, gates, bounded repair, recovery and acceptance predicates |
| Internal task/event contract | Work 52 reference, normalized in Work 102 | One canonical internal contract; no parallel W51/W52/W102 task schemas in runtime |
| Role behavior | Work 51 reference | Coder opacity, independent Tester, artifact-first verification |
| Provider adapters | Work 20/21; Work 52 adapter design reference | Provider dialect stays behind adapter; actual binding requires identity and live handshake evidence |
| Identity / authorization | Work 01/02/22 + Core | Fail closed; no local authorization substitute |
| Tool contracts / registry | Work 28 | Work 102 consumes typed tools; does not register a second tool catalog |
| Task/state/event persistence | Core :8000 | Sole canonical source of task identity/state/event; local JSON stores are test-only |
| Runtime execution / isolation | Work 12/13/27; Work 14 as E2E consumer | No local shell/process host or second executor in Work 102 |
| PC/workspace bridge | Work 24 | Consume only through authenticated, verified route |
| Cross-work evidence | Work 102 EVIDENCE/DOC-014 | Candidate hash, run ID, actor, timestamp, command, raw result, exit code and read-back |
| Lifecycle/layout | Work 70 standard | Apply layout/governance only; Work 70 is not merged into runtime |

## 4. Canonical contract and mapping rules
Work 52's provider-neutral contract is the preferred design reference for the normalized task/event envelope. It is not automatically promoted as a live Core schema. Before implementation, map each field to the existing Core schema and obtain owner confirmation; do not add or rename Core fields based only on Work 52 draft v0.1.

Mapping principles:
- Work 52 `task_id`, `correlation_id`, `parent_task_id`, `retry_of`, `work_id`, `requested_by`, `assigned_agent`, `role`, capability requirements, constraints, workspace scope and acceptance checks map to Core-owned task/context fields.
- Work 51 `WorkContract` maps to the normalized task plus a separately scoped tester-only acceptance payload. Acceptance programs are never placed in the Coder view.
- Work 102 `TaskRequest`, `ToolIntent`, `AuthorizationDecision`, `Observation`, `Budget` and `RunResult` map to the same task/context, authorized intent, execution observation and policy result. They do not create a parallel task store.
- Work 52 event sequence and candidate references map to Core events and immutable artifacts. The Core remains the event sequence authority.
- Keep three distinct concepts: task/workflow state, execution status, and acceptance verdict. `SUCCEEDED/COMPLETED` is not `PASS/ACCEPTED`.
- A PASS verdict must be issued by an authorized independent Tester/Reviewer or human and bind to the exact candidate hash plus verifiable evidence references.
- Repair/retry policy uses the locked Work 102 budget: max_repairs=2 and max_test_runs=3 per defect cycle, unless Vinh changes the decision.
- Idempotency, reauthorization before every side-effect attempt, path scope, cancellation confirmation, deadlines and budget exhaustion must fail closed.

## 5. Canonical Coder → Tester → Reviewer → Planner sequence
1. Core creates/assigns a task with authenticated requester, assignee, WorkContext, scope and correlation ID.
2. Work 102 validates policy and creates role-scoped handoff views.
3. Coder receives objective, allowed context, constraints and output schema only; never acceptance programs or hidden test oracle.
4. Coder publishes immutable candidate artifact with SHA-256 and provenance.
5. Independent Tester receives candidate + acceptance criteria, recomputes hash, executes through authorized Work 14 / Work 12/13 / Work 27 path, and records raw evidence.
6. FAIL may return bounded actionable feedback to Coder within repair budget. Each new candidate gets a new hash; old evidence remains immutable.
7. PASS requires all mandatory checks, candidate-hash match and evidence completeness. Missing evidence, identity mismatch, stale candidate or unconfirmed execution => BLOCKED.
8. Ka independently reviews architecture/security/evidence against the same candidate hash and An's test evidence.
9. Xu reconciles outcomes and records recommendation; Vinh retains final ACCEPT/RELEASE authority.
10. Core is updated through its authorized interface. No Markdown file or Sandbox write is dispatch/ACK proof.

## 6. State and failure semantics
- Preserve Core's existing canonical states; map local labels rather than inventing a parallel state machine.
- Execution result: SUCCEEDED / FAILED / TIMED_OUT / CANCEL_UNCONFIRMED / etc. only where the owning Core/Host contract supports them.
- Acceptance verdict: PASS / FAIL / BLOCKED / NOT_RUN, bound to candidate and evidence.
- Missing capability, absent adapter, unknown identity, authorization denial, stale sequence, invalid hash, scope violation, exhausted budget or missing evidence => fail closed.
- A cancellation request is not cancellation acknowledgement. Do not mark CANCELLED until Host confirms all descendant processes stopped.
- A provider fixture, mock adapter, local JSON store or Sandbox demo is not proof of live provider/Core/Host operation.

## 7. Preservation and canonical ownership of the three Works
- Work 51 and Work 52 remain ACTIVE/reference works with their own histories. Do not relabel them DONE or delete their source/evidence.
- Work 102 is the only canonical integration and forward-development Work.
- Do not copy entire Work 51 `a2a_ct` or Work 52 `room_a2a` runtime packages into Work 102. Extract requirements and specific reviewed behaviors through a compatibility ledger; implement only missing, approved deltas against Work 102's existing code.
- Existing Work 102 source files are candidate baseline, not automatically production source. Resolve canonical repository/branch/commit before any source promotion.
- Apply Work 70 v1.3 structure in Work 102: `00_ROOT, 01_DISCOVER, 02_DEFINE, 03_ARCHITECT, 04_PLAN, 05_BUILD, 06_VERIFY, EVIDENCE, 07_ACCEPT, 08_RELEASE, 09_OPERATE, DASHBOARD`. Existing legacy paths remain preserved until file-level mapping and rollback are verified.

## 8. Consolidation gates
C0 — Source inventory and provenance: all candidate source files, branches, commits, manifests and hashes identified.
C1 — Contract compatibility: field/state/event/error mapping reviewed against Core; no duplicate schema.
C2 — Capability mapping: each W51/W52 behavior mapped to W102 owner/code/test or marked deferred/rejected with reason.
C3 — Security and authority: identity, authorization, scope, idempotency, secret redaction, sandbox and cancellation boundaries independently reviewed.
C4 — Runtime integration: real CorePort/AuthorityPort/provider adapters/HostPort bindings verified by owning systems.
C5 — Independent verification: An tests exact candidate; Ka reviews same hash and evidence; Xu records decision.
C6 — Acceptance/release: Vinh approval only after technical and lifecycle gates pass.

Current status: C0 PARTIAL; C1–C6 NOT VERIFIED. No production acceptance or release claim.

## 9. Immediate next actions
1. Complete file-level source inventories and provenance for Work 51/52/102; verify GitHub branch/commit tips using the owning source channels.
2. Create a compatibility matrix for every Work 51/52 contract, module and test; identify equivalent Work 102 implementation and gaps.
3. Reconcile W52 task/event draft against Core's actual schema with Core owner; keep schema promotion blocked until approved.
4. Map Work 51 Coder opacity, artifact/hash/verdict and sandbox negative tests into Work 102 test specifications.
5. Map Work 52 adapter, event sequencing, cancellation and provider conformance requirements into Work 102 integration gates.
6. Have An independently test the consolidated candidate and Ka review the same immutable hash.
7. Update DOC-014, DOC-036, DOC-037, DOC-055 and DOC-035 with exact file/hash/status/read-back records before any retirement or source promotion.

## 10. Explicit non-claims
This document is a read-and-design consolidation baseline. No code was copied or modified; no tests were run; no provider was invoked; no Core or Execution Host integration was exercised; no GitHub branch was written; no directory was moved or deleted. Work 102 remains NOT ACCEPTED / NOT RELEASED.

[KÝ: VI | CODER]
