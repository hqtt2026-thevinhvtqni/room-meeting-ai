# Work 101 — Build Log

## 2026-10-13 — GitHub target
- Verified repository and dedicated branch.
- Compared `main` and branch before Work artifacts were added: identical, baseline `d7c90d9d31062d389810808e43dfdd19d7711b75`.
- Set canonical Work root to `work/101/ROOM-HOP-DUAL-WORKSPACE/`; sync remains DRY_RUN.
- Explicitly exclude `desktop.ini`, secrets, databases, logs, caches and runtime artifacts.
- No merge/release; tests, browser runtime, two-way sync and E2E remain NOT VERIFIED.

## 2026-10-13 — Branch scaffold read-back
- Canonical root and selected architecture, policy, test, evidence and Dashboard files were read back from the dedicated branch.
- The branch is 26 commits ahead of `main` and zero commits behind; all Work 101 changes are on `work/101-room-hop-dual-workspace` only.
- Added a focused unit-test case for a single backslash in a relative path. Test execution is still NOT RUN.
- No merge, release, or automatic integration occurred. Sync remains DRY_RUN; write/merge/release switches remain false.

## 2026-10-13 — Offline hardening (source review only)
- Added deterministic DRY_RUN plan generation and content-bound diff digest.
- Required explicit common-base markers for source and destination snapshots.
- Added case-insensitive path-collision rejection and permitted ordinary evidence documents while excluding logs/runtime artifacts.
- Baseline-file deletion on either side now enters DELETION_PENDING and blocks all transfer paths.
- Added a provider adapter contract; it deliberately has no delete method and no write implementation.
- Added a guarded PowerShell unit-test runner for PC use and a branch-scoped GitHub Actions workflow. No CI execution result is visible, so tests remain NOT RUN.
