# OPEN DECISIONS AND RISKS — WORK 117
- Status: OPEN REGISTER — DRAFT

| ID | Type | Item | Current status | Owner / next action |
|---|---|---|---|---|
| ODR-001 | Decision | Internal storage target | UNKNOWN | Cla/Platform: capacity and resilience assessment |
| ODR-002 | Decision | Cloud provider and region | UNKNOWN | Go/Ka: cost, privacy, residency and security comparison |
| ODR-003 | Decision | Internal-primary vs Cloud-primary | PROPOSED H1 | Cla/Go: compare workload and failure scenarios |
| ODR-004 | Decision | W33 reuse/extension boundary | PROPOSED | Cla: source and concurrency review |
| ODR-005 | Decision | Core authorization/artifact contract | UNKNOWN | Cla/Ka: inspect source/runtime; do not invent endpoint |
| ODR-006 | Decision | Metadata ownership / schema | OPEN | Cla: compare W33 SQLite and media-domain catalog |
| ODR-007 | Decision | Retention, purge and legal hold | OPEN | Ka/Vinh: privacy and governance review |
| ODR-008 | Decision | RPO/RTO, file-size and capacity targets | OPEN | Go/Platform: model and propose measurable targets |
| ODR-009 | Decision | Supported image/video formats | OPEN | Cla/Qw: propose format/codec matrix |
| ODR-010 | Decision | Media worker/transcoding stack | OPEN | Cla: isolation, resource and licensing review |
| ODR-011 | Decision | Encryption and key ownership | OPEN | Ka: threat model and key-management review |
| ODR-012 | Risk | Dual-write inconsistency / replication lag | OPEN | Cla/Qw: idempotency, reconciliation and fault tests |
| ODR-013 | Risk | Unauthorized media exposure | OPEN | Ka: threat model and negative authorization tests |
| ODR-014 | Risk | Cloud egress and storage cost growth | OPEN | Go: capacity and cost model |
| ODR-015 | Risk | Work 33 local-only implementation may not scale to multi-user use | OPEN | Cla: inspect code, concurrency and deployment assumptions |
| ODR-016 | Risk | Agent consultation cannot currently be dispatched through Notion | BLOCKED | Xu: forward consultation brief through authorized channel |


## 2026-11-16 — Architecture options decomposition
| ID | Type | Item | Current status | Owner / next action |
|---|---|---|---|---|
| ODR-017 | Decision | Storage topology: T1 internal-primary/Cloud-replica vs T2 Cloud-primary/internal-cache vs T3 active-active | T1 leading candidate; NOT APPROVED | Cla/Go/Qw: failure, workload, cost and recovery review |
| ODR-018 | Decision | Platform ownership: P1 evolve W33 vs P2 managed/object storage vs P3 bespoke store | P1 leading candidate; P2 valid alternative; NOT APPROVED | Cla: remediation effort, port boundary, migration comparison |
| ODR-019 | Requirement | Many-to-many asset–Work association with per-association authorization | REQUIRED / NOT IMPLEMENTED | Cla/Ka/Qw: model and negative authorization tests |
| ODR-020 | Requirement | Restore/purge lifecycle, idempotent replication, checksum reconciliation and concurrent-write safety | REQUIRED / TARGETS OPEN | Cla/Qw: state machine and fault-test plan |
| ODR-021 | Requirement | Measurable capacity, size, throughput, RPO/RTO, retention and format NFRs | OPEN | Go/Cla/Qw propose measurable values; Vinh approves |
| ODR-022 | Risk | Go egress sensitivity assumptions may not match provider tariffs or Room telemetry | OPEN — ASSUMPTION-BASED | Go: show formula, source tariff, units, measurement basis and sensitivity inputs |
