# Work 103 — Verification and E2E Acceptance Plan

## Local/unit gates
- [x] Syntax compile of 04_CODE/rag_retrieval.py
      PASS: GitHub Actions py_compile (rag_retrieval.py, rag_eval.py, both test
      files), Python 3.11 & 3.12 (runs d3eb8dd #1, a3a1ebb 40648696465)
- [x] Run unittest/pytest for 05_TEST/test_rag_retrieval.py
      PASS: 21/21 + 10/10 eval tests; CI re-runs on every push to work/103 paths
- [x] Verify deterministic ranking over a labeled query set.
      PASS: EVAL_SET.json v1 (14 labeled + 5 no-answer); determinism unit test
      plus fixed sweep output; baseline gate enforces floors in CI
      (06_EVIDENCE/EVAL_BASELINE_20261028.md)
- [x] Measure precision@k, recall@k, no-answer accuracy, and response latency.
      PASS at baseline scale: rag_eval.py measures Precision@5, Recall@5, Hit@5,
      MRR, no-answer accuracy, avg latency; operating min_score=0.35 chosen
      from measured sweep (plateau 0.35-0.40). NOTE: corpus is 6 documents;
      re-measure on a realistic corpus before release gate.
- [~] Add malformed document, path traversal, Unicode/Vietnamese, large-file, duplicate and deletion/reindex tests.
      PARTIAL: path traversal, Vietnamese, oversized line, duplicate, reindex
      closed at unit level; large-file and malformed-encoding cases remain open.
      Next: load_approved_text_files tests for huge files and non-UTF-8 bytes.

## Integration gates
- [ ] Read Work 28 manifest/contracts and live MCP tool inventory.
- [ ] Trace the actual Core service and approved repository abstraction; do not wire MCP to storage directly.
- [ ] Add Core-owned service/API contract using existing project conventions.
- [ ] Add MCP schema + adapter only after Core contract is stable.
- [ ] Test source allowlisting and identity/authorization behavior.
- [ ] Live E2E: MCP :8020 -> Core :8000 -> retrieval service -> canonical source -> returned citation -> source readback.
- [ ] Negative E2E: unapproved scope denied, empty query rejected, no evidence abstains, injected document commands are not followed, secrets are not indexed.
- [ ] Record raw command, exit code, timestamp, environment, test report, and source/commit identity.

## Release gate
No DONE/PASS claim until all required gates have evidence. Sandbox artifact creation/readback is not a substitute for executed tests or live integration.
Status per Xu decision 2026-10-28: unit-side PASS (CI-enforced, self-renewing);
labeled baseline recorded with documented limits; integration gates CLOSED
until opened deliberately after baseline acceptance. Work 103 stays IN DEVELOPMENT.
