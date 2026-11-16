# ARCHITECTURE CONSULTATION BRIEF — ROOM MEDIA HUB
- Work: 117
- Date: 2026-11-16
- Status: READY TO SEND — NOT YET DISPATCHED
- Product direction confirmed by Vinh: Hybrid internal + Cloud; shared Room-wide library.

## 1. Consultation question
How should ROOM-HOP deliver a single Room-wide media library over hybrid internal and Cloud storage while reusing existing storage/evidence foundations, preserving Core authorization, and avoiding duplicate binary stores?

## 2. Current evidence (document-level only)
- W33 RSFEH: local SHA-256 content-addressed blob store + SQLite metadata + audit log + Work/evidence links; CLI-first; no HTTP in v1; agent string is attribution, not full authorization; live Core/MCP integration BLOCKED in its own documentation.
- W26 Multimodal Platform: proposed artifact-reference model; Core authority; bounded media transfer and privacy controls; proposed contracts must be source/runtime verified.
- W29 Video Studio: candidate producer of video outputs.
- W116 Resource Library: catalog of external resources, not a binary media library.
- W70 DOC-033 and DOC-075: canonical document ownership and architecture lifecycle/gate rules.

## 3. Proposed boundary for review
- W117: media product layer, media metadata/search, gallery/preview/playback, collections, Work links, processing orchestration, replication status and user workflows.
- W33: candidate canonical blob/file storage abstraction. Prefer extending it with pluggable internal/cloud storage adapters over introducing a parallel blob store. This requires source review and an approved ADR; not a pre-approved implementation decision.
- Core :8000: intended authority for identity, authorization and audit decisions; exact contracts must be inspected and verified.
- Media workers: asynchronous thumbnail/proxy/transcode, malware scan and integrity verification; workers receive bounded references and report job status through approved authority.
- Cloud object store: encrypted secondary/replica tier in the initial candidate topology. Provider and primary/replica direction remain open.

## 4. Options to compare
A. Extend W33 as a single storage engine with internal + cloud adapters; W117 supplies media UX/catalog workflows.
B. Keep W33 local-only and let W117 own a separate cloud media store (risk: duplicate storage, split metadata, inconsistent audit).
C. Replace W33 storage backend with a cloud-first service and local cache (risk: cloud dependency and offline behavior).
D. Adopt an external managed media platform (risk: cost, vendor lock-in, data control and integration).
Reviewers should score each option for integrity, security, privacy, offline usability, availability, operability, cost, portability and migration effort.

## 5. Hybrid topology candidate (not approved)
- Ingest to controlled internal storage.
- Compute SHA-256 and persist immutable original.
- Commit metadata and audit through one transactional service boundary.
- Replicate encrypted objects to Cloud asynchronously with idempotent jobs and explicit states (PENDING / SYNCED / RETRYING / FAILED / CONFLICT / VERIFY_FAILED).
- Verify remote checksum after upload; do not mark SYNCED on upload acknowledgment alone.
- Serve previews via authorization-checked short-lived references; no public bucket or permanent public URL.
- Cloud outage must not silently lose accepted uploads; define queue, capacity and back-pressure.
- Restore rehearsal must prove that metadata and binary objects can be reconciled.

## 6. Required reviewer responses
For each reviewer, provide: (1) findings, (2) evidence/source inspected, (3) alternatives and counterarguments, (4) security/reliability/cost implications, (5) blockers/unknowns, (6) recommendation, (7) conditions before G3/BUILD. Mark each statement IMPLEMENTED / DOCUMENTED / PROPOSED / ASSUMED / UNKNOWN.

## 7. Assigned consultation roles (proposed routing; not yet accepted)
- Cla / AI-03: technical architecture, W33 source review, storage adapter feasibility, data consistency and integration.
- Ka / AI-02: independent architecture/CSA, identity, authorization, privacy, threat model, encryption and data lifecycle.
- Qw / AI-05: independent QE, integrity, replication failure, recovery, contract/E2E testability and acceptance.
- Go / AI-06: cost model, capacity forecast, egress, storage tiers, backup and operating cost.
- Co / AI coder assistant: feasibility and work-package decomposition after architectural alignment.

## 8. Dispatch limitation
Notion Custom Agent discovery was attempted on 2026-11-16 and returned entitlement_required (Business plan or higher). No agent sessions were started and no reviewer response exists yet. This brief is prepared for forwarding through an authorized channel.


## 9. Additional source evidence — 2026-11-16
The separate `EXISTING_WORK_TECHNICAL_AUDIT.md` now records source-level findings:
- W33 is currently local filesystem + SQLite + CLI; not a hybrid/cloud replicated service; its single work_id field cannot express one asset linked to many Works.
- W26 Core and artifact ports are abstract Protocols and are not wired to Core :8000 in the inspected source.
- W29 artifacts are local paths; no shared Media Hub registration handoff was visible.
Reviewers must assess these findings and may challenge them with newer source/runtime evidence. The audit is document/source inspection only; no runtime tests were executed.


## 10. Cla follow-up risk review — source-correlated, not runtime tested
The W117 follow-up source read of W33 `store.py`, `cli.py` and existing unit/E2E tests corroborates these risks:
- `link_work()` overwrites the single `work_id`; multi-Work association is not supported.
- Soft-delete has no restore method; re-put of the same hash after deletion is expected to conflict with the unique hash constraint (not runtime-tested).
- Active duplicate-hash `put()` returns the existing full metadata row, including Work association; without a trusted authorization boundary this can expose metadata across Work scopes. Actual deployed exposure is unknown.
- Same-hash writes share one `.tmp` path; concurrent publication race is plausible and requires a deterministic test.
- Existing tests do not cover these cases.
Review these as P0 architecture/security conditions, not as evidence of a deployed exploit. No W33 code was changed.
