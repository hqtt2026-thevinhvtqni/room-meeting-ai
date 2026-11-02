# DOC-066 — KẾ HOẠCH TRIỂN KHAI VÀ KIỂM THỬ ĐIỀU PHỐI GIAO VIỆC AI
- **STT / Document ID:** DOC-066
- **Priority:** P0
- **Read order:** 66
- **Depends on:** DOC-043; DOC-044; DOC-057; DOC-064; DOC-065
- **Status:** PLANNED — IMPLEMENTATION NOT AUTHORIZED / TESTS NOT RUN
- **Version / Updated:** 1.0 / 2026-11-02
- **Owner:** Xu / AI-01
- **Authority:** Vinh

## 1. Objective
Triển khai Hybrid AI Dispatch với ưu tiên giữ nguyên conversation/session, tái sử dụng quyền hiện có, hạn chế API cost; có dispatch, ACK, progress, result, review, audit và evidence thật. Không xây code trước khi xác minh Core boundary, source baseline, quyền và Work Entry gate.

## 2. Existing baseline / constraints
- DOC-043 đã quy định AI roster không chứng minh agent online/connected/capable.
- DOC-044 là assignment template hiện hữu; DOC-065 mở rộng thành provider-neutral transport/event contract, không thay thế DOC-044 cho đến khi migration được duyệt.
- MCP 8030 toolset đã kiểm tra có Sandbox CRUD/list/read và Meeting list/get/join/start/add-paste; không thấy dispatch tool trực tiếp đến conversation riêng của AI.
- Meeting relay chỉ chuyển nội dung trong ROOM Meeting; không được đồng nhất với ChatGPT/Gemini/Qwen private conversation.
- Core Work/Assignment/Evidence API và authoritative persistence chưa xác minh; không tạo database song song hoặc route giả định.
- Adapter/API capability từng provider chưa được kiểm chứng; status UNKNOWN đến khi test.

## 3. Workstreams and ownership proposal
| Track | Owner | Scope | Output | Gate |
|---|---|---|---|---|
| A — Core/authority discovery | Vi + Core owner | Router/service/auth/persistence/assignment/evidence source trace | capability matrix + source refs | no guessed API |
| B — Architecture/security | Ka | reconcile DOC-064/065 with DOC-043/044/057/061/063; threat model | approved ADR/contract delta | review independent |
| C — Session handoff MVP | Xu + Co | handoff packet generator, manual receipt import, no API | implementation + tests | one verified AI session |
| D — Connector capability | Xu/owner per provider | inventory existing connected plugins/permissions; test each action | capability registry evidence | per-provider allowlist |
| E — UI/read projection | Vi | dispatch status, ACK, progress, blockers, evidence, cost class | read-only dashboard view | Core source verified |
| F — Independent QE | An + Qw | contract, security, retry, timeout, concurrency, E2E | raw test evidence + report | independent reviewer |
| G — Integration | Xu | end-to-end integration and defect triage | integration evidence | owner approval |
No parallel edits to same files. Every track uses a dedicated branch/PR and named owner.

## 4. Implementation phases
### Phase 0 — Baseline and authority (READ-ONLY)
- Freeze source repository, branch, commit and working tree evidence.
- Identify Core owner and authoritative store.
- Trace current assignment/Work package structures and DOC-044/WORK_PACKAGE schema.
- Inventory installed connector actions and provider support without creating new API credentials.
- Define manual receipt trust level.
Exit: source map, capability matrix, open decisions, no code change.

### Phase 1 — Contract and schema validation
- Reconcile DOC-064/065 with canonical state machine, DOC-043/044/057 and Core auth.
- Define Assignment, DispatchAttempt, AI capability record, ACK, Progress, Result, Review, Audit event schemas.
- Add JSON Schema validation and contract fixtures.
- Freeze version 1.0 only after architecture/security review.
Exit: contract review approved by relevant owners; schema tests green; no unknown route assumed.

### Phase 2 — Session Handoff MVP (no new API)
- Generate immutable handoff packet containing assignment ID/version, scope, source baseline, instructions, acceptance criteria, due policy, nonce/challenge and return format.
- Provide copy/export/open-in-existing-conversation workflow only where platform supports it.
- AI pastes packet into its existing session; response includes ACK/result envelope.
- User/operator imports receipt into ROOM; label MANUAL_ATTESTED unless stronger verification exists.
- Track handoff-created, user-submitted, receipt-imported separately.
- No browser automation, cookie reuse, session scraping or impersonation.
Exit: one end-to-end handoff round trip with a real AI session, correct assignment binding, duplicate/replay negative test, evidence retained.

### Phase 3 — Native connector adapters (only supported providers)
- Discover existing connector actions and permissions.
- Implement only provider-supported send/read/callback actions; retain provider session if documented and tested.
- Per adapter: auth test, target binding, send receipt, read/ACK, timeout, revoke, error mapping, cost test.
- If action cannot continue existing conversation, classify as NEW_SESSION and do not silently substitute.
Exit: each adapter has its own evidence record; unsupported providers remain SESSION_HANDOFF/UNSUPPORTED.

