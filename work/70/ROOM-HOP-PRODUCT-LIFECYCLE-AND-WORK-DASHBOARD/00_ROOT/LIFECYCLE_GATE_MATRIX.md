# LIFECYCLE GATE MATRIX — V1.1

| Gate | Phase exit | Minimum evidence | Decision authority |
|---|---|---|---|
| G0 | Work initialized | Stable ID, owner, manifest, scope boundary and initial permissions | Work owner |
| G1 | DISCOVER → DEFINE | Problem statement, user/context evidence, opportunity and assumptions | Product owner |
| G2 | DEFINE → ARCHITECT | Approved brief, in/out scope, requirements, success metrics and constraints | Product owner |
| G3 | ARCHITECT → PLAN | Architecture, interfaces, data/security model, risks and operational design | Architecture authority |
| G4 | PLAN → BUILD | Roadmap, WPs, owners, dependencies, acceptance criteria and test strategy | Work owner |
| G5 | BUILD → VERIFY | Integrated implementation, build record, tests, known defects and traceable evidence | Work owner |
| G6 | VERIFY → ACCEPT | Independent verification, regression, applicable security checks and defect disposition | Independent QE + owner |
| G7 | ACCEPT → RELEASE | Acceptance record, release package, version, deployment and rollback plan | Acceptance/release authority |
| G8 | RELEASE → OPERATE | Deployment evidence, health checks, monitoring, runbook and support owner | Operations owner |
| G9 | OPERATE → improvement | Operational review, incidents, feedback and improvement backlog | Work owner |

## Rules
- Each gate has criteria, required evidence, evaluator, authority and timestamp.
- G0 must pass before the lifecycle begins. A later gate cannot pass while its predecessor gate is unresolved.
- Gate PASS is recorded by authorized evaluation, not typed by an implementer.
- Missing, stale, contradictory or unverifiable evidence means NOT_READY/FAIL, never PASS.
- WAIVED requires approver, rationale, scope, expiry/review date and accepted risk.
- Gate decisions are immutable; corrections supersede prior decisions with reason and link.
- A later PASS does not erase prior FAIL history.
- Dashboard progress and phase status never substitute for gate state.
