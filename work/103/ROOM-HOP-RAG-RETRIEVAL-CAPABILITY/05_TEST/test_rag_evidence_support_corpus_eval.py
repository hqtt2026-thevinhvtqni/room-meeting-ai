"""Tests for rag_evidence_support_corpus_eval.py (Gate C preparatory, report-only).

Covers: fact-specs validation against the corpus fixture, the report-only
diagnostic taxonomy, the end-to-end mini pipeline (retrieval -> assess_support),
and CLI exit-code discipline (exit 0 on outcomes, exit 1 on validation errors).

Run via unittest (matching the repo CI runner):
    python -m unittest discover -s ../05_TEST -p "test_rag_evidence_support_corpus_eval.py" -v
"""

from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

CODE_DIR = Path(__file__).resolve().parents[1] / "04_CODE"
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

import rag_evidence_support_corpus_eval as corpus_eval  # noqa: E402
from rag_evidence_support import DECISIONS  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURE = REPO_ROOT / "05_TEST" / "EVAL_SET_CORPUS_V4_V3.json"
DEFAULT_SPECS = REPO_ROOT / "05_TEST" / "EVIDENCE_SUPPORT_FACT_SPECS_V1.json"


def _load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _mini_fixture() -> dict:
    return {
        "documents": [
            {
                "source_id": "doc-a.md",
                "title": "doc-a.md",
                "text": (
                    "# Kiến trúc\n\n- Core service: chạy trên port 8000 và sở hữu dữ liệu chính tắc.\n"
                    "- Dashboard: render-only trên port 3000.\n"
                ),
            },
            {
                "source_id": "doc-b.md",
                "title": "doc-b.md",
                "text": (
                    "# Chính sách\n\n- Hệ thống không được lưu trữ hoặc trả về mật khẩu quản trị.\n"
                ),
            },
        ],
        "chunking": {"max_chars": 300, "overlap_chars": 40},
        "retrieval": {"top_k": 5, "operating_min_score": 0.1},
        "labeled_queries": [
            {"query_id": "QX1", "query": "Core service chạy trên port nào?",
             "expected": ["doc-a.md"]},
        ],
        "no_answer_queries": [
            {"query_id": "QX2", "query": "Mật khẩu quản trị được lưu trữ ở đâu trong hệ thống?",
             "kind": "easy"},
        ],
    }


def _mini_specs(qx2_patterns=None) -> dict:
    fact = {"fact_id": "test.admin_password.storage", "query_scope": "corpus"}
    if qx2_patterns is not None:
        fact["support_patterns"] = qx2_patterns
    return {
        "dataset_id": "test.mini-specs.v1",
        "rows": [
            {
                "query_id": "QX1",
                "ideal_decision": "SUPPORTED",
                "fact": {
                    "fact_id": "test.core.port",
                    "query_scope": "doc-a.md",
                    "support_patterns": [{"regex": "chạy trên port 8000"}],
                },
                "rationale": "answerable control",
            },
            {
                "query_id": "QX2",
                "ideal_decision": "INSUFFICIENT_EVIDENCE",
                "fact": fact,
                "rationale": "no-answer fail-closed row",
            },
        ],
    }


class ValidationTests(unittest.TestCase):
    def test_default_specs_validate_against_default_fixture(self):
        fixture = _load(DEFAULT_FIXTURE)
        specs = _load(DEFAULT_SPECS)
        corpus_eval.validate_fixture(fixture)
        corpus_eval.validate_fact_specs(specs, fixture)  # must not raise

    def test_specs_reject_unknown_query_id(self):
        specs = _mini_specs()
        specs["rows"][0]["query_id"] = "QZZ"
        with self.assertRaises(ValueError):
            corpus_eval.validate_fact_specs(specs, _mini_fixture())

    def test_specs_reject_unknown_ideal_decision(self):
        specs = _mini_specs()
        specs["rows"][0]["ideal_decision"] = "DEFINITELY_SUPPORTED"
        with self.assertRaises(ValueError):
            corpus_eval.validate_fact_specs(specs, _mini_fixture())

    def test_specs_require_both_kinds_covered(self):
        specs = _mini_specs()
        specs["rows"] = [r for r in specs["rows"] if r["query_id"] == "QX1"]
        with self.assertRaises(ValueError):
            corpus_eval.validate_fact_specs(specs, _mini_fixture())

    def test_specs_reject_duplicate_query_id(self):
        specs = _mini_specs()
        specs["rows"][1]["query_id"] = specs["rows"][0]["query_id"]
        with self.assertRaises(ValueError):
            corpus_eval.validate_fact_specs(specs, _mini_fixture())

    def test_fixture_rejects_missing_retrieval_config(self):
        fixture = _mini_fixture()
        del fixture["retrieval"]
        with self.assertRaises(ValueError):
            corpus_eval.validate_fixture(fixture)


