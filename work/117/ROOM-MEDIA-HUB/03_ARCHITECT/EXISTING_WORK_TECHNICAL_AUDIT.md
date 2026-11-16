# EXISTING WORK TECHNICAL AUDIT — W117
- Date: 2026-11-16
- Status: DOCUMENT-LEVEL SOURCE REVIEW — NOT RUNTIME VERIFIED
- Scope: Work 33 RSFEH, Work 26 Multimodal Platform, Work 29 Video Studio
- Purpose: establish evidence-based reuse boundaries for the Room-wide shared media library.

## 1. Work 33 — RSFEH source findings
Inspected Sandbox source:
- `ROOM-SHARED-FILE-EVIDENCE-HUB/04_CODE/src/rsfeh/store.py`
- `ROOM-SHARED-FILE-EVIDENCE-HUB/04_CODE/src/rsfeh/cli.py`
- `ROOM-SHARED-FILE-EVIDENCE-HUB/03_ARCHITECT/DATA_MODEL.md`
- `ROOM-SHARED-FILE-EVIDENCE-HUB/03_ARCHITECT/DECISIONS.md`

Observed:
1. Store is a local filesystem content-addressed blob directory keyed by SHA-256 plus a SQLite catalog and JSONL/SQLite audit.
2. Implemented operations visible in source: init, put, get, metadata, list, search, verify, link_work, soft_delete and audit_tail.
3. CLI is local filesystem oriented; it reads a local path and writes/reads bytes through Store.
4. Agent identity is a caller-provided string (default system); source comments and D-003 explicitly say it is attribution, not full authentication.
5. No cloud storage adapter, replication queue, replica state, remote checksum verification, multi-node coordination or HTTP/API server is visible in inspected source.
6. Current schema has one nullable work_id column per file, not a many-to-many asset_work relation. link_work updates that one work_id, so it cannot represent one shared asset linked to multiple Works without a schema/model change.
7. files.sha256 is UNIQUE. A duplicate active hash returns the existing row; that deduplicates bytes, but does not create a separate asset-to-Work association.
8. soft_delete changes status but no restore method was visible in inspected source.
9. Blob write precedes SQLite transaction; recovery/reconciliation of orphan blobs and metadata was not evidenced in the inspected methods.
10. Audit is written to SQLite and JSONL; atomicity/repair behavior between these two sinks was not established.

Assessment:
- Reuse W33 as a local content-addressed storage component is promising.
- W33 as-is is NOT a hybrid cloud media platform and NOT a Room-wide authorized multi-user service.
- W33 should not be declared the final canonical architecture until source ownership, transaction/recovery, concurrency, API and extension boundaries are reviewed.
- Preferred candidate: evolve W33 behind a stable storage port with internal and Cloud adapters, while W117 owns media-domain UX/catalog workflows. This is a proposal, not an approved change.

## 2. Work 26 — Multimodal source findings
Inspected:
- `04_CODE/multimodal/contracts.py`
- `04_CODE/multimodal/core_ports.py`
- `04_CODE/multimodal/gateway.py`
- `03_ARCHITECT/THREAT_MODEL_AND_ROLLBACK.md`

Observed:
1. Contracts are typed Python dataclasses/enums and explicitly state they are not wired to Core :8000.
2. CoreAuthorizationPort and ArtifactPort are Protocol interfaces, not concrete network integrations.
3. Gateway fails closed if no Core authorizer is configured or Core authorization raises an exception.
4. Caller-provided permission.granted is not trusted as authority.
5. ArtifactPort describes put/get with principal and TTL, but no production storage adapter is evidenced.
6. Threat model requires TTL/size/rate limits, secret hygiene, fail-closed behavior and feature flags off until gate evidence.

Assessment:
- Reuse the security principles and potentially align media reference contracts.
- Do not reuse the current Work 26 artifact port as a proven production media store or claim Core integration exists.

## 3. Work 29 — Video Studio source findings
Inspected:
- `src/video_studio/models.py`
- `src/video_studio/pipeline.py`
- `src/video_studio/provider.py`
- `src/video_studio/renderer.py`

