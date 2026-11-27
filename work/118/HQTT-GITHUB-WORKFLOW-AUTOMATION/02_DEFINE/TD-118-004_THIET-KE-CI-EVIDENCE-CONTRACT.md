# TD-118-004 — THIẾT KẾ CI & EVIDENCE CONTRACT (W118-03)

- **Work:** W118 — HQTT GitHub Workflow Automation
- **Ngày:** 2026-11-20
- **Trạng thái:** DRAFT — chờ phản biện (Ka) / tổng hợp (Xu) / ACK (Vinh) trước khi hiện thực hóa.

## 1. Ma trận jobs đề xuất cho CI chuẩn của một Work
| Job | Bật khi | Nội dung tối thiểu | Permissions |
|---|---|---|---|
| docs-check | push/PR chạm hồ sơ Work | markdown lint nhẹ, json/yaml parse | contents: read |
| unit | push/PR chạm code Work | pytest/unittest deterministic | contents: read |
| e2e | cần unit PASS | boot thật in-process, HTTP thật qua TCP | contents: read |
| evidence-write | sau các job trên (luôn chạy) | ghi evidence row vào register | contents: write |
| diagnostics | chỉ khi FAIL | tạo/cập nhật issue chẩn đoán | issues: write |

Quy tắc: permissions least-privilege theo job (không để contents: write ở job test); timeout mỗi job tối đa 20 phút; concurrency group theo ref, cancel-in-progress.

## 2. Evidence contract cho CI run
Mỗi run CI tạo đúng 1 evidence row theo schema W70 v1.1, kèm đề xuất mở rộng v1.2 (mục 3):
- evidence_id: idempotent theo run, dạng "ci-<run_id>-<attempt>".
- evidence_type: RUNTIME; producer: tên workflow + job.
- artifact_ref: URL tái tạo bằng chứng (run URL + summary hoặc artifact URI).
- source_commit: github.sha; created_at: thời điểm job kết thúc.
- state: RECORDED (chỉ Ka/Vinh nâng lên VERIFIED/REJECTED theo quy trình W70).
- limitations: ghi rõ "CI PASS không thay thế review/nghiệm thu" khi dùng làm bằng chứng gate.
- Metrics rút gọn đính kèm dưới dạng text artifact: job matrix, exit code từng step, thời gian chạy.

## 3. Đề xuất extension schema v1.2 (cần ACK tách rời)
Schema hiện tại additionalProperties: false và KHÔNG có field run-level. Đề xuất bổ sung dạng optional, backward-compatible:
- ci_run_id (string), ci_job (string), ci_conclusion (enum success/failure/cancelled/skipped), ci_url (string uri).
Không thêm field bắt buộc; register cũ vẫn hợp lệ v1.1. Việc nâng schema do Work 70 làm chủ; W118 chỉ đề xuất.

## 4. Lưu trữ và truy vết
- Bằng chứng chính: evidence row + artifact CI (retention tối thiểu 14 ngày, khuyến nghị 90).
- Raw log không là nguồn bằng chứng chính (cần admin để tải) — luôn ghi tóm tắt đủ ý vào evidence/artifact/diagnostics issue.
- Idempotency: nếu evidence_id đã có trong register, bot cập nhật thay vì chèn trùng (xem TD-118-006).

## 5. Điều kiện ghi nhận kết quả run
CI PASS của một run chỉ có giá trị khi:	run URL + commit SHA + evidence row đã ghi + artifact còn tồn tại hoặc diagnostics issue chứa output. Thiếu bất kỳ mục nào thì ghi NOT VERIFIED.


## Amendment — Auto E2E v2 evidence artifact (2026-11-20)

The feature branch implementation writes one immutable artifact per validation run: `w118-run-evidence-<run_id>-<attempt>`. It contains schema_version, work_id, workflow, run_id, run_attempt, source_commit, event, test_outcome, state=`RECORDED`, and an explicit limitation that CI evidence does not constitute review or acceptance.

- Artifact retention currently 30 days; retention is a pilot setting, not a Work 70 policy change.
- The artifact is uploaded even when the contract-test step fails, provided the evidence-writing step can run.
- No write is made to Work 70's `EVIDENCE_REGISTER.json`; the v1.2 extension remains subject to Work 70 owner approval.
- CI checks run on push, pull_request and workflow_dispatch. Mutation permissions are isolated to the specific handoff, ACK, review and diagnostics jobs.
- A successful run proves only the tests/jobs executed for that run and exact SHA.


## Amendment — event-level OPERATION artifacts (2026-11-20)

The `scripts/w118/event_evidence.py` builder creates an OPERATION artifact for handoff, ACK and review events. Required fields bind Work ID, event type/ID, source commit, run ID/attempt, actor and decision. Each record is immutable and remains `RECORDED`; it explicitly states that it is not a Work 70 Evidence Register row and cannot self-promote to VERIFIED/ACCEPTED/RELEASED.

- Handoff artifact: `w118-handoff-evidence-<run_id>-<attempt>`.
- ACK artifact: `w118-ack-evidence-<run_id>-<attempt>`; includes whether the authorized `w118-acked` label was applied.
- Review artifact: `w118-review-evidence-<run_id>-<attempt>`.
- PR checklist is recorded by a deduplicated GitHub comment from a separate base-context workflow; ordinary pull_request validation stays read-only.
- Work 70 register integration remains blocked until Work 70 approves the schema/owner contract.


### Run provenance refinement — 2026-11-20

The validation artifact now distinguishes `source_commit` (PR head SHA when applicable) from `tested_commit` (the exact checked-out GitHub Actions revision), and records repository, source ref, tested ref, actor, workflow ref, run URL, PR number and PR base SHA. This prevents a PR merge-ref test from being misrepresented as a test of the source branch SHA alone.
