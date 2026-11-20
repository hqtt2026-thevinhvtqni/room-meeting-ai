# QC-118-002 — QUY ƯỚC ISSUE / BRANCH / COMMIT / PR — WORK 118

- **Work:** W118 — HQTT GitHub Workflow Automation
- **Ngày:** 2026-11-20
- **Trạng thái:** DRAFT (nháp phục vụ phản biện) — CHƯA áp dụng强制 scope toàn repo, chỉ ràng buộc các flow vận hành đầu tiên.

## 1. Quy ước Issue
- Mỗi Work chính có ít nhất 1 Issue tracking (mẫu: #65 cho W118). Title bắt đầu bằng mã Work: `W118 — <mô tả ngắn>`.
- Nhãn quản trị bổ sung một mục đích duy nhất:
  - `w118-handoff` — issue cần một tác nhân nhận việc;
  - `w118-blocked` — issue đang FAIL/BLOCKED, chờ actor chỉ định;
  - `w118-retro` — issue ghi nhận sự cố/process sau khi xử lý xong.
- Labels phải được tạo trước khi bật flow (cấu hình repo-level), không tạo label lúc runtime trong pilot.
- Mọi issue event liên quan điều phối phải có comment bằng chứng do actor ghi (không phải bot tự suy).

## 2. Quy ước Branch
- Nhánh làm việc theo Work: `work/<số>-<kebab-case-tên>` (đã là pattern đa số: 28, 32, 103...). Nhánh phụ trợ: `work/<số>/ Nhánh nhỏ kebab` chỉ dùng khi cần tách topic trong cùng Work (viết: `work/<số>/kebab-topic`).
- Nhánh cấm pattern tự do không mang mã Work ad-hoc (exception: hạ tầng repo như `chore/*` vớiReviewer chỉ định).
- Pilot W118 bắt buộc: branch gắn comment issue đầu tiên có "branch: <tên>" để đối soát.

## 3. Quy ước Commit
- Format: `<type>(w<Work>): <mô tả ngắn>`
  - type: `docs`, `feat`, `fix`, `test`, `ci`, `style`, `chore`.
  - Ví dụ: `docs(w118): draft convention doc`.
- Commit phải chứa số Issue hoặc mã Work trong message để grep được (trừ docs-only siêu nhỏ vẫn khuyến khích).
- CI bot mutation (autofix) phải dùng prefix `style(w<number>): prettier autofix (ci run <id>)` như W300 đã làm, có cờ chống loop (xem DC-118-003).

## 4. Quy ước Pull Request
- Một PR gắn đúng 1 Work; title bắt đầu bằng mã Work.
- PR phải link Issue (`Refs #65`).
- Bắt buộc tối thiểu 1 review độc lập (actor khác pusher) trước merge trong phạm vi pilot; không auto-merge dù CI PASS.
- Merge method: squash preferred để 1 PR = 1 entry evidence sạch.

## 5. Templates (đề xuất nội dung, không tạo file .github ở giai đoạn này)
- Issue body: Mục tiêu / Scope / Actor chính / Gate hiện tại / Định nghĩa xong.
- PR body: Liên kết Issue / Đã thay đổi gì / Bằng chứng CI (run URL, SHA) / Rủi ro + rollback.
- Rationale: tạo file .github/ISSUE_TEMPLATE + PULL_REQUEST_TEMPLATE chỉ khi được phê duyệt (sau G3) tránh thay đổi flow toàn repo chưa phản biện.

## 6. Liên kết
- BB-118-001 (biên bản khởi tạo), EVIDENCE/W118-01_GITHUB_DISCOVERY_20261120.md (gaps), KH-118-001 (W118-02).
