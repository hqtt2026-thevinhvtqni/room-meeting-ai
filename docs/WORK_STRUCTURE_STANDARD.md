# HQTT AI — Work Structure and Sandbox Governance v1.0
Effective: 2026-10-28
Scope: all existing and future ROOM-HOP Works in Sandbox and GitHub.

## Required zones
- 08_DASHBOARD/: operational dashboard from actual runtime/API state; never hard-code PASS.
- 09_DASHBOARD_PREVIEW/: standalone visual preview; label sample/mock data; never treat preview as live verification.
- 10_AI_DEBUG_HANDOFF/00_INBOX/<AI>/<run-id>/: preserve complete incoming debug package unchanged.
- 10_AI_DEBUG_HANDOFF/01_REVIEW/: independent review of exact source baseline, full diff, specs, security and tests.
- 10_AI_DEBUG_HANDOFF/02_PATCH_CANDIDATES/: isolated candidate patches; do not overwrite canonical source.
- 10_AI_DEBUG_HANDOFF/03_VALIDATION/: baseline, patched and regression runs with logs, exit codes and hashes.
- 10_AI_DEBUG_HANDOFF/04_DECISIONS/: ACCEPT / REJECT / DEFER decision, rationale and next owner.

## Sandbox rules
1. Record exact repository, branch, commit/version and source baseline before editing.
2. Read before editing; preserve project-specific structure and existing evidence.
3. Never overwrite or change LOCKED contracts without a separately versioned and reviewed decision.
4. No fake PASS. Check helpers must fail when assertions return false; preserve inspectable evidence.
5. Core :8000 must never be placed inside Sandbox. Do not bypass authorization or execution boundaries.
6. Sandbox writes are not GitHub sync. GitHub source/policy changes must use an auditable work branch and PR; verify the resulting branch/commit and content.
7. Never bulk-delete or overwrite legacy files to make the tree look uniform. Reconcile by evidence.
8. Distinguish structure-complete, feature-complete, verification-complete and release-ready.
9. Record DONE / PASS / DECISION / BLOCKED honestly, with date, owner and evidence.
10. Every Work gets the three required zones; where a dashboard is not applicable, include a README stating why rather than inventing behavior.
