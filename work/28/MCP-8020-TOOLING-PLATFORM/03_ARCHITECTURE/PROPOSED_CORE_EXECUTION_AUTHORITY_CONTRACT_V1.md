# PROPOSED Core Execution Authority Contract — V1.1 (DESIGN ONLY)

* Work: W28 (MCP Tooling Platform)
* Stage: **DESIGN / PROPOSED — NOT APPROVED, NOT IMPLEMENTED, NOT WIRED**
* Date: 2026-10-25 (V1.1 same day: incorporates the independent reviewer's
  architectural principles as the normative invariant set, and converts the
  open questions into decision requests)
* Approver required: architecture owner (Xu/Mê + Vinh). This document
  requests decisions; it grants nothing.

## 1. Audit finding that motivates this document (unchanged from V1)

Repository source audit on branch `work/28-mcp-tooling-platform` confirmed:

* Core :8000 today is a **meeting lifecycle service only**
  (`room_hop_mcp/adapter/http_server.py`, `core/meeting_service.py`,
  `core/meeting_manager.py`; contract `API_CONTRACT.md` LOCKED v0.1).
* No route, service method, or data model authenticates a caller for
  **Work execution**, issues a **WorkContext**, or records execution
  authority. `work_id` / `WorkContext` / `execute` appear nowhere in
  the Core package.

Conclusion: the MCP -> Core :8000 -> W13 route cannot be wired today,
because the Core half of the route does not exist. Guessing an endpoint is
prohibited by the Work 28 discipline; therefore the contract below is
proposed explicitly for review, not implemented.

## 2. Normative architectural invariants (adopted from the independent
review round of 2026-10-25; PENDING APPROVAL)

These five principles are proposed as the common base for every decision in
section 5, so each decision can be taken once instead of re-litigated:

* **INV-1 — Core decides, MCP never self-authorizes.** Core :8000 is the
  sole authority that decides whether a caller may run executions for a
  given Work. MCP 8020/8030, the WEE bridge, and any client may not grant
  rights or construct a trusted WorkContext themselves. Caller identity
  comes from authenticated middleware, never from request body fields.
* **INV-2 — Grants are bound and verifiable.** A grant binds ALL of:
  the Work id, an authenticated caller identity, a scoped action purpose,
  an expiry, and a checkable status (active/expired/revoked). A grant for
  one Work conveys nothing about any other Work.
* **INV-3 — Durable authoritative state.** Run status, results,
  evidence, and handoffs must live in an authoritative store that
  survives restarts and is queryable by id. An in-process in-memory
  registry is never the source of truth (this is an acknowledged
  limitation of the staged `W13CoreExecutionClientV1`, evidence 11.2).
* **INV-4 — One canonical runtime.** W13/W12 remains the only execution
  site, under its OS isolation, snapshot, hash, and timeout gates. No
  second execution host is created, and MCP never bypasses Core by talking
  to the Execution Host directly.
* **INV-5 — Fail closed on every failure branch.** Authentication
  failure, expired grant, wrong Work, missing configuration, or missing
  evidence must all deny with stable error codes. No partial arming.

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

Authoritative grant status. Required by INV-2/INV-3: durable, restart-safe,
revocation-capable.

### 3.3 POST /works/{work_id}/execution-runs (record-only, phase 2)

Records run outcomes bound to a grant + source hash + exit status + output
refs. This is the authoritative store that `generate_evidence` and
`create_handoff` must write to (INV-3), instead of assembling local
dictionaries.

## 4. Integration seam (once approved AND implemented AND verified)

`W13CoreExecutionClientV1.work_context_provider(work_id)` becomes the
caller of 3.1: it derives the WorkContext from a live grant, never from the
public request. The bridge token continues to authenticate the W13 boundary;
the grant authenticates the Work rights. Both are required, in that order
(INV-1, INV-4). Wiring remains prohibited until the gates in section 6 pass.

## 5. Decision requests (each with a recommended default; recommendations
are proposals, not approvals)

* **DR-1 — Caller identity between services.** Which identity does Core
  accept for the grant call: (a) the MCP 8020 service identity (deployment
  token, mTLS, or signed header), or (b) an end-user identity propagated
  through MCP?
  *Recommended: (a) service identity first.* MCP 8020 is the only integrator
  today; user-identity propagation can be added later without changing the
  grant shape. Satisfies INV-1 with the smallest trusted surface.
* **DR-2 — Credential model for W13.** Does the grant carry its own
  short-lived execution token (separate from the deployment bridge token),
  or does the deployment token remain the only credential with Core-side
  Work allow-listing?
  *Recommended: separate short-lived grant token.* It bounds blast radius:
  leaking a W13-boundary credential does not outlive the grant expiry, and
  the W13 handler can validate expiry locally (INV-2, INV-5). The existing
  `X-Room-Hop-Execution-Auth` header stays as the transport; the token
  VALUE becomes grant-scoped.
* **DR-3 — Durable store for grants, runs, evidence, handoffs.** Where do
  grant state and run/evidence records live: (a) files under the Work
  evidence root with a lock protocol, (b) a Core-managed data file
  (`core/meeting_log.py` pattern), or (c) an external store?
  *Recommended: (b), Core-managed append-only record.* Core already owns
  durable append-only records; keeping authority state inside Core means
  INV-3 holds with no new infrastructure, and 3.2 can be honest across
  restarts.
* **DR-4 — Composer and mounting.** Which process composes
  `W13CoreExecutionClientV1` into the running service, and is the
  execution authority mounted inside the existing Core app or a separate
  service instance?
  *Recommended: separate app mount (same codebase, distinct process/port).*
  The meeting contract `API_CONTRACT.md` is LOCKED v0.1; an additive
  separate mount cannot regress it, and fail-closed startup of the
  execution authority cannot take the meeting service down (INV-5).

## 6. Gates before any wiring (in order; none may be skipped)

1. This contract APPROVED (DR-1..DR-4 answered) by the architecture owner.
2. Core-side implementation per the approved contract; no endpoint created
   merely to make the staged adapter appear to work.
3. W13 Sandbox alignment verified at runtime (not by reading files):
   hardened source deployed and proven active.
4. Security tests + E2E: live 401/403 probes, wrong-Work, expired-grant,
   wrong-hash, timeout, then MCP -> Core -> W13/W12 with evidence bound to
   the exact run.
5. Only then: gateway/catalog wiring, publishing only tools that are
   actually registered, executing, and verified.

## 7. Explicitly NOT claimed

* No endpoint exists. No code implements this. No test asserts it.
* Nothing here changes the v54 catalog: the seven execution tools remain
  NOT_IMPLEMENTED.
* The recommendations in section 5 are proposals by the repo-side agent
  for the architecture owner to accept, reject, or replace.
* Work 28 remains ACTIVE / BLOCKED / NOT RELEASED.
