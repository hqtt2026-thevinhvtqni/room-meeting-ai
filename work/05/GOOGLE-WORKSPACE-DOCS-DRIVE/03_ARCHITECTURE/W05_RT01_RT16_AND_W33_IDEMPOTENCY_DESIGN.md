# Work 05 / Work 33 — RT-01..RT-16 Test Mapping and Drive Upload Idempotency Design
Date: 2026-11-29
Branch baseline: work/05-google-drive-oauth-adapter
PR: #86 (Draft; do not merge)

## 1. Verified repository boundary

### Work 05 — present in this branch
Source handoff:
`work/05/GOOGLE-WORKSPACE-DOCS-DRIVE/10_TEST/MANUS_E2E_RUNS/W05_REAL_WORK_001/LOCAL_SOURCE_HANDOFF/`

Relevant Python modules:
- `src/work05_connections.py`: OAuth state, encrypted credential store, ConnectionManager, credential ownership and explicit refresh.
- `src/work05_drive_factory.py`: constructs Drive API v3 client from the exact Work/user-owned OAuth credential.
- `src/work05_google_adapter.py`: provider-neutral Docs adapter and fake provider; not a production Drive file-upload adapter.
- Existing tests include `tests/test_work05_connections.py`, `tests/test_work05_drive_factory.py`, and `tests/test_work05_google_adapter.py`.

Observed gaps in Work 05 source:
- `ConnectionManager.refresh()` has no per-connection single-flight lock and no stale-credential recheck. RT-06 is not implemented.
- Refresh failures are currently all mapped to REAUTH_REQUIRED; provider error classes such as invalid_grant vs transient 5xx are not represented distinctly.
- No test evidence in this document claims these new scenarios passed.

### Work 33 — implementation not found in this branch snapshot
The Work 33 tree under `work/33/ROOM-SHARED-FILE-EVIDENCE-HUB/` currently exposes its root/architecture/evidence zones and an execution-journal artifact, but no Python Google Drive storage/upload adapter or upload retry test module was found in the inspected tree.
Therefore RT-01..05, RT-07, RT-09..13, RT-15 and RT-16 cannot honestly be attached to a real Work 33 class yet. Do not duplicate a Work 33 storage adapter inside Work 05.

## 2. Ownership decisions

| Concern | Owner | Contract |
|---|---|---|
| OAuth authorization, state, token custody/encryption, refresh and disconnect | Work 05 | Resolve credentials only after Core authorizes room + user + connection_id. Tokens never leave trusted backend boundary. |
| Drive file create/update/list/get, upload retry, reconciliation, duplicate prevention | Work 33 | Accept a Work 05-authorized Drive client/capability; never read or store OAuth tokens itself. |
| Room/workspace membership and connection authorization | Core | Fail closed before Work 05 credential resolution. |
| Upload request identity and audit correlation | Core → Work 33 | Pass immutable operation_id/idempotency_key and authorized target context. |

## 3. RT-01..RT-16 ownership and acceptance mapping

| Test | Owner | Required behavior / acceptance evidence |
|---|---|---|
| RT-01 | Work 33 | 429 without Retry-After uses bounded exponential backoff with documented jitter. |
| RT-02 | Work 33 | 503 then success retries only a replay-safe operation and returns the success result. |
| RT-03 | Work 33 | 502 exhausts exactly 1 + maxRetries calls and returns final response/error. |
| RT-04 | Work 33 | Valid Retry-After within the remaining wait budget is honored. |
| RT-05 | Work 33 | Jitter near upper random boundary stays within configured bounds. |
| RT-06 | Work 05 | Concurrent refresh calls for one connection share one refresh operation/result; different connection IDs remain isolated. |
| RT-07 | Work 33 orchestration + Work 05 refresh | Upload gets one 401, requests/awaits one authorized refresh, then retries upload once with new credential. |
| RT-08 | Work 05 | Definitive invalid_grant moves connection to REAUTH_REQUIRED, preserves sanitized audit evidence, and does not retry. Do not delete audit history. Credential erasure follows explicit disconnect/revocation policy, not a blind exception handler. |
| RT-09 | Work 33 | Past HTTP-date Retry-After resolves to zero wait. |
| RT-10 | Work 33 | Retry-After beyond the remaining wait budget stops retry; never clamp downward and call early. |
| RT-11 | Work 33 + Work 05 classification | 403/insufficient scope is terminal and surfaced as permission/scope failure. |
| RT-12 | Work 33 | A second 401 after the single refresh is terminal; max two upload attempts and max one refresh. |
| RT-13 | Work 33 | After ambiguous upload timeout/5xx, reconcile by idempotency metadata before any create replay; return the already-created Drive file if found. |
| RT-14 | Work 05 | Refresh 5xx or ambiguous transport failure is not blindly replayed; preserve the current credential record and report a retry-safe/reauth decision based on classified provider response. |
| RT-15 | Work 33 | 429 attempts stop exactly at 1 + maxRetries. |
| RT-16 | Work 33 | Each replay obtains a fresh request body/media stream from a body factory. |

The user's sample snippets for RT-09, RT-10 and RT-05 are policy-level examples, not integration tests: they test local arithmetic and do not exercise a production retry implementation. The integration suite must call the actual Work 33 policy/client and actual Work 05 manager.

## 4. Work 33 duplicate-safe upload protocol

### 4.1 Immutable operation identity
Before the first network request, Core/Work 33 creates and persists an immutable `operation_id` (UUIDv4/UUIDv7) for one logical meeting-artifact upload. Retries of that logical operation MUST reuse the same ID. A new user-requested upload gets a new ID.

Derive a stable key:
`idempotency_key = SHA256(room_id || meeting_id || artifact_type || operation_id)`

Do not derive identity from filename alone: two legitimate artifacts can share a title/date, and filename normalization can collide.

