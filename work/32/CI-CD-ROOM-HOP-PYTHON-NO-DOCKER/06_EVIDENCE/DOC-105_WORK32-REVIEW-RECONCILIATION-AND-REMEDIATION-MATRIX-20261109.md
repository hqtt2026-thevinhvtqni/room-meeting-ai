# DOC-105 — Work32 Review Reconciliation & Remediation Matrix

- **Document Number:** DOC-105
- **Priority:** P0 — Xu/CTO-directed remediation before integration/release
- **Name:** Ka
- **Title:** CSA / Delegated Work32 Execution Owner
- **Date-Time:** 2026-11-09 (Asia/Ho_Chi_Minh)
- **Source branch:** `work/32-main-integration-20261109`
- **Source HEAD reviewed:** `f0a8e55bc16ed27b6c43fa51164bc9e8f74253ef`
- **Baseline:** Run #251 / `42518174608` — all six jobs SUCCESS on the exact source head
- **Status:** SOURCE MIRROR PASS — REMEDIATION NOT YET IMPLEMENTED — ACTIVE / NOT RELEASED

## 1. Reviewer decisions reconciled

### Xu — W32-LOG-20261109-XU-03
- D-102-03: Public MCP V1 is exactly four tools: `list_meetings`, `get_meeting`, `get_transcript`, `add_paste_to_meeting`. `join_meeting` / `start_meeting` remain Core lifecycle operations.
- D-102-04: Every paste must require active `JOIN_ACCEPTED` membership. Registry resolution alone is insufficient; default behavior fails closed.
- D-102-05: `identity_id` is not authentication. Local tests are stdio/loopback + disposable data only. Before untrusted exposure: TLS, short-lived signed bearer credentials, server-derived principal, identity binding, authenticated-principal quota, retire/gate anonymous path, protect `GET /identities`, explicit CORS and audit.
- D-102-06: SQLite remains same-host/local-filesystem only. Reserve quota in a short committed transaction, append transcript outside the lock, compensate the exact reservation on append failure; map lock timeout to controlled 503 + Retry-After.
- D-102-07: Browser Adapter remains loopback-only. Fix SSRF/redirect/private-address checks, path confinement, Chromium sandbox, URL query/fragment redaction, lifecycle actor trust and structured MCP rate-limit errors before staging.

### Cla — W32-EVIDENCE-017
- Local/single-host CI testing: conditionally acceptable under stdio/loopback, disposable store, and no claim that `identity_id` is authentication.
- Browser Adapter reachable beyond trusted loopback: not acceptable until S1/S2/S2b and identity boundary are fixed.
- Staging/production/multi-host: not acceptable yet.
- Findings S1–S10 recorded; S7/S8 were explicitly UNVERIFIED by Cla because required sources were missing from the review snapshot. Ka has now retrieved the missing source files from the exact PR branch and mirrored them below; S7/S8 still require code-path disposition and tests.

### Qw — evidence retrieval disposition
- The Work32 Sandbox did not contain a separately attributable Qw W32 product-QE report at the time of Xu-03.
- The Qw report found in Work 70 is explicitly scoped to Work70 Dashboard, dated 2026-11-07; it is not W32 product QE and is not substituted for W32 evidence.
- W32 Qw findings remain **PENDING SOURCE / TRACEABILITY**. Ka must obtain the original Qw report or its exact Work/meeting/source reference, preserve its author/build/SHA/scenario/results, and reconcile it without rewriting Qw's conclusions.

## 2. Exact source mirror — 11/11 byte-for-byte readback PASS

Read-only source copies are stored under:
`06_EVIDENCE/SOURCE_MIRROR_PR49_20261109/`

Manifest: `06_EVIDENCE/DOC-104_WORK32-PR49-SOURCE-MIRROR-MANIFEST-20261109.md`

All 11 mirrored files were fetched from the exact PR branch and independently read back from Sandbox with byte-for-byte equality:
- Core: `meeting_service.py`, `context_loader.py`, `identity_resolution.py`, `secretary.py`, `agent_registry.py`, `principal_registry.py`, `meeting_manager.py`, `paste_rate_limiter.py`.
- Adapters: MCP `server.py`, HTTP `http_server.py`, Browser Adapter `adapter.py`.

