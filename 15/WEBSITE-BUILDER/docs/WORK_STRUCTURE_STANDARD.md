# Work Structure Standard — Work 15

This document maps the shared ROOM-HOP Work structure onto the existing WEBSITE-BUILDER project; it does not replace its architecture or current folders.

- Preserve `README.md`, `WORK.md`, `docs/`, `decisions/`, `src/`, `tests/`, `scripts/`, and `evidence/` as the project-specific source of truth.
- Keep operational status separate from preview/demo data. Any mock data must be labelled `PREVIEW_ONLY`.
- Keep debug handoffs in `evidence/reports/` or add `10_AI_DEBUG_HANDOFF/` only when it does not conflict with established project paths; preserve original logs and patches.
- Pin repository, branch, and commit before source changes. Read before write and verify every write by readback.
- Sandbox is isolated; it does not prove GitHub synchronization. Never place Core :8000 inside Sandbox.
- Never claim PASS without reproducible test output. Separate structure compliance, implementation, test verification, and release status.
- GitHub changes must be auditable on a work branch or PR; do not merge or release without applicable authorization.

Manifest note: the Sandbox inventory did not show a `WORK_MANIFEST.md` at the project root. Do not invent canonical repo/branch/commit metadata; reconcile these fields from the authoritative GitHub Work branch before treating this Work as release-ready.
