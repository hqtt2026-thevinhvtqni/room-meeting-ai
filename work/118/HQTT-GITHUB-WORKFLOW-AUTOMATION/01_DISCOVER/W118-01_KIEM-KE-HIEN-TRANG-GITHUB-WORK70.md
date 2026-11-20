# W118-01 — KIỂM KÊ HIỆN TRẠNG GITHUB REPO VÀ WORK 70

- **Work:** W118 — HQTT GitHub Workflow Automation (Issue #65)
- **Ngày:** 2026-11-20 (UTC+07)
- **Phương pháp:** Đọc trực tiếp GitHub contents trên main (GitHub API, base SHA 8675ad57); không dùng token, không ghi mutation nào ngoài tài liệu này.

## 1. Hiện trạng Work

- \`work/\` có 19 thư mục: 0001, 17, 21, 28, 70, 75, 76, 103, 112, 113, 115, 116, 117, 118, 300, 501, 502, 802001 (`1111` cần kiểm tra lại cách đánh số).
- Work 103 có CI riêng \`.github/workflows/work-103-rag-ci.yml\` (matrix Python 3.11/3.12, unit + gate corpus-aligned; gate FAIL 0.300 là thiết kế cố ý, report-only, chờ adjudication).

## 2. Danh mục workflow GitHub Actions hiện có

### w300-dashboard-ci.yml (W300 Dashboard CI)
- **Events:** push (main, path-filter dashboard W300), pull_request (cùng filter), workflow_dispatch.
- **Permissions:** contents: write, issues: write.
- **Jobs:** Bun toolchain; prettier autofix **tự commit về nhánh** (ci-bot), sau đó typecheck / lint / unit test / build.
- **Điểm đáng chú ý:** mỗi job FAIL tạo diagnostics issue qua \`gh issue create\` (log truncated 40KB — workaround vì tải job log cần admin). Đây là mẫu evidence-on-failure tiềm năng nhưng hiện **không liên kết Issue nguồn, không label, không chống trùng lặp** — dễ spam issue khi fail lặp lại.

### work70-preview-host.yml (Work 70 Preview Host Tests)
- **Events:** push (main, path-filter preview_host + đăng ký DOC + EVIDENCE), workflow_dispatch. KHÔNG có pull_request.
- **Permissions:** contents: read.
- **Jobs:** preview-host tests matrix ubuntu/windows (py_compile + unittest + smoke HTTP 18060), document-governance (validator DOC codes + EVIDENCE_REGISTER.json schema/state/dedupe).

## 3. Trạng thái CI theo hướng tác động của W118

- KHÔNG có workflow nào trigger theo **issue events** hay **merge**.
- KHÔNG có CI nào chạy theo path \`work/118/**\` → tài liệu W118 chưa được kiểm định tự động.
- Branch protection / required checks chưa kiểm chứng được ở mức API không auth (cần quyền admin — ghi ở gaps).
- pull_request CI chỉ có ở W300; Work 70, 103 chỉ chạy trên push → **review gate không có kiểm tra độc lập trước merge** ở đa số Work.

## 4. Đối chiếu Work 70 (chuẩn vòng đời)

- EVIDENCE_REGISTER.json (schema v1.1, state ∈ MISSING/RECORDED/VERIFIED/REJECTED, evidence_id duy nhất) đang được CI kiểm định — đây là **evidence contract chuẩn** mà W118 nên tái dùng cho Work Journal/Dashboard (câu hỏi thiết kế #8: một nguồn sự thật).
- Document governance validator kiểm mã DOC hợp lệ → chuẩn hóa tài liệu W118-02 có thể bám theo.

## 5. Danh mục GAPS (đầu ra W118-01)

| # | Gap | Ảnh hưởng | Phương án đề xuất (cho W118-02..05) |
|---|---|---|---|
| 1 | Không có trigger theo issue events | Mắt xích Issue → Job chưa tồn tại | W118-04: ROOM-HOP polling issues (bổ trợ hoặc thay webhook; webhook cần token/secret — ngoài phạm vi giai đoạn này) |
| 2 | Không có CI cho tài liệu W118 | Thiết kế W118 không được kiểm định | Bổ sung job nhẹ validate YAML/markdown W118 khi đẩy PR |
| 3 | w300 diagnostics issue không idempotent | Spam issue khi fail lặp | W118-05: state machine + label \`ci-diagnostic\` + dedupe theo (job, sha) |
| 4 | pull_request CI thiếu ở đa số Work | Review gate không có kiểm tra độc lập | W118-06: mở rộng PR trigger + required check tại cổng G3 |
| 5 | Prettier autofix tự commit + contents:write | Mutation thiếu actor identity rõ ràng (vi phạm provenance) | W118-02: quy ước commit/actor identity; cân nhắc PR thay vì push thẳng |
| 6 | Branch protection / required checks chưa xác nhận | Merge không bị chặn khi thiếu CI | Kiểm chứng ở W118-05 (cần quyền admin — BLOCKED nếu không có) |
| 7 | Evidence khi FAIL thiếu log gốc | Tải job log cần admin | Giữ mẫu "truncated log + issue" của w300 làm chuẩn tạm |
