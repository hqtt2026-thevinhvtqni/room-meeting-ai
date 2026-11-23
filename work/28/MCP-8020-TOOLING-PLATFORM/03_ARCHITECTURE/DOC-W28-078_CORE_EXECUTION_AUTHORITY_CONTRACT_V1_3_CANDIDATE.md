# WORK 28 — CORE EXECUTION AUTHORITY CONTRACT V1.3 (CANDIDATE)

**Document ID:** DOC-W28-078  
**Work:** Work 28 — MCP-8020-TOOLING-PLATFORM  
**Priority:** P0 — authorization boundary / integration blocker  
**Status:** CANDIDATE — NOT APPROVED / NOT WIRED / NOT DEPLOYED  
**Author:** Ka — owner-delegated BUILD OWNER / CSA  
**Date:** 2026-11-23  
**Target review:** Xu / Vinh  
**Supersedes:** No document. This candidate supplements, but does not supersede, PR #74 V1.3 or Architecture Decision V2.

## 1. Purpose and non-goals

Define a versioned, testable wire contract for Core-authorized Work execution. The contract must let the approved W14 Execution Host validate a short-lived grant online, derive execution context from Core, and persist a correlated run outcome without trusting caller-supplied WorkContext.

This document is a candidate contract only. It does not authorize:
- adding routes to production Core :8000;
- starting or deploying a separate authority service on :8001;
- routing to the historical MCP :8020 listener;
- treating Work28's current `core/execution_authority/` package as canonical Core;
- using Work28 `execution_host/` as a replacement for W14 Host;
- executing a command, opening the execution gate, or releasing Work 28.

## 2. Authority and component ownership

| Component | Normative responsibility | Prohibited responsibility |
|---|---|---|
| Core :8000 | Sole identity, Work, assignment, policy, gate, grant, revocation and run-ledger authority | Delegating final authorization to MCP or Host |
| MCP Build/Verification :8030 | Build/verification orchestration; submit a bounded execution request after Core authorization | Issuing grants, inventing WorkContext, direct Host shell access |
| Runtime MCP (new clean deployment) | Runtime-facing MCP adapter with a distinct enrolled service identity | Reusing historical :8020 process/state or becoming an authority |
| W14 Execution Host | Sole process execution boundary; online grant validation; OS containment; report run outcome | Creating/altering WorkContext, deciding Work policy, accepting caller-provided authority |
| W70 | Authoritative Work/Gate lifecycle and policy snapshot source | Being replaced by static Work28 configuration |

**Integration rule:** all normative endpoints below are routes mounted inside the existing Core :8000 application composition, under its authentication, middleware, lifecycle, logging and deployment ownership. A separate :8001 process is not a conforming implementation. Until Core ownership and composition are reconciled, these routes remain unimplemented.

## 3. Protocol conventions

- Contract identifier: `room-hop.core.execution-authority`.
- Version: `1.3.0`; media type: `application/vnd.room-hop.execution-authority.v1+json`.
- Transport: HTTPS only. No redirect is permitted for authenticated requests. TLS identity must be bound to an enrolled service principal; the existing custom identity header alone is not sufficient proof of transport identity.
- Every request carries `request_id` (UUID), `sent_at` (UTC RFC3339), and `contract_version`.
- Every response carries `request_id`, `contract_version`, `status`, and `server_time`.
- IDs are opaque, case-sensitive strings. SHA-256 values are exactly 64 lowercase hexadecimal characters.
- Unknown fields are rejected for authority-bearing request objects. Missing, stale, ambiguous, malformed or unavailable authority data fails closed.
- Secrets and bearer tokens must never be logged, returned by status/readback, placed in CI artifacts, or persisted in plaintext.

## 4. Grant issuance

### 4.1 Request

`POST /api/v1/execution/grants`

Caller: enrolled MCP Runtime/Build service identity, authenticated by Core's approved service-authentication mechanism.

Required JSON fields:
- `request_id`: UUID
- `contract_version`: `1.3.0`
- `work_id`: canonical Work identifier
- `assignment_id`: Core-issued assignment identifier
- `operation`: registered operation identifier (not a shell command)
- `entry_path`: repository-relative approved entry path
- `source_sha256`: exact source snapshot SHA-256
- `purpose`: bounded non-empty purpose code

