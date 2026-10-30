# AI PROJECT INTAKE & EXECUTION STANDARD
- **STT / Document ID:** DOC-002
- **Priority:** P0
- **Read order:** 2
- **Depends on:** DOC-001
- **Status:** ACTIVE
- **Version / Updated:** 1.2 / 2026-10-30
Version: 1.1
Effective date: 2026-10-30
Status: ACTIVE / ADOPTED BY PRODUCT OWNER
Owner: Vinh (Product Owner / final authority)
Process owner: Xu (AI-01 / lifecycle orchestrator)

## 1. Purpose
Establish one mandatory, repeatable way for every AI to enter, understand, assess, plan, execute and hand off a Work/project. AI models may differ in reasoning and implementation technique; they must not invent different governance, status meanings, evidence rules, storage locations or reporting formats.

This standard applies to every AI role: orchestrator, architect, coder, tester, reviewer, analyst and external AI adapter. Work-specific instructions may add constraints but may not weaken this standard. A deviation requires a recorded decision from the authorized owner.

## 2. Core principles
1. Evidence First: inspect actual artifacts and runtime evidence; do not assume documents are current.
2. Structure Before Detail: map the Work structure and data model before broad code exploration.
3. Reality Over Claims: distinguish DESIGNED, IMPLEMENTED, EXECUTED, VERIFIED and ACCEPTED.
4. No Fake PASS: no PASS without reproducible evidence and the required reviewer/authority.
5. Architecture Before Code: understand boundaries, contracts, data ownership and failure behavior before material implementation.
6. Human Time First: proceed end-to-end within delegated authority; ask only when a real decision or blocker requires the owner.
7. Preserve History: do not silently overwrite, delete, rename, migrate or change branches.
8. One Source of Truth: identify the authoritative source for each kind of state; dashboards, mappings and snapshots are projections, not authorities.
9. Necessary and Sufficient: inspect enough to establish truth and make the next decision; do not read every file without a reason.
10. Honest Stop: when blocked, state the evidence, attempts, bottleneck, impact and exact missing condition.

## 3. Mandatory intake sequence
### Stage A — Identify the Work
Read, in order: DOC-001 Manifest; DOC-002 intake; DOC-033 documentation/storage; Document Register; DOC-003 sync contract; DOC-004 gates; DOC-005 state machine; DOC-006 decision log; DOC-038 naming; DOC-039 type-code standard; DOC-040 issuance ledger; then relevant P1 requirements/architecture/plans and relevant evidence/acceptance; P2/P3 only when task-relevant.

### Stage B — Read the Work structure and data model
Map lifecycle phases, WP ownership/dependencies, state transitions, evidence provenance, decisions, risks, source-of-truth boundaries, canonical storage paths, mapping references, branch/environment and permissions. Directory presence is not proof of implementation or authority.

### Stage C — Trace implementation reality
Inspect repository status, branch and commits; application entry points; configuration names (never expose secret values); data models/persistence; API routes/authorization; external integrations; tests/CI/logs. Trace requirements to implementation and claims to verification.

### Stage D — Verify baseline safely
Establish branch/commit/working-tree state; run read-only checks first; run tests only where safe and authorized; record command, environment/version, timestamp, exit code and output. Distinguish NOT RUN, BLOCKED, FAIL and PASS. No destructive migration, production write or release without authority.

### Stage E — Assess and decide
Produce a concise intake report with confirmed facts/source references, assumptions, unknowns, declared-vs-observed discrepancies, architecture/data flow, dependencies/owners, risks/blockers, verified baseline, decisions/options, execution sequence and measurable acceptance criteria.

