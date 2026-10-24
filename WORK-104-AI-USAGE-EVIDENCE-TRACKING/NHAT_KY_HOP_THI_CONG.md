# NHAT_KY_HOP_THI_CONG.md — Work 104: AI Usage & Evidence Tracking

- Nhật ký chung, một dòng thời gian liên tục từ khởi động đến bàn giao (AGENTS.md §06.2).
- Mọi AI (kể cả Co, Xu) ghi nối tiếp vào file này. Không tạo nhật ký riêng theo cá nhân/phiên.
- Ghi ngày giờ theo múi giờ Việt Nam (UTC+07:00).

---

## 2026-10-24 (UTC+7) — Xu (AI-01 GPT CEO / điều phối)
- Mã việc: W104-INIT.
- Hành động: Khởi tạo Work 104 trên ROOM-HOP Sandbox qua MCP 8030; tạo nhánh GitHub `work/104-ai-usage-evidence-tracking`; đồng bộ tài liệu gốc (manifest, request/scope, architecture, acceptance plan).
- Kết quả: Nhánh + tài liệu tồn tại. Trạng thái: DONE (khởi tạo), KHÔNG phải PASS triển khai.
- Quyết định: Tận dụng ROOM-HOP hiện có; khảo sát trước khi chọn proxy/database/dashboard; Core :8000 ngoài Sandbox; số liệu thiếu ghi `unavailable`.
- Bằng chứng: 00_ROOT/WORK_MANIFEST.md; 01_ORIGINAL/REQUEST_AND_SCOPE.md; 03_ARCHITECTURE/AI_USAGE_EVIDENCE_ARCHITECTURE.md; 05_TEST/ACCEPTANCE_AND_E2E_PLAN.md; commit lịch sử nhánh.
- (Mục gốc: 06_EVIDENCE/JOURNAL_THI_CONG_20261024.md — SUPERSEDED, đã hợp nhất vào đây.)

