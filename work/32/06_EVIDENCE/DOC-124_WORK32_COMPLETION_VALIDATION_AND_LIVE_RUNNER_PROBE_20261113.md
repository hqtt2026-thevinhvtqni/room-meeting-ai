# DOC-124 — Work32 Completion Validation and Live Runner Probe Finding

- **Document Number:** DOC-124
- **Priority:** P0 — execution evidence integrity / live authority proof
- **Work:** 32 — CI/CD
- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-13 10:20 Asia/Ho_Chi_Minh
- **Branch:** work/32-main-integration-authority-20261112
- **PR:** #52 — Core-owned Execution Authority
- **Latest workflow commit:** 17ba50ab2e8736e2636e323741ce735c107fe197
- **Status:** SOURCE VALIDATION PASS; HOSTED CI LANES PASS; LIVE CORE AUTHORITY PROBE BLOCKED

## 1. Scope and source changes

This continuation stayed within the Work32 PR branch. No change was made to main.

### Core Run Record completion validation

`core/execution_authority.py` now validates completion records before appending `run_completed`:

- `status` must be one of `PASS`, `FAILED`, `TIMEOUT`, `BLOCKED`.
- Optional `execution_status`, when present, must be one of the same values.
- `finished_at` must be valid ISO-8601 and timezone-aware; malformed and timezone-naive values are rejected.
- `exit_code` must be an integer or null; booleans and numeric strings are rejected.
- `evidence_sha256` must be exactly 64 lowercase hexadecimal characters.

Regression coverage adds 10 invalid-field cases and 2 valid `BLOCKED`/`TIMEOUT` completion cases.

### HTTP contract corrections

- `RunCompleteRequest` now accepts the Host's optional `execution_status` field.
- The completion HTTP route rejects a body `run_id` that differs from the `run_id` in the URL path.
- Regression test verifies that a mismatched completion request returns 422 and that a subsequent request using the correct path ID can still complete the Run Record.

### PC probe hardening

- Core invalid-credential probe now requires HTTP 401 or 403; HTTP 404 is not treated as proof of authentication denial.
- Host health must identify `execution-host`, `CORE_AUTHORIZED_PYTEST`, `CORE_ONLINE`, and `grant_cache=false`.
- Follow-up commit `17ba50ab2e8736e2636e323741ce735c107fe197` changed the read-only probe to collect both Core and Host diagnostics before failing, rather than stopping after the first failed check.

## 2. Exact-head CI evidence

### Run #414 — 43357234292

- PR head: `1394ceefa3fdc52a422b6aa208c50a1e00c32b77`.
- Unit: **250 passed**.
- Product Auto E2E: **122 passed**.
- Hosted Windows Browser Adapter E2E: **10 passed**; preflight, browser-context cleanup and adapter cleanup PASS.
- Work32 tooling/workflow mirror: PASS.
- Immutable product artifact: checksum verification, extracted dependency/compile checks and artifact-level E2E **1 passed**.
- Dedicated PC runner identity: PASS, but the stricter live authority probe failed as recorded below.
- Release acceptance gate: FAIL because the required live probe did not pass.

### Run #416 — 43357544278

- Exact PR head: `17ba50ab2e8736e2636e323741ce735c107fe197`.
- Unit: **250 passed**.
- Product Auto E2E: **122 passed**.
- Hosted Windows Browser Adapter E2E: **10 passed**; preflight and cleanup PASS.
- Work32 tooling/workflow mirror: PASS.
- Immutable product artifact: checksum verification, extracted dependency/compile checks and artifact-level E2E **1 passed**.
- Dedicated PC runner identity/authority probe: QUEUED at the time of this record.
- Release acceptance gate: pending the required self-hosted probe.

### Run #416 artifact references

| Artifact | ID | Uploaded ZIP SHA-256 |
|---|---:|---|
| Unit evidence | 14007295403 | `8ae54abf7956fc25738a9cca9dd9be0155a905f366e2dd01b09185e409d4365b` |
| Tooling evidence | 14006383321 | `d1739d652b0c888fc471aad29f5a73229f5f7280a2a9aae0296c08cbb57c1ca5` |
| Windows Browser Adapter evidence | 14006213872 | `3422efd9481de5a68924e3d0ba7b7c5430de2ba0d6db45e2bbd741613cd566f5` |
| Product release-candidate artifact | 14006049963 | `ea17226883c6157c935d0163cef4ac85c09ffd08ea2b0e00a662c2faf8be5ac0` |
| Product E2E evidence | 14005854362 | `12ce006bd21f1abe7b5c23bd47d9714420e4f7701930b70565d1aa290fb493f0` |

## 3. Live PC runner finding — Run #414

The dedicated runner identity check identified:

- Runner name: `ROOM-HOP-W32-PC`.
- OS / architecture: Windows / X64.
- Runner identity: PASS.
- Python command: `NOT_FOUND` in the runner service environment.
- Git: 2.55.0.windows.3.
- Ports 8000 and 8031 were listening on loopback.
- Process owner and module could not be resolved; entrypoint match was false for both protected ports.

The negative Core authority request used an invalid service identity and returned **HTTP 404**. The approved fail-closed authentication outcomes are HTTP 401/403. The current live listener therefore did not expose the expected Execution Authority status route at probe time.

The canonical source mounts the router in `room_hop_mcp/core_http_main.py`. The legacy `room_hop_mcp/adapter/http_server.py` does not mount that router. Because the live process command line/module was unresolved, the exact running entrypoint is **not proven**; an older HTTP entrypoint is a plausible explanation, not a confirmed fact.

The Host health request was not reached in Run #414 because the probe correctly failed immediately on the Core 404. Run #416 contains the diagnostic correction and must be allowed to collect Host health before final disposition.

## 4. Acceptance disposition

- Source completion validation: PASS by exact-head unit CI.
- HTTP Run Record contract tests: PASS by exact-head unit CI.
- Product Auto E2E: PASS.
- Hosted Windows Browser Adapter E2E: PASS.
- Tooling/workflow mirror: PASS.
- Immutable product artifact: PASS.
- Dedicated live Core authority proof: BLOCKED — HTTP 404.
- Host live identity proof: NOT YET OBSERVED.
- Independent security review: PENDING.
- Main integration, merge, CD, staging, production and release: NOT AUTHORIZED / NOT RUN.

No live Core/Host process was started, stopped, or reconfigured. No credentials or runtime Work policy were provisioned. No protected command was executed. PR #52 remains open and unmerged.

**Conclusion:** Work32 source and hosted CI lanes are passing, but the live Core authority route and Host identity are not attested. The release acceptance gate remains BLOCKED. **PROTECTED EXECUTION DENIED; WORK32 ACTIVE — NOT RELEASED.**

## BIÊN BẢN

- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-13 10:20 Asia/Ho_Chi_Minh
- **Decision:** Preserve the 404 as a P0 live-runtime blocker; do not convert it into PASS. Require the exact-head read-only probe to verify both Core denial semantics and Host identity.

## NHẬT KÝ

- **W32-LOG-20261113-117**
- Recorded completion validation, HTTP path/body binding, exact-head CI results, live PC runner identity and Core authority route blocker.
