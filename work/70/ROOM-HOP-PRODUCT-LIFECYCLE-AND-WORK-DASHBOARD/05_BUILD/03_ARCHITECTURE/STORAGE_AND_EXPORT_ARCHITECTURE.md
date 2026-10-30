# STORAGE & FILE EXPORT ARCHITECTURE — WORK 70

Version: 1.0
Date: 2026-10-30
Status: DESIGN PROPOSAL — NOT IMPLEMENTED / NOT VERIFIED
Scope: Work 70 / 05_BUILD only

## 1. Purpose

Add durable, auditable storage and controlled file export to the Work lifecycle product without creating a second source of truth.

The existing Dashboard is a read-only projection of `PRODUCT_STATUS.json`. It does not currently prove durable persistence or downloadable export. This document defines the target contract; it does not claim that APIs, database tables, storage buckets or UI actions already exist.

## 2. Non-negotiable architecture decisions

1. **Core remains the Single Source of Truth (nguồn dữ liệu chuẩn duy nhất)** for Work identity, permissions, lifecycle state, decisions and canonical evidence metadata.
2. Dashboard remains a read-only projection. It may request an export from an authorized backend service, but it must not write lifecycle state or become the canonical record store.
3. Binary files may live in a managed object/file store behind a Storage Adapter (bộ chuyển đổi lưu trữ). Core owns the metadata, authorization, provenance, integrity references and retention policy.
4. Sandbox and local browser storage are not canonical production storage. Browser cache/localStorage may hold temporary UI preferences or drafts only, clearly labelled as local.
5. Existing source artifacts are immutable. New versions create new artifact records; no silent overwrite.
6. No implementation may assume an API route, database schema, storage provider or permission model until the actual Core contract is inspected and verified.

## 3. Storage domain

### 3.1 Stored entities

- **WorkRecord**: stable Work ID, name, owner, lifecycle phase, status and canonical manifest reference.
- **WorkPackageRecord**: WP ID, parent Work ID, owner, reviewer, dependencies, status and output references.
- **EvidenceRecord**: evidence ID, Work/WP association, artifact type, logical filename, media type, byte size, SHA-256 hash, storage reference, producer/AI identity, created timestamp, source environment, verification status and access classification.
- **DecisionRecord**: decision ID, actor, timestamp, reason, scope, outcome and evidence references.
- **AuditEvent**: append-only event ID, actor/service, action, target, timestamp, correlation/idempotency key and outcome.
- **ExportJob**: export ID, requester, scope, format, filter set, creation time, completion state, manifest reference, expiry and audit reference.

### 3.2 Storage classes

| Class | Content | Rule |
|---|---|---|
| Canonical metadata | Work/WP/evidence/decision references | Owned by Core; versioned and auditable |
| Evidence artifacts | Reports, logs, test outputs, patches, screenshots and approved files | Stored through managed storage adapter; immutable by version |
| Temporary export | Generated JSON/CSV/Markdown/archive | Expiring artifact; access-controlled |
| Local draft/cache | Unsaved user draft or UI preference | Non-canonical; never shown as persisted evidence |

### 3.3 Required metadata and integrity

Every persisted artifact must have: stable artifact ID, Work ID, optional WP ID, logical filename, media type, byte size, SHA-256, created_at (UTC), producer, source/environment, version, classification, retention class, verification state and storage reference.

An upload is not considered persisted until the backend confirms the write, returns the artifact reference and a read-after-write check verifies metadata and hash. A client-side success toast is not evidence.

### 3.4 Versioning and lifecycle

- New content creates a new immutable version.
- Replacement is represented by a new version plus a supersedes relationship.
- Deletion is a governed tombstone/retention action, not silent physical deletion.
- Failed or partial writes remain visibly FAILED/PENDING_RECONCILIATION and must be safely retryable.
- Duplicate retries must be idempotent; use a server-issued or validated idempotency key.
- Audit events are append-only; corrections are new events referencing the prior event.

## 4. File export

### 4.1 Supported initial formats

- **JSON**: complete structured data for machine processing, including schema/version and provenance.
- **CSV**: tabular Work/WP/evidence/decision indexes; one CSV per logical table, with UTF-8 encoding.
- **Markdown (.md)**: readable Work dossier containing summary, lifecycle, WP list, blockers, decisions and evidence index.

PDF and ZIP bundles are deferred until a concrete requirement, renderer, packaging contract and security review are approved. Do not advertise unsupported formats.

### 4.2 Export scopes

1. Current Work summary.
2. Selected Work Package.
3. Evidence index for a Work or WP.
4. Full Work dossier (metadata and indexes; binary artifacts are not embedded by default).

