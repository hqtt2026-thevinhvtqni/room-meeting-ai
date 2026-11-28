# Google OAuth Security

The OAuth flow creates a single-use, expiring state bound to `room_id`, `user_id`, and the registered redirect URI. Callback validation rejects missing, mismatched, expired, or consumed state. The redirect URI is fixed by `OAuthConfig`; it is never supplied by the user or browser.

Authorization codes are accepted only in callback memory, exchanged immediately, and never logged or persisted in normal state. Provider errors and callback failures return generic sanitized errors; an error cannot create a CONNECTED state.

Credential data is encrypted before development-store persistence. The encryption key must be supplied by secure runtime configuration. Credential files are private-directory/0600 files. The production integration boundary is a managed secret manager implementing `save/load/delete/exists` and optional refresh/rotation.

The connection lifecycle supports CONNECTING, CONNECTED, ERROR, REAUTH_REQUIRED, and DISCONNECTED transitions. Refresh success returns to CONNECTED; refresh failure becomes REAUTH_REQUIRED; disconnect deletes the credential and prevents later operation resolution. No infinite retry is used.

Ownership checks require both `room_id` and `user_id` in addition to `connection_id`. Safe metadata responses exclude raw credential material. Offline tests verify state replay rejection, encrypted persistence, ownership isolation, sanitized responses, refresh failure, disconnect, and connection-bound operations.
