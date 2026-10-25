# PROPOSED Core Execution Authority Contract — V1 (DESIGN / NOT IMPLEMENTED)

* Work: W28 (MCP Tooling Platform)
* Stage: **DESIGN / PROPOSED — NOT IMPLEMENTED, NOT WIRED, NOT DEPLOYED**
* Date: 2026-10-25
* Status owner: architecture owner (Xu/Mê + Vinh). Nothing in this document
  authorizes implementation; it answers the open question "which real
  Core :8000 route authorizes Work execution" by proposing one for review.

## 1. Audit finding that motivates this document

Repository source audit on branch `work/28-mcp-tooling-platform` (commit
`c04c2e0` at audit time) confirmed:

* Core :8000 today is a **meeting lifecycle service only**
  (`room_hop_mcp/adapter/http_server.py`, `core/meeting_service.py`,
  `core/meeting_manager.py`; contract `API_CONTRACT.md` LOCKED v0.1).
* Its HTTP surface is exactly: `GET /identities`, `GET /meetings`,
  `GET /meetings/{id}`, `GET /meetings/{id}/transcript`,
  `POST /meetings`, `POST /meetings/{id}/paste|open|join|start|close`.
* No route, service method, or data model authenticates a caller for
  **Work execution**, issues a **WorkContext**, or records execution
  authority. `work_id` / `WorkContext` / `execute` appear nowhere in
  the Core package.

Conclusion: the MCP -> Core :8000 -> W13 route cannot be wired today,
because the Core half of the route does not exist. Guessing an endpoint is
prohibited by the Work 28 discipline; therefore the contract below is
proposed explicitly for review, not implemented.

## 2. Authority invariants (must hold in any approved version)

1. Core :8000 is the SOLE authority that decides whether a caller may run
   executions for a given Work. Neither MCP 8020/8030, the WEE bridge, nor
   any client may self-declare `authorized` (this was the original W13
   vulnerability, closed fail-closed on the branch).
2. The caller identity used for the decision is taken from authenticated
   middleware (deployment token chain), never from request body fields.
3. A grant is Work-scoped, single-purpose, and time-bounded. A grant for
   W28 conveys nothing about W12 or any other Work.
4. Core never executes anything itself: it issues grants and records
   outcomes. The approved W13 runtime remains the only execution site,
   under the OS isolation, snapshot, hash, and timeout gates.
5. Fail-closed everywhere: unknown caller, unknown Work, missing
   configuration, or expired grant => deny with a stable error code; no
   partial arming.

## 3. Proposed surface (for review)

### 3.1 POST /works/{work_id}/execution-grants

Request: authenticated via deployment identity headers (no body authority
fields). Optional body: `{"purpose": "pytest_run", "max_timeout_seconds": 60}`.

Response 200:

```json
{
  "grant_id": "GRANT-<uuid>",
  "work_id": "W28",
  "work_name": "MCP-TOOLING-PLATFORM",
  "workspace_root": "...",
  "execution_workspace": "...",
  "evidence_root": "...",
  "authorized": true,
  "expires_at": "2026-10-25T12:00:00Z",
  "execution_token_ref": "<opaque reference, never the token value>"
}
```

Errors: 401 `caller_authentication_failed`, 403 `caller_not_authorized_for_work`,
404 `unknown_work`, 409 `grant_already_active` (policy decision),
503 `execution_authority_not_configured`.

### 3.2 GET /works/{work_id}/execution-grants/{grant_id}

Authoritative grant status (active/expired/revoked). Needed because the
staged client's in-memory registry cannot survive restarts or coordinate
workers; durable status must come from Core (see evidence section 11.2).

### 3.3 POST /works/{work_id}/execution-runs (record-only, phase 2)

Records run outcomes bound to a grant + source hash + exit status + output
refs. This is the authoritative store that `generate_evidence` and
`create_handoff` must write to, instead of assembling local dictionaries.

## 4. Integration seam (once approved and implemented)

`W13CoreExecutionClientV1.work_context_provider(work_id)` becomes the
caller of 3.1: it derives the WorkContext from a live grant, never from the
public request. The bridge token continues to authenticate the W13 boundary;
the grant authenticates the Work rights. Both are required, in that order.

## 5. Open questions for the architecture owner

1. Does the grant carry its own short-lived execution token (separate from
   the deployment bridge token), or does the deployment token remain the
   only credential with Core-side Work allow-listing?
2. Is grant state persisted in Core storage (durable across restarts), and
   who owns revocation?
3. Which component composes the client: MCP 8020 service startup, or a
   separate trusted integrator process?
4. Contract versioning: this must not violate the LOCKED v0.1 lifecycle
   contract; execution authority is additive and must be a separate app
   mount or service instance to keep the meeting contract untouched.

## 6. Explicitly NOT claimed

* No endpoint exists. No code implements this. No test asserts it.
* Nothing here changes the v54 catalog: the seven execution tools remain
  NOT_IMPLEMENTED.
* Wiring `W13CoreExecutionClientV1` remains prohibited until this contract
  is approved, implemented, and verified with live 401/403 probes and one
  bound-evidence E2E run.
* Work 28 remains ACTIVE / BLOCKED / NOT RELEASED.
