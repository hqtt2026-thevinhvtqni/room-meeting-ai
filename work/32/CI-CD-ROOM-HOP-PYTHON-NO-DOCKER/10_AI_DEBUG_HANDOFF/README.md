# AI Debug Handoff — Work 32

- `00_INBOX/`: raw incident reports, logs, reproductions, proposed patches (untrusted).
- `01_REVIEW/`: root cause, impact, independent review.
- `02_PATCH_CANDIDATES/`: reviewed changes awaiting application.
- `03_VALIDATION/`: exact commands, environment, exit codes, test/CI results, readback evidence.
- `04_DECISIONS/`: decision, role/owner, timestamp, rationale, remaining risk.

Preserve existing source, tests, CI gate matrix, baseline reports, meeting records, and release policy. Keep Sandbox evidence distinct from GitHub/CI evidence. Do not weaken gates or mark PASS without reproducible proof. This guide is not release approval.
