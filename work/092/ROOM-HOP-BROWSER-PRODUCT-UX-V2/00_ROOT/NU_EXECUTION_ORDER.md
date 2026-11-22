# WORK 092 — ONE-SHOT EXECUTION ORDER (2026-11-22)

Execute end to end without intermediate ACK requests, stage-by-stage questions, or pauses for another agent dispatch. Review source and evidence; make scoped fixes; run available tests; handle failures; synchronize source, evidence, and CI to GitHub; then prepare handoff.

## Binding boundaries

1. Scope is Work 092 only. Do not alter ROOM-HOP Core :8000, MCP :8020, Work 91, Opera or external services.
2. Keep the product **MOCK ONLY**: no claim of real browser agent, website, Internet, external API or real screenshot artifact.
3. Distinguish Work Sandbox direct execution, Cloud Sandbox mirror, Chromium E2E and GitHub Actions. Do not treat one as evidence of another.
4. Do not mark DONE/PASS globally absent real evidence. Preserve PARTIAL/BLOCKED where requirements remain unverified.
5. Identify executor accurately; an ACK from the current Manus session is not evidence of independent Nu dispatch.
6. Xu retains independent final review and acceptance authority.

## Mission

Complete Browser Agent V2 source and regression tests, repair in-scope failures, sync to a separate GitHub branch, add/execute CI, preserve browser screenshots/test artifacts with provenance, and update the manifest, minutes, error log, journal, evidence index and acceptance report. Report only after completion or a genuine blocker.
