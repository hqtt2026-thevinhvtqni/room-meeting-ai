"""Supplemental diagnostic: distinguish empty retrieval from grounded evidence of absence.

This report-only analysis does not alter rag_eval.py's strict no-answer gate.
It uses a manually reviewed mapping of queries whose source explicitly says the
requested detail is unspecified. It exits 0 so the strict baseline gate remains
the sole release gate.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "04_CODE"))
from rag_eval import load_eval_set
from rag_retrieval import Document, RetrievalIndex, index_documents

EVAL_PATH = ROOT / "05_TEST" / "EVAL_SET_CORPUS_V4_V3.json"

# Query IDs reviewed against exact source text. These are evidence for abstention,
# not evidence that the requested answer itself is present.
DOCUMENTED_ABSENCE = {
    "Q004": ["00_CORPUS/network.md"],
    "Q008": ["00_CORPUS/sales.md"],
    "Q016": ["03_ARCHITECTURE/RAG_RETRIEVAL_ARCHITECTURE.md"],
    "Q044": ["00_CORPUS/architecture.md", "03_ARCHITECTURE/RAG_RETRIEVAL_ARCHITECTURE.md"],
    "Q046": ["03_ARCHITECTURE/RAG_RETRIEVAL_ARCHITECTURE.md"],
}


def main() -> int:
    data = load_eval_set(EVAL_PATH)
    docs = [Document(d["source_id"], d["title"], d["text"]) for d in data["documents"]]
    index = RetrievalIndex(index_documents(docs, **data["chunking"]))
    rows = []
    for threshold in (0.25, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60):
        strict = []
        grounded = []
        details = []
        for item in data["no_answer_queries"]:
            results = index.search(item["query"], top_k=data["retrieval"]["top_k"], min_score=threshold)
            sources = sorted({r.source_id for r in results})
            explicit = DOCUMENTED_ABSENCE.get(item.get("query_id", ""), [])
            strict_ok = not results
            grounded_ok = strict_ok or (bool(explicit) and bool(results) and all(s in explicit for s in sources))
            strict.append(int(strict_ok))
            grounded.append(int(grounded_ok))
            details.append({
                "query_id": item.get("query_id"),
                "query": item["query"],
                "strict_empty_retrieval_correct": strict_ok,
                "grounded_abstention_correct": grounded_ok,
                "documented_absence_sources": explicit,
                "retrieved_sources": sources,
                "top_results": [
                    {"source_id": r.source_id, "chunk_id": r.chunk_id, "score": r.score}
                    for r in results
                ],
            })
        rows.append({
            "min_score": threshold,
            "strict_no_answer_accuracy": mean(strict),
            "grounded_no_answer_accuracy": mean(grounded),
            "strict_correct_count": sum(strict),
            "grounded_correct_count": sum(grounded),
            "n_no_answer": len(strict),
            "details": details,
        })
    print(json.dumps({
        "diagnostic_only": True,
        "baseline_gate_unchanged": True,
        "interpretation": "Grounded accuracy credits a non-empty retrieval only when every returned source is explicitly annotated as evidence that the requested detail is unspecified. This is supplemental, not a replacement for strict no-answer accuracy.",
        "thresholds": rows,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
