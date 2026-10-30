# WORK 70 — BUILD MAPPING REGISTER
- **STT / Document ID:** DOC-036
- **Priority:** P1
- **Read order:** 18
- **Depends on:** DOC-001; DOC-003; DOC-033
- **Status:** ACTIVE / MIGRATION IN PROGRESS
- **Version / Updated:** 1.0 / 2026-10-30

## 1. Purpose
This register is the navigation and mapping index for the 05_BUILD layer. It does not own original documents, plans, drawings, source code, tests, or canonical evidence. It records where each canonical artifact lives and which exact version the build workflow references.

## 2. Mapping rules
- Canonical target is the source of truth; this register is only a pointer.
- Every verified mapping must include canonical repository, relative path/URI and exact branch + commit/version. Record SHA-256 when available.
- A missing target, unknown commit or unverified content means NOT VERIFIED; never infer a target from a similar filename.
- Existing files remain untouched until classification and migration are completed.
- Temporary copies must be labelled TEMPORARY and identify their source version.
- 05_BUILD branch work/70/05-build is a mapping/coordination branch, not the canonical product source repository.

## 3. Current inventory and classification

| Build item | Current branch path | Classification | Intended canonical owner/target | Exact target/version | Status / next action |
|---|---|---|---|---|---|
| Build Register Markdown | 00_ROOT/BUILD_REGISTER.md | CANONICAL CANDIDATE | 04_PLAN — Work Package plan/register | NOT ESTABLISHED | Compare WP data with roadmap; decide canonical WP registry path before moving or rewriting |
| Build Register JSON | 00_ROOT/BUILD_REGISTER.json | CANONICAL CANDIDATE | 04_PLAN — Work Package plan/register | NOT ESTABLISHED | Preserve current data; validate and reconcile against approved plan |
| Build Register schema | 00_ROOT/BUILD_REGISTER.schema.json | CANONICAL CANDIDATE | 03_ARCHITECT — Work Package data contract | NOT ESTABLISHED | Determine canonical schema path and references |
| Work Package schema | 00_ROOT/WORK_PACKAGE.schema.json | CANONICAL CANDIDATE | 03_ARCHITECT — Work Package data contract | NOT ESTABLISHED | Determine canonical schema path and references |
| AI Participants & Token Usage | 00_ROOT/AI_PARTICIPANTS_AND_TOKEN_USAGE.md | LEGACY / REFERENCE | 00_ROOT governance reference, if still needed | NOT ESTABLISHED | Audit factual accuracy and decide retain/archive; do not treat roster as participation proof |
| Storage & Export Architecture | 03_ARCHITECTURE/STORAGE_AND_EXPORT_ARCHITECTURE.md | CANONICAL CANDIDATE | 03_ARCHITECT — architecture/design | NOT ESTABLISHED | Compare with top-level architecture; reconcile into one canonical document |
| Core Capability Gap Assessment | 03_ARCHITECTURE/CORE_CAPABILITY_GAP_ASSESSMENT.md | CANONICAL CANDIDATE | 03_ARCHITECT or 06_VERIFY — assessment/evidence | NOT ESTABLISHED | Verify source commit freshness and choose one canonical home |
| Storage & Export Acceptance | 05_TEST/STORAGE_AND_EXPORT_ACCEPTANCE.md | CANONICAL CANDIDATE | 06_VERIFY — test/acceptance plan | NOT ESTABLISHED | Reconcile with Work verification plan; do not treat planned tests as executed |
| Work 70 Session Log | 10_AI_DEBUG_HANDOFF/WORK70_SESSION_LOG_20261030.md | LEGACY / HISTORICAL | 00_ROOT/NHAT_KY_THI_CONG.md | Journal reference only; original session detail retained here | Keep as historical detail; link relevant events from Work-wide journal |

Directory marker files (.gitkeep) are structural placeholders, not canonical product artifacts and need no artifact mapping.

## 4. Current migration state
- 05_BUILD is designated as a mapping/engineering coordination layer.
- This inventory is an initial classification, not proof that the target documents have been migrated.
- No legacy file has been moved, deleted or rewritten as part of this register creation.
- All CANONICAL CANDIDATE items remain UNVERIFIED until their target path, exact content/version and ownership are reconciled.
- Work 70 status for 05_BUILD normalization: ACTIVE / MIGRATION NOT VERIFIED.

## 5. Next controlled actions
1. Compare each candidate with the current Work-root records and avoid duplicate content.
2. Decide canonical path and version for each candidate.
3. Migrate only after a documented plan and verified backup/history.
4. Replace each migrated candidate in 05_BUILD with a mapping entry, not a second copy.
5. Verify branch and Sandbox readback, target version/hash and Document Register consistency.
6. Obtain independent QE review before marking the mapping migration PASS.

