"""Work 103 — Gate B tests for the evidence-support stage (contract V3).

Covers the mandatory per-case suite T1-T7 (with the B1 T4a/T4b split),
the B4 metamorphic score-independence protocol, provenance fail-closed
behaviour (T5), strict schema validation of the committed decision set,
and the per-case (no aggregate hiding) gate runner.
"""

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "04_CODE"))

import rag_evidence_support as res
from rag_evidence_support import (
    DECISIONS,
    REASON_CODES,
    assess_support,
    candidate_provenance_valid,
    compile_pattern,
    load_decision_set,
    run_decision_set,
    scope_covers,
    validate_decision_set,
)

SALES_FULL_TEXT = (
    "# Quy trình xác nhận đơn hàng xi măng\n\n"
    "## Xác nhận đơn hàng\n"
    "Khi tiếp nhận yêu cầu từ khách hàng, nhân viên kinh doanh cần thực hiện hai bước xác nhận chính:\n"
    "1. Xác nhận lịch giao hàng cho đơn đặt hàng của khách hàng (Customer order delivery schedule).\n"
    "2. Xác nhận số lượng xi măng trong đơn hàng (Confirm cement quantity).\n\n"
    "*Lưu ý:* Tài liệu này không quy định chi tiết về quy trình xử lý khi khách hàng yêu cầu "
    "thay đổi lịch giao hàng, cũng như không chỉ định tên hoặc vai trò cụ thể của người phụ trách "
    "phê duyệt thay đổi."
)


class CommittedSetTests(unittest.TestCase):
    """The committed decision set must validate, run, and pass per case."""

    @classmethod
    def setUpClass(cls):
        cls.data = load_decision_set()  # strict validation runs here

    def test_every_expected_decision_enum_is_known(self):
        for row in self.data["rows"]:
            self.assertIn(row["expected_decision"], DECISIONS)

    def test_all_required_families_covered_by_gate_counted_rows(self):
        counted = {r["case_family"] for r in self.data["rows"] if r["gate_counted"]}
        for family in self.data["required_case_families"]:
            self.assertIn(family, counted)

    def test_all_required_decisions_covered(self):
        counted = {r["expected_decision"] for r in self.data["rows"] if r["gate_counted"]}
        for decision in self.data["required_decisions"]:
            self.assertIn(decision, counted)

    def test_gate_runner_passes_every_case_individually(self):
        summary = run_decision_set(self.data)
        self.assertTrue(summary["passed"])
        for result in summary["results"]:
            self.assertTrue(result["passed"], f"case {result['row_id']} failed")

    def test_pending_rows_are_excluded_from_gate_and_marked(self):
        summary = run_decision_set(self.data)
        counted_ids = {r["row_id"] for r in summary["results"]}
        pending = [r for r in self.data["rows"] if not r["gate_counted"]]
        self.assertTrue(pending, "dataset must carry the pending borderline rows")
        for row in pending:
            self.assertNotIn(row["row_id"], counted_ids)
            self.assertEqual(row["adjudication"]["status"], "PENDING_INDEPENDENT_ADJUDICATION")

    def test_per_case_expected_decisions(self):
        by_id = {r["row_id"]: r for r in self.data["rows"]}
        expected = {
            "T1": "EXPLICITLY_UNSPECIFIED",
            "T2": "INSUFFICIENT_EVIDENCE",
            "T3": "INSUFFICIENT_EVIDENCE",
            "T4a": "EXPLICITLY_UNSPECIFIED",
            "T4b": "INSUFFICIENT_EVIDENCE",
            "T5": "INSUFFICIENT_EVIDENCE",
            "T6": "CONFLICTING_EVIDENCE",
            "T7": "CONTRADICTED",
            "C1": "SUPPORTED",
            "C2": "INSUFFICIENT_EVIDENCE",
            "C3": "SUPPORTED",
        }
        for row_id, decision in expected.items():
            self.assertIn(row_id, by_id)
            self.assertEqual(by_id[row_id]["expected_decision"], decision)

    def test_t4_reason_codes_are_deterministic(self):
        by_id = {r["row_id"]: r for r in self.data["rows"]}
        summary = run_decision_set(self.data)
        reasons = {r["row_id"]: r["reason_code"] for r in summary["results"]}
        self.assertEqual(reasons["T4a"], "ABSENCE_SCOPE_EXCEEDS_QUERY")
        self.assertEqual(reasons["T4b"], "SCOPE_LIMITED_OUTPUT_UNAVAILABLE")
        self.assertEqual(reasons["T5"], "PROVENANCE_INVALID")
        self.assertEqual(reasons["C2"], "NO_CANDIDATES")
        self.assertEqual(reasons["T7"], "NEGATED_BY_SOURCE")
        self.assertEqual(reasons["T6"], "CONFLICTING_VALUES")
        # scope-limited flag: T4a limited, T1 not
        limited = {r["row_id"]: r["scope_limited"] for r in summary["results"]}
        self.assertTrue(limited["T4a"])
        self.assertFalse(limited["T1"])


