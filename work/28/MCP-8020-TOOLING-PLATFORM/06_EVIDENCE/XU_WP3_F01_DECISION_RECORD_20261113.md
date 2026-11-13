# WORK 28 — WP3-F01 XU DECISION RECORD

**Decision ID:** XU-W28-WP3-F01-DEC-20261113-01  
**Date:** 2026-11-13  
**Authority:** Vinh delegation to Xu for Work 28 architecture and integration decisions  
**Decision owner:** Xu  
**Source brief:** `work/28-wp3-xu-decision-brief`, commit `a37a5bea115c962ebd879e0384e520ca7ff114a6`  
**Source proposal:** `06_EVIDENCE/VI_WP3_BINARY_UPLOAD_AUTHORIZATION_CONTRACT_PROPOSAL_20261104.md`  
**Canonical branch:** `work/28-mcp-tooling-platform`  
**Status:** PARTIALLY DECIDED — 3 OF 4 CONTRACT DECISIONS APPROVED; CAPABILITY-GRANT BLOCKED PENDING KA REVIEW. IMPLEMENTATION NOT AUTHORIZED.

## 1. Decision summary

| Decision | Selected option | Status |
|---|---|---|
| Q1 — Trusted caller context | A — authenticated MCP/transport session context, resolved server-side and passed out-of-band | DECIDED WITH CONDITIONS |
| Q2 — Core Work ID to Sandbox ID mapping | B — dynamic mapping returned by Core WorkContext/authorization response | DECIDED |
| Q3 — Upload protocol | B — explicit begin/chunk/finalize session protocol, with an abort/cancel path | DECIDED |
| Q4 — Core capability-grant semantics | No option approved yet; Ka security review is a mandatory prerequisite | BLOCKED / PENDING KA |

## 2. Q1 — Trusted caller context: Option A

The server may trust only an authenticated principal/session established by a trusted MCP transport/runtime boundary. The caller identity must be resolved from server-side transport/session state and passed to the service adapter out-of-band; it must never be accepted from tool arguments, caller-supplied identity fields, or tool output.

Conditions:
- stdio is trusted only when launched and bound by the approved trusted parent/runtime with an authenticated principal context;
- HTTP must not expose upload operations until authentication and principal binding are enforced before tool dispatch;
- missing, invalid, ambiguous or expired caller context means DENY/BLOCKED before filesystem access;
- a future public HTTP deployment may add a pinned service credential as a separately reviewed transport authentication mechanism; this does not weaken the current fail-closed rule.

This decision does not assert that the existing v54 dispatch already supplies this context. The adapter and Core authorizer must be wired and independently verified before implementation can proceed.

## 3. Q2 — Work ID mapping: Option B

Core :8000 is the sole authority for canonical Work identity and authorization. Core must return the authoritative provider/Sandbox Work mapping as part of a trusted WorkContext/authorization response.

Conditions:
- no hardcoded W28 → Sandbox 28 mapping in tool code;
- no mapping inferred from client arguments or string normalization;
- unknown, missing, conflicting or stale mapping means BLOCKED before staging or filesystem side effects;
- mapping response must be bound to the authenticated principal, canonical Work ID and authorization decision;
- no static mapping fallback is approved for production. A future temporary migration mechanism requires a separate documented and audited decision.

## 4. Q3 — Upload protocol: Option B

Adopt a bounded upload-session protocol with three primary operations:
1. **begin** — authorize the intended Work/path, reserve bounded quota, validate expected byte count and SHA-256, enforce chunk limits and expiry, then return an opaque upload/session ID;
2. **chunk** — accept bounded chunks with strict index/offset, length and integrity validation; reject duplicate, missing, reordered, oversized or out-of-scope chunks;
3. **finalize** — revalidate authorization and session binding, require complete contiguous byte coverage, verify exact total byte count and SHA-256, atomically promote, perform independent readback, and append audit evidence before reporting success.

A separately controlled abort/cancel operation or equivalent server-side cancellation path is required. Expiry and cancellation must clean staging idempotently and leave no partial final artifact. Session state must be short-lived and bound to (authenticated caller, canonical Work ID, normalized destination, quota and expiry). Staging must remain contained and inaccessible as a final artifact.

The registered MCP catalog, schemas, handlers, service dispatch and provider contract must agree. No placeholder tool or claim of binary upload support is permitted.

## 5. Q4 — Capability grant: NOT APPROVED

No Core upload capability grant is approved by this record. Vinh explicitly required Ka review before approval.

Ka must review the original authorization contract proposal and the concrete grant design, including at minimum:
- principal and canonical Work binding;
- operation/capability name and normalized path scope;
- quota and maximum object/chunk sizes;
- expiry, revocation and replay/idempotency behavior;
- overwrite authority (default remains no-overwrite);
- authorization check before every side effect, including begin, chunk, finalize and abort;
- audit event/correlation requirements and safe failure behavior.

Xu may decide Q4 only after Ka records an independent review artifact on the exact proposal/design revision. Xu must not approve a grant broader than the reviewed design. Until then, all upload operations remain DENY/BLOCKED and must not create staging directories or write files.

## 6. Implementation and release gates

This record approves contract direction only. It does NOT authorize implementation, deployment, capability issuance, production routing changes or release.

Before WP3-F01 implementation may start:
1. Ka review Q4 grant design and publish an evidence-backed review artifact.
2. Xu records the final Q4 decision in a new append-only journal entry and, if needed, a superseding decision record.
3. The approved contract is translated into an implementation plan and test matrix.
4. An independently reviews the test plan/acceptance boundary; no one may claim An's QA acknowledgement on An's behalf.

After implementation:
- test unauthenticated/spoofed caller, Core unavailable/denied/revoked/expired, mapping mismatch, path traversal/symlink escape, quota, chunk reorder/duplication/gap, cancellation/expiry, checksum/readback mismatch, atomic promotion and cleanup failure;
- prove exact binary byte preservation, SHA-256 and authorized readback;
- CI and independent QA/security evidence must reference the exact tested commit;
- Sandbox upload and GitHub publication/synchronization remain separate operations.

## 7. Preserved boundaries and current status

- Do not interact with the quarantined historical MCP :8020 listener.
- Core :8000 remains the sole identity, Work-context, authorization and task authority.
- MCP Build/Verification :8030 remains a separate build/evidence lane, not an authorization bypass.
- Execution Host :8031 remains the approved execution boundary; no change is authorized here.
- WP3-F01 remains IMPLEMENTATION BLOCKED until Q4 review and approval plus required implementation gates.
- Work 28 remains ACTIVE / INTEGRATION BLOCKED / NOT RELEASED. Execution Gate CLOSED.
- CI run #327 status is independent of this WP3 decision and must be read from its live workflow result; no PASS is inferred here.
