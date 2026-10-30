# WORK 70 — BUILD REGISTER
- **STT / Document ID:** DOC-013
- **Priority:** P1
- **Read order:** 17
- **Depends on:** DOC-033; DOC-011
- **Status:** MIGRATION PENDING
- **Version / Updated:** 1.0 / 2026-10-30

Machine-readable source: `BUILD_REGISTER.json`, validated by `BUILD_REGISTER.schema.json` and `WORK_PACKAGE.schema.json`. This Markdown table is the human-readable mirror.

Version: 1.0
Scope: 05_BUILD only. WP records are logical delivery units and reference the fixed build areas.

| WP ID | Title | Objective / output | Owner | Reviewer | Build areas | Dependencies | Acceptance / evidence | Status |
|---|---|---|---|---|---|---|---|---|
| WP-70-01 | Canonical Work standard | Align Work structure, lifecycle, gates and authority | Xu / AI-01 | Qw / AI-05 | 00_ROOT, 03_ARCHITECTURE | None | README, manifest, architecture and gate/state docs agree | IN_PROGRESS |
| WP-70-02 | Work Package registry | Define WP record contract, schema and build area mapping | Xu / AI-01 | Qw / AI-05 | 00_ROOT | WP-70-01 | Register validates against schema; no duplicate WP folder tree | IN_PROGRESS |
| WP-70-03 | Dashboard reference | Validate dashboard data schema, read-only behavior and source labels | Xu / AI-01 | Qw / AI-05 | 03_ARCHITECTURE, 04_CODE, 05_TEST | WP-70-01 | Schema validation, browser test, read-only and UNKNOWN behavior | IN_PROGRESS |
| WP-70-04 | Core read integration | Inspect actual Core routes, auth and freshness; integrate only verified contract | Xu / Core owner TBD | Qw / AI-05 | 03_ARCHITECTURE, 04_CODE, 05_TEST | WP-70-03 | CORE_CAPABILITY_GAP_ASSESSMENT.md; real Work endpoint/E2E evidence still absent | BLOCKED |
| WP-70-05 | Storage and export | Design then implement evidence storage and JSON/CSV/Markdown export | Xu / AI-01 | Qw / AI-05 | 03_ARCHITECTURE, 04_CODE, 05_TEST, 06_EVIDENCE | WP-70-04 | Storage/export architecture exists; implementation and tests NOT_RUN | IN_PROGRESS |
| WP-70-06 | Verification and handoff | Independent regression, acceptance package and handoff | Xu / AI-01 | Qw / AI-05 | 05_TEST, 06_EVIDENCE, 10_AI_DEBUG_HANDOFF | WP-70-01..05 | Independent QE report and release recommendation | PLANNED |

## Register rules
- One WP has one accountable owner and an independent reviewer.
- Build areas are selected from the fixed 05_BUILD child folders.
- Every WP has explicit inputs, outputs, dependencies and acceptance evidence; expand rows or link a WP detail record when needed.
- Status does not advance Work lifecycle automatically.
- A WP is DONE only when acceptance criteria and evidence are verified.
- Never use PASS as a work-progress status; PASS belongs to a gate/test result.
