# WORK 101 — DEPENDENCY AUDIT & NEXT EXECUTION GATE
Date: 2026-10-13 (+07)
Coordinator: Xu | Authority: Vinh
Status: DESIGN BASELINED; IMPLEMENTATION NOT VERIFIED

## 1. Audit result
- MAIN_SOURCE and ROOM CONTEXT were read through MCP. Core :8000 remains the single source of truth; MCP :8020 is the AI boundary; Workspace :8010 is separate; Sandbox is the build zone; MAIN_SOURCE is read-only for AI build operations.
- Work Index 99 was read back. Work 101 is registered as ACTIVE / NO; runtime count is 37. Registry rule says ACTIVE/TEST/BLOCKED/IN_PROGRESS must not be locked.
- Work 101 requirements, architecture, sync contract and E2E acceptance plan were read. They agree on two-way rule-based sync, no silent overwrite, digest-bound approval, audit evidence, and no PASS without runtime evidence.
- Work 24 architecture and gap register were read. It has a filesystem scaffold, but the Core-initiated authorization/transport route to the canonical PC is not exposed/proven in this session. Do not invent an endpoint or treat cloud-session localhost:8031 as the PC.
- Work 27 contract/architecture were read. It owns runtime packaging, workspace identity, isolation, evidence normalization and cross-work runtime tests. Work 101 must not create a second execution host.
- Work 28 tool registry/decision were read. Its registry is DRAFT / NOT REGISTERED IN LIVE MCP; current connector tools do not include execution_submit/python_run. Canonical MCP -> Core -> runtime route, isolation, and approved execution remain BLOCKED. Do not register a new execution tool from Work 101.
- Work 14 current snapshot and dependency audit were read. W14 is described in its current snapshot as ACTIVE / UNLOCKED with current full product E2E/security acceptance incomplete. Work Index 99, however, says W14 COMPLETED / LOCKED. Historical release evidence conflicts with newer blockers. This is a lifecycle/source-of-truth contradiction; Work 101 must not change W14 status or assume current acceptance.
- Work 100 is present as the incident/RCA and lessons Work; use it as a source for incident patterns, not as a substitute for fresh acceptance tests.

## 2. Reuse / ownership boundary
- Work 101 owns only: sync target/policy, path mapping, change ledger, conflict workflow, digest-bound approval binding, and Sandbox-GitHub adapter contract.
- Work 24 owns shared PC source/workspace bridge; Work 27 owns runtime packaging/isolation; Work 28 owns MCP tool contract and authorization/E2E harness; Work 14 is the intended canonical autonomous product E2E/release owner, but its status contradiction must be reconciled first.
- No duplicate Core, runtime, shell, browser/Git provider, or PC bridge is permitted.

## 3. Current capability reality
Available and verified in this session:
- Read/list/write within authorized Work Sandbox through MCP.
- Read-only MAIN_SOURCE structure/context.
- Work 101 row in Work Index 99 confirmed by readback.

Not available/proven in this session:
- Running Python/pytest/PowerShell or a process from the Work Sandbox.
- Live PC MCP/Core deployed SHA and authenticated route attestation.
- GitHub adapter credentials/write path, repository/branch allowlist and live bidirectional read-back.
- Conflict simulation, transfer idempotency, or real cross-environment E2E.
Therefore no sync implementation or runtime acceptance can honestly be marked PASS.

## 4. Decisions
1. Keep Work 101 ACTIVE / NOT LOCKED.
2. Keep all sync actions in DRY_RUN until the actual GitHub target, branch, credential boundary and adapter are verified.
3. Do not write MAIN_SOURCE, merge, release, commit or push.
4. Do not use last-write-wins. Same-path concurrent changes become CONFLICT_PENDING.
5. Do not add MCP tools before comparing the actual live registry and Core service contract.
6. Keep integration/merge/release behind explicit Vinh approval bound to operation ID, diff digest, destination branch and base revision.
7. Missing PC/GitHub/runtime evidence is BLOCKED / NOT VERIFIED, never PASS.

## 5. Next execution order
P0 — Establish canonical target contracts:
- Inspect Work 101 existing target mapping/manifest and determine whether repository URL, branch and permitted path roots are explicitly supplied. Do not guess them.
- Read Work 24 scoped filesystem contract and Work 28 live-vs-draft registry evidence; identify exact interfaces available and missing.
- Request read-only, source-backed reconciliation of Work 14 status in Work Index 99 versus its manifest/current snapshot. Do not change either lifecycle record without evidence/authority.

P1 — Implement only the isolated sync-policy core in Work 101 Sandbox:
- Typed target/policy/change-plan/conflict/approval/evidence models.
- Pure path/digest/revision/conflict/idempotency validation; no network writes or credentials.
- Dry-run plan generation and deterministic conflict classification.
- Unit tests and fixtures can be authored, but are NOT PASS until run by an approved execution environment.

P2 — Integrate only after verified adapter contract:
- Use an existing authorized GitHub adapter or request its creation under an approved owner; no credential in Sandbox.
- Transfer to a non-protected feature branch only after configured target + write authorization exists.
- Verify destination by read-back digest; persist correlated evidence.
- Run real two-way E2E and negative security tests in an approved runner.

P3 — Integration gate:
- Show exact diff, target branch, base SHA, operation ID, digest, tests and evidence to Vinh.
- No integration/merge/release until Vinh explicitly approves that exact digest and target.

## 6. Evidence discipline
This is a source-backed static dependency audit and registry read-back, not runtime acceptance. No code implementation, GitHub write, PC operation, commit, push, merge, release or E2E execution occurred during this audit.
