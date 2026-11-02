# DOC-065 — HỢP ĐỒNG ĐIỀU PHỐI GIAO VIỆC AI KẾT HỢP
- **STT / Document ID:** DOC-065
- **Priority:** P0
- **Read order:** 65
- **Depends on:** DOC-043; DOC-044; DOC-057; DOC-064
- **Status:** DRAFT — CONTRACT PROPOSAL / NOT IMPLEMENTATION APPROVED
- **Version / Updated:** 1.0 / 2026-11-02
- **Owner:** Xu / AI-01
- **Authority:** Vinh

## 1. Contract scope
Định nghĩa logical interface độc lập provider cho AI Registry, Assignment, Dispatch, ACK, Progress, Delivery và Review. Đây là contract proposal; không khẳng định API route, database hoặc Core service đã tồn tại. Khi tích hợp phải map vào convention và auth model thực tế của Core.

## 2. Identifiers
- `work_id`: Work identity canonical.
- `wp_id`: Work Package identity.
- `assignment_id`: stable assignment identity; unique within system.
- `dispatch_id`: one delivery attempt group; retry attempt has its own attempt_id.
- `attempt_id`: unique transport attempt.
- `ai_id`: roster identity, not authentication proof.
- `adapter_id` / `adapter_mode`: selected channel.
- `session_ref`: opaque provider/session locator; never secret or raw cookie.
- `event_id`: globally unique event identity.
- `idempotency_key`: stable key for a command retry.
- `correlation_id`: end-to-end trace identifier.

## 3. Assignment payload (logical JSON)
```json
{
  "schema_version": "1.0",
  "assignment_id": "A70-0001",
  "work_id": "70",
  "wp_id": "WP-70-01",
  "title": "Implement approved lifecycle module",
  "objective": "Deliver the agreed outcome",
  "issuer": {"principal_ref": "xu-ai-01"},
  "assignee": {"ai_id": "co-ai-07", "role": "coder"},
  "reviewer": {"ai_id": "qw-ai-05", "independent": true},
  "priority": "P1",
  "status": "READY",
  "source_baseline": {
    "repository": "canonical-repository",
    "branch": "work/70/...",
    "commit": "full-commit-sha",
    "working_tree": "clean"
  },
  "scope": {
    "read": ["declared paths"],
    "write": ["declared paths"],
    "execute": ["declared commands"],
    "network": [],
    "prohibited": ["out-of-scope changes", "secret disclosure"]
  },
  "inputs": [{"ref": "DOC-064", "version": "1.0"}],
  "deliverables": [{"id": "D1", "kind": "source", "required": true}],
  "acceptance_criteria": [{"id": "AC1", "condition": "observable condition", "evidence_required": true}],
  "dependencies": [],
  "due_at": null,
  "permission_grant_ref": "grant-reference",
  "created_at": "2026-11-02T00:00:00Z",
  "expires_at": null
}
```
Values above are illustrative only, not live assignment or credentials.

## 4. Dispatch command
Request:
- assignment_id, assignment_version
- dispatch_id, attempt_id
- adapter_id, adapter_mode
- target_ref/session_ref (opaque, optional according to mode)
- payload_ref or signed payload digest
- idempotency_key
- issued_at, expires_at, correlation_id

Response:
- attempt_id, transport_status, adapter_receipt_ref
- provider_message_ref when actually returned
- delivered_at when provider confirms delivery
- retryable, stable_error_code
- observed_at

Transport status enum:
`CREATED | SEND_ATTEMPTED | DELIVERED | DELIVERY_UNKNOWN | DELIVERY_FAILED`.

Rules:
- DELIVERED requires adapter/provider delivery confirmation; HTTP request accepted alone is not proof unless connector semantics explicitly define it.
- DELIVERY_UNKNOWN must be reconciled before retry to avoid duplicate task delivery.
- SESSION_HANDOFF returns HANDOFF_READY, not DELIVERED; user-mediated transfer is recorded separately as HANDOFF_SUBMITTED only after receipt.
- No target/session proof => reject dispatch or create a manual handoff packet; never guess target.

## 5. ACK contract
AI response:
- event_id, assignment_id, dispatch_id, attempt_id
- ai_id, identity_proof_ref (or manual_receipt_ref)
- decision: `ACCEPT | REJECT | NEED_CLARIFICATION`
- accepted_scope_digest
- acknowledged_at
- estimated_next_update_at
- reason_code / note (required for reject or clarification)
- nonce/challenge_ref where enabled

Only verified connector identity or an explicitly classified manual receipt can create ACKNOWLEDGED. A typed AI ID alone is not proof. Manual ACK is labeled `MANUAL_ATTESTED`, not cryptographically verified. No ACK => remain DISPATCHED or DELIVERY_UNKNOWN depending on transport evidence.

