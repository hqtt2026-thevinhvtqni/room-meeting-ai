# ERROR LOG — Work 092

## 2026-10-06 — V2

- V1 đã được redesign theo Browser-first hierarchy; các phần developer/test được chuyển xuống secondary Demo/Test Mode và Developer/Architecture View.
- V2 E2E phát hiện Agent Workflow đếm cả metadata `Workflow complete` trong Evidence (`8/6`). Đã sửa để chỉ tính 6 evidence keys chuẩn; clean-state retest PASS `6/6`.
- Không ghi nhận lỗi known sau vòng clean-state retest V2.
