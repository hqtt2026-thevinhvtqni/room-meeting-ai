# BIÊN BẢN PHÂN CÔNG REVIEW ĐỘC LẬP — WORK 28
- Work: 28 — MCP-8020-TOOLING-PLATFORM
- Ngày: 2026-10-11
- Authority: Vinh
- Điều phối/thi công: Xu
- Trạng thái Work: ACTIVE / NOT LOCKED
- Biên bản ROOM-HOP: MEETING-GATE2-EXT-001
- Transcript message đã ghi: msg_aaa93ea4fa1b
- Trạng thái xác minh: nội dung biên bản ROOM-HOP đã được đọc lại từ transcript; chưa có bằng chứng Go/Cla đã nhận hoặc thực thi.

## 1. Mục tiêu
Xây dựng khả năng để AI chạy Python và kiểm thử qua MCP :8020, nhận kết quả chạy thật, đọc lỗi, sửa mã, chạy lại và lưu bằng chứng. Luồng chuẩn: AI → MCP :8020 → Core :8000 (authorization + WorkContext) → runtime canonical đã được duyệt (W12/W13 hoặc Work 27 sau khi tích hợp thật) → kết quả/evidence.

Không tạo Core 2, không thêm execution host trùng lặp, không cung cấp unrestricted shell, không bypass Core.

## 2. Phân công cho Go (Grok) — Review E2E
1. Đọc requirement, architecture plan, MCP tool registry, quyết định AI chạy Python qua MCP, test plan và implementation checkpoint của Work 28.
2. Kiểm tra đường đi thực tế MCP → Core → runtime → stdout/stderr/exit code → evidence; phân loại phần chưa triển khai và phần chưa có bằng chứng.
3. Đề xuất ca acceptance: smoke test; chương trình/test cố tình thất bại; timeout và cleanup; WorkContext không được phép; path traversal; sửa file Sandbox rồi chạy lại với run_id/correlation và readback/hash.
4. Báo cáo từng mục PASS / FAIL / BLOCKED, kèm evidence/ref. Không suy ra PASS từ tài liệu hoặc mock.
5. Chỉ review và báo cáo; không sửa source Work 28 trong lượt review này.

## 3. Phân công cho Cla (Claude) — Review bảo mật
1. Đọc cùng bộ tài liệu Work 28.
2. Đánh giá WorkContext/authorization, traversal và symlink, command injection, process isolation, timeout/cleanup, CPU/memory/output bounds, package installation, network, secrets/host access, concurrent runs, log redaction và audit.
3. Tạo negative-test matrix gồm input/attack, expected status, evidence cần thu và severity/risk nếu lọt.
4. Kiểm tra contract/schema có cho phép unrestricted shell hoặc tạo PASS khi không có bằng chứng runtime thật hay không.
5. Chỉ review và báo cáo; không sửa source Work 28 trong lượt review này.

## 4. Đầu ra bắt buộc
Mỗi agent nộp báo cáo riêng dưới `06_EVIDENCE/` hoặc phản hồi qua cơ chế ROOM-HOP được phép. Báo cáo phải có agent, thời điểm, phạm vi đọc, phát hiện, mức độ nghiêm trọng, test đề xuất, evidence/ref và trạng thái. Nếu không truy cập được Sandbox/runtime, ghi BLOCKED và nêu điểm chặn chính xác. Không chỉ phản hồi “đã nhận”.

## 5. Trạng thái hiện tại / điều kiện hoàn tất
Các file contract, test scaffold, registry, quyết định Python qua MCP và checkpoint đã được ghi/readback qua Sandbox. Python tests chưa được chạy; `python_run` chưa được xác minh là tool live; full E2E chưa PASS. Work 28 tiếp tục ACTIVE / NOT LOCKED cho đến khi có bằng chứng acceptance thật và được xem xét.

Xu hợp nhất báo cáo, xử lý phát hiện và tổ chức kiểm thử lại. Chỉ Vinh/Xu quyết định tích hợp và hoàn tất Work.


---

## 6. BIÊN BẢN TIẾP NỐI ĐIỀU PHỐI — 2026-10-12