class MetamorphicTests(unittest.TestCase):
    """B4 protocol: decisions must be invariant to score changes/reordering
    when candidate spans and provenance are held constant."""

    @classmethod
    def setUpClass(cls):
        cls.data = load_decision_set()

    def test_decision_invariant_to_score_perturbation(self):
        for row in self.data["rows"]:
            if not row["gate_counted"]:
                continue
            base = assess_support(row["query"], row["candidates"], row["fact"],
                                  row.get("scope_limited_answers_enabled", True)).decision
            mutations = [
                # uniformly low scores
                lambda cs: [dict(c, score=0.01 + i * 0.005) for i, c in enumerate(cs)],
                # reversed order with near-perfect scores
                lambda cs: [dict(c, score=0.99 - i * 0.01) for i, c in enumerate(reversed(cs))],
                # absurd score magnitudes
                lambda cs: [dict(c, score=12345.6) for c in cs],
                # scores removed entirely
                lambda cs: [{k: v for k, v in c.items() if k != "score"} for c in cs],
            ]
            for mutate in mutations:
                candidates = mutate(copy.deepcopy(row["candidates"]))
                mutated = assess_support(row["query"], candidates, row["fact"],
                                         row.get("scope_limited_answers_enabled", True))
                self.assertEqual(
                    mutated.decision, base,
                    f"row {row['row_id']}: decision changed under score mutation; "
                    f"the score leaked into the support decision",
                )

    def test_changing_span_text_can_change_decision(self):
        # T3 setup: confirmation-only span abstains...
        row = next(r for r in self.data["rows"] if r["row_id"] == "T3")
        abstain = assess_support(row["query"], row["candidates"], row["fact"],
                                 row.get("scope_limited_answers_enabled", True))
        self.assertEqual(abstain.decision, "INSUFFICIENT_EVIDENCE")
        # ...but the same query against a span that contains the explicit
        # absence statement must change the decision.
        candidates = [dict(copy.deepcopy(row["candidates"][0]), text=SALES_FULL_TEXT,
                           start_line=1, end_line=8)]
        changed = assess_support(row["query"], candidates, row["fact"],
                                 row.get("scope_limited_answers_enabled", True))
        self.assertEqual(changed.decision, "EXPLICITLY_UNSPECIFIED")