The request MUST NOT contain caller WorkContext, caller-supplied identity claims, workspace/evidence roots, policy decisions, gate state, allowed paths, or an `authorized` boolean.

### 4.2 Core-derived checks

Core resolves the authenticated service principal, Work, assignment, registered operation, source snapshot and W70 gate/policy state itself. It checks:
1. Work exists and is active.
2. Assignment belongs to the authenticated principal and Work, is active, and permits the requested operation.
3. Operation and entry path are registered and permitted for this Work.
4. Source snapshot matches the approved source identity.
5. W70 policy source is reachable, current, versioned and internally consistent.
6. Gate is explicitly OPEN for this operation; missing/stale/closed/unknown means DENY.
7. Service principal is enrolled and allowed for this exact Work/operation.
8. No applicable revocation, suspension, freeze or conflict exists.

### 4.3 Response

On success: HTTP 201, `status=GRANTED`, with:
- `grant_id`
- `grant_token` (high-entropy opaque bearer token, returned exactly once)
- `issued_at`, `expires_at` (UTC RFC3339; maximum lifetime is Core policy controlled)
- `principal_id`, `work_id`, `assignment_id`
- `operation`, `entry_path`, `source_sha256`
- `policy_version`, `policy_snapshot_sha256`
- `gate_id`, `gate_version`, `gate_snapshot_sha256`
- `host_audience` (exact W14 Host service identity)
- `grant_record_id`

Core stores only a one-way token verifier, never the raw token. The grant is bound to the fields above; any mismatch invalidates it. No field may be silently defaulted.

## 5. Online validation by W14 Host

### 5.1 Request

`POST /api/v1/execution/grants/{grant_id}:validate`

Caller: authenticated W14 Host service identity only.

Required JSON fields:
- `request_id`, `contract_version`
- `grant_token`
- `host_instance_id`
- `operation`
- `entry_path`
- `source_sha256`
- `execution_request_id` (stable idempotency/correlation key)

No caller WorkContext is accepted.

### 5.2 Response

On success: HTTP 200, `status=VALID`, with Core-derived, read-only `execution_context`:
- `principal_id`, `work_id`, `assignment_id`
- `work_name`, `workspace_root`, `execution_workspace`, `evidence_root`
- `operation`, `entry_path`, `source_sha256`
- `policy_version`, `policy_snapshot_sha256`
- `gate_id`, `gate_version`, `gate_snapshot_sha256`
- `grant_id`, `issued_at`, `expires_at`, `host_audience`
- `validation_id`, `validated_at`

The Host must compare every request binding with the Core response and its locally measured source/build identity. Host must reject mismatches, expired grants, wrong audience, revoked grants, stale policy/gate snapshots, duplicate or replayed execution IDs, and any validation response that is incomplete or unverifiable.

The response is not a reusable authorization cache. Validation must occur online for each execution attempt. Core unavailability means BLOCKED.

## 6. Run lifecycle, sequence and idempotency

Core records an execution lifecycle using append-only events:
- `RUN_ACCEPTED`
- `RUN_STARTED`
- exactly one terminal event: `RUN_COMPLETED`, `RUN_FAILED`, `RUN_TIMED_OUT`, `RUN_CANCELLED`, or `RUN_BLOCKED`.

Each event includes `event_id`, `request_id`, `execution_request_id`, `grant_id`, `work_id`, `host_instance_id`, monotonic `sequence`, `occurred_at`, `event_type`, and a content digest. Events are append-only; sequence gaps, conflicting duplicate sequence values, or a second terminal event are rejected and surfaced as integrity failures.

### 6.1 Start acknowledgement

`POST /api/v1/execution/runs/{execution_request_id}:start`

W14 Host sends the grant ID, validation ID, host instance, operation, source digest and idempotency key. Core returns an ACK only after durable append of `RUN_STARTED`. No ACK means Host must not treat the run as accepted.

### 6.2 Terminal report

`POST /api/v1/execution/runs/{execution_request_id}:complete`

W14 Host sends terminal status, exit code (nullable), start/end timestamps, output digests/references, evidence references, containment result, cancellation result, and final event sequence. Core validates that the grant is still valid for the run and that all required fields/evidence references are present. Core returns an ACK only after durable append and read-after-write verification.

