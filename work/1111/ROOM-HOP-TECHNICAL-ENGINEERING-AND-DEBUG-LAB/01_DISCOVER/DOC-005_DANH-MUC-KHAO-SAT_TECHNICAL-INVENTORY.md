# DISCOVER-1111-001 — DANH MỤC KHẢO SÁT KỸ THUẬT

## Phạm vi kiểm kê
- Repository, nhánh chuẩn; trạng thái đồng bộ GitHub / Sandbox / PC.
- Core, Dashboard, Workspace, Gateway, Event Listener, Agent Runtime.
- MCP Build, Execution Host và adapter.
- Agent registry, identity, principal/policy và token usage.
- CI/CD, runner, unit/integration/E2E tests.
- Work kỹ thuật liên quan, lỗi tồn đọng, quyết định kiến trúc và nhật ký bằng chứng.

## Trạng thái
- Work Sandbox 1111: CREATED — PASS.
- Technical inventory: PLANNED — chưa khảo sát.
- Không suy diễn trạng thái thành phần khi chưa đọc source/evidence.

## Kết quả khảo sát ban đầu — 2026-11-08
- Sandbox registry: 60 Works; W1111 được đăng ký và có manifest.
- MCP 8030: file operations trên Sandbox; Working Source read-only; không merge/commit/push; capability list không có process/pytest execution.
- W32: 6/6 cặp GitHub↔Sandbox file bị DRIFT theo audit 2026-11-07; Run #133 exact SHA 554ebe3145e8b13206b50d8722879b0bae3db094 có Windows E2E SKIPPED và release gate FAILURE.
- W70: nhật ký 2026-11-08 ghi nhận PC working tree dirty và GitHub/PC parity chưa xác minh; bảo toàn nguyên trạng.
- W09: listing có 4,127 entries, bao gồm .venv, site-packages, __pycache__; cần phân loại inventory, chưa xóa.
- W102: kiến trúc tích hợp ghi nhận thiếu process/pytest execution adapter trong MCP, live PC/Core bridge và canonical execution evidence chưa được chứng minh.
- **Trạng thái tổng:** PARTIAL — đây là baseline từ hồ sơ Sandbox và MCP metadata, không phải xác minh live GitHub/PC/runtime.

## Bổ sung sau GitHub/W13 source trace — 2026-11-08
- GitHub main có source Execution Host :8031 (server, host, security, identity, WEE bridge); đây là source evidence, không phải runtime evidence.
- Branch work/28-mcp-tooling-platform có handler hardening riêng; không đồng nhất với main. Main và branch hardening có blob SHA khác nhau.
- W13 Sandbox có PC integration handoff và historical attestation: /health PASS trên PID 5188 ngày 2026-10-08; /execute vẫn INCONCLUSIVE/NOT RUN. Không lặp /health cũ.
- DOC-061 W70 đã ghi nhận các gap của :8031: shared token không phải per-agent identity; static Work allow-list; Core grant fallback local; snapshot_only mặc định false; runtime deployment/build/network perimeter chưa xác minh; có nguy cơ false aggregate PASS khi nested test fail.
- **Correction:** W1111 không kết luận thiếu Execution Host source. Chỉ kết luận MCP 8030 không expose process/pytest action; live :8031 và deployed revision/auth chưa xác minh.
