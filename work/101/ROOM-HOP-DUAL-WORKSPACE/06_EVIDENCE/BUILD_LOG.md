# Work 101 — Build Log

## 2026-10-13 — Scope and branch isolation
- Verified repository `hqtt2026-thevinhvtqni/room-meeting-ai` and dedicated branch `work/101-room-hop-dual-workspace`.
- Work root: `work/101/ROOM-HOP-DUAL-WORKSPACE/`; frozen baseline recorded as `d7c90d9d31062d389810808e43dfdd19d7711b75`.
- Sync remains DRY_RUN; `write_enabled`, `merge_enabled`, and `release_enabled` remain false.
- Architecture preserves Core :8000 as source of truth, MCP :8020 as agent boundary, Workspace :8010 as build workspace. Work 24/27/28/14 contracts must be verified before adapter integration.

## 2026-10-13 — Policy implementation and hardening
- Added pure deterministic snapshot classification and DRY_RUN planning with SHA-256 content-bound diff digest.
- Enforced path canonicalization, Windows reserved-name/trailing-dot checks, path allowlist, excluded secrets/database/log/cache/generated files, protected-branch denial, baseline revision binding, approval binding and idempotency fingerprint.
- Same-path divergent edits become `CONFLICT_PENDING` with zero transfer paths.
- Any deletion relative to baseline becomes `DELETION_PENDING`, including deletion on both sides; zero transfer paths are emitted. No delete adapter exists.
- Added a regression test for bilateral deletion. Current suite contains 23 tests, including Windows-invalid filename characters, OS metadata, temporary/backup files and private-key material.

## 2026-10-13 — Runner repair and observed CI
- Repaired malformed PowerShell runner origin validation and removed duplicated/corrupted script content. Script was read back from GitHub; it has NOT been executed on the user's Windows PC.
- GitHub Actions run [38341525183](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/38341525183) completed SUCCESS on commit `2263ae1d180aa4503822cb53b554719fc6ecfffa`.
- Python 3.12.15 job log confirms `Ran 23 tests in 0.004s` and `OK`.
- Evidence recorded in `CI_POLICY_TESTS_20261013.md`.
- Workflow emitted a non-fatal post-checkout warning because `.gitmodules` has no URL for submodule path `room-meeting-ai`, plus a Node.js 20 deprecation warning. Test job conclusion remained SUCCESS.

## 2026-10-13 — Verification boundary
- Static read-back and JSON schema inspection are complete; unit tests PASS in GitHub-hosted CI.
- No local Windows PowerShell run, runtime adapter, Sandbox/GitHub round-trip, Core/MCP authorization test, live Dashboard/browser test, or ROOM-HOP E2E test has been performed.
- Work 14 lifecycle conflict remains unresolved; Work 24/27/28 live contracts remain unverified.
- `main` has not been merged by this Work. No integration, write, merge or release is authorized.

## Next gate
Verify Work 24/27/28 live contracts and Work 14 lifecycle from authoritative ROOM-HOP sources. Then implement and test the provider adapter in an isolated disposable fixture with realpath/symlink containment, Core authorization, atomic writes, read-back digest checks, audit persistence and restart/recovery. Keep DRY_RUN until exact operation approval.
