# G0 Discovery Inventory — Mở rộng (Expansion 1)

- Thời điểm: 2026-10-24 (UTC+7)
- Người thực hiện: Vibe (agent hỗ trợ, ủy quyền tự chủ của Vinh)
- Căn cứ: DECISION_G0_INTEGRATION_POINT_20261024.md mục "Scope and caveats" yêu cầu mở rộng coverage trước khi tuyên bố toàn hệ thống.
- Trạng thái: DONE — bản ghi mở rộng; G0 vẫn RECORDED / NOT PASS (submodule chưa kiểm kê — xem BLOCKER dưới).

## 1. Các khu vực vừa kiểm kê (đọc trực tiếp file, commit ab2428f)

| Khu vực | File evidence | Kết luận về AI invocation / usage |
|---|---|---|
| `integration/room_hop_integration.py` | Toàn file | MCP **client** passthrough (stdio → Public V1). KHÔNG gọi AI provider, không có usage. Điểm quan trọng cho G4: client yêu cầu **5 tool** gồm cả `join_meeting`, trong khi bản inventory gốc ghi adapter chỉ khai báo 4 hằng số — cần đính chính (xem §3). |
| `10/COMPUTER-AGENT/04_CODE/` (agent_runtime.py, agent_api.py, browser_adapter.py, models.py) | Toàn 4 file | Playwright browser agent (observe/navigate/click/type/extract/screenshot). KHÔNG gọi LLM — không phát sinh token. Là **tool-activity path** cho G4 (từng action có evidence entry sẵn, tiền lệ tốt cho event envelope). |
| `30/GPT-AUTONOMOUS-BUILD-TEAM/` + `30/README.md` | README + listing | Mirror tài liệu governance của Work 30 (Sandbox); phase "independent planning", **không có code gọi AI** trong phần đã mirror. README tự ghi: mirror chưa byte-for-byte, "Do not treat as E2E verification". |
| `research/RC005, RC006, RC007` | Listing + file nhỏ | Fixture/test CRUD của ROOM-2026-001 (README 19–50 bytes, test_agent.txt). KHÔNG phải invocation path. |
| `core/secretary.py` | Toàn file | Secretary v0.3 chỉ append/read transcript thuần — không AI. |
| `docs/secretary_log.jsonl` | 44KB log | **Bằng chứng runtime thật 2026-08-15/16**: có chứng cứ lỗi Groq 429 với limit/used/requested tokens, model llama-3.3-70b-versatile; xác nhận P5 là đường gọi thật từng chạy. Cũng là tiền lệ JSONL ts+speaker+raw cho ledger format. |
| `docs/`, `schemas/`, `principals/`, `wee/`, `agents/`, `context/` | Listing | Không thêm đường gọi provider ngoài P1–P7 đã kê. `wee/` là runtime/gateway Python nội bộ (git_gateway, authority) — cần runtime check khi có môi trường ủy quyền, tĩnh không thấy HTTP AI call. |

## 2. Tổng kết coverage sau mở rộng

- Số invocation path provider: **vẫn 7 (P1–P7)**, không thêm đường mới; các thư mục còn lại không chứa đường gọi AI mới ở mức tĩnh.
- Usage-discard points: **vẫn 6** (không đổi).
- Tool-activity paths cho G4: MCP 8030 (5 tool), Execution host :8031 (/execute), Computer-Agent :8787 (/agent/execute) — tổng **3 instrument point cho tool events**.

## 3. Đính chính inventory gốc (errata)

1. `room_hop_mcp/adapter/server.py` khai báo 4 tool, nhưng `integration/room_hop_integration.py` yêu cầu **5** gồm `join_meeting`. Cần runtime verify xem Public V1 thật có 5 tool không — không kết luận chỉ từ static read.
2. `room-meeting-ai/` ở gốc repo là **git submodule** (SHA eeb497e9...), KHÔNG phải thư mục thường. Nội dung submodule **chưa được kiểm kê** trong discovery này.

## 4. BLOCKER còn lại trước khi G0 có thể PASS

- **Submodule `room-meeting-ai`**: phải checkout/đọc riêng submodule mới dám tuyên bố coverage toàn hệ thống. Đề xuất đầu việc mới: kiểm kê submodule, hoặc ghi rõ trong WORK_MANIFEST rằng scope Work 104 giới hạn ở cây chính.
- Runtime check MCP 8030 / Execution host :8031 / Computer-Agent :8787 chỉ làm được trong môi trường ủy quyền (điều kiện #3 của Decision W104-G0-006).
