# WORK51 Evidence — Hồ sơ bàn giao

Trạng thái: **IMPLEMENTATION COMMITTED — TEST EXECUTION PENDING.**

Nguyên tắc (PLAN §4 P4): chỉ ghi PASS khi đã chạy và có bằng chứng. Do môi
trường tác giả hiện tại không có runtime Python, toàn bộ test suite được
viết nhưng **chưa được thực thi** ở đây — không tiêu chí nghiệm thu nào
được đánh dấu PASS trong file này cho đến khi có output chạy thật.

## Đã làm (có bằng chứng trên Git)

- P0 READ/TRACE: đọc charter, plan v1.1, cây Work 51, AGENTS.md, PROJECT_STATE.md, API_CONTRACT.md.
- P1: `contract.py` (schema + validation), `states.py` (state machine A2A), decision register D-01..D-09, architecture doc.
- P2 vertical slice: `a2a.py` (JSON-RPC 2.0 binding: Agent Card, message/send, tasks/get, continuation, error model), `coder_agent.py`, `tester_agent.py`, `sandbox.py`, `orchestrator.py`, `run_demo.py`.
- P3 (tác giả, chưa chạy): `04_TEST/` — 40 test case phủ: happy path, seeded fail→fix→PASS, luôn fail→BLOCKED sau 2 vòng, max_fix_rounds=0, timeout sandbox, malformed payload (-32602), taskId lạ, transport error→BLOCKED, PASS thiếu evidence→BLOCKED, idempotent tasks/get, continuation feedback, hash mismatch, full pipeline qua HTTP thật.
- P4: README, ARCHITECTURE, DECISION_REGISTER, plan v1.2 changelog, file này.

## Lệnh cần chạy để sinh evidence thật

```bash
cd work/51/HQTT-AI-CODER-TESTER
python -m pytest 04_TEST -q          # kết quả -> dán vào mục "Kết quả chạy"
python 03_CODE/run_demo.py           # 3 kịch bản + evidence_runs/<ts>/evidence.jsonl
```

Yêu cầu: Python ≥ 3.9, pytest. Không cần API key.

## Kết quả chạy

_(chưa có — An/Qc/Vinh chạy lệnh trên rồi ghi lại output + commit SHA; sau đó mới được cập nhật trạng thái từng gate G1–G8)_

## Gate mapping (để An kiểm độc lập)

| Gate (charter §7) | Test file | Trạng thái |
|---|---|---|
| G1 Contract hợp lệ/lệch format được xử lý | test_contract.py | PENDING EXECUTION |
| G2 Tách quyền Coder/Tester; Tester thấy artifact thật | test_pipeline.py, test_http.py | PENDING EXECUTION |
| G3 Feedback loop có giới hạn, không vòng lặp vô hạn | test_pipeline.py (always_bug, max_rounds=0) | PENDING EXECUTION |
| G4 Evidence đầy đủ, reproducible (hash, verdict) | test_pipeline.py, test_evidence_log_records_full_run | PENDING EXECUTION |
| G5 Timeout/transport/malformed được xử lý tường minh | test_sandbox.py, test_http.py, DeadClient | PENDING EXECUTION |
| G6 Không PASS khi thiếu evidence | test_pass_without_evidence_is_blocked | PENDING EXECUTION |
| G7 BLOCKED có lý do + đề xuất xử lý | RunReport.reason + DECISION_REGISTER D-04/D-08/D-09 | PENDING EXECUTION |

## Giới hạn còn tồn tại (blockers tương lai, không chặn slice)

1. Sandbox chưa container hóa — không chạy untrusted code thật (D-04, cần phê duyệt).
2. Task store in-memory — restart mất state (D-08).
3. Agent Card chưa ký theo A2A v1.0 (signed card) (D-01).
4. Coder là deterministic generator — LLM adapter là bước kế tiếp (D-03).
5. Nhánh `work/51` 27 commits behind main (D-09 — escalate Vinh).

## Commit

- Implementation commit: xem git log nhánh `work/51-hqtt-coder-tester`, message `feat(work51): A2A coder-tester vertical slice — contract, state machine, JSON-RPC binding, coder/tester agents, sandbox, orchestrator, tests, docs`.
