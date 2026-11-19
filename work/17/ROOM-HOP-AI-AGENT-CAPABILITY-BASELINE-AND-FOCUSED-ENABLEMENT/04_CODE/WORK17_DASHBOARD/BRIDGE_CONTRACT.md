# Work 17 — MCP Bridge Contract

**Version:** 1.0 · 2026-11-19  ·  Owner: Work 17 / Vinh · Coordinator: Xu / AI-01

Dashboard Work 17 **không** gọi MCP tools trực tiếp từ browser. Server chỉ gọi HTTP bridge (nếu có) hoặc fallback cache.

## 1. Endpoint

```
GET {MCP_BRIDGE_URL}
```

- Method: `GET`
- Timeout khuyến nghị phía dashboard: **7 giây**
- Header tùy chọn: `Authorization: Bearer {MCP_BRIDGE_TOKEN}`
- Response: `200 application/json` đúng schema bên dưới

## 2. Required JSON shape (normalized)

Bridge **bắt buộc** trả object có đủ 8 key:

| Key        | Type   | Mô tả ngắn |
|------------|--------|------------|
| `meta`     | object | Nguồn, timestamp, fresh flag |
| `summary`  | object | works, mirrors, agentsRead, p0Open |
| `gates`    | array  | G0–G7 với id/name/state/detail |
| `portfolio`| object | works, mirrors, missingMirrors |
| `agents`   | array  | 13 dòng [type, evidence, finding, source] |
| `members`  | array  | [id, role, status1, status2] |
| `gaps`     | array  | [id, title, domain, priority, state, criteria, gate] |
| `e2e`      | array  | [step, name, detail, owner, state] |

### meta (bắt buộc)

```json
{
  "source": "mcp-live",
  "fresh": true,
  "syncedAt": "2026-11-19T21:48:00+07:00",
  "workId": "17",
  "bridgeConfigured": true,
  "note": "optional free text"
}
```

- `source` phải là `"mcp-live"` khi data đến từ MCP tools thật.
- `fresh` = `true` khi vừa lấy từ MCP trong lần gọi này.
- Dashboard sẽ set `meta.source = "mcp-cache"` và `fresh = false` nếu fallback.

### summary

```json
{
  "works": 71,
  "mirrors": 17,
  "agentsRead": 13,
  "p0Open": 5
}
```

### gates (ví dụ 1 phần tử)

```json
{
  "id": "G0",
  "name": "Inventory snapshot",
  "state": "REFRESHED",
  "detail": "71 Work snapshot..."
}
```

States hợp lệ (badge): `REFRESHED | IN PROGRESS | NOT VERIFIED | BLOCKED | OPEN | NOT STARTED | PENDING | LOCKED | PARTIAL | CONFLICT | DESIGN ONLY`

### portfolio

```json
{ "works": 71, "mirrors": 17, "missingMirrors": 54 }
```

### agents / members / gaps / e2e

Giữ đúng shape mảng-of-arrays như trong `live-data.json` (xem file đó làm reference canonical).

## 3. Nguồn data mà bridge nên gọi

Bridge (khi có quyền MCP) nên:

1. `sandbox_list_works` → đếm works, cập nhật `summary.works` + `portfolio`
2. Đọc `04_PLAN/WORK_17_GAP_REGISTER.md` (và/hoặc journal) → gaps
3. Đọc capability matrix / member matrix nếu có → agents + members
4. **Không** tự suy diễn PASS / E2+ nếu không có evidence runtime

Dashboard **không** tin bất kỳ claim PASS nào nếu không có bằng chứng tương ứng trong payload.

## 4. Cách dùng với dashboard hiện tại

```bash
# 1. Chạy bridge thật (sau này) ở một process khác, ví dụ port 3100
#    GET http://localhost:3100/api/work17-live  → JSON đúng contract

# 2. Trỏ dashboard tới bridge
export MCP_BRIDGE_URL="http://localhost:3100/api/work17-live"
# export MCP_BRIDGE_TOKEN="..."   # nếu bridge yêu cầu

cd 04_CODE/WORK17_DASHBOARD
node server.js
# → UI hiện MCP LIVE khi bridge healthy
```

Nếu `MCP_BRIDGE_URL` trống hoặc bridge lỗi → dashboard tự fallback `live-data.json` và hiện **MCP CACHE**.

## 5. Stub trong Work 17

File `mcp-bridge-stub.js` (cùng thư mục) là stub HTTP nhỏ:

- Đọc `live-data.json`
- Trả về với `meta.source = "mcp-live"` + `fresh = true` (giả lập live)
- Dùng để test đường `/api/live` → bridge trước khi có bridge MCP thật

```bash
# Terminal 1 — stub bridge
node mcp-bridge-stub.js
# lắng nghe :3100

# Terminal 2 — dashboard
export MCP_BRIDGE_URL="http://127.0.0.1:3100/api/work17-live"
node server.js
```

Khi Gateway / Work 01 / Work 113 cung cấp bridge MCP thật, chỉ cần đổi `MCP_BRIDGE_URL` — không cần sửa frontend.

## 6. Giới hạn hiện tại (evidence-first)

- Node process trong sandbox **không** có MCP client native → stub không thể tự gọi `sandbox_list_works`.
- Data “thật” hiện tại được AI (qua MCP tools) ghi vào `live-data.json` rồi dashboard đọc cache.
- Bridge HTTP thật cần chạy ở lớp có quyền MCP (Gateway / Core / service riêng).

## 7. Checklist khi implement bridge thật

- [ ] Trả đủ 8 key bắt buộc
- [ ] `meta.source = "mcp-live"` và `meta.fresh = true` khi thành công
- [ ] Timeout / error → dashboard tự fallback, không crash UI
- [ ] Không tạo claim PASS / E2+ nếu không có evidence
- [ ] Ghi `syncedAt` ISO 8601 có timezone


## Work17 dashboard integrity addendum — 2026-11-20

1. **Truthful source labels:** local stub replay MUST return `meta.source=mcp-stub`, `meta.fresh=false`, and `realMcp=false`. It MUST NOT impersonate `mcp-live` or be used as live acceptance evidence.
2. **Live acceptance:** dashboard accepts MCP LIVE only when the bridge payload passes the complete normalized schema, explicitly declares `meta.source=mcp-live` and `meta.fresh=true`, and supplies a parseable `meta.syncedAt` no older than five minutes (maximum age configurable by `MCP_LIVE_MAX_AGE_MS`; timestamps more than 60 seconds in the future are rejected).
3. **Fallback:** invalid, stale, malformed, unreachable or non-live bridge responses fall back to a schema-valid cache with `source=mcp-cache`, `fresh=false`, and a warning. Cache fallback is never relabelled as live.
4. **Health semantics:** `/api/health` distinguishes process liveness from cache readiness and reports a configured bridge as `configured-not-probed`; it does not claim the bridge is healthy without an actual bridge probe.
5. **Static file boundary:** static paths are URL-decoded, resolved and checked with path-relative boundary checks; symlink-resolved paths must remain inside the dashboard root. Only GET/HEAD are served.
6. **Testing:** run `npm test` from the dashboard directory. Tests cover schema rejection, live freshness/provenance labels, health/cache readiness, method restrictions and encoded traversal. Runtime results must be journaled separately; source presence is not PASS.