Observed:
1. VideoProject records artifacts as local path strings.
2. MockProvider emits fixture JSON, not actual video bytes; renderer can generate deterministic FFmpeg fixture clips.
3. Provider is a protocol and current source does not show a ROOM MEDIA HUB upload/asset registration adapter.
4. Pipeline evidence is local project state; no shared library handoff is visible in inspected files.

Assessment:
- W29 is a candidate media producer. W117 should define a future ingestion contract for approved outputs.
- Do not assume generated artifacts are already registered in a shared media library.

## 4. Cross-Work architecture consequences
- Shared Room library must separate immutable binary identity from Work associations: one asset may belong to zero, one or many Works.
- Require asset-to-Work many-to-many relation, collection membership and authorization policy; do not overload W33's single work_id.
- Require explicit replication manifest/state per object and per replica, checksum verification, retry/idempotency and reconciliation.
- Require Core-backed service authorization before preview/download/upload; shared library means common discovery surface, not public access.
- Preserve W33 content hash/integrity concept, W26 fail-closed/TTL security principles, and W29 producer integration as separate responsibilities.
- GitHub remains code/config/docs only.

## 5. Verification limits
- This is a source/document inspection through Work Sandbox, not execution of unit tests or live Core/API tests.
- W33 source pointer contains canonical source hashes, but this audit did not independently recompute hashes against the original artifact path.
- No production host, cloud bucket, credentials, Core endpoint or replication process was accessed.
- No tests were run; no PASS is claimed.


## 6. Follow-up review of Cla-reported W33 risks — source readback, 2026-11-16
Status: SOURCE-CORROBORATED / NOT RUNTIME TESTED. Reviewed `04_CODE/src/rsfeh/store.py`, `04_CODE/src/rsfeh/cli.py`, `05_TEST/unit/test_store.py` and `05_TEST/e2e/test_e2e_cli.py` in Work 33 Sandbox.

1. **Work-link overwrite — CORROBORATED.** `link_work()` executes `UPDATE files SET work_id=? ... WHERE file_id=?`; schema has one `work_id` column. Linking a second Work replaces the first association. Existing tests assert only one link and do not test multiple associations.
2. **Soft-delete / restore gap — CORROBORATED WITH PRECISION.** `soft_delete()` changes status to deleted; no restore method is present in the inspected Store/CLI. Because `files.sha256` is UNIQUE and `put()` only deduplicates rows with status='active', attempting to put the same bytes after soft-delete is expected to hit the unique constraint rather than restore/reuse the deleted record. This is a source-level control-flow inference; not executed.
3. **Cross-Work metadata exposure on dedup — CORROBORATED AS A SECURITY RISK, IMPACT CONDITIONAL.** On active duplicate hash, `put()` returns `dict(row)` for the existing file, including its `work_id`, original name and other metadata; CLI prints that result. No authorization check exists in the inspected Store/CLI. This creates a potential metadata disclosure if the CLI/store is exposed across principals without a trusted authorization boundary. It is not evidence of a deployed cross-tenant exploit; runtime/service exposure is unknown.
4. **Concurrent temporary-file collision — CORROBORATED AS A RACE CONDITION RISK.** All writes for the same hash use the same `blob_path.with_suffix('.tmp')` path before replace. Concurrent puts of identical content can contend on that shared temporary path. Failure mode/race reproducibility is not yet tested.
5. **Test coverage gap — CORROBORATED.** The inspected unit/E2E tests cover basic dedup, single Work link, soft-delete, round-trip and integrity checks, but no multi-Work link, restore-after-delete, cross-principal dedup response or concurrent same-hash write test is present.

Architecture impact:
- Treat W33 as a local prototype/component candidate only until authorization is enforced at a trusted service boundary and the above data-integrity/security cases are resolved.
- Required design/test work: normalized asset_work relation with per-association authorization; explicit restore/purge lifecycle; dedup response that does not disclose unauthorized metadata; unique per-operation temp files plus atomic publication; crash/concurrency/reconciliation tests.
- These findings do not authorize changes to W33. No tests were executed and no runtime exploit was demonstrated.
