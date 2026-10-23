# Work 51 — HQTT AI Coder–Tester (A2A) — Quickstart

Status: **P3 EXTENDED (iteration 3 verified); WORK 51 NOT DONE** — CI run [39948132321](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/39948132321) confirms **62 tests passed in 23.22s** and HTTP E2E demo exit 0. D-04c uses Docker ContainerSandbox when available; official A2A SDK/signed-card conformance and independent QA sign-off remain open.

## Chạy demo end-to-end (HTTP thật)

```bash
cd work/51/HQTT-AI-CODER-TESTER
python 03_CODE/run_demo.py
```

Demo chạy 3 kịch bản qua 2 A2A server (Coder :random, Tester :random):
`correct` → PASS ngay; `seeded_bug` → FAIL→feedback→sửa→PASS; `always_bug` → BLOCKED sau 2 vòng sửa. Evidence JSONL ghi vào `03_CODE/evidence_runs/<ts>/` và được upload thành artifact trong CI run [39948132321](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/39948132321).

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
| `DECISION_REGISTER.md` | QĐ kiến trúc D-01..D-09 + iteration 2, 3 (D-01b/D-04b/D-08b/D-04c) (ghi rõ cái nào cần Vinh phê duyệt) |

## Cắm LLM vào sau (không đổi protocol)

`CoderBackend._emit` là điểm thay determi
nistic generator bằng LLM adapter
(Qwen Coder) — interface `handle_task(task_id, payload, existing) -> task` giữ nguyên.

## Iteration 2 mới gì?

- sandbox.py: env scrub (child không thừa kế secrets của parent), rlimits CPU/mem/file/nproc, network isolation "auto" (unshare -n khi khả dụng), cap input 200KB.
- task_store.py: PersistentTaskStore — JSON, atomic rename; task state sống qua restart (đóng D-08 cho slice).
- a2a.py: binding v1.2 — Agent Card có protocolVersion "1.0"; Task có contextId + timestamps; method tasks/cancel.
- Test: **58/58 PASS** trên CI run [39945767381](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/39945767381); HTTP E2E demo PASS đúng ba kịch bản; evidence artifact ID `12498725031`. Work 51 vẫn PARTIAL, không đồng nghĩa nghiệm thu toàn Work.

## Iteration 3 — verified

- `sandbox_container.py`: ContainerSandbox dùng Docker `--network none`, Docker default seccomp profile, `--cap-drop ALL`, `no-new-privileges`, `--read-only`, resource caps và mount read-only. `TesterBackend` chọn container khi Docker/image khả dụng, nếu không fallback sang `Sandbox()`.
- 4 container tests đã chạy thật, không skip, trong CI run [39948132321](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/39948132321): tổng **62 passed**; artifact ID `12499500891`.
- Giới hạn còn lại: image chưa pin digest, chưa có seccomp whitelist riêng; cần independent security review, official A2A SDK/signed-card conformance và QA sign-off.
