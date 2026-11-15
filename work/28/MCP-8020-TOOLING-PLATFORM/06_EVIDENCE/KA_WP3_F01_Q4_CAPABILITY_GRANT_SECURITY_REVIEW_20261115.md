# WORK 28 — INDEPENDENT Q4 CAPABILITY-GRANT SECURITY REVIEW

- **Evidence ID:** KA-W28-Q4-REV-20261115-001
- **Priority / Read order:** P0 / 01
- **Type:** Independent architecture and security review
- **Reviewer:** Ka
- **Title:** Chief Security Architect (CSA) — Independent Reviewer
- **Date-time:** 2026-11-15 13:07 UTC+07:00
- **Work:** W28 — MCP Tooling Platform
- **Repository:** hqtt2026-thevinhvtqni/room-meeting-ai
- **Branch reviewed:** work/28-mcp-tooling-platform
- **Scope:** Xu decision XU-W28-WP3-F01-DEC-20261113-01, Q4 — Core capability-grant semantics for WP3-F01 sandbox_upload_file
- **Disposition:** **Q4 NOT APPROVED — DESIGN INSUFFICIENT / REVISE REQUIRED**
- **Execution Gate:** CLOSED
- **WP3-F01:** IMPLEMENTATION BLOCKED

## 1. Executive finding

The reviewed material does not contain a complete upload-specific capability-grant contract. The Vi proposal describes the intended upload workflow and security properties, while Xu's decision approves Q1–Q3 only and explicitly holds Q4 for this review. The available Core Execution Authority V1.2 is an execution-grant proposal, not an approved upload-capability design; it is explicitly marked DESIGN / PROPOSED / NOT APPROVED / NOT WIRED.

**Ka does not approve Q4 on the current revision.** Do not create upload staging, accept chunks, promote files, or register a public upload tool until Xu records a subsequent decision based on a revised grant contract.

## 2. Exact source revisions inspected

The following GitHub blob revisions were read from branch `work/28-mcp-tooling-platform`. The branch HEAD itself was not pinned by the available read operation; these blob SHAs identify the exact files reviewed and must not be represented as a branch-wide immutable commit.

| File | Blob SHA | Review use |
|---|---|---|
| `work/28/MCP-8020-TOOLING-PLATFORM/06_EVIDENCE/XU_WP3_F01_DECISION_RECORD_20261113.md` | `8dbd82b69b4c295626ab5fb101c28b9bb0b6195e` | Q1–Q3 decisions; Q4 pending Ka |
| `work/28/MCP-8020-TOOLING-PLATFORM/06_EVIDENCE/VI_WP3_BINARY_UPLOAD_AUTHORIZATION_CONTRACT_PROPOSAL_20261104.md` | `b957eba4fce949bfdfba56ba8da9dd71d9bfc29` | Proposed upload trust boundary and session protocol |
| `work/28/MCP-8020-TOOLING-PLATFORM/06_EVIDENCE/VI_WP3_BINARY_UPLOAD_SOURCE_TRACE_20261104.md` | `fb4a95a49214b54c5c28407179860999f5bf7a16` | Current v54 binary-upload and Core-wiring gaps |
| `work/28/MCP-8020-TOOLING-PLATFORM/03_ARCHITECTURE/PROPOSED_CORE_EXECUTION_AUTHORITY_CONTRACT_V1.md` | Sandbox readback; GitHub blob not independently pinned in this pass | Execution grant proposal V1.2; explicitly not approved |
| `core/execution_authority/authority.py` | `bfb052fed0fde69767dd219f17a0b14ae6383560` | Grant lifecycle implementation candidate |
| `core/execution_authority/http_server.py` | `6363c277ce410d3f5465f449b730199e06e5024c` | Candidate Core authority HTTP surface |
| `core/execution_authority/store.py` | `a628dc578c68c05bb875318d1b74528b26f0e4eb` | Append-only record store candidate |
| `execution_host/work28_core_grant_client.py` | `75b28b49a8d2ce7561d722519af293d00fac13aa` | Host-side Core grant client |
| `execution_host/server.py` | `87644127a9a2df638b5677758cfc4d0c883b2985` | Execution Host dispatch and fallback behavior |

No code was changed and no tests or live services were run in this review.

## 3. Q4 checklist — assessment

