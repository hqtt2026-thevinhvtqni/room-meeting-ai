# WORK51 Evidence — Hồ sơ bàn giao

Trạng thái: **P2 VERTICAL SLICE VERIFIED — P3 PARTIAL — WORK 51 NOT DONE.**

Nguyên tắc (PLAN §4 P4): chỉ ghi PASS khi đã chạy và có bằng chứng. GitHub Actions đã chạy test suite và demo thật trên nhánh Work 51. Các kết quả dưới đây chỉ chứng minh hành vi của vertical slice đã kiểm tra; không chứng minh đủ các tiêu chí bảo mật, persistence, A2A spec conformance hoặc tích hợp production.

## Đã làm (có bằng chứng trên Git)

- P0 READ/TRACE: đọc charter, plan v1.1, cây Work 51, AGENTS.md, PROJECT_STATE.md, API_CONTRACT.md.
- P1: `contract.py` (schema + validation), `states.py` (state machine A2A), decision register D-01..D-09, architecture doc.
- P2 vertical slice: `a2a.py` (JSON-RPC 2.0 binding: Agent Card, message/send, tasks/get, continuation, error model), `coder_agent.py`, `tester_agent.py`, `sandbox.py`, `orchestrator.py`, `run_demo.py`.
- P3 automated tests: `04_TEST/` — 43 tests đã chạy thành công, phủ: happy path, seeded fail→fix→PASS, luôn fail→BLOCKED sau 2 vòng, max_fix_rounds=0, timeout sandbox, malformed payload (-32602), taskId lạ, transport error→BLOCKED, PASS thiếu evidence→BLOCKED, idempotent tasks/get, continuation feedback, hash mismatch, full pipeline qua HTTP thật.
- P4: README, ARCHITECTURE, DECISION_REGISTER, plan v1.2 changelog, file này.

## Kết quả chạy — bằng chứng CI thực tế

- Workflow: `.github/workflows/work51-a2a.yml`
- Run: [39930470092](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/39930470092)
- Tested code commit: `2645366de183e7a0905a6c9d1b378741aec7b693`
- Kết quả pytest: **43 passed, 0 failed** (Python 3.11; 8.59s). Pytest collection warning đã được sửa bằng `TesterBackend.__test__ = False`; test run này không còn `PytestCollectionWarning`.
- HTTP demo: **exit code 0**; `correct → PASS` (0 vòng sửa), `seeded_bug → PASS` (1 vòng sửa), `always_bug → BLOCKED` (2 vòng sửa, `max_fix_rounds_exceeded`). Evidence JSONL đã được tạo trong workspace của runner: `03_CODE/evidence_runs/20261023T091508Z/evidence.jsonl`. GitHub Actions chưa upload file JSONL làm artifact tải xuống, vì vậy log run là bằng chứng hiện có.
- Một cảnh báo cleanup vẫn còn: `fatal: No url found for submodule path 'room-meeting-ai' in .gitmodules`. Đây là gitlink sai đã xác định ở main/repo hygiene; Work 51 đang 27 commit behind và chưa tự ý xóa gitlink/rebase. Cảnh báo không làm test/demo job thất bại. Có thêm cảnh báo deprecation từ runner/action Node.js.

## Lệnh tái lập

```bash
cd work/51/HQTT-AI-CODER-TESTER
python -m pytest 04_TEST -q
python 03_CODE/run_demo.py
```

Yêu cầu: Python ≥ 3.9, pytest. Không cần API key.

## Gate mapping (để An kiểm độc lập)

| Gate (charter §7) | Test file | Trạng thái |
|---|---|---|
| G1 Contract hợp lệ/lệch format được xử lý | test_contract.py | PASS — covered by 43-test CI run |
| G2 Tách vai trò backend Coder/Tester; Tester kiểm artifact thật | test_pipeline.py, test_http.py | PASS — slice behavior only; no production identity/auth proof |
| G3 Feedback loop có giới hạn, không vòng lặp vô hạn | test_pipeline.py + HTTP demo `always_bug` | PASS — BLOCKED after 2 rounds |
| G4 Evidence/hash/verdict cho run | test_pipeline.py, test_evidence_log_records_full_run | PASS — test coverage; CI JSONL not uploaded as downloadable artifact |
| G5 Timeout/transport/malformed được xử lý tường minh | test_sandbox.py, test_http.py, DeadClient | PASS — tested scenarios only |
| G6 Không PASS khi thiếu evidence | test_pass_without_evidence_is_blocked | PASS — automated test |
| G7 BLOCKED có lý do + đề xuất xử lý | RunReport.reason + DECISION_REGISTER D-04/D-08/D-09 | PASS — slice emits reason; remaining infrastructure gates are open |

## Giới hạn còn tồn tại (blockers tương lai, không chặn slice)

1. Sandbox chưa container hóa — không chạy untrusted code thật (D-04, cần phê duyệt).
2. Task store in-memory — restart mất state (D-08).
3. Agent Card chưa ký theo A2A v1.0 (signed card) (D-01).
4. Coder là deterministic generator — LLM adapter là bước kế tiếp (D-03).
5. Full conformance với A2A spec/official SDK, signed Agent Card và interoperability với implementation A2A độc lập chưa được chứng minh; binding hiện tại là JSON-RPC 2.0 tối thiểu.
6. Nhánh `work/51` đang phân kỳ với `main`: **8 commits ahead, 27 commits behind** tại lần so sánh mới nhất (D-09). Không rebase/merge vì chưa có quyết định riêng.

## Commit

- Implementation commit: `23087dae4ff4f3eeb82a7b33be7a07c0c19b44f3` (vertical slice; 21 files).
- Evidence metadata commit: `6954db26f44aaaac3dea85f64d42256e3a1e0e32`.
- CI workflow commit: `ad69c05c7c4dac6bedf3f5dced8d69e3a4ee3778`.
- Test hygiene fix commit: `2645366de183e7a0905a6c9d1b378741aec7b693`.
- Verified CI run: `39930470092` — 43 passed, HTTP demo exit 0. Current report is a tested vertical slice, not full Work 51 acceptance.
