# W118-03 — THIẾT KẾ CI VÀ EVIDENCE CONTRACT

- **Work:** W118 (Issue #65) · **Ngày:** 2026-11-20 (UTC+07) · **Trạng thái:** DRAFT chờ phản biện

## 1. Ma trận CI đề xuất

| Workflow | Trigger | Loại | Nội dung |
|---|---|---|---|
| \`w118-coordination-ci\` | push/PR theo \`work/118/**\` và \`.github/workflows/w118-*\` | lint/schema | Validate YAML W118, markdown hồ sơ, tính hợp lệ của label trạng thái |
| \`w300-dashboard-ci.yml\` (có sẵn) | push/PR/dispatch | chuẩn tham chiếu | Giữ nguyên; bổ sung idempotency diagnostics theo W118-05 |
| \`work70-preview-host.yml\` (có sẵn) | push main | chuẩn tham chiếu | Giữ làm chuẩn evidence contract |
| \`work-103-rag-ci.yml\` (có sẵn) | push nhánh 103 | domain | Giữ nguyên; gate FAIL cố ý nằm ngoài state machine sửa-lỗi |

- Xử lý Gap #2: CI W118 nhẹ — lint YAML + kiểm chứng markdown có tiêu đề/trạng thái/evidence entry; không thêm runtime nặng.

## 2. Evidence Contract (tái dùng chuẩn Work 70 — xử lý Gap #7, câu hỏi #8)

- **Một nguồn sự thật:** \`EVIDENCE_REGISTER.json\` schema v1.1 của Work 70 (evidence_id, state ∈ MISSING/RECORDED/VERIFIED/REJECTED, purpose, producer, timestamp UTC+07, branch/commit SHA, run URL, kết quả, limitations).
- Quy tắc ghi:
  1. KHÔNG ghi PASS khi thiếu (run URL + commit SHA + logs/metrics + exit code).
  2. Idempotency: \`EV-W118-<YYMMDD>-<NNN>\`, không trùng \`evidence_id\`.
  3. Evidence FAIL cũng ghi đầy đủ (state RECORDED + limitations); FAIL có chủ đích đánh dấu \`intentional: true\`.
  4. Document-governance validator của Work 70 kiểm schema — W118 tái sử dụng qua path-filter, không viết validator trùng lặp.
- Log khi FAIL: giữ mẫu "truncated log 40KB + issue" của w300 làm chuẩn tạm; việc tải log gốc cần admin được ghi là \`limitation\` (Gap #7).

## 3. Quyền CI

- W118 CI: \`contents: read\`, \`issues: write\` (chỉ cần diagnostics issue; không cần push về nhánh).
- KHÔNG dùng secrets/\`GITHUB_TOKEN\` vai trò ghi ngoài CI; token tạo mutation ngoài CI bị BLOCKED chờ G3 + W118-08 phê duyệt.
