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
- Work 104 — AI Usage & Evidence Tracking (nhánh `work/104-ai-usage-evidence-tracking`): 🟡 ACTIVE — G0 DISCOVERY RECORDED 2026-10-24 (06_EVIDENCE/G0_DISCOVERY_INVENTORY_20261024.md: 7 invocation paths, 6 usage-discard points; kiến nghị integration point = usage_ledger module, không proxy). Bản ghi discovery RECORDED; Xu đã ghi quyết định #6 chọn hướng in-process core/usage_ledger.py + JSONL cho G1 design (01_ORIGINAL/DECISION_G0_INTEGRATION_POINT_20261024.md). Discovery đã mở rộng 2026-10-24 (G0_DISCOVERY_INVENTORY_EXPANSION: không thêm provider path — vẫn 7; 3 tool-activity paths :8030/:8031/:8787; 2 errata: MCP client yêu cầu 5 tool, room-meeting-ai/ gốc là GIT SUBMODULE chưa kiểm kê → G0 vẫn NOT PASS). G1 Design **REV 6 (FINAL, ACKED)** 2026-10-24: Vinh ACK có điều kiện — điều kiện chuẩn hóa nhãn §3 (xong trong REV 6, nội dung kỹ thuật giữ nguyên REV 5), #7c giữ mở chưa triển khai, gitlink giữ nguyên. File: 03_ARCHITECTURE/G1_DESIGN_USAGE_LEDGER_20261024.md. **G1 gate: PASS theo tiêu chí #7 (design approved) — evidence: ACK của Vinh 2026-10-24 qua Vibe + commit REV 6.** G2 #8 IN PROGRESS: code ban đầu đã ghi trên nhánh theo REV 6; evidence: WORK-104-AI-USAGE-EVIDENCE-TRACKING/06_EVIDENCE/G2_IMPLEMENTATION_PROGRESS_20261024.md. Unit/regression tests CHƯA CHẠY trong môi trường ủy quyền, nên G2 NOT PASS; G3 Verification chưa bắt đầu và còn chờ môi trường test ủy quyền + model thật ở agents/*.yaml. Kiểm kê submodule tiếp tục BLOCKED (orphaned gitlink, chờ URL từ Vinh). Không gate nào khác PASS.

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
- Work 104: #6 DECISION đã ghi; discovery đã mở rộng (submodule room-meeting-ai/ SHA eeb497e9 CHƯA kiểm kê — đầu việc mới). #7 G1 REV 6 ACKED (Vinh, có điều kiện — xong). #8 G2 Implementation đang IN PROGRESS theo lệnh Vinh; code candidate và evidence được ghi trong G2_IMPLEMENTATION_PROGRESS_20261024.md. Chưa có test result, KHÔNG khai PASS; cần môi trường test ủy quyền trước khi xác nhận G2/G3. #7b điền giá sau G3; #7c giữ mở. Submodule room-meeting-ai/ (SHA eeb497e9) tiếp tục BLOCKED: orphaned gitlink, không .gitmodules — chờ Vinh cung cấp URL nguồn (quyết định: giữ nguyên gitlink). Blocker khác: model rỗng ở xu.yaml/claude.yaml; môi trường test ủy quyền chưa có. Blocker: submodule room-meeting-ai/ (SHA eeb497e9) chưa kiểm kê (G0 NOT PASS coverage); agents/xu.yaml và claude.yaml còn model rỗng → chưa có usage thật từ P1/P2; môi trường test ủy quyền chưa có.
- Work 102: đóng blocker pytest/review/Gate A trước khi mở rộng mặt bằng.

### GOVERNANCE PRINCIPLE (Xu phát hiện - thêm vào AGENTS.md)
Agent autonomy ≠ unlimited authority
- Agent có quyền tự quyết: REPLY / PASS / FINAL
- NHƯNG Room có authority cao hơn để: giới hạn vòng, chặn loop, kết thúc room, bảo vệ hệ thống

### IMMUTABILITY RULE
MEETING-2026-002 là CLOSED - KHÔNG được sửa khi API thật chạy.
API thật phải tạo MEETING-2026-003 mới -> Evidence mới -> PROJECT_STATE update.

MeAgent integrated - ready for MEETING-2026-003