| Required property | Assessment | Finding |
|---|---|---|
| Authenticated principal binding | PARTIAL | Proposal requires server-side transport context, but no upload-grant schema binds immutable principal/session identity and credential audience. |
| Canonical Work binding | PARTIAL | Q2 selects dynamic Core mapping, but grant/session contract does not define mapping ID/version or how stale/revoked mappings invalidate an active upload. |
| Capability / operation scope | FAIL | No concrete grant schema. Free-form `purpose` in Execution Authority V1.2 is not a bounded upload capability/operation allow-list. |
| Normalized path scope | FAIL | Proposal mentions normalized destination, but no grant representation or canonicalization/equality rule binds the grant to a directory/path scope. |
| Quota and size limits | PARTIAL | Proposal mentions expected bytes, chunk limits and per-Work/per-file quotas, but does not define quota reservation, concurrent accounting, release, or immutable grant ceilings. |
| TTL / expiry | PARTIAL | Upload sessions are described as short-lived, but no grant TTL/session TTL relationship, maximum TTL, clock-skew rule or expiry transition is defined. |
| Revocation | FAIL | No upload-specific revocation contract or atomic invalidation of all sessions issued under a grant. |
| Replay / idempotency | FAIL | No defined single-use nonce, chunk replay rule, finalize replay rule, or idempotency key semantics. |
| Overwrite policy | PASS WITH CONDITION | No-overwrite-by-default is stated; explicit overwrite must remain a separately authorized capability with a race-safe precondition. |
| Pre-side-effect checks | PARTIAL | Core authorization before begin is described, but reauthorization/state checks for every chunk, finalize and abort are not fully specified. |
| Audit / correlation | PARTIAL | Required fields are listed, but ordering, durability, failure behavior and event linkage to the immutable grant/session are not specified. |
| Fail-closed behavior | PARTIAL | Intended behavior is stated, but the current adjacent execution-grant implementation contains fallback and atomicity defects; it cannot be reused as proof. |

## 4. Critical distinction: execution grant is not upload capability grant

Core Execution Authority V1.2 is explicitly a proposed execution authority contract, not a finalized WP3-F01 upload grant. It must not be silently repurposed.

Source-level observations from the reviewed candidate:
1. `ExecutionAuthority.issue_grant()` binds service identity, Work ID, a free-form purpose, workspace paths and expiry. It does not bind a named upload capability, normalized destination scope, upload quota, chunk limits, mapping version, overwrite policy or upload-session ID.
2. The active-grant check is a read/scan followed by append. The reviewed store has no inter-process transaction/lock or unique constraint for active-grant issuance; concurrent issue calls can race.
3. Revocation is represented by a separate append. Grant validation, run recording and revocation are not one atomic state transition; a revoke can interleave with a side effect/record operation.
4. `record_run()` accepts any non-empty source SHA string; it does not enforce a 64-character SHA-256 or equality with a grant-bound immutable source hash.
5. `AppendOnlyRecordStore.append()` flushes and fsyncs a record, but the in-memory index and JSONL append have no inter-process lock or torn-tail recovery policy.
6. The HTTP candidate uses `X-Room-Hop-Service-Identity` and exposes a grant-specific GET route. The Execution Host `HttpCoreGrantSource` instead expects a GET response containing a list and sends optional Bearer authentication. No compatible adapter/protocol integration was established.
7. The Core authority proposal itself says it is NOT APPROVED / NOT IMPLEMENTED / NOT WIRED and awaits Vinh's final approval. Local temp-store and ephemeral-port tests do not prove deployed Core authority.

These observations mean the current execution-grant implementation is not a safe drop-in upload capability service.

## 5. Adjacent P0 boundary blockers (must remain separate from Q4)

The reviewed Execution Host candidate has two independent fail-closed concerns:
- `build_grant_source()` returns `FileGrantSource` when the Core URL is absent. In addition, `execution_host/server.py` catches a Core grant-fetch exception and falls back to the local grant registry. A Core outage/unavailable route can therefore select local grant state rather than remain BLOCKED.
- `dispatch_execute()` accepts `mode=command` unless `snapshot_only` is enabled. The HTTP server defaults `snapshot_only=False`, authenticates a static Execution Host token and Work allow-list, then sets `work_context.authorized=True`. This path is not evidence of a Core-issued upload grant and must not be treated as Core authorization.