- Người chốt thứ tự kỹ thuật: Ka (CSA), theo quyền điều phối Work 28 do Vinh giao.
- Người thực hiện gói tiếp theo: Xu — implementation owner; cần đọc mục này cùng toàn bộ requirement, architecture plan, báo cáo Go/Cla và quyết định kỹ thuật của Ka trước khi sửa source.
- Trạng thái Work: ACTIVE / NOT LOCKED. Đây là giao việc; không phải xác nhận Xu đã nhận hoặc đã thực thi.

### Quyết định bắt buộc
1. **NO-GO** đăng ký/bật `python_run` hoặc bất kỳ công cụ chạy Python nào cho đến khi chứng minh được authorization, WorkContext, cô lập OS và đường chạy runtime chuẩn.
2. **GO** cho source/boundary discovery chỉ-đọc và hardening contract có giới hạn. Không tạo Core 2, không dựng execution host trùng lặp, không unrestricted shell, không bypass Core.
3. Core :8000 tiếp tục là authority duy nhất về authorization và WorkContext; MCP :8020 chỉ là adapter.
4. Mọi kết luận PASS phải có bằng chứng chạy thật: lệnh/target đã duyệt, run_id do server cấp (nếu có thực thi), exit code, output/test summary đáng tin cậy, source hash và evidence_ref. Sandbox write/readback hoặc test trong container riêng không thay thế G3/G5.
5. Evidence chạy phải được ghi bởi runtime/Core vào vùng được bảo vệ; không để agent bất kỳ ghi đè/xóa báo cáo review hoặc log chứng cứ của agent khác.

### Giao Xu — WP0 trước, WP1 sau
**WP0 — Source/boundary discovery (bắt buộc trước khi tích hợp):**
- Kiểm kê source và revision thực tế của MCP :8020: tool registry, handler và điểm gọi Core.
- Truy dấu Core :8000: authorization, principal đã xác thực, WorkContext routing và quyền đọc/ghi/run theo Work.
- Xác định interface runtime canonical hiện có ở W12/W13 hoặc Work 27; chứng minh runtime nào thật sự đã được tích hợp, không chỉ dựa vào tài liệu.
- Lập source map gồm file path, revision/SHA, function/route, request/response schema, principal source, timeout/isolation/evidence path và các dependency chưa truy cập được.
- Nếu thiếu source hoặc không truy cập được runtime, ghi **BLOCKED + bằng chứng cụ thể**; dừng tại boundary, không tự phát minh endpoint hoặc sửa Core để demo chạy.

**WP1 — Contract hardening (chỉ sau khi đã lập source map; regression tests đi kèm):**
- Sửa contract để không thể biểu diễn execution PASS nếu thiếu run_id, exit_code=0, evidence_ref và test summary đáng tin cậy; tách kết quả non-execution nếu cần.
- Thêm trạng thái non-terminal/terminal cần thiết (QUEUED, RUNNING, CANCELLED) và không ánh xạ chúng thành FAIL.
- Siết path validation cho Unicode confusables/bidi/invisible/control chars, Windows reserved names, trailing dot/space, option-like components; bổ sung regression test. Validator thuần không thay thế kiểm tra containment thật và chặn symlink/reparse point ở filesystem adapter.
- Sửa cách đóng gói/discovery test để có lệnh chạy sạch, lặp lại được, không phụ thuộc PYTHONPATH thủ công; thất bại nếu không chạy test nào.
- Không tuyên bố PASS nếu chưa chạy bằng runner đã được phê duyệt và lưu exit code/output.

### Phân công phối hợp
- **Xu:** thực hiện WP0, đề xuất patch WP1 dựa trên source thật, ghi checkpoint và evidence.
- **Cla:** giữ security review/veto cho execution; rà soát isolation, authorization, evidence integrity và negative-test matrix sau patch. Không tự chứng nhận implementation của Xu.
- **Go:** giữ độc lập E2E; chỉ chạy acceptance sau khi WP0/WP1 và security prerequisites đủ bằng chứng.
- **Ka:** điều phối thứ tự, rà soát evidence và cập nhật PASS/FAIL/BLOCKED; không suy ra PASS từ báo cáo tự khai.
- **Vinh:** final authority đối với quyết định tích hợp và đóng Work.