class CategorizeTests(unittest.TestCase):
    CASES = [
        # (fixture_kind, ideal, actual, expected category)
        ("ANSWERABLE", "SUPPORTED", "SUPPORTED", "MATCH"),
        ("NO_ANSWER", "EXPLICITLY_UNSPECIFIED", "EXPLICITLY_UNSPECIFIED", "MATCH"),
        # The strict leak: affirmative answer on a no-answer query.
        ("NO_ANSWER", "INSUFFICIENT_EVIDENCE", "SUPPORTED", "NO_ANSWER_LEAK"),
        # Answerable question that abstains instead of answering.
        ("ANSWERABLE", "SUPPORTED", "INSUFFICIENT_EVIDENCE", "FALSE_ABSTENTION"),
        ("ANSWERABLE", "SUPPORTED", "EXPLICITLY_UNSPECIFIED", "FALSE_ABSTENTION"),
        # Negative-safety query whose contradiction is missed.
        ("ANSWERABLE", "CONTRADICTED", "SUPPORTED", "CONTRADICTION_MISSED"),
        ("ANSWERABLE", "CONTRADICTED", "INSUFFICIENT_EVIDENCE", "CONTRADICTION_MISSED"),
        # Any other combination.
        ("NO_ANSWER", "INSUFFICIENT_EVIDENCE", "EXPLICITLY_UNSPECIFIED", "IDEAL_MISMATCH_OTHER"),
        ("ANSWERABLE", "SUPPORTED", "CONFLICTING_EVIDENCE", "IDEAL_MISMATCH_OTHER"),
    ]

    def test_categorize(self):
        for kind, ideal, actual, expected in self.CASES:
            with self.subTest(kind=kind, ideal=ideal, actual=actual):
                self.assertIn(ideal, DECISIONS)
                self.assertIn(actual, DECISIONS)
                self.assertEqual(corpus_eval.categorize(kind, ideal, actual), expected)


class EndToEndTests(unittest.TestCase):
    def test_answerable_supported_match(self):
        report = corpus_eval.run_corpus_eval(_mini_fixture(), _mini_specs())
        by_id = {r["query_id"]: r for r in report["results"]}
        self.assertEqual(by_id["QX1"]["decision"], "SUPPORTED")
        self.assertEqual(by_id["QX1"]["category"], "MATCH")
        self.assertEqual(by_id["QX1"]["reason_code"], "SUPPORTED_BY_SOURCE")
        self.assertTrue(by_id["QX1"]["citations"], "SUPPORTED must carry provenance citations")
        self.assertGreaterEqual(by_id["QX1"]["retrieval_count"], 1)

    def test_no_answer_fail_closed_and_leak_detection(self):
        # Fail-closed: topical overlap retrieves a chunk but no pattern matches.
        report = corpus_eval.run_corpus_eval(_mini_fixture(), _mini_specs())
        qx2 = next(r for r in report["results"] if r["query_id"] == "QX2")
        self.assertEqual(qx2["decision"], "INSUFFICIENT_EVIDENCE")
        self.assertEqual(qx2["reason_code"], "NO_ADEQUATE_SUPPORT")
        self.assertEqual(qx2["category"], "MATCH")

        # Leak: if a (wrong) support pattern fires on retrieved text, the
        # diagnostic must flag it instead of hiding it.
        leak_specs = _mini_specs(qx2_patterns=[{"regex": "Core service"}])
        report = corpus_eval.run_corpus_eval(_mini_fixture(), leak_specs)
        qx2 = next(r for r in report["results"] if r["query_id"] == "QX2")
        self.assertEqual(qx2["decision"], "SUPPORTED")
        self.assertEqual(qx2["category"], "NO_ANSWER_LEAK")
        self.assertEqual(report["summary"]["n_no_answer_leak"], 1)

    def test_report_summary_counts_are_consistent(self):
        report = corpus_eval.run_corpus_eval(_mini_fixture(), _mini_specs())
        s = report["summary"]
        self.assertEqual(s["n_specs"], len(report["results"]))
        total = (s["n_match"] + s["n_no_answer_leak"] + s["n_false_abstention"]
                 + s["n_contradiction_missed"] + s["n_ideal_mismatch_other"])
        self.assertEqual(total, s["n_specs"])
        self.assertEqual(report["adjudication_status"],
                         "AUTHORED_PENDING_INDEPENDENT_ADJUDICATION")
        self.assertTrue(report["report_only"])


class CliDisciplineTests(unittest.TestCase):
    def _run_main(self, fixture: dict, specs: dict) -> tuple[int, str]:
        with tempfile.TemporaryDirectory() as tmp:
            fixture_path = Path(tmp) / "fixture.json"
            specs_path = Path(tmp) / "specs.json"
            fixture_path.write_text(json.dumps(fixture, ensure_ascii=False), encoding="utf-8")
            specs_path.write_text(json.dumps(specs, ensure_ascii=False), encoding="utf-8")
            argv = ["rag_evidence_support_corpus_eval.py",
                    "--fixture", str(fixture_path),
                    "--specs", str(specs_path),
                    "--json"]
            stdout = io.StringIO()
            with mock.patch.object(sys, "argv", argv), \
                    contextlib.redirect_stdout(stdout):
                code = corpus_eval.main()
        return code, stdout.getvalue()

    def test_main_exits_zero_even_with_leak(self):
        code, out = self._run_main(_mini_fixture(),
                                   _mini_specs(qx2_patterns=[{"regex": "Core service"}]))
        self.assertEqual(code, 0, "report-only harness must not fail on evaluation outcomes")
        self.assertIn("NO_ANSWER_LEAK", out)

    def test_main_exits_one_on_validation_error(self):
        specs = _mini_specs()
        specs["rows"][0]["query_id"] = "QZZ"
        code, _ = self._run_main(_mini_fixture(), specs)
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
