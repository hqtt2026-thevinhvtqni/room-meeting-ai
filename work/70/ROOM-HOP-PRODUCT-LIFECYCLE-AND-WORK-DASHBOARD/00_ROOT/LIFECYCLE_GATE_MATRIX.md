# LIFECYCLE GATE MATRIX — V1.1
| Gate | Phase exit | Minimum evidence | Decision authority |
|---|---|---|---|
| G0 | Work initialized | Stable ID, owner, manifest, scope, initial permissions | Work owner |
| G1 | DISCOVER → DEFINE | Problem statement, user/context evidence, opportunity, assumptions | Product owner |
| G2 | DEFINE → ARCHITECT | Approved brief, in/out scope, requirements, success metrics, constraints | Product owner |
| G3 | ARCHITECT → PLAN | Architecture, interfaces, data/security model, risks, operational design | Architecture authority |
| G4 | PLAN → BUILD | Roadmap, WPs, owners, dependencies, acceptance criteria, test strategy | Work owner |
| G5 | BUILD → VERIFY | Integrated implementation, build record, tests, defects, evidence | Work owner |
| G6 | VERIFY → ACCEPT | Independent verification, regression, security checks, defect disposition | Independent QE + owner |
| G7 | ACCEPT → RELEASE | Acceptance record, release package, version, deployment and rollback plan | Acceptance/release authority |
| G8 | RELEASE → OPERATE | Deployment evidence, health checks, monitoring, runbook, support owner | Operations owner |
| G9 | OPERATE → improvement | Operational review, incidents, feedback, improvement backlog | Work owner |

Rules: predecessor gates must pass in order; gate PASS is recorded only by authorized evaluation; missing/stale/conflicting evidence blocks PASS; WAIVED requires approver, rationale, scope, expiry/review and accepted risk; gate decisions are immutable and corrections supersede with traceability.
