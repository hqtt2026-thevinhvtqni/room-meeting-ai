"""Work 103 — Gate C preparatory experiment (v1, REPORT-ONLY).

Runs the real retrieval pipeline (rag_retrieval RetrievalIndex) at the
corpus fixture operating point, feeds the retrieved spans to the
evidence-support stage (rag_evidence_support.assess_support) with
AUTHORED fact specs (EVIDENCE_SUPPORT_FACT_SPECS_V1.json), and reports
the five-state decision per query.

This harness is a DIAGNOSTIC, not a gate:
- It always exits 0 when the evaluation itself completes (report-only),
  even if every row mismatches its authored ideal decision.
- It exits 1 only on fixture/spec loading or validation errors.
- Ideal decisions in the specs are AUTHORED and PENDING INDEPENDENT
  ADJUDICATION (Ka, DEBT-ES-02). Results are adjudication material.

Independence (contract section 4) is preserved end to end: retrieval
scores order candidates only and are never read by the support decision.

Usage:
    python rag_evidence_support_corpus_eval.py [--fixture PATH] [--specs PATH]
        [--json] [--ci-notice]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

CODE_DIR = Path(__file__).resolve().parent
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from rag_retrieval import Document, RetrievalIndex, index_documents  # noqa: E402
from rag_evidence_support import DECISIONS, assess_support, compile_pattern  # noqa: E402

DEFAULT_FIXTURE_PATH = CODE_DIR.parent / "05_TEST" / "EVAL_SET_CORPUS_V4_V3.json"
DEFAULT_SPECS_PATH = CODE_DIR.parent / "05_TEST" / "EVIDENCE_SUPPORT_FACT_SPECS_V1.json"

# Refusal-to-answer family for the FALSE_ABSTENTION category.
# CONFLICTING_EVIDENCE is deliberately NOT here: the stage found evidence
# and reported a conflict, which is a distinct ideal-mismatch
# (IDEAL_MISMATCH_OTHER), not a refusal to answer.
ABSTAIN_FAMILY = ("EXPLICITLY_UNSPECIFIED", "INSUFFICIENT_EVIDENCE")

CATEGORIES = (
    "MATCH",
    "NO_ANSWER_LEAK",
    "FALSE_ABSTENTION",
    "CONTRADICTION_MISSED",
    "IDEAL_MISMATCH_OTHER",
)


def _require(cond: bool, message: str) -> None:
    if not cond:
        raise ValueError(f"FACT_SPECS invalid: {message}")


def validate_fixture(data: Any) -> None:
    _require(isinstance(data, dict), "fixture top level must be an object")
    for key in ("documents", "chunking", "retrieval", "labeled_queries", "no_answer_queries"):
        _require(key in data, f"fixture missing required key: {key}")
    _require(isinstance(data["documents"], list) and data["documents"],
             "fixture.documents must be a non-empty list")
    for doc in data["documents"]:
        _require(isinstance(doc, dict), "each fixture document must be an object")
        for key in ("source_id", "title", "text"):
            _require(isinstance(doc.get(key), str) and doc[key].strip(),
                     f"fixture document missing non-empty {key}")
    chunking = data["chunking"]
    _require(isinstance(chunking, dict), "fixture.chunking must be an object")
    _require(isinstance(chunking.get("max_chars"), int) and chunking["max_chars"] > 0,
             "fixture.chunking.max_chars must be a positive int")
    _require(isinstance(chunking.get("overlap_chars"), int) and chunking["overlap_chars"] >= 0,
             "fixture.chunking.overlap_chars must be a non-negative int")
    retrieval = data["retrieval"]
    _require(isinstance(retrieval, dict), "fixture.retrieval must be an object")
    _require(isinstance(retrieval.get("top_k"), int) and retrieval["top_k"] >= 1,
             "fixture.retrieval.top_k must be a positive int")
    _require(isinstance(retrieval.get("operating_min_score"), (int, float))
             and 0.0 <= retrieval["operating_min_score"] <= 1.0,
             "fixture.retrieval.operating_min_score must be a number in [0, 1]")
    _require(isinstance(data["labeled_queries"], list), "labeled_queries must be a list")
    _require(isinstance(data["no_answer_queries"], list), "no_answer_queries must be a list")


def build_query_map(fixture: dict) -> dict:
    """Map query_id -> {query, kind} for both groups."""
    queries: dict = {}
    for row in fixture["labeled_queries"]:
        queries[row["query_id"]] = {"query": row["query"], "kind": "ANSWERABLE"}
    for row in fixture["no_answer_queries"]:
        queries[row["query_id"]] = {"query": row["query"], "kind": "NO_ANSWER"}
    return queries


def validate_fact_specs(specs: Any, fixture: dict) -> None:
    """Strict validation of the fact-specs dataset against the fixture."""
    _require(isinstance(specs, dict), "top level must be an object")
    _require(isinstance(specs.get("dataset_id"), str) and specs["dataset_id"].strip(),
             "dataset_id must be a non-empty string")
    _require(isinstance(specs.get("rows"), list) and specs["rows"],
             "rows must be a non-empty list")
    queries = build_query_map(fixture)
    seen = set()
    kinds_covered = set()
    for row in specs["rows"]:
        _require(isinstance(row, dict), "each row must be an object")
        query_id = row.get("query_id")
        _require(isinstance(query_id, str) and query_id.strip(),
                 "row.query_id must be a non-empty string")
        _require(query_id in queries, f"unknown query_id not present in fixture: {query_id}")
        _require(query_id not in seen, f"duplicate query_id: {query_id}")
        seen.add(query_id)
        _require(row.get("ideal_decision") in DECISIONS,
                 f"row {query_id}: unknown ideal_decision")
        fact = row.get("fact")
        _require(isinstance(fact, dict), f"row {query_id}: fact must be an object")
        _require(isinstance(fact.get("fact_id"), str) and fact["fact_id"].strip(),
                 f"row {query_id}: fact.fact_id must be a non-empty string")
        _require(isinstance(fact.get("query_scope"), str) and fact["query_scope"].strip(),
                 f"row {query_id}: fact.query_scope must be a non-empty string")
        for group in ("support_patterns", "absence_patterns", "negation_patterns", "value_patterns"):
            patterns = fact.get(group) or []
            _require(isinstance(patterns, list), f"row {query_id}: fact.{group} must be a list")
            for pattern in patterns:
                compile_pattern(pattern)  # raises ValueError on malformed pattern
        _require(isinstance(row.get("rationale"), str) and row["rationale"].strip(),
                 f"row {query_id}: rationale must be a non-empty string")
        kinds_covered.add(queries[query_id]["kind"])
    _require("ANSWERABLE" in kinds_covered, "coverage gap: no ANSWERABLE row in specs")
    _require("NO_ANSWER" in kinds_covered, "coverage gap: no NO_ANSWER row in specs")


def categorize(fixture_kind: str, ideal: str, actual: str) -> str:
    """Classify one evaluation row (report-only diagnostic taxonomy)."""
    if actual == ideal:
        return "MATCH"
    if fixture_kind == "NO_ANSWER":
        # The strict no-answer leak: an affirmative SUPPORTED answer on a
        # query the adjudicated labels hold to have no answer.
        return "NO_ANSWER_LEAK" if actual == "SUPPORTED" else "IDEAL_MISMATCH_OTHER"
    # ANSWERABLE rows.
    if ideal == "CONTRADICTED":
        return "CONTRADICTION_MISSED"
    if actual in ABSTAIN_FAMILY:
        return "FALSE_ABSTENTION"
    # Remaining mismatches (e.g. SUPPORTED ideal with CONFLICTING_EVIDENCE
    # actual) are distinct evidence-quality failures, not abstentions.
    return "IDEAL_MISMATCH_OTHER"


def run_corpus_eval(fixture: dict, specs: dict) -> dict:
    """Run retrieval + evidence-support for every spec'd query."""
    documents = [
        Document(source_id=doc["source_id"], title=doc["title"], text=doc["text"])
        for doc in fixture["documents"]
    ]
    chunking = fixture["chunking"]
    chunks = index_documents(
        documents,
        max_chars=chunking["max_chars"],
        overlap_chars=chunking["overlap_chars"],
    )
    index = RetrievalIndex(chunks)
    retrieval_config = fixture["retrieval"]
    top_k = retrieval_config["top_k"]
    min_score = retrieval_config["operating_min_score"]
    queries = build_query_map(fixture)

    results = []
    for row in specs["rows"]:
        query_id = row["query_id"]
        meta = queries[query_id]
        found = index.search(meta["query"], top_k=top_k, min_score=min_score)
        candidates = [
            {
                "source_id": r.source_id,
                "chunk_id": r.chunk_id,
                "start_line": r.start_line,
                "end_line": r.end_line,
                "text": r.text,
                "score": r.score,  # interface-compat only; never read by assess_support
            }
            for r in found
        ]
        decision = assess_support(meta["query"], candidates, row["fact"])
        results.append({
            "query_id": query_id,
            "kind": meta["kind"],
            "query": meta["query"],
            "retrieval_count": len(candidates),
            "retrieved": [
                {"source_id": c["source_id"], "chunk_id": c["chunk_id"], "score": c["score"]}
                for c in candidates
            ],
            "decision": decision.decision,
            "reason_code": decision.reason_code,
            "citations": [dict(c) for c in decision.citations],
            "ideal_decision": row["ideal_decision"],
            "category": categorize(meta["kind"], row["ideal_decision"], decision.decision),
        })

    summary = {
        "n_specs": len(results),
        "n_match": sum(1 for r in results if r["category"] == "MATCH"),
        "n_no_answer_leak": sum(1 for r in results if r["category"] == "NO_ANSWER_LEAK"),
        "n_false_abstention": sum(1 for r in results if r["category"] == "FALSE_ABSTENTION"),
        "n_contradiction_missed": sum(1 for r in results if r["category"] == "CONTRADICTION_MISSED"),
        "n_ideal_mismatch_other": sum(1 for r in results if r["category"] == "IDEAL_MISMATCH_OTHER"),
    }
    return {"dataset_id": specs.get("dataset_id"), "report_only": True,
            "adjudication_status": "AUTHORED_PENDING_INDEPENDENT_ADJUDICATION",
            "results": results, "summary": summary}


