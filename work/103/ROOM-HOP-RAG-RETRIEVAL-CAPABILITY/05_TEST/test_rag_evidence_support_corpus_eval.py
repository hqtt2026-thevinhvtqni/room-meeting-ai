"""Tests for rag_evidence_support_corpus_eval.py (Gate C preparatory, report-only).

Covers: fact-specs validation against the corpus fixture, the report-only
diagnostic taxonomy, the end-to-end mini pipeline (retrieval -> assess_support),
citation-source alignment + relaxed-threshold retrieval probe (DEBT-ES-08/06
seeds), and CLI exit-code discipline (exit 0 on outcomes, exit 1 on
validation errors).

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

    def test_fixture_rejects_malformed_expected_list(self):
        fixture = _mini_fixture()
        fixture["labeled_queries"][0]["expected"] = "doc-a.md"  # string, not list
        with self.assertRaises(ValueError):
            corpus_eval.build_query_map(fixture)


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
        leak_specs = _mini_specs(qx2_patterns=[{"regex": "không được lưu trữ"}])
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


class CitationAlignmentTests(unittest.TestCase):
    """DEBT-ES-08 seed: citation-source alignment measurement (report-only)."""

    def test_aligned_answerable_row(self):
        report = corpus_eval.run_corpus_eval(_mini_fixture(), _mini_specs())
        qx1 = next(r for r in report["results"] if r["query_id"] == "QX1")
        self.assertEqual(qx1["expected_sources"], ["doc-a.md"])
        self.assertEqual(qx1["cited_sources"], ["doc-a.md"])
        self.assertIs(qx1["citation_aligned"], True)
        self.assertIs(qx1["expected_in_top_k"], True)
        self.assertIsNone(qx1["relaxed_probe"], "probe must be skipped when expected source is retrieved")
        self.assertEqual(report["summary"]["n_citation_misaligned"], 0)
        self.assertEqual(report["summary"]["n_expected_source_missed"], 0)

    def test_misaligned_answerable_row_is_counted(self):
        # Duplicate-content scenario: the support span lives in doc-b while
        # the fixture expects doc-a. The decision may be MATCH while the
        # citation points at the wrong source; the diagnostic must surface it.
        fixture = _mini_fixture()
        fixture["documents"][0]["text"] = (
            "# Kiến trúc\n\n- Core service: sở hữu dữ liệu chính tắc.\n"
        )
        fixture["documents"][1]["text"] = (
            "# Chính sách\n\n- Core service: chạy trên port 8000 (bản sao).\n"
            "- Hệ thống không được lưu trữ hoặc trả về mật khẩu quản trị.\n"
        )
        report = corpus_eval.run_corpus_eval(fixture, _mini_specs())
        qx1 = next(r for r in report["results"] if r["query_id"] == "QX1")
        self.assertEqual(qx1["decision"], "SUPPORTED")
        self.assertEqual(qx1["cited_sources"], ["doc-b.md"])
        self.assertIs(qx1["citation_aligned"], False)
        self.assertEqual(report["summary"]["n_citation_misaligned"], 1)

    def test_no_answer_rows_are_not_alignment_measured(self):
        report = corpus_eval.run_corpus_eval(_mini_fixture(), _mini_specs())
        qx2 = next(r for r in report["results"] if r["query_id"] == "QX2")
        self.assertIsNone(qx2["expected_sources"])
        self.assertIsNone(qx2["citation_aligned"])
        self.assertIsNone(qx2["expected_in_top_k"])
        self.assertIsNone(qx2["relaxed_probe"])

    def test_relaxed_probe_when_expected_source_missed(self):
        # DEBT-ES-06 material: operating threshold set so high that the
        # expected source is not retrieved; the probe must quantify the gap.
        # QX3 matches doc-c only partially (query terms 'ưu tiên/hay/không'
        # are absent), so no chunk reaches the 0.99 operating threshold
        # while doc-c still surfaces in the relaxed top-10.
        fixture = _mini_fixture()
        fixture["retrieval"]["operating_min_score"] = 0.99
        fixture["documents"].append({
            "source_id": "doc-c.md",
            "title": "doc-c.md",
            "text": "# Phụ lục\n\n- Core service dự phòng: chạy trên port 9000.\n",
        })
        fixture["labeled_queries"].append({
            "query_id": "QX3",
            "query": "Core service dự phòng chạy trên port nào, ưu tiên dự phòng hay không?",
            "expected": ["doc-c.md"],
        })
        specs = _mini_specs()
        specs["rows"].append({
            "query_id": "QX3",
            "ideal_decision": "SUPPORTED",
            "fact": {
                "fact_id": "test.core.port9000",
                "query_scope": "doc-c.md",
                "support_patterns": [{"regex": "chạy trên port 9000"}],
            },
            "rationale": "relaxed probe row",
        })
        report = corpus_eval.run_corpus_eval(fixture, specs)
        qx3 = next(r for r in report["results"] if r["query_id"] == "QX3")
        self.assertEqual(qx3["retrieval_count"], 0)
        self.assertIs(qx3["expected_in_top_k"], False)
        self.assertEqual(qx3["decision"], "INSUFFICIENT_EVIDENCE")
        self.assertEqual(qx3["reason_code"], "NO_CANDIDATES")
        self.assertEqual(qx3["category"], "FALSE_ABSTENTION")
        probe = qx3["relaxed_probe"]
        self.assertIsNotNone(probe)
        self.assertTrue(probe["expected_in_top10_relaxed"])
        self.assertIsNotNone(probe["expected_best_relaxed_score"])
        self.assertLess(probe["expected_best_relaxed_score"], 0.99,
                        "relaxed best score must be below the unreachable operating threshold")
        self.assertEqual(report["summary"]["n_expected_source_missed"], 1)


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
                                   _mini_specs(qx2_patterns=[{"regex": "không được lưu trữ"}]))
        self.assertEqual(code, 0, "report-only harness must not fail on evaluation outcomes")
        self.assertIn("NO_ANSWER_LEAK", out)

    def test_main_exits_one_on_validation_error(self):
        specs = _mini_specs()
        specs["rows"][0]["query_id"] = "QZZ"
        code, _ = self._run_main(_mini_fixture(), specs)
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
