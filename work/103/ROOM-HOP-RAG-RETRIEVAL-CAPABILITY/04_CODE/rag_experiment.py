"""Controlled Work 103 retrieval experiments; never changes production defaults.

Runs the same committed labeled set and corpus against:
- baseline BM25-lite (K1=1.2, B=0.75)
- conservative query normalization (NFKC + whitespace normalization)
- BM25 parameter variants
- hybrid score (BM25-lite + unique-token coverage)

All variants get a full threshold sweep. This is experimental evidence, not
a release gate. Scores are ranking signals, not probabilities.
"""
from __future__ import annotations

import json
import sys
import time
import unicodedata
from dataclasses import replace
from pathlib import Path
from statistics import mean

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rag_retrieval as rr
from rag_eval import load_eval_set, evaluate
from rag_retrieval import Document, RetrievalIndex, SearchResult, index_documents, tokenize

THRESHOLDS = [round(x / 100, 2) for x in range(20, 71, 5)]
K = 5


class QueryNormalizedIndex:
    def __init__(self, base):
        self.base = base
        self.chunks = base.chunks

    def search(self, query, top_k=5, min_score=0.15):
        normalized = " ".join(unicodedata.normalize("NFKC", query).split())
        return self.base.search(normalized, top_k=top_k, min_score=min_score)


class HybridIndex:
    """Blend BM25 score and query-token coverage; threshold is swept independently."""
    def __init__(self, base, bm25_weight=0.75):
        self.base = base
        self.chunks = base.chunks
        self.bm25_weight = bm25_weight

    def search(self, query, top_k=5, min_score=0.15):
        terms = set(tokenize(query))
        if not terms:
            return []
        # Retrieve all scored chunks first so hybrid ranking is not truncated by
        # the BM25 top-k window before blending.
        candidates = self.base.search(query, top_k=max(1, len(self.chunks)), min_score=0.0)
        blended = []
        for result in candidates:
            coverage = len(terms.intersection(tokenize(result.text))) / len(terms)
            score = self.bm25_weight * result.score + (1.0 - self.bm25_weight) * coverage
            if score >= min_score:
                blended.append(replace(result, score=round(score, 6)))
        blended.sort(key=lambda item: (-item.score, item.source_id, item.start_line, item.chunk_id))
        return blended[:top_k]


def make_index(data, k1=1.2, b=0.75):
    docs = [Document(d["source_id"], d["title"], d["text"]) for d in data["documents"]]
    chunks = index_documents(docs, **data["chunking"])
    # Existing implementation reads K1/B module constants during search.
    old = (rr.K1, rr.B)
    rr.K1, rr.B = k1, b
    return RetrievalIndex(chunks), old


def summarize(index, data, threshold):
    m = evaluate(index, data["labeled_queries"], data["no_answer_queries"], K, threshold)
    # Independent top-1 metric; does not replace the evaluator's multi-label metrics.
    top1 = []
    start = time.perf_counter()
    for item in data["labeled_queries"]:
        got = index.search(item["query"], top_k=K, min_score=threshold)
        top1.append(int(bool(got) and got[0].source_id in item["expected"]))
    latency = (time.perf_counter() - start) * 1000 / max(1, len(top1))
    return {
        "threshold": threshold,
        "top1_accuracy": round(mean(top1), 4),
        "hit_at_5": round(m["hit_at_5"], 4),
        "precision_at_5": round(m["precision_at_5"], 4),
        "recall_at_5": round(m["recall_at_5"], 4),
        "mrr": round(m["mrr"], 4),
        "answered_rate": round(m["answered_rate"], 4),
        "no_answer_accuracy": round(m["no_answer_accuracy"], 4),
        "near_miss_leaks": m["near_miss_leaks"],
        "avg_latency_ms": round(latency, 3),
    }


def main():
    data = load_eval_set()
    variants = [
        ("baseline_bm25_k1_1.2_b_0.75", 1.2, 0.75, "bm25"),
        ("query_normalization_control", 1.2, 0.75, "normalize"),
        ("bm25_k1_0.8_b_0.5", 0.8, 0.5, "bm25"),
        ("bm25_k1_1.6_b_0.9", 1.6, 0.9, "bm25"),
        ("hybrid_75pct_bm25_25pct_coverage", 1.2, 0.75, "hybrid"),
    ]
    report = {
        "experiment": "work-103-controlled-retrieval-v1",
        "dataset_version": data["version"],
        "labeled_queries": len(data["labeled_queries"]),
        "no_answer_queries": len(data["no_answer_queries"]),
        "corpus_documents": len(data["documents"]),
        "chunking": data["chunking"],
        "thresholds": THRESHOLDS,
        "notes": [
            "Same committed corpus and labels for every variant.",
            "Thresholds are swept per variant; scores are not calibrated probabilities.",
            "Normalization is deliberately conservative (NFKC + whitespace only).",
            "Hybrid is a lightweight lexical coverage blend, not semantic embeddings.",
            "No variant is promoted automatically; compare all metrics and latency.",
        ],
        "variants": {},
    }
    for name, k1, b, kind in variants:
        base, old = make_index(data, k1=k1, b=b)
        try:
            index = QueryNormalizedIndex(base) if kind == "normalize" else (
                HybridIndex(base) if kind == "hybrid" else base
            )
            report["variants"][name] = [summarize(index, data, t) for t in THRESHOLDS]
        finally:
            rr.K1, rr.B = old
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
