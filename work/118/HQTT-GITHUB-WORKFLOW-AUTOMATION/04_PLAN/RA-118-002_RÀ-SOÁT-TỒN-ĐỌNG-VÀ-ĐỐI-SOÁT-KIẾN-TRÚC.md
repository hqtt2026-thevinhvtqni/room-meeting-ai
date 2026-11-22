# RA-118-002 — RÀ SOÁT TỒN ĐỌNG, ĐỐI SOÁT KIẾN TRÚC v1.2 VÀ KẾ HOẠCH ĐÓNG BLOCKER

- **Work:** W118 — HQTT GitHub Workflow Automation
- **Document ID:** RA-118-002
- **Priority:** P0 — architecture/status/evidence reconciliation
- **Read order:** 13
- **Name:** Ka / AI-02
- **Title:** CSA / W118 Delegated Build Owner
- **Date-Time:** 2026-11-21 16:02 +07:00
- **Repository:** hqtt2026-thevinhvtqni/room-meeting-ai
- **Branch:** `work/118-auto-e2e-v2`
- **Issue / PR:** #65 / #67
- **Disposition:** AUDIT RECORDED — PARTIAL REMEDIATION — Xu review required; not acceptance, merge or release.

## 1. Executive finding

W118 has moved from the earlier Auto E2E v2 / locally proposed lifecycle model to the owner-directed **TD-118-012 v1.2 — Sandbox initiates; GitHub controls versioning** baseline. The current implementation correctly narrows W118 to GitHub-specific stateless adapters and evidence. Runtime authority remains with existing Works.

The long-standing blockers are not solved by adding more W118-local infrastructure. They require approved service contracts and real runtime access from Core, W102, W12/W13 and W70. Do not revive the superseded W118-local TaskRegistry, Agent Registry, dispatcher, durable inbox/Event Bus, Execution Host or Git Gateway.

## 2. Evidence inspected

1. Issue #65 and its W118 history/comments.
2. PR #67 and branch `work/118-auto-e2e-v2`.
3. TD-118-012 v1.2, README, STATUS, KH-118-001, TASK_REGISTER.json.
4. W118-13..17 adapter implementation note and test matrix.
5. XR-118-001 review checklist and BB-118-002 handoff.
6. Work Journal through Entry 074.
7. GitHub compare `main...${branch}`, PR review submissions and inline review threads.
8. GitHub Actions runs #44882420198 (push) and #44882422288 (pull_request), jobs, logs and artifacts.

## 3. Verified current evidence

### 3.1 Exact contract CI

- Tested branch SHA: `5f02a9eafbf68eb0bcfca2942733882dab9cc5bf`.
- Push run #44882420198: validate SUCCESS; job log confirms **94 tests / 0.209s**.
- Push event jobs: `handoff-request-capture`, `ack-claim-capture`, `review-observation-capture` = SKIPPED.
- Push artifact: ID `14697683781`; digest `sha256:a2703f70b4a250197b14a84bb5408cef18f2917266f542c7850a54c70e098abc`; present, expires 2026-12-21.
- Source binding: `UNBOUND_LEGACY_BRANCH`; correct fail-closed behavior for the aggregate feature branch; no Task linkage is inferred.
- PR run #44882422288: validate SUCCESS; ACK/review/handoff jobs SKIPPED. PR artifact ID `14698875552`, digest `sha256:97152807cf040ac20b122a5a6e3cb854aa7e211f6df357d66600a1a74c31e2fb`.
- These runs prove contract/unit tests only. They do not prove live Core/W102/W12/W13 runtime, webhook, Issue mirror, dispatch, ACK or full lifecycle E2E.

### 3.2 PR and branch state

- PR #67: OPEN, UNMERGED (latest PR search snapshot); no merge/release performed.
- Formal PR review submissions: 0.
- Inline review threads: 0.
- Branch compare snapshot at 2026-11-21 16:02 +07:00: **440 ahead / 86 behind main; DIVERGED**; merge base `cf2537e07bfd71d5823bd98f8673b3ab5644fcdc`.
- Do not rebase, force-push, merge or bulk-sync the 86 commits without a path-level ownership/security classification and Xu's review. The current compare is a hard integration blocker, not a reason to discard the feature branch.

### 3.3 Work Task Register

Seven planning tasks are present; this register is not Core runtime Task state:

