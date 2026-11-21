# W118-13 / W118-16 — IMPLEMENTATION NOTE: TASK LIFECYCLE & SOURCE BINDING

- **Work:** W118
- **Architecture:** TD-118-012
- **Authority:** Vinh directed Xu to BUILD without waiting for multi-agent review (2026-11-21).
- **Status:** FOUNDATION IMPLEMENTED — EXACT-HEAD CI PASS — RUNTIME INTEGRATION PENDING
- **Branch:** `work/118-auto-e2e-v2`
- **Scope:** first executable foundations for Loop A (Sandbox Task lifecycle) and Loop B (GitHub source-to-Task binding).
- **Non-scope:** no GitHub Issue API mutation, no agent dispatch, no production ACK identity, no push webhook state mutation, no Work 70 write, no merge/release.

---

## 1. W118-13 — Sandbox Task Contract & Lifecycle Registry

**Code:** `scripts/w118/task_lifecycle.py`

### Implemented
- Versioned Task contract `schema_version=1.0` with Work/WP/Task IDs, objective, scope, priority, acceptance criteria, required capabilities, risk, dependencies and owner principal.
- SQLite Task Registry; Task snapshot and append-only `task_events`.
- Explicit state transition graph: DRAFT → READY → ISSUE_LINKED → ASSIGNED → DISPATCHED → ACKED → STARTED → IN_PROGRESS → COMPLETED → VERIFYING → VERIFIED → ACCEPTED → CLOSED; controlled BLOCKED/REJECTED/CANCELLED/EXPIRED recovery paths.
- Actor role allowlist and mandatory `identity_verified=True` from trusted caller; unverified actors fail closed.
- Assignment binding: ACK/START/PROGRESS/COMPLETE must come from the active assigned principal; ACK dispatch ID must match active dispatch.
- Owner binding: Owner transitions must come from the Task's owner principal.
- Required assignment evidence: assignment ID, agent ID, principal, policy version, capability match and evidence reference.
- Required dispatch receipt; ACK nonce is represented only by a reference, not stored raw.
- VERIFIED and ACCEPTED require evidence refs; CLOSED requires positive Issue synchronization readback and evidence reference.
- Optimistic concurrency through expected version; idempotency key + canonical request hash; duplicate identical event is a no-op, key reuse with different payload is rejected.
- Transition detail allowlist prevents a caller from overwriting Task identity, owner, state, version or other protected fields.

### Deliberate limits
- `identity_verified` is a trusted assertion from the caller, not a self-authenticating claim. Runtime principal verification and secure dispatch integration are still required.
- SQLite registry is a library-level local store. ROOM-HOP service endpoint, durable volume/backup, multi-process concurrency policy and operational migration are not wired yet.
- Assignment evidence is recorded as a reference; this module does not independently verify an Agent Registry or runtime capability.

## 2. W118-16 — GitHub Push Source Binding

**Code:** `scripts/w118/source_binding.py`

### Implemented
- Canonical Task branch: `work/{work_id}/task-{task_id}`; no free-form slug, to keep parsing deterministic.
- Required commit trailers, exactly once each:
  - `Work-ID: W118`
  - `Task-ID: W118-TASK-013`
  - `Issue: #65`
- Push payload must match configured repository, `refs/heads/` branch, full 40-character head SHA, non-deleted/non-force-push state, and include the pushed head SHA in the commit list.
- Every commit in a task-scoped push must carry the same Work ID, Task ID and Issue ID as the branch.
- Legacy aggregate branch (for example `work/118-auto-e2e-v2`) returns `UNBOUND_LEGACY_BRANCH`; no Task or Issue is guessed and no state transition is permitted.
- Task-scoped branch with malformed canonical name is rejected.
- Validator result explicitly states `EVIDENCE_ONLY_NO_TASK_TRANSITION`; a validated push is not itself a Task state transition.

### Deliberate limits
- Validator is not yet wired into a GitHub push workflow job or ROOM-HOP event gateway.
- GitHub event authenticity is expected to be supplied by the trusted GitHub Actions event context; a standalone arbitrary JSON file must not be treated as authenticated.
- PR linkage, branch creation, remote ref readback and CI callback reconciliation remain next implementation slices.

## 3. Tests and evidence

- `tests/w118/test_task_lifecycle.py`: lifecycle, authorization, identity, owner/assignment binding, evidence requirements, stale version, idempotency, append-only event history and immutable Task fields.
- `tests/w118/test_source_binding.py`: task branch parsing, legacy branch no-inference, repository binding, commit trailers, mixed Issue rejection, exact head SHA, force-push, deletion and missing commit rejection.
- Existing workflow already triggers contract validation when `scripts/w118/**` or `tests/w118/**` changes.
- First Task-only exact-head validation on `849d84d74571a20bb9c2b1d476c3d7f7584a188c`: 69 tests PASS (CI contract only; event-specific jobs skipped).
- Source-binding test phase exposed a malformed multiline signature, then a missing repository CLI argument and artifact-path mismatch. Each failure was read from the actual GitHub job log and corrected; failed runs are retained as failures, not PASS.
- Source-binding contract exact-head validation on `3136931ddfb56e4574dd3f87a9484f1619693746`: **85 tests PASS / 0.450s**, run [#44876926415](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44876926415), validate SUCCESS.
- Workflow-integrated exact-head validation on `5e131e108a7195ca1ff5ae96b3fadb119e4bc31b`: **86 tests PASS / 0.332s**, run [#44877054701](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44877054701), validate SUCCESS; PR validation [#44877057892](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44877057892) also SUCCESS.
- Artifact ID `14696186741`, SHA-256 `9dae6385ae1e68572305ee6314bf1edf046361fc9993301cc85367603c56531a`. Artifact includes run evidence and source-binding result.
- Push to the existing aggregate branch correctly recorded `source_binding_status=UNBOUND_LEGACY_BRANCH`; this is not a Task-level PASS and no Task state was inferred. Task-specific branch push binding is not yet exercised by a live test.
- All event-specific jobs (handoff, ACK, acceptance review, controlled failure and dispatch) were SKIPPED. Runtime E2E remains NOT VERIFIED.

## 4. Next build slices

1. Wire push source-binding validator into the trusted W118 GitHub Actions push path, preserving legacy branch as explicitly UNBOUND.
2. Build GitHub Issue mirror adapter with create/readback/update idempotency; Sandbox remains Task authority.
3. Add Branch/Commit/PR metadata reconciliation with exact SHA and no automatic Task acceptance.
4. Add runtime dispatch/ACK only after an actual verified Agent principal and permission path exist.
5. Expose the SQLite registry through a ROOM-HOP service adapter and durable storage policy.
6. Add controlled integration tests for CI PASS/FAIL callbacks, duplicate/out-of-order events and exact Task routing.

## 5. Acceptance boundary

This implementation note records code existence and contract scope only. It does not assert full Loop A/B, live runtime E2E, Agent identity readiness, Work 70 integration, product acceptance, merge permission or release.
