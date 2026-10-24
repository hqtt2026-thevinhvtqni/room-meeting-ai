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
- Work 104 — AI Usage & Evidence Tracking (nhánh `work/104-ai-usage-evidence-tracking`): 🟡 ACTIVE — G0 DISCOVERY RECORDED 2026-10-24 (06_EVIDENCE/G0_DISCOVERY_INVENTORY_20261024.md: 7 invocation paths, 6 usage-discard points; kiến nghị integration point = usage_ledger module, không proxy). Bản ghi discovery RECORDED; Xu đã ghi quyết định #6 chọn hướng in-process core/usage_ledger.py + JSONL cho G1 design (01_ORIGINAL/DECISION_G0_INTEGRATION_POINT_20261024.md). G0 vẫn NOT PASS vì inventory static-only/chưa bao phủ toàn bộ invocation paths. Tiếp theo #7 G1 Design → Vinh ACK; chưa có implementation/test evidence. Không gate nào PASS.

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
- Work 104: #6 DECISION đã ghi — hướng kiến trúc được chọn cho G1 design, không phải G0 PASS. Tiếp theo #7 G1 Design → Vinh ACK; mở rộng inventory các invocation paths chưa khảo sát. Blocker: agents/xu.yaml và claude.yaml còn model rỗng → chưa có usage thật từ P1/P2.
- Work 102: đóng blocker pytest/review/Gate A trước khi mở rộng mặt bằng.

### GOVERNANCE PRINCIPLE (Xu phát hiện - thêm vào AGENTS.md)
Agent autonomy ≠ unlimited authority
- Agent có quyền tự quyết: REPLY / PASS / FINAL
- NHƯNG Room có authority cao hơn để: giới hạn vòng, chặn loop, kết thúc room, bảo vệ hệ thống

### IMMUTABILITY RULE
MEETING-2026-002 là CLOSED - KHÔNG được sửa khi API thật chạy.
API thật phải tạo MEETING-2026-003 mới -> Evidence mới -> PROJECT_STATE update.

MeAgent integrated - ready for MEETING-2026-003