| Task | Status | Mode | Remaining blocker |
|---|---|---|---|
| W118-TASK-013 / Core Task projection | IN_PROGRESS | OWNER_DIRECTED_BUILD | Core API schema/port and approved field map |
| W118-TASK-014 / W102 identity & Assignment | BLOCKED | CORE_AGENT_TASK | Core/W102 port and verified principal |
| W118-TASK-015 / W12/W13 execution | BLOCKED | CORE_AGENT_TASK | Existing Host/Work Authority/CIAdapter not exposed |
| W118-TASK-016 / Issue mirror & source binding | IN_PROGRESS | OWNER_DIRECTED_BUILD | Core lock/API, live GitHub operation and task-scoped push |
| W118-TASK-017 / webhook & Core event adapter | IN_PROGRESS | OWNER_DIRECTED_BUILD | Core Event ingress and production webhook endpoint/secret/TLS |
| W118-TASK-018 / W70 projection | BLOCKED | CORE_AGENT_TASK | W70 schema/owner ACK |
| W118-TASK-019 / full lifecycle acceptance | PLANNED | CORE_AGENT_TASK | Depends on W118-13..18 runtime gates |

## 4. Long-standing findings and disposition

| ID | Priority | Finding | Disposition |
|---|---|---|---|
| F01 | P0 | Previous RA-118-001 proposed W118-owned Agent Registry/dispatcher and independent lifecycle machinery; that conflicts with TD-118-012 v1.2 ownership | SUPERSEDED as implementation proposal. Preserve RA-118-001 historically; v1.2 is current baseline |
| F02 | P0 | Journal ends at Entry 074 and still describes the prior SQLite TaskRegistry/webhook inbox/event reconciler path | Corrected by this Entry 075; future entries must record the stateless refactor and current evidence |
| F03 | P0 | STATUS said exact-head CI was pending despite run #44882420198 and 94-test log | STATUS updated with verified run/artifact and explicit runtime limitation |
| F04 | P0 | Branch DIVERGED 440/86 | BLOCKED for integration; no unsafe rebase/merge |
| F05 | P0 | Core Task API, approved field map, per-Task lock and Event ingress unavailable | BLOCKED on Core owner; W118 adapters remain unbound/stateless |
| F06 | P0 | W102 identity/Assignment/dispatch/ACK cannot be verified; role-map does not provide an executor identity | BLOCKED; do not infer GitHub login or fake positive ACK |
| F07 | P0 | W12/W13 execution Host, GitHub Gateway and CIAdapter not exposed | BLOCKED on W12/W13; do not build parallel host/gateway |
| F08 | P0 | W70 Evidence Register/Dashboard integration lacks schema/owner approval | BLOCKED; read-only mapping proposal only; no W70 schema write |
| F09 | P0 | Runtime event jobs skipped; no live Issue round-trip, task-specific push, production webhook, Core event persistence or full E2E | NOT VERIFIED; requires authorized integration test after dependencies are exposed |
| F10 | P0 | Xu formal review and Go QE evidence absent; review endpoint currently has zero submissions/threads | PENDING; Xu review and independent QE are separate gates; identity/access must be verified, not guessed |
| F11 | P1 | Work Task Register tasks marked IN_PROGRESS while external runtime blockers remain | Valid only as owner-directed implementation progress; do not interpret as runtime completion or percent progress. Keep blockers explicit |

## 5. Architecture alignment / build decisions

1. Keep TD-118-012 v1.2 as the implementation baseline.
2. Keep W118-13/16/17 as stateless adapter contract work; bind them only when owning services expose approved ports.
3. Keep W118-14/15/18 BLOCKED until W102/Core, W12/W13 and W70 dependencies are available.
4. Do not restore superseded SQLite TaskRegistry, webhook inbox/event reconciler or GitHub-login authorization. Core owns runtime Task/Assignment/Event and deduplication; W102 owns Agent policy; W12/W13 own execution/Git/CI.
5. Keep Issue, ACK, push, CI and review as observations until Core/W102 makes an authorized state transition.
6. Treat `UNBOUND_LEGACY_BRANCH` as safe and expected on the aggregate branch; next push proof must use a task-scoped branch with exact Work/Task/Issue/SHA binding.
7. No credentials, repository secrets, branch protection, permissions, Work70 schema, merge or release changes are authorized by this report.

## 6. Closure plan — dependency-driven

| Order | Priority | Owner | Closure action | Evidence required |
|---|---|---|---|---|
| 1 | P0 | Ka | Keep current stateless code/test contract stable; reconcile journal/status and exact CI evidence | Exact branch SHA, run log, artifact digest, readback |
| 2 | P0 | Core owner / Xu coordination | Expose Task read schema, approved field map, per-Task lock and Event ingress contract | Owner-approved schema, authenticated read/lock/event round-trip |
| 3 | P0 | W102 + Identity owners | Expose verified principal, assignment/dispatch/ACK APIs and positive/negative fixtures | Principal-bound dispatch/ACK event trace |
| 4 | P0 | W12/W13 | Expose Work Authority, execution host, GitHub Gateway and CIAdapter | Real execution ID, exact branch/commit/push and CI callback |
| 5 | P0 | W70 owner | Approve read-only Evidence Register/Dashboard mapping | Written schema/owner ACK and parity/readback evidence |
| 6 | P0 | Ka + Xu + QE | Run task-scoped end-to-end and adversarial tests after all ports are available | Handoff/ACK deny+allow, push, CI, failure/retry, event dedupe, evidence and runtime logs |
| 7 | P0 | Xu then Vinh | Independent review, then Vinh product acceptance; release remains a separate decision | Exact-SHA review disposition and Vinh acceptance record |