### 4.2 Drive metadata
On file create, Work 33 writes Drive `appProperties` at creation time:
- `roomhop_operation_id`: immutable operation ID
- `roomhop_idempotency_key`: stable hash
- `roomhop_meeting_id`: opaque meeting identifier
- `roomhop_artifact_type`: allow-listed artifact type
- `roomhop_schema_version`: metadata contract version

Do not place secrets, access tokens, meeting text, participant email addresses, or sensitive personal data in appProperties. Use private appProperties (not userProperties) for application-owned correlation.

### 4.3 Durable operation ledger
Work 33 persists an upload-operation row before sending bytes. Minimum fields:
- operation_id (unique)
- idempotency_key (unique)
- room_id, meeting_id, artifact_type
- target_parent_id
- expected_content_sha256 and byte_size
- state: PREPARED | UPLOADING | UNKNOWN_OUTCOME | RECONCILING | COMMITTED | FAILED_FINAL
- drive_file_id (nullable)
- attempt_count, last_http_status, last_error_class
- created_at, updated_at, committed_at

Enforce database UNIQUE constraints on operation_id and idempotency_key. Use a compare-and-set/state transition or row lock so concurrent workers cannot create the same operation twice. A process-local mutex alone is insufficient across replicas.

### 4.4 Upload flow
1. Authorize user/room/connection through Core and Work 05. Resolve one connection-bound Drive client.
2. Create or load the durable operation row. If COMMITTED, return the recorded drive_file_id without another API call.
3. Query Drive for exact private appProperties match on idempotency key, constrained to the authorized parent/drive and non-trashed files.
4. If exactly one match exists, verify parent, expected size and content hash where retrievable; mark COMMITTED and return its file ID.
5. If multiple matches exist, mark a reconciliation conflict and stop. Never pick an arbitrary file or delete automatically.
6. If no match exists, transition PREPARED → UPLOADING and create the file with appProperties in the same create request as the media upload.
7. On confirmed success, persist file ID and COMMITTED atomically in the local ledger.
8. On timeout, connection reset, or ambiguous 5xx, transition to UNKNOWN_OUTCOME. Do not blindly replay create.
9. Reconcile by exact appProperties key. If one matching file is found, verify metadata and commit it. If none is found, wait through a bounded consistency/reconciliation window and query again before considering a new create. If still absent, transition to a controlled retry decision; preserve the same idempotency key.
10. On 429, honor Retry-After only if it fits the remaining retry/wait budget. Otherwise stop and enqueue/defer; never shorten the server's requested delay.
11. On 403, invalid request, or other permanent error, mark FAILED_FINAL with sanitized classification. Never retry as transient.
12. A retry must recreate the media body/stream from immutable source bytes or a body factory. Never reuse an exhausted stream.

### 4.5 Important Google Drive caveats
- Drive API does not provide a universal server-side idempotency-key header for file creation. The application ledger plus appProperties reconciliation is the idempotency mechanism.
- appProperties search/reconciliation must be scoped to the correct Drive/parent and authorized account; do not assume global visibility.
- A metadata query alone does not prove content equality. Compare stored SHA-256 and size against the source artifact; if the provider response cannot prove content hash, download/read back only when policy and scope permit.
- Filename is descriptive metadata, not the uniqueness key. Never use `name = ...` as the only duplicate check.
- If two concurrent workers race before either sees the other's file, the durable unique operation row/lease is the primary guard; Drive query is the recovery guard.
- Keep an append-only audit record of attempts and reconciliation decisions without logging tokens or meeting content.

## 5. Retry policy contract

Retry is limited to Work 33 Drive operations that are replay-safe or reconciled:
- Transient statuses: 429, 500, 502, 503, 504; bounded by attempt count and total wait budget.
- Retry-After seconds and HTTP-date are parsed against an injected clock for deterministic tests.
- If Retry-After exceeds remaining wait budget, stop/defer. Do not cap it and retry early.
- Exponential backoff uses injected random source and clock/sleeper for deterministic tests.
- Do not retry 400, 401 (except one refresh flow), 403, 404, invalid_grant, or validation/conflict failures as generic transient errors.
- A 401 upload flow allows one refresh and one replay only. A second 401 is terminal.
- OAuth refresh endpoint is not covered by the generic upload retry wrapper. Ambiguous refresh outcomes must not be blindly resent.
- For create/upload, an ambiguous outcome requires reconciliation before any replay.

## 6. Implementation order and gates

1. Work 05: add per-connection single-flight refresh semantics with stale-credential recheck and classified refresh outcomes; add RT-06, RT-08 and RT-14 tests against ConnectionManager.
2. Work 33: locate/restore its canonical storage adapter and test harness in its own Work branch; do not add it to Work 05.
3. Work 33: implement injected retry policy and upload-operation ledger/reconciliation; add RT-01..05, RT-09..13, RT-15..16 against the real adapter.
4. Integrate RT-07 and RT-11/12 across Work 05 + Work 33 with fake provider tests and Core authorization tests.
5. Run focused tests, then combined regression suite, then independent security review.
6. Keep PR #86 Draft/unmerged until real integration and all release gates are evidenced.

## 7. Status

- PASS — repository boundary inspection: Work 05 Python modules and tests were read from the PR head.
- BLOCKED — Work 33 upload adapter: no canonical upload implementation was present in the inspected Work 33 tree, so no production-class integration test can yet be attached.
- BLOCKED — RT-01..RT-16 execution: this document is a mapping/design artifact, not an implementation or test run.
- DECISION — keep OAuth/token lifecycle in Work 05 and Drive upload/retry/idempotency in Work 33. No TypeScript/Vitest/Prisma parallel stack is introduced.
- PR #86 remains Draft and unmerged.