class ProvenanceTests(unittest.TestCase):
    """T5 fail-closed behaviour at component level."""

    def valid_candidate(self):
        return {
            "source_id": "00_CORPUS/network.md",
            "chunk_id": "00_CORPUS/network.md#chunk-1",
            "start_line": 1,
            "end_line": 3,
            "text": "Kiểm tra công suất RX trên thiết bị.",
            "scope": "00_CORPUS/network.md",
            "score": 0.5,
        }

    def test_valid_candidate_accepted(self):
        self.assertTrue(candidate_provenance_valid(self.valid_candidate()))

    def test_invalid_variants_rejected(self):
        mutations = [
            lambda c: c.update(source_id="   "),
            lambda c: c.update(chunk_id=""),
            lambda c: c.update(text="  "),
            lambda c: c.update(start_line=0),
            lambda c: c.update(end_line=0),
            lambda c: c.update(start_line=5, end_line=3),   # end < start
            lambda c: c.update(start_line="1"),             # string, not int
            lambda c: c.update(start_line=True),            # bool is not an int line
        ]
        for mutate in mutations:
            candidate = self.valid_candidate()
            mutate(candidate)
            self.assertFalse(candidate_provenance_valid(candidate))

    def test_all_invalid_candidates_fail_closed(self):
        fact = {"fact_id": "f", "query_scope": "corpus",
                "support_patterns": [{"regex": "RX"}]}
        candidate = self.valid_candidate()
        candidate["chunk_id"] = ""  # invalid provenance, would otherwise match
        decision = assess_support("RX?", [candidate], fact)
        self.assertEqual(decision.decision, "INSUFFICIENT_EVIDENCE")
        self.assertEqual(decision.reason_code, "PROVENANCE_INVALID")
        self.assertEqual(decision.dropped_candidates, ("00_CORPUS/network.md",))
        self.assertEqual(decision.citations, ())

    def test_invalid_candidates_are_dropped_but_valid_ones_still_count(self):
        fact = {"fact_id": "f", "query_scope": "corpus",
                "support_patterns": [{"regex": "RX"}]}
        invalid = self.valid_candidate()
        invalid["chunk_id"] = ""
        valid = self.valid_candidate()
        valid["source_id"] = "00_CORPUS/other.md"
        decision = assess_support("RX?", [invalid, valid], fact)
        self.assertEqual(decision.decision, "SUPPORTED")
        self.assertEqual(decision.dropped_candidates, ("00_CORPUS/network.md",))
        self.assertEqual(decision.citations[0]["source_id"], "00_CORPUS/other.md")


class BehaviourTests(unittest.TestCase):
    """Unit-level behaviour of the locked rules."""

    def test_scope_covers_rule(self):
        self.assertTrue(scope_covers("a.md", "a.md"))
        self.assertTrue(scope_covers("*", "anything"))
        self.assertFalse(scope_covers("a.md", "corpus"))

    def test_empty_query_rejected(self):
        with self.assertRaises(ValueError):
            assess_support("   ", [], {"fact_id": "f", "query_scope": "corpus"})

    def test_empty_candidates_abstain_without_asserting_absence(self):
        fact = {"fact_id": "f", "query_scope": "corpus",
                "absence_patterns": [{"regex": "not specified", "source_scope": "a.md"}]}
        decision = assess_support("anything?", [], fact)
        self.assertEqual(decision.decision, "INSUFFICIENT_EVIDENCE")
        self.assertEqual(decision.reason_code, "NO_CANDIDATES")
        self.assertFalse(decision.scope_limited)

    def test_negation_wins_over_support_fail_closed(self):
        fact = {
            "fact_id": "f",
            "query_scope": "corpus",
            "negation_patterns": [{"regex": "không được phép"}],
            "support_patterns": [{"regex": "được phép"}],
        }
        candidate = {
            "source_id": "a.md", "chunk_id": "a.md#1", "start_line": 1,
            "end_line": 1, "text": "Hệ thống không được phép làm điều này.",
        }
        decision = assess_support("Hệ thống được phép?", [candidate], fact)
        self.assertEqual(decision.decision, "CONTRADICTED")

    def test_conflict_requires_same_value_scope(self):
        fact = {
            "fact_id": "port",
            "query_scope": "corpus",
            "value_patterns": [{"regex": "port (\\d+)", "value_scope": "current"}],
        }
        current = {"source_id": "a.md", "chunk_id": "a.md#1", "start_line": 1,
                   "end_line": 1, "text": "port 8000", "scope": "current"}
        legacy = {"source_id": "b.md", "chunk_id": "b.md#1", "start_line": 1,
                  "end_line": 1, "text": "port 9000", "scope": "legacy"}
        decision = assess_support("port?", [current, legacy], fact)
        self.assertEqual(decision.decision, "INSUFFICIENT_EVIDENCE")  # no conflict, no support
        conflict = {"source_id": "c.md", "chunk_id": "c.md#1", "start_line": 1,
                    "end_line": 1, "text": "port 9000", "scope": "current"}
        decision = assess_support("port?", [current, conflict], fact)
        self.assertEqual(decision.decision, "CONFLICTING_EVIDENCE")

    def test_citations_carry_exact_provenance(self):
        fact = {"fact_id": "f", "query_scope": "corpus",
                "support_patterns": [{"regex": "top_k=5"}]}
        candidate = {
            "source_id": "00_CORPUS/architecture.md",
            "chunk_id": "00_CORPUS/architecture.md#chunk-2",
            "start_line": 9, "end_line": 12,
            "text": "`rag_search(query, top_k=5)`: trả về kết quả tìm kiếm.",
        }
        decision = assess_support("top_k?", [candidate], fact)
        self.assertEqual(decision.citations, ({
            "source_id": "00_CORPUS/architecture.md",
            "chunk_id": "00_CORPUS/architecture.md#chunk-2",
            "start_line": 9, "end_line": 12,
        },))

    def test_reason_codes_all_within_locked_enum(self):
        for code in REASON_CODES:
            self.assertTrue(code.isupper())
        # locked count documents the full contract surface
        self.assertEqual(len(REASON_CODES), 9)