No implementation can safely close F05–F09 by guessing service APIs, identities, secrets or permissions. Record those as BLOCKED until the owner supplies the required contract/runtime.

## 7. Required Xu attention

Xu should review:
- Whether TD-118-012 v1.2 is the controlling baseline and RA-118-001 is now historical/proposal-only.
- The 440/86 branch divergence and safe integration strategy.
- The exact 94-test contract evidence versus skipped runtime jobs.
- The unresolved Core/W102/W12/W13/W70 dependencies and order of closure.
- The absence of formal PR review and independent QE evidence.

## 8. BIÊN BẢN

- **Name:** Ka / AI-02
- **Title:** CSA / W118 Delegated Build Owner
- **Date-Time:** 2026-11-21 16:02 +07:00
- **Result:** Completed GitHub audit, verified 94 contract tests and artifact, identified integration divergence and runtime dependency blockers; reconciled current STATUS and journal.
- **Disposition:** PARTIAL REMEDIATION — W118 ACTIVE / NOT ACCEPTED / NOT RELEASED.
- **Xu independent review:** PENDING.
- **Vinh product acceptance / release:** NOT REQUESTED.

## Addendum v1.3 — Owner contract intake and evidence closure matrix

- **Document ID:** RA-118-002 (controlled addendum v1.3)
- **Priority:** P0 — unblock cross-Work integration without inventing authority.
- **Read order:** 14
- **Name / Title:** Ka / AI-02 — CSA / W118 Delegated Build Owner.
- **Date-Time:** 2026-11-23 02:39:57 +07:00.
- **Canonical implementation candidate:** PR #68, branch work/118-auto-e2e-v2-clean, audited HEAD 225ba620ad7698bd39cab250f8f50c1f6bd52383.
- **Architecture baseline:** TD-118-012 v1.3; W118 remains stateless GitHub adapters and evidence normalization. Existing Work owners retain authority and persistence.

### A. Contract intake matrix

| ID / owner | Minimum owner-supplied contract | Required negative/security semantics | Evidence required before W118 binds | Current state |
|---|---|---|---|---|
| DEP-CORE-01 / Core :8000 | Versioned Task read DTO/schema; canonical Task ID and Work ID; approved field map; authenticated read port; source revision/freshness | Unknown fields/schema version fail closed; stale/missing Task rejected; read-only adapter cannot mutate Task state | Owner approval + authenticated read of one non-sensitive pilot Task + exact response and source revision | BLOCKED / NOT VERIFIED |
| DEP-CORE-02 / Core :8000 | Lease issuer identity; signed/authenticated lease validation API; Task+Work binding; audience; expiry; revocation; lock scope; validation response | Wrong Task/Work, expired, revoked, wrong audience, forged, replayed or unavailable validator must reject before GitHub POST/PATCH | Core-issued positive and negative lease fixtures + authenticated validator trace + GitHub mirror no-write-on-reject proof | BLOCKED; P1-118-02 |
| DEP-CORE-03 / Core :8000 | Event-intent ingress DTO; authenticated producer contract; idempotency/delivery key; Core-assigned event ID/sequence/time; retry/readback behavior | Duplicate/replay/out-of-order delivery is idempotent/deferred; CI never changes Task acceptance; W118 does not assign sequence or persist an inbox | Owner-approved schema + signed event ingress/readback + duplicate/replay/out-of-order traces | BLOCKED / NOT VERIFIED |
| DEP-W102-01 / W102 + Identity owners | Canonical source/ref and hash; verified principal schema; Agent identity proof; policy decision; Assignment create/read contract; ACK actor binding | GitHub username/comment/label is not principal proof; wrong Agent/Task, expired grant, replayed or unauthenticated ACK denied | Owner-approved source parity + verified principal fixture + positive/negative Assignment and ACK traces tied to Core Task ID | BLOCKED; Gate A in W102 currently BLOCKED |
| DEP-W14-01 / W14 | Current canonical source/ref/hash; Work Authority contract; ExecutionHostBridge/HostPort contract; execution request/result schema; GitHub Gateway and CI callback ownership | No parallel W118 host/gateway; unauthorized Work, wrong execution, stale SHA, duplicate request or failed execution cannot be reported PASS | W14 owner approval + live health/readback + one authorized non-sensitive execution with execution ID, exact commit SHA, result and failure-path trace | BLOCKED / NOT VERIFIED |
| DEP-W33-01 / W33 | Current canonical artifact lineage/version/ref/hash; authenticated evidence-ingress API/CLI contract; evidence ID, content digest, provenance and source-actor fields | No treating local CLI/E2E report as live ingress; tampered digest, missing provenance, duplicate or unauthorized source rejected | W33 owner decision on v0.1/v0.2 lineage + authenticated ingress/readback of one test evidence item + digest/provenance verification | BLOCKED / NOT VERIFIED |
| DEP-W70-01 / W70 | Current schema version/hash; written owner ACK; approved W118-to-W70 field mapping; read-only projection endpoint and access model | No W118 schema/register writes; no second Evidence Register; no Dashboard write-back; unknown fields rejected | W70 owner ACK + schema validation + source-to-projection parity/freshness trace + proof projection cannot mutate canonical Task/Register | BLOCKED; no W118 write authority |

