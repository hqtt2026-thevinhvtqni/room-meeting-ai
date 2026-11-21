import hashlib
import hmac
import json
import unittest

from scripts.w118.webhook_inbox import (
    WebhookInbox,
    WebhookReplayConflict,
    WebhookSecurityError,
)


SECRET = "w118-test-secret-with-at-least-32-characters"
REPOSITORY = "hqtt2026-thevinhvtqni/room-meeting-ai"
DELIVERY = "123e4567-e89b-12d3-a456-426614174000"


def body(repository=REPOSITORY, action="synchronize"):
    return json.dumps(
        {
            "repository": {"full_name": repository},
            "action": action,
            "sender": {"login": "test-actor"},
        },
        sort_keys=True,
    ).encode("utf-8")


def signature(raw):
    digest = hmac.new(SECRET.encode("utf-8"), raw, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


class Work118WebhookInboxTests(unittest.TestCase):
    def setUp(self):
        self.inbox = WebhookInbox()
        self.raw = body()

    def tearDown(self):
        self.inbox.close()

    def ingest(self, raw=None, delivery=DELIVERY, event="pull_request", signature_header=None):
        payload = self.raw if raw is None else raw
        return self.inbox.ingest(
            delivery_id=delivery,
            event_type=event,
            signature_header=signature(payload) if signature_header is None else signature_header,
            secret=SECRET,
            raw_body=payload,
            expected_repository=REPOSITORY,
            received_at="2026-11-21T06:50:00Z",
        )

    def test_valid_signed_delivery_is_stored_pending_without_task_mutation(self):
        result = self.ingest()
        self.assertEqual(result["status"], "RECEIVED")
        self.assertEqual(result["processing_state"], "PENDING")
        self.assertEqual(result["state_effect"], "INBOX_ONLY_NO_TASK_TRANSITION")
        record = self.inbox.get_delivery(DELIVERY)
        self.assertEqual(record["event_type"], "pull_request")
        self.assertEqual(record["payload"]["repository"]["full_name"], REPOSITORY)

    def test_invalid_signature_is_rejected(self):
        with self.assertRaises(WebhookSecurityError):
            self.ingest(signature_header="sha256=" + "0" * 64)

    def test_malformed_signature_header_is_rejected(self):
        with self.assertRaises(WebhookSecurityError):
            self.ingest(signature_header="sha1=bad")

    def test_short_secret_is_rejected(self):
        with self.assertRaises(WebhookSecurityError):
            self.inbox.ingest(
                delivery_id=DELIVERY, event_type="push",
                signature_header=signature(self.raw), secret="short",
                raw_body=self.raw, expected_repository=REPOSITORY,
                received_at="2026-11-21T06:50:00Z",
            )

    def test_non_allowlisted_event_is_rejected(self):
        with self.assertRaises(WebhookSecurityError):
            self.ingest(event="repository_dispatch")

    def test_wrong_repository_is_rejected(self):
        with self.assertRaises(WebhookSecurityError):
            self.ingest(raw=body(repository="attacker/other"))

    def test_invalid_json_is_rejected_after_signature_verification(self):
        raw = b"{not-json"
        with self.assertRaises(WebhookSecurityError):
            self.ingest(raw=raw)

    def test_delivery_id_must_be_uuid(self):
        with self.assertRaises(WebhookSecurityError):
            self.ingest(delivery="not-a-uuid")

    def test_duplicate_delivery_is_idempotent(self):
        first = self.ingest()
        duplicate = self.ingest()
        self.assertEqual(first["status"], "RECEIVED")
        self.assertEqual(duplicate["status"], "DUPLICATE")
        self.assertEqual(len(self.inbox.list_pending()), 1)

    def test_delivery_id_reuse_with_different_payload_is_rejected(self):
        self.ingest()
        changed = body(action="closed")
        with self.assertRaises(WebhookReplayConflict):
            self.ingest(raw=changed)

    def test_pending_delivery_can_be_processed_once(self):
        self.ingest()
        self.inbox.mark_processed(DELIVERY, {"decision": "RECORDED"})
        record = self.inbox.get_delivery(DELIVERY)
        self.assertEqual(record["processing_state"], "PROCESSED")
        self.assertEqual(record["result"], {"decision": "RECORDED"})
        self.assertEqual(self.inbox.list_pending(), [])

    def test_processed_delivery_cannot_be_marked_processed_again(self):
        self.ingest()
        self.inbox.mark_processed(DELIVERY, {"decision": "RECORDED"})
        with self.assertRaises(ValueError):
            self.inbox.mark_processed(DELIVERY, {"decision": "OVERWRITE"})

    def test_pending_limit_is_bounded(self):
        with self.assertRaises(ValueError):
            self.inbox.list_pending(limit=1001)


if __name__ == "__main__":
    unittest.main()
