# QE RUNBOOK — Tái lập CI Work 76 (PR #55)

- ASG: ASG-W76-VIBE-20261114-01 | Người thực hiện: QE độc lập (Qw / An)

## Bước 1 — Tái lập CI
1. Checkout nhánh work/76-trigger-engine-vibe-v1 (commit 8e73fdf).
2. Chạy: pytest 05_BUILD/05_TEST/test_trigger_engine.py -v
3. Kỳ vọng: toàn bộ PASS trên Python 3.11 và 3.12. Đối chiếu run 43541364364 (PASS).

## Bước 2 — Kiểm chứng 10 test DOC-006
- W76-CE-001..004: điều kiện (match/compare/window/viền biên 16:59:59Z)
- W76-RG-001..002: registry single-ACTIVE + CAS expected-revision
- W76-MD-001..002: model bất biến + digest ổn định
- W76-EV-001..002: payload untrusted size/depth + fail-closed

## Bước 3 — Mutation nhanh (khuyến nghị)
- Sửa 1 assertion trong conditions.py (ví dụ đảo since/until) → kỳ vọng test FAIL.
- Trả lại nguyên trạng → PASS lại. Ghi nhận kết quả vào Evidence Register.

## Bước 4 — Ghi nhận
- Tạo EV-76-0xx mới (canonical) kèm link run/log, KHÔNG tái sử dụng EV-76-023.
- Cập nhật EVIDENCE_REGISTER + PRODUCT_STATUS.json, không tuyên bố gate mới nếu chưa đủ điều kiện.
