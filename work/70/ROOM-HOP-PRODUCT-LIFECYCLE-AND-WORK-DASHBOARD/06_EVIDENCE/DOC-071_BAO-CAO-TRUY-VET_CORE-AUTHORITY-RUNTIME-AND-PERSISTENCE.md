# DOC-071 — BÁO CÁO TRUY VẾT CORE AUTHORITY, RUNTIME COMPOSITION VÀ PERSISTENCE

- **Document ID:** DOC-071
- **Priority:** P0
- **Read order:** 71
- **Depends on:** DOC-001; DOC-011; DOC-035; DOC-055; DOC-061; DOC-066
- **Status:** SOURCE TRACE COMPLETE — READ-ONLY / CORE OWNER NOT IDENTIFIED / RUNTIME NOT VERIFIED
- **Version / Updated:** 1.0 / 2026-11-02
- **Owner:** Xu / AI-01
- **Authority:** Vinh
- **Source baseline:** `hqtt2026-thevinhvtqni/room-meeting-ai`, GitHub `main`, HEAD `9ab3b80a979c1952f0b2b45a168e8ea94d73d424`
- **Execution boundary:** Source inspection only. No runtime invocation, code mutation, API creation, database mutation, permission change, or BUILD authorization.

## 1. Purpose and scope

Bổ sung truy vết cho WP-70-04 / SD-05 sau các báo cáo router-level trước đó. Mục tiêu lần này là phân biệt:
1. HTTP app factory có tồn tại với HTTP app thực sự được runtime khởi chạy;
2. Meeting persistence hiện có với authoritative Work/WP/Assignment/Evidence persistence;
3. Identity resolution với authorization/authority;
4. Search không có kết quả với bằng chứng khẳng định toàn repository không có implementation.

Không lặp lại audit chi tiết Execution Host `:8031`; phần đó tiếp tục tham chiếu DOC-061 và Work 28.

## 2. Source evidence inspected

| Source | Blob SHA | Direct observation |
|---|---|---|
| `room_hop_mcp/__main__.py` | `43adaa746f8e51a6ecce762a7b01694d0411d105` | Entrypoint khởi tạo `MeetingManager → MeetingService → create_server` và chạy MCP STDIO. Không thấy khởi tạo Work service. |
| `room_hop_mcp/adapter/server.py` | `f34b4eebc847dac31feb7c9161c2d8bded812991` | MCP adapter công bố 4 tools: list meetings, get meeting, get transcript, add paste. |
| `room_hop_mcp/adapter/http_server.py` | `54cb3ecbce2e6b13083f31c14f0c1f0738f1457d` | `create_http_app()` tạo FastAPI app với `/identities` và Meeting routes. Không có Work/WP/Assignment/Evidence routes trong file đầy đủ đã đọc. |
| `room_hop_mcp/browser_main.py` | `0d9e8956c52c2276388df56bf7336ba82766e0d1` | Entrypoint Uvicorn import `create_browser_app` từ browser adapter và bind `127.0.0.1:8001`; không import `create_http_app`. |
| `room_hop_mcp/adapter/browser_server.py` | `1b9dfe4b9d3f62e08a324ff146a9a50bb63e1313` | Browser runtime chỉ có Meeting list/get/transcript/paste, gọi qua `RoomHOPBridge`. |
| `core/meeting_service.py` | `0b80a81663c1be328c41878a6762d16d95378aab` | Application service boundary là Meeting-specific, delegate vào MeetingManager. Artifact operation là Meeting-scoped. |
| `core/meeting_manager.py` | `d4d7b28f0f0df9208648d0870c42cb6e451eda50` | MeetingManager dùng thư mục `meetings/`, mỗi Meeting có `meeting.yaml`; log/transcript/artifact là file-backed. Comment tại ID allocation ghi rõ `max(existing_seq)+1` không atomic, collision-detected. |
| `core/agent_registry.py` | `7e4b98e68fa1a208ebd5788d9235d9c222e402a3` | Module docstring nêu rõ registry không xử lý permissions/authority; fields authority/permissions chỉ là data forward-compatible. |
| `core/principal_registry.py` | `1eda0c80f413c1405415f92e0e2ff3b82a43b5ef` | Registry đọc human principal từ YAML; docstring nói không xử lý authorization/JOIN. |
| `core/identity_resolution.py` | `207c0ea74e3c77929c1723b0e66beba4ccf36201` | Chỉ resolve identity type và registry check; docstring nói Meeting Policy là bước riêng. |
| `requirements.txt` | `59e0a4c07842154d82784eff85a9b412c6b33263` | Dependency file không khai báo một database/ORM layer cho Work registry; đây không phải bằng chứng toàn repo không có storage adapter khác. |

## 3. Runtime composition findings

### 3.1 MCP STDIO runtime

`python -m room_hop_mcp` chạy `room_hop_mcp/__main__.py`; composition thực tế trong entrypoint là MeetingManager → MeetingService → MCP server. Tool surface hiện tại chỉ là Meeting.

### 3.2 Browser HTTP runtime

`python -m room_hop_mcp.browser_main` (theo entrypoint) khởi chạy Browser Runtime tại `127.0.0.1:8001`, dùng `create_browser_app()` và `RoomHOPBridge`. Browser adapter cũng chỉ công bố Meeting routes.

### 3.3 Core HTTP app factory

