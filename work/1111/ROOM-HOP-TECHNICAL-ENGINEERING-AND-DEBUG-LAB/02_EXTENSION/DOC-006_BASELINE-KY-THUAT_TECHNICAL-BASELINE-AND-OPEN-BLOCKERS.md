
# TECHNICAL BASELINE & OPEN BLOCKERS — WORK 1111

Ngày khảo sát: 2026-11-08  
Nguồn thao tác: ROOM-HOP MCP 8030, Sandbox Works và hồ sơ kỹ thuật đã lưu.  
Phạm vi: baseline ban đầu, không phải nghiệm thu toàn hệ thống.

## 1. Source-of-truth và môi trường

| Lớp | Vai trò tạm xác định | Bằng chứng / giới hạn |
|---|---|---|
| GitHub | Nguồn chuẩn cho source code và revision đã phát hành | W32 audit phân biệt exact branch/SHA; W1111 chưa tự truy vấn HEAD hiện tại |
| Sandbox | Không gian AI đọc/ghi hồ sơ, candidate và phối hợp | MCP context xác nhận Sandbox read/write |
| Working Source qua MCP | Read-only | get_room_context |
| PC | Runtime/working copy cục bộ, cần đối chiếu theo exact path/SHA | W70 log ghi nhận working tree dirty và parity chưa xác minh |
| MCP 8030 | File operations trong Sandbox | get_room_structure; không có process/pytest execution trong capability list |
| Git merge/commit/push | Không thuộc quyền AI trong MCP boundary hiện tại | get_room_context |

Đây là mô hình vận hành ban đầu. Chưa coi GitHub/Sandbox/PC đã đồng bộ.

## 2. Bản đồ thành phần ROOM-HOP (danh mục cần xác minh)

- Core :8000 — authority / application truth.
- Dashboard :3000 — render-only, không được dùng làm authority.
- Workspace :8010 — workspace/application layer.
- Gateway :8040 — gateway.
- Event Listener :8050 — event intake.
- Agent Runtime :8051 — runtime agent.
- Build MCP :8030 — Sandbox build/file operations.
- Execution Host :8031 — execution host cần xác minh contract và đường gọi thực.
- Adapter / Browser Agent — cần phân biệt source, process, health, contract và E2E evidence.
- Agent Registry / Principal / Policy / Token — cần kiểm tra mapping identity và quyền theo hồ sơ canonical.

Tên/cổng ở trên là baseline danh mục từ hồ sơ dự án; trạng thái live của từng service chưa được xác minh trong lượt này.

## 3. Nút thắt đã có bằng chứng

### B-1111-01 — GitHub/Sandbox drift (W32)
- Evidence: audit 2026-11-07 ghi 6/6 cặp file DRIFT.
- Impact: review hoặc test trên mirror cũ có thể xác nhận sai revision.
- Next: lập mapping exact branch + SHA + path + blob/hash; chỉ đồng bộ theo change control, không overwrite mù.

### B-1111-02 — Windows Browser E2E / release gate (W32)
- Evidence: Run #133, SHA 554ebe3145e8b13206b50d8722879b0bae3db094; Windows job SKIPPED; release gate FAILURE.
- Impact: W32 chưa RELEASED; hosted tests không thay thế Windows live lane.
- Next: xác minh runner readiness và service provenance theo đúng hồ sơ; không bypass readiness guard.

### B-1111-03 — Thiếu execution adapter qua MCP
- Evidence: MCP capability/context và W102 integration gap ledger.
- Impact: không thể tuyên bố pytest đã chạy chỉ từ việc tạo/đọc file; không có stdout/stderr, exit code hay test result thực.
- Next: khảo sát công cụ execution host/CI có thể truy cập; thiết lập exact-SHA run evidence và readback.

### B-1111-04 — PC/GitHub/Sandbox parity chưa xác minh (W70)
- Evidence: DOC-035 ngày 2026-11-08; PC working tree dirty, mirror path mismatch.
- Impact: thao tác đồng bộ hoặc cleanup có thể phá thay đổi chưa commit.
- Next: chỉ read-only inventory; path/hash mapping; không reset/clean/stash/checkout hoặc overwrite.

### B-1111-05 — Inventory noise (W09)
- Evidence: sandbox listing có 4,127 entries, bao gồm .venv, site-packages, __pycache__.
- Impact: khó phân biệt source, dependency cache và runtime artifacts.
- Next: phân loại file-level; chưa xóa/di chuyển.

## 4. Những gì chưa được xác minh
- GitHub main và từng branch HEAD tại thời điểm hiện tại.
- Live health/contract của các service và ports.
- Registry identity/principal/policy/token đầy đủ.
- Runner/service state thực tế trên PC.
- Pytest execution trong MCP session.
- Exact SHA parity GitHub↔Sandbox↔PC.
- Dependency graph hoàn chỉnh giữa các Work.

## 5. Kết luận baseline
DISCOVER = PARTIAL.  
Không có source mutation, Git mutation, PC mutation, test execution hoặc release action trong lượt khảo sát này.  
Các kết luận được giới hạn đúng theo hồ sơ đã đọc; cần bổ sung kiểm chứng live trước khi nâng trạng thái.

## Bổ sung/correction sau GitHub source trace — 2026-11-08
Nhận định "không có execution host" sẽ là sai. Source GitHub main có Execution Host :8031 và code thực thi process thật. Kết luận đúng là: MCP 8030 không expose process/pytest action trong phiên hiện tại; live service :8031 và revision được deploy chưa được xác minh. Branch work/28-mcp-tooling-platform có handler hardening riêng, nhưng main vẫn trả source handler khác; không đồng nhất hai nhánh. DOC-061 trên GitHub main còn ghi nhận các giới hạn auth/grant/snapshot và potential false aggregate PASS. Chi tiết và SHA được lưu tại 03_ARCHITECTURE/EXECUTION_HOST_SOURCE_TRACE.md.
