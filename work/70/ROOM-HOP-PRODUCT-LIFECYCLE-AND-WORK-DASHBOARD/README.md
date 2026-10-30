# WORK 70 — ROOM-HOP WORK MASTER STANDARD
Version: 1.1 | Date: 2026-10-30 | Status: ACTIVE / DESIGN BASELINE

Work 70 defines the reusable product lifecycle standard, Work Package (WP — gói thi công) model, evidence/gate rules and per-Work Dashboard reference for ROOM-HOP. It is a master standard and reference product, not proof that existing Works have migrated or Core integration is live.

## Canonical Work structure
```
WORK-<id>-<name>/
├── 00_ROOT/
├── 01_DISCOVER/
├── 02_DEFINE/
├── 03_ARCHITECT/
├── 04_PLAN/
├── 05_BUILD/
│   ├── 00_ROOT/
│   ├── 01_ORIGINAL/
│   ├── 02_EXTENSION/
│   ├── 03_ARCHITECTURE/
│   ├── 04_CODE/
│   ├── 05_TEST/
│   ├── 06_EVIDENCE/
│   ├── 07_RELEASE/
│   └── 10_AI_DEBUG_HANDOFF/
├── 06_VERIFY/
├── 06_EVIDENCE/
├── 07_ACCEPT/
├── 08_RELEASE/
├── 09_OPERATE/
└── DASHBOARD/
```

The nine 05_BUILD child directories are fixed engineering work areas, not another lifecycle and not per-WP folder trees. WPs are logical records in 05_BUILD/00_ROOT/BUILD_REGISTER.md validated by WORK_PACKAGE.schema.json.

Top-level 06_EVIDENCE is the cross-phase evidence index; 05_BUILD/06_EVIDENCE is build evidence staging.

## Lifecycle
01_DISCOVER → 02_DEFINE → 03_ARCHITECT → 04_PLAN → 05_BUILD → 06_VERIFY → 07_ACCEPT → 08_RELEASE → 09_OPERATE.
A phase becomes DONE only after its exit gate is PASS. Progress and gate readiness are separate.

## Authority and system boundaries
Vinh is Product Owner/final authority. Xu/AI-01 orchestrates end-to-end within approved scope. ROOM-HOP Core is the intended source of truth for identity, permissions, lifecycle state, decisions and evidence metadata. Dashboard is read-only. AI providers are replaceable adapters. Sandbox/local JSON are not production truth.

## Truth rules
No evidence, no PASS. UNKNOWN is not PASS. Missing/stale/conflicting evidence blocks PASS. WAIVED requires authorized approver, rationale, scope, expiry/review and accepted risk. File creation/readback does not prove runtime correctness.

## Storage and export
Core remains the Single Source of Truth. Artifacts are immutable/versioned with provenance and SHA-256. Initial export design supports JSON, CSV and Markdown metadata/indexes. PDF/ZIP are deferred. No secrets in exports. The implementation is not yet verified.

## Migration and reuse
New Works use this exact structure and standard version. Existing Works require inventory, mapping, backup/checksum, dry run, owner approval, migration log, reconciliation and rollback. Do not modify Work 10/15/28 or bulk-migrate without separate approval.

## Current truth
ACTIVE / DESIGN BASELINE. Dashboard reads a local snapshot. Core API, persistent storage, export backend, independent QE, browser E2E and release are NOT VERIFIED. No existing Work is migrated.
