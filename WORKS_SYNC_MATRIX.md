# ROOM-HOP Common GitHub Work Roots — Reconciliation Register

Date: 2026-10-28 (UTC+7)
Owner: Co — ROOM-HOP AI coder assistant
Repository: `hqtt2026-thevinhvtqni/room-meeting-ai`
Branch: `work/missing-work-roots-20261028`
Base: `main`
Status: IN PROGRESS — REGISTRATION CHANGES ONLY; FULL SOURCE SYNC NOT COMPLETE

## Scope

The Sandbox inventory currently lists 53 Work IDs. GitHub root listing on `main` returned 60 top-level entries and only numeric Work directories `10/` and `30/`. This indicates that most Work IDs do not have a same-numbered landing directory at the root of this repository; it does **not** mean their source is absent from GitHub, because several have separate repositories and/or work branches.

## Registration entries added in this branch

| Work | Common location | Sandbox evidence | Registration status | Full source sync |
|---|---|---|---|---|
| 15 — WEBSITE-BUILDER | `15/WEBSITE-BUILDER/README.md` | Work 15 tree exists; `WEBSITE-BUILDER/WORK.md` readback 607 bytes; manifest_exists=false | Landing entry added | NOT DONE |
| 98 — ONT care | `98/ONT-CARE/README.md` | Work 98 tree exists; `WORK_98_README.md` readback 1,261 bytes; manifest_exists=false | Landing entry added | NOT DONE |

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
