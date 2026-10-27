# WORK 10 — HOST E2E RUNBOOK (P3 gate)

Mục tiêu: đóng gate "Host real-browser E2E" bằng evidence thật, không fake PASS.

## 1. Chuẩn bị môi trường (chạy 1 lần)

```bash
cd room-meeting-ai
pip install -r 10/COMPUTER-AGENT/requirements.txt
playwright install chromium
```

## 2. Chạy offline contract tests trước (gate CI re-verify)

```bash
python 10/COMPUTER-AGENT/05_TEST/test_p0_p5.py
```

Kỳ vọng: `Offline contract tests: ALL PASSED`. Nếu FAIL → dừng, sửa rồi chạy lại.

## 3. Chạy real-browser E2E

```bash
python 10/COMPUTER-AGENT/05_TEST/e2e_real_browser.py
echo "exit code: $?"
```

| Exit code | Ý nghĩa | Hành động |
|---|---|---|
| 0 | PASS | Sang bước 4 |
| 1 | FAIL (test thật thất bại) | Đọc `real-browser-e2e-result.json` → self-fix → chạy lại |
| 2 | BLOCKED (thiếu Playwright/Chromium) | Làm lại bước 1, KHÔNG coi là fail của product |

## 4. Kiểm tra evidence (bắt buộc trước khi ghi PASS)

Vào `10/COMPUTER-AGENT/06_EVIDENCE/`:

- [ ] `real-browser-e2e-result.json` tồn tại, `status == "PASS"`
- [ ] `state_trace` = `PLANNED → RUNNING → VERIFYING → PASS` (không bỏ VERIFYING)
- [ ] Tất cả `steps[].ok == true` (14 bước: navigate, observe, click, type, key_press, scroll, wait, click, observe, extract, screenshot, download, observe, close)
- [ ] `evidence` có entry `verification: PASS` với 2 checks
- [ ] `real-browser-e2e.png` tồn tại và là screenshot trang đã SUBMITTED

## 5. Sau khi PASS

1. Cập nhật `00_ROOT/WORK_MANIFEST.md`: `HOST E2E: PASS (yyyy-mm-dd)` kèm đường dẫn evidence.
2. Không sửa evidence bằng tay — nếu nghi ngờ, chạy lại E2E.
3. Qe review → release decision (P5 smoke test qua `agent_api.py` nếu cần).
