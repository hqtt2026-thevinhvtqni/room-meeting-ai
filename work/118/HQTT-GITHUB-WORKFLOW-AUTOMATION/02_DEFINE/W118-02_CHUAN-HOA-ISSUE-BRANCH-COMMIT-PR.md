# W118-02 — CHUẨN HÓA ISSUE / BRANCH / COMMIT / PR

- **Work:** W118 — HQTT GitHub Workflow Automation (Issue #65)
- **Ngày:** 2026-11-20 (UTC+07) · **Trạng thái:** DRAFT chờ phản biện (W118-08)

## 1. Quy ước Issue (đầu vào của quy trình — không chỉ nơi ghi chú)

- Label trạng thái bắt buộc, một Issue chỉ mang đúng một label trạng thái:
  - \`status/queued\` → \`status/in-progress\` → \`status/in-review\` → \`status/accepted\`
  - Nhánh lỗi: \`status/blocked\` (ghi reason trong comment), \`status/failed-ci\` (tự sinh khi CI FAIL, có link run).
- Label vai trò: \`owner/vibe\`, \`owner/ka\`, \`owner/xu\` — ai là AI/vai trò phụ trách.
- Label loại: \`type/feature\`, \`type/docs\`, \`type/fix\`, \`type/debt\`.
- Issue thuộc dạng **FAIL có chủ đích** (gate chờ adjudication, ví dụ gate 0.300 ở W103) phải gắn \`type/debt\` + \`status/blocked\`; state machine KHÔNG sinh nhiệm vụ sửa lặp cho debt đã ghi nhận (nguyên tắc idempotency, xem W118-05).
- Mọi Issue thực thi phải có mục "Tiêu chí hoàn thành" — thiếu coi như chưa thể nhận việc.

## 2. Quy ước Branch

- Nhánh làm việc: \`work/<số>-<tên-ngắn>\`, VD \`work/118-github-workflow-automation\` (đang dùng đúng quy ước).
- Một Issue = một nhánh (hoặc một cụm Issue cùng phạm vi được ghi rõ trong Issue).
- Không push trực tiếp vào \`main\` từ AI executor; mọi thay đổi đi qua PR (xử lý Gap #5).

## 3. Quy ước Commit / Provenance (xử lý Gap #5)

- Tiêu đề commit: \`<type>(w<số>): <mô tả ASCII> (refs #<issue>)\` — tương thích chuẩn hiện \`docs(w118): ... (refs #65)\`.
- Body commit (bắt buộc khi là mutation hệ thống): \`actor:\`, \`intent:\`, \`evidence:\` (run URL / SHA / file đọc-ghi).
- Actor identity: commit do AI phải ghi rõ actor trong body; không mạo danh human. Prettier autofix giữ \`ci-bot\` nhưng kèm link run trong body commit.
- Idempotency: mutation theo Issue phải kiểm tra trạng thái hiện tại trước khi ghi; key = \`<issue>#<bước>\`.

## 4. Quy ước Pull Request

- PR phải: liên kết Issue (\`Closes #<số>\` hoặc \`Refs #<số>\`), liệt kê checklist acceptance criteria, ghi evidence (CI run URL, commit SHA).
- PR chỉ được merge khi: (a) required checks PASS, (b) reviewer độc lập phê duyệt (không phải actor tự review), (c) đạt các cổng G theo W118-06.
- CI PASS không tự merge (nguyên tắc README W118).

## 5. Templates đề xuất (khi triển khai — sau G3)

- \`.github/ISSUE_TEMPLATE/work-execution.md\`: mục tiêu / tiêu chí hoàn thành / owner / loại / yêu cầu evidence.
- \`.github/PULL_REQUEST_TEMPLATE.md\`: Issue liên kết / thay đổi / evidence / checklist cổng.
