# Work 51 — HQTT AI Coder–Tester (A2A) — Quickstart

Status: **P2 VERTICAL SLICE PASS; P3 PARTIAL; WORK 51 NOT DONE** — 43 tests passed and HTTP demo passed in [GitHub Actions run 39930470092](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/39930470092). Security isolation, task persistence/restart, official A2A spec conformance, and branch divergence remain open.

## Chạy demo end-to-end (HTTP thật)

```bash
cd work/51/HQTT-AI-CODER-TESTER
python 03_CODE/run_demo.py
```

Demo chạy 3 kịch bản qua 2 A2A server (Coder :random, Tester :random):
`correct` → PASS ngay; `seeded_bug` → FAIL→feedback→sửa→PASS; `always_bug` → BLOCKED sau 2 vòng sửa. Evidence JSONL ghi vào `03_CODE/evidence_runs/<ts>/` trong runner; CI log xác nhận kết quả, nhưng file JSONL hiện chưa được upload làm artifact.

## Chạy test suite

```bash
cd work/51/HQTT-AI-CODER-TESTER
python -m pytest 04_TEST -q
```

Chỉ cần Python ≥ 3.9 + pytest, không cần key/API ngoài. CI chạy bằng Python 3.11. Sandbox dùng `sys.executable`.

## Bố cục

| Đường dẫn | Nội dung |
|---|---|
| `01_PLAN/PLAN_WORK51_v1.0.md` | Kế hoạch canonical (duy nhất, update in-place) |
| `02_ARCHITECTURE/ARCHITECTURE_WORK51.md` | Kiến trúc, sequence, mapping A2A, error model |
| `03_CODE/a2a_ct/` | Package implementation (stdlib-only) |
| `03_CODE/run_demo.py` | Demo E2E qua HTTP |
| `04_TEST/` | pytest: contract gate, state machine, sandbox, pipeline, HTTP binding |
| `05_EVIDENCE/EVIDENCE_WORK51.md` | Hồ sơ evidence — KHÔNG ghi PASS khi chưa chạy thật |
| `DECISION_REGISTER.md` | QĐ kiến trúc D-01..D-08 (ghi rõ cái nào cần Vinh phê duyệt) |

## Cắm LLM vào sau (không đổi protocol)

`CoderBackend._emit` là điểm thay deterministic generator bằng LLM adapter
(Qwen Coder) — interface `handle_task(task_id, payload, existing) -> task` giữ nguyên.
