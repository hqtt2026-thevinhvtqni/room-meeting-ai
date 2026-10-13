# Work 101 Dashboard

Static shell only. It does not invent live status. Until an approved read-only data contract/API is connected, it explicitly reports live data as not connected.

Required data: Work lifecycle from authoritative registry; target/revisions/read-back; structure and digest parity; pending changes/conflicts/blocked dependencies/approvals; test and E2E evidence with timestamps; freshness and operation IDs.

Render-only: no browser-held tokens and no direct mutation. Mutations must go through approved Core/MCP capabilities. Unknown data is never PASS. File read-back is not browser runtime evidence.
