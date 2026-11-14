# DOC-101 — Work32 Main Integration Review Package

- **Document Number:** DOC-101
- **Priority Order:** P0 — Independent review required before main integration
- **Work:** 32 — CI/CD ROOM HOP Python CI
- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-08 14:24 (+07:00)
- **Repository:** hqtt2026-thevinhvtqni/room-meeting-ai
- **Implementation branch:** `work/32-ci-runner-owned-fixture-v2`
- **Review snapshot SHA:** `0fd12a94dcf598583e402cdb92352ee2f6596880`
- **Main HEAD snapshot:** `024e2c9797da091b83c2e0ea5e3ac7f3b593eafb`
- **Latest exact-SHA CI:** Run #234 / `42460406640` — SUCCESS, 6/6 jobs

## 1. Executive disposition

Work32 CI implementation has repeatable exact-SHA CI, Product Auto E2E, Windows Browser Adapter + MCP Sub handoff/readback, and immutable artifact verification. This is a feature-branch CI acceptance result, not main integration acceptance and not a product release.

**Decision: MAIN INTEGRATION BLOCKED pending independent review.** Do not merge/rebase/cherry-pick the existing branch directly into main. Build a reviewed integration plan against current main after the file-level review.

## 2. Branch topology evidence

- GitHub compare status: `diverged`.
- Work32 branch: 251 commits ahead, 273 commits behind.
- Merge base: `9e4002cbd93a6b92684b17623d79a1adda161d37`.
- Changed paths reported by GitHub compare: 124.
- The current compare includes 44 tracked `desktop.ini` deletions and Work32-owned docs; it is not equivalent to 124 product-code changes.
- The 44 `desktop.ini` files were confirmed Windows Explorer metadata containing only a local Google Drive File Stream icon reference. They were removed in one feature-branch commit; the resulting tree has zero `desktop.ini` paths. Existing `.gitignore` rule remains.
- Real test source and test directories were retained; no mass test cleanup was performed.
- No main ref has been modified.

## 3. Change classification for reviewer

### A. CI / packaging / runner
- `.github/workflows/ci-validation.yml` — exact-SHA CI jobs, Windows runner lane, immutable artifact build and acceptance gate.
- `constraints-ci.txt`, `requirements.txt` — deterministic Python runtime dependencies.
- `scripts/w32_install_python_runtime.ps1` — runner-local portable Python provisioning.
- `scripts/w32_windows_browser_adapter_fixture.py` — disposable meeting/store and dynamic loopback fixture.
- `scripts/w32_browser_adapter_bootstrap.py` — exact checkout-root import bootstrap.
- Work32 workflow mirror is tested and reports IN_SYNC.

### B. Core resource policy / F4
- `core/meeting_manager.py`, `core/paste_rate_limiter.py`, `core/secretary.py`, `room_hop_mcp/adapter/http_server.py`, `room_hop_mcp/adapter/server.py`.
- These changes are not accidental CI side effects: DOC-065 records Xu's explicit Option A decision — 100 accepted paste requests per resolved identity per meeting per rolling 60 seconds; SQLite `BEGIN IMMEDIATE` atomic admission; persistent same-host local-filesystem state; reservation rollback on append failure; preserve 1 MiB UTF-8 byte ceiling; HTTP 429 + Retry-After; MCP maxLength as character-level early bound only.
- Explicit limitation: SQLite implementation is not certified for multi-host or unreliable network filesystems. Identity is registry-resolved but is not independent transport authentication. Legacy unidentified callers share an anonymous per-meeting quota.
- Reviewer must verify the implementation against DOC-065 and the current main Core contracts. Do not expand its claim to multi-host deployment.

### C. Browser Adapter / MCP Sub integration
- `integration/room_hop_integration.py` adds optional explicit subprocess args while preserving default `python -m room_hop_mcp` behavior for existing callers.
- `room_hop_mcp/browser_agent_adapter/adapter.py` runs the MCP stdio client on a dedicated worker thread outside Playwright's synchronous event-loop thread; isolated child bootstrap inserts the exact checkout root for portable Python.
- Handoff checks the exact four Public V1 tools, exact disposable meeting and identity, sends a bounded artifact marker through `add_paste_to_meeting`, and verifies transcript readback. Timeout does not auto-retry an uncertain append.
- No second Core is created; the MCP subprocess is a transport client/server process boundary and delegates to the existing MeetingService/Core path.
- Windows E2E on Run #234: meeting `MEETING-W32-42460406640-1`, PID 21468, port 58821, exact SHA preflight PASS, 10 tests PASS, browser and exact process cleanup PASS.

### D. Tests / evidence
- Unit: 189 passed.
- Product Auto E2E: 68 passed.
- Windows Browser Adapter E2E: 10 passed.
- Immutable extracted-artifact E2E: 1 passed.
- Tooling mirror: IN_SYNC.
- CI release acceptance gate: PASS.
- Product artifact ID `13609402495`, uploaded ZIP digest `98c896bd080f6564d0a2e225ab3a534f04ae95d4f02d5752cd68d53256eec507`.
- Windows evidence artifact ID `13609512084`, SHA-256 `e8e5801a81014b99c18a89ee25230bd01bbf49cc5cb0b8ec2498fbfb4c3ac95e`.

