import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "04_CODE"))

import rag_eval
from rag_eval import (
    EVAL_SET_PATH,
    Document,
    RetrievalIndex,
    evaluate,
    gate_verdict,
    hit_at_k,
    index_documents,
    load_eval_set,
    mrr,
    precision_at_k,
    recall_at_k,
    validate_eval_set,
)


def minimal_valid_set() -> dict:
    return {
        "version": 1,
        "chunking": {"max_chars": 300, "overlap_chars": 40},
        "retrieval": {"top_k": 5, "operating_min_score": 0.35},
        "baseline_gate": {
            "hit_at_5": 0.9, "recall_at_5": 0.9, "mrr": 0.9,
            "no_answer_accuracy": 0.8, "precision_at_5": 0.8, "answered_rate": 0.9,
        },
        "documents": [
            {"source_id": "a.md", "title": "a.md", "text": "ONT optical signal"},
            {"source_id": "b.md", "title": "b.md", "text": "sales delivery schedule"},
        ],
        "labeled_queries": [
            {"query": "ONT optical", "expected": ["a.md"]},
        ] * 10,
        "no_answer_queries": [
            {"query": "football score last night", "kind": "easy"},
        ] * 5,
    }


class MetricTests(unittest.TestCase):
    def test_hit_at_k(self):
        self.assertEqual(hit_at_k(["a", "b"], ["b"], 5), 1)
        self.assertEqual(hit_at_k(["a", "b"], ["c"], 5), 0)

    def test_precision_at_k(self):
        self.assertAlmostEqual(precision_at_k(["a", "b"], ["b"], 5), 0.5)
        self.assertAlmostEqual(precision_at_k([], ["b"], 5), 0.0)

    def test_recall_at_k(self):
        self.assertAlmostEqual(recall_at_k(["b"], ["b", "c"], 5), 0.5)
        self.assertAlmostEqual(recall_at_k(["b", "c"], ["b", "c"], 5), 1.0)

    def test_mrr(self):
        self.assertAlmostEqual(mrr(["a", "b"], ["b"]), 0.5)
        self.assertAlmostEqual(mrr(["a"], ["z"]), 0.0)

    def test_gate_verdict_pass_and_fail(self):
        baseline = {"hit_at_5": 0.9, "recall_at_5": 0.9, "mrr": 0.9,
                    "no_answer_accuracy": 0.8, "precision_at_5": 0.8, "answered_rate": 0.9}
        passed, failures = gate_verdict({k: 1.0 for k in baseline}, baseline)
        self.assertTrue(passed)
        self.assertEqual(failures, [])
        low = {**{k: 1.0 for k in baseline}, "answered_rate": 0.5}
        passed, failures = gate_verdict(low, baseline)
        self.assertFalse(passed)
        self.assertTrue(any("answered_rate" in f for f in failures))


