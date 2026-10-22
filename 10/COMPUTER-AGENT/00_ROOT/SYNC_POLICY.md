# WORK 10 — SYNC POLICY
Version: 1.0
Date: 2026-10-22

## Single source of truth
- Canonical source for Work 10 code and release history: GitHub branch `work/10-computer-agent-mirror`.
- Sandbox Work 10 (`work_id=10`, root `COMPUTER-AGENT/`) is the execution/test mirror, not an independent source of truth.
- Do not push Sandbox-only changes over GitHub automatically.

## Direction of sync
1. GitHub -> Sandbox before execution/testing: fetch the canonical branch files, write to the matching Sandbox paths, then read-after-write and compare file content/hash where available.
2. Changes made in Sandbox are proposals until reviewed and committed to the canonical GitHub branch. No blind reverse sync.
3. Qc/other contributors must work on `work/10-computer-agent-mirror` (or a dedicated child branch and PR), never directly on `main`.
4. Every sync records source branch, source commit SHA, file list, write result, read-after-write result, and test status.
5. Never label PASS without fresh, reproducible test evidence. Standalone browser tests do not prove integrated ROOM-HOP E2E.

## Current baseline / limitation
- Last verified repository commit on main: `0958c723a76d0f3e878f1e13883860b9b768de00`.
- The Work 10 files currently retrievable from the canonical branch match the older implementation; commit `c3a465e` and the claimed P0/P1 changes are not present in the accessible branch snapshot yet.
- Therefore this policy establishes the sync direction, but does not claim that the newer P0/P1 implementation has been recovered or synced.

## Handoff gate
Before Qc continues, verify the canonical branch contains the intended changes; sync that exact commit into Sandbox; read-after-write; run offline tests; then run integrated ROOM-HOP E2E when available.