Duplicate identical requests return the original ACK. Reuse of an idempotency key with different content returns HTTP 409 `idempotency_conflict`. Failure to persist or verify the event means Host reports BLOCKED and must not claim PASS.

### 6.3 Cancellation and close semantics

Cancellation is a request, not proof of termination. Host must report cancellation requested, cancellation acknowledged, process-tree termination verified, descendants absent, and containment cleanup outcome as separate facts. A run is terminal only after the Host has verified process-tree exit and cleanup. Missing ACK, missing terminal event or unknown descendant state remains BLOCKED/INCOMPLETE.

## 7. Revocation and status

- `POST /api/v1/execution/grants/{grant_id}:revoke` — only Core policy authority or an explicitly authorized operator; append-only revocation record, idempotent.
- `GET /api/v1/execution/grants/{grant_id}` — returns non-secret status and binding digests only; never returns token or token verifier.
- Revocation is checked online during validation and before accepting terminal run evidence.
- Revoked, expired, suspended, policy-stale or gate-stale grants are never reactivated. A new grant requires a new authorization decision.

## 8. Error taxonomy

All error responses include stable `error_code`, `status=BLOCKED`, `request_id`, `contract_version`, and non-sensitive `message`.

| HTTP | Error code | Meaning / Host action |
|---|---|---|
| 400 | `invalid_request` | Schema or field violation; deny |
| 401 | `service_authentication_failed` | Principal not authenticated; deny |
| 403 | `policy_denied` | Work/assignment/operation/gate not permitted; deny |
| 404 | `grant_not_found` | Unknown or non-disclosable grant; deny |
| 409 | `binding_mismatch` / `idempotency_conflict` | Integrity conflict; deny and audit |
| 410 | `grant_expired_or_revoked` | Grant no longer valid; deny |
| 412 | `policy_or_gate_stale` | W70 snapshot stale/missing/mismatch; deny |
| 422 | `source_or_operation_mismatch` | Source, entry or operation differs; deny |
| 429 | `rate_limited` | Retry only under bounded policy; no execution |
| 503 | `authority_unavailable` / `ledger_unavailable` | BLOCKED; no execution or PASS claim |
| 500 | `authority_integrity_failure` | BLOCKED; incident/evidence required |

No error branch may fall back to static grants, caller context, local Work allowlists or cached PASS.

## 9. Evidence and integrity requirements

- Core ledger records are append-only and tamper-evident. A simple JSONL append/fsync store is not by itself proof of hash-chain integrity, concurrency safety, corruption detection, backup/restore or read-after-write verification.
- Each record includes canonical serialization version, previous-record digest, current-record digest, sequence, and stable record ID. On startup/read, verify the full chain and fail closed on corruption or truncation.
- Writes require process-safe serialization/locking and durable flush semantics; concurrent append tests are mandatory.
- Evidence must bind repository, commit, source SHA-256, build artifact SHA-256, service identity, process identity, Work/assignment/grant IDs, operation, policy/gate snapshot digests, Host instance, event sequence and readback digest.
- No secret values in records, logs, artifacts, telemetry or error payloads.

## 10. Required verification matrix

| ID | Priority | Test / proof | Required result |
|---|---|---|---|
| CEA-01 | P0 | Caller submits forged WorkContext or `authorized=true` | Rejected; no Host dispatch |
| CEA-02 | P0 | Missing/unknown Work or assignment | Denied |
| CEA-03 | P0 | Wrong principal, operation, entry path or source digest | Denied |
| CEA-04 | P0 | W70 unavailable, stale, mismatched or gate not OPEN | Denied |
| CEA-05 | P0 | Expired, revoked, replayed, wrong-audience token | Denied |
| CEA-06 | P0 | Core validation endpoint unavailable / redirect attempted | BLOCKED; no dispatch |
| CEA-07 | P0 | Core ledger write/readback failure | BLOCKED; no PASS |
| CEA-08 | P0 | Duplicate event/idempotency replay | Same ACK only for identical content; conflict otherwise |
| CEA-09 | P0 | Sequence gap, duplicate sequence, second terminal event | Integrity failure |
| CEA-10 | P0 | Cancellation ACK vs actual process-tree exit | No terminal PASS until verified exit/cleanup |
| CEA-11 | P1 | Concurrent grant/run writes and restart recovery | Ordered, durable, tamper-evident ledger |
| CEA-12 | P1 | Linux and Windows exact-source lifecycle | Both pass with raw logs and immutable artifacts |
| CEA-13 | P0 | Actual Core :8000 → MCP 8030 → approved Runtime → W14 Host → ledger readback | Live E2E with process/build identity and evidence hashes |

