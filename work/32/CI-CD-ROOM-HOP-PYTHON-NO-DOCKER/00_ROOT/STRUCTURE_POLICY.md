# Structure Policy — Work 32

This policy does not certify implementation or release.

- Preserve the manifest, original request, CI/CD architecture, Python test runtime plans, code, classifier tests, evidence reports, minutes, and release policy. Do not move project-specific files to fit a generic template.
- Record canonical GitHub repository/branch/commit, scope, status, constraints, and acceptance criteria in `WORK_MANIFEST.md` or link to authoritative records.
- Keep `08_DASHBOARD/` operational and evidence-backed; keep `09_DASHBOARD_PREVIEW/` demo-only and label sample data `PREVIEW_ONLY`. Document existing preview locations instead of overwriting them.
- Use `10_AI_DEBUG_HANDOFF/{00_INBOX,01_REVIEW,02_PATCH_CANDIDATES,03_VALIDATION,04_DECISIONS}` for debug lifecycle.
- Sandbox is isolated and does not prove GitHub sync. Never create or install Core `:8000` inside Sandbox.
- Preserve contracts and tests. Review incoming patches before application. Never claim PASS without reproducible commands, exit codes, and evidence; separate structural compliance, implementation verification, CI status, and release readiness.
- GitHub changes must be auditable on a Work branch/PR. Do not merge to `main` or release without applicable governance approval.
