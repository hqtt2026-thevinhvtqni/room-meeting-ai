# Google Workspace Connection Architecture

The product boundary is:

`User → Room UI → Core/MCP → Google Workspace Connection → Secure Credential Store → Google Workspace Adapter → Google Drive/Docs`

Core owns connection metadata, ownership, authorization state, and a credential reference. The Secure Credential Store owns credential material. The Google Workspace Adapter receives credential material only inside the trusted backend operation boundary. AI, MCP messages, Room state, audit, and normal responses receive only connection IDs and sanitized metadata.

Connection metadata contains `connection_id`, `room_id`, `user_id`, provider, state, account identity, granted scopes, timestamps, and a credential reference. It never contains raw access tokens, refresh tokens, client secrets, private keys, or authorization codes.

The existing Core remains the single source of truth. No parallel Google pipeline or second Core was introduced. `ConnectionBoundOperations` resolves a credential only after checking room/user ownership and connection state, then creates the provider inside the backend boundary.

The development store is encrypted-file based using Fernet. Its key is mandatory runtime input from `W05_CREDENTIAL_STORE_KEY`; it is never hard-coded. Production must replace this implementation with a managed secret store behind the same `CredentialStore` interface.
