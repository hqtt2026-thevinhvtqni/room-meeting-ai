# W05 — Google Drive OAuth Adapter Security Architecture
Date: 2026-11-29
Status: DECISION / DESIGN BASELINE — NOT IMPLEMENTED

## 1. Purpose and ownership
Work05 owns Google OAuth user-connection lifecycle and credential custody. Work33 owns storage operations and the storage adapter. Meeting/AI business services consume normalized application interfaces and must not handle OAuth tokens or Google client objects.

## 2. Security invariants
1. Least privilege: default scope is `https://www.googleapis.com/auth/drive.file`. This scope is limited to files created by the app or files explicitly selected/shared with the app through a supported user-selection flow; it is not blanket access to all existing Drive files. Any broader scope requires a documented use case, user consent, and security review.
2. Server-side secrets: client secret, authorization code, access token and refresh token never enter browser storage, frontend logs, URLs beyond the standard short-lived OAuth callback code, or client-visible API responses.
3. Token at rest: encrypt refresh tokens using authenticated encryption (AES-256-GCM or KMS envelope encryption). Persist key version and nonce/IV; authenticate user/connection metadata as AAD where supported. Keep encryption keys outside the database and source control. Access tokens should be short-lived/in-memory where practical; if persisted, encrypt them too.
4. CSRF protection: cryptographically random, single-use state bound to the initiating authenticated session and user/workspace, with short expiry and server-side validation before code exchange. Consume state once. Use PKCE (S256) where supported by the OAuth client flow.
5. Isolation: every credential lookup and Drive operation must be scoped to the authenticated user plus connection ID and an authorized room/workspace membership check. Never trust userId, roomId, or connectionId supplied by an untrusted client without Core authorization.
6. Refresh concurrency: single-flight/mutex per connection; atomically update token material and expiry. Handle invalid_grant by marking connection reauthorization-required, not by retrying indefinitely.
7. Disconnect: revoke with Google when possible, delete or cryptographically erase stored token material, and write an audit event without recording secrets.
8. Reliability: classify 401/invalid credentials, insufficient scope, invalid_grant, 403 quota/permission, 429 and 5xx distinctly. Retry transient 429/5xx with bounded exponential backoff and jitter; do not retry authorization failures as transient.
9. Data integrity: no silent overwrite. Use explicit create/version/update semantics and record artifact metadata, actor, room, destination and result in audit logs. Avoid logging transcript/audio contents or OAuth secrets.

## 3. OAuth lifecycle
A. Start connect: authenticated server endpoint creates state + expiry + session/user binding; returns Google authorization URL with offline access. Request consent only when needed to obtain/repair a refresh token, not on every connection attempt.
B. Callback: validate state, session and user binding; exchange code only on server; validate granted scopes; encrypt and persist token record; redirect to a safe application URL. Never accept arbitrary redirect targets.
C. Access: Core authorization confirms actor, room/workspace membership and connection ownership before Work05 resolves credentials. Work05 returns a valid server-side credential to the adapter only.
D. Refresh: refresh before expiry or on an eligible authentication failure; serialize refresh per connection; persist rotated token material atomically; handle revoked/expired refresh tokens as reauthorization-required.
E. Disconnect: explicit user action revokes token and removes credential material. Room membership removal separately removes room-level authorization and sharing; it must not automatically revoke the user's entire personal Drive connection unless an explicit policy says so.

## 4. Data model (logical)
- connection_id, user_id, provider, status
- encrypted_refresh_token, key_version, nonce/tag metadata
- encrypted_access_token only if persistence is required; expires_at
- granted_scopes, created_at, updated_at, last_used_at
- workspace/tenant association where applicable
Do not store plaintext tokens, client secrets, authorization codes, or raw state values.

## 5. API boundary
GoogleDriveOAuthAdapter should expose normalized operations such as:
- createAuthorizationUrl(authenticatedContext)
- handleCallback(code, state)
- getValidAccessToken(authorizedConnectionContext)
- uploadMeetingArtifact(authorizedContext, metadata, content)
- readSelectedReference(authorizedContext, fileId)
- disconnect(connectionId, authenticatedContext)
Business services must not receive refresh tokens or Google SDK credential objects.

## 6. AI meeting-room policy
- Personal minutes and private references: user-owned connection, with room authorization checked per operation.
- Shared workspace repository: use an explicitly approved workspace connection or delegated model with documented ownership, admin controls and audit trail. Do not silently substitute a service account.
- On room leave: revoke room access and remove room-level shares/permissions as policy requires; preserve unrelated personal Drive connection.
- Audio/transcript/minutes are sensitive meeting data: explicit destination, access list, retention/deletion policy and audit trail are required.

## 7. Required test gates
- state mismatch, expiry, replay and cross-user callback rejection
- no token/client secret leakage in responses/logs
- encryption/decryption and key-version rotation
- scope validation and insufficient-scope behavior
- refresh single-flight under concurrent requests
- invalid_grant -> reauthorization-required
- disconnect revocation and local credential erasure
- user/room/workspace cross-tenant isolation
- 401/403/429/5xx classification and bounded retry
- upload collision/no-overwrite behavior and audit event
- Work05 + Work33 + Core authorization integration regression

## 8. Current evidence and gaps
- Existing Work05 branch contains an OAuth-user Drive factory draft and four authored tests, previously reported as NOT RUN.
- The draft resolves credentials through Work05 ConnectionManager and uses drive.file.
- This does not prove a complete OAuth lifecycle, encryption at rest, CSRF state handling, refresh serialization, revocation, Core authorization, Work33 integration, or live Google API operation.
- Sandbox read tool did not return file contents in this session; no source-level inspection or test execution is claimed here.

## 9. Merge/release gates
Keep PR #86 Draft and unmerged until source-level review, Core authorization integration, Work33 contract integration, focused and combined tests, and independent security review all pass with inspectable evidence.


## 10. Retry policy decision — 429 and 5xx
- Retry only transient failures: HTTP 429, 500, 502, 503 and 504. Do not retry 400-class validation/authentication failures (including invalid_grant), 401 refresh loops, 403 permission/insufficient-scope failures, or malformed requests.
- For Drive API operations, honor a valid Retry-After header (delta-seconds or HTTP-date) subject to a configured maximum wait. Otherwise use exponential backoff with full jitter; cap both the delay and total attempts (initial attempt plus at most 2 retries by default). Make limits configurable and test them with fake timers; never sleep indefinitely.
- Retry only operations with safe replay semantics. Upload must use an idempotency strategy or detect/reconcile an ambiguous prior create before retrying, so a timeout/5xx after Google accepted the upload cannot create duplicate meeting artifacts. Do not silently overwrite an existing file.
- For OAuth token refresh endpoint calls, do not blindly reuse a refresh token after an ambiguous network failure or 5xx: the provider may have processed a rotating refresh token even if the response was lost. Preserve the last known encrypted credential, surface a sanitized transient refresh error, and retry on a later authorized operation unless provider-specific behavior and atomic rotation handling prove immediate retry safe. A definitive 429 response may be retried only under an explicit provider-specific policy, with bounded Retry-After.
- A 429 from Drive API must never delete or invalidate the user's token. An invalid_grant from the token endpoint transitions the connection to REAUTH_REQUIRED and prevents further refresh attempts until the user reconnects; preserve a non-secret audit record of the transition.
- Tests must assert attempt count, Retry-After handling/cap, jitter bounds, no retry on permanent errors, no token deletion for 429/5xx, no infinite retry, and no duplicate upload after ambiguous outcomes.
