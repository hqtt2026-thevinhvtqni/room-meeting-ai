# PRODUCT REQUIREMENTS — WORK 70 / VERSION 1.1
- **STT / Document ID:** DOC-008
- **Priority:** P1
- **Read order:** 12
- **Depends on:** DOC-007
- **Status:** ACTIVE
- **Version / Updated:** 1.0 / 2026-10-30

## Product objective
Provide a reusable, auditable product lifecycle standard for ROOM-HOP Works, with one consistent Work manifest, controlled build workspace, WP registry, evidence/gate model, read-only Dashboard, and future Core-backed storage/export.

## Functional requirements
- FR-01: Every Work has a stable ID, owner, standard version and manifest.
- FR-02: Every Work has exactly one current lifecycle phase across the nine defined phases.
- FR-03: Every phase has owner, entry/exit criteria, status, gate and evidence references.
- FR-04: 05_BUILD has the nine canonical child directories defined in the Work standard.
- FR-05: WPs are records in BUILD_REGISTER and validate against WORK_PACKAGE.schema.json; they reference build areas and evidence.
- FR-06: Every Work has a Dashboard generated from a common template.
- FR-07: Dashboard exposes phase/gate state, WPs, blockers, risks, decisions, evidence and freshness.
- FR-08: Dashboard is read-only and cannot mutate authoritative state.
- FR-09: Evidence has provenance, integrity, verification state and access classification.
- FR-10: Existing Work IDs, links, commits, evidence and history are preserved during approved migration.
- FR-11: Core is the authoritative source; local snapshots are clearly labelled.
- FR-12: Storage supports immutable versioned artifacts and read-after-write integrity checks when implemented.
- FR-13: Export supports authorized JSON, CSV and Markdown metadata/indexes from a consistent snapshot when implemented.
- FR-14: Storage/export actions are audited and secrets/restricted data are excluded.

## Quality requirements
Traceability, server-side authorization, fail-closed behavior, idempotency, immutable evidence, accessibility, responsive UI, data freshness, portability, auditability and recoverability.

## Acceptance criteria
- AC-01: Canonical top-level and 05_BUILD child structures are consistent across manifest, README and Sandbox.
- AC-02: Nine lifecycle phases and gates have one consistent definition.
- AC-03: WP register and schema validate the same records.
- AC-04: Evidence registry supports provenance, hash and verification status.
- AC-05: Dashboard JSON validates against schema and renders source mode accurately.
- AC-06: Dashboard has no authoritative write path and displays UNKNOWN/STALE safely.
- AC-07: Core read API is verified before live integration is claimed.
- AC-08: Storage/export design has security, integrity, retention and failure contracts.
- AC-09: Storage/export implementation passes independent tests before being marked available.
- AC-10: Migration preserves IDs/history and requires per-Work approval.
