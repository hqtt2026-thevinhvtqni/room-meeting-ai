# AI Debug Handoff — Work 15

This file documents the debugging handoff lifecycle using the project's existing `evidence/` tree; it does not imply a new implementation or release.

1. Preserve incoming reports, logs, screenshots, and proposed patches unchanged.
2. Review the relevant source and record scope, risks, and reviewer findings before applying any patch.
3. Keep patch candidates separate from applied changes.
4. Store reproducible commands, raw test output, and validation evidence under `evidence/`.
5. Record decisions with AI/person identity, title, date/time, rationale, and outcome.

Safety: preserve existing project folders and contracts; read before write and verify by readback. No PASS without evidence. Sandbox does not prove GitHub synchronization. Never place Core :8000 inside Sandbox. Keep GitHub changes auditable on a work branch/PR; do not merge or release without applicable authorization.
