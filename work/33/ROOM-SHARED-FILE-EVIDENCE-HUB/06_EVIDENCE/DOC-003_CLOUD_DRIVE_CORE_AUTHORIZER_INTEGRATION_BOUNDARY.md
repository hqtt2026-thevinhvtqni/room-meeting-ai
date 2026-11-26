# DOC-003 — WORK 33: CLOUD DRIVE CORE AUTHORIZER INTEGRATION BOUNDARY

- Work: W33 — ROOM-SHARED-FILE-EVIDENCE-HUB
- Date: 2026-11-26 (+07)
- Status: DESIGN BOUNDARY / NOT IMPLEMENTED / CORE AUTHORITY NOT ACCEPTED FOR CLOUD DRIVE
- Evidence basis: read-only source trace of W1111 branch `work/w1111-core-execution-authority-v1-2`, observed HEAD `c70eb2b82f54a000a81263dc519078ddf105f075`.
- Purpose: prevent Work 33 from treating an execution grant as a general-purpose Cloud Drive user/agent authorization token.

## 1. Decision

The W1111 Execution Authority V1.2 contract is a narrow **service-to-Execution-Host pytest execution grant**, not a general identity and authorization service for Cloud Drive.

Work 33 MUST NOT:
- reuse `pytest_run` grants to authorize file upload/download/share/delete;
- treat a service credential identity (e.g. `mcp-8020`) as the authenticated human or AI agent who initiated an operation;
- accept caller-provided `authorized=true`, display name, agent nickname, WorkBinding, or registry membership as proof of identity;
- infer Cloud Drive user membership from the execution grant's Work-level allow-list;
- ship an adapter that silently maps all Cloud Drive actions to a generic allow decision.

The Work 33 `UnconfiguredAuthorizer` remains default-deny.

## 2. What the inspected Core grant actually proves

The feature branch's `ExecutionAuthority.authenticate()` hashes a presented service credential and matches it against the configured service-identity digest registry. `issue_grant()` then checks that this service identity is listed in the selected Work's `allowed_identities`, that the requested purpose is in `allowed_purposes`, and issues a short-lived bearer grant.

The grant binds:
- service identity label;
- Work ID;
- purpose (currently W13 Host enforces `pytest_run`);
- expiry and maximum execution timeout;
- configured Work paths and source snapshot hash returned by Core at validation.

This is useful evidence for a service execution boundary. It does not prove the identity of the human user or AI agent behind the service, nor Cloud Drive membership/role/object permissions.

## 3. Cloud Drive principal contract still required

Before implementing a production authorizer, Core must expose a verified, stable principal assertion for each request. Required fields (names are conceptual; do not assume these are existing claims):

| Concept | Required meaning |
|---|---|
| subject_id | Stable opaque ID of HUMAN_USER, AI_AGENT or SERVICE |
| principal_type | Explicit principal class |
| issuer / audience | Trusted issuer and intended Cloud Drive API |
| tenant_id | Authoritative tenant boundary |
| status / revocation | Active state and revocation freshness |
| issued_at / expires_at | Bounded token lifetime |
| token_id | Replay/revocation reference |
| assurance / auth_method | Evidence class sufficient for the operation |
| delegation | If an agent acts for a human, explicit actor + subject + scope + expiry |
| work_id / task_id | When operation is performed on behalf of a Work/task |
| assignment_state | Authoritative claimed/ACK/active/revoked version when task delegation is required |

The Cloud Drive API must validate issuer, audience, signature, expiry, status/revocation and scope. Exact token format, claim names, signing keys, key rotation and introspection endpoints must be verified from Core implementation and approved contract; none are invented here.

## 4. Authorization decision contract

Cloud Drive authorization must be action/resource scoped and default deny. Conceptual request:

- principal: verified principal assertion;
- action: one of `space.create`, `space.read`, `space.manage_members`, `object.upload`, `object.read`, `object.update`, `object.delete`, `version.restore`, `share.create`, `share.revoke`, `quota.read`, `audit.read`, `recovery.propose`, `recovery.approve`;
- resource: tenant, space, object/version/share IDs and ownership context;
- delegation: actor/subject and exact scope, if applicable;
- context: Work/task/assignment only when relevant.

Only an explicit Core `ALLOW` bound to the same principal, action, resource, tenant, and policy version may proceed. `DENY`, timeout, unavailable Core, malformed response, stale policy, missing assignment, or unknown action must deny. Do not cache positive decisions beyond a verified short TTL/revocation model. For sensitive operations (sharing, delete/purge, recovery, role changes), require fresh authorization.

## 5. Execution grant versus Cloud Drive authorization

| Operation | W1111 execution grant | Cloud Drive principal + policy required |
|---|---|---|
| Run approved pytest for a Work | Intended use | Not a substitute for Cloud Drive auth |
| Upload a file | Not authorized | Yes |
| Download/read an object | Not authorized | Yes |
| Create/revoke share link | Not authorized | Yes, stronger step-up policy |
| Delete/restore object | Not authorized | Yes |
| Manage space membership | Not authorized | Yes |
| Read audit or quota | Not authorized | Yes |
| Propose/approve recovery | Not authorized | Yes, distinct proposer/approver |

## 6. Acceptance gates before adapter implementation

All gates are mandatory:
1. Core documents and implements a separate principal/token contract for HUMAN_USER, AI_AGENT and SERVICE, including delegation semantics.
2. Verified issuer, audience, signature/key rotation, expiry and revocation behavior, and exact API route are available from source and runtime.
3. Core returns explicit action/resource/tenant-scoped authorization decisions; unknown action defaults deny.
4. Task/assignment authorization is bound when agent work is delegated; no caller-supplied ACK booleans.
5. Grant source-hash defect C-CORE-01 is fixed for the execution subsystem; W1111 task/assignment and atomicity gaps are addressed where applicable.
6. Independent negative tests cover impersonation, cross-tenant/space IDOR, stale/revoked token, action escalation, share abuse, timeout, Core outage, stale policy, delegation mismatch and recovery self-approval.
7. Core startup/configuration and production key lifecycle are verified without exposing secrets; audit durability and backup/restore are tested.
8. Independent QE signs off against exact source commit and exact runtime build.

Until then, Work 33 may continue isolated local adapter and synthetic-principal tests, but no real user/agent integration or production file access.

## 7. Implementation seam (future, not active)

Keep the current application-facing interface narrow:
- `authorize(principal, action, resource, context) -> Decision`
- Decision must include `allow`, stable `reason_code`, policy/version reference and expiry/freshness metadata.
- `UnconfiguredAuthorizer` returns DENY for every request.
- A future `CoreAuthorizer` must be an explicit injected dependency; construction fails closed if required Core endpoint/trust configuration is absent.
- Do not expose raw bearer tokens to storage adapters, object metadata, audit text, exception messages or logs.
- Storage adapters receive only an already-authorized, server-derived object operation; they do not decide identity or permissions.

No CoreAuthorizer code is implemented by this document.

## 8. Current status

- W1111 execution grant source: inspected on feature branch only.
- W1111 grant: pytest execution purpose only; not Cloud Drive auth.
- Human/AI Agent principal contract for Cloud Drive: NOT VERIFIED.
- Core action/resource policy API: NOT VERIFIED.
- Work 33 CoreAuthorizer: NOT IMPLEMENTED.
- Default-deny authorization: retained as required.
- Runtime/tests/security QE: NOT RUN / NOT VERIFIED.
- No PASS claimed.
