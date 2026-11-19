# Work 17 Capability Dashboard

Evidence-first dashboard for **ROOM-HOP-AI-AGENT-CAPABILITY-BASELINE-AND-FOCUSED-ENABLEMENT**.

## Quick Start (CACHE mode — data thật từ MCP snapshot)

```bash
cd 04_CODE/WORK17_DASHBOARD
node server.js
# or npm start
```

Open: **http://localhost:3000**

- No external dependencies (Node.js ≥ 18 built-ins only).
- Serves static + `/api/live` + `/api/health`.
- Default = **MCP CACHE** (đọc `live-data.json` — snapshot MCP thật do AI cập nhật).

## MCP LIVE mode (bridge)

```bash
# Terminal 1 — stub local (test đường live)
node mcp-bridge-stub.js
# lắng nghe :3100

# Terminal 2 — dashboard trỏ vào stub
export MCP_BRIDGE_URL="http://127.0.0.1:3100/api/work17-live"
node server.js
```

UI sẽ hiện **MCP LIVE** khi bridge healthy. Khi có bridge MCP thật (Gateway / Core), chỉ cần đổi `MCP_BRIDGE_URL` — không sửa frontend.

Xem chi tiết contract: **`BRIDGE_CONTRACT.md`**.

## Features

- KPI overview (Works, mirrors, agents, P0 gaps)
- Gate progression G0–G7
- 13 Agent types matrix + evidence level
- AI Member readiness (CONFLICT / NOT VERIFIED)
- Gap register + filters
- End-to-end trace map
- Dynamic mirror coverage ring
- MCP live adapter + cache fallback + reconnect/backoff
- Auto-refresh 30s + health heartbeat 15s
- Responsive mobile-first
- HTML escaping an toàn

## Files

| File | Vai trò |
|------|---------|
| `server.js` | HTTP server + `/api/live` + bridge client |
| `mcp-bridge-stub.js` | Stub HTTP giả lập bridge (test MCP LIVE) |
| `BRIDGE_CONTRACT.md` | Contract chuẩn hóa payload |
| `live-data.json` | Cache snapshot MCP (AI refresh) |
| `index.html` / `app.js` / `styles.css` | UI |
| `MCP_LIVE_INTEGRATION.md` | Giải thích runtime behavior |

## Status

- Dashboard **runnable + complete** (READ / TRACE ONLY).
- Data cache refresh: **2026-11-19 21:48 +07** (71 Works từ `sandbox_list_works`).
- Bridge HTTP thật: chờ Gateway / Work 01 / Work 113 — contract + stub đã sẵn trong Work 17.


## Integrity hardening — 2026-11-20

- Local bridge stub is intentionally labelled `mcp-stub` / `fresh=false`; it cannot produce MCP LIVE status.
- MCP LIVE requires a schema-valid payload with explicit live provenance and a timestamp within the configured freshness window.
- Cache fallback remains `mcp-cache` / `fresh=false` and carries a warning when the bridge fails validation.
- `/api/health` verifies cache readability; a configured bridge is reported as configured but not probed.
- Static file paths are checked against the resolved dashboard root, including symlink resolution.
- Run `npm test` for the Node built-in regression suite. No runtime PASS is claimed until the suite is executed and its output is journaled.
