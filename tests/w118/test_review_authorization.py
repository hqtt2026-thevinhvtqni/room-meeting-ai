import copy
import unittest

from scripts.w118.authorization import load_role_map
from scripts.w118.authorization import authorize_acceptance


class Work118ReviewAuthorizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.role_map = load_role_map(".github/w118/role-map.json")

    def test_owner_can_review_independently_when_pr_author_is_different_mapped_principal(self):
        role_map = copy.deepcopy(self.role_map)
        role_map["principals"]["different-pr-author"] = {
            "principal": "vi",
            "roles": ["coder"],
            "ack_roles": [],
            "can_accept": False,
            "can_trigger_controlled_test": False,
            "active": True,
        }
        allowed, reason, principal = authorize_acceptance(
            role_map, "hqtt2026-thevinhvtqni", "different-pr-author"
        )
        self.assertTrue(allowed, reason)
        self.assertEqual(principal, "vinh")

    def test_owner_alias_cannot_review_same_owner_account_pr(self):
        allowed, reason, _ = authorize_acceptance(
            self.role_map, "thevinhqtni-1911", "hqtt2026-thevinhvtqni"
        )
        self.assertFalse(allowed)
        self.assertIn("same HQTT principal", reason)

    def test_unmapped_pr_author_blocks_independence_claim(self):
        allowed, reason, _ = authorize_acceptance(
            self.role_map, "hqtt2026-thevinhvtqni", "unmapped-author"
        )
        self.assertFalse(allowed)
        self.assertIn("cannot be verified", reason)

    def test_owner_cannot_self_review(self):
        allowed, reason, _ = authorize_acceptance(
            self.role_map, "hqtt2026-thevinhvtqni", "hqtt2026-thevinhvtqni"
        )
        self.assertFalse(allowed)
        self.assertIn("same HQTT principal", reason)

    def test_unmapped_reviewer_is_denied(self):
        allowed, _, _ = authorize_acceptance(
            self.role_map, "xu-unverified-login", "different-pr-author"
        )
        self.assertFalse(allowed)


if __name__ == "__main__":
    unittest.main()
