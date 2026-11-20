import unittest

from scripts.w118.authorization import load_role_map
from scripts.w118.authorization import authorize_acceptance


class Work118ReviewAuthorizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.role_map = load_role_map(".github/w118/role-map.json")

    def test_owner_can_review_independently_when_not_pr_author(self):
        allowed, reason, principal = authorize_acceptance(
            self.role_map, "hqtt2026-thevinhvtqni", "different-pr-author"
        )
        self.assertTrue(allowed, reason)
        self.assertEqual(principal, "vinh")

    def test_owner_cannot_self_review(self):
        allowed, reason, _ = authorize_acceptance(
            self.role_map, "hqtt2026-thevinhvtqni", "hqtt2026-thevinhvtqni"
        )
        self.assertFalse(allowed)
        self.assertIn("self-review", reason)

    def test_unmapped_reviewer_is_denied(self):
        allowed, _, _ = authorize_acceptance(
            self.role_map, "xu-unverified-login", "different-pr-author"
        )
        self.assertFalse(allowed)


if __name__ == "__main__":
    unittest.main()
