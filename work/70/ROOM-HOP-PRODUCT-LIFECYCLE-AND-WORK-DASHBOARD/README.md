# WORK 70 — ROOM-HOP WORK MASTER STANDARD
Version: 1.1 | Date: 2026-10-30 | Status: ACTIVE / DESIGN BASELINE

## 1. Purpose and product boundary
Work 70 defines the reusable product lifecycle standard, Work Package (WP — gói thi công) model, evidence/gate rules and per-Work Dashboard reference for ROOM-HOP. It is a master standard and reference product. It does not mean existing Works have been migrated or that Core integration is live.

## 2. Canonical Work structure
Every Work uses exactly these top-level directories:

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

The nine child directories under 05_BUILD are the approved engineering workspace layout. They are not a second product lifecycle and must not be replaced with per-WP folder trees. Preserve this exact layout for the Work 70 build branch.

## 3. Work Package model
A WP is a logical, trackable delivery record, not a separate lifecycle and not a mandatory directory tree. The canonical machine-readable register is `05_BUILD/00_ROOT/BUILD_REGISTER.json`, validated by `BUILD_REGISTER.schema.json` and `WORK_PACKAGE.schema.json`; `BUILD_REGISTER.md` is its human-readable mirror. A WP references its branch, assigned build area(s), owner, independent reviewer, dependencies, acceptance criteria, tests and evidence.

## 4. Evidence model
Top-level `06_EVIDENCE` is the cross-phase evidence index for the Work. `05_BUILD/06_EVIDENCE` holds evidence produced by build activities before it is indexed at Work level. Evidence records must retain provenance, timestamp, source, integrity hash and verification state. Creating a file is not equivalent to verifying its claim.

## 5. Lifecycle
01_DISCOVER → 02_DEFINE → 03_ARCHITECT → 04_PLAN → 05_BUILD → 06_VERIFY → 07_ACCEPT → 08_RELEASE → 09_OPERATE.

Each Work has exactly one current phase. A phase becomes DONE only after its exit gate is PASS. Work progress and gate readiness are separate.

## 6. Authority and system boundaries
- Vinh: Product Owner and final decision authority.
- Xu / AI-01: end-to-end lifecycle orchestration and routine decisions within approved scope.
- Implementer: owns submitted changes and records exact paths/commits.
- Independent QE/reviewer: verifies implementation and evidence; does not self-certify.
- ROOM-HOP Core: intended authoritative source for identity, permissions, lifecycle state, decisions and canonical evidence metadata.
- Dashboard: read-only projection; never mutates authoritative state.
- Storage adapter: stores file bytes only under Core-governed metadata, authorization and retention.
- Sandbox/local JSON: design/build artifacts or snapshots, not production truth.

## 7. Status and truth rules
Work/phase/WP: NOT_STARTED, PLANNED, ACTIVE, BLOCKED, DONE, CANCELLED (WP may additionally use DRAFT, READY, IN_PROGRESS, IN_REVIEW).
Gate: NOT_READY, PENDING, PASS, FAIL, WAIVED.
Evidence: MISSING, RECORDED, VERIFIED, REJECTED.
UNKNOWN is not PASS. Missing, stale, conflicting or unverifiable evidence blocks PASS. WAIVED requires authorized approver, rationale, scope, expiry/review and accepted risk.

## 8. Standard delivery loop
READ → TRACE → ANALYZE → DECIDE → ARCHITECT → PLAN → BUILD → INTEGRATE → VERIFY → DEBUG → REGRESSION → ACCEPTANCE PREPARATION → HANDOFF.
Proceed end-to-end without routine micro-approvals. Stop only for missing authority, irreversible action, material scope/security/cost risk, required credentials/payment or an external blocker.

## 9. Storage and export
Core remains the Single Source of Truth (nguồn dữ liệu chuẩn duy nhất). Evidence artifacts are versioned and immutable; metadata includes stable ID, Work/WP scope, producer, timestamp, source, media type, size, SHA-256, classification and retention. Initial export formats are JSON, CSV and Markdown metadata/indexes. PDF/ZIP are deferred. No secrets in artifacts or exports. Storage/export design is documented under 05_BUILD/03_ARCHITECTURE and tests under 05_BUILD/05_TEST; both are design-only until integrated tests pass.

## 10. Migration and reuse
New Works are instantiated from this exact directory structure and current standard version. Existing Works require inventory, mapping, backup/checksum, dry run, owner approval, migration log, reconciliation, verification and rollback plan. Never bulk-migrate, renumber, overwrite or delete history silently. Work 10/15/28 remain untouched unless separately authorized.

## 11. Current truth boundary
Work 70 is ACTIVE / DESIGN BASELINE. Dashboard currently reads a local PRODUCT_STATUS.json snapshot. Core API, persistent storage, export service, independent QE, browser E2E and release are not verified. No existing Work is migrated. Do not claim CORE LIVE, RELEASED or overall PASS until evidence is attached and reviewed.
