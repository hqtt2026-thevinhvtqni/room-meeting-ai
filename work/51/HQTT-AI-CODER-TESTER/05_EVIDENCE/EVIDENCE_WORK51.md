# WORK51 Evidence — Hồ sơ bàn giao

Trạng thái: **P3 EXTENDED — ITERATION 3 CI VERIFIED — WORK 51 NOT DONE.**

Nguyên tắc (PLAN §4 P4): chỉ ghi PASS khi đã chạy và có bằng chứng. GitHub Actions đã chạy test suite và demo thật trên nhánh Work 51. Các kết quả dưới đây chỉ chứng minh hành vi của vertical slice đã kiểm tra; không chứng minh đủ các tiêu chí bảo mật, persistence, A2A spec conformance hoặc tích hợp production.

## Đã làm (có bằng chứng trên Git)

- P0 READ/TRACE: đọc charter, plan v1.1, cây Work 51, AGENTS.md, PROJECT_STATE.md, API_CONTRACT.md.
- P1: `contract.py` (schema + validation), `states.py` (state machine A2A), decision register D-01..D-09, architecture doc.
- P2 vertical slice: `a2a.py` (JSON-RPC 2.0 binding: Agent Card, message/send, tasks/get, continuation, error model), `coder_agent.py`, `tester_agent.py`, `sandbox.py`, `orchestrator.py`, `run_demo.py`.
- P3 automated tests: `04_TEST/` — 43 tests đã chạy thành công, phủ: happy path, seeded fail→fix→PASS, luôn fail→BLOCKED sau 2 vòng, max_fix_rounds=0, timeout sandbox, malformed payload (-32602), taskId lạ, transport error→BLOCKED, PASS thiếu evidence→BLOCKED, idempotent tasks/get, continuation feedback, hash mismatch, full pipeline qua HTTP thật.
- P4: README, ARCHITECTURE, DECISION_REGISTER, plan v1.2 changelog, file này.

## Kết quả chạy — bằng chứng CI thực tế

- Workflow: `.github/workflows/work51-a2a.yml`
- Initial code-verification run: [39930470092](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/39930470092) on code commit `2645366de183e7a0905a6c9d1b378741aec7b693`.
- Latest full-branch verification before artifact upload: [39930817040](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/39930817040) on commit `ccbe2985c260c05582a315885d51f6d481cd6910` (43 passed, demo exit 0).
- Evidence artifact verification: [run 39931057210](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/39931057210) on commit `503c17c5b9fdd9a99aa436d3

3f599de0556924e5`; uploaded artifact `work51-evidence-39931057210` (artifact ID `12491197678`, SHA-256 `ef3182702e1070b127134302b67bd00a8e650dd07a519ba72e6e7338329f8e9f`, expires 2026-11-22).
- Kết quả pytest: **43 passed, 0 failed** (Python 3.11; 8.58s on latest run). Pytest collection warning đã được sửa bằng `TesterBackend.__test__ = False`; test run này không còn `PytestCollectionWarning`.
- HTTP demo: **exit code 0**; `correct → PASS` (0 vòng sửa), `seeded_bug → PASS` (1 vòng sửa), `always_bug → BLOCKED` (2 vòng sửa, `max_fix_rounds_exceeded`). Evidence JSONL được upload làm GitHub Actions artifact trên run `39931057210`; tải artifact từ trang run trước ngày hết hạn 2026-11-22. SHA-256 của archive artifact: `ef3182702e1070b127134302b67bd00a8e650dd07a519ba72e6e7338329f8e9f`.
- Một cảnh báo cleanup vẫn còn: `fatal: No url found for submodule path 'room-meeting-ai' in .gitmodules`. Đây là vấn đề repo hygiene độc lập với Work 51; đã quan sát trong CI và không làm test/demo job thất bại. Không xóa gitlink trong phạm vi Work 51. Có thêm cảnh báo deprecation từ runner/action Node.js.

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
| G4 Evidence/hash/verdict cho run | test_pipeline.py, test_evidence_log_records_full_run | PASS — test coverage; JSONL uploaded as artifact on run `39931057210` |
| G5 Timeout/transport/malformed được xử lý tường minh | test_sandbox.py, test_http.py, DeadClient | PASS — tested scenarios only |
| G6 Không PASS khi thiếu evidence | test_pass_without_evidence_is_blocked | PASS — automated test |
| G7 BLOCKED có lý do + đề xuất xử lý | RunReport.reason + DECISION_REGISTER D-04/D-08/D-09 | PASS — slice emits reason; remaining infrastructure gates are open |

