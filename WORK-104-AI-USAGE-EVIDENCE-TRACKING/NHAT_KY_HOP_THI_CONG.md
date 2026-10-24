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

## 2026-10-24 (UTC+7) — Vibe (agent hỗ trợ, ủy quyền tự chủ của Vinh)
- Mã việc: W104-G1-007REV3 (sửa 3 điểm chưa nhất quán theo thẩm định vòng 2 của Xu).
- Lý do: Xu xác minh REV 2 và chỉ 3 điểm: (a) ghi chú "cost chưa thêm" mâu thuẫn với 4 trường cost đã trong schema; (b) event_id gắn lúc nhận response → mất dấu lần gọi không có response; (c) failures.log cùng hệ thống lưu trữ → không được mặc định bộ đếm vẫn ghi được.
- Hành động: Sửa chính bản G1 (REV 3, không tạo file cạnh tranh): (1) Bỏ ghi chú mâu thuẫn; định nghĩa cost_status 3 giá trị actual/estimated/unavailable với điều kiện rõ ràng từng loại. (2) Vòng đời event mới: khởi tạo event_id lúc BẮT ĐẦU cuộc gọi, kết thúc bằng nhánh có-response hoặc nhánh hết-timeout/không-response (vẫn ghi dòng hoàn chỉnh, status=error, token null); 1 cuộc gọi = đúng 1 dòng; occurred_at ≠ ingested_at làm dấu vết reconciliation phát hiện event treo. (3) Giới hạn bộ đếm: failures.log chỉ best-effort; nếu nó cũng hỏng thì đánh dấu "không đối soát được"; báo cáo G4 hiển thị 3 mức (trong ledger / loss theo counter / loss không xác định); cấm tuyên bố completeness khi còn loss không xác định; thêm bài test G3: hỏng cả 2 path → luồng chính vẫn PASS.
- Kết quả: DONE — REV 3. G1 vẫn PROPOSED CHỜ VINH ACK. Retention 365 ngày là chính sách thiết kế, chưa phải bằng chứng triển khai. G0 vẫn NOT PASS (submodule chưa kiểm kê). Không gate nào PASS.
- Bằng chứng: Commit này trên nhánh work/104-ai-usage-evidence-tracking; diff REV2→REV3 trong file G1 (mục §2 cost, §4 lifecycle, §3 mục 3).
- Bước tiếp: Xu thẩm định lại REV 3 → gửi Vinh ACK; song song kiểm kê submodule room-meeting-ai/ (SHA eeb497e9); sau ACK mới #8 (Co).

