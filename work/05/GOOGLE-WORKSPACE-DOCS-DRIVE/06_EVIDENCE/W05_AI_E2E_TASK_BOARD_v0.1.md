# WORK 05 — AI E2E TASK BOARD v0.1

Status: ACTIVE — GOOGLE DOCS/DRIVE DECISIONS OPEN; PROCESS VALIDATION TRACK REPORTED PASS (v0.1–v0.3)

## Mục tiêu
Dùng 8 quyết định mở của Work 05 để các AI nghiên cứu độc lập, tạo proposal có evidence, sau đó Xu tổng hợp thành Architecture Specification.

## Quy tắc
- Không pre-lock architecture.
- Không xếp hạng AI.
- Mỗi task cần proposal độc lập và evidence.
- Claim quan trọng phải chỉ rõ cách kiểm chứng.
- Không chuyển sang Build khi chưa qua Evidence Gate và VINH GATE nếu quyết định thuộc thẩm quyền Vinh.

## Task Board

| Task | Chủ đề | Output bắt buộc | Stage | Status |
|---|---|---|---|---|
| A01 | Google Docs ↔ Core: vai trò/source-of-truth | Proposal + evidence + test needed | Research | OPEN |
| A02 | Metadata / Data Model | Proposal + evidence + test needed | Research | OPEN |
| A03 | Authentication + Authorization | Proposal + evidence + test needed | Research | OPEN |
| A04 | My Drive vs Shared Drive | Proposal + evidence + test needed | Research | OPEN |
| A05 | Write Model + Revision | Proposal + evidence + test needed | Research | OPEN |
| A06 | Concurrency + Queue | Proposal + evidence + test needed | Research | OPEN |
| A07 | Sync + Reconciliation | Proposal + evidence + test needed | Research | OPEN |
| A08 | Conflict + Recovery | Proposal + evidence + test needed | Research | OPEN |

## Proposal Contract

Mỗi AI proposal nên có:

1. CLAIM — khẳng định/đề xuất chính.
2. REASONING — lập luận.
3. OPTIONS — các phương án đã xem xét.
4. EVIDENCE — nguồn/bằng chứng hoặc test output.
5. RISKS — rủi ro và giới hạn.
6. PROPOSAL — phương án AI đề xuất.
7. TEST NEEDED — test cần chạy để xác nhận.

## Completion Contract của từng Task

DONE chỉ khi có proposal + evidence + test-needed rõ ràng.
Nếu thiếu evidence: NEED_EVIDENCE.
Nếu proposal xung đột: CONFLICT.
Nếu cần quyết định của Vinh: VINH_GATE.


## State separation — important

The AI E2E Build Process validation track and the Google Docs/Drive architecture decision track are separate.

- Process milestones reported: v0.1 Process Mechanics PASS; v0.2 Real Build PASS; v0.3 Failure & Recovery PASS. These indicate prototype/runner readiness only; confirm immutable run artifacts before an E2E PASS claim.
- A01–A08 remain OPEN. Process validation does not resolve or close any Google Docs/Drive decision.
- Continue requiring independent proposal, evidence, test-needed, Evidence Gate, and VINH GATE where applicable.