def _notice(message: str) -> None:
    # GitHub Actions workflow command: surfaces as a check annotation,
    # readable via the checks API without log-download permissions.
    print(f"::notice::{message}")


def print_report(report: dict, as_json: bool, ci_notice: bool) -> None:
    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("query_id kind       ideal                  actual                 reason                 category")
        for r in report["results"]:
            print(f"{r['query_id']:<8} {r['kind']:<10} {r['ideal_decision']:<22} "
                  f"{r['decision']:<22} {r['reason_code']:<22} {r['category']}")
        print()
        s = report["summary"]
        print(f"specs={s['n_specs']} match={s['n_match']} "
              f"no_answer_leak={s['n_no_answer_leak']} "
              f"false_abstention={s['n_false_abstention']} "
              f"contradiction_missed={s['n_contradiction_missed']} "
              f"mismatch_other={s['n_ideal_mismatch_other']}")
        print("REPORT-ONLY diagnostic (Gate C preparatory); exit status unaffected.")
    if ci_notice:
        s = report["summary"]
        _notice(f"work103 evidence-support corpus eval: "
                f"specs={s['n_specs']} match={s['n_match']} "
                f"no_answer_leak={s['n_no_answer_leak']} "
                f"false_abstention={s['n_false_abstention']} "
                f"contradiction_missed={s['n_contradiction_missed']} "
                f"mismatch_other={s['n_ideal_mismatch_other']} "
                f"status={report['adjudication_status']}")
        for r in report["results"]:
            top = (f"{r['retrieved'][0]['source_id']}@{r['retrieved'][0]['score']}"
                   if r["retrieved"] else "none")
            _notice(f"qid={r['query_id']} kind={r['kind']} ideal={r['ideal_decision']} "
                    f"actual={r['decision']} reason={r['reason_code']} "
                    f"category={r['category']} top1={top}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE_PATH)
    parser.add_argument("--specs", type=Path, default=DEFAULT_SPECS_PATH)
    parser.add_argument("--json", action="store_true", help="print JSON report only")
    parser.add_argument("--ci-notice", action="store_true",
                        help="emit GitHub Actions ::notice:: annotations per row")
    args = parser.parse_args()

    try:
        with args.fixture.open(encoding="utf-8") as handle:
            fixture = json.load(handle)
        validate_fixture(fixture)
        with args.specs.open(encoding="utf-8") as handle:
            specs = json.load(handle)
        validate_fact_specs(specs, fixture)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"VALIDATION ERROR: {exc}", file=sys.stderr)
        return 1

    report = run_corpus_eval(fixture, specs)
    print_report(report, as_json=args.json, ci_notice=args.ci_notice)
    return 0  # report-only: never fail CI on evaluation outcomes


if __name__ == "__main__":
    raise SystemExit(main())
