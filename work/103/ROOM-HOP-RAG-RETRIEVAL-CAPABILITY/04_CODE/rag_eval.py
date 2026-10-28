"""Work 103 — Labeled retrieval evaluation harness.

Loads the labeled evaluation set, measures retrieval quality
(Precision@k, Recall@k, Hit@k, MRR, no-answer accuracy, latency),
sweeps min_score thresholds, and enforces a baseline gate:
exit code 1 if any measured metric falls below the baseline in EVAL_SET.json.

Usage (from 04_CODE or anywhere):
    python rag_eval.py            # sweep table + gate verdict + JSON summary
    python rag_eval.py --json     # JSON only
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from statistics import mean

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rag_retrieval import Document, RetrievalIndex, index_documents

EVAL_SET_PATH = Path(__file__).resolve().parents[1] / "05_TEST" / "EVAL_SET.json"


def load_eval_set(path: Path = EVAL_SET_PATH) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def hit_at_k(retrieved: list[str], expected: list[str], k: int) -> int:
    return int(any(s in expected for s in retrieved[:k]))


def precision_at_k(retrieved: list[str], expected: list[str], k: int) -> float:
    top = retrieved[:k]
    if not top:
        return 0.0
    return sum(1 for s in top if s in expected) / len(top)


def recall_at_k(retrieved: list[str], expected: list[str], k: int) -> float:
    got = {s for s in retrieved[:k] if s in expected}
    return len(got) / len(set(expected))


def mrr(retrieved: list[str], expected: list[str]) -> float:
    for rank, s in enumerate(retrieved, start=1):
        if s in expected:
            return 1.0 / rank
    return 0.0


def evaluate(index: RetrievalIndex, labeled: list[dict], no_answer: list[str],
             top_k: int, min_score: float) -> dict:
    hits, precs, recs, mrrs = [], [], [], []
    start = time.perf_counter()
    for item in labeled:
        results = index.search(item["query"], top_k=top_k, min_score=min_score)
        retrieved = [r.source_id for r in results]
        expected = item["expected"]
        hits.append(hit_at_k(retrieved, expected, top_k))
        precs.append(precision_at_k(retrieved, expected, top_k))
        recs.append(recall_at_k(retrieved, expected, top_k))
        mrrs.append(mrr(retrieved, expected))
    latency_ms = (time.perf_counter() - start) * 1000.0 / max(1, len(labeled))
    abstained = [
        0 if index.search(q, top_k=top_k, min_score=min_score) else 1
        for q in no_answer
    ]
    return {
        "min_score": min_score,
        "n_labeled": len(labeled),
        "n_no_answer": len(no_answer),
        "hit_at_5": mean(hits) if hits else 0.0,
        "precision_at_5": mean(precs) if precs else 0.0,
        "recall_at_5": mean(recs) if recs else 0.0,
        "mrr": mean(mrrs) if mrrs else 0.0,
        "no_answer_accuracy": mean(abstained) if abstained else 0.0,
        "avg_latency_ms": round(latency_ms, 3),
    }


def sweep(index: RetrievalIndex, labeled: list[dict], no_answer: list[str],
          top_k: int, low: float = 0.05, high: float = 0.60, step: float = 0.05) -> list[dict]:
    rows = []
    t = low
    while t <= high + 1e-9:
        rows.append(evaluate(index, labeled, no_answer, top_k, round(t, 2)))
        t += step
    return rows


def gate_verdict(metrics: dict, baseline: dict) -> tuple[bool, list[str]]:
    failures = []
    for key, floor in baseline.items():
        if metrics.get(key, 0.0) < floor:
            failures.append(f"{key}={metrics.get(key, 0.0):.3f} < baseline {floor}")
    return (not failures), failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="print JSON summary only")
    args = parser.parse_args()

    data = load_eval_set()
    docs = [Document(d["source_id"], d["title"], d["text"]) for d in data["documents"]]
    known = {d["source_id"] for d in data["documents"]}
    for item in data["labeled_queries"]:
        unknown = [s for s in item["expected"] if s not in known]
        if unknown:
            raise ValueError(f"labeled query references unknown source: {unknown}")

    chunks = index_documents(docs, **data["chunking"])
    index = RetrievalIndex(chunks)
    top_k = data["retrieval"]["top_k"]
    op = data["retrieval"]["operating_min_score"]

    rows = sweep(index, data["labeled_queries"], data["no_answer_queries"], top_k)
    metrics = evaluate(index, data["labeled_queries"], data["no_answer_queries"], top_k, op)
    passed, failures = gate_verdict(metrics, data["baseline_gate"])
    verdict = "PASS" if passed else "FAIL"

    if args.json:
        print(json.dumps({"operating": metrics, "verdict": verdict, "sweep": rows}, ensure_ascii=False, indent=2))
    else:
        print("min_score  hit@5  prec@5  rec@5   mrr    no_ans")
        for r in rows:
            print(f"{r['min_score']:<9}  {r['hit_at_5']:<5.3f}  {r['precision_at_5']:<6.3f}  {r['recall_at_5']:<6.3f}  {r['mrr']:<5.3f}  {r['no_answer_accuracy']:<6.3f}")
        print()
        print("Operating threshold:", op)
        print(json.dumps(metrics, ensure_ascii=False, indent=2))
        print("Baseline gate:", verdict)
        for f in failures:
            print("  BELOW BASELINE:", f)

    if not passed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