class SchemaValidationTests(unittest.TestCase):
    """Each case mutates a known-valid set and must be REJECTED."""

    def setUp(self):
        self.good = minimal_valid_set()

    def assert_rejected(self, mutate, fragment):
        data = copy.deepcopy(self.good)
        mutate(data)
        with self.assertRaises(ValueError) as ctx:
            validate_eval_set(data)
        self.assertIn(fragment, str(ctx.exception))

    def test_valid_minimal_set_accepted(self):
        validate_eval_set(self.good)

    def test_missing_top_level_key(self):
        def m(d): del d["baseline_gate"]
        self.assert_rejected(m, "missing required key")

    def test_empty_documents(self):
        self.assert_rejected(lambda d: d.update(documents=[]), "documents")

    def test_duplicate_source_id(self):
        def m(d): d["documents"].append(copy.deepcopy(d["documents"][0]))
        self.assert_rejected(m, "duplicate source_id")

    def test_empty_labeled_queries(self):
        self.assert_rejected(lambda d: d.update(labeled_queries=[]), "labeled_queries")

    def test_empty_no_answer_queries(self):
        self.assert_rejected(lambda d: d.update(no_answer_queries=[]), "no_answer_queries")

    def test_unknown_expected_reference(self):
        def m(d): d["labeled_queries"][0]["expected"] = ["zzz.md"]
        self.assert_rejected(m, "unknown source")

    def test_empty_expected_list(self):
        def m(d): d["labeled_queries"][0]["expected"] = []
        self.assert_rejected(m, "non-empty list")

    def test_blank_query_string(self):
        def m(d): d["labeled_queries"][0]["query"] = "   "
        self.assert_rejected(m, "non-empty string")

    def test_invalid_chunking(self):
        def m(d): d["chunking"]["overlap_chars"] = 999
        self.assert_rejected(m, "overlap_chars")

    def test_invalid_top_k(self):
        def m(d): d["retrieval"]["top_k"] = 0
        self.assert_rejected(m, "top_k")

    def test_invalid_operating_min_score(self):
        def m(d): d["retrieval"]["operating_min_score"] = 2.0
        self.assert_rejected(m, "operating_min_score")

    def test_missing_gate_key(self):
        def m(d): del d["baseline_gate"]["answered_rate"]
        self.assert_rejected(m, "missing key")

    def test_malformed_json_raises_on_load(self):
        bad = EVAL_SET_PATH.with_name("EVAL_SET_BAD.json")
        bad.write_text("{not valid json", encoding="utf-8")
        try:
            with self.assertRaises(Exception):
                json.loads(Path(bad).read_text(encoding="utf-8"))
        finally:
            bad.unlink(missing_ok=True)


class BehaviorTests(unittest.TestCase):
    def setUp(self):
        docs = [
            Document("a/travel.md", "travel.md",
                     "Vé máy bay cần phê duyệt của quản lý\nHỗ trợ per diem mỗi ngày"),
            Document("b/other.md", "other.md", "Kỷ luật họp tuần của phòng"),
        ]
        self.index = RetrievalIndex(index_documents(docs, max_chars=300, overlap_chars=40))

    def test_answered_rate_detects_false_abstention(self):
        labeled = [{"query": "vé máy bay phê duyệt", "expected": ["a/travel.md"]},
                   {"query": "zzzqqq xyzzyy không tồn tại", "expected": ["a/travel.md"]}]
        no_answer = [{"query": "football", "kind": "easy"}] * 5
        m = evaluate(self.index, labeled, no_answer, top_k=5, min_score=0.35)
        self.assertLess(m["answered_rate"], 1.0)
        self.assertTrue(any("false abstention" in s for s in m["ranked_misses"]))

    def test_near_miss_leak_is_reported_not_hidden(self):
        no_answer = [{"query": "đặt vé máy bay đi Đà Nẵng", "kind": "near_miss"}] * 5
        labeled = [{"query": "vé máy bay phê duyệt", "expected": ["a/travel.md"]}] * 10
        m = evaluate(self.index, labeled, no_answer, top_k=5, min_score=0.35)
        self.assertLess(m["no_answer_accuracy"], 1.0)
        self.assertEqual(len(m["near_miss_leaks"]), 5)


class CommittedSetTests(unittest.TestCase):
    def setUp(self):
        self.data = load_eval_set()  # also runs full schema validation

    def test_committed_set_meets_xu_targets(self):
        self.assertGreaterEqual(len(self.data["labeled_queries"]), 50)
        self.assertGreaterEqual(len(self.data["no_answer_queries"]), 15)
        kinds = [i["kind"] for i in self.data["no_answer_queries"]]
        self.assertGreaterEqual(kinds.count("near_miss"), 3)
        self.assertGreaterEqual(kinds.count("easy"), 10)

    def test_operating_threshold_is_experimental_range(self):
        op = self.data["retrieval"]["operating_min_score"]
        self.assertGreaterEqual(op, 0.30)
        self.assertLessEqual(op, 0.40)


if __name__ == "__main__":
    unittest.main()
