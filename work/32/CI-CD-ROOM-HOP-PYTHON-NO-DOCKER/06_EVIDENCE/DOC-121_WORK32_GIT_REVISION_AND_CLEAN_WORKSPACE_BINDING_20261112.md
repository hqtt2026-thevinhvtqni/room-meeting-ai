# DOC-121 — Work32 Git Revision and Clean Workspace Binding

- **Document Number:** DOC-121
- **Priority:** P0 — source provenance / execution integrity
- **Work:** 32 — CI/CD
- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-12 00:25 Asia/Ho_Chi_Minh
- **Architecture owner:** Xu — Core owns authority; Host owns execution
- **Status:** SOURCE HARDENING ADDED — EXACT-SHA CI RETEST PENDING

## 1. Why this binding was added

A per-run source fingerprint proves which bytes the Host is about to execute, but it does not by itself prove that those bytes are the clean checkout of the canonical Work revision. Work32 therefore binds both the content fingerprint and the Git revision.

## 2. Core Grant binding

Core policy now requires:
- exact repository owner/name;
- allowed branch allow-list;
- allowed issuer and Host service identities;
- allowed Work Assignment and Task IDs;
- canonical workspace/evidence paths;
- environment ID, exact pytest entrypoint and timeout ceiling.

Each Grant additionally binds the per-run source SHA-256, exact expected Git commit SHA, repository, branch, Agent principal, Assignment, Task, Host identity, environment, command, policy version and expiry.

The source SHA-256 is intentionally per-run, not a static Work policy field. The WEE adapter computes it from the canonical WorkContext workspace; Core validates its format and stores it in the Grant; Host independently recomputes it before execution. This permits authorized commits on allow-listed branches without weakening the Host's content check.

## 3. Host provenance checks before process execution

Host verifies, from the execution workspace:
1. git rev-parse HEAD equals the expected Git SHA returned by Core.
2. git branch --show-current equals the Core-bound branch; detached HEAD is denied.
3. git remote get-url origin resolves to the exact repository authorized by Core; only GitHub.com HTTPS or SCP-style SSH origin is accepted, and credential-bearing URLs are rejected.
4. git status --porcelain --untracked-files=all is clean; modified or untracked source is denied.
5. deterministic workspace source SHA-256 matches the Grant.
6. evidence root is outside both the source workspace and the Git repository root, so generated evidence cannot contaminate source identity or make later runs appear dirty.

Only after those checks does Host persist run_started, revalidate the Grant online immediately before process creation, execute the Core-bound pytest entrypoint, write evidence and persist run_completed.

## 4. New negative coverage

- Core denies a repository or branch outside Work policy and malformed expected Git SHA.
- Host denies mismatched Git commit, branch, remote origin, dirty worktree and evidence storage inside the Git repository.
- Host denies execution if Core cannot persist run_started, if Core is unavailable before authorization, or if Core cannot persist run_completed. A test process that completed locally but lacks a completed Core Run Record is reported BLOCKED, never PASS.

## 5. Runtime limitation

Canonical Work policy and WorkContext must agree on repository, branch, Assignment, Task, Environment and Host identity. The execution workspace must be a clean branch checkout with an origin matching the repository. A detached GitHub Actions checkout is not accepted by this first contract; the Work32 runner must materialize the approved branch locally before invoking LifecycleController.

No credentials or runtime Work policy are committed. No protected command has been executed. Exact-SHA CI and independent security review remain pending.

**Conclusion:** Core owns the decision; Host verifies the actual repository, branch, commit and clean source before the protected test effect. PROTECTED EXECUTION DENIED; Work32 ACTIVE — NOT RELEASED.

## BIÊN BẢN
- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-12 00:25 Asia/Ho_Chi_Minh
- Recorded Git provenance and clean-worktree requirements for the Core-owned Grant path.

## NHẬT KÝ
- **W32-LOG-20261112-114**
- Added repository/branch/expected-head Grant binding and Host Git origin/clean-tree verification.