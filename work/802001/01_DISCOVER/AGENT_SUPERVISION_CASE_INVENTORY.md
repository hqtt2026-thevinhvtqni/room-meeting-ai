# DISCOVER — INVENTORY TÌNH HUỐNG GIÁM SÁT AGENT
## Agent Work Supervision Case Inventory

- Work: 802001
- Version: 0.1 — historical evidence extraction
- Date: 2026-11-17
- Governing standard: Work 70
- Phase: DISCOVER
- Status: INITIAL BASELINE — NEEDS REVIEW
- Scope: Rút tình huống thực tế từ hồ sơ thi công Work 802001; chưa kết luận mọi trường hợp là lỗi của Agent.

## 1. Quy tắc đọc bằng chứng
- VERIFIED-IN-RECORD: nội dung có ghi trực tiếp trong hồ sơ lịch sử được liệt kê.
- REPORTED-IN-TRANSCRIPT: kết luận hoặc diễn biến do người/Agent ghi trong transcript, chưa tái chạy độc lập.
- INFERENCE: bài học giám sát rút ra từ hồ sơ; cần DEFINE/reviewer xác nhận trước khi biến thành policy.
- NOT-OBSERVED: chưa có bằng chứng trực tiếp, không được đưa thành finding.

Các hồ sơ cũ chủ yếu phản ánh một dự án kỹ thuật E2E. Vì vậy, chúng cung cấp tình huống điều phối/kiểm chứng có thật trong quá trình thi công, nhưng chưa đủ để khẳng định đã quan sát đầy đủ mọi dạng hành vi Agent trong nhiều Work.

## 2. Case inventory

| Case | Tình huống được ghi nhận | Nguồn lịch sử | Bằng chứng | Tác động/rủi ro | Hướng giám sát cần có |
|---|---|---|---|---|---|
| C-01 | Plumbing/test PASS nhưng Real LLM hoặc Real Ka còn BLOCKED; dễ đánh đồng kiểm thử mô phỏng với acceptance thật | 03_ARCHITECTURE/REPORT_802001_PHASE2.md; 04_CODE/CODE_ANALYSIS.md; 05_TEST/TEST_ANALYSIS.md; AUTO-WARE/05_DECISION.md | VERIFIED-IN-RECORD | Báo cáo tiến độ vượt quá mức bằng chứng; quyết định sai về readiness | Bắt Agent tách PASS theo từng lớp; yêu cầu artefact/runtime evidence cho từng claim; không cho nâng trạng thái từ MOCK sang REAL |
| C-02 | System Wake (tạo PENDING task) bị nhầm với Agent Wake (phiên Agent tự thức dậy và tự xử lý) | transcript.md, các quyết định AUTO-WAKE-ARCH-02 và PAUSE-AUTOWAKE-01; AUTO-WARE/05_DECISION.md | REPORTED-IN-TRANSCRIPT | Sai định nghĩa mục tiêu, kéo dài triển khai và làm lệch acceptance | Briefing phải định nghĩa outcome quan sát được; checkpoint phân biệt event received / task queued / agent started / task completed |
| C-03 | Trigger HTTP có speaker=null do route không truyền identity; identity_id có nơi chỉ là lời khai, không phải xác thực | REPORT_802001_PHASE2.md; RUNBOOK_REAL_KA.md; transcript.md | VERIFIED-IN-RECORD | Không xác định chắc chắn actor; audit và quyền có thể bị hiểu sai | Kiểm tra actor identity và trust level; nếu thiếu hoặc chưa xác thực thì cảnh báo/hold/escalate, không tự gán danh tính |
| C-04 | Ka gửi message vào chính meeting của mình tạo self_loop; không được tính là trigger hợp lệ | REPORT_802001_PHASE2.md; RUNBOOK_REAL_KA.md; transcript.md | VERIFIED-IN-RECORD | Agent có thể hiểu nhầm việc tự gửi phản hồi là đã nhận assignment | Hướng dẫn rõ nguồn giao việc, người giao, trigger_message_id; phân biệt self-loop với assignment hợp lệ |
| C-05 | Connector trong package là local-file adapter; RealLLMAdapter NotImplementedError; MOCK chỉ chứng minh plumbing | 04_CODE/CODE_ANALYSIS.md; 06_EVIDENCE/EVIDENCE.md; E2E_802001/README_EVIDENCE.md | VERIFIED-IN-RECORD | Đầu ra demo không đại diện production boundary hoặc năng lực thật | Yêu cầu chỉ rõ môi trường, adapter, model thật/giả và destination; kiểm tra evidence ở boundary đích |
| C-06 | Idempotency ban đầu chỉ ở RAM/process-local, chưa đủ chứng minh restart/replay an toàn | 04_CODE/CODE_ANALYSIS.md; REPORT_802001_PHASE2.md; AUTO-WARE/04_GAP_ANALYSIS.md | VERIFIED-IN-RECORD | Retry/restart có thể tạo phản hồi hoặc tác vụ trùng | Checkpoint sau restart/replay; yêu cầu stable event/task key và bằng chứng durable state |
| C-07 | Test có khả năng tự sửa transcript/evidence, làm giảm tính độc lập và khả năng tái lập | 04_CODE/CODE_ANALYSIS.md; 05_TEST/TEST_ANALYSIS.md | VERIFIED-IN-RECORD | Evidence có thể bị test làm nhiễm; reviewer khó phân biệt input/output gốc | Tách input fixture, output và immutable evidence; reviewer kiểm tra hash/readback |
| C-08 | Tài liệu transcript và gói source có chỗ không khớp; ví dụ mô tả endpoint/auth so với zip source được review | AUTO-WARE/04_GAP_ANALYSIS.md | VERIFIED-IN-RECORD (mismatch được báo cáo trong gap analysis) | Agent có thể làm theo tài liệu cũ hoặc tuyên bố trạng thái không khớp bản đang chạy | Mọi hướng dẫn phải ghi source version/commit/runtime target; trước khi sửa phải TRACE source thực tế |
| C-09 | Thiếu quyền, API channel, token hoặc môi trường thực khiến E2E thật BLOCKED; có nguy cơ tìm cách workaround ngoài quyền | AUTO-WARE/05_DECISION.md; RUNBOOK_REAL_KA.md; transcript.md | VERIFIED-IN-RECORD | Vượt quyền, dùng sai credential, hoặc báo DONE dù điều kiện chưa có | Dùng blocker protocol: điều kiện thiếu / bằng chứng / các cách đã thử / lựa chọn / owner cần cấp quyền; không giả lập PASS |
| C-10 | Có nhiều lần thay đổi định hướng và cuối cùng tạm dừng nhánh Workspace Agent/API theo quyết định của Vinh | transcript.md, PAUSE-AUTOWAKE-01; các hồ sơ AUTO-WARE | REPORTED-IN-TRANSCRIPT | Tiếp tục đầu tư sau khi scope đã dừng; phát sinh công việc và chi phí không cần thiết | Scope lock/change control: mọi thay đổi mục tiêu phải có decision record; khi PAUSED thì dừng implementation và giữ nguyên artefact |

