# Google Workspace Room UI — Readiness / Blocker

The available Work 05 workspace contains the Python Core/MCP/adapter harness and connection façade, but no Room UI source, frontend framework, Room entry point, browser router, session/auth identity mechanism, or HTTP API routing layer. No parallel UI architecture is being created.

The future panel must render backend state: NOT_CONNECTED, CONNECTING, CONNECTED, REAUTH_REQUIRED, ERROR, and DISCONNECTED. It must call the existing backend connection façade using room ID, authenticated user context, and connection ID, and never receive or store tokens, authorization codes, private keys, client secrets, or raw credentials.

Once the canonical ROOM-HOP UI workspace is supplied, add the panel to the existing Room route, use the existing API layer, return OAuth callback to Room, and re-fetch backend state. The eventual panel must be responsive and keyboard/accessibility safe.

Status: ROOM UI BLOCKED by missing existing UI architecture, not by backend OAuth code.
