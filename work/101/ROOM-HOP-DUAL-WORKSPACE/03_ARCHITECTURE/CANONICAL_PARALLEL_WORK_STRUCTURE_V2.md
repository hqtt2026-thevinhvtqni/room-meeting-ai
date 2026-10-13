# Canonical Parallel Work Structure — v2 (Reconciled)

This version supersedes any earlier note that described the GitHub target as UNBOUND. Repository, branch, work root and frozen baseline have now been identified. This binding is for target identity only; it does not enable sync writes.

- Repository: `hqtt2026-thevinhvtqni/room-meeting-ai`
- Branch: `work/101-room-hop-dual-workspace`
- Work root: `work/101/ROOM-HOP-DUAL-WORKSPACE/`
- Frozen base revision: `d7c90d9d31062d389810808e43dfdd19d7711b75`
- Sync mode: DRY_RUN; write/merge/release disabled.

Canonical folders are `00_ROOT/`, `01_ORIGINAL/`, `02_EXTENSION/`, `03_ARCHITECTURE/`, `04_CODE/`, `05_TEST/`, `06_EVIDENCE/`, `07_RELEASE/`, `08_DASHBOARD/` and `09_DASHBOARD_PREVIEW/`.

`08_DASHBOARD/` is canonical; `09_DASHBOARD_PREVIEW/` is a separate static, read-only visual review surface. Both must not fabricate live status. Runtime PASS requires dated evidence. Sandbox and GitHub use parallel relative paths; never use last-write-wins or silently delete destination-only files. Any integration approval must bind exact operation ID, diff digest, destination branch and base revision.
