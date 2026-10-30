# WORK 70 — VERIFICATION CHECKLIST
Status: OPEN — NOT YET EXECUTED

## A. Structure and governance
- [ ] Canonical top-level structure matches 00_ROOT/WORK_MANIFEST.md.
- [ ] All nine fixed 05_BUILD child directories exist.
- [ ] No duplicate/competing WP folder structure is populated.
- [ ] Manifest, README, version and authority agree.
- [ ] Nine lifecycle phases and gate matrix agree.

## B. WP and evidence
- [ ] BUILD_REGISTER validates against WORK_PACKAGE.schema.json.
- [ ] Each WP has owner, independent reviewer, objective, build areas, dependencies and acceptance criteria.
- [ ] Top-level 06_EVIDENCE register/schema validate.
- [ ] Evidence states distinguish RECORDED from VERIFIED.
- [ ] No secrets or private credentials are present.

## C. Dashboard data and runtime
- [ ] PRODUCT_STATUS.json parses and validates against schema.
- [ ] Exactly nine phases exist with valid status, gate, owner and evidence_refs.
- [ ] Only one current phase is selected; no phase advances without predecessor gate PASS.
- [ ] Work Package status vocabulary matches schema.
- [ ] Blockers, risks and decisions_needed fields are present.
- [ ] Dashboard displays owner, WP, blockers, risks, decisions, evidence, source mode and freshness.
- [ ] LOCAL SNAPSHOT / SAMPLE / CORE LIVE are distinguished correctly.
- [ ] Network/data errors show UNKNOWN/STALE, never fabricated PASS.
- [ ] Dashboard has no authoritative write path.
- [ ] Responsive and keyboard behavior checked on mobile and desktop.

## D. Core, storage and export
- [ ] Actual Core endpoints and auth contracts inspected before configuration.
- [ ] 401/403/404/429/5xx/timeout and Work scoping tested.
- [ ] No secret in client bundle or logs.
- [ ] Storage read-after-write and SHA-256 integrity pass.
- [ ] Immutable versioning and idempotent retries pass.
- [ ] JSON/CSV/Markdown exports match one source snapshot.
- [ ] CSV formula injection protection passes.
- [ ] Restricted data/secret exclusion and export audit pass.

## E. Migration
- [ ] Inventory and mapping approved per Work.
- [ ] Backup/checksum before change.
- [ ] Dry run has no source writes.
- [ ] Work IDs, branches, commits, issues, evidence and history preserved.
- [ ] Reconciliation and rollback tested.

## F. Gate and result
G0 remains PENDING until independent reviewer verifies identity, owner, manifest and scope. All unchecked items remain NOT_RUN. No overall PASS until evidence and independent review are attached.
