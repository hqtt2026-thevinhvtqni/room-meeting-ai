# WORK 103 — DECISIONRAG RETRIEVAL EXPERIMENT PLAN
- Work: ROOM-HOP-RAG-RETRIEVAL-CAPABILITY
- Date: 2026-11-11 (UTC+07)
- Owner: Xu / xu
- Authority: Vinh
- Status: PROPOSED EXPERIMENT — NOT EXECUTED; BASELINE UNCHANGED
- Related architecture: Work 70 DOC-095 and DOC-096
- Research: Retriever-Free Retrieval: Navigating Documents with Decision Models (2026), https://arxiv.org/abs/2610.35868

## 1. Purpose
Evaluate DecisionRAG as an additional retrieval strategy against Work 103's existing baseline. This plan does not replace the current RAG pipeline, threshold, corpus, blind-label protocol or acceptance criteria.

## 2. Non-negotiable controls
1. Preserve the existing baseline and its configuration as an immutable comparator.
2. Do not alter, relabel, inspect or unfreeze the blind 50-query labels as part of this experiment. The blind-label/independent-review gate remains governed by its existing evidence and status.
3. Create a separate experiment branch/run namespace and a separate DecisionRAG result artifact. No overwriting baseline results.
4. Pin and record corpus snapshot/hash, query-set version/hash, code commit, model/provider/version, prompt, tree-building version/hash, runtime configuration and run ID.
5. Enforce the same source permissions and authorization boundaries as the existing Work 103 contract. Unauthorized content must not enter tree summaries, candidate context or model prompts.
6. No Core/API/DB/runtime/production changes are authorized by this plan.

## 3. Experiment arms
- A0 — Existing RAG baseline: exact current implementation/configuration; no retuning.
- A1 — DecisionRAG candidate-wise: evaluate candidate nodes/passages independently.
- A2 — DecisionRAG shared-context: evaluate multiple sibling candidates together in one context.
- A3 — Optional hybrid control: existing lexical/dense/hybrid path plus reranking, only if it can be run without changing A0.
A1 vs A2 isolates the shared-context hypothesis. A0 vs A1/A2 compares end-to-end retrieval strategy.

## 4. Document tree design
Initial controlled hierarchy:
Work / Corpus → Document → Section → Chunk.
Each node must carry stable IDs, source revision, permission metadata, parent/child links and provenance. Summaries are navigation hints only; final evidence must resolve to exact source passages and locators. Tree build/update cost and stale-node behavior must be measured.

## 5. Required evaluation
Retrieval: Precision@5, Recall@5, MRR, R@1/Hit@1.
Answerability: answer rate, no-answer accuracy, false abstention, unsupported-answer/leak rate.
Evidence: exact source/locator correctness, source coverage, pruning miss rate, permission violations (must be zero).
Operations: p50/p95 latency, input/output tokens, cost/query, throughput, tree build/update time.
Report raw counts and denominators alongside percentages. Report answerable and no-answer slices separately.

## 6. Protocol
1. READ/TRACE: verify the exact current baseline, existing evaluation gate, corpus and label provenance before any run.
2. FREEZE: snapshot corpus/tree/query-set and record hashes. Blind labels remain sealed from model outputs and retrieval scores.
3. BUILD: implement the experimental strategy in an isolated branch or test harness; do not alter production or baseline.
4. RUN: run A0/A1/A2 on the same eligible query set and permissions; randomize run order where practical; repeat enough times to characterize variance.
5. VERIFY: validate exact source locators, permissions, pruning trace, deterministic behavior and raw outputs.
6. ANALYZE: calculate metrics using identical definitions and denominators; include failure examples and confidence/variance where feasible.
7. REVIEW: independent reviewer examines protocol, raw evidence and conclusions before any recommendation.
8. DECIDE: Xu recommends; Vinh alone authorizes architecture or production changes.

## 7. Failure conditions
- Any unauthorized source exposure: immediate FAIL and stop.
- Any baseline mutation or blind-label leakage: INVALID RUN.
- Missing corpus/query/model/tree hashes or raw outputs: NOT REPRODUCIBLE.
- Pruned branch containing required gold evidence: count as retrieval miss; do not hide it.
- A higher R@1 with materially worse leak rate, permission safety, source correctness or operating cost is not an automatic win.

## 8. Current status
- Plan recorded: DONE.
- Existing baseline: PRESERVED; not re-run in this action.
- DecisionRAG code: NOT BUILT.
- Benchmark: NOT RUN.
- Independent review: NOT RUN.
- Production adoption: NOT APPROVED.

## 9. Next action
Xu first verifies the current canonical Work 103 architecture, baseline code/configuration, corpus snapshot and blind-label gate. If any canonical source or immutable snapshot is missing, record BLOCKED with evidence; do not start the benchmark or reconstruct labels.
