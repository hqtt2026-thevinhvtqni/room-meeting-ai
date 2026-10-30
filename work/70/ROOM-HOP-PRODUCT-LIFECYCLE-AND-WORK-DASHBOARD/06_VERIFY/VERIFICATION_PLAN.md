# 06 — VERIFY / KIỂM CHỨNG
Status: PLANNED — NOT EXECUTED

## Verification domains
1. Structure: canonical top-level folders and nine fixed 05_BUILD child folders.
2. Governance: manifest, authority, version, lifecycle gates and state machine are consistent.
3. Work Packages: BUILD_REGISTER validates against WORK_PACKAGE.schema.json; no conflicting WP folder tree.
4. Evidence: top-level evidence index and schema are valid; build staging is distinct.
5. Dashboard data: PRODUCT_STATUS.json validates against schema; current phase and gate rules are consistent.
6. Dashboard runtime: lifecycle, owners, WPs, blockers, risks, decisions, evidence, source mode and freshness render correctly.
7. Truthfulness: sample/local data is visibly distinct from Core live; errors become UNKNOWN/STALE.
8. Security: no Dashboard write path; server-side authorization for any future storage/export.
9. Core: inspect actual routes/auth before integration; test permission, scope, freshness and failures.
10. Storage/export: integrity, immutability, idempotency, CSV safety, access control and audit.
11. Migration: inventory, mapping, backup/checksum, dry run, approval, reconciliation and rollback.

## Current state
Document and structure checks are being consolidated. JSON/schema and browser runtime tests remain NOT_RUN until executed and evidence is stored. Independent QE review remains PENDING. No gate PASS is inferred from file creation or readback.
