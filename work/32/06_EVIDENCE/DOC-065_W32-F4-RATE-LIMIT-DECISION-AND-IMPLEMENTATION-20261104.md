# DOC-065 — F4 RATE LIMIT DECISION AND IMPLEMENTATION RECORD

- **Document Number:** DOC-065
- **Priority Order:** P0 — Core resource protection / accepted-request boundary
- **Work:** 32 — CI-CD-ROOM-HOP-PYTHON-NO-DOCKER
- **Decision owner:** Xu — CEO / Lead Architect / Work coordinator
- **Implementation owner:** Ka — CSA / Backend execution
- **Date-Time:** 2026-11-04 (Asia/Ho_Chi_Minh; exact minute not captured)
- **Status:** PASS — exact-SHA run #34; same-host SQLite scope; multi-host not certified
- **Baseline decision:** Option A — 100 accepted paste requests per resolved identity per meeting per rolling 60 seconds.

## 1. Xu decision received
The latest Xu instruction authorizes implementation without returning routine technical choices to Vinh:
- Limit: 100 accepted requests.
- Scope: identity/user + meeting.
- Window: rolling 60 seconds.
- Atomic concurrency control and persistent state are required.
- Existing 1 MiB UTF-8 byte guard remains authoritative.
- MCP schema declares maxLength, but JSON Schema character length is not byte enforcement.
- Browser Adapter remains same-host :8787 deferred; Track B remains source/contract discovery only; no main merge, CD, production or release.

## 2. Evidence-first architecture adjustment
Source audit at branch HEAD `c21b59e23d0a9c03f05aad86170ff20c577f4bf6` found:
- Core persists meetings as per-meeting files under `meetings/` (meeting.yaml, transcript.txt and append-only meeting log).
- No Redis, PostgreSQL, or existing shared quota service is declared in the inspected repository tree or dependency manifest.
- Current HTTP/MCP paste boundaries do not receive an authenticated principal context separate from optional `identity_id`.
- Existing `identity_id` is resolved through Principal/Agent Registry, but registry resolution alone is not proof of transport authentication.

### Selected implementation baseline
- Use SQLite from Python standard library at `meetings/.room_hop_paste_rate_limits.sqlite3`, beside Core's existing meeting storage.
- Use `BEGIN IMMEDIATE` plus an indexed event table to make admission atomic across local threads/processes sharing the same host filesystem.
- Store a SHA-256 pseudonymous identity key rather than the raw identity ID.
- Count only successful raw transcript appends. Reserve inside a transaction; commit quota only after Secretary append succeeds; rollback on append failure.
- Expire event rows older than 60 seconds on each admission.
- A resolved `identity_id` forms the quota key. Legacy callers omitting identity remain backward compatible but share a single per-meeting `legacy:unidentified` bucket; omission cannot bypass the limit.
- HTTP returns 429 with `Retry-After` and structured retry metadata. MCP error text carries `RATE_LIMIT_EXCEEDED retry_after_seconds=N`.
- The store is explicitly same-host/local-filesystem scoped. It is not certified for multi-host shared network storage. Work 32 has no approved multi-host deployment target and CD remains blocked; no Redis/PostgreSQL service is invented. Any future multi-host deployment must replace this adapter with an approved shared atomic store before release.

## 3. Source/test scope
- Add `core/paste_rate_limiter.py` using SQLite standard library.
- Centralize validation in `Secretary.validate_text`; retain 1 MiB UTF-8 byte guard.
- Enforce in Core Meeting.add_paste, after active-meeting, text-size and identity validation, before transcript append.
- Keep legacy `identity_id` optional; add optional HTTP identity propagation and MCP schema `maxLength=1048576`.
- Map rate rejection to HTTP 429 with retry header; preserve prior domain-error behavior for all other paste failures.
- Add deterministic quota, rolling expiry, persistence, rollback, concurrency, Core and HTTP boundary tests.
- Add the F4 test module to bounded unit CI. Strict coverage remains report-only and unauthorized.

## 4. Known limitations / explicit non-claims
- Resolved registry identity is the best caller key exposed by the current public contract; it is not an independently authenticated transport principal. Do not describe it as cryptographic authentication.
- Legacy unidentified calls share one anonymous per-meeting quota.
- SQLite coordinates same-host local processes; it does not coordinate multiple hosts or unreliable network filesystems.
- No production deployment, multi-host operation, final acceptance or release is claimed.
- Node.js Actions and Starlette/httpx warnings are separate changes and must be validated independently.

## BIÊN BẢN / MINUTES
- **Name:** Ka
- **Title:** CSA / Backend execution owner, delegated by Xu
- **Date-Time:** 2026-11-04 (Asia/Ho_Chi_Minh; exact minute not captured)
- **Decision recorded:** Implement Xu's Option A with same-host SQLite atomic persistence; preserve compatibility and enforce at Core paste boundary.

## NHẬT KÝ / JOURNAL
- **Name:** Ka
- **Title:** CSA / Backend execution owner, delegated by Xu
- **Date-Time:** 2026-11-04 (Asia/Ho_Chi_Minh; exact minute not captured)
- **Action:** Re-read Work 32 structure policy, ADR-001/002/003, DOC-063, source tree, Meeting/MeetingService/Secretary/MCP/HTTP contracts and F4 tests. Prepared SQLite same-host adaptation and dedicated concurrency/integration tests.
- **Result:** Implementation committed for exact-SHA CI validation; no main merge, CD, deployment or release.


## CI correction addendum — RUN #33
- Run #33 / `41805259568` on exact SHA `409ba7f382f46372484fa967867f4e5b8c6fdd5f`: Unit failed (181 passed, 8 failed), E2E PASS, tooling PASS, immutable artifact job skipped.
- Raw logs identified two concrete defects: SQLite connection cleanup after quota rejection, and violating Secretary's locked three-method public API by adding a validation method.
- Corrected by keeping validation as module-level `validate_transcript_text` and consolidating SQLite rollback/close handling. No tests were weakened or removed.
- Status: F4 implementation remains IN PROGRESS; next exact-SHA validation pending.


## Exact-SHA validation addendum — F4 PASS
- **Run:** GitHub Actions #34 / `41805684024`, exact SHA `c7359d4cb5eae62992129dd1a3615652ce93680e`, COMPLETED / SUCCESS, 4/4 jobs.
- **Results:** Unit 189 passed (1 Starlette/httpx warning); Product Auto E2E 45 passed (1 warning); tooling 20 tests OK; immutable product artifact verified and extracted-artifact E2E 1 passed.
- **F4 status:** PASS for same-host implementation scope. Dedicated F4 tests cover 100/101 boundary, per-identity/per-meeting scope, rolling expiry, persistence across limiter instances, rollback, concurrent admission, Core quota enforcement, oversized-input non-counting and HTTP 429/Retry-After.
- **Artifacts:** product RC ID 13309367495, SHA-256 `27e6cb702d8cc56c49b8a438878f78678085a8ca9ea9609de97f25b5ee4c6dd1`; unit ID 13310185300; E2E ID 13308994396; tooling ID 13308869618.
- **Known limitations:** identity_id is registry-resolved but not independent transport authentication; unidentified legacy calls share an anonymous per-meeting bucket; SQLite is same-host/local-filesystem only. Multi-host deployment requires a shared atomic store and separate approval.
- **Remaining:** Node.js Actions runtime warning and Starlette/httpx deprecation are separate remediation items; Browser Adapter :8787 remains deferred; Track B blocked; branch governance pending; CD/release blocked. Work 32 remains ACTIVE — NOT RELEASED.
