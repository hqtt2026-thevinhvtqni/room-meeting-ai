# NHẬT KÝ THI CÔNG & KIỂM THỬ — WORK 118

## Entry 001 — Khởi tạo Work
- **Thời gian:** 2026-11-20 (UTC)
- **Phạm vi:** Kiểm tra danh mục Work trên GitHub main; tạo Issue #65; khởi tạo hồ sơ W118.
- **Phương pháp:** Đọc GitHub repository contents cho `work/`, kiểm tra cấu trúc W117 và W70; tạo GitHub Issue qua GitHub API; tạo hồ sơ Work.
- **Bằng chứng:**
  - Issue #65: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/issues/65
  - Work root: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/tree/main/work/118/HQTT-GITHUB-WORKFLOW-AUTOMATION
  - Tham chiếu W70: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/tree/main/work/70/ROOM-HOP-PRODUCT-LIFECYCLE-AND-WORK-DASHBOARD
- **Kết quả:** DONE — đã tạo Issue và hồ sơ khởi tạo trên GitHub main.
- **Kiểm thử CI / runtime:** NOT RUN — chưa có code hoặc workflow mới được triển khai.
- **Trạng thái Work:** DISCOVER / DEFINE — IN PROGRESS.
- **Bước tiếp theo:** Rà soát workflow/permissions hiện có, lập ma trận sự kiện và actor; sau đó chuẩn bị brief phản biện kiến trúc.

## Entry 002 — W118-01 Kiểm kê hiện trạng GitHub (Discovery)
- **Thời gian:** 2026-11-20 (UTC+7)
- **Phạm vi:** W118-01 — kiểm kê workflows, branches, quyền, cơ chế CI/evidence hiện có trong repo; đối chiếu 8 câu hỏi thiết kế của BB-118-001 §4.
- **Phương pháp:** Đọc trực tiếp GitHub contents API tại main head `8675ad5`: liệt kê `.github/workflows/`, đọc toàn bộ 2 workflow file (w300-dashboard-ci.yml, work70-preview-host.yml), liệt kê 77 branches và 19 thư mục work trên main; đối chiếu bài học đã ghi nhận của Work 300 (2026-11-15).
- **Kết quả:** W118-01 **DONE (docs-only)**. Kết luận chính:
  - Chỉ có 2 workflow, đều push-trigger trên main, path-filtered; 0 workflow lắng nghe issue events; không có webhook/ROOM-HOP integration nào.
  - Không có evidence contract cho CI; log Actions cần quyền admin để tải; pattern duy nhất hiện có là "đăng diagnostics lên issue" (w300).
  - Phát hiện rủi ro thiết kế: w300 CI tự commit/Prettier rồi push lại (GITHUB_TOKEN không trigger workflow) → cần item chống vòng lặp trong W118-05.
  - Khuyến nghị hướng thiết kế (nháp chưa phản biện): GitHub-native events trước, webhook sau; tái dùng schema EVIDENCE_REGISTER của Work 70; không auto-merge.
- **Bằng chứng:** [EVIDENCE/W118-01_GITHUB_DISCOVERY_20261120.md](W118-01_GITHUB_DISCOVERY_20261120.md); workflows source tại commit `8675ad5`.
- **Blocker mới:** không đọc được secrets/webhook settings cấp repo qua API read-only — ghi BLOCKED phụ, cần Vinh xác nhận khi cấu hình phần pilot (sau G3).
- **Kiểm thử CI / runtime:** NOT RUN — bước này thuần khảo sát, không triển khai gì.
- **Trạng thái Work:** DISCOVER / DEFINE — IN PROGRESS (W118-01 DONE; kế hoạch KH-118-001 đã cập nhật).
- **Bước tiếp theo:** W118-02 — soạn quy ước Issue/Branch/Commit/PR + templates (nháp); đồng thời soạn brief phản biện kiến trúc để phục vụ W118-08.

## Entry 003 — W118-02 Quy ước + DC-118-003 brief phản biện (docs-only DRAFT)
- **Thời gian:** 2026-11-20 (UTC+7)
- **Phạm vi:** W118-02 soạn quy ước Issue/Branch/Commit/PR (QC-118-002, DRAFT) và DC-118-003 brief phản biện kiến trúc (6 AD) để chuẩn bị W118-08; đồng thời sửa lỗi văn bản phát hiện khi readback commit `229d2b0`.
- **Bằng chứng:** 2 file mới trong 02_DEFINE; commits `229d2b0` và commit sửa lỗi của phiên này.
- **Kiểm thử CI / runtime:** NOT RUN.
- **Trạng thái:** W118-02 DRAFT (chờ phản biện — không coi là DONE vì chưa qua review); W118-08 IN PROGRESS (brief sẵn sàng giao Ka/Xu).
- **Bước tiếp:** giao brief cho Ka review độc lập; Xu tổng hợp ý kiến; Vinh ACK để chuyển gate G1/G2 trước khi chốt kiến trúc.

