# TODO — Work 17 Capability Dashboard

## Status: COMPLETED + BRIDGE READY (2026-11-19 21:48)

- [x] Hiển thị tổng quan ACTIVE / READ–TRACE ONLY và các chỉ số evidence-first.
- [x] Hiển thị Gate G0–G7 cùng trạng thái, tiêu chí và bằng chứng liên quan.
- [x] Hiển thị ma trận 13 loại AI Agent với mức evidence và giới hạn.
- [x] Hiển thị GAP register P0/P1/P2, trạng thái và tiêu chí nghiệm thu.
- [x] Hiển thị portfolio 71 Work, mirror coverage (dynamic ring) và vị trí của Work 17.
- [x] Hiển thị AI member capability và các điểm NOT VERIFIED/CONFLICT.
- [x] Hiển thị chuỗi end-to-end và các điểm OPEN/BLOCKED.
- [x] Có bộ lọc theo trạng thái, gate, priority và search.
- [x] Responsive mobile-first, route manifest, chạy được trên Preview port 3000.
- [x] MCP live adapter + cache fallback + reconnect/backoff + health check.
- [x] Ring coverage động theo dữ liệu thực tế.
- [x] Fix HTML escaping (esc) — XSS-safe.
- [x] Refresh live-data.json từ MCP thật (sandbox_list_works = 71) — 21:48 +07.
- [x] **BRIDGE_CONTRACT.md** — contract chuẩn hóa payload cho bridge MCP.
- [x] **mcp-bridge-stub.js** — stub HTTP local để test đường MCP LIVE.
- [x] server.js + README cập nhật hướng dẫn LIVE / CACHE.

## Cách chạy

### CACHE (mặc định — data thật snapshot)
```bash
cd 04_CODE/WORK17_DASHBOARD
node server.js
```

### LIVE (stub local)
```bash
# Terminal 1
node mcp-bridge-stub.js

# Terminal 2
export MCP_BRIDGE_URL="http://127.0.0.1:3100/api/work17-live"
node server.js
```

## Ghi chú
- Không cần dependencies ngoài.
- Bridge MCP thật (gọi sandbox_list_works trực tiếp) cần lớp Gateway/Core có quyền MCP — contract đã sẵn, chỉ đổi URL.
- AI có thể tiếp tục refresh `live-data.json` bất cứ lúc nào để giữ snapshot mới.


## Integrity hardening implementation — 2026-11-20

- [x] Prevent local cache stub from claiming MCP LIVE; label it `mcp-stub` / `fresh=false`.
- [x] Validate normalized payload structure and required field types.
- [x] Require explicit live provenance and bounded freshness before MCP LIVE acceptance.
- [x] Preserve cache fallback and warning on bridge failure or invalid/stale payload.
- [x] Make health response verify cache readability and distinguish configured-but-unprobed bridge.
- [x] Harden static file containment with decoded path, path-boundary and resolved-path checks.
- [x] Add client-side schema guard and preserve last valid data on invalid response.
- [x] Add Node built-in regression tests for schema, freshness, health, traversal and method policy.
- [ ] Run Node regression tests and browser E2E on PC/VS Code.
- [ ] Independent QE review and GitHub main read-back/sync.

Status: SOURCE PREPARED IN WORK17 SANDBOX; RUNTIME NOT RUN; NOT PASS.