### Điều kiện chuyển bước
Xu cần công bố source map và blocker trước khi mở execution implementation. Chỉ sau khi boundary/runtime được xác minh và Cla xem xét mô hình cô lập mới lập kế hoạch bật runner; sau đó Go thực hiện checklist E2E qua entry point MCP thật. Work 28 chỉ được COMPLETED/LOCKED khi các gate tương ứng có evidence readback độc lập.


---

## 7. Điều chỉnh người điều phối theo chỉ thị Vinh — 2026-10-12

Vinh giao Ka (CSA) chủ động điều phối và triển khai toàn trình Work 28 trong thời gian Xu tập trung dự án khác. Đây là thay đổi phạm vi điều phối/thi công của Work 28, không chuyển quyền kiến trúc tổng thể hoặc quyền phê duyệt cuối khỏi Vinh.

- Điều phối và thi công trong phạm vi Work 28: **Ka (CSA)**.
- Xu: không bị yêu cầu dừng dự án khác; chỉ tham gia khi cần quyết định kiến trúc vượt phạm vi đã ủy quyền hoặc khi Vinh yêu cầu.
- Cla: reviewer bảo mật độc lập, có quyền giữ NO-GO với execution nếu chưa có bằng chứng cô lập/ủy quyền/evidence.
- Go: reviewer E2E độc lập; không tự chứng nhận khi chưa chạy qua MCP entry point thật.
- Vinh: final authority, phê duyệt tích hợp và đóng Work.

Căn cứ kỹ thuật mới: source map tại `06_EVIDENCE/KA_WP0_SOURCE_BOUNDARY_MAP_20261012.md`; contract hardening checkpoint tại `06_EVIDENCE/KA_CONTRACT_HARDENING_CHECKPOINT_20261012.md`; execution tool design tại `03_ARCHITECTURE/PROPOSED_EXECUTION_TOOL_CONTRACT_V1.md`.

Trạng thái không đổi: ACTIVE / NOT LOCKED. Không bật `python_run` khi deployed Core route, authenticated principal, canonical runtime và OS isolation chưa được chứng minh.

## 8. BIÊN BẢN ĐIỀU PHỐI AUTOMATIC E2E — 2026-10-12

**Quyết định của Ka theo ủy quyền Vinh:** chủ động xây dựng quy trình E2E Automatic trong Work 28 Sandbox; giữ nguyên MAIN SOURCE và không đăng ký execution tool live khi security gates chưa đạt.

### 8.1 Phần đã xây dựng
1. `03_ARCHITECTURE/WORK_28_AUTOMATIC_E2E_BLUEPRINT.md`: pipeline DISCOVER → AUTHORIZE → SNAPSHOT → HASH → DISPATCH → COLLECT → VERIFY → PERSIST → READBACK → REPORT; có 18 ca acceptance A01–A18.
2. `03_ARCHITECTURE/PROPOSED_EXECUTION_TOOL_CONTRACT_V1.md`: hợp đồng tool dự kiến, chưa đăng ký.
3. `04_CODE/tool_contracts.py`: contract 1.1.0 được harden, thêm `ExecutionOperation`; RUN_TESTS PASS cần test count > 0 và failures/errors = 0.
4. `05_TEST/test_tool_contracts.py`: thêm regression tests cho operation declaration, zero tests, test failure và serialization.
5. `05_TEST/WORK_28_TEST_PLAN.md`: lệnh test chuẩn và gate status.
6. `06_EVIDENCE/PC_READONLY_RUNTIME_EVIDENCE_REQUEST_20261012.md`: yêu cầu metadata PC chỉ đọc.

### 8.2 Giao Cla — security review độc lập
- Đọc source map, proposed tool contract, E2E blueprint, contract 1.1.0/1.2 changes và báo cáo security trước đó.
- Kiểm tra threat model và negative cases A02–A07, A11–A15, A17–A18; tập trung authenticated principal, spoofed `authorized`, symlink/reparse containment, OS isolation, resource caps, process-tree cleanup, evidence tamper resistance.
- Lập `06_EVIDENCE/CLA_AUTOMATIC_E2E_SECURITY_REVIEW_20261012.md`, ghi từng finding PASS/FAIL/BLOCKED, severity, source path, exact evidence. Chỉ ghi test command/log/exit code nếu thật sự chạy.
- Không cần chờ Ka để nêu NO-GO; không sửa hoặc ghi đè evidence của Ka.