## 4. Required independent review checklist

- [ ] Compare every Work32-owned source change against current main contracts and identify conflicts.
- [ ] Verify Core/MeetingService/Secretary/F4 behavior and DOC-065 authority, especially same-host-only quota scope.
- [ ] Verify MCP Public V1 remains exactly four tools and all callers preserve backward compatibility.
- [ ] Review subprocess environment minimization, explicit Python bootstrap, bounded timeout, cancellation, and no automatic retry after uncertain append.
- [ ] Review Windows runner permissions, action pin SHAs, artifact contents, retention and secret exposure.
- [ ] Review 44 metadata deletions and confirm no business content was removed.
- [ ] Review test coverage report and classify any not-run suites without weakening mandatory gates.
- [ ] Decide a clean integration branch strategy based on current main; do not merge the 251-ahead/273-behind branch as-is.
- [ ] Record independent reviewer, title, timestamp, decision and exact reviewed SHA.

## 5. Release boundary

- Dashboard browser→Core integration: BLOCKED / NOT RUN.
- CD/staging/production: BLOCKED / NOT RUN; no attested target, protected approval environment, credentials, health-check target or tested rollback.
- DOC-050 G7 RELEASE: NOT READY / NOT AUTHORIZED. Product Owner authority remains Vinh.
- No merge, tag, deployment or production release is claimed.
- Work32 status: **ACTIVE — NOT RELEASED**.

## BIÊN BẢN

- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-08 14:24 (+07:00)
- **Record:** Prepared a source-backed main integration review package; no main branch mutation or release approval.

## NHẬT KÝ

- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-08 14:24 (+07:00)
- **Priority:** P0
- **Action:** Classified Work32 changes, reconciled F4 authority to DOC-065, checked current branch topology and recorded exact CI evidence.
- **Result:** Review package prepared; main integration remains BLOCKED pending independent review.


## 2026-11-09 — Current source reconciliation addendum

- Current feature branch: `work/32-ci-runner-owned-fixture-v2`, SHA `b7acbea7a7fa71f40c37525b1c288a7fb64ad6a5`.
- Current compare snapshot: main SHA `024e2c9797da091b83c2e0ea5e3ac7f3b593eafb`; branch is diverged, 256 ahead / 273 behind, 125 changed paths (81 added/modified plus 44 tracked desktop.ini removals).
- The 44 desktop.ini removals are excluded from the clean integration candidate. The candidate is created from main and overlays only audited added/modified paths; no diverged history merge, rebase or force-push is performed.
- PR #47 is a DRAFT from `work/32-ci-windows-runner-owned-fixture` to `work/32-ci-cd-python-ci-v2`, head SHA `1028bb6139a896dad6c250f6d8831ee6139d1458`; it is not the current feature branch or main integration PR. It has no submitted reviews.
- W32-ADR-002 already resolves the Public V1 contract to exactly four tools. Main's Integration client has a stale fifth `join_meeting` requirement; Work32's four-tool client/test aligns with ADR-002 and the actual server. No new Xu decision is required for the tool inventory.
- DOC-065 confirms F4 Option A and limitations: 100 accepted pastes per resolved identity per meeting per rolling 60 seconds; SQLite atomic same-host only; `identity_id` is not transport authentication.
- Browser Adapter has been hardened with a re-entrant operation lock and dedicated single-worker Playwright executor. Two new tests cover workflow isolation and single-thread ownership. These changes still require a new exact-SHA CI result.
- Xu review is requested for the serialization/concurrency tradeoff. CTO review is required before staging/production for the security boundary and multi-host storage limitation.
- Release disposition unchanged: ACTIVE — NOT RELEASED; main, staging and production remain untouched.


## 2026-11-09 — Exact-SHA CI acceptance result

- Clean integration PR #49: `work/32-main-integration-20261109` → `main`, exact head SHA `44848a31026dd2bce6e01a4dce14acda417154dd`.
- Run #249 (`42517462912`) concluded SUCCESS.
- Python 3.12 compile/unit: 189 passed; Product Auto E2E: 70 passed; Windows Browser Adapter E2E: 10 passed; tooling/mirror PASS; immutable artifact and extracted dependency check PASS.
- Windows evidence: 10/10 tests passed, browser context cleanup PASS, adapter process cleanup PASS. The PR lane uses GitHub-hosted Windows; self-hosted `ROOM-HOP-W32-PC` remains the push lane for `work/32-ci-*`. Earlier Run #229 remains evidence for the PC runner.
- PR diff: 82 changed paths, 70 added, 12 modified, zero deleted. No tracked desktop.ini deletions were included.
- PR remains DRAFT, mergeable and unmerged. Main remains unchanged.
- Remaining release blockers are not CI: Dashboard→Workspace→Core E2E is NOT RUN; Workspace :8010 canonical source/contract needs Xu/Mê confirmation; CTO security review is required before staging/production. Status ACTIVE — NOT RELEASED.
