# Work 05 ↔ Work 33 — Google Drive OAuth Capability Contract
Date: 2026-11-29
Status: CONTRACT DECIDED; cross-Work integration pending.

## 1. Boundary

- Core authorizes the actor, room membership, and selected Google connection.
- Work 05 owns OAuth state, refresh-token custody, encryption, refresh coordination, disconnect, and construction of an authorized Google Drive API v3 capability.
- Work 33 owns Drive file operations: create/update/list/get, upload retry, idempotency ledger, duplicate reconciliation, and file lifecycle.
- Work 33 MUST NOT read Work 05 credential storage, receive refresh tokens, persist OAuth credentials, or independently call Google's OAuth token endpoint.
- AI/LLM-facing code receives neither OAuth tokens nor Google SDK credential objects.

## 2. Request contract

Core → Work 05 factory (server-to-server only):

```python
build_connection_bound_drive_adapter(
    manager,
    room_id: str,
    user_id: str,
    connection_id: str,
    *,
    client_id: str,
    client_secret: str,   # runtime secret reference/value; never request input
    parent_id: str,       # authorized target folder
    adapter_factory: Callable,
)
```

Preconditions:
1. Core has authorized room + user + connection.
2. Work 05 independently checks that the connection belongs to the same room and user and is CONNECTED.
3. The granted scope includes `https://www.googleapis.com/auth/drive.file`.
4. The parent folder is an allowed destination for this operation.

Result:
- A server-side Drive adapter/service capability scoped to the selected user's OAuth credential.
- No raw access token, refresh token, authorization code, client secret, or SDK Credentials object is returned to UI, AI, or business-layer callers.
- Work 33 calls the capability's narrow file-operation methods only.

Failure contract:
- ownership/connection denied → authorization failure; no Google API call.
- missing/insufficient scope → permission/scope failure; no retry.
- disconnected/reauth-required → reauthorization-required; no upload.
- provider 429/5xx → Work 33 classifies according to its retry policy; Work 05 does not replay file creation.

## 3. Refresh after a Drive 401

The caller must preserve the access-token generation used by the failed request as an opaque comparison marker inside the trusted backend. The marker is not a refresh token and is not exposed to the AI/UI.

Required Work 05 operation (to be exposed as a capability wrapper; not yet implemented in this commit):

```python
refresh_connection_bound_drive_adapter(
    manager,
    room_id,
    user_id,
    connection_id,
    *,
    expected_access_token,
    client_id,
    client_secret,
    parent_id,
    adapter_factory,
)
```

Semantics:
1. Work 33 may invoke this operation at most once after the first 401.
2. Work 05 calls `ConnectionManager.refresh(..., expected_access_token=...)`.
3. If another request already refreshed the same connection, Work 05 detects that the stored access token no longer matches the expected marker and skips a second refresh.
4. Work 05 rebuilds and returns a fresh Drive capability from the currently stored credential.
5. Work 33 retries the original file operation at most once with a newly created request body.
6. A second 401 is terminal. No loop.

The current `ConnectionManager.refresh` implementation returns sanitized connection metadata, not tokens. The wrapper must build and return the authorized adapter; do not change the public refresh method to return token material.

## 4. Refresh outcome classification

| Provider outcome | Work 05 behavior | Work 33 behavior |
|---|---|---|
| Success | Save rotated credential atomically; status CONNECTED; sanitized audit | Rebuild capability; one retry of original operation allowed |
| `invalid_grant` | Delete unusable credential, status REAUTH_REQUIRED, raise `ReauthRequiredError`, preserve audit | Stop; request user reauthorization |
| 5xx / timeout / connection loss / ambiguous response | Do not replay; preserve current credential; status ERROR; raise `RefreshOutcomeUnknownError` | Stop; surface uncertain refresh outcome; do not assume token rotation failed |
| 403 / insufficient scope | Preserve credential; classify permission failure | Stop; no generic retry |
| second 401 after refresh | No further refresh | Stop after exactly two upload attempts and one refresh |

A generic network retry wrapper MUST NOT wrap the OAuth refresh endpoint.

## 5. Work 33 upload request contract

Work 33 accepts immutable operation data and an authorized Drive capability:

```python
upload_artifact(
    drive_capability,
    *,
    operation_id: str,
    idempotency_key: str,
    room_id: str,
    meeting_id: str,
    artifact_type: str,
    parent_id: str,
    file_name: str,
    content_sha256: str,
    byte_size: int,
    body_factory: Callable[[], BinaryIO],
)
```

Rules:
- `operation_id` and `idempotency_key` remain unchanged across retries and reconciliation.
- `body_factory()` returns a fresh stream for every attempt (RT-16).
- The create request writes the operation ID/idempotency key into Drive private `appProperties` in the same request as file creation.
- On ambiguous timeout/5xx, Work 33 transitions to UNKNOWN_OUTCOME and searches by exact appProperties key within the authorized parent/drive before considering another create (RT-13).
- Filename is not a uniqueness key.
- Work 33 owns durable operation ledger, duplicate detection, retry budget, Retry-After parsing, backoff, and reconciliation.
- Multiple matching files are a conflict requiring review; never auto-delete or arbitrarily choose one.

## 6. Retry ownership

| RT group | Owner |
|---|---|
| RT-01..05, RT-09..10, RT-13, RT-15..16 | Work 33 |
| RT-06, RT-08, RT-14 | Work 05 |
| RT-07, RT-11..12 | Cross-Work integration (Work 05 capability + Work 33 operation policy + Core authorization) |

## 7. Current implementation status

- Implemented in Work 05 source: per-connection synchronous single-flight lock; expected-access-token stale-call check; invalid_grant credential invalidation and typed reauth error; ambiguous 5xx/timeout no-replay error that preserves the credential.
- Added pytest cases: RT-06 concurrent refresh; RT-08 invalid_grant; RT-14 503 no-replay; timeout no-replay companion.
- Not implemented yet: refresh-capability wrapper returning a newly built Drive adapter; Work 33 production upload adapter; RT-07 end-to-end bridge.
- Tests have been authored but NOT EXECUTED in this environment. No PASS is claimed.
- PR #86 remains Draft and unmerged.