### 8.3 Giao Go — E2E acceptance độc lập
- Đọc E2E blueprint và security review của Cla.
- Trước khi chạy: chứng minh deployed MCP/Core SHA, live registered tool list, authenticated principal, Core WorkContext route, canonical runtime identity, OS isolation và protected evidence.
- Khi prerequisites đủ, chạy A01, A02, A04, A06, A07, A08–A11, A14–A18 qua MCP entry point thật; thực hiện baseline → test-only mutation FAIL → patch → rerun PASS trong disposable test Work.
- Lập `06_EVIDENCE/GO_AUTOMATIC_E2E_ACCEPTANCE_20261012.md` với command, run_id, source SHA, runtime build identity, exit code, stdout/stderr refs, evidence readback và từng gate.
- Không gọi direct runtime, mock adapter hoặc local unit tests là live E2E. Nếu prerequisite thiếu, ghi BLOCKED và bằng chứng cụ thể.

### 8.4 Gate và điều kiện đóng
- Contract source/test persistence + readback: PASS về ghi/đọc file, không phải test execution.
- G3 approved runner, G4 authorization/isolation, G5 live MCP→Core→runtime→protected evidence, G6 E2E: BLOCKED.
- NO-GO đăng ký/bật `python_run` cho tới khi Cla không còn security blocker và Go cung cấp E2E evidence độc lập.
- Work 28 vẫn ACTIVE / NOT LOCKED; Vinh giữ quyền final approval.


## 8. CẬP NHẬT ĐIỀU PHỐI KA — READBACK CLA/GO — 2026-10-12

### Bằng chứng MCP quan sát được
- `sandbox_list_works` và `sandbox_list(work_id="28")` trả kết quả `status=ok`; Work 28 hiện diện, manifest tồn tại và các artifact handoff/review có thể đọc.
- `list_meetings` trả danh sách meeting.
- Inbox cá nhân Cla và Go qua `get_pending_tasks` đều rỗng. Do đó không ghi nhận task đã được dispatch tới inbox riêng; việc phân công hiện được lưu bằng artifact Sandbox.
- Không có `python_run`, `python_status` hoặc execution tool nào trong live tool surface đã quan sát. Các readback trên không chứng minh PC listener, deployed revision, authorization hay runtime.

### Quyết định sau báo cáo độc lập
- Cla đã nộp `CLA_AUTOMATIC_E2E_SECURITY_REVIEW_20261012.md`: **SECURITY NO-GO**; các finding N01–N03 được xác minh trong container riêng của Cla, N08 Critical vẫn cần kiểm tra listener PC chỉ-đọc.
- Go đã nộp `GO_AUTOMATIC_E2E_ACCEPTANCE_20261012.md`: A01–A18 NOT RUN/BLOCKED, prerequisites G3–G6 BLOCKED. File Go ghi “Cla artifact missing” tại thời điểm viết; readback hiện tại xác nhận file Cla đã tồn tại. Đây là cập nhật trạng thái artifact, không phải đổi gate.
- Ưu tiên ngay: PC read-only evidence theo `PC_READONLY_RUNTIME_EVIDENCE_REQUEST_20261012.md`; dùng `git --no-optional-locks -c core.fsmonitor=false` để giảm tác động của status. Kiểm tra listener 8000/8020/8031; không dừng/khởi động dịch vụ, không đọc/in secrets hoặc command lines.
- Chỉ sau khi xác minh boundary PC mới triển khai contract patch N01–N07 và regression tests. Không bật execution trong lúc N08 chưa được loại trừ, N02 chưa có trusted test result design, và OS isolation/evidence protection chưa được chứng minh.

### Gate status
- G3 canonical/approved runner: BLOCKED.
- G4 authenticated principal + Core authorization + OS isolation: BLOCKED.
- G5 live MCP → Core → canonical runtime → protected evidence: BLOCKED.
- G6 full automatic E2E: BLOCKED.
- `python_run`: NOT REGISTERED; NO-GO.
- Work 28: ACTIVE / NOT LOCKED. Vinh giữ quyền phê duyệt cuối.