An export must clearly state whether it contains metadata only or includes artifact bytes. The initial implementation exports metadata/indexes only.

### 4.3 Export manifest

Each export includes:
- export_id and schema_version;
- generated_at (UTC), requester and authorization context reference;
- Work ID and requested scope;
- selected filters and included record counts;
- source snapshot/version and freshness;
- included file names, media types, sizes and SHA-256 hashes where applicable;
- excluded items and reason (for example restricted or unavailable);
- integrity status and expiry.

### 4.4 Filename convention

Use deterministic, filesystem-safe names:

`ROOM-HOP_<WORK-ID>_<SCOPE>_<YYYYMMDDTHHMMSSZ>_<SCHEMA-VERSION>.<ext>`

Normalize unsafe characters. Do not put personal secrets, credentials or private prompt contents in filenames.

### 4.5 Export security

- Enforce authorization on the server for every requested Work/WP and each restricted evidence item.
- Never trust a client-supplied Work ID, role, permission flag or PASS status as authorization.
- Exclude API keys, access tokens, passwords, private credentials and secrets from exports.
- Respect classification, retention and user access policy.
- Use short-lived download links or authenticated streaming; do not make private evidence publicly addressable.
- Record export request, decision, completion/failure and download event in the audit trail.
- Escape spreadsheet formula-leading values in CSV (for example =, +, - and @) to prevent formula injection.
- Validate filters, media types, file sizes and output encoding.

## 5. UI behavior

Dashboard may expose:
- **Lưu bằng chứng** (Save evidence): available only where an authorized upload workflow exists; shows pending, persisted, failed and reconciliation states.
- **Xuất file** (Export): choose scope and JSON/CSV/Markdown; show record count, source snapshot, excluded items and generation status before download.
- **Lịch sử lưu trữ/xuất** (Storage/export history): show artifact/export ID, actor, timestamp, version, integrity state and status.

If Core/storage/export service is unavailable, show BLOCKED/UNAVAILABLE and preserve the existing read-only dashboard. Never silently save only to browser storage or label a local copy as a canonical backup.

## 6. Logical service boundaries

- Core Work/Lifecycle service: authoritative Work state and decisions.
- Evidence Registry: canonical metadata, provenance, hashes and access classification.
- Storage Adapter: stores and retrieves artifact bytes from an approved backend.
- Export Service: creates authorized, versioned exports from a consistent source snapshot.
- Audit/Event Log: records storage and export actions.
- Dashboard: read-only presentation and user-initiated requests.

These are logical responsibilities, not proof that the services currently exist. Actual endpoint names and schemas must be discovered from Core before implementation.

## 7. Failure and recovery

| Failure | Required behavior |
|---|---|
| Core unavailable | No canonical write/export; show unavailable and preserve last-known snapshot with timestamp |
| Storage write fails | Mark FAILED; retain retry/reconciliation metadata; do not report saved |
| Hash mismatch | Reject artifact; quarantine reference; emit audit event |
| Partial upload | Mark PENDING_RECONCILIATION; retry idempotently or clean up under policy |
| Export generation fails | Mark FAILED with trace ID; allow safe retry |
| Permission denied | Deny without leaking restricted metadata; audit denial |
| Snapshot changes during export | Bind export to one explicit source snapshot/version |
| Expired export | Deny download and require a new export |

## 8. Implementation sequence

1. READ/TRACE: inspect actual Core contracts, evidence registry, authorization and existing file storage.
2. DECIDE: record approved provider, metadata schema, retention, size limits and API contracts.
3. BUILD: implement backend storage adapter and evidence registry integration before UI upload controls.
4. BUILD: implement export service for JSON, CSV and Markdown from a consistent authorized snapshot.
5. BUILD: add Dashboard controls and history view.
6. VERIFY: run authorization, integrity, idempotency, failure, CSV safety, export fidelity and read-after-write tests.
7. HANDOFF: publish evidence, known limitations and operational procedures.

## 9. Release gates

Do not mark this capability DONE/PASS until:
- Core authority and actual API contracts are verified;
- storage provider and retention policy are approved;
- authorization is enforced server-side;
- persisted artifacts pass read-after-write and SHA-256 checks;
- exports match the selected source snapshot and pass schema/content checks;
- secrets and restricted records are excluded;
- audit events are present;
- independent tests pass.

Current status: **DESIGN ONLY — implementation and runtime verification pending**.

---
Maintainer: Xu (AI-01)
Final authority: Vinh (Product Owner)
