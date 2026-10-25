# PROPOSED Core Execution Authority Contract — V1.2 (DESIGN ONLY)

* Work: W28 (MCP Tooling Platform)
* Stage: **DESIGN / PROPOSED — NOT APPROVED, NOT IMPLEMENTED, NOT WIRED**
* History: V1 (241bdba) initial proposal; V1.1 (1936ad3) principles as
  invariants + decision requests; V1.2 (this revision) incorporates the
  architecture reviewer's (Xu) conditions on DR-2/DR-3/DR-4 and the amended
  DR-1. Awaiting final approval by Vinh.
* Approver: Vinh (with Xu). This document requests decisions; it grants
  nothing.

## 1. Audit finding that motivates this document (unchanged)

Repository source audit on branch `work/28-mcp-tooling-platform` confirmed:

* Core :8000 today is a **meeting lifecycle service only**
  (`room_hop_mcp/adapter/http_server.py`, `core/meeting_service.py`,
  `core/meeting_manager.py`; contract `API_CONTRACT.md` LOCKED v0.1).
* No route, service method, or data model authenticates a caller for
  **Work execution**, issues a **WorkContext**, or records execution
  authority. `work_id` / `WorkContext` / `execute` appear nowhere in
  the Core package.

## 2. Normative architectural invariants (INV-1..INV-5, unchanged in V1.2)

* **INV-1 — Core decides, MCP never self-authorizes.** Core :8000 is the
  sole authority that decides whether a caller may run executions for a
  given Work. MCP services, the WEE bridge, and any client may not grant
  rights or construct a trusted WorkContext themselves. Caller identity
  comes from authenticated middleware, never from request body fields.
* **INV-2 — Grants are bound and verifiable.** A grant binds ALL of:
  the Work id, an authenticated caller identity, a scoped action purpose,
  an expiry, and a checkable status (active/expired/revoked). A grant for
  one Work conveys nothing about any other Work.
* **INV-3 — Durable authoritative state.** Run status, results,
  evidence, and handoffs must live in an authoritative store that
  survives restarts and is queryable by id.
* **INV-4 — One canonical runtime.** W13/W12 remains the only execution
  site, under its OS isolation, snapshot, hash, and timeout gates. No
  second execution host; MCP never bypasses Core.
* **INV-5 — Fail closed on every failure branch.** Authentication
  failure, expired grant, wrong Work, missing configuration, or missing
  evidence must all deny with stable error codes. No partial arming.

## 3. Proposed surface (for review; unchanged from V1.1)

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

Authoritative grant status (active/expired/revoked). Required by INV-2/INV-3.

### 3.3 POST /works/{work_id}/execution-runs (record-only, phase 2)

Records run outcomes bound to a grant + source hash + exit status + output
refs. The authoritative store that `generate_evidence` and
`create_handoff` must write to.

## 4. Integration seam (once approved AND implemented AND verified)

`W13CoreExecutionClientV1.work_context_provider(work_id)` becomes the
caller of 3.1 on behalf of an ENROLLED service identity (see DR-1): it
derives the WorkContext from a live grant, never from the public request.
The bridge token authenticates the W13 boundary; the grant authenticates
the Work rights. Both are required, in that order.

## 5. Decision requests — reviewer conditions incorporated (V1.2)

* **DR-1 — Caller identity: Core-enrolled service identity, port-agnostic.
  STATUS: revised per Xu (2026-10-25).**
  The grant call is made by a **service identity that Core itself has
  enrolled and authorized**. Enrollment is by identity, not by port or
  process: the identity registry lives in Core configuration, and any MCP
  instance (8020, 8030, or a future adapter) presenting an enrolled
  identity may request grants; any instance without one is denied
  fail-closed. Migrating ports or replacing adapters therefore never
  requires redesigning the authority mechanism. The identity credential
  must be injectable per deployment (env/secret), never hardcoded.
* **DR-2 — Grant token: separate, short-lived, server-validated.
  STATUS: Xu condition added.**
  The grant carries its own short-lived execution token, separate from any
  transport credential. CONDITIONS: the W13 boundary validates rights,
  Work, action scope, and expiry SERVER-SIDE on every call; the token
  value is never written to logs, blockers, or evidence (non-leak property
  is testable the same way as the existing bridge token tests).
* **DR-3 — Durable store: Core-managed append-only, with proof obligations.
  STATUS: Xu condition added.**
  Grant state and run/evidence/handoff records are Core-managed
  append-only records. The existence of the `meeting_log` pattern is a
  PRECEDENT, not proof. PROOF OBLIGATIONS before any wiring: (a) records
  persist across a service restart and remain queryable by id; (b) history
  is append-only (no mutation or deletion of past records); (c) each run
  record links grant id, source hash, exit status, output refs, evidence
  refs, and handoff ids — linkage is verifiable by reading the store.
* **DR-4 — Deployment separation: additive mount inside Core's authority.
  STATUS: Xu condition added.**
  The execution authority is a separate mount/process (fail-closed startup
  cannot affect the LOCKED v0.1 meeting API), BUT it remains inside the
  Core authority boundary: it is not a second Core, not an independent
  execution route, and it holds no authority of its own beyond what this
  contract grants. Its configuration, code ownership, and evidence live
  under the Core package's governance.

## 6. Gates before any wiring (in order; none may be skipped)

1. This contract APPROVED (DR-1..DR-4 as revised in V1.2) by Vinh.
2. Core-side implementation per the approved contract; no endpoint created
   merely to make the staged adapter appear to work; DR-2/DR-3 proof
   obligations hold in tests.
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
* Xu's review comments are incorporated as proposed contract text; final
  approval belongs to Vinh and has NOT been given yet.
* Work 28 remains ACTIVE / BLOCKED / NOT RELEASED.