## 4. Standard output artifacts
Each Work uses the approved lifecycle locations:
- 00_ROOT/WORK_MANIFEST.md — identity, authority, scope, status, source repositories and sync boundaries.
- 00_ROOT/DOCUMENT_REGISTER.md — stable document IDs, priority, read order and dependencies.
- 00_ROOT/DECISION_LOG.md — binding decisions, rationale, authority and date.
- 00_ROOT/BIEN_BAN.md — official meeting/minutes register (create only when adopting the Work's standard file set).
- 00_ROOT/NHAT_KY_THI_CONG.md — chronological Work-wide execution log.
- 01_DISCOVER/DISCOVER_BRIEF.md — problem, users, context and evidence.
- 02_DEFINE/PRODUCT_REQUIREMENTS.md — requirements, non-goals, constraints and acceptance criteria.
- 03_ARCHITECT/ — canonical drawings, models, architecture and contracts.
- 04_PLAN/ — canonical plans, roadmap, dependencies and WP plan.
- 05_BUILD/ — mapping and engineering coordination only; not canonical original source.
- 06_VERIFY/ — verification strategy and checklist.
- 06_EVIDENCE/ — cross-phase canonical evidence index and verified evidence references.
- 07_ACCEPT/, 08_RELEASE/, 09_OPERATE/ — acceptance, release and operations records.
- DASHBOARD/ — read-only status projection, never an independent authority.

The four standard Work records are: BIÊN BẢN, KẾ HOẠCH, BẢN VẼ/MÔ HÌNH (when needed), and NHẬT KÝ THI CÔNG. Their exact canonical paths and ownership are defined by WORK_DOCUMENTATION_AND_STORAGE_STANDARD.md. Do not create competing copies.

## 5. Mandatory AI handoff/report format
Every AI contribution states: AI identity/role; Work/WP/scope; branch and starting commit; inspected files/evidence; changes (or read-only); commands/tests and exact results; status with evidence; risks/dependencies/next owner; ending commit and sync status.

A roster is not proof of participation. Never invent token usage, test output, CI results or approvals.

## 6. Shared status vocabulary
PLANNED, ACTIVE, BLOCKED, DONE, PASS, FAIL, NOT RUN, NOT VERIFIED, UNKNOWN, ACCEPTED and RELEASED retain their defined meanings. DONE is not PASS; PASS is not ACCEPTED; ACCEPTED is not RELEASED. UNKNOWN, NOT RUN and NOT VERIFIED are not PASS.

## 7. Authority and escalation
AI may make routine, reversible decisions within assigned scope and approved architecture. Stop before changing product goals, authority, security policy, destructive data, production, material recurring cost, canonical schemas/source-of-truth boundaries or release without authorized approval.

When blocked, report problem, attempts/evidence, bottleneck, impact, options and precise missing condition. Do not repeat retries without new evidence.

## 8. Execution after intake
Use READ → TRACE → ANALYZE → DECIDE → ARCHITECT → PLAN → BUILD → INTEGRATE → VERIFY → DEBUG → REGRESSION → ACCEPTANCE PREPARATION → HANDOFF. Complete the applicable workflow end-to-end within approved scope; keep implementation, independent verification and final acceptance distinct.

## 9. Adoption and compliance
Xu maintains this standard. Every AI acknowledges Work ID, role, assigned scope and applicable standards before changes. Deviations require a recorded authorized decision. Standard changes are versioned.

## 10. First-response checklist
- [ ] Identify Work ID, owner, scope, status and standard version.
- [ ] Read Manifest, documentation/storage standard and Document Register.
- [ ] Read repository/Sandbox sync contract and source-of-truth boundaries.
- [ ] Map canonical Work structure and registers.
- [ ] Read relevant brief, requirements, architecture and decisions.
- [ ] Inspect branch, commit and working-tree state.
- [ ] Trace implementation and verify baseline safely.
- [ ] Produce intake report before material implementation.
- [ ] State blockers and next actions; do not claim unverified status.

## 11. Document numbering and reading priority
Every Work document must be indexed in 00_ROOT/DOCUMENT_REGISTER.md. Every new or materially revised Markdown document must have stable STT/Document ID, Priority P0-P3, Read order, Depends on, Status, Version/Updated immediately below title. STT is stable identity, not rank. Never renumber existing IDs. Priority and read order are separate. Legacy documents are indexed and receive metadata on next material edit; do not mass-rewrite them. JSON records carry equivalent metadata in their schema/register where applicable. Register conflicts must be reconciled before relying on reading order.
