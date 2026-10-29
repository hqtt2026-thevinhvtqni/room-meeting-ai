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


## Ka audit addendum — 2026-10-29 (UTC+07:00)

This addendum corrects stale descriptive counts without deleting the earlier history.

### Verified current EVAL_SET.json v2 shape
- `documents`: 8 embedded synthetic benchmark documents.
- `labeled_queries`: 50.
- `no_answer_queries`: 15.
- Therefore, the earlier statement above describing `EVAL_SET.json v1` as “14 labeled + 5 no-answer” is historical/stale and must not be used to describe the current v2 file.
- `EVAL_SET.json` v2 is a self-contained synthetic retrieval benchmark. Its documents and query set differ from the six-source corpus fixture in `00_CORPUS/CORPUS_MANIFEST_v4.0.md` and the 50-query Qw V5 label artifact. Results from one set must not be reported as measured on the other.

### Adjudication and integrity evidence
- Ka's row-by-row source adjudication is recorded in `06_EVIDENCE/KA_ADJUDICATED_LABELS_50_QUERIES_V2_20261029.json`.
- 50/50 row hashes and the canonical dataset hash were independently recomputed after GitHub readback.
- Adjudications: Q009, Q016 and Q046 change from `NO_ANSWER` to `ANSWERABLE` in Ka's new version; Qw V5 remains immutable.
- Six Manifest V4 source hashes match SHA-256 computed from the published GitHub raw-content representation (UTF-8/LF). This proves the published GitHub snapshot matches the declared logical hashes; it does not prove the original Sandbox's raw bytes or blind annotation provenance.

### Gate status
- Unit-test and baseline claims in the earlier plan are historical plan entries, not a new test execution in this Ka session.
- This session did not execute Python tests or live MCP/Core E2E; no CI run was returned for the documentation-only audit commit.
- Corpus freeze, blind-process provenance, selection of the release benchmark snapshot, and live integration/negative E2E remain BLOCKED.
