# DOC-013 — WORK 102 CONSOLIDATION IMPLEMENTATION PLAN
- Work: 102 — AI-AGENT-LOOP-PRODUCTION-READINESS
- Date: 2026-11-12 (+07:00)
- Status: PLANNED / EXECUTION IN PROGRESS ONLY AFTER GATE EVIDENCE
- Governing architecture: DOC-012
- Authority: Vinh | Coordinator: Xu | Build: Co/Vi as assigned | Independent QA: An | Review: Ka

## Objective
Consolidate reusable Work 51 Coder–Tester and Work 52 provider-neutral A2A capabilities into Work 102 without copying duplicate runtimes or taking ownership away from Core/Work 01/02/22/20/21/28/12/13/14/24/27.

## Work packages

### WP0 — Freeze and provenance baseline
- Inventory all files in the canonical roots of Work 51, 52 and 102.
- Identify canonical GitHub repository, branch, commit and sync direction for each Work.
- Record per-file SHA-256, candidate manifest, source owner and last verified timestamp.
- Mark stale Sandbox-only files and conflicting candidates; do not overwrite.
- Exit: inventory and provenance register read back; unresolved files explicitly UNVERIFIED.

### WP1 — Contract normalization
- Build a field-by-field mapping: W51 WorkContract/A2A Task/Artifact ↔ W52 room.a2a.task/event ↔ W102 TaskRequest/ToolIntent/Observation/RunResult ↔ actual Core schema.
- Ask Core owner to validate existing fields, identity, sequence, idempotency and state mapping.
- Do not promote W52 draft v0.1 or add Core fields before owner confirmation.
- Preserve tester-only acceptance payload opacity.
- Exit: approved mapping, compatibility tests specified, no parallel task/event schema.

### WP2 — Role and workflow policy
- Normalize Planner/Coder/Tester/Reviewer role contracts and authorized identity checks.
- Enforce Coder cannot read acceptance programs; Tester cannot mutate candidate; Reviewer independent from author/tester.
- Require same immutable candidate hash for Tester, Reviewer and acceptance decision.
- Preserve max_repairs=2 and max_test_runs=3 per defect cycle.
- Exit: policy matrix and negative tests defined.

### WP3 — Adapter/provider boundary
- Map W52 CorePort/AuthorityPort/HostPort/RpcPort to actual existing owner interfaces.
- Map Codex/Qwen/provider protocol to Work 20/21 adapter ownership; no direct provider call from policy core.
- Capability discovery must distinguish AVAILABLE, NOT_CONFIGURED, BLOCKED and FAILED.
- Exit: live binding identity and contract evidence from owners; mocks/fixtures remain TEST_ONLY.

### WP4 — Execution, sandbox and cancellation
- Map Work 51 sandbox hardening and Work 52 HostPort rules to Work 12/13/27 and Work 14.
- No process spawn/shell in Work 102; no local host or fallback isolation for untrusted code.
- Timeout and cancellation require host-side enforcement and confirmed descendant-process stop.
- Exit: authorized host identity, scope, isolation, timeout and stop evidence.

### WP5 — Evidence and recovery
- Candidate hashes, run IDs, correlation IDs, event sequence, raw stdout/stderr, exit code, interpreter/runtime identity, redaction and read-back.
- Reauthorization on each side-effect attempt; stable idempotency key on retry.
- Checkpoint recovery must reconcile with Core and Host before resume; local checkpoint adapter is development-only.
- Exit: restart/duplicate delivery/stale worker/lease/cancel tests tied to immutable candidate.

### WP6 — Independent QA and review
- An runs independent positive, negative, recovery and security matrix against exact candidate hash.
- Ka reviews architecture, authority boundaries, adapter correctness and evidence completeness against same hash.
- Xu records discrepancies and handoff; Vinh decides acceptance.
- Exit: signed independent reports, reproducible commands/results and no unresolved P0/P1.

### WP7 — Controlled acceptance and release
- Reconcile DOC-015 technical gates A–G and lifecycle gates under Work 70 standard.
- Keep SANDBOX_REFERENCE_PASS, LOCAL_TEST_PASS, PC_RUNTIME_PASS, LIVE_E2E_PASS and ACCEPTED/RELEASED distinct.
- Exit: explicit Vinh decision; no inferred release.

## Immediate execution order
1. WP0 inventory and provenance.
2. WP1 Core contract mapping.
3. WP2 role and acceptance policy.
4. WP3/WP4 owner interface verification.
5. WP5 recovery/evidence.
6. WP6 independent QA/review.
7. WP7 acceptance.

## Current execution record
- WP0: PARTIAL — Sandbox inventories and selected documents read; GitHub branch tips/commits not independently fetched.
- WP1: DESIGN BASELINE RECORDED — actual Core schema mapping not yet approved.
- WP2–WP7: NOT RUN / NOT VERIFIED.
- No source changes, test execution, live provider invocation, Core/Host write, GitHub write, move or delete is authorized by this planning record alone.

[KÝ: VI | CODER]