Notable current-source findings:
1. **S4 confirmed:** `Meeting.add_paste()` checks active meeting and resolves identity, but does not check active `JOIN_ACCEPTED` membership; `identity_id` remains optional and anonymous legacy paste is accepted. This conflicts with Xu D-102-04 and must be changed with explicit positive/negative tests.
2. **S5 confirmed:** `SQLitePasteRateLimiter.admission()` opens `BEGIN IMMEDIATE` and returns a live connection; `Meeting.add_paste()` calls `Secretary.append()` before `admission.commit()`. The database write lock therefore spans transcript I/O.
3. **S6 confirmed:** MCP `call_tool()` does not translate `MeetingRateLimitError` into a structured tool error. HTTP route already emits 429 + Retry-After.
4. **S9 confirmed:** Browser workflow stores `final_url` and `page_title` in evidence and sends both to meeting transcript without visible query/fragment redaction.
5. **S1/S2/S2b confirmed in current branch source:** Browser `navigate()` accepts arbitrary URL; screenshot/download/work-id names are joined to evidence paths without visible confinement; Chromium launch includes `--no-sandbox`.
6. **S3 confirmed in HTTP source:** lifecycle routes accept actor/identity strings from request bodies; no transport-auth principal is established by those fields.
7. **S7 confirmed for further remediation:** `MeetingManager.get_meeting()` and explicit creation compose `meetings_dir / meeting_id`; the current source does not visibly validate the identifier before path use.
8. **S8 confirmed for further remediation:** `context_loader.validate_context_files()` joins caller-selected names to `CONTEXT_DIR`; `package_context()` copies them without basename/containment validation.
9. **Xu semantic issue:** `MeetingManager.join()` writes `auth_verified: True` after registry resolution. This overstates the transport-authentication boundary. Consumer trace and a separately reviewed semantic correction are required; do not reinterpret the field silently.

## 3. Remediation matrix and execution order

| Priority | Finding / decision | Required action | Owner | Acceptance evidence |
|---|---|---|---|---|
| P0-A | Source provenance / S7-S8 | Mirror core/service/identity/registry sources and trace path validation | Ka | 11/11 byte-identical source mirror; blob SHA manifest |
| P0-B | Qw product QE | Retrieve original W32 QE report; map each finding to S1-S10 and Xu decisions | Ka + Qw | Original report/source, author/date/SHA, scenarios and raw results |
| P0-C1 | S4 / D-102-04 | Require active JOIN_ACCEPTED participant before any paste; fail closed | Ka | accepted participant PASS; non-member/pending/rejected/closed FAIL |
| P0-C2 | S5 / D-102-06 | Short committed reservation transaction; append outside lock; compensate exact event on append failure; map lock timeout to 503 + Retry-After | Ka, Cla consult | concurrency, compensation, timeout and quota-boundary tests |
| P0-C3 | S6 | Return structured MCP tool error with retry guidance; preserve HTTP 429 contract | Ka | MCP stdio contract tests + HTTP regression |
| P0-C4 | S9 | Redact URL query and fragment before transcript/evidence persistence | Ka, Cla review | token-in-query/fragment regression test |
| P0-D1 | S1/S2/S2b | URL scheme + redirect + DNS/IP range controls; safe output basename and resolved-path confinement; review/remove Chromium --no-sandbox | Ka with Cla review | SSRF/redirect/private IP/path traversal/absolute path/sandbox tests |
| P0-D2 | S3 + auth_verified | Trace all consumers; remove misleading auth claim; do not treat caller actor strings as authenticated principal | Ka with Cla review | consumer map, semantic tests, security re-review |
| P0-D3 | S7/S8 | Validate meeting IDs and context file names; reject absolute/traversal paths and prove resolved path remains within approved roots | Ka | path traversal/absolute-path tests and positive nested-name policy |
| P1 | Remote authentication | Separate ADR/design for TLS + signed short-lived credentials, server principal binding, CORS/audit/registry protection | Xu/Cla; Vinh approves exposure | reviewed ADR + exact-SHA tests; no remote exposure before approval |

