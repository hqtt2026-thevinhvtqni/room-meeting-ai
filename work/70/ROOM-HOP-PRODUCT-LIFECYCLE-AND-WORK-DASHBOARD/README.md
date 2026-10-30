# WORK 70 — ROOM-HOP WORK MASTER STANDARD
- **STT / Document ID:** DOC-037
- **Priority:** P3
- **Read order:** 37
- **Depends on:** DOC-001; DOC-033; DOC-036
- **Status:** ACTIVE
- **Version / Updated:** 1.2 / 2026-10-30

## 1. Purpose and product boundary
Work 70 defines the reusable product lifecycle standard, Work Package (WP — gói thi công) model, evidence/gate rules, documentation/storage standard and per-Work Dashboard reference for ROOM-HOP. It is a master standard and reference product. It does not mean existing Works have been migrated or that Core integration is live.

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

The nine child directories under 05_BUILD are fixed navigation/mapping/engineering coordination areas. They are not a second product lifecycle and do not own canonical original documents or product source code.

## 3. Four official Work records
Every Work maintains three required records and one conditional design record:
1. BIÊN BẢN — official minutes and agreement register.
2. KẾ HOẠCH — scope, milestones, WPs, owners, dependencies and acceptance criteria.
3. NHẬT KÝ THI CÔNG — chronological record of actual execution and handoffs.
4. BẢN VẼ / MÔ HÌNH SẢN PHẨM — when the product requires architecture, workflows, data models, UI, technical drawings or 3D models.

Canonical paths are declared in each Work Manifest and Document Register. Do not create duplicate files for the same record.

## 4. Source and storage ownership
- Work root owns official lifecycle records, approved requirements, plans, drawings/models, acceptance/release records and cross-phase evidence index.
- Product source code and test source live in the canonical source repository/path explicitly declared by the Work Manifest.
- Sandbox is a working/execution environment, not an independent source of truth.
- 05_BUILD is a mapping layer: it links WPs and engineering areas to canonical source artifacts using stable IDs, repository/path, exact branch/commit/version and hashes where available.
- Temporary copies required by tools must be labelled TEMPORARY and traceable to the source version.
- A file's presence in 05_BUILD does not make it canonical.

## 5. Work Package model
A WP is a logical, trackable delivery record, not a separate lifecycle and not a mandatory directory tree. WP planning is owned at Work level in 04_PLAN. The 05_BUILD mapping register links each WP to engineering areas, canonical source files and evidence. Legacy Build Register files under 05_BUILD are migration candidates until reconciled; they are not a second canonical plan.

## 6. Evidence model
Top-level 06_EVIDENCE is the cross-phase evidence index for the Work. 05_BUILD/06_EVIDENCE may stage temporary build evidence before it is registered at Work level. Evidence records retain provenance, timestamp, source, integrity hash and verification state. Creating a file is not equivalent to verifying its claim.

## 7. Lifecycle
01_DISCOVER → 02_DEFINE → 03_ARCHITECT → 04_PLAN → 05_BUILD → 06_VERIFY → 07_ACCEPT → 08_RELEASE → 09_OPERATE.

Each Work has exactly one current phase. A phase becomes DONE only after its exit gate is PASS. Work progress and gate readiness are separate.

## 8. Authority and system boundaries
- Vinh: Product Owner and final decision authority.
- Xu / AI-01: end-to-end lifecycle orchestration and routine decisions within approved scope.
- Implementer: owns submitted changes and records exact paths/commits.
- Independent QE/reviewer: verifies implementation and evidence; does not self-certify.
- ROOM-HOP Core: intended authoritative source for identity, permissions, lifecycle state, decisions and canonical evidence metadata.
- Dashboard: read-only projection; never mutates authoritative state.
- Sandbox/local JSON: design/build artifacts or snapshots, not production truth.

## 9. Status and truth rules
Work/phase/WP: NOT_STARTED, PLANNED, ACTIVE, BLOCKED, DONE, CANCELLED (WP may additionally use DRAFT, READY, IN_PROGRESS, IN_REVIEW).
Gate: NOT_READY, PENDING, PASS, FAIL, WAIVED.
Evidence: MISSING, RECORDED, VERIFIED, REJECTED.
UNKNOWN is not PASS. Missing, stale, conflicting or unverifiable evidence blocks PASS. WAIVED requires authorized approver, rationale, scope, expiry/review and accepted risk.

## 10. Standard delivery loop
READ → TRACE → ANALYZE → DECIDE → ARCHITECT → PLAN → BUILD → INTEGRATE → VERIFY → DEBUG → REGRESSION → ACCEPTANCE PREPARATION → HANDOFF.
Proceed end-to-end without routine micro-approvals. Stop only for missing authority, irreversible action, material scope/security/cost risk, required credentials/payment or an external blocker.

## 11. Migration and reuse
New Works are instantiated from this exact directory structure and current standard version. Existing Works require inventory, mapping, backup/checksum, dry run, independent review, owner approval, migration log, reconciliation, verification and rollback plan. Never bulk-migrate, renumber, overwrite or delete history silently. Work 10/15/28 remain untouched unless separately authorized.

## 12. Current truth boundary
Work 70 is ACTIVE / DESIGN BASELINE. Dashboard currently reads a local PRODUCT_STATUS.json snapshot. Core API, persistent storage, export service, independent QE, browser E2E and release are not verified. No existing Work is migrated. Do not claim CORE LIVE, RELEASED or overall PASS until evidence is attached and reviewed.
