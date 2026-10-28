import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "04_CODE"))

import rag_eval
from rag_eval import (
    EVAL_SET_PATH,
    gate_verdict,
    hit_at_k,
    load_eval_set,
    mrr,
    precision_at_k,
    recall_at_k,
)


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
        good = {"hit_at_5": 1.0, "precision_at_5": 1.0}
        bad = {"hit_at_5": 0.5, "precision_at_5": 1.0}
        passed, failures = gate_verdict(good, {"hit_at_5": 0.9, "precision_at_5": 0.8})
        self.assertTrue(passed)
        self.assertEqual(failures, [])
        passed, failures = gate_verdict(bad, {"hit_at_5": 0.9, "precision_at_5": 0.8})
        self.assertFalse(passed)
        self.assertTrue(any("hit_at_5" in f for f in failures))


class EvalSetTests(unittest.TestCase):
    def setUp(self):
        self.data = load_eval_set()

    def test_eval_set_exists_and_wellformed(self):
        self.assertTrue(EVAL_SET_PATH.is_file())
        self.assertGreaterEqual(len(self.data["labeled_queries"]), 10)
        self.assertGreaterEqual(len(self.data["no_answer_queries"]), 5)
        known = {d["source_id"] for d in self.data["documents"]}
        for item in self.data["labeled_queries"]:
            self.assertTrue(item["expected"])
            for s in item["expected"]:
                self.assertIn(s, known)
        for q in self.data["no_answer_queries"]:
            self.assertTrue(q.strip())

    def test_operating_threshold_has_positive_margin(self):
        # The operating min_score must sit below the first sweep step that loses hit.
        op = self.data["retrieval"]["operating_min_score"]
        self.assertGreaterEqual(op, 0.30)
        self.assertLessEqual(op, 0.40)


if __name__ == "__main__":
    unittest.main()
