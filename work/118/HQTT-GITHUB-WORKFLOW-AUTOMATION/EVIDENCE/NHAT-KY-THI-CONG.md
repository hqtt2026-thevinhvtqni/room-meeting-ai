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
