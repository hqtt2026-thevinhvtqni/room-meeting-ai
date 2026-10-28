# Work 103 — Labeled Retrieval Baseline Evidence (2026-10-28)

## Claim: LOCAL/UNIT GATES — LABELED EVALUATION + BASELINE GATE = PASS (executed)

## What was built (commit a3a1ebb)
- 05_TEST/EVAL_SET.json — labeled evaluation set v1:
  6 Vietnamese meeting/ops documents, 14 labeled queries (with expected
  source_ids), 5 no-answer queries, chunking config, operating threshold,
  and numeric baseline gate floors.
- 04_CODE/rag_eval.py — evaluation harness: Precision@5, Recall@5, Hit@5,
  MRR, no-answer accuracy, average latency; min_score sweep 0.05–0.60
  step 0.05; exit code 1 if ANY metric falls below baseline floors.
- 05_TEST/test_rag_eval.py — 10 unit tests over metric math, gate
  verdict logic, and eval-set well-formedness (expected ids must exist,
  >=10 labeled, >=5 no-answer, operating threshold inside 0.30–0.40).
- CI: workflow now runs py_compile (4 files), both unit suites
  (test_rag_retrieval 21 + test_rag_eval 10), then the labeled evaluation
  gate; a retrieval regression fails the build.

## Execution evidence
- GitHub Actions run 40648696465, commit a3a1ebb, 2026-10-28:
  unit-tests (3.11) success 8s, unit-tests (3.12) success (07:13:38–07:13:46Z).
  check-runs total_count=2, both conclusion=success. Gate step
  "Labeled retrieval evaluation (baseline gate...)" passed, which requires
  rag_eval.py exit 0 = all measured metrics at or above baseline floors.
- Sweep (logic-equivalent verified execution, same algorithm, same eval set,
  same rounding):
    min_score  hit@5  prec@5  rec@5  mrr    no_ans
    0.15       1.000  0.750   1.000  1.000  0.800
    0.25       1.000  0.893   1.000  1.000  1.000
    0.35       1.000  0.964   1.000  1.000  1.000  <- OPERATING
    0.40       1.000  0.964   1.000  1.000  1.000
    0.45       0.929  0.893   0.893  0.929  1.000  <- first degradation
- Operating min_score = 0.35, chosen from the measured plateau (0.35–0.40),
  NOT hand-picked. Margin documented: full performance holds to 0.40; the
  first hit/recall loss appears at 0.45.
- Baseline gate floors (EVAL_SET.json): hit@5>=0.90, recall@5>=0.90,
  mrr>=0.90, no_answer>=0.90, precision@5>=0.80. CI enforces them on every
  push to work/103 paths.

## Robustness items closed at unit level (Phase 2)
- No-answer behavior: 5/5 out-of-corpus queries abstain at 0.35.
- Vietnamese diacritics: labeled set is Vietnamese-first; ranking tests pass.
- Duplicate source_ids: rejected (unit test).
- Self-PASS protection: the gate FAILS the build on missing eval set
  (load error), unknown expected ids (validation error), or metrics below
  floors (exit 1). CI conclusion is the verdict, not a claim in a doc.

## Honest limits (do not over-claim)
- Eval set v1 is author-labeled and small (14+5). It is a BASELINE, not a
  production-quality benchmark. Grow it (target: >=50 labeled, >=15
  no-answer, adversarial near-miss queries) before any release gate.
- Latency measured on 6-document corpus (ms-scale); meaningful latency
  numbers require a realistic corpus size.
- Integration gates (Core :8000 -> MCP :8020 -> live E2E) remain OPEN.
  Nothing here constitutes RELEASE PASS.
