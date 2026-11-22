# ERROR LOG — Work 092

## 2026-10-06 — V2

- V1 đã được redesign theo Browser-first hierarchy; các phần developer/test được chuyển xuống secondary Demo/Test Mode và Developer/Architecture View.
- V2 E2E phát hiện Agent Workflow đếm cả metadata `Workflow complete` trong Evidence (`8/6`). Đã sửa để chỉ tính 6 evidence keys chuẩn; clean-state retest PASS `6/6`.
- Không ghi nhận lỗi known sau vòng clean-state retest V2.

## 2026-11-22 — Regression fixes found by final mirror testing

9. **Favicon 404:** initial Chromium run on the local read-back mirror found a missing favicon request. Added `data:,` favicon and static pytest assertion; final E2E had no console/page/network errors.
10. **Tab close was inert:** the × was decorative and `aria-hidden`. Added semantic close button, focus style, switching/removal logic and guard against closing the final tab; static pytest and Playwright checks pass on mirror.
11. **Verification boundary:** pytest 12/12, Node 14/14, JS syntax and Chromium E2E 11/11 passed on Cloud Sandbox mirror only. Not direct Work Sandbox or GitHub Actions. CI remains pending until a real run is verified.