These are not solved by approving Q4. Keep them as separate WP5 / Execution Host integration blockers; do not enable any upload or execution tool based on this review.

## 6. Required Q4 revision before approval can be reconsidered

Vi/Xu must provide one versioned upload-capability contract with at least:

1. **Grant identity:** opaque grant ID; authenticated principal/session reference; service audience; canonical Work ID; trusted Sandbox mapping ID/version; policy/contract version.
2. **Narrow scope:** capability exactly `sandbox_upload_file`; operation allow-list `begin|chunk|finalize|abort`; normalized destination or explicitly bounded destination prefix; no caller-selected broader Work root.
3. **Hard limits:** max total bytes, max chunk bytes, max chunk count, per-Work quota, concurrent-session limit, and atomic quota reservation/release rules. The grant must never be widened by request fields.
4. **Session binding:** upload/session ID bound to grant, principal, Work, mapping version, destination, expected byte count, expected SHA-256, expiry and correlation ID.
5. **Lifecycle:** short bounded grant/session TTL; every operation checks active grant, session state and mapping version before side effects. Revocation invalidates all associated sessions and blocks chunk/finalize immediately.
6. **Replay/idempotency:** explicit behavior for duplicate chunks, reordered chunks, repeated finalize, retry after timeout and duplicate begin. Use monotonic index/offset plus an idempotency key bound to exact chunk digest; changed replay content is DENIED.
7. **Overwrite:** default DENY. Any replace operation requires a separate explicit capability and an expected destination version/hash precondition; no implicit overwrite flag from the caller.
8. **Atomicity:** reserve quota and create staging only after authorization; prevent concurrent issue/revoke/finalize races with transactional or equivalent atomic state transitions; promote only after complete byte coverage, final SHA-256 and independent readback.
9. **Audit:** durable append-only grant/session lifecycle events with principal reference, Work, mapping version, capability, operation, destination scope, size/quota, chunk index, digest, correlation/upload IDs, policy decision and outcome. No credentials or file bytes. Audit failure must not yield a success result.
10. **Failure cleanup:** expiry, cancellation, revocation, checksum mismatch, quota exhaustion and write/readback failure leave no partial final artifact; cleanup is idempotent and auditable.

## 7. Required independent test matrix

Before Q4 can be approved, the revised contract must include tests for:
- missing/forged/expired principal; wrong Work; stale/missing mapping; Core unavailable/denied;
- wrong capability, wrong operation, destination escape and scope widening;
- zero-byte, invalid UTF-8 binary and ZIP exact-byte round trip;
- max size, over-limit, quota exhaustion, concurrent quota reservation;
- chunk duplicate/reorder/gap/overlap/truncation/oversize and changed-content replay;
- grant expiry/revocation between begin, chunk and finalize;
- duplicate begin/finalize and retry after transport timeout;
- overwrite denied by default and explicit replace with stale destination version denied;
- symlink swap/race, atomic promotion failure, disk-full, audit failure and cleanup failure;
- independent readback byte count and SHA-256 equality.

Tests must run against the exact code-bearing SHA. Mocks/local HTTP may prove component behavior only; they cannot be called deployed Core integration.

## 8. Decision and next handoff

**Ka decision:** Q4 = **BLOCKED / NOT APPROVED** on the current revision. The upload-specific grant design is incomplete, and the existing Execution Authority V1.2 candidate is not approved or integrated. No upload implementation, tool registration, staging or filesystem side effect is authorized by this review.

**Required next owner actions:**
- **Xu:** record Q4 as NOT APPROVED and request a revised versioned grant contract from Vi; do not approve until the required fields and state transitions are explicit.
- **Vi:** prepare the revised contract and defect-to-test matrix; no code implementation until Xu records the Q4 decision.
- **An:** independently review the test plan after the contract is revised; do not claim acknowledgement or test execution before evidence exists.
- **Ka:** review the exact revised contract/blob SHAs and re-evaluate Q4 independently.

**Current Work status:** ACTIVE / INTEGRATION BLOCKED / NOT RELEASED. Execution Gate CLOSED. Historical MCP :8020 listener remains DO NOT USE.

**[KÝ: KA | CSA / INDEPENDENT REVIEWER]**
