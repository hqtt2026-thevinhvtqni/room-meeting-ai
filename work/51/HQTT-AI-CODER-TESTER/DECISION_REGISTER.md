# WORK51 Decision Register

Quy tắc: mỗi quyết định ghi Options → Choice → Impact. Cột "Vinh approval" = có cần phê duyệt để mở rộng/không (decision trong phạm vi Qc tự quyết theo PLAN §2).

| ID | Quyết định | Options | Choice | Impact | Vinh approval |
|---|---|---|---|---|---|
| D-01 | Wire binding A2A | (a) Official A2A SDK; (b) JSON-RPC 2.0 + text-part tự viết tối thiểu; (c) LangGraph/AutoGen | (b) stdlib-only, mọi wire code gom trong `a2a.py` | Chạy được không cần cài thêm gì; swap sang SDK sau chỉ sửa 1 file; rủi ro lệch spec ở chi tiết (signed card, streaming) — đã ghi trong ARCHITECTURE §6 | Không (đã swap-point) |
| D-02 | BLOCKED mapping | (a) Thêm state `blocked` ngoài spec; (b) BLOCKED = outcome pipeline, task nằm trong state chuẩn | (b) | Không phá A2A task lifecycle; BLOCKED rõ ràng trong RunReport + evidence | Không |
| D-03 | Coder intelligence | (a) Gọi LLM ngay; (b) Deterministic generator + swap-point `_emit` | (b) | Slice xác minh được *protocol + loop*, không phụ thuộc API key; LLM/Qwen cắm sau mà không đổi interface | Không |
| D-04 | Sandbox | (a) Docker/container; (b) subprocess + `python -I` + timeout + tempdir | (b) cho slice | Đủ cho demo/test local; **không an toàn cho untrusted code thật** (network egress chưa chặn) | **CÓ** — trước khi chạy artifact từ nguồn ngoài |
| D-05 | Tách vai trò Coder/Tester | (a) 1 agent 2 mũ; (b) 2 backend + 2 server riêng, session/context riêng | (b) | Đúng charter §5 (Coder không tự phê duyệt); chi phí vận hành thấp vì in-process/HTTP local | Không |
| D-06 | Evidence gate | (a) Tin verdict PASS; (b) PASS chỉ khi có `results` + `artifact_sha256` khớp hash artifact đã giao | (b) | Tester hỏng/âm sửa không thể tạo PASS giả; test `test_pass_without_evidence_is_blocked` lock hành vi | Không |
| D-07 | Kênh làm việc | (a) ROOM-HOP trực tiếp; (b) GitHub branch `work/51-hqtt-coder-tester` | (b) theo PLAN | Qc không truy cập ROOM-HOP; mọi hồ sơ qua Git, evidence JSONL là file xuất kèm | Không |
| D-08 | Task persistence | (a) In-memory store; (b) Persist JSON ngay | (a) cho slice | Restart mất state; P3 "trạng thái sau restart" còn mở — cần layer persist trước khi nối vào Core :8000 | **CÓ** — khi tích hợp ROOM-HOP |
| D-09 | Đồng bộ nhánh Work 51 với `main` | Trước đồng bộ: Work 51 20 commits ahead / 27 behind; so sánh merge-base cho thấy 27 commit riêng của `main` chỉ thêm file trong `10/COMPUTER-AGENT/`, không sửa đường dẫn Work 51; PR #24 báo mergeable clean | **Xu quyết định merge `main` → `work/51-hqtt-coder-tester`** bằng merge commit, không force-push | Đã tích hợp 27 commit của `main` vào nhánh Work 51; `main` không nhận code Work 51. Sau merge, Work 51 ahead 22 / behind 0. Cần CI chạy lại trên merge head; không coi merge là nghiệm thu Work 51. | Không — quyết định vận hành trong phạm vi đã giao Xu |

## Cập nhật iteration 2 (2026-10-23)

| ID | Quyết định | Options | Choice | Impact | Vinh approval |
|---|---|---|---|---|---|
| D-01b | Binding v1.2 | (a) giữ binding tối thiểu như iteration 1; (b) thêm protocolVersion/version/preferredTransport vào Agent Card, contextId + createdAt/updatedAt + status.timestamp vào Task, method tasks/cancel | (b) | Tiệm gần A2A spec hơn mà vẫn stdlib-only, wire code vẫn gom trong a2a.py; signed Agent Card và official SDK vẫn mở (ARCHITECTURE §6) | Không |
| D-04b | Sandbox hardening | (a) container ngay; (b) env scrub + POSIX rlimits + unshare -n (có probe) + cap input 200KB | (b) | Chặn rò secrets, chặn cpu/mem/file/nproc, cách ly network khi khả dụng; KHÔNG coi là đủ cho untrusted code thật — D-04 giữ nguyên cần phê duyệt | CÓ (giữ nguyên — untrusted ngoài) |
| D-08b | Task persistence | (a) in-memory; (b) TaskStore + PersistentTaskStore (JSON, atomic rename, validate khi load) | (b) | Restart-safe — đóng được yêu cầu P3 "trạng thái sau restart" ở tầng store; giới hạn single-writer, flush O(n) | Không |

## Cập nhật iteration 3 (2026-10-23)

| ID | Quyết định | Options | Choice | Impact | Vinh approval |
|---|---|---|---|---|---|
| D-04c | Container-grade sandbox | (a) giữ rlimits/unshare của D-04b là đủ; (b) thêm profile Docker khóa chặt (network none, Docker default seccomp profile bằng cách không override, cap-drop ALL, read-only, memory/cpu/pids caps) làm tầng tùy chọn | (b) | Đóng khoảng cách container/seccomp cho untrusted code: mạng bị chặn trong container; resource caps do cgroup cưỡng chế; CI run `39948132321` xác nhận 4 test container. Profile được chọn khi Docker khả dụng và fallback Sandbox nếu không; còn mở: custom seccomp whitelist, pin image digest, independent security review | Xu — theo ưu tiên đã công bố sau D-09 |
