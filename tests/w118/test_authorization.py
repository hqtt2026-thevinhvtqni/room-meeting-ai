import json
import tempfile
import unittest
from pathlib import Path

from scripts.w118.authorization import (
    authorize_acceptance,
    authorize_ack,
    load_role_map,
    parse_ack,
)


class Work118AuthorizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.role_map = load_role_map(".github/w118/role-map.json")

    def test_owner_accounts_are_mapped_for_acceptance(self):
        for login in ("hqtt2026-thevinhvtqni", "thevinhqtni-1911"):
            allowed, reason, principal = authorize_acceptance(self.role_map, login, "reviewer-not-owner")
            self.assertTrue(allowed, reason)
            self.assertEqual(principal, "vinh")

    def test_owner_accounts_cannot_ack_execution_roles(self):
        for login in ("hqtt2026-thevinhvtqni", "thevinhqtni-1911"):
            allowed, reason, _ = authorize_ack(self.role_map, login, "ka")
            self.assertFalse(allowed)
            self.assertIn("not authorized", reason)

    def test_unmapped_actor_is_denied(self):
        allowed, _, _ = authorize_ack(self.role_map, "unknown-contributor", "coder")
        self.assertFalse(allowed)

    def test_self_review_is_denied(self):
        allowed, reason, _ = authorize_acceptance(self.role_map, "hqtt2026-thevinhvtqni", "hqtt2026-thevinhvtqni")
        self.assertFalse(allowed)
        self.assertIn("self-review", reason)

    def test_inactive_actor_is_denied(self):
        data = json.loads(Path(".github/w118/role-map.json").read_text(encoding="utf-8"))
        data["principals"]["disabled-user"] = {
            "principal": "disabled",
            "roles": ["tester"],
            "ack_roles": ["tester"],
            "can_accept": False,
            "active": False,
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "roles.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            role_map = load_role_map(path)
        allowed, _, _ = authorize_ack(role_map, "disabled-user", "tester")
        self.assertFalse(allowed)

    def test_ack_parser_requires_exact_role_and_issue(self):
        self.assertEqual(parse_ack("ACKED-tester 65"), ("tester", 65))
        self.assertIsNone(parse_ack("please ACKED-tester 65"))
        self.assertIsNone(parse_ack("ACKED-tester"))
        self.assertIsNone(parse_ack("ACKED-TESTER 65"))


    def test_explicitly_mapped_executor_can_ack_its_own_role(self):
        data = json.loads(Path(".github/w118/role-map.json").read_text(encoding="utf-8"))
        data["principals"]["fixture-executor"] = {
            "principal": "fixture-executor",
            "roles": ["tester"],
            "ack_roles": ["tester"],
            "can_accept": False,
            "active": True,
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "roles.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            role_map = load_role_map(path)
        allowed, reason, principal = authorize_ack(role_map, "fixture-executor", "tester")
        self.assertTrue(allowed, reason)
        self.assertEqual(principal, "fixture-executor")

    def test_executor_cannot_ack_another_role(self):
        data = json.loads(Path(".github/w118/role-map.json").read_text(encoding="utf-8"))
        data["principals"]["fixture-executor"] = {
            "principal": "fixture-executor",
            "roles": ["tester"],
            "ack_roles": ["tester"],
            "can_accept": False,
            "active": True,
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "roles.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            role_map = load_role_map(path)
        allowed, _, _ = authorize_ack(role_map, "fixture-executor", "coder")
        self.assertFalse(allowed)

    def test_role_map_rejects_ack_role_not_in_roles(self):
        data = json.loads(Path(".github/w118/role-map.json").read_text(encoding="utf-8"))
        data["principals"]["bad-user"] = {
            "principal": "bad",
            "roles": ["tester"],
            "ack_roles": ["owner"],
            "can_accept": False,
            "active": True,
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "roles.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_role_map(path)


if __name__ == "__main__":
    unittest.main()
