# DOC-107 — Work32 Security Remediation Run #264 Evidence

- **Document Number:** DOC-107
- **Priority:** P0 — exact-SHA security remediation verification
- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-09 (Asia/Ho_Chi_Minh)
- **PR:** #49 — clean integration from main
- **Branch:** work/32-main-integration-20261109
- **Validated HEAD:** 3b25f2759a5b8daf7477b155d306ddaa7e1032ac
- **Workflow Run:** #264 / 42521404004
- **Conclusion:** SUCCESS — 6/6 required jobs
- **Status:** REMEDIATION CI PASS — REVIEW / PRODUCT INTEGRATION GATES OPEN — ACTIVE / NOT RELEASED

## 1. Exact-SHA evidence

Run #264 was triggered by PR #49 on exact HEAD 3b25f2759a5b8daf7477b155d306ddaa7e1032ac and completed SUCCESS.

| Required lane | Result |
|---|---|
| Python 3.12 compile + bounded unit tests | PASS |
| Product Auto E2E — HTTP + MCP stdio + persisted evidence | PASS |
| Windows Browser Adapter E2E | PASS |
| Work32 tooling / workflow mirror | PASS |
| Immutable product artifact — build, checksum, extracted dependency check and artifact E2E | PASS |
| Work32 release acceptance gate | PASS |

Run #254 (42520909842) was the first remediation validation and failed on compatibility/test wiring: 3 unit failures, 7 product E2E failures, and a Windows fixture blocked by missing explicit loopback allowlist. Ka corrected callers/tests, structured MCP result handling, and the Windows fixture allowlist. Run #263 (42521327021) then passed Unit/Tooling but failed one Product E2E assertion due to a stale variable name; the Windows job was cancelled by the next PR synchronization. Run #264 confirms the corrected exact head across all six jobs.

## 2. Remediation verified by code and tests

### S4 — accepted participant paste gate
- Core rejects missing identity and identity not present in the meeting's JOIN_ACCEPTED participant set.
- HTTP DTO and MCP Public V1 schema require identity_id.
- Integration and CLI callers pass explicit identities.
- Anonymous/legacy paste is no longer accepted by the Core path.
- Added positive, missing-identity, and invited-but-not-joined tests.

### S5 — short SQLite reservation
- SQLite reservation transaction commits and closes before transcript append.
- A unique reservation event_id is compensated if append fails.
- SQLite lock/store failure maps to controlled 503 + Retry-After in HTTP and a structured MCP error.
- Added lock-release and compensation tests.
- Store remains same-host/local-filesystem only; no distributed quota authority is claimed.

### S6 — structured MCP rate-limit errors
- MCP returns isError with structured RATE_LIMIT_EXCEEDED and retry_after_seconds.
- Store-unavailable MCP error is structured separately.
- HTTP preserves 429 + Retry-After and uses 503 + Retry-After for quota-store unavailability.

### S9 — URL secret redaction
- Browser navigation/evidence/transcript URL values drop query and fragment before persistence.
- Added query/fragment regression test.

### S1/S2/S2b — Browser Adapter hardening
- Browser navigation accepts only HTTP/HTTPS; DNS answers resolving to non-public IPs are blocked.
- Browser context route guard checks request/redirect targets.
- Evidence filenames are constrained to safe basenames under the evidence directory; traversal, absolute paths and platform-unsafe characters are rejected.
- Chromium launch no longer disables its sandbox.
- Tests cover private destination/redirect, explicit test-only loopback allowlist, path traversal, unsafe names and sandbox flag.
- Residual: DNS rebinding and non-HTTP egress channels still require Cla's security re-review and deployment-level outbound network controls before any untrusted/remote exposure.

### S3 — identity boundary / transport exposure
- Core HTTP entrypoint now refuses non-loopback bind while authenticated transport is not implemented.
- This is a local-only containment gate, not transport authentication. identity_id is still caller-supplied metadata and is not proof of an authenticated principal.
- Remote exposure remains BLOCKED pending TLS, signed short-lived credentials, server-derived principal binding, authenticated quota key, CORS/audit/registry protections and separate Xu/Cla approval.

### S7/S8 — filesystem path validation
- Meeting IDs are validated before meeting directory creation/read.
- Context file inputs must be plain basenames and resolve inside the approved context directory.
- Added traversal and absolute-path regression tests.

## 3. Remaining review and product gates

