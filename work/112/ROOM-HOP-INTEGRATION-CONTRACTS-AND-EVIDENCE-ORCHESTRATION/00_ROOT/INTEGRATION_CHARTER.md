# WORK 112 — INTEGRATION CHARTER
## Objective
Make existing ROOM-HOP capabilities behave as one coherent machine through explicit, versioned and testable contracts.
## Initial Work Packages
- WP112-01 Inventory & ownership reconciliation: map W70/W32/W1111/W0000/W21/W33/W52/W16/W51/W39/W37/W38/W14 and other relevant Works; inspect canonical manifests, decisions, journals and source contracts.
- WP112-02 Integration contract registry: define Work/Task/Agent identity, assignment, ACK/progress/result, event, evidence, artifact, state transition, correlation and error schemas.
- WP112-03 Event and evidence correlation: connect task lifecycle events to CI runs, test results, artifacts, journal entries and dashboard projections.
- WP112-04 Cross-Work dependency and concurrency: define dependency readiness, idempotency, locking, duplicate delivery, retries, timeout and recovery.
- WP112-05 Integration test harness: test end-to-end flows across real components; distinguish mocks, snapshots and live evidence.
- WP112-06 Independent QE & acceptance: negative, race, replay, security, recovery and multi-agent/multi-work tests.
## Ownership boundaries
W70 defines authority and approves system-level contracts. W112 owns cross-boundary contracts only. Component owners implement their own adapters. W32 owns CI engine; W33 evidence storage; W52 communication; W16 workflow execution; W14 execution host; W37 Core; W38 Gateway; W39 Build MCP. No component is modified outside its owner contract.
## Entry rule
Read W70 entry standard, Manifest, decisions and full relevant journal, then target Work records. Record read scope and source revision before implementation.
## Acceptance
Every integration claim includes source SHA/version, test command/method, raw result, artifact/evidence reference, independent reviewer and exact status. Founder acceptance required for system-level release.