## 11. Ownership reconciliation and open decisions

These items are deliberately NOT guessed:
1. Core :8000 composition owner and approved module/router integration point.
2. Canonical Core source baseline: main, W1111 PR #48, PR #74 candidate and Work28 branch must be compared; no branch is assumed canonical by name.
3. W14 Host repository/module, service identity, HostPort envelope and sole process ownership.
4. W70 API/contract version, authoritative policy fields, snapshot freshness and gate semantics.
5. Approved service authentication mechanism (mTLS/workload identity or equivalent) and credential rotation.
6. Core ledger persistence backend, transaction/locking guarantees, tamper-evidence and backup/restore.
7. Normative timeout, retry, cancellation and retention limits.

Before implementation, Xu must reconcile these contracts and Vinh must approve the authority boundary where required by the Work Manifest. This candidate does not claim those approvals.

## 12. Acceptance gate

This document is accepted as a design candidate only when:
- schemas and examples are converted into executable JSON Schema/OpenAPI fixtures;
- ownership and provenance are resolved against actual Core/W14/W70 source;
- independent review closes all P0 findings;
- Linux/Windows contract and failure-injection tests pass;
- Core :8000 integration is explicitly approved and verified;
- live end-to-end evidence proves grant issue, online validation, execution, event ACK, durable ledger readback and revocation;
- Vinh's required approval is recorded.

Until then: **CANDIDATE / NOT APPROVED / NOT WIRED / EXECUTION GATE CLOSED / WORK 28 NOT RELEASED.**


## 13. Source-provenance addendum — 2026-11-23 (DOC-W28-078-A1)

This addendum narrows the source claims to exact fetched paths and blobs.

### Main source snapshot

- Main HEAD inspected: `0902cd26518673aa078bb4c7c7899e1e4a95656a`.
- `room_hop_mcp/core_http_main.py` blob `8dd6bb5ea500026d932ca52eb6079c980d722ab0`: `build_app()` creates MeetingManager/MeetingService and returns `create_http_app(service)`; no execution-authority router is imported or mounted in this function.
- `room_hop_mcp/adapter/http_server.py` blob `54cb3ecbce2e6b13083f31c14f0c1f0738f1457d`: inspected adapter defines Identity and Meeting routes; no execution-grant route is present in this file.
- `execution_host/server.py` blob `45aec57525b5d55bb63544b7bd7fd23062e06151`: `POST /execute` constructs `WorkContext(**body['work_context'])` from request JSON and calls `host.execute_work`; no Core grant validation occurs in this handler.
- `CORE_EXECUTION_AUTHORITY_V1_2_DEPLOYMENT.md` blob `ce130f1f9a95daeaafff75ef37eacd4dffc797e2` claims the grant routes are mounted in Core :8000. The inspected entrypoint/adapter do not show that mount. This is a bounded documentation/source discrepancy; no live HTTP test was run.

### W1111 PR #48 candidate comparison

- Branch: `work/w1111-core-execution-authority-v1-2`; PR #48 remains an unmerged candidate.
- `core/execution_authority.py` blob `163b126178b67c6e0a3f68ba33eaf7b9e6d91503` contains a hash-chained JSONL store with lock-file serialization and chain verification.
- `room_hop_mcp/adapter/execution_authority_http.py` blob `8cb21fadf6bf2318f4884d368b77f2abf796b807` contains a candidate route mount, including online token validation.
- Prior bounded source audit (Work17 GAP-01 Entry 030) records a static defect: run recording did not compare submitted `source_sha256` against the grant-bound Work policy, and its test accepted a different digest. This finding must be reproduced against the exact PR #48 HEAD before reuse; it is not silently treated as a current-main defect.
- PR #48 is not canonical Core and cannot be copied wholesale into Work28. Its store design is a reference for further review only.