## Entry 004 — W118-03/04/05 thiết kế (docs-only DRAFT)
- **Thời gian:** 2026-11-20 (UTC+7)
- **Phạm vi:** TD-118-004 (CI & evidence contract), TD-118-005 (event orchestration), TD-118-006 (failure/retry/idempotency). Đã đọc schema EVIDENCE_REGISTER v1.1 của Work 70: additionalProperties false, không có field run-level, nên đề xuất extension v1.2 (ci_run_id, ci_job, ci_conclusion, ci_url) dạng optional, backward-compatible.
- **Bằng chứng:** 3 file TD mới trong 02_DEFINE + commit của entry này.
- **Kiểm thử CI / runtime:** NOT RUN.
- **Trạng thái:** cả 3 thiết kế DRAFT chờ phản biện; KHÔNG PASS.
- **Bước tiếp:** Ka review các TD kèm DC-118-003; Xu tổng hợp; Vinh ACK.

## Entry 005 — W118-06/07 thiết kế (docs-only DRAFT)
- **Thời gian:** 2026-11-20 (UTC+7)
- **Phạm vi:** TD-118-007 (gate matrix: MERGE cần CI PASS + evidence RECORDED + 1 review độc lập; ACCEPTANCE cần evidence VERIFIED bởi Ka; RELEASE do Vinh duyệt; không auto-merge) và TD-118-008 (evidence register là nguồn bot-ghi duy nhất ở state RECORDED; Dashboard W70 là read-only projection; reconciliation định kỳ đăng lên issue audit; bot append-only, không ghi đè nhật ký người).
- **Bằng chứng:** 2 file TD mới trong 02_DEFINE; commit của entry này. Readback 3 file TD trước đó tại commit 389d3d7 đã sạch.
- **Kiểm thử CI / runtime:** NOT RUN.
- **Trạng thái:** W118-06, W118-07 DRAFT. Hoàn tất soạn thảo W118-01..07; còn lại chờ W118-08 phản biện tổng hợp.
- **Bước tiếp:** cập nhật DC-118-003 tham chiếu đủ bộ TD; Ka review; Xu tổng hợp; Vinh ACK (chuyển G2 sang G3).

## Entry 006 — PRODUCT v1 pilot deployed (code)
- **Thời gian:** 2026-11-20 (UTC+7)
- **Phạm vi:** Theo quyết định của Vinh ("sản phẩm trước, Xu nghiệm thu, Vibe quyết cấu trúc"): Vibe quyết cấu trúc, bỏ vòng phản biện dài, triển khai pilot v1 thật.
- **Sản phẩm:** .github/workflows/w118-workflow-automation.yml — 3 jobs (handoff-brief, ack-verification, ci-failure-diagnostics), least-privilege, chống vòng lặp nhờ GITHUB_TOKEN không tự re-trigger, chống retry vô hạn bằng quy trình RETRY-n với cap 2.
- **Cấu trúc:** 1 workflow duy nhất, 3 trigger (issues / issue_comment / workflow_run), không webhook, không PAT, không auto-merge.
- **Bằng chứng:** commit sản phẩm + readback; STATUS.md trong 00_ROOT.
- **Kiểm thử:** cú pháp file được kiểm tra kỹ bằng tay; RUNTIME TEST_PENDING — cần issue gắn label w118-handoff và comment ACKED-test để có bằng chứng chạy thật trước khi Xu nghiệm thu.
- **Trạng thái Work:** BUILD (PILOT DEPLOYED) — chờ runtime evidence.

## Entry 007 — Runtime test W118 pilot — RUN QUEUED (chưa PASS)
- **Thời gian:** 2026-11-20 ~13:31 UTC (UTC+7 ~20:31)
- **Phạm vi:** Bật runtime thật cho pilot: comment ACKED-orchestrator 65 (id 7032614831 rồi 7032645457) kích hoạt workflow W118 Workflow Automation Pilot.
- **Trình tự commit phiên này:** 7665f47 (deploy pilot v1) -> run #1 FAILURE do YAML parse lỗi tại L55 (bằng chứng: annotation "Invalid workflow file ... #L55" trên trang run) -> 549b480 (sửa printf xuống dòng) -> 0143482 (viết lại if một dòng, bỏ folded if, bỏ concurrency phức tạp) -> run #2 (Issue comment #65, created) ở trạng thái QUEUED tại thời điểm ghi (bằng chứng trang Actions, ~15 phút mà chưa có runner).
- **Kết quả:** CHƯA PASS — theo Evidence First, PILOT status = RUNTIME TEST_PENDING/QUEUED; cần theo dõi run #2 tới xanh (bằng chứng: run URL + kết quả job ack-verification post comment lên #65).
- **Cách kiểm tra cho ai tiếp theo:** mở https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/workflows/w118-workflow-automation.yml — nếu run #2 xanh, comment "W118 pilot: ACK recorded" của bot phải xuất hiện trên Issue #65; sau đó trình Xu nghiệm thu theo STATUS.md.
- **Trạng thái Work:** BUILD (PILOT DEPLOYED, RUN PENDING).