### Phase 4 — Assignment lifecycle and durable ingest
- Implement state transition guard, event dedupe, sequence ordering, idempotency, retry/reconcile.
- Store authoritative state through approved Core service; if Core service absent, stop and submit Core-owned design proposal.
- Ingest ACK, progress, result and review events; append audit.
- Enforce assignment version, expiry and grant revocation.
Exit: persistence/recovery and concurrency tests pass against authoritative implementation.

### Phase 5 — Dashboard and operations
- Read-only projection with transport vs assignment status.
- Show manual vs connector verified provenance, stale/unknown, timeout, blocker, reviewer and cost.
- No optimistic success state; no UI writes to authoritative registry.
Exit: live read integration verified; mock/snapshot visibly distinguished.

### Phase 6 — Independent E2E and release readiness
- An/Qw run independent suite on canonical branch/environment.
- Resolve defects, rerun regression, capture raw output, commit/PR and deployment attestation.
- Vinh decides acceptance/release. No automatic release.

## 5. Test strategy and matrix
Test layers must remain distinct: unit, schema/contract, adapter integration, Core integration, controller/orchestrator E2E, deployed runtime attestation. A lower-level test does not prove a higher-level layer.

| ID | Scenario | Expected result |
|---|---|---|
| HD-001 | DRAFT assignment dispatch | reject NOT_READY; no transport attempt |
| HD-002 | READY assignment with missing permission | deny; no send |
| HD-003 | capability UNKNOWN/expired | automated adapter denied; handoff alternative may be offered |
| HD-004 | wrong target/session | reject TARGET_UNVERIFIED |
| HD-005 | native connector confirms delivery | DELIVERED with provider receipt |
| HD-006 | HTTP accepted but no provider receipt | DELIVERY_UNKNOWN, not DELIVERED |
| HD-007 | session handoff packet created | HANDOFF_READY only |
| HD-008 | manual packet pasted and receipt imported | HANDOFF_SUBMITTED / MANUAL_ATTESTED; not cryptographic ACK |
| HD-009 | verified AI ACK with correct assignment/nonce | ACKNOWLEDGED |
| HD-010 | spoofed AI ID or wrong assignment ID | reject; no ACK |
| HD-011 | duplicate ACK/event | one effect; duplicate ignored |
| HD-012 | same idempotency key, changed payload | IDEMPOTENCY_CONFLICT |
| HD-013 | delivery unknown then retry | reconcile first; no blind duplicate |
| HD-014 | ACK timeout | EXPIRED or escalation per policy; never assume decline |
| HD-015 | expired/revoked grant | deny next privileged action |
| HD-016 | out-of-order progress sequence | reject/quarantine; preserve audit |
| HD-017 | author submits result without evidence | remain IN_PROGRESS/BLOCKED; no IN_REVIEW |
| HD-018 | reviewer equals author | downgrade SELF_CHECK; no independent approval |
| HD-019 | reviewer requests changes | return to IN_PROGRESS with findings |
| HD-020 | reviewer approves but no closure authority | REVIEW_APPROVED; not DONE |
| HD-021 | API adapter without cost approval | COST_APPROVAL_REQUIRED |
| HD-022 | connector fails and fallback would create new session | do not fallback silently |
| HD-023 | callback signature/nonce invalid or replayed | reject |
| HD-024 | secret appears in prompt/log | test fails; redact and rotate if exposed |
| HD-025 | Core/persistence outage | fail closed; no local shadow source |
| HD-026 | concurrent command same assignment version | at most one state transition |
| HD-027 | Dashboard write attempt | denied; read-only |
| HD-028 | stale projection | show stale/version; no live claim |
| HD-029 | provider session continuity unsupported | classify NEW_SESSION or unsupported; no continuity claim |
| HD-030 | provider usage/cost unavailable | cost UNKNOWN, not zero |

## 6. Required evidence per phase
- source repo/branch/commit and working tree status;
- schema validator output and fixtures;
- adapter capability test and exact provider response;
- dispatch/ACK event IDs and correlation IDs;
- raw positive and negative test output;
- audit persistence/readback and event dedupe proof;
- reviewer independence record;
- dashboard data source/freshness;
- cost evidence or UNKNOWN;
- deployment identity/build hash for runtime tests.

## 7. Release criteria
- all mandatory tests for enabled adapter modes pass independently;
- no unresolved critical/high security defect;
- no fake delivery/ACK/completion or API-cost claims;
- Core authority/persistence contract verified;
- evidence provenance, idempotency, replay, revocation and recovery verified;
- Dashboard read-only and honest about source/freshness;
- Vinh approval recorded.

## 8. Current execution status
- Architecture and contract documents created as proposals in Sandbox.
- No source code changed.
- No AI dispatch executed by these documents.
- No AI ACK received.
- No tests executed.
- GitHub sync not verified.
- Implementation authorization remains BLOCKED pending Work Entry and source/Core owner verification.

**Next action:** Xu to reconcile DOC-064/065 with Ka, Vi and An existing evidence; then create implementation assignments only after owner ACK and Work Entry authorization. Prefer Phase 0 and Phase 2 manual handoff MVP before any paid API.
