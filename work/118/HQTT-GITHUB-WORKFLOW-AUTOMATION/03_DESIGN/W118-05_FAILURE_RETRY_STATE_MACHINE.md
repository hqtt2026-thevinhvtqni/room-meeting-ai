# W118-05 — THIẾT KẾ FAILURE / RETRY / IDEMPOTENCY (STATE MACHINE)

- **Work:** W118 (Issue #65) · **Ngày:** 2026-11-20 (UTC+07) · **Trạng thái:** DRAFT chờ phản biện

## 1. State machine

\`\`\`
status/queued ──> status/in-progress ── CI PASS ──> status/in-review ── review OK ──> status/accepted
     │                  │                                                 │
     │                  └─ CI FAIL ──> status/failed-ci ── fix ── back to in-progress
     │                                                  (tối đa 2 retry)
     └─ thiếu acceptance criteria / phụ thuộc ──> status/blocked
\`\`\`

- \`accepted\` KHÔNG tự động merge — merge phải qua cổng G theo W118-06.

## 2. Retry policy

- Lỗi thực thi (CI FAIL không phải debt cố ý): tối đa **2 lần** tự sửa bởi actor phụ trách; hết hạn → \`status/blocked\` + comment reason + ghi debt.
- Lỗi cấu hình/permission (ví dụ thiếu admin để tải job log, branch protection): KHÔNG retry; ghi \`limitation\` vào evidence, \`status/blocked\` + phân công vai trò có quyền.
- Mọi retry ghi bản ghi: lần thử, commit SHA, run URL, kết quả; key idempotency \`<issue>#<bước>#<attempt>\`.

## 3. Idempotency (xử lý Gap #3)

- Trước khi tạo diagnostics issue: tra cứu issue mở có cùng (job, commit SHA, run URL); có rồi thì chỉ comment, không tạo mới.
- State machine đọc trạng thái hiện tại TRƯỚC KHI ghi (labels + EVIDENCE_REGISTER) — không chuyển trạng thái lặp.

## 4. Timeout / Không có event

- Phiên polling không thấy event mới → không ghi state (tránh nhiễu).
- Issue ở \`in-progress\` quá hạn không có commit mới → ROOM-HOP đánh dấu nghi vấn và hỏi lại owner (policy phiên, không phải auto-CI).
