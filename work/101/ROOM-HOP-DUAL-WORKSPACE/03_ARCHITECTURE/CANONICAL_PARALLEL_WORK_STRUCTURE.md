# Canonical Work Folder Structure

Every Work lives under `work/<ID>/` in the shared repository. Work 101's canonical root is `work/101/ROOM-HOP-DUAL-WORKSPACE/`. Do not scatter Work artifacts at repository root.

## Required structure
- `00_ROOT/` — manifest, context and sync target.
- `01_ORIGINAL/` — source requirements.
- `02_EXTENSION/` — approved scope extensions.
- `03_ARCHITECTURE/` — architecture, sync contracts and ADRs.
- `04_CODE/` — implementation.
- `05_TEST/` — unit, contract and E2E acceptance tests.
- `06_EVIDENCE/` — logs, reports, hashes and verification evidence.
- `07_RELEASE/` — release notes and handoff.
- `08_DASHBOARD/` — canonical Dashboard UI and data contract.
- `09_DASHBOARD_PREVIEW/` — separate static preview and visual review.

Sandbox and GitHub use the same relative paths below the Work root. Structural parity and content-digest parity are checked separately. Exclude `desktop.ini`, temporary files, caches, secrets, runtime databases and logs. Never use last-write-wins or silently delete destination-only files. Divergent same-path edits become `CONFLICT_PENDING`.

Dedicated branch: `work/101-room-hop-dual-workspace`; frozen baseline: `d7c90d9d31062d389810808e43dfdd19d7711b75`. Target identification does not authorize routine sync writes. Integration, merge and release require Vinh's explicit approval bound to operation ID, diff digest, destination branch and base revision.

Folder creation/read-back does not prove tests, browser runtime, synchronization or E2E. Missing evidence remains NOT VERIFIED.