## Entry 008 — RUNTIME TEST PASS — PILOT có bằng chứng thật
- **Thời gian:** 2026-11-20 (~13:45 UTC / 20:45 UTC+7)
- **Bằng chứng runtime (kiểm trực tiếp trên trang Issue #65):**
  - Run #2 "W118 Workflow Automation Pilot", event issue_comment #65, kết luận completed success (thời lượng 6 giây). Trang: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/workflows/w118-workflow-automation.yml
  - Comment của bot github-actions trên Issue #65 (ngay sau comment ACKED-orchestrator 65 của người thực thi): "W118 pilot: ACK recorded. - Actor: hqtt2026-thevinhvtqni. Token acked: yes (body starts with ACKED-). ..." — nghĩa là job ack-verification đã: nhận event thật, đánh giá if-condition đúng, mount env vars, thực thi shell, và post bằng chứng có cấu trúc.
- **Kết luận:** PILOT RUNTIME VERIFIED (1/3 job có bằng chứng chạy thật: ack-verification). 2 job còn lại (handoff-brief, ci-failure-diagnostics) có cùng cơ chế trigger/steps, chờ sự kiện tự nhiên tiếp theo để có bằng chứng riêng; cùng runtime đã đạt ở mức nền tảng.
- **Điểm đối soát:** run #1 FAILURE (YAML L55) được sửa ở 0143482 — run #2 chạy trên cấu trúc if-một-dòng, chứng minh parse OK.
- **Trạng thái Work:** BUILD -> PILOT RUNTIME VERIFIED. Trình Xu nghiệm thu theo STATUS.md; sau khi Xu ACK thì gate G4/G5 coi như đạt ở mức pilot, work chuyển OPERATE-ready (docs-only).


## Entry 009 — Nghiệm thu độc lập GitHub W118 (NOT ACCEPTED)
- **Thời gian:** 2026-11-20 (UTC+7).
- **Phạm vi:** Kiểm tra nghiệm thu hồ sơ W118 trên GitHub `main`: Issue #65, PR #66, workflow pilot, Actions runs, STATUS, kế hoạch và các thiết kế event/retry/gate.
- **Phương pháp:** Đọc trực tiếp GitHub API; kiểm tra PR changed-files, Issue labels, metadata workflow run, nội dung STATUS.md, KH-118-001, TD-118-005/006/007 và nhật ký hiện hành.
- **Bằng chứng:**
  - Issue #65: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/issues/65 — Issue đang mở, nhãn hiện thấy là `enhancement`; chưa thấy bằng chứng nhãn `w118-handoff` được dùng để kiểm thử handoff.
  - PR #66: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/pull/66 — PR ở trạng thái Draft/chưa merge; thay đổi gồm workflow `w118-coordination-ci.yml`, templates và hồ sơ thiết kế/pilot. Không đồng nhất tên với workflow pilot đang được STATUS.md mô tả là `w118-workflow-automation.yml`; cần đối chiếu hai luồng và commit head trước khi chốt.
  - Run #2: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44690614366 — workflow `W118 Workflow Automation Pilot`, event `issue_comment`, kết luận `success`, head SHA `0143482692afa7a0569218a8e656665e19e54ce8`. Nhật ký/STATUS ghi nhận bot đã đăng comment ACK recorded trên Issue #65. Đây là bằng chứng runtime thật cho job `ack-verification`.
  - Run #1: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44690358863 — được hồ sơ hiện có ghi nhận thất bại do lỗi YAML; không dùng lần thất bại này làm bằng chứng kiểm thử job diagnostics.
  - STATUS.md: `PILOT RUNTIME VERIFIED`, nhưng chính tài liệu giới hạn bằng chứng ở 1/3 job.
  - KH-118-001: W118-02..08 vẫn DRAFT/IN PROGRESS; W118-09 có runtime evidence nhưng không thay thế review/acceptance.
  - TD-118-005: thiết kế yêu cầu mapping role → GitHub login và xác minh actor; bằng chứng thực tế hiện mới cho thấy workflow ACK kiểm tra nội dung bắt đầu bằng `ACKED-`, chưa chứng minh mapping danh tính/role được áp dụng.
  - TD-118-006: chưa có run kiểm thử FAIL thực tế chứng minh diagnostics issue được tạo/cập nhật đúng, chống trùng và giới hạn retry.
  - TD-118-007: yêu cầu review độc lập và evidence VERIFIED; PR #66 vẫn Draft, chưa có bằng chứng merge/review đạt điều kiện.
- **Kết quả nghiệm thu: NOT ACCEPTED — chưa đủ điều kiện nghiệm thu toàn Work.** Chỉ xác nhận có runtime success giới hạn cho `ack-verification`; không suy rộng thành PASS cho toàn bộ sản phẩm.
- **Phân loại:**
  - PASS có giới hạn: pilot `ack-verification` đã chạy thành công trên GitHub Actions.
  - NOT VERIFIED: `handoff-brief`, `ci-failure-diagnostics`, kiểm thử failure/retry/idempotency, đồng bộ Evidence Register/Dashboard.
  - BLOCKED: xác thực actor/role theo mapping; review độc lập và điều kiện nghiệm thu PR; đối chiếu workflow pilot trên main với workflow trong PR #66.
- **Giới hạn thao tác:** Chỉ đọc/truy vết và ghi nhật ký; không sửa mã/workflow, không đổi labels/permissions, không merge PR, không bật auto-merge.
- **Bước tiếp theo:** (1) đối chiếu hai workflow và xác định một luồng pilot canonical; (2) lập test cases riêng cho handoff, ACK identity/role và diagnostics FAIL; (3) bổ sung bằng chứng retry/idempotency; (4) yêu cầu review độc lập theo TD-118-007; (5) cập nhật Evidence Register/Dashboard sau khi schema được chốt. Mỗi test phải có run URL, commit SHA, job conclusion và output thực tế.
- **Trạng thái:** WORK 118 = NOT ACCEPTED / PILOT PARTIALLY VERIFIED. Không đánh dấu G4/G5 PASS toàn Work.

## Entry 009 — Kết luận nghiệm thu của Xu: NOT ACCEPTED — vòng kiểm thử độc lập được thiết lập
- **Thời gian:** 2026-11-20 (sau Entry 008)
- **Phạm vi:** ghi nhận kết luận nghiệm thu độc lập của Xu trên Issue #65; không chỉnh sửa bất kỳ mã nguồn nào (đúng phương án của Xu).
- **Kết luận của Xu:** NOT ACCEPTED — pilot chạy được một phần (Run #2 SUCCESS, ack-verification có bằng chứng) nhưng chưa đủ chuỗi end-to-end; AC-R1..AC-R6 (chi tiết hồ sơ XU-118-AC-001).
- **Quyết định tuân theo:** giữ nguyên main, chưa merge PR #66, chưa bật tự động hóa diện rộng; Vibe KHÔNG sửa mã trong vòng nghiệm thu.
- **Bàn giao:** KT-118-009 là danh sách kiểm thử bổ sung (T-01..T-06) cho Xu thực hiện vòng kiểm thử độc lập; Vibe hỗ trợ ghi hồ sơ và đối chiếu PR #66 khi được gọi.
- **Bằng chứng:** hồ sơ XU-118-AC-001 + KT-118-009 gồm links issue/run do Xu cung cấp (Run #1 FAILURE, Run #2 SUCCESS).
- **Kiểm thử CI / runtime:** của vòng này — NOT RUN (đang chờ Xu thực hiện theo plan).
- **Trạng thái Work:** BUILD/PILOT — XU NOT ACCEPTED, vòng kiểm thử độc lập IN PROGRESS.

## Entry 010 — Trạng thái liên bắt buộc cho vòng kiểm thử độc lập (chốt trước khi tay bắt đầu)
- **Thời gian:** 2026-11-20
- **Chốt freeze phiên bản:** Vibe sẽ không chủ động push/phát sinh bất kỳ thay đổi nào trong .github/workflows hay hồ sơ W118 khác ngoài Nhật ký này + hồ sơ kết quả kiểm thử của Xu.
- **Thứ tự ưu tiên theo KT-118-009:** T-01 (label w118-handoff) -> T-02/T-03 (ACK & actor test) -> T-04 (runtime diagnostics re-run Run #1) -> T-05 (đề xuất mở listener) -> T-06 (đối chiếu PR vs main).
- **Định nghĩa xong vòng kiểm thử:** có đủ 6 (hoặc có trường hợp SKIP có chú thích) kết quả thực thi với run URL + SHA, trạng thái mới củaeron STATUS.
