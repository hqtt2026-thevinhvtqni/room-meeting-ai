# W118-01 — KIỂM KÊ HIỆN TRẠNG GITHUB (DISCOVERY)

- **Work:** W118 — HQTT GitHub Workflow Automation
- **Ngày:** 2026-11-20
- **Phương pháp:** Đọc trực tiếp GitHub API/contents của repo `hqtt2026-thevinhvtqni/room-meeting-ai` tại main (head `8675ad5`); đọc toàn bộ `.github/workflows/`; liệt kê branches và thư mục `work/`.
- **Trạng thái:** DONE (docs-only) — đây là kiểm kê quan sát, không có kiểm thử runtime nào.

## 1. Workflows hiện có (2)

### 1.1 `.github/workflows/w300-dashboard-ci.yml` — "W300 Dashboard CI"
- Trigger: `push` (main, path-filtered vào dashboard W300 + chính workflow), `pull_request` (cùng path filters), `workflow_dispatch`.
- Permissions: `contents: write`, `issues: write`. Concurrency group theo ref, cancel-in-progress. Timeout 20 phút.
- Jobs: 1 job (typecheck tsc, eslint, vitest, production build bằng Bun).
- Cơ chế đặc biệt cần lưu ý khi thiết kế W118:
  - **Prettier autofix rồi commit/push lại từ CI** (bot `w300-ci-bot`) → mutation do CI tạo ra, GITHUB_TOKEN push sẽ không tự kích hoạt workflow (đã ghi nhận ở Work 300) → có rủi ro vòng phản hồi im lặng.
  - **Chẩn đoán lỗi đăng lên issue** dùng `gh issue create` + `GH_TOKEN` (vì job logs cần quyền admin) → đây là mẫu "failure handling" duy nhất đang tồn tại, không có actor/retry limit.

### 1.2 `.github/workflows/work70-preview-host.yml` — "Work 70 Preview Host Tests"
- Trigger: `push` (main, path-filtered rất rộng vào cả docs W70), `workflow_dispatch`. **Không có `pull_request`.**
- Permissions: `contents: read`.
- Jobs: (1) preview host tests matrix ubuntu/windows gồm compile + unittest + materialize host thật trên Windows; (2) document governance tests — py_compile validator, chạy validator document codes và validate JSON evidence register (schema, uniqueness, state enum).

## 2. Gaps đối chiếu với 8 câu hỏi thiết kế (BB-118-001 §4)

| # | Câu hỏi | Hiện trạng | Gap |
|---|---|---|---|
| 1 | Issue event kích hoạt gì, actor nào | **KHÔNG có workflow lắng nghe issue event** | Không có event-driven fix |
| 2 | Xác nhận đúng AI nhận việc | Không có cơ chế; chỉ dựa assignee GitHub | Không có ACK/evidence nhận việc |
| 3 | Quy ước Issue↔Branch↔Commit | Không chuẩn hóa; 77 branches với tên không theo mẫu (thấy tự do, `work/…`, `fix/…`, ad-hoc) | Cần quy ước + kiểm tra ở CI hoặc bot |
| 4 | CI push/PR, lưu log/SHA/exit code | 2 workflow push-only trên main (w300 thêm PR); log chỉ nằm trong Actions (tải cần admin); không có evidence hồng bất biến ngoài diagnostics issue | Không có evidence contract |
| 5 | CI FAIL → ai sửa, retry limit | Chỉ có patterns đăng issue; không có routing actor, không có retry bound | Không có state machine fail |
| 6 | CI PASS → review/nghiệm thu | Không có điều kiện review tự động nào | Không có gate matrix |
| 7 | Webhook/API về ROOM-HOP | KHÔNG tồn tại; không có secrets/webhook nào cấu hình qua workflows | Cần thiết kế auth/replay/idempotency từ 0 |
| 8 | Đồng bộ Journal/Dashboard, không trùng nguồn sự thật | Work 70 có EVIDENCE_REGISTER.json (schema states MISSING/RECORDED/VERIFIED/REJECTED) và validator; Dashboard cập nhật thủ công | Nên tái dùng contract Work 70, không tạo nguồn thứ hai |

## 3. Hiện trạng cấu trúc liên quan
- Thư mục `work/` trên main: 19 Work (0001, 103, 1111, 112, 113, 115, 116, 117, 118, 17, 21, 28, 300, 501, 502, 70, 75, 76, 802001).
- Branches: 77 nhánh, quy ước đặt tên không nhất quán; nhiều Work dùng nhánh riêng, một số Work (116, 118) nằm thẳng trên main.
- Hệ quả W118: mọi hồ sơ W118 giai đoạn DISCOVER/DEFINE được commit thẳng main (docs-only), đúng như W116 đã làm; pipeline mutation thật chỉ thử nghiệm sau G3.

## 4. Kiến nghị cho W118-02..07 (nháp, chờ phản biện)
1. **Event orchestration nhỏ nhất khả thi:** start với GitHub-native trước (workflow `issues`/`issue_comment`/`pull_request` events + labels một mục đích), không viết webhook server ngay — giảm bề mặt xác thực/replay cần thiết kế.
2. **Evidence contract:** tái dùng mẫu schema của Work 70 (EVIDENCE_REGISTER.json + validator) thay vì chế contract mới; mỗi run CI ghi một evidence row (run_id, SHA, job, exit code, timestamp, actor).
3. **Branch/commit convention:** thêm job lint-nhẹ (docs-only) kiểm tra pattern branch/commit-message khi có PR, không block docs push trên main giai đoạn đầu.
4. **Failure path:** tiếp tục pattern "diagnostics lên issue" của w300, bổ sung assign + label + retry counter (cap 2–3 lần, sau đó BLOCKED có người chịu trách nhiệm).
5. **Không auto-merge:** dù CI PASS, merge chỉ qua PR review của actor được chỉ định (vẫn khớp nguyên tắc 00_ROOT §3).
6. **Di sản w300 cần giám sát:** autofix-commit-loop từ CI — phải là design item của W118-05 (idempotency/anti-loop), không nhân rộng trước khi có giới hạn.

## 5. Bế tắc & giới hạn hiện tại
- Job logs của Actions chỉ đọc được khi có quyền admin (đã biết từ Work 300) → bằng chứng CI phải lấy từ artifacts/diagnostics issue/summary, không từ raw log.
- Chưa kiểm kê được secrets/webhook cài ở cấp repo settings (API read-only không thấy) → phần này ghi BLOCKED cần Vinh xác nhận qua UI.
- Không có bất kỳ kiểm thử runtime nào trong giai đoạn này; không có PASS nào.

## 6. Bằng chứng
- Workflows dir: `.github/workflows/` (2 file, đọc toàn bộ nội dung tại SHA `8675ad5`).
- Danh sách branches (77, page 1/100) và `work/` dirs (19) tại cùng SHA.
- W300 lessons: Nhật ký Work 300 2026-11-15 (run #7 root cause, GITHUB_TOKEN không trigger).
