# PRODUCT REQUIREMENTS — ROOM MEDIA HUB (DRAFT)
- Work: 117
- Status: DRAFT — NOT APPROVED
- Requirement IDs are provisional.

| ID | Requirement | Priority | Acceptance evidence |
|---|---|---:|---|
| RMH-F-001 | Upload image/video with metadata and integrity hash | P0 | Upload/readback/hash comparison test |
| RMH-F-002 | Browse gallery and preview images | P0 | Browser E2E with authorized sample assets |
| RMH-F-003 | Play supported video and show processing state | P0 | Playback test across declared codec/profile matrix |
| RMH-F-004 | Search/filter by metadata, tags and linked Work | P0 | Query tests with seeded dataset |
| RMH-F-005 | Associate one asset with multiple Works without duplicating original bytes | P0 | Relationship and deduplication tests |
| RMH-F-006 | Enforce shared Room-wide access policy through Core authority | P0 | Positive/negative authorization contract tests |
| RMH-F-007 | Hybrid internal + Cloud storage with observable replication status | P0 | Replication, outage and reconciliation tests |
| RMH-F-008 | Verify asset integrity and expose corruption/missing-replica state | P0 | Hash mismatch and missing replica fault tests |
| RMH-F-009 | Audit upload, view/download, share, update, restore and delete | P0 | Audit completeness tests |
| RMH-F-010 | Soft-delete and restore; permanent purge requires approved policy | P0 | Lifecycle and authorization tests |
| RMH-F-011 | Create thumbnails/proxies asynchronously without altering original | P1 | Worker output and original hash unchanged |
| RMH-F-012 | Support albums/collections and controlled sharing | P1 | Collection and access-scope tests |
| RMH-NF-001 | No raw media binaries in GitHub source history | P0 | Repository inspection and CI guard |
| RMH-NF-002 | No direct AI-to-filesystem or public-bucket bypass | P0 | Threat review and negative tests |
| RMH-NF-003 | Encrypt media at rest and in transit | P0 | Configuration and deployment evidence |
| RMH-NF-004 | Define capacity, max file size, throughput and RPO/RTO before BUILD | P0 | Approved NFR baseline |
| RMH-NF-005 | Export/restore without depending on one cloud vendor | P1 | Restore/export rehearsal |

## Pending measurable targets
Maximum file size, supported formats/codecs, upload throughput, preview latency, concurrent sessions, expected asset volume, retention period, RPO, RTO, replication lag and budget must be decided from workload/cost/security evidence. No numeric target is invented in this draft.
