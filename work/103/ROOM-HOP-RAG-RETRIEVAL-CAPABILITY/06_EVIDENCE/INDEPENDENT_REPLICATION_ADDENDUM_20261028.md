# Work 103 — Independent Replication Addendum (2026-10-28)

## Status and scope

This addendum records the independent sandbox replication reported during review of the controlled retrieval experiment. It supplements, and does not overwrite, the original CI artifacts.

## Independently replicated findings

| Check | Replicated result |
|---|---|
| Baseline at threshold 0.35, ONT near-miss | score 0.355384 |
| Baseline at thresholds 0.35 and 0.45, Hanoi Q4 revenue near-miss | score 0.511820 at both thresholds |
| Hybrid 75/25 at threshold 0.50 | all three existing near-miss cases abstain |
| Hybrid at threshold 0.50 | 49/50 answerable queries return a result |
| Hybrid top-1 among returned answers | no returned answer is ranked against the wrong expected source; the one lost answer is empty/abstained, not a wrong ranking |

The replication matches the controlled experiment report for these checks.

## Diagnosis: hybrid trade-off, not semantic understanding

The answerable query rejected by Hybrid@0.50 is **“kỷ luật họp tuần gồm những gì”**, expected source `docs/ky-luat-hop.md`. Its blend score is 0.484, just below threshold 0.50. This list-type/general question has relatively low query-token coverage, so the 25% coverage component reduces a relevant BM25 result below the threshold.

The Hanoi revenue near-miss has strong lexical overlap on “doanh thu” and “quý 4”, while “chi nhánh” and “Hà Nội” are not supported by the corpus text. BM25 score is 0.511820. The hybrid coverage penalty makes it abstain at 0.50, but it still leaks at 0.45. This demonstrates threshold-sensitive lexical overlap, not a semantic reasoning capability.

## Decision and next experiment

1. Keep production/default operating `min_score=0.35` unchanged. The 0.45 value remains a candidate, not a decision.
2. Keep hybrid as research-only. Do not promote it based on three near-miss cases.
3. Build a blinded challenge pool with both:
   - near-miss/no-answer queries that overlap corpus vocabulary but require missing branch, location, time, quarter, metric, or entity facts;
   - answerable list-type/general queries, including “gồm những gì”, “các bước”, “quy định nào”, and “liệt kê”.
4. Have an independent annotator assign answerability and expected source IDs without seeing retrieval scores, ranking, or model outputs. Resolve disagreements before unblinding and freeze the labeled set version/hash.
5. Evaluate baseline at 0.35 and candidate thresholds 0.40–0.48, plus hybrid at matched operating points. Report precision@5, recall@5, MRR, top-1, answered rate, no-answer accuracy, false-abstention count, near-miss leakage count, and latency. Report raw counts alongside percentages because the current no-answer sample is only 15.
6. No change to integration/release gates: ROOM-HOP integration remains **BLOCKED / gate CLOSED**; release remains **NOT PASS**.

## Limitation

The current corpus has eight documents and only three near-miss/no-answer hard cases. Results are useful for diagnosis but too small to establish generalization or production readiness.
