# 06 — VERIFY / KIỂM CHỨNG
- **STT / Document ID:** DOC-015
- **Priority:** P1
- **Read order:** 17
- **Depends on:** DOC-008; DOC-013; DOC-014; DOC-033; DOC-036
- **Status:** PLANNED — NOT EXECUTED
- **Version / Updated:** 1.1 / 2026-10-30

## Verification domains
1. Structure: canonical top-level folders and nine fixed 05_BUILD mapping/engineering child areas.
2. Governance: Manifest, four official records, authority, version, lifecycle gates and state machine are consistent.
3. Work Packages: Work-level plan is authoritative; 05_BUILD mapping register links WP to canonical engineering artifacts without duplicating plan ownership.
4. Mapping: every mapped artifact resolves to canonical repository/path and exact branch/commit/version; hash matches where available.
5. Evidence: top-level evidence index and schema are valid; build staging is distinct.
6. Dashboard data: PRODUCT_STATUS.json validates against schema; current phase and gate rules are consistent.
7. Dashboard runtime: lifecycle, owners, WPs, blockers, risks, decisions, evidence, source mode and freshness render correctly.
8. Truthfulness: sample/local data is visibly distinct from Core live; errors become UNKNOWN/STALE.
9. Security: no Dashboard write path; server-side authorization for any future storage/export.
10. Core: inspect actual routes/auth before integration; test permission, scope, freshness and failures.
11. Storage/export: integrity, immutability, idempotency, CSV safety, access control and audit.
12. Migration: inventory, mapping, backup/checksum, dry run, explicit approval, reconciliation and rollback.
13. Independent QE: reviewer verifies source, target, exact version, hashes, links and no duplicate canonical owners.

## Current state
Documentation and readback synchronization checks are recorded separately in the Work journal. Full JSON/schema and browser runtime tests remain NOT RUN until executed and evidence is stored. 05_BUILD legacy-file migration remains NOT VERIFIED. Independent QE review remains PENDING. No gate PASS is inferred from file creation or readback.
