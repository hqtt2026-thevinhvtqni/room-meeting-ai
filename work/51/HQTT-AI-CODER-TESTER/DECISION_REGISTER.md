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
| D-09 | Nhánh bị lệch | So sánh mới nhất: `work/51-hqtt-coder-tester` diverged — **8 commits ahead, 27 commits behind `main`** | Không tự rebase/merge; giữ nhánh làm việc riêng | Rebase/merge sẽ xử lý lịch sử nhánh chung và có thể tạo xung đột với 27 commit mới trên main. Chưa có quyết định tích hợp; main không bị sửa. | **CÓ** |
