# DOC-008 — Cloud Drive Core Adapter Design Gate (Provider-Neutral, No Invented API)

- Work: 33 — ROOM-SHARED-FILE-EVIDENCE-HUB
- Date: 2026-11-27
- Status: DESIGN PROPOSAL / NOT IMPLEMENTED / BLOCKED ON CORE TRUST CONTRACT
- Inputs: DOC-006, DOC-007, CORE_IDENTITY_PERMISSION_CONTRACT_V1.md, current Cloud Drive authorization.py.

## 1. Purpose

Define the smallest safe Cloud Drive integration seam without pretending Core already exposes token issuance, token verification, or resource authorization APIs. This is an interface design only. It does not select JWT/OAuth/mTLS, routes, claims, key URLs, or Core endpoints.

## 2. Current implementation boundary

Current cloud_drive/service/authorization.py has:
- Principal(subject_id) as a caller-supplied data object.
- Authorizer.authorize(principal, scope_id, action).
- UnconfiguredAuthorizer, which denies all.

This is safe only while no caller can mistake Principal for an authenticated identity. It is not a production principal model. Do not wire request JSON identity_id into it.

## 3. Required two-stage trust pipeline

HTTP request
  -> credential extraction (transport boundary)
  -> CredentialVerifier.verify(credential, expected_audience)
  -> VerifiedPrincipal (immutable, server-created)
  -> CorePolicyClient.authorize(principal, resource, action, context)
  -> explicit ALLOW with freshness/policy metadata
  -> Cloud Drive service operation
  -> audit event

Stage A — Authentication:
- Accept only a credential carried by the agreed trusted transport.
- Verify using Core-approved issuer/key or workload credential mechanism.
- Return a server-created immutable VerifiedPrincipal, never instantiate it from request body.
- Bind issuer, stable subject ID, principal type, tenant/organization, audience, issued/expiry times, token ID/revocation state and assurance.
- Reject missing, duplicate, malformed, expired, revoked, wrong-issuer, wrong-audience or inactive identity.
- Do not log raw credentials.
- Do not infer an AI identity from model name, agent display name, chat speaker or caller-supplied agent_id.

Stage B — Authorization:
- Ask the authoritative policy service for an exact resource/action decision.
- Bind tenant, Work, space, object ancestry and operation.
- Only explicit ALLOW with valid decision freshness permits operation.
- DENY, timeout, 5xx, malformed response, unknown policy version, stale response or unavailable authority => DENY.
- Do not cache until Core defines revocation and maximum-staleness semantics.
- Storage adapter must never receive credentials or make authorization decisions.

## 4. Proposed internal interfaces (not Core API)

These are internal Python ports only; they do not define HTTP route names or Core payload fields.

CredentialVerifier:
- verify(credential: SecretStr, expected_audience: str) -> VerifiedPrincipal
- raises AuthenticationDenied for every unverifiable or inactive credential.

VerifiedPrincipal (server-created, immutable):
- issuer
- subject_id
- principal_type: HUMAN_USER | AI_AGENT | SERVICE | OPERATOR
- tenant_id (nullable only where Core explicitly permits)
- audience
- issued_at
- expires_at
- token_id / revocation handle
- assurance level
- credential reference (never secret material)

CorePolicyClient:
- authorize(principal, resource_type, resource_id, space_id, work_id, action, request_context) -> AuthorizationDecision
- AuthorizationDecision carries ALLOW/DENY, decision_id, policy_id/version, evaluated_at, expires_at/max_age, safe reason code and obligations.
- Unknown resource/action combinations deny.

CloudDriveRequestContext:
- correlation_id
- operation_id/idempotency key
- environment
- request timestamp
- client metadata only where policy explicitly needs it; no client-provided identity authority.

These ports are adapters behind the existing service layer. Core transport schema is mapped only after actual Core contract is found and reviewed.

## 5. Principal binding and anti-spoof rules

- Request body/query identity fields are ignored for authority; if present, they may only be compared for diagnostics and must not override authenticated principal.
- Agent ID must be bound by verified workload credential to a registered AI_AGENT subject. A human's permission to invoke an agent does not make the agent equal to that human.
- SERVICE credentials are not interchangeable with HUMAN_USER or AI_AGENT.
- Registry membership may validate that a verified subject is registered/active, but membership alone never authenticates it.
- auth_verified=true, authorized=true, Message Header, YAML role, IP address and display name are not trusted principal proofs.

## 6. Authorization coverage

Every operation must call policy authorization, including reads:
- list spaces, list objects, read/download object
- create/rename/move/update metadata
- create/write/list/complete/abort upload
- list/read/restore versions
- create/revoke/use share links
- read/configure quota
- read audit
- propose/approve/execute recovery

A parent scope permission must not implicitly grant child operations unless Core policy explicitly defines that inheritance. Share-link access is a separate capability with expiry/revocation and bounded object/version scope.

## 7. Failure and security test contract

Authentication negative tests:
- missing credential, malformed header, duplicate Authorization header
- unknown key/algorithm, invalid signature, wrong issuer/audience
- expired/not-yet-valid/revoked token
- inactive/deleted subject, wrong principal type
- caller changes identity_id/agent_id in body while reusing another principal's credential

Authorization negative tests:
- explicit DENY, unknown action/resource, wrong tenant, wrong Work, wrong space/object
- Core timeout, 5xx, malformed response, stale decision/policy version
- attempted role escalation and SERVICE/HUMAN/AI_AGENT type confusion
- revocation between upload begin and complete; reauthorize at completion
- audit sink failure blocks protected mutation.

Positive tests:
- registered active human with explicit scoped ALLOW
- registered AI workload identity with explicit scoped ALLOW
- service identity only for its own narrowly scoped operations
- same principal denied outside authorized tenant/Work/resource scope.

## 8. Implementation gates

GATE A — Core discovery:
- Identify actual Core credential issuer/verifier or approved external identity provider.
- Verify issuer, signature/key lifecycle, audience, subject/principal binding, expiry/revocation.
- Identify actual policy decision contract and owner.
- Confirm Core HTTP route mount and live runtime parity.
No implementation until A passes.

GATE B — adapter:
- Implement CredentialVerifier and CorePolicyClient as separate injectable adapters.
- Fail startup or deny all if trust configuration absent.
- Never fall back to local registry or caller booleans.
- Ensure raw token is not passed to storage/audit layers.

GATE C — Cloud Drive integration:
- Replace caller-created Principal with VerifiedPrincipal at HTTP/service boundary.
- Reauthorize sensitive transitions, especially upload complete, share use/revoke, quota changes and recovery.
- Add complete negative/positive test matrix.

GATE D — independent verification:
- Security review and exact-HEAD CI.
- Runtime positive/negative probes on approved environment.
- No production acceptance from unit tests alone.

## 9. Decision

- This design can proceed independently of Core API naming because it defines only internal trust ports.
- Implementation of CredentialVerifier/CorePolicyClient is BLOCKED until actual trusted issuer and policy API are evidenced.
- Keep current UnconfiguredAuthorizer as DENY ALL.
- No code change, no Core route creation, no secret provisioning, no merge/deployment is authorized by this document.
