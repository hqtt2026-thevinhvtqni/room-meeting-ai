# Work 103 — EVAL_V2 Execution Evidence (2026-10-28)

## Claim: EVAL_V2 (labeled evaluation, v2 suite) = PASS, executed and verified

## Execution record
- Repository/branch: hqtt2026-thevinhvtqni/room-meeting-ai @ work/103-rag-retrieval-capability
- Commit: 2bd10ba3d76f098cec8d80e04adc491dc10d7b61
  (fix: false-abstention labelling independent of ranking misses;
   near-miss leak test pinned with pre-measured fixture — leak 0.462,
   answerable control 0.858 at min_score 0.35)
- GitHub Actions run: 40650318524
  https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/40650318524
- Jobs (verified via GitHub API 2026-10-28): unit-tests (3.11) SUCCESS,
  unit-tests (3.12) SUCCESS — 6/6 steps succeeded, including:
    1. py_compile (rag_retrieval.py, rag_eval.py, both test files)
    2. Unit tests: retrieval suite (19) + eval suite (25) — all pass
    3. Labeled retrieval evaluation gate — SUCCESS (exit 0)
- Prior failed run 40649716882 (commit 25e1d69/6f585a2: 2 behavior-test
  failures, gate SKIPPED) is retained as history: CI correctly blocked.

## Measured metrics at operating min_score = 0.35 (experimental, not locked)
- Hit@5 = 1.000, Recall@5 = 0.970, MRR = 1.000 (logic-equivalent verified run)
- Precision@5 = 0.860, answered_rate = 1.000 (no false abstention)
- no_answer_accuracy = 0.867 (13/15; 12/12 easy, 2/3 near-miss leaked)
- Latency: ms-scale per query on 8-document corpus (not meaningful yet)
- CI-verifiable fact: gate exit 0 => every metric at/above the floors in
  EVAL_SET.json (hit/recall/mrr/answered >= 0.90, no_answer >= 0.80,
  precision >= 0.80).

## Warnings recorded (do not ignore)
- Xu observed a .gitmodules-related warning in the CI logs. Checked
  2026-10-28: .gitmodules does NOT exist on work/103 branch nor on main.
  The "Post Checkout ... exit code 128" annotation appears on all runs of
  this workflow (including PASS runs) — treated as cleanup noise for now,
  but flagged OPEN for one review of the raw run log.
- Node.js 20 deprecation warnings on actions/checkout@v4, setup-python@v5 —
  cosmetic; ubuntu-latest migration notice applies repo-wide.

## Interpretation limits (per Xu decision 2026-10-28)
- The 2/3 near-miss leak is a LIMITATION of the current lexical
  configuration, not a satisfied requirement. It motivates the controlled
  retrieval-improvement experiment (task 03) but does NOT prove embeddings
  would fix it — that conclusion requires a controlled comparison on the
  same labeled set.
- CI green = unit + eval gates pass. It is NOT a product-readiness or
  RELEASE claim. Integration gate stays CLOSED.
- min_score = 0.35 remains EXPERIMENTAL.