## Giới hạn còn tồn tại (blockers tương lai, không chặn slice)

1. ContainerSandbox D-04c đã được chạy trong CI khi Docker khả dụng; đây chưa phải kiểm toán bảo mật độc lập. Khi Docker không khả dụng, fallback Sandbox vẫn chỉ là lớp bảo vệ best-effort và không phù hợp để chạy mã không tin cậy từ nguồn ngoài.
2. PersistentTaskStore dùng JSON + atomic rename đã có test restart; giới hạn còn lại là single-writer và flush O(n) mỗi lần cập nhật.
3. Agent Card chưa ký theo A2A v1.0 (signed card) (D-01).
4. Coder là deterministic generator — LLM adapter là bước kế tiếp (D-03).
5. Full conformance với A2A spec/official SDK, signed Agent Card và interoperability với implementation A2A độc lập chưa được chứng minh; binding hiện tại là JSON-RPC 2.0 tối thiểu.
6. Ảnh chụp lịch sử ban đầu ghi nhận nhánh `work/51` phân kỳ với `main` (8 ahead / 27 behind); con số này là lịch sử trước khi Xu ra quyết định D-09 và không còn là trạng thái hiện tại.

## Commit

- Implementation commit: `23087dae4ff4f3eeb82a7b33be7a07c0c19b44f3` (vertical slice; 21 files).
- Evidence metadata commit: `6954db26f44aaaac3dea85f64d42256e3a1e0e32`.
- CI workflow commit: `ad69c05c7c4dac6bedf3f5dced8d69e3a4ee3778`.
- Test hygiene fix commit: `2645366de183e7a0905a6c9d1b378741aec7b693`.
- Verified CI runs: `39930470092` (implementation test) and `39930817040` (latest full branch) — both 43 passed, HTTP demo exit 0. Latest branch head at verification: `ccbe2985c260c05582a315885d51f6d481cd6910`. Current report is a tested vertical slice, not full Work 51 acceptance.

## Iteration 2 — sandbox hardening, persistence, binding v1.2 (2026-10-23)

Scope theo plan v1.4 (không tạo Work mới; D-09 đã được Xu quyết định và thực hiện bằng cách đồng bộ `main` vào nhánh Work 51, không đưa Work 51 vào `main`):

- sandbox.py v1.2 (D-04b): env scrub (không rò secrets), POSIX rlimits (CPU 10s / AS 1GB / FSIZE 4MB / NPROC 64), unshare -n network isolation có availability probe, cap input 200KB (SandboxInputError).
- task_store.py (D-08b): TaskStore in-memory + PersistentTaskStore JSON atomic rename; backend nhận store qua constructor; restart giữ continuation/idempotency/audit.
- a2a.py v1.2 (D-01b): Agent Card protocolVersion/version/preferredTransport; Task contextId/createdAt/updatedAt/status.timestamp; tasks/cancel ở server + client.
- 15 test mới: 04_TEST/test_http.py (+4: cancel working/unknown/terminal-noop, binding v1.2 fields), 04_TEST/test_persistence.py (6), 04_TEST/test_sandbox_hardening.py (5). Kỳ vọng suite: 58.

Trạng thái thực thi: **PASS — CI đã chạy thật** trên commit `0dbf964bd64c2c8129bff3aaa60915c681fd403d` sau khi sửa ba dòng Python bị tách giữa token/câu lệnh ở `coder_agent.py`, `test_http.py`, `tester_agent.py`.