## 4. Baseline and boundaries
- Run #251 (`42518174608`) completed all six jobs successfully on source head `f0a8e55bc16ed27b6c43fa51164bc9e8f74253ef`.
- This is the pre-remediation CI baseline, not evidence that S1–S10 are fixed.
- Keep PR #49 DRAFT and main unchanged.
- Browser Adapter and Core HTTP remain loopback-only; tests use disposable data only.
- Do not touch the PC runner, WORK09 process, port 8787, PATH, service account, or repository variables under this directive.
- No staging, production, CD/G7, merge, or release.

## 5. Next execution
1. Complete Qw source retrieval/traceability without substituting the Work70 report.
2. Capture exact-SHA test baseline and focused current-source tests for S4/S5/S6/S9/S1/S2/S2b/S3/S7/S8.
3. Implement Xu-authorized S4/S5/S6/S9 and path hardening on an isolated Work32 branch; obtain Cla review for S1/S2/S2b/S3 and the `auth_verified` semantic correction.
4. Run focused tests, then full CI on the exact resulting SHA.
5. Request Qw independent retest and Cla security re-review; return to Xu/Vinh with evidence-based gate disposition.

## BIÊN BẢN
- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-09 (Asia/Ho_Chi_Minh)
- **Decision:** Reconciled Xu and Cla review results; source mirror is 11/11 byte-identical. Qw W32 report remains pending retrieval. No code or release gate claimed PASS.

## NHẬT KÝ
- **W32-LOG-20261109-94**
- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-09 (Asia/Ho_Chi_Minh)
- Read Xu-03 and Cla W32-EVIDENCE-017; found Qw's available report belongs to Work70 Dashboard, not W32.
- Retrieved and read back 11 source files from PR #49 exact branch; all 11 were byte-for-byte equal to GitHub source.
- Confirmed current source reproduces S4, S5, S6, S9, S1, S2, S2b, S3, S7 and S8 findings; recorded remediation owners and acceptance evidence.
- Run #251 all six jobs PASS is recorded as pre-remediation baseline only.
- No source code, main, runner, PC process, staging, production or release changed.


## Addendum — Cla S10 disposition
- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-09 (Asia/Ho_Chi_Minh)
- Cla S10 identifies non-atomic meeting.yaml read-modify-write and non-atomic ID allocation.
- This finding was not included in the first remediation batch and is **OPEN**. Do not claim full S1–S10 closure.
- Follow-up: implement atomic meeting.yaml replacement with appropriate same-process serialization; make generated ID reservation retry-safe using atomic directory creation; add concurrent update/allocation tests. Cross-process consistency must be separately proven or deployment constrained to one Core process.
- Owner: Ka. Cla re-review required before staging/production.


## Addendum — S10 implementation submitted for exact-SHA CI
- Atomic YAML replacement now writes a per-thread temporary file, flushes/fsyncs, then os.replace()s the meeting.yaml.
- A process-wide per-meeting RLock serializes read-modify-write operations across Meeting instances in the same Core process.
- Generated meeting IDs use a process lock for allocation and atomic directory creation with collision retry.
- Added tests for concurrent ID allocation, concurrent JOIN_ACCEPTED updates from separate Meeting objects, and atomic YAML replacement.
- **Residual:** meeting.yaml read-modify-write is not yet cross-process serialized. Deployment must remain one Core process per local store until a cross-process lock or transactional state store is implemented and reviewed.
- CI status for this S10 batch: pending Run #274 (`42522244216`) on head `fb7eadcc59bf22d4a91060e738760b4d5380c2fd`; do not mark S10 PASS until that exact run completes.


## Addendum — S10 acceptance boundary after Run #277
- Run #277 (`42522681112`) passed 6/6 on exact PR head `d72b68659e9717d8ea33a5c41b2d379fc15064e2`.
- S10 is **PASS within the single-Core-process local deployment boundary**: atomic YAML replacement, same-process per-meeting serialization, atomic ID directory reservation/collision retry, and concurrency tests all passed.
- Cross-process read-modify-write is still **OPEN**. No multi-process or multi-host deployment; use one Core process per local meeting store until cross-process locking/transactional storage is reviewed.
- Cla re-review remains required before staging/production.
