"""Work 103 — Labeled retrieval evaluation harness (v2).

Loads and STRICTLY validates the labeled evaluation set, then measures
retrieval quality: Precision@k, Recall@k, Hit@k, MRR, answered_rate
(false-abstention guard), no-answer accuracy (easy + near-miss reported
separately), and latency. Sweeps min_score thresholds and enforces the
baseline gate: exit code 1 if ANY metric falls below the floors in
EVAL_SET.json or if the set fails schema validation.

Usage:
    python rag_eval.py [--json]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from statistics import mean
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rag_retrieval import Document, RetrievalIndex, index_documents

EVAL_SET_PATH = Path(__file__).resolve().parents[1] / "05_TEST" / "EVAL_SET.json"

REQUIRED_TOP_KEYS = (
    "version", "chunking", "retrieval", "baseline_gate",
    "documents", "labeled_queries", "no_answer_queries",
)
GATE_KEYS = (
    "hit_at_5", "recall_at_5", "mrr", "no_answer_accuracy",
    "precision_at_5", "answered_rate",
)
MIN_LABELED = 10
MIN_NO_ANSWER = 5


def _require(cond: bool, message: str) -> None:
    if not cond:
        raise ValueError(f"EVAL_SET invalid: {message}")


def validate_eval_set(data: Any) -> None:
    """Strict schema validation. Raises ValueError on any violation."""
    _require(isinstance(data, dict), "top level must be an object")
    for key in REQUIRED_TOP_KEYS:
        _require(key in data, f"missing required key: {key}")

    chunking = data["chunking"]
    _require(isinstance(chunking, dict), "chunking must be an object")
    _require(isinstance(chunking.get("max_chars"), int) and chunking["max_chars"] > 0,
             "chunking.max_chars must be a positive int")
    _require(isinstance(chunking.get("overlap_chars"), int)
             and 0 <= chunking["overlap_chars"] < chunking["max_chars"],
             "chunking.overlap_chars must be >= 0 and < max_chars")

    retrieval = data["retrieval"]
    _require(isinstance(retrieval, dict), "retrieval must be an object")
    _require(isinstance(retrieval.get("top_k"), int) and retrieval["top_k"] >= 1,
             "retrieval.top_k must be an int >= 1")
    _require(isinstance(retrieval.get("operating_min_score"), (int, float))
             and 0.0 < retrieval["operating_min_score"] < 1.0,
             "retrieval.operating_min_score must be in (0, 1)")

    gate = data["baseline_gate"]
    _require(isinstance(gate, dict), "baseline_gate must be an object")
    for key in GATE_KEYS:
        _require(key in gate, f"baseline_gate missing key: {key}")
        _require(isinstance(gate[key], (int, float)) and 0.0 <= gate[key] <= 1.0,
                 f"baseline_gate.{key} must be numeric in [0, 1]")

    docs = data["documents"]
    _require(isinstance(docs, list) and len(docs) > 0, "documents must be a non-empty list")
    seen_ids = set()
    for d in docs:
        _require(isinstance(d, dict), "each document must be an object")
        for field in ("source_id", "title", "text"):
            _require(isinstance(d.get(field), str) and d[field].strip(),
                     f"document field {field} must be a non-empty string")
        _require(d["source_id"] not in seen_ids,
                 f"duplicate source_id: {d['source_id']}")
        seen_ids.add(d["source_id"])

    labeled = data["labeled_queries"]
    _require(isinstance(labeled, list) and len(labeled) >= MIN_LABELED,
             f"labeled_queries must have at least {MIN_LABELED} items")
    for item in labeled:
        _require(isinstance(item, dict), "each labeled query must be an object")
        _require(isinstance(item.get("query"), str) and item["query"].strip(),
                 "labeled query must be a non-empty string")
        expected = item.get("expected")
        _require(isinstance(expected, list) and len(expected) > 0,
                 "labeled query expected must be a non-empty list")
        for s in expected:
            _require(s in seen_ids, f"labeled query references unknown source: {s}")

    no_answer = data["no_answer_queries"]
    _require(isinstance(no_answer, list) and len(no_answer) >= MIN_NO_ANSWER,
             f"no_answer_queries must have at least {MIN_NO_ANSWER} items")
    for item in no_answer:
        _require(isinstance(item, dict), "each no-answer query must be an object")
        _require(isinstance(item.get("query"), str) and item["query"].strip(),
                 "no-answer query must be a non-empty string")
        _require(item.get("kind") in ("easy", "near_miss"),
                 "no-answer kind must be easy or near_miss")


def load_eval_set(path: Path = EVAL_SET_PATH) -> dict:
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    validate_eval_set(data)
    return data


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


def evaluate(index: RetrievalIndex, labeled: list[dict], no_answer: list[dict],
             top_k: int, min_score: float) -> dict:
    hits, precs, recs, mrrs, answered = [], [], [], [], []
    misses: list[str] = []
    for item in labeled:
        results = index.search(item["query"], top_k=top_k, min_score=min_score)
        retrieved = [r.source_id for r in results]
        expected = item["expected"]
        hits.append(hit_at_k(retrieved, expected, top_k))
        precs.append(precision_at_k(retrieved, expected, top_k))
        recs.append(recall_at_k(retrieved, expected, top_k))
        mrrs.append(mrr(retrieved, expected))
        answered.append(1 if results else 0)
        # False abstention is recorded independently of ranking misses:
        # an empty result set is a false abstention even when the query would
        # also be counted as a ranking miss.
        if not results:
            misses.append(f"(false abstention) {item['query']}")
        elif not hit_at_k(retrieved, expected, top_k):
            misses.append(item["query"])

    start = time.perf_counter()
    for item in labeled:
        index.search(item["query"], top_k=top_k, min_score=min_score)
    latency_ms = (time.perf_counter() - start) * 1000.0 / max(1, len(labeled))

    abstained = []
    near_miss_leaks: list[str] = []
    easy_leaks: list[str] = []
    for item in no_answer:
        q = item["query"]
        empty = not index.search(q, top_k=top_k, min_score=min_score)
        abstained.append(1 if empty else 0)
        if not empty:
            if item["kind"] == "near_miss":
                near_miss_leaks.append(q)
            else:
                easy_leaks.append(q)

    return {
        "min_score": min_score,
        "n_labeled": len(labeled),
        "n_no_answer": len(no_answer),
        "hit_at_5": mean(hits) if hits else 0.0,
        "precision_at_5": mean(precs) if precs else 0.0,
        "recall_at_5": mean(recs) if recs else 0.0,
        "mrr": mean(mrrs) if mrrs else 0.0,
        "answered_rate": mean(answered) if answered else 0.0,
        "no_answer_accuracy": mean(abstained) if abstained else 0.0,
        "easy_leaks": easy_leaks,
        "near_miss_leaks": near_miss_leaks,
        "ranked_misses": misses,
        "avg_latency_ms": round(latency_ms, 3),
    }


def sweep(index: RetrievalIndex, labeled: list[dict], no_answer: list[dict],
          top_k: int, low: float = 0.05, high: float = 0.60, step: float = 0.05) -> list[dict]:
    rows = []
    t = low
    while t <= high + 1e-9:
        rows.append(evaluate(index, labeled, no_answer, top_k, round(t, 2)))
        t += step
    return rows


def gate_verdict(metrics: dict, baseline: dict) -> tuple[bool, list[str]]:
    failures = []
    for key in GATE_KEYS:
        if metrics.get(key, 0.0) < baseline[key]:
            failures.append(f"{key}={metrics.get(key, 0.0):.3f} < baseline {baseline[key]}")
    return (not failures), failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="print JSON summary only")
    args = parser.parse_args()

    data = load_eval_set()  # load + validate; raises on any schema violation
    docs = [Document(d["source_id"], d["title"], d["text"]) for d in data["documents"]]
    chunks = index_documents(docs, **data["chunking"])
    index = RetrievalIndex(chunks)
    top_k = data["retrieval"]["top_k"]
    op = data["retrieval"]["operating_min_score"]

    rows = sweep(index, data["labeled_queries"], data["no_answer_queries"], top_k)
    metrics = evaluate(index, data["labeled_queries"], data["no_answer_queries"], top_k, op)
    passed, failures = gate_verdict(metrics, data["baseline_gate"])
    verdict = "PASS" if passed else "FAIL"

    if args.json:
        print(json.dumps({"operating": metrics, "verdict": verdict,
                          "sweep": [{k: r[k] for k in ("min_score", "hit_at_5", "precision_at_5",
                                                        "recall_at_5", "mrr", "answered_rate",
                                                        "no_answer_accuracy")} for r in rows]},
                         ensure_ascii=False, indent=2))
    else:
        print("min_score  hit@5  prec@5  rec@5   mrr    ansrd  no_ans")
        for r in rows:
            print(f"{r['min_score']:<9}  {r['hit_at_5']:<5.3f}  {r['precision_at_5']:<6.3f}  "
                  f"{r['recall_at_5']:<6.3f}  {r['mrr']:<5.3f}  {r['answered_rate']:<5.3f}  {r['no_answer_accuracy']:<6.3f}")
        print()
        print("Operating threshold:", op)
        print(json.dumps({k: v for k, v in metrics.items() if not isinstance(v, list)},
                         ensure_ascii=False, indent=2))
        if metrics["ranked_misses"]:
            print("Ranked misses:", metrics["ranked_misses"])
        if metrics["easy_leaks"]:
            print("Easy no-answer leaks:", metrics["easy_leaks"])
        if metrics["near_miss_leaks"]:
            print("Near-miss leaks (known lexical gap, evidence for extension gate):", metrics["near_miss_leaks"])
        print("Baseline gate:", verdict)
        for f in failures:
            print("  BELOW BASELINE:", f)

    if not passed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