- CI run: [39945767381](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/39945767381) — workflow kết thúc `success`.
- Test suite: **58 passed in 10.82s**, không có test fail.
- HTTP E2E demo: `correct → PASS`; `seeded_bug → PASS` sau 1 vòng feedback; `always_bug → BLOCKED` sau khi đạt giới hạn 2 vòng. Demo exit 0.
- Evidence artifact: `work51-evidence-39945767381`, artifact ID `12498725031`, SHA-256 `05aa58d781682c44a84707ca8f30f4c248a01878aff21c4513bdf71771b79685`, hết hạn `2026-11-22T11:24:09Z`.
- Các lỗi cú pháp được sửa bằng các commit `b07c6fe`, `ce76a13`, `0dbf964`; `main` không bị sửa.

Giới hạn còn lại: sandbox vẫn chưa container/seccomp; signed Agent Card và khả năng tương thích với official A2A SDK/spec chưa được chứng minh; CI cleanup vẫn có cảnh báo gitlink `room-meeting-ai` không có URL trong `.gitmodules` nhưng không làm job thất bại. D-09: PR [#24](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/pull/24) đã merge `main` → `work/51-hqtt-coder-tester` bằng merge commit `23194b90efe993614bc961607d3d481165d56b36`; `main` không bị thay đổi bởi code Work 51. So sánh sau merge xác nhận nhánh Work 51 **22 commits ahead / 0 behind** `main`. 
Merge commit và các cập nhật hồ sơ cần CI xác minh lại; chỉ run `39945767381` là bằng chứng 58/58 trên code commit `0dbf964` trước đồng bộ.

## Iteration 3 — container-grade sandbox profile (2026-10-23)

Scope theo ưu tiên của Xu sau D-09: thêm Docker ContainerSandbox D-04c, không tạo Work mới và không sửa `main`.

- `sandbox_container.py`: Docker `--network none`, `--memory 512m`, `--cpus 1.0`, `--pids-limit 64`, `--cap-drop ALL`, `no-new-privileges`, Docker default seccomp profile (không override bằng `seccomp=default`), `--read-only`, mount read-only; chạy bằng UID/GID host trên POSIX để đọc tempdir mà không cần capability root.
- `TesterBackend` chọn ContainerSandbox khi Docker và image khả dụng; nếu không, fallback về `Sandbox()`. Fallback không được xem là đủ cho mã không tin cậy từ nguồn ngoài.
- Bốn test container đã chạy thật trên CI, không skip.

Trạng thái thực thi: **PASS — CI đã chạy thật** trên commit `24e06ca66df407d2c0e2d6b285e5d8dededd8da7`.

- CI run: [39948132321](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/39948132321) — workflow `success`.
- Test suite: **62 passed in 23.22s**, 0 failed, 0 skipped.
- HTTP E2E demo exit 0: `correct → PASS` (0 vòng), `seeded_bug → PASS` (1 vòng), `always_bug → BLOCKED` (2 vòng).
- Evidence artifact: `work51-evidence-39948132321`, artifact ID `12499500891`, SHA-256 `2fa28680779adca5e14b6b18ff188b1585b9516ddb664c596b1633edeff7b7b4`; [mở run và artifact](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/39948132321).
- Hai lỗi container phát hiện trước khi PASS đã được sửa: Docker hiểu `seccomp=default` là đường dẫn; sau khi bỏ override, `--cap-drop ALL` làm root trong container không đọc được tempdir mode 0700, nên container được chạy bằng UID/GID host. Các run thất bại trước không được tính là PASS.
- GitHub Actions cleanup vẫn cảnh báo gitlink `room-meeting-ai` không có URL trong `.gitmodules`; warning không làm test/demo job thất bại và được giữ ngoài phạm vi Work 51.

Còn mở: signed Agent Card + official A2A SDK conformance; independent QA sign-off của Qw; custom seccomp whitelist/image digest pinning và gitlink `.gitmodules` (repo hygiene). signed Agent Card + official A2A SDK conformance; independent QA sign-off của Qw; gitlink .gitmodules (repo hygiene, ngoài phạm vi Work 51).
