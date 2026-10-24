# PROJECT_STATE.md - ROOM HOP Truth Table
# READ ONLY cho Agent - Chỉ Xu + Quản Gia được update

## PROJECT: ROOM HOP
## CURRENT VERSION: v0.2

### VERIFIED STATUS TREE (Không được ghi gọn là PASS)
ROOM HOP v0.2
├── Discussion Engine: 🟢 PASS (Evidence: MEETING-2026-002)
├── REPLY / PASS / FINAL: 🟢 PASS (3 nhánh đã test)
├── Room Stop Guard: 🟢 PASS (An toàn cần thiết, không phải giới hạn tùy tiện)
├── MockConnector: 🟢 PASS (4 rounds -> FINAL)
└── Real API Connector: 🟡 PENDING VERIFICATION

### TỔNG KẾT
- Mechanism: 🟢 PASS
- Integration Real API: 🟡 PENDING
- v0.2 Hoàn tất toàn bộ: 🔴 CHƯA

### ACTIVE WORKS (cập nhật 2026-10-24, theo AGENTS.md §06)
- Work 102 — AI Agent Loop Production Readiness (nhánh `work/102-ai-agent-loop-production-readiness`): 🔴 ACTIVE / NOT PASS / NOT RELEASED. Blocker: môi trường pytest ủy quyền, review độc lập của Ka theo hash candidate, Gate A (Core task authority, dispatch/ACK, leases/fencing, W14 Host binding).
- Work 104 — AI Usage & Evidence Tracking (nhánh `work/104-ai-usage-evidence-tracking`): 🟡 ACTIVE — G0 DISCOVERY RECORDED 2026-10-24 (06_EVIDENCE/G0_DISCOVERY_INVENTORY_20261024.md: 7 invocation paths, 6 usage-discard points; kiến nghị integration point = usage_ledger module, không proxy). Bản ghi discovery RECORDED; Xu đã ghi quyết định #6 chọn hướng in-process core/usage_ledger.py + JSONL cho G1 design (01_ORIGINAL/DECISION_G0_INTEGRATION_POINT_20261024.md). Discovery đã mở rộng 2026-10-24 (G0_DISCOVERY_INVENTORY_EXPANSION: không thêm provider path — vẫn 7; 3 tool-activity paths :8030/:8031/:8787; 2 errata: MCP client yêu cầu 5 tool, room-meeting-ai/ gốc là GIT SUBMODULE chưa kiểm kê → G0 vẫn NOT PASS). G1 Design **REV 5** 2026-10-24 — Xu thẩm định vòng cuối duyệt nội dung chính REV 4; REV 5 khép điểm cuối (§3d: khoảng thời gian mất khi cả 2 path hỏng PHẢI do người vận hành cung cấp/xác nhận kèm nguồn; không căn cứ → "KHÔNG xác định được"; cấm suy đoán): 03_ARCHITECTURE/G1_DESIGN_USAGE_LEDGER_20261024.md (PROPOSED REV 5 — CHỜ XU ĐỌC BẢN CUỐI → TRÌNH VINH ACK; điền giá #7b; #7c giữ mở chưa triển khai). Chưa có implementation/test evidence. Không gate nào PASS.

### LAST VERIFIED EVENT
MEETING-2026-002 - 2026-08-14 - CLOSED / IMMUTABLE
- Participants: xu, claude
- Context: XU_CORE.md, XU_SESSION.md, PROJECT_STATE.md
- Decision: v0.2 PASS về mặt cơ chế, chờ xác nhận với API thật
- Final: meetings/MEETING-2026-002/final.md

### PENDING ACTION
- Vinh gắn API key thật và chạy MEETING-2026-003 để verify Real API
  - Nếu PASS -> v0.2 = FULL PASS
  - Nếu FAIL -> v0.2 vẫn = MECHANISM PASS, ghi BLOCKED
- Work 104: #6 DECISION đã ghi; discovery đã mở rộng (submodule room-meeting-ai/ SHA eeb497e9 CHƯA kiểm kê — đầu việc mới). #7 G1 Design REV 5 CHỜ Xu đọc bản cuối → trình Vinh ACK trước implementation #8; #7b điền giá sau G3; #7c giữ mở chưa triển khai. Kiểm kê submodule room-meeting-ai/ (SHA eeb497e9) BLOCKED 2026-10-24: phát hiện ORPHANED GITLINK — repo không có .gitmodules nên không phân giải được URL; chờ Vinh cung cấp URL nguồn hoặc quyết định gỡ gitlink. Blocker khác: model rỗng ở xu.yaml/claude.yaml; môi trường test ủy quyền chưa có. Blocker: submodule room-meeting-ai/ (SHA eeb497e9) chưa kiểm kê (G0 NOT PASS coverage); agents/xu.yaml và claude.yaml còn model rỗng → chưa có usage thật từ P1/P2; môi trường test ủy quyền chưa có.
- Work 102: đóng blocker pytest/review/Gate A trước khi mở rộng mặt bằng.

### GOVERNANCE PRINCIPLE (Xu phát hiện - thêm vào AGENTS.md)
Agent autonomy ≠ unlimited authority
- Agent có quyền tự quyết: REPLY / PASS / FINAL
- NHƯNG Room có authority cao hơn để: giới hạn vòng, chặn loop, kết thúc room, bảo vệ hệ thống

### IMMUTABILITY RULE
MEETING-2026-002 là CLOSED - KHÔNG được sửa khi API thật chạy.
API thật phải tạo MEETING-2026-003 mới -> Evidence mới -> PROJECT_STATE update.

MeAgent integrated - ready for MEETING-2026-003
