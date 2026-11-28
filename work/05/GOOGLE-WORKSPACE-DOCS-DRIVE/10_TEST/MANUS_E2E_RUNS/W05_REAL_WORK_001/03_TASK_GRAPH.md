# W05 REAL WORK 001 — TASK GRAPH

STATUS: PASS — graph complete; implementation status recorded in final report.
OWNER / AGENT: Manus Orchestrator
TIMESTAMP: 2026-10-05T02:40:00+07:00
INPUT: User command minimum T01–T35 and prior W05 category table.
ACTION: Decompose all required categories with objective/dependencies/owner/research/proposal/evidence/test/decision/status fields.
RESULT:

| ID | Objective | Dependencies | Owner/role | Research | Proposal | Evidence/test | Decision | Implementation | Final |
|---|---|---|---|---|---|---|---|---|---|
| T01 | Overall architecture | existing architecture | Architect | room-hop context | Core-first | topology + tests | DECIDED | built mock | PASS |
| T02 | ROOM-HOP mapping | T01 | Architect | context | MCP→Core→adapter | boundary test | DECIDED | built | PASS |
| T03 | Docs API | T01 | Researcher | official Docs docs | batchUpdate behind adapter | source URLs | PROPOSAL | mock only | PARTIAL |
| T04 | Drive API | T01 | Researcher | official Drive docs | metadata/changes behind adapter | source URLs | PROPOSAL | mock only | PARTIAL |
| T05 | Create document | T03/T04 | Builder | API evidence | adapter create | test_create | BUILT | built | PASS |
| T06 | Read document | T05 | Builder | API evidence | Core read | test_read | BUILT | built | PASS |
| T07 | Append operation | T05 | Builder | Docs writes | idempotent append | test_append | DECIDED | built | PASS |
| T08 | Section update | T05 | Builder | named ranges/markers | controlled section update | test_update | DECIDED | built | PASS |
| T09 | Concurrent write | T07/T08 | Tester | revision controls | serialized Core write | conflict test | DECIDED | mock conflict | PASS |
| T10 | Revision control | T09 | Architect | requiredRevisionId | expected revision | conflict evidence | DECIDED | mock revision | PASS |
| T11 | Conflict handling | T10 | Architect | Docs conflict facts | reject/replan tier | conflict test | DECIDED | mock reject | PASS |
| T12 | Idempotency | T07 | Builder | integration patterns | operation IDs | duplicate test | DECIDED | built | PASS |
| T13 | Queue | T09 | Architect | concurrency | Core single-flight | code lock | DECIDED | in-process lock | PARTIAL |
| T14 | Sync | T04 | Architect | Drive changes/watch | hybrid sync | research only | PROPOSAL | not built | PARTIAL |
| T15 | Reconciliation | T14 | Architect | changes API | bounded recovery poll | research only | PROPOSAL | not built | PARTIAL |
| T16 | Human edit | T08/T11 | Architect | Docs collaboration | drift/intake policy | planned | VINH_GATE | not built | PARTIAL |
| T17 | Authentication | T01 | Researcher | OAuth docs | hybrid | no creds | VINH_GATE | mock auth | PARTIAL |
| T18 | Authorization | T17 | Builder | permission model | Core deny-by-default | auth test | DECIDED | built | PASS |
| T19 | Storage model | T01 | Architect | Drive properties | Core + appProperties | source URLs | VINH_GATE | mock | PARTIAL |
| T20 | Versioning | T10 | Architect | Docs/Drive revisions | Core revision/audit | revision test | DECIDED | built | PASS |
| T21 | Audit/logging | T01 | Builder | process contract | Core audit | audit assertion | DECIDED | built | PASS |
| T22 | Error handling | T11 | Builder | API errors | typed errors | negative tests | DECIDED | built | PASS |
| T23 | Rate/quota | T03/T04 | Architect | official limits | backoff | research only | PROPOSAL | not built | PARTIAL |
| T24 | Middleware boundary | T02 | Builder | room context | thin MCP interface | boundary test | DECIDED | built | PASS |
| T25 | Data model | T01 | Builder | docs model | Document/revision/op | persistence test | DECIDED | built | PASS |
| T26 | Security | T17/T18 | QE | auth guidance | no secrets, Core egress | static review | VINH_GATE | built mock | PARTIAL |
| T27 | Deployment | T01 | Architect | room context | later :8020/:8000 deployment | environment evidence | BLOCKED | local only | PARTIAL |
| T28 | Create/read tests | T05/T06 | Tester | test contract | automated pytest | pytest output | BUILT | PASS | PASS |
| T29 | Concurrent tests | T09 | Tester | concurrency | stale revision test | pytest output | BUILT | PASS | PASS |
| T30 | Human edit tests | T16 | Tester | Docs behavior | planned real test | no creds | N/A—real Google unavailable | not run | PARTIAL |
| T31 | Retry/recovery | T22 | Tester | process contract | bounded retry | adapter failure test | BUILT | PASS | PASS |
| T32 | Permission/auth tests | T17/T18 | Tester | auth docs | unauthorized actor | pytest output | BUILT | PASS | PASS |
| T33 | Evidence | all | Evidence | artifact contract | durable run records | room-hop files | BUILT | PASS | PASS |
| T34 | Migration | T04/T19 | Architect | Shared Drive facts | owner-approved later | no corpus | VINH_GATE | not built | PARTIAL |
| T35 | Backup/recovery | T21/T22 | Architect | recovery contract | Core audit + export later | no real corpus | VINH_GATE | not built | PARTIAL |

EVIDENCE: This table itself plus 04_RESEARCH.md, 07_EVIDENCE.md, 10_TEST.md.
NEXT: Research and proposal synthesis.