### B. Integration sequence (strict dependencies)

1. **Source authority first:** each owner identifies canonical branch/ref/commit and content hash, and explicitly states whether that source is approved/current. Sandbox listing is inventory only; it cannot replace source readback or owner attestation.
2. **Contract second:** owner supplies versioned schema, authentication, authorization, error, retry and idempotency semantics. W118 records the exact contract version and owner approval before coding the binding.
3. **Runtime proof third:** owner executes or authorizes a non-sensitive pilot; capture exact endpoint/service identity, actor/principal, request/correlation IDs, timestamps, exact source SHA, response/readback and negative cases. Do not put secrets or tokens in the evidence record.
4. **Adapter binding fourth:** Ka adds only a stateless W118 adapter against the approved port; no local authority, persistence, queue, registry, host, secret or policy substitute.
5. **Cross-work E2E fifth:** Xu/QE verifies Plan → Core Task → W102 Assignment/verified ACK → W14 execution → GitHub push/CI → Core event reconciliation → W33 evidence ingress → W70 read-only projection. Missing any hop means E2E remains NOT RUN/BLOCKED, not partial PASS.
6. **Acceptance last:** independent Xu review, independent QE evidence and Vinh's explicit product acceptance remain distinct from CI, PR review, merge and release.

### C. No implicit permission / no false inference

- A branch name, Sandbox directory listing, old release snapshot, README claim, unit test, mock, local callback stub, GitHub account identity or successful CI job does not grant cross-Work authority.
- If an owner has no API/service or cannot attest source parity, record NOT PROVIDED / NOT VERIFIED and retain the blocker. Do not invent an endpoint, port, credential, schema or runtime behavior.
- W118 may prepare DTO mapping drafts and test vectors, but cannot execute a real external integration until owner authorization and authenticated runtime access exist.

### D. PR inventory control

- PR #68 is the current clean implementation/review candidate.
- PR #67 is CLOSED / UNMERGED and superseded by #68.
- PR #66 remains OPEN / UNMERGED as the historical pilot. Existing owner comment explicitly says keep it as a historical pilot until Xu confirms whether it should be closed. Do not close or merge #66 without that confirmation; preserve its branch/history.

### E. Current gate decision

- W118 contract/unit CI: PASS at tested exact SHAs only (102 tests); aggregate branch source binding remains UNBOUND_LEGACY_BRANCH; PR source binding remains NOT_RUN.
- P1-118-01: PASS at adapter-contract level only.
- P1-118-02: BLOCKED pending DEP-CORE-02.
- W118-TASK-013/014/015/016/017/018 runtime bindings: IN PROGRESS or BLOCKED as recorded in TASK_REGISTER; no status is promoted by this matrix.
- W118-TASK-019 Runtime Auto E2E: NOT RUN / BLOCKED until all mandatory owner contracts and runtime evidence pass.
- Xu review: PENDING. Vinh acceptance: NOT ACCEPTED. Main merge/release: NOT DONE.

### BIÊN BẢN — Addendum v1.3

- **Name:** Ka / AI-02
- **Title:** CSA / W118 Delegated Build Owner
- **Date-Time:** 2026-11-23 02:39:57 +07:00
- **Result:** Converted cross-Work blockers into owner-specific contract intake, security semantics, exact evidence requirements and ordered integration gates. No external Work source/runtime/permission/secret changed.
- **Disposition:** ACTIVE — BLOCKED — NOT ACCEPTED — NOT RELEASED.