## 3. Chuỗi giám sát suy ra từ các case
1. Intake: xác nhận Work, mục tiêu, owner, quyền, nguồn chuẩn và output mong đợi.
2. Briefing: nêu rõ việc phải làm/không được làm, tiêu chí PASS/BLOCKED và đường dẫn evidence.
3. Acknowledgement: Agent xác nhận hiểu scope, nguồn và checkpoint; không xem im lặng là nhận việc.
4. Checkpoint: đo tiến độ theo artefact/outcome, không theo lời báo cáo đơn thuần.
5. Observation: so sánh báo cáo với source, runtime, commit, test output và readback.
6. Guidance: nhắc đúng finding, dẫn nguồn chuẩn, nêu hành động sửa cụ thể và thời hạn/checkpoint.
7. Correction: Agent nộp bằng chứng sửa; không tự đóng finding.
8. Recheck: reviewer hoặc supervisor xác minh độc lập; giữ nguyên FAIL/BLOCKED nếu thiếu bằng chứng.
9. Escalation: lặp lỗi, vượt quyền, sai identity, scope drift hoặc không phản hồi thì chuyển cấp có thẩm quyền.
10. Journal: ghi thời điểm, actor, assignment, finding, source, nhắc nhở, phản hồi, correction, kết quả và next step.

## 4. Những gì chưa được phép kết luận
- Chưa có bằng chứng Work 802001 hiện đã có runtime giám sát tự động, reminder tự động hoặc enforcement.
- Chưa đủ dữ liệu để xác định tần suất nhắc tối ưu hay SLA chung cho mọi loại Work.
- Chưa chứng minh các case trên đại diện cho toàn bộ hành vi Agent trong ROOM-HOP.
- Chưa được biến mọi tình huống kỹ thuật thành vi phạm cá nhân; một số là thiếu điều kiện hệ thống hoặc sai lệch tài liệu.
- Chưa mở BUILD; chưa sửa code, API, Core, MCP hoặc Agent Runtime.

## 5. Câu hỏi cần chốt ở DEFINE
- Phân loại finding: scope / source-of-truth / identity-authority / evidence-quality / technical-blocker / execution-quality / safety.
- Severity và reminder cadence theo rủi ro, deadline và checkpoint.
- Ai có quyền phát reminder, yêu cầu correction, đóng finding và escalation.
- Khi nào Agent được tự sửa; khi nào phải xin phê duyệt.
- Evidence tối thiểu để chuyển IN_PROGRESS → PASS, BLOCKED → RESOLVED, và finding → CLOSED.
