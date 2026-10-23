# Work 10 — COMPUTER AGENT

Sandbox handoff from ROOM-HOP Work 10 on 2026-10-06.

## Source of truth
This branch is a source handoff from the shared Work 10 Sandbox. Qe Coder may continue implementation here.

## Current status
- Specification: LOCKED
- Agent contracts/runtime: IMPLEMENTED + HARDENED
- Real Playwright/Chromium adapter: IMPLEMENTED
- Offline contract tests: FULL COVER
- Host real-browser E2E: NOT YET VERIFIED
- Release: NOT READY until host E2E evidence exists

## Boundary
Work 10 is independent. Do NOT integrate ROOM-HOP runtime into this implementation at this stage. Work 092 is UX reference only.

## Next gate
Run real Chromium/Playwright E2E on the available host, persist evidence, self-fix/retest any failures, and only then claim PASS.
