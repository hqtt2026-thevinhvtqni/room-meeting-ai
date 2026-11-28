# Google Connection API Contract

Room-facing operations are represented by `ConnectionAPI`:

- `connect(room_id, user_id)` returns `connection_id` and a controlled authorization URL.
- `callback(room_id, user_id, connection_id, callback_params)` validates state and returns sanitized connection metadata.
- `get(room_id, user_id, connection_id)` returns sanitized metadata only.
- `test(room_id, user_id, connection_id, client_factory)` loads credentials inside the trusted backend and returns sanitized metadata.
- `disconnect(room_id, user_id, connection_id)` invalidates the connection, deletes the credential, and returns sanitized metadata.

Work 05 operations use `ConnectionBoundOperations` and accept IDs plus operation input, never credential arguments. Credential resolution requires room and user ownership and CONNECTED state.

Safe response fields are connection ID, room/user ownership metadata needed by the backend, provider, status, account identity, scopes, and timestamps. Access token, refresh token, client secret, private key, authorization code, and raw credential object are excluded.
