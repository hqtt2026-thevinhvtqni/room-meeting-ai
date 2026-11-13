# SỔ LÀM VIỆC WORK 103 / WORK 103 WORK PACKAGE REGISTER
- **STT / Document ID:** DOC-060
- **Priority:** P0
- **Read order:** 8
- **Depends on:** DOC-001; DOC-045; DOC-055; DOC-056; DOC-057; DOC-035
- **Status:** ACTIVE — INITIAL REGISTER (Batch 3, DOC-056)
- **Version / Updated:** 1.0 / 2026-11-09
- **Owner:** Xu / AI-01
- **Authority:** Vinh
- **Producer:** Vibe (2026-11-09, under Vinh's standing full-build authorization; "xây tiếp, không chờ" — DOC-035 LOG-W103-20261109-007/008)

Quy tắc (DOC-001 §6): mọi WP có owner, reviewer, dependencies, deliverables, acceptance criteria, status, evidence links. "No evidence, no PASS." Status build-level không phải gate PASS.

| WP | Tên | Deliverables | Owner / Reviewer | Depends on | Acceptance criteria | Status | Evidence |
|---|---|---|---|---|---|---|---|
| WP-103-01 | Retrieval core | 04_CODE/rag_retrieval.py; 05_TEST/test_rag_retrieval.py | Vibe / Ka | — | Unit suite green py3.11+3.12; approved-roots loader; untrusted input as data | DONE (build-level) | EVD-001; CI runs hiện hành |
| WP-103-02 | Labeled evaluation baseline | 04_CODE/rag_eval.py; 05_TEST/EVAL_SET.json | Vibe / Ka | WP-103-01 | Baseline gate PASS trong CI; schema validation | DONE (build-level) | EVD-001; CI step "Labeled retrieval evaluation" |
| WP-103-03 | Evidence-support stage | 03_ARCHITECTURE/EVIDENCE_SUPPORT_STAGE_CONTRACT_V3.md; 04_CODE/rag_evidence_support.py; 05_TEST/EVIDENCE_SUPPORT_DECISION_SET_V1.json + test | Vibe / Ka | WP-103-01 | Gate B 11/11 trong CI; adjudication độc lập contract + decision set | Build DONE; adjudication OPEN | EVD-005/008; DEBT-ES-01/02 |
| WP-103-04 | Corpus diagnostic harness (report-only) | 04_CODE/rag_evidence_support_corpus_eval.py; 05_TEST/EVIDENCE_SUPPORT_FACT_SPECS_V1.json và V2.json + test | Vibe / Ka | WP-103-01/03 | Unit suite green; V1+V2 summaries trong CI; adjudication 50 rows | DONE (report-only); adjudication OPEN | EVD-009/010/011; DEBT-ES-07 |
| WP-103-05 | Governance & standardization | DOC-034/035/045/055/056/057/058/059/060; batches 0–6 | Xu / Ka | — | DOC-056 §6 acceptance criteria; independent QE | IN_PROGRESS (0 DONE; 1,2,5 IN_PROGRESS; 3 register DONE; 4,6 NOT_STARTED) | DOC-056; EVD-007..011 |
| WP-103-06 | Gate C design (corpus-aligned five-state) | Thiết kế + phê duyệt Gate C | Xu / Ka | WP-103-04 + adjudication (DEBT-ES-02/07) | Thiết kế sau adjudication; gộp citation alignment (DEBT-ES-08) | BLOCKED | DEBT-ES-03/08 |
| WP-103-07 | E2E integration MCP :8020 → Core :8000 | Quyết định tích hợp riêng | Xu / Vinh | Offline gates | DOC-001 §2/§7; không phụ thuộc endpoint legacy | CLOSED (chưa mở lại) | DEBT-ES-04; DOC-035 |
| WP-103-08 | Remediation retrieval-side (no-answer leaks/misses) | Phương án có ma trận tradeoff (EVD-011); KHÔNG sửa rag_retrieval.py khi chưa có quyết định | Ka/Qw / Xu | EVD-011 | Cải thiện no_answer_accuracy mà không mở lại leak; giữ nguyên gate tới khi có quyết định | OPEN | DEBT-ES-06; EVD-011 |

## Ghi chú
- Chỉ dẫn Vinh 2026-11-09: các xác nhận chưa có được ghi nợ (DEBT-ES-09/10 và các debt hiện hữu) và build tiếp tục không chờ.
- Vibe không tự phê chuẩn; mọi status DONE ở đây là build-level, không phải gate PASS.