## 2026-10-24 (UTC+7) — Vibe (agent hỗ trợ, ủy quyền tự chủ của Vinh)
- Mã việc: W104-G1-007REV4 (khép 3 lỗ hổng thẩm định vòng 3 của Xu).
- Lý do: Xu xác nhận REV 3 xử lý đúng 3 điểm cũ nhưng phát hiện 3 lỗ hổng mới: (A) event khởi tạo trong bộ nhớ → crash giữa 2 thời điểm làm mất dấu, occurred_at≠ingested_at không tự phát hiện event treo; (B) §2 cho phép estimated nhưng §5 cấm cost_amount khi chưa verified; (C) stderr không được thu thập vào nguồn truy vấn + test kép chưa có mục riêng trong §7.
- Hành động: Sửa chính bản G1 (REV 4): (A) chọn phương án GIỚI HẠN TUYÊN BÁO — "1 cuộc gọi = 1 dòng" chỉ đúng khi tiến trình sống đến lúc ghi; crash trước ghi = mất-không-dấu-vết được chấp nhận ở v1; ghi rõ occurred/ingested chỉ là dấu vết trên event đã ghi; mở đầu việc #7c "crash-detection decision" (start-marker bền vững hoặc đối soát billing provider) chỉ làm khi có phê duyệt; báo cáo reconciliation bắt buộc ghi giới hạn. (B) Khớp quy tắc giá thành 3 nhánh duy nhất: verified→actual, unverified→estimated (kèm pricing_version), không match→unavailable/null; bỏ câu "cost_amount CHỈ khi verified" mâu thuẫn. (C) Khai báo thẳng: v1 KHÔNG có cơ chế thu thập stderr vào nguồn truy vấn được — khi cả 2 path hỏng, G4 báo cáo mất bằng khoảng thời gian + phạm vi, KHÔNG bằng số đếm; đối soát service journal bên ngoài là việc thủ công của người vận hành. (D) Thêm test #7 (kép, từ §3d) và test #8 (crash-limit — xác minh tuyên bố giới hạn bằng bằng chứng) vào test plan §7. (E) Hợp nhất dòng #7 Kế hoạch: bỏ chữ "REV 2" cũ trong ô bằng chứng, một trạng thái duy nhất REV 4.
- Kết quả: DONE — REV 4. G1 vẫn PROPOSED CHỜ XU THẨM ĐỊNH LẦN CUỐI rồi Vinh ACK. G0 vẫn NOT PASS (submodule chưa kiểm kê). Không gate nào PASS.
- Bằng chứng: Commit này trên nhánh work/104-ai-usage-evidence-tracking; diff REV3→REV4 (§4 giới hạn, §5 quy tắc 3 nhánh, §3 mục b-c stderr, §7 test 7-8, Kế hoạch dòng #7).
- Bước tiếp: Xu thẩm định lần cuối REV 4 → gửi Vinh ACK; song song: kiểm kê submodule room-meeting-ai/ (SHA eeb497e9), quyết định #7c.

## 2026-10-24 (UTC+7) — Vibe (agent hỗ trợ, ủy quyền tự chủ của Vinh)
- Mã việc: W104-G1-007REV5 (khép điểm cuối theo thẩm định vòng cuối của Xu) + W104-G0-SUBPROBE (thăm dò submodule).
- Lý do: Xu duyệt nội dung chính REV 4, chỉ còn 1 điểm: nguồn nào xác định "khoảng thời gian và phạm vi mất" khi cả ledger lẫn failures.log đều hỏng — hệ thống không tự phát hiện được, không được suy đoán.
- Hành động: (1) Sửa §3 mục d (REV 5): khoảng mất PHẢI do người vận hành xác nhận/cung cấp kèm nguồn cung cấp; không có căn cứ → ghi thẳng "KHÔNG xác định được thời gian và phạm vi thất thoát"; cấm suy ra thời gian/số lượng/phạm vi từ việc chỉ biết 2 path hỏng; đối soát journal ngoài là đầu vào thủ công, không phải output tự động. (2) Thăm dò đầu việc kiểm kê submodule: truy vấn Git tree qua GitHub API xác nhận gitlink room-meeting-ai (SHA eeb497e906b6b65e625a7ba7c50d93ada6ada9cfc) — và phát hiện repo KHÔNG có file .gitmodules → đây là ORPHANED GITLINK, không phân giải được URL submodule từ repo chính. Kiểm kê submodule BLOCKED chờ Vinh cung cấp URL nguồn (hoặc quyết định gỡ gitlink nếu là commit lỗi thời đẩy nhánh).
- Kết quả: DONE — REV 5 (khép điểm cuối). G1 PROPOSED REV 5 — đủ điều kiện Xu đọc lại bản cuối và trình Vinh ACK. G0 vẫn NOT PASS; kiểm kê submodule BLOCKED vì orphaned gitlink.
- Bằng chứng: Commit này trên nhánh work/104 (diff §3d); truy vấn API Git tree trả {type: submodule, sha eeb497e9...} và .gitmodules 404.
- Bước tiếp: Xu đọc lại REV 5 → trình Vinh ACK (kèm 2 quyết định Xu đã đề xuất: #7c giữ mở chưa triển khai; kiểm kê submodule trước #8 — nhưng cần Vinh cho URL vì orphaned gitlink). Sau ACK: #8 G2 Implementation (Co).

## 2026-10-24 (UTC+7) — Vibe (agent hỗ trợ, ghi thay vì Xu vì thao tác ghi của Xu bị chặn)
- Mã việc: W104-G1-007FINAL (chuẩn hóa nhãn §3 + ghi nhận ACK).
- Lý do: Xu xác nhận nội dung chính REV 4/5 đạt; Vinh ACK CÓ ĐIỀU KIỆN với 3 điều kiện: (1) chuẩn hóa nhãn §3 bị lặp; (2) #7c giữ mở, chưa triển khai; (3) gitlink room-meeting-ai/ giữ nguyên, chưa có URL nguồn nên kiểm kê tiếp tục BLOCKED, không tự gỡ. Xu không đẩy được commit (thao tác ghi bị chặn) nên Vibe ghi thay theo ủy quyền của Vinh.
- Hành động: (1) Chuẩn hóa §3: hai mục cuối trùng nhãn c./d. đổi thành e./f., mục test kép tham chiếu mục #7 trong test plan §7 — nội dung kỹ thuật KHÔNG đổi từ REV 5. Nâng bản thành REV 6 (FINAL). (2) Ghi nhận ACK có điều kiện của Vinh vào header G1, Kế hoạch #7 và PROJECT_STATE.
- Kết quả: DECISION — G1 Design REV 6 (FINAL) ACKED bởi Vinh 2026-10-24 (ACK có điều kiện, điều kiện chuẩn hóa đã hoàn tất trong cùng commit). KHÔNG tự nâng bất kỳ gate nào: G0 vẫn NOT PASS; G2 chưa bắt đầu.
- Bằng chứng: Commit này trên nhánh work/104 (diff nhãn §3 + header ACK); ACK phát biểu bởi Vinh trong phiên Vibe ngày 2026-10-24, Xu đã xác nhận điều kiện trước đó.
- Bước tiếp: #8 G2 Implementation (Co): viết core/usage_ledger.py + instrumentation 6 discard points theo REV 6. Lưu ý điều kiện §8: G3 Verification cần môi trường test ủy quyền (chưa có) và model thật ở agents/*.yaml cho usage thật; code G2 có thể bắt đầu nhưng KHÔNG khai PASS khi chưa test được. Kiểm kê submodule tiếp tục BLOCKED chờ Vinh cung cấp URL.


## 2026-10-24 (UTC+7) — Xu (AI-01 GPT CEO / điều phối G2)

- Mã việc: W104-G2-008-START.
- Chỉ thị: Vinh ra lệnh “bắt đầu G2”; phạm vi theo G1 REV 6, không triển khai #7c, không đổi gitlink, không khai PASS khi thiếu bằng chứng.
- Truy cập: MCP 8030 trả lỗi kết nối trong phiên này; chuyển sang GitHub connector và chỉ ghi trên nhánh `work/104-ai-usage-evidence-tracking`.
- Hành động: tạo `core/usage_ledger.py` + `tests/test_usage_ledger.py`; tích hợp usage vào `core/connectors.py` (Anthropic/OpenAI), `core/intent_router.py` (Claude), `core/llama_intent_router.py` (Groq), `core/gemini_intent_router.py` (Gemini), và `llama_chat_v2.py` (hai lần gọi Groq trong đường chat dùng chung client).
- Evidence: `06_EVIDENCE/G2_IMPLEMENTATION_PROGRESS_20261024.md` (danh sách commit và giới hạn).
- Kết quả: code được ghi lên nhánh; **G2 IN PROGRESS / NOT PASS**. Unit tests và regression tests chưa chạy trong môi trường ủy quyền; không có provider call thật nào được chạy.
- Blocker/giới hạn: model rỗng ở `agents/xu.yaml` và `agents/claude.yaml`; môi trường test ủy quyền chưa xác định/khả dụng; G0 vẫn NOT PASS do gitlink chưa kiểm kê; pricing #7b chưa triển khai.
- Ranh giới: #7c giữ OPEN, chưa triển khai; gitlink `room-meeting-ai/` giữ nguyên; Work 102 không đổi.
- Bước tiếp: kiểm tra cú pháp + unit/regression tests trong môi trường ủy quyền, sửa lỗi dựa trên kết quả thật, rồi giao Ka review độc lập trước khi xét G3. Không tuyên bố PASS trước khi có test report.


## 2026-10-24 (UTC+7) — Xu (AI-01 GPT CEO / điều phối G2, cập nhật)

- Mã việc: W104-G2-008-UPDATE.
- Hành động: bổ sung ghi event `usage_source=unavailable` cho Mock/Internal connector theo G1 §3; thu hẹp failure counter để chỉ đếm lỗi append ledger (lỗi index/rotation chỉ stderr, không ghi thành loss event); cập nhật evidence.
- Kiểm tra hồ sơ: phát hiện tiêu đề G1 REV 6 còn chữ “PROPOSED, chờ Vinh ACK” dù nội dung đã ghi ACKED; sửa tiêu đề và §8 để thống nhất, vẫn giữ điều kiện môi trường test ủy quyền.
- Bằng chứng: `06_EVIDENCE/G2_IMPLEMENTATION_PROGRESS_20261024.md`; commit `3ff659047831cbde8444536854b6fdfb3745d684`, `df7d40ddeba08f0ea9b2b35b17082e89e19d4540`, `ebad679a08bbc1fc7339f2429fd172b5b6c7c3bc`.
- Trạng thái: G2 IN PROGRESS / NOT PASS; tests chưa chạy. #7c OPEN; gitlink giữ nguyên; G0 NOT PASS.


## 2026-10-24 (UTC+7) — Xu (AI-01 GPT CEO / G2 code review pass, chưa phải nghiệm thu)

- Mã việc: W104-G2-008-QUALITY-FIX.
- Hành động: bổ sung xử lý nested SDK usage objects (cache/reasoning token details) và unit-test tương ứng; ghi lại commit vào evidence.
- Bằng chứng: commit module `e8efbcc15ca5f696107cf165ca8455eb13ddc4f5`, test `9891647f0ea3978d7296720579a2aed560563e41`, evidence file G2.
- Kết quả: code đã cập nhật; chưa chạy test. G2 vẫn IN PROGRESS / NOT PASS.


## 2026-10-24 (UTC+7) — Xu (AI-01 GPT CEO / hồ sơ trạng thái G2)

- Mã việc: W104-G2-008-DOC-CONSISTENCY.
- Hành động: đồng bộ trạng thái đầu kế hoạch từ INITIALIZATION sang IMPLEMENTATION; sửa câu mô tả đường dẫn mặc định của ledger để thống nhất quy tắc xoay vòng theo tháng ở §5b G1.
- Bằng chứng: commit kế hoạch `8261e838a71bd8900aa552b898d999aefe201c6c`, G1 design `421dfb936792cf4ea349381169d2652a31ad42c6`, cập nhật trong G2 evidence.
- Trạng thái gate không đổi: G0 NOT PASS; G1 ACKED; G2 IN PROGRESS / NOT PASS; G3 chưa bắt đầu.