1. **Xu re-review:** confirm the Browser Adapter serialized ownership model, four-tool Public V1 contract (ADR-002), and whether the remaining auth_verified field should be replaced with explicit registry_resolved / transport_authenticated semantics. No silent schema migration was performed.
2. **Cla re-review:** assess S1/S2/S2b/S3/S5 residual risks, especially DNS rebinding/non-HTTP egress, identity spoofing on local loopback, same-host SQLite, subprocess environment and artifact controls.
3. **Qw independent product QE:** the original W32 Qw report was not found in the Work32 Sandbox. The retrieved Qw report belongs to Work70 Dashboard and is not substituted. Qw must provide/locate the original W32 report or independently retest this exact SHA with attributable report, scenarios and raw results.
4. **Dashboard → Workspace → Core:** still NOT RUN. Dashboard defaults to mock and canonical Workspace source/runtime/API contract remains unproven. Xu/Mê must confirm source and approve the contract before real wiring.
5. **CD / staging / production:** NOT RUN. No remote exposure, merge to main, G7, staging or production authorized.

## 4. Boundaries preserved
- PR #49 remains DRAFT and targets main, but is not merged.
- Main remains unchanged.
- PR #50 remains an isolated remediation work branch/record; code changes were curated into PR #49 for exact-SHA CI.
- Browser Adapter/Core HTTP remain loopback-only; CI uses disposable fixtures.
- No PC runner service, Work09 process, port 8787, PATH, repository variable or service account was modified.
- Status: **CI REMEDIATION PASS — REVIEW / DASHBOARD INTEGRATION PENDING — ACTIVE / NOT RELEASED.**

## BIÊN BẢN
- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-09 (Asia/Ho_Chi_Minh)
- **Decision:** Run #264 PASS on exact SHA. Remediation is not declared fully security-approved or product-released.

## NHẬT KÝ
- **W32-LOG-20261109-96:** Run #254 failure evidence and corrections recorded; no rollback of Xu's fail-closed membership decision.
- **W32-LOG-20261109-97:** Run #264 exact-SHA PASS, six required jobs successful; Xu/Cla re-review, Qw original W32 QE evidence, Dashboard → Workspace → Core E2E and release gates remain open.


## Addendum — Run #265 documentation-head revalidation
- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-09 (Asia/Ho_Chi_Minh)
- After DOC-107 was added, latest PR head became `a7fe318d14ef06bf3c25bf6005b80dede81a307f` (documentation-only commit).
- Run #265 / `42521596692` completed SUCCESS across all six jobs: Unit, Product Auto E2E, Windows Browser Adapter E2E, Work32 tooling/mirror, immutable artifact, and release acceptance gate.
- This confirms the latest documentation head without changing the code SHA validated by Run #264.
- PR #49 remains DRAFT; main unchanged; no merge/deployment/release.

**W32-LOG-20261109-98:** Run #265 docs-only exact-head revalidation 6/6 PASS.


## Addendum — Run #266 final documentation-head revalidation
- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-09 (Asia/Ho_Chi_Minh)
- Latest PR #49 head: `6369ce2578492e996390a422b759e40d0585acf5` (DOC-107 addendum only).
- Run #266 / `42521781012` completed SUCCESS across all six jobs: Python compile/unit, Product Auto E2E, Windows Browser Adapter E2E, Work32 tooling/workflow mirror, immutable artifact, and release acceptance gate.
- The code SHA remains `3b25f2759a5b8daf7477b155d306ddaa7e1032ac`, already validated by Run #264. Run #265 validated the preceding documentation-only head.
- PR #49 remains DRAFT; main unchanged; no merge, deployment or release.

**W32-LOG-20261109-99:** Run #266 final docs-head exact-SHA revalidation 6/6 PASS.


## Addendum — S10 and Run #267
- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-09 (Asia/Ho_Chi_Minh)
- Cla S10 (meeting.yaml read-modify-write and ID allocation atomicity) was omitted from the first remediation batch and remains OPEN. No S1–S10 full-closure claim is made.
- Ka will implement atomic state-file replacement and retry-safe ID directory reservation with concurrency tests; cross-process consistency remains a review gate.
- Run #267 / `42521925585` completed SUCCESS across all six jobs on documentation-only PR head `79dd24cc3451a58646643982af3003cc5712edb9`.
- Code SHA `3b25f2759a5b8daf7477b155d306ddaa7e1032ac` remains validated by Run #264; Run #265–#267 revalidated successive documentation-only heads.
- PR #49 remains DRAFT; main unchanged; no merge, deployment or release.
