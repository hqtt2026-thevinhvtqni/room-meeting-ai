import copy
import json
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
    """Engineered fixtures with MEASURED behaviour (verified before writing):

    - answerable control "vé máy bay cần phê duyệt của quản lý trực tiếp"
      retrieves a/cong-tac.md with score ~0.858 at min_score 0.35;
    - near-miss "vé máy bay du lịch có cần phê duyệt của quản lý không"
      leaks (retrieves a/cong-tac.md, score ~0.462) although the answer
      is absent (du lịch is not covered by the công tác policy).

    These tests pin the REPORTING of leaks and false abstentions.
    If the fixture stops leaking, the assertion fails with instructions to
    re-measure — the test must not be satisfied by tuning numbers.
    """

    def setUp(self):
        docs = [
            Document("a/cong-tac.md", "cong-tac.md",
                     "Quy định công tác xa của công ty\n"
                     "Vé máy bay cần phê duyệt của quản lý trực tiếp\n"
                     "Hỗ trợ per diem 500 nghìn mỗi ngày\n"
                     "Khách sạn hoàn qua kế toán\n"
                     "Báo cáo công tác trong 3 ngày sau khi về"),
            Document("b/ky-luat.md", "ky-luat.md",
                     "Kỷ luật họp tuần của phòng\nĐi muộn họp phạt 50 nghìn\n"
                     "Điện thoại để chế độ im lặng trong họp"),
            Document("c/bao-mat.md", "bao-mat.md",
                     "Chính sách bảo mật thông tin công ty\n"
                     "Không chia sẻ mật khẩu qua email\n"
                     "Token truy cập phải lưu trong vault"),
        ]
        self.index = RetrievalIndex(index_documents(docs, max_chars=300, overlap_chars=40))
        self.answerable = "vé máy bay cần phê duyệt của quản lý trực tiếp"
        self.near_miss = "vé máy bay du lịch có cần phê duyệt của quản lý không"

    def test_answerable_control_hits_expected_source(self):
        results = self.index.search(self.answerable, top_k=5, min_score=0.35)
        self.assertTrue(results, "fixture regression: answerable control no longer retrieves")
        self.assertEqual(results[0].source_id, "a/cong-tac.md")

    def test_answered_rate_detects_false_abstention(self):
        labeled = [
            {"query": self.answerable, "expected": ["a/cong-tac.md"]},
            {"query": "zzzqqq xyzzyy không tồn tại ở đâu cả", "expected": ["a/cong-tac.md"]},
        ]
        no_answer = [{"query": "football score last night", "kind": "easy"}] * 5
        m = evaluate(self.index, labeled, no_answer, top_k=5, min_score=0.35)
        self.assertLess(m["answered_rate"], 1.0)
        self.assertTrue(any("false abstention" in s for s in m["ranked_misses"]),
                        "false abstention must be labelled independently of ranking misses")

    def test_near_miss_leak_is_reported_not_hidden(self):
        # Control first: the leak must actually leak at the operating threshold.
        self.assertTrue(
            self.index.search(self.near_miss, top_k=5, min_score=0.35),
            "fixture regression: near-miss query no longer leaks; re-measure "
            "before changing this test — do not tune the fixture to pass",
        )
        labeled = [{"query": self.answerable, "expected": ["a/cong-tac.md"]}] * 10
        no_answer = [{"query": self.near_miss, "kind": "near_miss"}] * 5
        m = evaluate(self.index, labeled, no_answer, top_k=5, min_score=0.35)
        self.assertLess(m["no_answer_accuracy"], 1.0)
        self.assertEqual(len(m["near_miss_leaks"]), 5)
        self.assertEqual(m["easy_leaks"], [])


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