### Disposition

Core :8000 route mount, W14 Host ownership, W70 policy snapshot and canonical source provenance remain BLOCKED / NOT VERIFIED. This addendum does not claim live endpoint behavior, runtime process identity, test PASS or approval. Execution Gate remains CLOSED.


## 14. Alignment addendum — AD-W28-20261123-002 / PR #74 (2026-11-23)

This document is a subordinate wire-level implementation proposal. It MUST be interpreted under the architecture baseline in PR #74, not as a competing authority or independent architecture decision.

### 14.1 Normative ownership inherited from PR #74

- W70 owns Work/WP/Gate lifecycle and eligibility.
- Core :8000 remains the sole authority and durable system of record.
- W52 owns Agent orchestration, assignment dispatch, recipient-authenticated ACK/NACK, event cursor, retry/cancel/recovery semantics.
- W14 is the sole Execution Host product and side-effect boundary.
- W10 remains LOCKED / NO CHANGE; no direct provider invocation.
- W092/W113 are read-only projections.
- W12/W13 are historical/internal foundations, not separate active Host products.
- Historical MCP :8020 remains DO NOT USE.

### 14.2 Grant prerequisites and full binding

A Core grant MUST NOT be issued merely because a service identity requests one. It is issued only after Core verifies the W52 assignment and a recipient-authenticated ACK from the exact assigned Agent runtime, plus W70 Work/WP/Gate eligibility.

The V1.3 architecture identifiers are mandatory bindings: `work_id`, `wp_id`, Gate/policy version, `task_id`, `assignment_id`, idempotency key, correlation ID, authenticated `agent_principal_id`, runtime instance/build identity, `grant_id`, `host_id`, `provider_id`, `run_id`, source repository/branch/commit/tree digest and immutable input snapshot, action/capability scope, environment, timestamps and event sequence.

For clarity:
- Principal identity, recipient ACK state, Work/WP/Gate policy, assignment state and authoritative roots are resolved by Core from trusted sources; they are not accepted as caller authority claims.
- The service request may carry opaque task/assignment/correlation identifiers and the requested operation/snapshot; Core must resolve and verify every identifier.
- Any omitted binding, stale source, unsupported capability, wrong recipient, wrong Host/provider, missing ACK, or inconsistent environment must deny.
- This candidate's initial §4/§5 field lists are incomplete unless augmented by this §14.2. The full AD-W28-20261123-002 binding set takes precedence.

### 14.3 Route/transport status

PR #74 §6 deliberately leaves exact transport and route names as implementation decisions. Therefore the route paths shown in §4–§7 of this document are illustrative candidates only, not approved route names or a mandate to create a second HTTP interface. Final route/transport design must be reconciled with the existing Core :8000 composition, W52 delivery/ACK protocol and W14 HostPort contract before implementation.

The grant-validation/run-report API described here does not itself implement W14 bidirectional HostPort request/notify/receive/respond/close semantics. A one-shot HTTP API cannot be presented as HostPort completion. The W14 capability profile and process-tree close/cancel semantics remain separate P0 proof obligations.

### 14.4 PR #74 and PR #48 provenance snapshot

- PR #74 title: `W28: Core Execution Authority & Agent-to-Computer Contract V1.3`; source contract blob `85c88a5ac50a6d12e4edcd34879a9db79277466a`; architecture baseline decided, implementation not approved by this document alone, not deployed, not wired, not released. Its §8 records the Main source mismatch and PR #48 candidate limitations.
- PR #48 title: `feat(core): implement Work-scoped Execution Authority V1.2`; head `c70eb2b82f54a000a81263dc519078ddf105f075`; OPEN / unmerged; branch comparison to Main at this inspection: 157 ahead / 986 behind. It is not canonical Core or W14.
- The PR #48 source-hash binding defect and W12/W13 ownership drift remain blockers to reuse. Any future reuse must be selective, aligned to W14 and the complete AD-W28 V1.3 bindings, fixed and re-tested on a fresh canonical Core baseline.

**Precedence:** AD-W28-20261123-002 (PR #74) owns architecture and component boundaries. DOC-W28-078 proposes only a possible versioned wire-level realization. Where they differ, PR #74 controls and DOC-W28-078 must be revised.
