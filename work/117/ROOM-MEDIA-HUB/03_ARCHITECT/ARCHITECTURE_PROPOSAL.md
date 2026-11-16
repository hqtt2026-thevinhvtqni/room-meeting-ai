# ARCHITECTURE PROPOSAL — ROOM MEDIA HUB
- Work: 117
- Status: PROPOSAL FOR CONSULTATION — NOT BASELINED
- Version: 0.1

## Context
ROOM-HOP needs a Room-wide media experience and hybrid storage. Existing W33 documents already define a local content-addressed file store, but not cloud replication, full authorization or production Core integration.

## Logical architecture
1. Room UI / Media Hub: upload, gallery, search, preview, playback, collections and Work links.
2. Media API / application service (PROPOSED): validates requests, metadata and media policy; delegates authorization to Core contract.
3. Media metadata catalog: media identity, checksum, type, dimensions/duration, owner/creator, tags, Work associations, version, retention, processing and replication state.
4. Storage abstraction: adapter interface for internal blob storage and Cloud object storage. W33 is the preferred candidate to host/evolve this abstraction, subject to code review.
5. Processing workers: thumbnail, video proxy/transcode, media inspection and malware scanning; asynchronous and bounded.
6. Core authority: identity, permissions, policy decisions and audit correlation. No second independent identity/authorization database.
7. Observability and operations: replication lag, capacity, failed uploads, checksum mismatch, worker queue, restore and audit health.

## Data ownership
- Core: identity and authorization decisions; canonical Work/agent identity; audit authority if current contracts confirm.
- W117: media-domain metadata and collection/Work relationship model, subject to decision on W33 metadata reuse.
- W33: candidate physical blob storage and integrity primitives; exact ownership boundary to be decided.
- Internal and Cloud storage: bytes only; neither is a business metadata authority.
- GitHub: source, schema, configuration templates and documentation; never original media binaries.

## Hybrid storage model candidates
Candidate H1 (preferred for consultation): internal primary + encrypted Cloud replica, asynchronous replication, checksummed reconciliation and restore tests.
Candidate H2: Cloud primary + internal cache/replica, useful for remote collaboration but dependent on connectivity, egress and cloud availability.
Candidate H3: active-active dual-write is not recommended initially because conflict resolution, partial failures and consistency complexity are materially higher.

## Security and privacy baseline
- Authentication and authorization must be enforced at the service/Core boundary.
- Least-privilege role and Work/asset scope; shared library does not mean public access.
- Encrypt in transit and at rest; define key ownership and rotation.
- Short-lived authorized preview/download references; no public bucket.
- MIME sniffing plus extension validation, file-size limits, malware scanning and safe media decoding.
- Keep secrets out of metadata and logs; audit consequential access and mutations.
- Explicit retention, soft-delete, restore, legal hold and approved purge.
- Define treatment of personal/sensitive media and prohibit secondary use/training absent explicit policy and authorization.

## Resilience and consistency
- Immutable original object identified by cryptographic checksum.
- Idempotent replication jobs; explicit replication states and retry policy.
- Acknowledge upload only after durable internal write and metadata commit; Cloud replication completion is a separate state.
- Remote checksum verification before marking replica healthy.
- Reconciliation detects missing object, orphan metadata, duplicate content and stale replica.
- Define RPO/RTO, offline capacity, queue limits and back-pressure before implementation.

## Risks / unknowns
- W33 source-code/runtime state and concurrency safety not independently inspected.
- No verified Core media authorization or artifact URL contract.
- Internal storage hardware and network capacity unknown.
- Cloud provider, region, cost and legal terms unknown.
- Thumbnail/transcoding toolchain, codec support and worker isolation unknown.
- No agreed retention, file-size, volume or performance targets.

## Architecture status
This proposal is a consultation artifact only. It is not a decision baseline, API specification, implementation claim or permission to BUILD.