`room_hop_mcp/adapter/http_server.py` có factory `create_http_app()`, nhưng GitHub indexed code search cho `create_http_app uvicorn` không trả kết quả; tree/source đã kiểm tra cũng chưa xác định được một entrypoint khởi chạy factory này. Vì vậy:
- **Factory tồn tại:** VERIFIED.
- **Factory được gắn vào runtime đang chạy:** NOT VERIFIED.
- **Runtime endpoint của factory:** NOT RUN.
- Không được suy diễn từ việc có file FastAPI factory rằng route đang được serve.

Search là bounded theo GitHub code search/index và source paths đã kiểm tra; không phải chứng minh không tồn tại entrypoint ngoài phạm vi.

## 4. Persistence and authority boundary

- **Meeting persistence:** VERIFIED — file-backed trong phạm vi MeetingManager: thư mục `meetings/<meeting_id>/`, metadata `meeting.yaml`, log/transcript/artifact theo Meeting.
- **Work/WP/Assignment persistence:** NOT FOUND IN INSPECTED SCOPE / NOT VERIFIED. Không tìm thấy Work service/model/registry trong các entrypoint và service paths được kiểm tra.
- **Work Evidence Registry:** NOT FOUND IN INSPECTED SCOPE / NOT VERIFIED. Không có bằng chứng về Core-backed upload/read/version, atomic audit hoặc retention contract cho Work.
- **Database/transaction semantics:** NOT VERIFIED cho Work. Không lấy cơ chế YAML/file của Meeting làm bằng chứng cho authoritative Work store.
- **Core owner:** NOT IDENTIFIED. Không có bằng chứng owner được chỉ định có thẩm quyền chịu trách nhiệm Work API/persistence trong source baseline này.

Meeting ID allocation có comment nêu rõ không atomic; do đó Meeting file persistence không phải mẫu để suy rộng thành Work-level transactional store.

## 5. Identity is not Work authorization

- AgentRegistry và PrincipalRegistry là hai registry danh tính riêng.
- Identity Resolution chỉ trả lời identity thuộc loại nào và có resolve được hay không.
- MeetingManager có Meeting Policy riêng dựa trên creator/invited participants/participants.
- Không có bằng chứng trong các source trên về Work-scoped grant, permission check, assignment binding, expiry/revocation, or authorization middleware cho Work/WP/Evidence.
- Các field `permissions`/`authority` trong agent YAML không tự tạo enforcement.

## 6. Capability disposition

| Capability | Status | Reason |
|---|---|---|
| MCP Meeting STDIO | VERIFIED — source composition | Entry point and 4 tools inspected; runtime not invoked in this trace. |
| Browser Meeting HTTP | VERIFIED — source composition | Browser entrypoint binds port 8001; routes remain Meeting-scoped. |
| Core HTTP app factory | VERIFIED — factory only | `create_http_app` exists; runtime wiring not verified. |
| Work product-status API | NOT FOUND IN INSPECTED SCOPE | No Work route in inspected HTTP/browser adapters or MCP tool list. |
| Work Package API | NOT FOUND IN INSPECTED SCOPE | No Work Package route/service identified. |
| Assignment / ACK API | NOT FOUND IN INSPECTED SCOPE | No Work-scoped assignment service/route identified. |
| Work Evidence upload/read/version | NOT FOUND IN INSPECTED SCOPE | Meeting artifact methods are not a generic Work evidence registry. |
| Work-scoped authorization | NOT VERIFIED | Identity resolution and Meeting policy do not prove Work authorization. |
| Authoritative Work persistence and audit | NOT VERIFIED | No Work data service/store/transaction contract identified. |
| Core owner / accountable service owner | NOT IDENTIFIED | No authoritative owner evidence surfaced in inspected scope. |
| Runtime behavior and deployed endpoints | NOT RUN | Read-only source inspection only. |

## 7. Required next actions

1. Obtain the canonical Core owner and source baseline from the accountable maintainer; ask for the actual runtime composition/entrypoint, not only a proposed API contract.
2. Require source paths and exact revisions for any claimed Work registry, Work Package, assignment, Evidence Registry, authorization middleware, persistence adapter and audit implementation.
3. Trace router → service → model/schema → authorization → persistence → tests for each claimed Work capability.
4. If the owner confirms no Work service exists, submit a Core-owned architecture/implementation proposal; do not create a parallel Work database or guessed endpoint in Work 70.
5. Keep Dashboard in explicit local-snapshot mode until a real Core Work read API is proven.
6. Independent QE must verify positive and negative Work-scope authorization, tenant/work isolation, stale/error handling, audit persistence and runtime deployment before any live claim.

## 8. Gate and execution status

- WP-70-04 / SD-05: **BLOCKED — Core owner/API/auth/persistence NOT VERIFIED**.
- WP-70-03 / SD-06: **LOCAL SNAPSHOT ONLY — Core-live BLOCKED**.
- WP-70-05 / SD-07: **DESIGN ONLY — authoritative evidence storage contract NOT VERIFIED**.
- G0/G1: **NOT_READY**.
- G4 / BUILD: **NOT_READY / NOT PASS**.
- Runtime tests / independent QE: **NOT RUN**.
- Code, Core, API, database, permission, branch merge/rebase: **NOT MODIFIED / NOT PERFORMED**.
- Work 70: **NOT ACCEPTED / NOT RELEASED**.

**Conclusion:** Core hiện có Meeting/Identity capability trong source đã kiểm tra; chưa có bằng chứng đủ để Work 70 tích hợp Core-backed Work lifecycle, authorization, assignment hoặc evidence. Cần Core owner và source-level proof trước khi thiết kế adapter hoặc chuyển sang BUILD.
