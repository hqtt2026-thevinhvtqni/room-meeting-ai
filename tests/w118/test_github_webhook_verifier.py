import hashlib
import hmac
import json
import unittest
import uuid

from scripts.w118.github_webhook_verifier import (
    GitHubWebhookError,
    verify_github_webhook,
)


SECRET = "test-secret-value-with-at-least-32-characters"
REPOSITORY = "hqtt2026-thevinhvtqni/room-meeting-ai"


def signed_delivery(payload=None, *, event_type="push", delivery_id=None, secret=SECRET):
    body = json.dumps(payload or {"repository": {"full_name": REPOSITORY}}, separators=(",", ":")).encode()
    digest = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return {
        "raw_body": body,
        "secret": secret,
        "signature_header": "sha256=" + digest,
        "delivery_id": delivery_id or str(uuid.uuid4()),
        "event_type": event_type,
        "expected_repository": REPOSITORY,
        "received_at": "2026-11-21T13:00:00Z",
    }


class GitHubWebhookVerifierTests(unittest.TestCase):
    def test_valid_signature_returns_transient_verified_envelope(self):
        result = verify_github_webhook(**signed_delivery())
        self.assertTrue(result["signature_verified"])
        self.assertEqual(result["repository"], REPOSITORY)
        self.assertEqual(result["persistence_owner"], "ROOM_HOP_CORE_EVENT_PATH")
        self.assertEqual(len(result["payload_sha256"]), 64)

    def test_invalid_signature_is_rejected(self):
        args = signed_delivery()
        args["signature_header"] = "sha256=" + ("0" * 64)
        with self.assertRaises(GitHubWebhookError):
            verify_github_webhook(**args)

    def test_short_secret_is_rejected(self):
        args = signed_delivery(secret="short")
        with self.assertRaises(GitHubWebhookError):
            verify_github_webhook(**args)

    def test_missing_signature_header_is_rejected(self):
        args = signed_delivery()
        args["signature_header"] = ""
        with self.assertRaises(GitHubWebhookError):
            verify_github_webhook(**args)

    def test_non_uuid_delivery_id_is_rejected(self):
        args = signed_delivery(delivery_id="not-a-uuid")
        with self.assertRaises(GitHubWebhookError):
            verify_github_webhook(**args)

    def test_unallowlisted_event_type_is_rejected(self):
        args = signed_delivery(event_type="deployment_status")
        with self.assertRaises(GitHubWebhookError):
            verify_github_webhook(**args)

    def test_repository_mismatch_is_rejected(self):
        args = signed_delivery({"repository": {"full_name": "attacker/other"}})
        with self.assertRaises(GitHubWebhookError):
            verify_github_webhook(**args)

    def test_invalid_json_is_rejected(self):
        body = b"{bad-json"
        args = signed_delivery()
        args["raw_body"] = body
        args["signature_header"] = "sha256=" + hmac.new(SECRET.encode(), body, hashlib.sha256).hexdigest()
        with self.assertRaises(GitHubWebhookError):
            verify_github_webhook(**args)

    def test_body_size_limit_is_enforced(self):
        body = b"x" * 200
        args = signed_delivery()
        args["raw_body"] = body
        args["signature_header"] = "sha256=" + hmac.new(SECRET.encode(), body, hashlib.sha256).hexdigest()
        args["max_body_bytes"] = 100
        with self.assertRaises(GitHubWebhookError):
            verify_github_webhook(**args)

    def test_naive_timestamp_is_rejected(self):
        args = signed_delivery()
        args["received_at"] = "2026-11-21T13:00:00"
        with self.assertRaises(GitHubWebhookError):
            verify_github_webhook(**args)

    def test_verifier_does_not_persist_or_queue_delivery(self):
        result = verify_github_webhook(**signed_delivery())
        self.assertNotIn("queue_id", result)
        self.assertNotIn("inbox_state", result)
        self.assertNotIn("event_id", result)
        self.assertNotIn("seq", result)


if __name__ == "__main__":
    unittest.main()
