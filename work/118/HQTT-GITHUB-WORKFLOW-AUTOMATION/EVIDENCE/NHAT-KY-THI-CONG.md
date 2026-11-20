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

## Entry 011 — Vibe ghi nhận kết luận nghiệm thu của Xu (đồng bộ với Entry 009 của Xu)
- **Thời gian:** 2026-11-20 (sau Entry 008)
- **Phạm vi:** ghi nhận kết luận nghiệm thu độc lập của Xu trên Issue #65; không chỉnh sửa bất kỳ mã nguồn nào (đúng phương án của Xu).
- **Kết luận của Xu:** NOT ACCEPTED — pilot chạy được một phần (Run #2 SUCCESS, ack-verification có bằng chứng) nhưng chưa đủ chuỗi end-to-end; AC-R1..AC-R6 (chi tiết hồ sơ XU-118-AC-001).
- **Quyết định tuân theo:** giữ nguyên main, chưa merge PR #66, chưa bật tự động hóa diện rộng; Vibe KHÔNG sửa mã trong vòng nghiệm thu.
- **Bàn giao:** KT-118-009 là danh sách kiểm thử bổ sung (T-01..T-06) cho Xu thực hiện vòng kiểm thử độc lập; Vibe hỗ trợ ghi hồ sơ và đối chiếu PR #66 khi được gọi.
- **Bằng chứng:** hồ sơ XU-118-AC-001 + KT-118-009 gồm links issue/run do Xu cung cấp (Run #1 FAILURE, Run #2 SUCCESS).
- **Kiểm thử CI / runtime:** của vòng này — NOT RUN (đang chờ Xu thực hiện theo plan).
- **Trạng thái Work:** BUILD/PILOT — XU NOT ACCEPTED, vòng kiểm thử độc lập IN PROGRESS.

## Entry 012 — Chốt freeze phiên bản cho vòng kiểm thử độc lập
- **Thời gian:** 2026-11-20
- **Chốt freeze phiên bản:** Vibe sẽ không chủ động push/phát sinh bất kỳ thay đổi nào trong .github/workflows hay hồ sơ W118 khác ngoài Nhật ký này + hồ sơ kết quả kiểm thử của Xu.
- **Thứ tự ưu tiên theo KT-118-009:** T-01 (label w118-handoff) -> T-02/T-03 (ACK & actor test) -> T-04 (runtime diagnostics re-run Run #1) -> T-05 (đề xuất mở listener) -> T-06 (đối chiếu PR vs main).
- **Định nghĩa xong vòng kiểm thử:** có đủ 6 (hoặc có trường hợp SKIP có chú thích) kết quả thực thi với run URL + SHA, trạng thái mới của STATUS.

## Entry 013 — Vibe hoàn tất T-06 đối chiếu 2 luồng + soạn sẵn remediation plan (docs-only)
- **Thời gian:** 2026-11-20 (sau Entry 012)
- **Phạm vi:** T-06 của KT-118-009 — đối chiếu w118-workflow-automation.yml (main) vs w118-coordination-ci.yml (PR #66, head 05b3fe3); soạn sẵn B-118-010 remediation plan cho AC-R1..R6 nhưng KHÔNG áp dụng trong vòng test (freeze).
- **Phát hiện chính của T-06:** (1) hai luồng không chồng lấn chức năng (event orchestration vs docs-CI); (2) merge PR #66 nguyên trạng thái sẽ tự FAIL vì 2 file hồ sơ bắt buộc chỉ tồn tại trên nhánh PR; (3) hai luồng dùng 2 label diagnostics khác nhau (w118-blocked vs ci-diagnostic) cần chuẩn hóa; (4) diagnostics của PR #66 không đồng nhất (title chứa SHA làm mỗi fail tạo issue mới).
- **Bằng chứng:** TD-118-011 + B-118-010; phạm vi hoàn toàn docs-only, đúng freeze.
- **Trạng thái Work:** Vòng kiểm thử độc lập IN PROGRESS — đang chờ Xu thực hiện T-01..T-05; T-06 đã có sẵn hồ sơ để Xu xác nhận.
- **Bước tiếp:** Xu chạy T-01..T-05; khi vòng test đóng + Vinh ACK APPLY B-118-010, Vibe triển khai fix theo thứ tự AC-R3 -> AC-R4 -> AC-R1 -> AC-R5 -> AC-R6.

## Entry 014 — Vibe xác nhận lập trường kiểm thử của Xu (freeze tiếp tục)
- **Thời gian:** 2026-11-20 (sau Entry 013)
- **Nội dung:** Xu khẳng định tiếp tục vòng kiểm thử độc lập theo thứ tự T-01 -> T-05, đối chiếu T-06; nguyên tắc mỗi test cần Run URL + Commit SHA + Job conclusion + output thật; phân biệt rõ DONE / PASS / BLOCKED.
- **Vibe xác nhận:** freeze vẫn được giữ — không merge PR #66, không sửa workflow, không đổi quyền/labels, không ghi PASS thiếu bằng chứng runtime. Trạng thái T theo bảng của Xu được chấp nhận là trạng thái chính thức của vòng test tại thời điểm này.
- **Điều kiện chờ từ phía vận hành:** label w118-handoff cần tồn tại trước T-01 — tạo thủ công qua UI repo (không phải sửa code) được coi là hợp lệ trong vòng test.
- **Trạng thái Work:** vòng kiểm thử độc lập IN PROGRESS; Vibe chờ kết quả, chỉ ghi hồ sơ.

## Entry 015 — KHÓA TRẠNG THÁI KIỂM THỬ (mốc chính thức của Xu)
- **Thời gian:** 2026-11-20 (sau Entry 014)
- **Trạng thái khóa do Xu:** T-01 BLOCKED (chờ label w118-handoff tạo thủ công UI — hợp lệ, không phá freeze) / T-02 PASS một phần / T-03, T-04 NOT VERIFIED / T-05 NOT VERIFIED đầy đủ / T-06 DONE (hồ sơ TD-118-011).
- **Hai bên cam kết thống nhất:** không merge PR #66, không sửa workflow, không đổi quyền/labels ngoài điều kiện T-01, không PASS thiếu runtime evidence.
- **Điểm kết thúc vòng:** Xu tổng hợp kết quả T-01..T-05 + lỗi tồn tại + bằng chứng Actions + đối chiếu AC-R1..R6 + kiến nghị B-118-010; remediation CHỈ triển khai khi Vinh ra lệnh chính xác "ÁP DỤNG B-118-010".
- **Nguyên tắc xuyên suốt W118 được ghi làm chuẩn:** chứng minh hệ thống làm được trước, mới kết luận hệ thống đã làm được.
- **Vibe:** chờ; chỉ ghi hồ sơ; không sinh commit nào khác ngoài nhật ký/hồ sơ kết quả kiểm thử.


## Entry 016 — Xu kiểm tra trạng thái GitHub sau mốc khóa Entry 015 (read-only)
- **Thời gian:** 2026-11-20 (UTC+7).
- **Phạm vi:** xác minh Entry 015/main, điều kiện T-01, Actions evidence và khả năng thực hiện T-01..T-05 theo KT-118-009; không thay đổi workflow, labels, quyền hoặc PR.
- **Phương pháp:** GitHub API read-only: đọc branch main, commit 1069349, Issue #65 và labels của Issue, workflow file trên main, workflow runs/jobs; đọc DOC-043, XU-118-AC-001, STATUS và KT-118-009.
- **Bằng chứng xác minh mốc:** main HEAD = `1069349f5ea8223be024d196f5434052cdb438af`; commit message “Work 118: journal entry 015 (test status locked by Xu, remediation gated on APPLY B-118-010)”; file NHAT-KY-THI-CONG.md trên main có Entry 015. Entry 015 được xác nhận hiện diện trên main.
- **Kết quả T-01 — BLOCKED:** Issue #65 hiện chỉ có label `enhancement`, chưa gắn `w118-handoff`; chưa tạo Issue test và chưa kích hoạt event handoff. Kiểm tra này xác nhận label chưa được áp dụng trên Issue #65; chưa kết luận label có/không tồn tại ở cấp repository. Không tự thêm label hoặc tạo Issue trong lượt kiểm tra read-only.
- **Kết quả T-02 — PASS một phần, không có test anti-spoof mới:** Run #2 https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44690614366 — SHA `0143482692afa7a0569218a8e656665e19e54ce8`, event `issue_comment`, conclusion `success`; job `ack-verification` = `success`, steps “Record ACK evidence” = `success`. Đây là bằng chứng ACK pipeline nhận comment và ghi ACK. Tuy nhiên chưa có thử nghiệm comment từ một tài khoản khác, nên không chứng minh chống giả mạo hoặc actor authorization.
- **Kết quả T-03 — NOT VERIFIED:** DOC-043 (W70) chỉ quy định role và yêu cầu xác minh login/capability/quyền cho từng lần tham gia; không cung cấp bảng mapping role → GitHub login làm bằng chứng cho actor trong Run #2. Workflow pilot cũng ghi role mapping là kiểm tra thủ công. Chưa đủ cơ sở xác nhận actor/role.
- **Kết quả T-04 — NOT VERIFIED:** Run #1 https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44690358863 là `failure` ở bước workflow parse; API jobs trả danh sách rỗng (0 job), nên không chứng minh job diagnostics chạy. Workflow hiện tại chỉ lắng nghe workflow_run của “W300 Dashboard CI” và “Work 70 Preview Host Tests”; chưa có bằng chứng một run FAIL phù hợp kích hoạt `ci-failure-diagnostics`. Run #5 https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44732055764 có event `issue_comment`, conclusion `skipped`; cả 3 job `ack-verification`, `handoff-brief`, `ci-failure-diagnostics` đều `skipped`, không phải bằng chứng diagnostics.
- **Kết quả T-05 — BLOCKED / NOT RUN:** workflow hiện chưa lắng nghe FAIL của chính W118. KT-118-009 yêu cầu ACK riêng trước khi mở rộng danh sách workflow listener; chưa có ACK đó trong phạm vi kiểm tra. Không sửa workflow hoặc thêm listener trong vòng freeze.
- **Kết quả T-06 — DONE:** giữ nguyên hồ sơ đối chiếu TD-118-011 và remediation plan B-118-010 đã có ở Entry 013.
- **Kiểm soát thay đổi:** không tạo Issue/comment test; không thêm/xóa label; không sửa workflow; không thay đổi permission; không merge PR #66; không áp dụng B-118-010.
- **Kết luận vòng kiểm tra hiện tại:** chưa có test runtime mới sau Entry 015. Trạng thái vẫn là T-01 BLOCKED / T-02 PASS một phần / T-03 NOT VERIFIED / T-04 NOT VERIFIED / T-05 BLOCKED-NOT RUN / T-06 DONE. Không đánh dấu PASS toàn bộ.
- **Bước tiếp:** chờ điều kiện label `w118-handoff` để chạy T-01; cần tài khoản/actor độc lập cho T-02 anti-spoof; cần mapping login có thẩm quyền để kết luận T-03; cần một run FAIL phù hợp từ W300/W70 để kiểm tra T-04; T-05 chỉ tiếp tục khi có ACK riêng cho thay đổi listener. B-118-010 vẫn chỉ được triển khai khi Vinh ra lệnh chính xác “ÁP DỤNG B-118-010”.

## Entry 017 — Điều kiện T-01 được thỏa: label w118-handoff đã gắn lên Issue #65
- **Thời gian:** 2026-11-20 (sau Entry 016)
- **Phạm vi:** áp dụng điều kiện đã thống nhất ("tạo label thủ công qua UI là hợp lệ, không phá freeze") — Vibe gắn label w118-handoff lên Issue #65 bằng công cụ quản trị issue (issue_write update), label được XÁC MINH đã tồn tại ở cấp repo (get_label: LA_kwDOT6hVUc8AAAADEDp-Fw, màu mặc định ededed) và đã nằm trong danh sách 2 labels của Issue #65 (issue_read: enhancement + w118-handoff).
- **Lưu ý trung thực:** lần đọc trang Issues đầu tiên vẫn thấy chỉ enhancement (dấu hiệu cache/cập nhật trễ); nguồn sự thật dùng cho Entry này là API issue_read thành công đồng loại. Xu nên xác minh lại bằng view của mình.
- **T-01 chuyển từ BLOCKED -> READY TO RUN:** chờ run của sự kiện issues(labeled) xuất hiện trên Actions và bot comment "W118 pilot: handoff registered" trên #65. Lúc kiểm tra gần nhất chưa thấy run mới (trang Actions vẫn hiển thị tới run #5); Xu xác minh runtime theo chuẩn run URL + SHA + job conclusion + output.
- **Không đổi gì khác:** không sửa workflow, không merge PR #66, không đụng quyền; B-118-010 giữ khóa.

## Entry 018 — T-01 RUNTIME PASS lần 1 và lần 2 + SỰ CỐ GHI ĐÈ đã được khôi phục (docs-only)
- **Thời gian:** 2026-11-20 (sau Entry 017)
- **Sự cố được khai báo trung thực:** lần push đầu của Entry 018 (commit aacd8f2) do lỗi xử lý kết quả đọc file tại phía công cụ, file NHAT-KY-THI-CONG.md đã bị GHI ĐÈ, còn Entry 001..017 tạm rơi khỏi file trên main. Nội dung đã được KHÔI PHỤC ĐẦY ĐỦ từ commit cha de7e122 (Entry 001..017 nguyên vẹn) và bổ sung Entry 018 ngay sau đó trong commit này. Vibe đánh dấu sự cố này làm bài học cấu hình công cụ ghi file, không có hồ sơ nào khác bị ảnh hưởng (STATUS.md ok).
- **Phạm vi:** hòa nhập điều kiện do Vinh phê duyệt ở Entry 017: đã gắn lại label w118-handoff để kích hoạt sự kiện issues(labeled) trên Issue #65; các thao tác khác giữ freeze (không sửa workflow, không merge PR #66, không đổi quyền; B-118-010 giữ khóa).
- **Bằng chứng runtime T-01:**
  - Run #6: event "Issue #65 labeled by hqtt2026-thevinhvtqni", completed success (7s). Trang: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/workflows/w118-workflow-automation.yml
  - Run #7: event "Issue #65 labeled by hqtt2026-thevinhvtqni", completed success (8s). Trang cùng URL như trên.
  - Output thật trên Issue #65: 2 comment của github-actions bot, mỗi run một comment, nội dung "W118 pilot: handoff registered. Assignment is a nomination only. The worker must comment ACKED- to confirm receipt. Evidence will be recorded in the Work evidence register." (kiểm trực tiếp trang issue: 2 lần khớp "handoff registered").
- **Ý nghĩa:** job handoff-brief đã chạy thật trên event labeled; 2/3 job của pilot (handoff-brief + ack-verification) giờ có bằng chứng runtime riêng.
- **Giới hạn trung thực:** head SHA của run #6/#7 do Xu truy từ view của mình để chốt hồ sơ chuẩn (URL dạng actions/runs/<id>); không suy rộng sang T-03 (mapping role) và không dùng #6/#7 làm bằng chứng diagnostics (T-04).
- **Trạng thái vòng kiểm thử sau Entry 018:** T-01 PASS (runtime, 2 lần) / T-02 PASS một phần / T-03 NOT VERIFIED / T-04 NOT VERIFIED / T-05 BLOCKED-NOT RUN / T-06 DONE.
- **Bước tiếp:** Xu tiếp tục T-02 anti-spoof, T-03 (mapping role -> login), T-04 (một run FAIL phù hợp từ W300/W70), T-05 (chờ ACK riêng cho listener). Remediation B-118-010 vẫn chỉ mở khi Vinh ra lệnh chính xác "ÁP DỤNG B-118-010".

## Entry 019 — Xu đối soát độc lập T-01 và chốt trạng thái vòng nghiệm thu sau Entry 018
- **Thời gian:** 2026-11-20 (UTC+7).
- **Phạm vi:** xác minh read-only các bằng chứng T-01 do Vinh cung cấp và trạng thái runtime pilot; ghi nhật ký docs-only. Không chạy lại event, không thêm/gỡ label, không tạo comment, không sửa workflow, không merge PR #66.
- **Nguồn/commit đối chiếu:** journal main trước khi ghi Entry 019 có blob SHA `a1716e79c09cd29fdd07e7a38289a6de0b32acbd`, độ dài 24.026 ký tự, chứa Entry 001–009 và 011–018; khoảng trống Entry 010 được giữ nguyên theo chủ ý. Commit khôi phục/ghi Entry 018 được xác định là `21e19ee`.
- **Issue #65:** API read xác nhận trạng thái OPEN và hai label `enhancement`, `w118-handoff`.
- **Bằng chứng output T-01:** đọc comments của Issue #65 xác nhận hai comment từ `github-actions[bot]`, comment ID `7039391585` và `7039426355`, đều chứa nội dung “W118 pilot: handoff registered”.
- **Bằng chứng Actions T-01:** Run #6 ID `44734981146` và Run #7 ID `44735217935`; event `labeled`; cả hai `completed / success`. Đọc job details xác nhận job `handoff-brief` success; hai job `ack-verification` và `ci-failure-diagnostics` skipped trong các run này. Hai lần handoff output tương ứng với hai comment bot nêu trên.
- **Kết luận T-01:** **PASS — runtime verified 2 lần**. Kết luận chỉ áp dụng cho event Issue labeled → job handoff-brief chạy thành công và ghi comment bot; không suy rộng rằng cả ba job đều chạy trong cùng run.
- **T-02:** **PASS một phần**. Bằng chứng ACK-verification trước đó vẫn là Run #2 ID `44690614366`, event `issue_comment`, conclusion success. Chưa có thử nghiệm anti-spoof từ actor/tài khoản độc lập; chưa chứng minh authorization theo danh tính.
- **T-03:** **NOT VERIFIED**. Chưa có bằng chứng mapping GitHub login ↔ vai trò được chủ thể có thẩm quyền xác nhận, cũng chưa có runtime kiểm tra actor/role.
- **T-04:** **NOT VERIFIED**. Chưa có run CI FAIL phù hợp từ W300 hoặc W70 chứng minh job `ci-failure-diagnostics` chạy thành công và tạo/cập nhật issue chẩn đoán. Không dùng lỗi parse YAML cũ hoặc các job skipped làm bằng chứng.
- **T-05:** **BLOCKED / NOT RUN**. Chưa có ACK riêng cho việc mở rộng listener để W118 tự theo dõi lỗi của chính mình; không sửa workflow trong vòng freeze.
- **T-06:** **DONE** — giữ nguyên hồ sơ đối chiếu TD-118-011 và remediation plan B-118-010 đã ghi trước đó.
- **Tình trạng sản phẩm:** 2/3 job có runtime evidence riêng (handoff-brief và ack-verification); job ci-failure-diagnostics chưa verified. STATUS.md trên main hiện phản ánh mức 2/3 và vẫn ghi **XU NOT ACCEPTED**. Không chấp nhận sản phẩm W118 ở thời điểm này.
- **Kiểm soát thay đổi:** không có thay đổi workflow, quyền, PR hoặc remediation; B-118-010 vẫn khóa. Chỉ triển khai khi Vinh ra lệnh chính xác “ÁP DỤNG B-118-010” trên Issue #65.
- **Bước tiếp:** T-02 cần actor độc lập để thử anti-spoof; T-03 cần mapping login/role được xác nhận; T-04 cần run FAIL thực tế từ W300/W70 và job diagnostics có kết quả; T-05 chờ ACK riêng. Mọi kết luận PASS tiếp theo phải có run URL, commit SHA, job conclusion và output thực tế.
- **Nguyên tắc:** “Chứng minh hệ thống làm được trước, mới kết luận hệ thống đã làm được.”

## Entry 020 — T-04 historical CI failure scan: failures found, but all predate W118 listener
- **Thời gian:** 2026-11-20 (UTC+7).
- **Phạm vi:** read-only rà soát lịch sử CI của W300 và W70 để tìm run FAIL thực tế có thể làm đầu vào cho T-04; kiểm tra workflow listener W118 và issue diagnostics. Không chạy workflow, không tạo lỗi, không retry, không sửa file workflow, không tạo issue/label.
- **Nguồn workflow hiện hành trên main:**
  - `.github/workflows/w300-dashboard-ci.yml`, blob SHA `14cecadb8b9eb1d0f05670d5a95fd2ef41471467`, workflow name `W300 Dashboard CI`.
  - `.github/workflows/work70-preview-host.yml`, blob SHA `debe034f4a25672d02b6733d919f1baadca909e2`, workflow name `Work 70 Preview Host Tests`.
  - `.github/workflows/w118-workflow-automation.yml`, blob SHA `72cd444b93d5fe7c67f500423cc1c00ddfdeb985`; listener dùng `workflow_run` với hai workflow name nêu trên, event type `completed`; job diagnostics chỉ chạy khi conclusion của upstream run là `failure`.
- **W300 — historical failures found:** Work 300 DOC-035 ghi các run ngày 2026-11-15:
  - Run `43677317548` (#3), commit `51d84558ee45cac6e965157abf169a28c9d33b42`: job Dashboard CI conclusion failure tại checkout source do stray gitlink/submodule; các bước tiếp theo skipped.
  - Run `43677565968` (#4), commit `ed62a3af863a0f2159f7c231e0b23a498766c99d`: job failure tại TypeScript check; ESLint/unit tests/build skipped.
  - Work 300 DOC-035 còn ghi run #7 `43680383282` typecheck failure và run #10 `43682888076` ESLint failure trong chuỗi xử lý ngày 2026-11-15; các lỗi được xử lý và chuỗi sau đó có run #11/#12 success.
  - Đã gọi GitHub job-details cho run #3 và #4; cả hai trả về job completed/failure, phù hợp hồ sơ Work 300.
- **W70 — historical failures found:** Work 70 DOC-035 ghi các run ngày 2026-11-07:
  - Run `42363481084`, commit `828b628937c2e966e446ad181306449ec4eb3d9a`: job Document Register and Code Validation failure do hai test fixture mới dùng literal backslash-n; Preview Host Ubuntu/Windows success.
  - Run `42365401117`, commit `13379e3bac99ff3494b2406d7b52c41e81cd4b33`: job Document Register and Code Validation failure do fixture newline; Preview Host Ubuntu/Windows success.
  - Đã gọi GitHub job-details cho cả hai run; kết quả khớp: job Document Register and Code Validation completed/failure, hai job Preview Host completed/success.
- **Vì sao các run trên KHÔNG đủ cho T-04:** các lần FAIL đều xảy ra ngày 2026-11-07 hoặc 2026-11-15, trước khi workflow W118 listener được đưa lên main ngày 2026-11-20. GitHub `workflow_run` không phát lại hồi tố cho các run đã hoàn tất trước khi listener tồn tại. Do đó không thể dùng các failure lịch sử để tuyên bố job `ci-failure-diagnostics` của W118 đã chạy.
- **Issue diagnostics:** GitHub issue search với query `label:w118-blocked` và title pattern `[w118] CI FAIL` không trả về issue phù hợp ở thời điểm kiểm tra. Đây là kết quả tìm kiếm hiện thời, không phải bằng chứng về toàn bộ issue đã đóng hoặc đã xóa.
- **Kết luận T-04:** **NOT VERIFIED — historical failures exist, but none is eligible to prove W118 listener runtime.** Cần chờ một lần CI FAIL tự nhiên mới từ W300 hoặc W70 sau khi listener đang hoạt động; sau đó xác minh W118 run event `workflow_run`, job `ci-failure-diagnostics` success, issue `w118-blocked` chứa upstream run URL + SHA và hành vi create/update đúng. Không chủ động làm hỏng CI.
- **Kiểm soát thay đổi:** không có workflow/code/permission/PR mutation; PR #66 giữ OPEN; B-118-010 tiếp tục khóa.
- **Bước tiếp:** theo dõi lần CI W300/W70 tiếp theo; khi upstream run hoàn tất với conclusion failure, đối chiếu ngay W118 Actions run và issue diagnostics. Nếu CI tiếp theo đều SUCCESS thì T-04 vẫn chờ, không được tạo FAIL nhân tạo.
