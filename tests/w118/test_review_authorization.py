import copy
import unittest

from scripts.w118.authorization import load_role_map, authorize_independent_review


class Work118ReviewAuthorizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.role_map = load_role_map(".github/w118/role-map.json")

    def test_distinct_mapped_independent_reviewer_is_allowed(self):
        role_map = copy.deepcopy(self.role_map)
        role_map["principals"]["xu-verified-fixture"] = {
            "principal": "xu",
            "roles": ["reviewer"],
            "ack_roles": [],
            "can_accept": False,
            "can_independently_review": True,
            "can_trigger_controlled_test": False,
            "active": True,
        }
        role_map["principals"]["different-pr-author"] = {
            "principal": "vi",
            "roles": ["coder"],
            "ack_roles": [],
            "can_accept": False,
            "can_independently_review": False,
            "can_trigger_controlled_test": False,
            "active": True,
        }
        allowed, reason, principal = authorize_independent_review(
            role_map, "xu-verified-fixture", "different-pr-author"
        )
        self.assertTrue(allowed, reason)
        self.assertEqual(principal, "xu")

    def test_owner_cannot_be_independent_reviewer(self):
        role_map = copy.deepcopy(self.role_map)
        role_map["principals"]["different-pr-author"] = {
            "principal": "vi",
            "roles": ["coder"],
            "ack_roles": [],
            "can_accept": False,
            "can_independently_review": False,
            "can_trigger_controlled_test": False,
            "active": True,
        }
        for login in ("hqtt2026-thevinhvtqni", "thevinhqtni-1911"):
            self.assertTrue(role_map["principals"][login]["can_accept"])
            self.assertFalse(role_map["principals"][login]["can_independently_review"])
            allowed, reason, _ = authorize_independent_review(
                role_map, login, "different-pr-author"
            )
            self.assertFalse(allowed)
            self.assertIn("independent reviewer", reason)

    def test_same_principal_cross_account_review_is_denied(self):
        role_map = copy.deepcopy(self.role_map)
        role_map["principals"]["thevinhqtni-1911"]["can_independently_review"] = True
        allowed, reason, _ = authorize_independent_review(
            role_map, "thevinhqtni-1911", "hqtt2026-thevinhvtqni"
        )
        self.assertFalse(allowed)
        self.assertIn("same HQTT principal", reason)

    def test_unmapped_pr_author_blocks_independence_claim(self):
        role_map = copy.deepcopy(self.role_map)
        role_map["principals"]["xu-verified-fixture"] = {
            "principal": "xu",
            "roles": ["reviewer"],
            "ack_roles": [],
            "can_accept": False,
            "can_independently_review": True,
            "can_trigger_controlled_test": False,
            "active": True,
        }
        allowed, reason, _ = authorize_independent_review(
            role_map, "xu-verified-fixture", "unmapped-author"
        )
        self.assertFalse(allowed)
        self.assertIn("cannot be verified", reason)

    def test_unmapped_reviewer_is_denied(self):
        allowed, _, _ = authorize_independent_review(
            self.role_map, "xu-unverified-login", "hqtt2026-thevinhvtqni"
        )
        self.assertFalse(allowed)


if __name__ == "__main__":
    unittest.main()
