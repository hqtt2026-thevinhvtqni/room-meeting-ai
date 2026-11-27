import unittest

from scripts.w118.event_evidence import build_event_evidence


class Work118EventEvidenceTests(unittest.TestCase):
    def test_builds_operation_evidence_bound_to_event_and_run(self):
        record = build_event_evidence(
            event_type="issue_comment",
            event_id="comment-123",
            source_commit="a" * 40,
            run_id=10,
            run_attempt=2,
            actor="verified-executor",
            decision="ACK_AUTHORIZED",
            details={"issue": 65, "role": "tester", "label_applied": True},
        )
        self.assertEqual(record["work_id"], "118")
        self.assertEqual(record["evidence_type"], "OPERATION")
        self.assertEqual(record["event_id"], "comment-123")
        self.assertEqual(record["run_id"], 10)
        self.assertEqual(record["run_attempt"], 2)
        self.assertEqual(record["state"], "RECORDED")
        self.assertNotIn("verified", record["state"].lower())

    def test_record_never_promotes_itself_to_verified_or_accepted(self):
        record = build_event_evidence(
            event_type="issues",
            event_id="issue-65-label-1",
            source_commit="b" * 40,
            run_id=11,
            run_attempt=1,
            actor="owner",
            decision="HANDOFF_RECORDED",
        )
        self.assertEqual(record["state"], "RECORDED")
        self.assertTrue(any("not a Work 70" in x for x in record["limitations"]))

    def test_rejects_missing_event_identity(self):
        with self.assertRaises(ValueError):
            build_event_evidence(
                event_type="issue_comment",
                event_id="",
                source_commit="c" * 40,
                run_id=1,
                run_attempt=1,
                actor="actor",
                decision="ACK_DENIED",
            )

    def test_rejects_invalid_run_numbers(self):
        with self.assertRaises(ValueError):
            build_event_evidence(
                event_type="issue_comment",
                event_id="comment-1",
                source_commit="d" * 40,
                run_id=0,
                run_attempt=1,
                actor="actor",
                decision="ACK_DENIED",
            )


    def test_rejects_boolean_and_float_run_metadata(self):
        for field, value in (("run_id", True), ("run_id", 1.5), ("run_attempt", False), ("run_attempt", 2.5)):
            kwargs = dict(event_type="issues", event_id="issue-1", source_commit="a" * 40, run_id=1, run_attempt=1, actor="actor", decision="OBSERVED")
            kwargs[field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                build_event_evidence(**kwargs)

    def test_rejects_string_zero_and_negative_run_metadata(self):
        for field, value in (("run_id", "1"), ("run_id", 0), ("run_attempt", "1"), ("run_attempt", -1)):
            kwargs = dict(event_type="issues", event_id="issue-1", source_commit="a" * 40, run_id=1, run_attempt=1, actor="actor", decision="OBSERVED")
            kwargs[field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                build_event_evidence(**kwargs)

    def test_rejects_non_hex_or_non_full_source_commit(self):
        for sha in ("g" * 40, "a" * 39, "a" * 41, "not-a-sha"):
            with self.subTest(sha=sha), self.assertRaises(ValueError):
                build_event_evidence(event_type="issues", event_id="issue-1", source_commit=sha, run_id=1, run_attempt=1, actor="actor", decision="OBSERVED")

if __name__ == "__main__":
    unittest.main()