## 6. Progress contract
- event_id, assignment_id, ai_id, sequence
- progress_state: `IN_PROGRESS | BLOCKED | READY_FOR_REVIEW`
- summary, completed_items, remaining_items
- blocker: code, description, owner, next_action
- source_revision, evidence_refs
- occurred_at, received_at, provenance

Sequence must be monotonic per assignment/producer. Duplicate event_id is ignored; conflicting duplicate is rejected/audited. Progress cannot mutate Work/Gate state.

## 7. Result / handoff contract
Required:
- assignment_id, ai_id, result_version
- outcome: `COMPLETED | PARTIAL | BLOCKED | FAILED`
- summary, changed_files, start_revision, end_revision
- branch, commit_or_pr
- commands_run and exact raw outcomes
- tests with `PASS | FAIL | NOT_RUN | BLOCKED`
- evidence_refs, artifact_hashes, known_gaps
- sync_state: `NOT_SYNCED | LOCAL_ONLY | PUSHED | VERIFIED`
- submitted_at, provenance

A completion claim only moves assignment to IN_REVIEW. DONE requires independent review plus authorized closure.

## 8. Review contract
- review_id, assignment_id, reviewer_ai_id
- independence_check
- acceptance_results (AC ID, PASS/FAIL/NOT_VERIFIED, evidence ref)
- test_results (raw output ref)
- findings, severity, disposition
- review_decision: `APPROVE | REQUEST_CHANGES | BLOCKED`
- reviewed_at, signature/provenance

Author and reviewer must differ unless explicitly downgraded to SELF_CHECK (never independent QE). Reviewer cannot change implementation evidence or authoritative Work/Gate status.

## 9. Error model
Stable categories:
- `INVALID_ASSIGNMENT`, `NOT_READY`, `DEPENDENCY_BLOCKED`, `CAPABILITY_UNVERIFIED`
- `ADAPTER_UNAVAILABLE`, `TARGET_UNVERIFIED`, `AUTH_FAILED`, `FORBIDDEN`
- `DELIVERY_FAILED`, `DELIVERY_UNKNOWN`, `ACK_TIMEOUT`, `ASSIGNMENT_EXPIRED`
- `IDEMPOTENCY_CONFLICT`, `VERSION_CONFLICT`, `REPLAY_REJECTED`
- `EVIDENCE_INVALID`, `REVIEWER_NOT_INDEPENDENT`, `COST_APPROVAL_REQUIRED`.

Error response: code, safe_message, retryable, retry_after, assignment_version, attempt_id, correlation_id. Never include secrets or raw credentials.

## 10. Event envelope
Every event has:
`event_id, event_type, schema_version, work_id, wp_id, assignment_id, actor_ref, producer_ref, occurred_at, received_at, sequence, correlation_id, causation_id, payload_digest, provenance, evidence_refs`.
Audit is append-only. Consumer deduplicates by event_id. Event ordering uses assignment sequence, not wall-clock alone.

## 11. Security and privacy
- Authenticated principal comes from trusted adapter/Core context, never caller-supplied actor text.
- Manual receipt remains lower-assurance and explicitly labeled.
- Callback signature, timestamp, nonce and assignment binding required for automated ingress.
- Scope and expiry checked at dispatch and before privileged actions.
- Secrets only in secret manager/connector-managed auth; never in prompts, handoff files or logs.
- Redact sensitive conversation content; store only task-relevant extracts and provenance.
- API adapter requires explicit cost approval and usage telemetry.

## 12. Versioning and compatibility
- Schema version is explicit.
- Additive optional fields are backward-compatible.
- Enum additions require consumer compatibility review.
- Breaking changes require new major version and migration plan.
- Unknown fields rejected at trust boundary unless extension namespace is explicitly allowed.
- Contract route names are intentionally omitted until Core owner approves actual routing convention.

## 13. Acceptance invariants
1. No READY assignment => no dispatch.
2. No verified capability => no automated adapter selection.
3. No delivery proof => no DELIVERED.
4. No verified ACK/marked manual receipt => no ACKNOWLEDGED.
5. No result evidence => no IN_REVIEW.
6. No independent approval => no DONE through normal path.
7. No reviewer authority => no Work Gate PASS/RELEASE.
8. Same idempotency key + same payload => at most one effect.
9. Same key + changed payload => conflict.
10. Expired/revoked grant => deny.
11. Unknown provider/session => no blind retry.
12. API cost approval absent => API adapter unavailable.

**Disposition:** Contract proposal only. Requires Core owner mapping, security review, schema validation, and independent QE before implementation approval.
