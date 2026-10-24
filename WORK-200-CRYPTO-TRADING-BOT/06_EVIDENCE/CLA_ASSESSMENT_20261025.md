# CLA ASSESSMENT — Work 200
**Ngày:** 2026-10-25 ICT · **Người lập:** Cla — AI-03 / CTO Code-Debug
**Phạm vi:** đánh giá độc lập source lõi và tài liệu Work 200 để phục vụ `PLAN_WORK200_v2.0.md`.
**Bậc evidence:** E1 (chạy ngoài Sandbox, trong container của Cla). Không phải E2/E3. Không có PASS toàn Work.

## 1. Đã đọc (qua MCP 8030, đọc nguyên văn)
`00_ROOT/PLAN_WORK200_v1.0.md`, `WORK_MANIFEST.md`, `01_ORIGINAL/PROJECT_BRIEF.md`, `03_ARCHITECTURE/INITIAL_ARCHITECTURE_PLAN.md`, `05_TEST/ACCEPTANCE_CRITERIA.md`, `05_TEST/tests/test_core.py`, `04_CODE/pyproject.toml`, `04_CODE/crypto_bot/{__init__,models,data_validation,strategy,risk,paper_broker,signal_intake}.py`, `02_EXTENSION/DASHBOARD_SCOPE_AND_INTEGRATION_PLAN.md`, `02_EXTENSION/BaoXtra_BX42MR_V4_2_8/{WORK200_BX428_INTEGRATION_PLAN,ALERT_COMPATIBILITY_CONTRACT_V01}.md`, `MT5_FULL_PORT_V1/MASTER_IMPLEMENTATION_PLAN.md`, `06_EVIDENCE/{IMPLEMENTATION_STATUS_20261024,BX428_INTEGRATION_VERIFICATION_20261024,WORK_JOURNAL_20261024,WORK200_MINUTES_20261025_01}.md`.

**Chưa đọc:** `test_signal_intake.py`, `04_CODE/dashboard/index.html`, file `.pine`, `.mq5`, hai file TSV, `ACCEPTANCE_GATES.md`, `FEATURE_PARITY_MATRIX.md`, `DEV_SEQUENCE_AND_MODES.md`, các evidence MT5, và thư mục `06_EVIDENCE/` ở root sandbox. Mọi nhận định về các file này dựa vào tài liệu tóm tắt, không dựa vào việc đọc chúng.

## 2. Môi trường chạy của Cla
- Cách làm: chép lại nguyên văn các module lõi vừa đọc vào container, giữ cấu hình `pyproject.toml` (`testpaths=../05_TEST/tests`, `pythonpath=.`).
- Python 3.12.3, pytest cài sẵn/được cài bằng `pip --break-system-packages`.
- **Giới hạn:** bản chép không phải file trong Sandbox; không có hash đối chiếu hai phía; `signal_intake.py` được đọc nhưng không đưa vào lần chạy này.

## 3. Kết quả
**Lệnh:** `python3 -m pytest -q` (từ `04_CODE`)
**Kết quả:** `6 passed in 0.01s` (`test_core.py`).

### Probe có mục tiêu (script ad-hoc, kết quả quan sát được)
| Probe | Nội dung | Kết quả quan sát |
|---|---|---|
| P1 | SELL 5 @100 khi long 1800, trần vị thế 2000 | `approve` = `False` (lệnh giảm vị thế bị chặn) |
| P2 | `OrderRequest(quantity=Infinity)` / `NaN` | Infinity tạo được và bị `approve` từ chối; NaN ném `decimal.InvalidOperation` |
| P3 | `reference_price = Infinity` | `approve` = `False` |
| P4 | Trần vị thế 150, trần lệnh 1000, 3 lệnh BUY ~100 với tham số mặc định | 3 fills, tổng ~300.15, `halted = False` |
| P5 | `MovingAverageCross(5,20)` gọi lần 1 trên chuỗi phẳng, lần 2 và lần 3 cùng một chuỗi tăng | `None`, `BUY`, `None` (lần 3 khác lần 2 dù input giống); instance mới cho `BUY` |
| P6 | Chuỗi nến 15m thiếu 10 nến | `validate_candles` chấp nhận |
| P7 | Trộn nến cách nhau 1 phút và 15 phút | `validate_candles` chấp nhận |

Lần chạy P4 đầu tiên dùng trần quá rộng nên không chứng minh được gì; probe được viết lại với trần chặt và chỉ kết quả lần sau được tính làm evidence cho D1.

## 4. Kết luận
Phát hiện D1–D11 và các task xử lý nằm ở `PLAN_WORK200_v2.0.md` mục 3.3 và `references/task-graph.md`. Các phát hiện D1, D2, D5, D6 được chứng minh bằng probe ở E1. D3, D7, D8, D9, D10, D11 dựa trên đọc source/tài liệu. D4 có evidence một phần: an toàn hiện nay chỉ nhờ phép so sánh trong risk.

**Trạng thái Work 200:** ACTIVE / PARTIAL IMPLEMENTATION / NOT RELEASED. Không PASS. Giao dịch tiền thật: NO-GO.
