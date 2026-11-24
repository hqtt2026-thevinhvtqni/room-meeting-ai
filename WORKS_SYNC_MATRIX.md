# ROOM-HOP Common GitHub Work Roots — Reconciliation Register

Date: 2026-10-28 (UTC+7)
Owner: Co — ROOM-HOP AI coder assistant
Repository: `hqtt2026-thevinhvtqni/room-meeting-ai`
Branch: `work/missing-work-roots-20261028`
Base: `main`
Status: IN PROGRESS — WORK 15 PARTIAL SOURCE SYNC VERIFIED; FULL SYSTEM SYNC NOT COMPLETE

## Scope

The Sandbox inventory currently lists 53 Work IDs. GitHub root listing on `main` returned 60 top-level entries and only numeric Work directories `10/` and `30/`. This indicates that most Work IDs do not have a same-numbered landing directory at the root of this repository; it does **not** mean their source is absent from GitHub, because several have separate repositories and/or work branches.

## Registration entries added in this branch

| Work | Common location | Sandbox evidence | Registration status | Full source sync |
|---|---|---|---|---|
| 15 — WEBSITE-BUILDER | `15/WEBSITE-BUILDER/` | Work 15 tree exists; `WEBSITE-BUILDER/WORK.md` readback 607 bytes; manifest_exists=false | Landing entry + 21 files content-equality verified | PARTIAL; remaining tree not yet copied |
| 98 — ONT care | `98/ONT-CARE/README.md` | Work 98 tree exists; `WORK_98_README.md` readback 1,261 bytes; manifest_exists=false | Landing entry added | NOT DONE; canonical root unresolved |

## Known root folders already present on main

- `10/COMPUTER-AGENT/`
- `30/GPT-AUTONOMOUS-BUILD-TEAM/`

## Rules for subsequent sync

- Do not write directly to `main`; use this branch and a PR.
- Do not infer source equivalence from a branch name or Sandbox listing.
- Do not create manifests for Work 15 or 98 until canonical roots and GitHub source have been inspected.
- Preserve locked contracts, tests, logs, screenshots, release/freeze packages and duplicate-looking roots.
- Work 200 trading logic/live execution/risk limits/frozen package are out of scope.
- Core `:8000` must never be installed, created or moved into Sandbox.
- Keep PR #27 open and do not merge it as part of this work.

## Current blockers

1. Complete per-Work GitHub repository/branch/commit mapping for all 53 Sandbox Works.
2. Transfer missing source files to common root folders only after identifying canonical source and checking for duplicates.
3. Independently verify paths and content hashes after every transfer.
4. Record each Work as `REGISTERED`, `SOURCE SYNC VERIFIED`, or `BLOCKED`; these states are not interchangeable.


## Work 15 source transfer — 2026-10-28

**Status: PARTIAL SOURCE SYNC VERIFIED** (not full Work sync, not acceptance PASS).

The following 21 text/source files were copied from Sandbox Work 15 and independently fetched from the same GitHub branch. Every source string compared equal to the GitHub readback:

1. `WEBSITE-BUILDER/README.md`
2. `WEBSITE-BUILDER/WORK.md`
3. `WEBSITE-BUILDER/docs/ARCHITECTURE.md`
4. `WEBSITE-BUILDER/docs/REQUIREMENTS.md`
5. `WEBSITE-BUILDER/docs/UX.md`
6. `WEBSITE-BUILDER/docs/E2E.md`
7. `WEBSITE-BUILDER/docs/WORK_STRUCTURE_STANDARD.md`
8. `WEBSITE-BUILDER/src/frontend/roomhop/TODO.md`
9. `WEBSITE-BUILDER/src/frontend/roomhop/app.config.ts`
10. `WEBSITE-BUILDER/src/frontend/roomhop/index.html`
11. `WEBSITE-BUILDER/src/frontend/roomhop/manus-routes.json`
12. `WEBSITE-BUILDER/src/frontend/roomhop/plan.md`
13. `WEBSITE-BUILDER/src/frontend/roomhop/public/manus-routes.json`
14. `WEBSITE-BUILDER/src/frontend/roomhop/roomhop-logo.svg`
15. `WEBSITE-BUILDER/src/frontend/roomhop/script.js`
16. `WEBSITE-BUILDER/src/frontend/roomhop/styles.css`
17. `WEBSITE-BUILDER/scripts/e2e.ps1`
18. `WEBSITE-BUILDER/scripts/start.ps1`
19. `WEBSITE-BUILDER/scripts/test.ps1`

Additional files `WEBSITE-BUILDER/decisions/DECISIONS.md` and `WEBSITE-BUILDER/evidence/reports/AI_DEBUG_HANDOFF_README.md` were also copied and read back successfully. The common-root index `15/README.md` was also created. The project files are located under `15/WEBSITE-BUILDER/`, matching the numeric Work-root pattern used by existing `10/` and `30/` entries.

Not yet copied: all other files/directories in Work 15, including backend/shared trees and test directories. These remain **NOT SYNCED** until individually inventoried and transferred. No tests or runtime were executed as part of this file transfer.

## Work 98 status after source review

- Common-root landing entry exists at `98/ONT-CARE/README.md` on this branch and has been read back from GitHub.
- Sandbox Work 98 still reports `manifest_exists=false`; do not create a manifest in this pass.
- The existing GitHub branch `work/98-ont-care` is accessible, but its top-level listing resembles the general `room-meeting-ai` repository root and does not establish canonical Work 98 source equivalence. The full Work 98 project source remains **NOT SYNCED / BLOCKED FOR CANONICAL ROOT MAPPING**.

## PR / merge state

- PR #30: open, draft, unmerged; branch `work/missing-work-roots-20261028` targeting `main`.
- No direct writes to `main`.
- PR #27 remains out of scope and must not be merged.


20. `WEBSITE-BUILDER/decisions/DECISIONS.md`
21. `WEBSITE-BUILDER/evidence/reports/AI_DEBUG_HANDOFF_README.md`


### Candidate repository review for Work 98

- The separate GitHub repository `hqtt2026-thevinhvtqni/004.ont-customer-protection-platform` exists and its README describes an ONT/customer protection platform with mock customer data and three apps.
- This is a plausible related project, but the inspected README alone does not prove it is the canonical GitHub counterpart of Sandbox Work 98. No source files were copied from this repository into Work 98, to avoid mixing projects before the mapping is confirmed.
