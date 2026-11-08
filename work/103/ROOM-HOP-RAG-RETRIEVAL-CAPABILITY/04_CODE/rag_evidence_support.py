"""Work 103 — Evidence-support decision stage (v1, Gate B prototype).

Deterministic five-state support assessment consumed AFTER lexical
retrieval. Implements the Evidence-Support Stage Contract V3
(03_ARCHITECTURE/EVIDENCE_SUPPORT_STAGE_CONTRACT_V3.md).

Decisions (locked enum):
    SUPPORTED, EXPLICITLY_UNSPECIFIED, CONTRADICTED,
    CONFLICTING_EVIDENCE, INSUFFICIENT_EVIDENCE

Locked decision precedence:
    provenance validation -> absence -> negation -> conflict -> support
    -> insufficient evidence. Earlier stages short-circuit later ones.

Independence requirement (contract section 4 / case T3):
    the retrieval score may order candidates only; it never appears in,
    weights, or short-circuits the support decision. All matching runs
    over span text and declared provenance/scopes only.

This is an isolated Sandbox prototype. It is not wired into Core :8000
or MCP :8020, and it changes no retrieval code, fixture, threshold, or
label set.

Usage:
    python rag_evidence_support.py [--decision-set PATH] [--json]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

DEFAULT_DECISION_SET_PATH = (
    Path(__file__).resolve().parents[1] / "05_TEST" / "EVIDENCE_SUPPORT_DECISION_SET_V1.json"
)

DECISIONS = (
    "SUPPORTED",
    "EXPLICITLY_UNSPECIFIED",
    "CONTRADICTED",
    "CONFLICTING_EVIDENCE",
    "INSUFFICIENT_EVIDENCE",
)

REASON_CODES = (
    "NO_CANDIDATES",
    "PROVENANCE_INVALID",
    "ABSENCE_SCOPE_COVERED",
    "ABSENCE_SCOPE_EXCEEDS_QUERY",
    "SCOPE_LIMITED_OUTPUT_UNAVAILABLE",
    "NEGATED_BY_SOURCE",
    "CONFLICTING_VALUES",
    "SUPPORTED_BY_SOURCE",
    "NO_ADEQUATE_SUPPORT",
)

PATTERN_GROUPS = (
    "support_patterns", "absence_patterns", "negation_patterns", "value_patterns",
)

REQUIRED_ROW_KEYS = (
    "row_id", "case_family", "query", "expected_decision", "fact",
    "candidates", "rationale", "adjudication",
)

REQUIRED_TOP_KEYS = (
    "dataset_id", "version", "required_case_families", "required_decisions",
    "scope_matching_rule", "rows", "adjudication_record",
)


def _require(cond: bool, message: str) -> None:
    if not cond:
        raise ValueError(f"DECISION_SET invalid: {message}")


@dataclass(frozen=True)
class SupportDecision:
    """Result of one support assessment. Citations are exact provenance."""

    decision: str
    reason_code: str
    citations: tuple
    scope_limited: bool
    dropped_candidates: tuple

    def to_dict(self) -> dict:
        return {
            "decision": self.decision,
            "reason_code": self.reason_code,
            "citations": list(self.citations),
            "scope_limited": self.scope_limited,
            "dropped_candidates": list(self.dropped_candidates),
        }


def compile_pattern(pattern: Any) -> "re.Pattern[str]":
    """Compile a declared pattern. Patterns are REVIEWED DATA, not code."""
    _require(isinstance(pattern, dict), "pattern must be an object")
    _require(isinstance(pattern.get("regex"), str) and pattern["regex"].strip(),
             "pattern.regex must be a non-empty string")
    try:
        return re.compile(pattern["regex"], re.IGNORECASE)
    except re.error as exc:
        raise ValueError(
            f"DECISION_SET invalid: pattern.regex is not a valid regex: {exc}"
        ) from exc


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def candidate_provenance_valid(candidate: Any) -> bool:
    """Provenance gate (T5): no usable evidence without complete provenance."""
    if not isinstance(candidate, dict):
        return False
    return (
        isinstance(candidate.get("source_id"), str) and bool(candidate["source_id"].strip())
        and isinstance(candidate.get("chunk_id"), str) and bool(candidate["chunk_id"].strip())
        and isinstance(candidate.get("text"), str) and bool(candidate["text"].strip())
        and _is_int(candidate.get("start_line")) and _is_int(candidate.get("end_line"))
        and candidate["start_line"] >= 1
        and candidate["end_line"] >= candidate["start_line"]
    )


def scope_covers(source_scope: str, query_scope: str) -> bool:
    """Locked scope rule: a scope covers a query scope iff equal or '*'."""
    return source_scope == query_scope or source_scope == "*"


def _candidate_label(candidate: dict) -> str:
    return candidate.get("source_id") or "(missing source_id)"


def _citation(candidate: dict) -> dict:
    return {
        "source_id": candidate["source_id"],
        "chunk_id": candidate["chunk_id"],
        "start_line": candidate["start_line"],
        "end_line": candidate["end_line"],
    }


def assess_support(query: str, candidates: list, fact: dict,
                   scope_limited_answers_enabled: bool = True) -> SupportDecision:
    """Assess support for one fact request from retrieved candidates.

    The candidate `score` field is accepted for interface compatibility and
    is deliberately never read here (contract section 4: independence).
    """
    if not (isinstance(query, str) and query.strip()):
        raise ValueError("query must be a non-empty string")
    if not isinstance(candidates, list):
        raise ValueError("candidates must be a list")
    if not isinstance(fact, dict):
        raise ValueError("fact must be an object")
    if not (isinstance(fact.get("fact_id"), str) and fact["fact_id"].strip()):
        raise ValueError("fact.fact_id must be a non-empty string")
    if not (isinstance(fact.get("query_scope"), str) and fact["query_scope"].strip()):
        raise ValueError("fact.query_scope must be a non-empty string")

    usable = [c for c in candidates if candidate_provenance_valid(c)]
    dropped = tuple(_candidate_label(c) for c in candidates
                    if not candidate_provenance_valid(c))

    if not candidates:
        return SupportDecision("INSUFFICIENT_EVIDENCE", "NO_CANDIDATES", (), False, dropped)
    if not usable:
        return SupportDecision("INSUFFICIENT_EVIDENCE", "PROVENANCE_INVALID", (), False, dropped)

    # Stage 1 — explicit absence statements (EXPLICITLY_UNSPECIFIED vs fail-closed).
    for pattern in fact.get("absence_patterns") or []:
        compiled = compile_pattern(pattern)
        for candidate in usable:
            if compiled.search(candidate["text"]):
                if scope_limited_answers_enabled:
                    limited = ("source_scope" in pattern
                               and not scope_covers(pattern["source_scope"],
                                                    fact["query_scope"]))
                    reason = ("ABSENCE_SCOPE_EXCEEDS_QUERY" if limited
                              else "ABSENCE_SCOPE_COVERED")
                    return SupportDecision("EXPLICITLY_UNSPECIFIED", reason,
                                           (_citation(candidate),), limited, dropped)
                return SupportDecision("INSUFFICIENT_EVIDENCE",
                                       "SCOPE_LIMITED_OUTPUT_UNAVAILABLE", (), False, dropped)

    # Stage 2 — direct negation of the query proposition.
    for pattern in fact.get("negation_patterns") or []:
        compiled = compile_pattern(pattern)
        for candidate in usable:
            if compiled.search(candidate["text"]):
                return SupportDecision("CONTRADICTED", "NEGATED_BY_SOURCE",
                                       (_citation(candidate),), False, dropped)

    # Stage 3 — conflicting values for the same fact within one value scope.
    values_by_scope: dict = {}
    for pattern in fact.get("value_patterns") or []:
        compiled = compile_pattern(pattern)
        value_scope = pattern.get("value_scope", "default")
        bucket = values_by_scope.setdefault(value_scope, set())
        for candidate in usable:
            if value_scope != "default" and candidate.get("scope", "default") != value_scope:
                continue
            match = compiled.search(candidate["text"])
            if match:
                raw = match.group(1) if match.groups() else match.group(0)
                bucket.add(raw.strip().casefold())
    for value_scope, values in values_by_scope.items():
        if len(values) >= 2:
            return SupportDecision("CONFLICTING_EVIDENCE", "CONFLICTING_VALUES", (), False, dropped)

    # Stage 4 — direct support.
    for pattern in fact.get("support_patterns") or []:
        compiled = compile_pattern(pattern)
        for candidate in usable:
            if compiled.search(candidate["text"]):
                return SupportDecision("SUPPORTED", "SUPPORTED_BY_SOURCE",
                                       (_citation(candidate),), False, dropped)

    return SupportDecision("INSUFFICIENT_EVIDENCE", "NO_ADEQUATE_SUPPORT", (), False, dropped)


def validate_decision_set(data: Any) -> None:
    """Strict schema validation. Raises ValueError on any violation."""
    _require(isinstance(data, dict), "top level must be an object")
    for key in REQUIRED_TOP_KEYS:
        _require(key in data, f"missing required key: {key}")
    _require(isinstance(data["dataset_id"], str) and data["dataset_id"].strip(),
             "dataset_id must be a non-empty string")
    _require(isinstance(data["required_case_families"], list) and data["required_case_families"],
             "required_case_families must be a non-empty list")
    _require(isinstance(data["required_decisions"], list) and data["required_decisions"],
             "required_decisions must be a non-empty list")
    for decision in data["required_decisions"]:
        _require(decision in DECISIONS, f"required_decisions contains unknown decision: {decision}")
    _require(isinstance(data["scope_matching_rule"], str) and data["scope_matching_rule"].strip(),
             "scope_matching_rule must be a non-empty string")

    rows = data["rows"]
    _require(isinstance(rows, list) and len(rows) >= len(data["required_case_families"]),
             "rows must be a list covering every required case family")

    seen_row_ids = set()
    counted_families = set()
    counted_decisions = set()
    for row in rows:
        _require(isinstance(row, dict), "each row must be an object")
        for key in REQUIRED_ROW_KEYS:
            _require(key in row, f"row missing required key: {key}")
        _require(row["row_id"] not in seen_row_ids, f"duplicate row_id: {row['row_id']}")
        seen_row_ids.add(row["row_id"])
        _require(isinstance(row["query"], str) and row["query"].strip(),
                 f"row {row['row_id']}: query must be a non-empty string")
        _require(row["expected_decision"] in DECISIONS,
                 f"row {row['row_id']}: unknown expected_decision")
        _require(isinstance(row["case_family"], str) and row["case_family"].strip(),
                 f"row {row['row_id']}: case_family must be a non-empty string")
        _require(isinstance(row.get("gate_counted"), bool),
                 f"row {row['row_id']}: gate_counted must be a boolean")

        fact = row["fact"]
        _require(isinstance(fact, dict), f"row {row['row_id']}: fact must be an object")
        _require(isinstance(fact.get("fact_id"), str) and fact["fact_id"].strip(),
                 f"row {row['row_id']}: fact.fact_id must be a non-empty string")
        _require(isinstance(fact.get("query_scope"), str) and fact["query_scope"].strip(),
                 f"row {row['row_id']}: fact.query_scope must be a non-empty string")
        for group in PATTERN_GROUPS:
            patterns = fact.get(group) or []
            _require(isinstance(patterns, list), f"row {row['row_id']}: fact.{group} must be a list")
            for pattern in patterns:
                compile_pattern(pattern)  # raises ValueError on malformed pattern

        _require(isinstance(row["candidates"], list),
                 f"row {row['row_id']}: candidates must be a list")
        for candidate in row["candidates"]:
            _require(isinstance(candidate, dict),
                     f"row {row['row_id']}: each candidate must be an object")

        _require(isinstance(row["rationale"], str) and row["rationale"].strip(),
                 f"row {row['row_id']}: rationale must be a non-empty string")
        adjudication = row["adjudication"]
        _require(isinstance(adjudication, dict), f"row {row['row_id']}: adjudication must be an object")
        _require(isinstance(adjudication.get("author"), str) and adjudication["author"].strip(),
                 f"row {row['row_id']}: adjudication.author must be a non-empty string")
        reviewer = adjudication.get("independent_reviewer")
        _require(reviewer is None or isinstance(reviewer, str),
                 f"row {row['row_id']}: adjudication.independent_reviewer must be a string or null")

        if row["gate_counted"]:
            counted_families.add(row["case_family"])
            counted_decisions.add(row["expected_decision"])
        else:
            _require(adjudication.get("status") == "PENDING_INDEPENDENT_ADJUDICATION",
                     f"row {row['row_id']}: non-gate row must be PENDING_INDEPENDENT_ADJUDICATION")

    for family in data["required_case_families"]:
        _require(family in counted_families,
                 f"coverage gap: no gate-counted row for case family {family}")
    for decision in data["required_decisions"]:
        _require(decision in counted_decisions,
                 f"coverage gap: no gate-counted row for decision {decision}")


def load_decision_set(path: Path = DEFAULT_DECISION_SET_PATH) -> dict:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    validate_decision_set(data)
    return data


def run_decision_set(data: dict) -> dict:
    """Run every gate-counted row; per-case verdicts, no aggregate hiding."""
    results = []
    for row in data["rows"]:
        if not row.get("gate_counted"):
            continue
        decision = assess_support(
            row["query"],
            row["candidates"],
            row["fact"],
            row.get("scope_limited_answers_enabled", True),
        )
        results.append({
            "row_id": row["row_id"],
            "case_family": row["case_family"],
            "expected_decision": row["expected_decision"],
            "actual_decision": decision.decision,
            "reason_code": decision.reason_code,
            "scope_limited": decision.scope_limited,
            "passed": decision.decision == row["expected_decision"],
        })
    passed = bool(results) and all(r["passed"] for r in results)
    return {"passed": passed, "results": results}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--decision-set", type=Path, default=DEFAULT_DECISION_SET_PATH,
                        help="path to an evidence-support decision JSON file")
    parser.add_argument("--json", action="store_true", help="print JSON summary only")
    args = parser.parse_args()

    data = load_decision_set(args.decision_set)  # load + strict validation
    summary = run_decision_set(data)
    pending = [row["row_id"] for row in data["rows"] if not row.get("gate_counted")]

    if args.json:
        payload = {**summary, "pending_rows": pending}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("row    case_family            expected                 actual                   reason")
        for r in summary["results"]:
            print(f"{r['row_id']:<6} {r['case_family']:<22} {r['expected_decision']:<24} "
                  f"{r['actual_decision']:<24} {r['reason_code']}")
        print()
        print("Pending rows (not gate-counted, awaiting independent adjudication):", pending)
        print("Gate B decision-set verdict:", "PASS" if summary["passed"] else "FAIL")
        for r in summary["results"]:
            if not r["passed"]:
                print(f"  FAIL {r['row_id']}: expected {r['expected_decision']}, "
                      f"got {r['actual_decision']} ({r['reason_code']})")
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