class SchemaValidationTests(unittest.TestCase):
    """Each mutation of a known-valid dataset must be REJECTED."""

    @classmethod
    def setUpClass(cls):
        cls.good = load_decision_set()

    def assert_rejected(self, mutate, fragment):
        data = copy.deepcopy(self.good)
        mutate(data)
        with self.assertRaises(ValueError) as ctx:
            validate_decision_set(data)
        self.assertIn(fragment, str(ctx.exception))

    def test_valid_committed_set_accepted(self):
        validate_decision_set(copy.deepcopy(self.good))

    def test_missing_top_level_key(self):
        def m(d): del d["scope_matching_rule"]
        self.assert_rejected(m, "missing required key")

    def test_row_missing_required_key(self):
        def m(d): del d["rows"][0]["rationale"]
        self.assert_rejected(m, "row missing required key")

    def test_duplicate_row_id(self):
        def m(d): d["rows"][1]["row_id"] = d["rows"][0]["row_id"]
        self.assert_rejected(m, "duplicate row_id")

    def test_unknown_decision_rejected(self):
        def m(d): d["rows"][0]["expected_decision"] = "MAYBE"
        self.assert_rejected(m, "unknown expected_decision")

    def test_malformed_regex_rejected(self):
        def m(d): d["rows"][0]["fact"]["absence_patterns"][0]["regex"] = "([unclosed"
        self.assert_rejected(m, "pattern.regex")

    def test_blank_regex_rejected(self):
        def m(d): d["rows"][0]["fact"]["absence_patterns"][0]["regex"] = "  "
        self.assert_rejected(m, "non-empty string")

    def test_missing_family_coverage(self):
        def m(d): d["required_case_families"].append("T99")
        self.assert_rejected(m, "coverage gap")

    def test_missing_decision_coverage(self):
        def m(d):
            # Keep CONTRADICTED required but remove the only gate-counted row
            # that produces it (un-gate T7 and drop the T7 family requirement
            # so the family check does not fire first).
            d["required_case_families"] = [f for f in d["required_case_families"] if f != "T7"]
            for row in d["rows"]:
                if row["case_family"] == "T7":
                    row["gate_counted"] = False
                    row["adjudication"]["status"] = "PENDING_INDEPENDENT_ADJUDICATION"
        self.assert_rejected(m, "coverage gap: no gate-counted row for decision CONTRADICTED")

    def test_non_gate_row_must_be_pending(self):
        def m(d):
            d["rows"][0]["gate_counted"] = False
        self.assert_rejected(m, "PENDING_INDEPENDENT_ADJUDICATION")

    def test_gate_counted_must_be_boolean(self):
        def m(d): d["rows"][0]["gate_counted"] = "yes"
        self.assert_rejected(m, "gate_counted must be a boolean")

    def test_runner_fails_when_one_case_mismatches(self):
        data = copy.deepcopy(self.good)
        for row in data["rows"]:
            if row["row_id"] == "C1":
                row["expected_decision"] = "INSUFFICIENT_EVIDENCE"
        summary = run_decision_set(data)
        self.assertFalse(summary["passed"])
        failed = [r for r in summary["results"] if not r["passed"]]
        self.assertEqual(len(failed), 1)
        self.assertEqual(failed[0]["row_id"], "C1")


class PatternTests(unittest.TestCase):
    def test_patterns_compile_case_insensitive(self):
        compiled = compile_pattern({"regex": "top_k=5"})
        self.assertTrue(compiled.search("Tham số TOP_K=5 mặc định"))

    def test_non_dict_pattern_rejected(self):
        with self.assertRaises(ValueError):
            compile_pattern("top_k=5")


if __name__ == "__main__":
    unittest.main()