## 2026-10-24 (UTC+7) — Vibe (agent hỗ trợ, theo ủy quyền tự chủ của Vinh)
- Mã việc: W104-GOV-001.
- Lý do: Đánh giá nhánh Work 104 phát hiện: (a) Work 104 chưa có 3 hồ sơ điều hành chuẩn theo AGENTS.md §06; (b) context/PROJECT_STATE.md (Truth Table) chưa phản ánh Work 104; (c) 00_ROOT/README chưa dẫn đọc 3 hồ sơ điều hành; (d) cây repo gốc có thư mục rác tmp/trash/agent_test.
- Hành động: Tạo BIEN_BAN.md, KE_HOACH_THI_CONG_XU.md, NHAT_KY_HOP_THI_CONG.md tại thư mục gốc Work 104; hợp nhất nội dung JOURNAL_THI_CONG_20261024.md vào đây và đánh dấu file cũ SUPERSEDED (không xóa bằng chứng); cập nhật PROJECT_STATE.md thêm mục Work 104; cập nhật 00_ROOT/README.md thứ tự đọc; ghi quyết định dọn repo làm đầu việc #12 chờ Vinh/Xu phê duyệt (Evidence First: không tự xóa).
- Kết quả: Hồ sơ điều hành chuẩn hóa. Trạng thái: DONE — hồ sơ; PHẠM VI KHÔNG TỰ KHAI BÁO PASS cho bất kỳ gate G nào.
- Bằng chứng: Commit tạo 3 hồ sơ + cập nhật PROJECT_STATE.md/README trên nhánh `work/104-ai-usage-evidence-tracking`; diff so với commit trước (ad84291).
- Người phụ trách bước tiếp theo: Cla/C — thi công G0 Discovery (#5 trong KE_HOACH_THI_CONG_XU.md).

## 2026-10-24 (UTC+7) — Vibe (agent hỗ trợ, ủy quyền tự chủ của Vinh "hoàn thiện không chờ không hỏi")
- Mã việc: W104-G0-005 (+ W104-CLEAN-012 một phần).
- Lý do: Kế hoạch chỉ định bước tiếp theo là thi công #5 G0 Discovery; Vinh ủy quyền hoàn thiện tự chủ.
- Hành động: (1) Đọc trực tiếp code trên nhánh work/104 (commit c750ad6f): core/connectors.py, core/intent_router refs, core/llama_intent_router.py, core/gemini_intent_router.py, core/groq_config.py, agents/*.yaml, room_hop_mcp/adapter/server.py, execution_host/server.py. (2) Lập bản ghi G0 Discovery: 06_EVIDENCE/G0_DISCOVERY_INVENTORY_20261024.md — 7 đường invocation, 6 usage-discard points, kiến nghị integration point nhỏ nhất (module usage_ledger tại các discard point, không cần proxy). (3) Xóa 3 file desktop.ini rác Windows (tmp/, core/, agents/) theo ủy quyền của Vinh — giữ nguyên toàn bộ trash/ là bằng chứng đã cách ly. (4) Cập nhật KE_HOACH #5, #12 và PROJECT_STATE.
- Kết quả: Discovery record tồn tại. Trạng thái: DONE — bản ghi; KHÔNG tự khai PASS gate G0 (chờ Cla/Xu phê duyệt #6).
- Bằng chứng: 06_EVIDENCE/G0_DISCOVERY_INVENTORY_20261024.md; commit này trên nhánh work/104-ai-usage-evidence-tracking.
- Người phụ trách bước tiếp theo: Cla/Xu — phê duyệt G0 + quyết định integration point (#6), rồi #7 G1 Design approve → Vinh ACK.


## 2026-10-24 (UTC+7) — Xu (AI-01 GPT CEO / điều phối kiến trúc)
- Mã việc: W104-G0-006.
- Hành động: Đọc trực tiếp G0 inventory, kế hoạch, nhật ký và PROJECT_STATE trên nhánh work/104; ghi quyết định chọn hướng in-process `core/usage_ledger.py` + append-only JSONL cho G1 design, chưa dùng proxy.
- Căn cứ: 06_EVIDENCE/G0_DISCOVERY_INVENTORY_20261024.md; decision record 01_ORIGINAL/DECISION_G0_INTEGRATION_POINT_20261024.md.
- Kết quả: DONE — quyết định hướng kiến trúc cho G1. Không phải PASS triển khai và không đóng G0.
- Giới hạn/blocker: discovery mới là static-only; còn invocation paths chưa khảo sát; usage thật bị chặn với xu.yaml/claude.yaml nếu model rỗng; Work 102 vẫn NOT PASS/NOT RELEASED.
- Bước tiếp: G1 design hoàn chỉnh và chờ Vinh ACK; mở rộng inventory trước khi tuyên bố coverage toàn hệ thống.

## 2026-10-24 (UTC+7) — Vibe (agent hỗ trợ, ủy quyền tự chủ của Vinh)
- Mã việc: W104-G0-005B (mở rộng discovery) + W104-G1-007DRAFT (soạn thảo G1 design).
- Lý do: Decision W104-G0-006 yêu cầu mở rộng inventory trước khi tuyên bố coverage; Kế hoạch bước tiếp theo là #7 G1 Design chờ ACK.
- Hành động: (1) Đọc trực tiếp integration/room_hop_integration.py, 10/COMPUTER-AGENT/04_CODE (4 file), 30/README.md, research/RC005-007, core/secretary.py, docs/secretary_log.jsonl, docs/schemas/principals/wee/context listing. (2) Ghi bản mở rộng: 06_EVIDENCE/G0_DISCOVERY_INVENTORY_EXPANSION_20261024.md — không thêm provider path mới (vẫn 7); 3 tool-activity paths (:8030/:8031/:8787); 2 đính chính: Integration yêu cầu 5 tool MCP (adapter static chỉ thấy 4), room-meeting-ai/ ở gốc là GIT SUBMODULE chưa kiểm kê. (3) Soạn thảo 03_ARCHITECTURE/G1_DESIGN_USAGE_LEDGER_20261024.md: envelope schema v1, extraction map 4 provider, idempotency, fail-safe, redaction, test plan G3, pricing provenance để sau.
- Kết quả: DONE — bản ghi + bản thảo thiết kế. KHÔNG khai PASS G0 (submodule chưa kiểm kê) và KHÔNG tự coi G1 đã approve.
- Bằng chứng: 2 file mới trong 06_EVIDENCE và 03_ARCHITECTURE; commit này; docs/secretary_log.jsonl (chứng cứ 429 Groq 2026-08-15 xác nhận P5 chạy thật).
- Blocker: (a) submodule room-meeting-ai/ (SHA eeb497e9) chưa kiểm kê — G0 chưa thể PASS coverage toàn hệ thống; (b) runtime verify 5 tool MCP cần môi trường ủy quyền; (c) chờ Vinh ACK G1 trước implementation.
- Bước tiếp: Vinh ACK/chỉnh G1 design; kiểm kê submodule; sau đó #8 G2 Implementation (Co).

## 2026-10-24 (UTC+7) — Vibe (agent hỗ trợ, ủy quyền tự chủ của Vinh)
- Mã việc: W104-G1-007REV2 (chỉnh G1 theo 5 điểm thẩm định của Xu).
- Lý do: Xu kết luận G1 "cần bổ sung" 5 mục: retention, cấu trúc pricing provenance, correlation, usage theo giai đoạn lỗi, trạng thái verify MCP 5 tool.
- Hành động: Sửa CHÍNH BẢN 03_ARCHITECTURE/G1_DESIGN_USAGE_LEDGER_20261024.md lên REV 2 (không tạo file cạnh tranh): (1) §5b Retention — xoay vòng theo tháng + ngưỡng 20MB, lưu tối thiểu 365 ngày, xóa chỉ khi Vinh phê duyệt, index JSONL kèm sha256 đầu-cuối cho reconciliation; (2) §5 — chốt cấu trúc pricing_provenance.json + 4 trường cost đưa vào envelope schema v1 ngay (điền giá là #7b, không phá schema sau); (3) §4.2 Correlation — chỉ điền mã có sẵn từ caller, cấm sinh mã giả, attempt_id/parent_event_id cho retry; (4) §3 — 3 giai đoạn lỗi tách rõ: lỗi trước phản hồi (token null), lỗi có usage (trích đúng), lỗi ghi ledger (counter failures.log + đối chiếu G4); (5) §7b — ghi rõ mâu thuẫn 4-vs-5 tool MỚI là static, KHÔNG kết luận tương thích trước runtime check.
- Kết quả: DONE — bản REV 2. G1 vẫn PROPOSED, CHỜ VINH ACK. G0 vẫn NOT PASS (submodule chưa kiểm kê). Không gate nào PASS.
- Bằng chứng: Commit này trên nhánh work/104-ai-usage-evidence-tracking; diff REV1→REV2 trong file G1.
- Bước tiếp: Vinh ACK G1 REV 2 (hoặc yêu cầu chỉnh tiếp); song song: kiểm kê submodule room-meeting-ai/ (SHA eeb497e9); sau ACK mới bắt đầu #8 (Co).
