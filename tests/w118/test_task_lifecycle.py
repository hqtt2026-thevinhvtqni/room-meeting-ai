import unittest

from scripts.w118.task_lifecycle import (
    IdempotencyConflict,
    TaskRegistry,
    TaskValidationError,
    TransitionDenied,
    VersionConflict,
)


class Work118TaskLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.registry = TaskRegistry()
        self.task = {
            "schema_version": "1.0",
            "work_id": "W118",
            "wp_id": "W118-13",
            "task_id": "W118-TASK-001",
            "title": "Build Task lifecycle contract",
            "objective": "Track one Task through verified lifecycle transitions",
            "scope_in": ["Task schema", "state transitions", "event history"],
            "scope_out": ["GitHub API calls", "agent runtime dispatch"],
            "priority": "P0",
            "acceptance_criteria": [{
                "id": "AC-1",
                "description": "Transitions are authorized and versioned",
                "verification_method": "unit tests",
            }],
            "required_capabilities": ["python", "workflow-automation"],
            "risk_level": "MEDIUM",
            "dependencies": [],
            "owner_principal": "owner:vinh",
        }
        self.registry.create_task(
            self.task,
            actor_principal="owner:vinh",
            actor_role="owner",
            identity_verified=True,
            event_id="evt-create-1",
            occurred_at="2026-11-21T06:00:00Z",
        )

    def tearDown(self):
        self.registry.close()

    def transition(self, state, role, principal, version, suffix, details=None, evidence=()):
        return self.registry.transition_task(
            "W118-TASK-001",
            state,
            actor_principal=principal,
            actor_role=role,
            identity_verified=True,
            expected_version=version,
            event_id=f"evt-{suffix}",
            idempotency_key=f"idem-{suffix}",
            occurred_at=f"2026-11-21T06:{int(suffix):02d}:00Z",
            details=details or {},
            evidence_refs=evidence,
        )

    def advance_to_dispatched(self):
        self.transition("READY", "owner", "owner:vinh", 1, "01")
        self.transition(
            "ISSUE_LINKED", "orchestrator", "room:orchestrator", 2, "02",
            {"issue_id": 65, "issue_url": "https://github.com/example/repo/issues/65"},
        )
        self.transition(
            "ASSIGNED", "orchestrator", "room:orchestrator", 3, "03",
            {
                "assignment_id": "asg-001",
                "assigned_agent_id": "agent-ka",
                "assigned_principal": "agent:ka-runtime",
                "assignment_policy_version": "policy-1",
                "capability_match": ["python"],
                "assignment_evidence_ref": "assignment://001",
            },
        )
        self.transition(
            "DISPATCHED", "orchestrator", "room:orchestrator", 4, "04",
            {"dispatch_id": "dispatch-001", "dispatch_receipt_ref": "dispatch://receipt-001"},
        )

    def test_create_starts_in_draft_with_version_one_and_event(self):
        task = self.registry.get_task("W118-TASK-001")
        self.assertEqual(task["state"], "DRAFT")
        self.assertEqual(task["version"], 1)
        events = self.registry.list_events("W118-TASK-001")
        self.assertEqual([event["event_type"] for event in events], ["task.created"])

    def test_only_verified_owner_can_create_task(self):
        with self.assertRaises(TransitionDenied):
            self.registry.create_task(
                {**self.task, "task_id": "W118-TASK-002"},
                actor_principal="agent:ka",
                actor_role="executor",
                identity_verified=True,
                event_id="evt-create-2",
                occurred_at="2026-11-21T06:00:00Z",
            )

    def test_unverified_actor_fails_closed(self):
        with self.assertRaises(TransitionDenied):
            self.registry.transition_task(
                "W118-TASK-001", "READY",
                actor_principal="owner:vinh", actor_role="owner",
                identity_verified=False, expected_version=1,
                event_id="evt-unverified", idempotency_key="idem-unverified",
                occurred_at="2026-11-21T06:01:00Z",
            )

    def test_invalid_task_contract_is_rejected(self):
        invalid = {**self.task, "task_id": "W118-TASK-003", "acceptance_criteria": []}
        with self.assertRaises(TaskValidationError):
            self.registry.create_task(
                invalid, actor_principal="owner:vinh", actor_role="owner",
                identity_verified=True, event_id="evt-invalid",
                occurred_at="2026-11-21T06:00:00Z",
            )

    def test_task_id_must_match_work_id_contract(self):
        invalid = {**self.task, "task_id": "W117-TASK-002"}
        with self.assertRaises(TaskValidationError):
            self.registry.create_task(
                invalid, actor_principal="owner:vinh", actor_role="owner",
                identity_verified=True, event_id="evt-wrong-work-id",
                occurred_at="2026-11-21T06:00:00Z",
            )

    def test_task_cannot_be_readied_by_executor(self):
        with self.assertRaises(TransitionDenied):
            self.transition("READY", "executor", "agent:ka-runtime", 1, "05")

    def test_full_lifecycle_requires_separate_authorities_and_evidence(self):
        self.advance_to_dispatched()
        self.transition(
            "ACKED", "executor", "agent:ka-runtime", 5, "05",
            {"dispatch_id": "dispatch-001", "ack_event_id": "ack-001", "ack_nonce_ref": "nonce-ref-001"},
        )
        self.transition("STARTED", "executor", "agent:ka-runtime", 6, "06")
        self.transition("IN_PROGRESS", "executor", "agent:ka-runtime", 7, "07")
        self.transition("COMPLETED", "executor", "agent:ka-runtime", 8, "08", {"result_ref": "result://001"})
        self.transition("VERIFYING", "orchestrator", "room:orchestrator", 9, "09", {"result_ref": "result://001"})
        self.transition("VERIFIED", "verifier", "qe:go", 10, "10", evidence=["evidence://test-report"])
        self.transition("ACCEPTED", "owner", "owner:vinh", 11, "11", evidence=["evidence://acceptance"])
        self.transition(
            "CLOSED", "orchestrator", "room:orchestrator", 12, "12",
            {"issue_sync_verified": True, "issue_sync_evidence_ref": "github://issue/65/readback"},
        )
        task = self.registry.get_task("W118-TASK-001")
        self.assertEqual(task["state"], "CLOSED")
        self.assertEqual(task["version"], 13)
        self.assertEqual(len(self.registry.list_events("W118-TASK-001")), 13)

    def test_ack_must_match_active_assignment_and_dispatch(self):
        self.advance_to_dispatched()
        with self.assertRaises(TransitionDenied):
            self.transition(
                "ACKED", "executor", "agent:other", 5, "05",
                {"dispatch_id": "dispatch-001", "ack_event_id": "ack-001", "ack_nonce_ref": "nonce-ref-001"},
            )
        with self.assertRaises(TransitionDenied):
            self.transition(
                "ACKED", "executor", "agent:ka-runtime", 5, "06",
                {"dispatch_id": "dispatch-wrong", "ack_event_id": "ack-002", "ack_nonce_ref": "nonce-ref-002"},
            )

    def test_ci_or_agent_cannot_accept_task(self):
        self.advance_to_dispatched()
        with self.assertRaises(TransitionDenied):
            self.transition("ACCEPTED", "executor", "agent:ka-runtime", 5, "05", evidence=["ci://pass"])

    def test_verified_requires_evidence(self):
        self.advance_to_dispatched()
        self.transition("ACKED", "executor", "agent:ka-runtime", 5, "05", {
            "dispatch_id": "dispatch-001", "ack_event_id": "ack-001", "ack_nonce_ref": "nonce-ref-001"
        })
        self.transition("STARTED", "executor", "agent:ka-runtime", 6, "06")
        self.transition("IN_PROGRESS", "executor", "agent:ka-runtime", 7, "07")
        self.transition("COMPLETED", "executor", "agent:ka-runtime", 8, "08", {"result_ref": "result://001"})
        self.transition("VERIFYING", "orchestrator", "room:orchestrator", 9, "09", {"result_ref": "result://001"})
        with self.assertRaises(TaskValidationError):
            self.transition("VERIFIED", "verifier", "qe:go", 10, "10")

    def test_closed_requires_issue_sync_readback(self):
        self.advance_to_dispatched()
        self.transition("ACKED", "executor", "agent:ka-runtime", 5, "05", {
            "dispatch_id": "dispatch-001", "ack_event_id": "ack-001", "ack_nonce_ref": "nonce-ref-001"
        })
        self.transition("STARTED", "executor", "agent:ka-runtime", 6, "06")
        self.transition("IN_PROGRESS", "executor", "agent:ka-runtime", 7, "07")
        self.transition("COMPLETED", "executor", "agent:ka-runtime", 8, "08", {"result_ref": "result://001"})
        self.transition("VERIFYING", "orchestrator", "room:orchestrator", 9, "09", {"result_ref": "result://001"})
        self.transition("VERIFIED", "verifier", "qe:go", 10, "10", evidence=["evidence://test"])
        self.transition("ACCEPTED", "owner", "owner:vinh", 11, "11", evidence=["evidence://accept"])
        with self.assertRaises(TaskValidationError):
            self.transition("CLOSED", "orchestrator", "room:orchestrator", 12, "12", {"issue_sync_verified": False})

    def test_stale_version_is_rejected(self):
        self.transition("READY", "owner", "owner:vinh", 1, "01")
        with self.assertRaises(VersionConflict):
            self.transition("ISSUE_LINKED", "orchestrator", "room:orchestrator", 1, "02", {
                "issue_id": 65, "issue_url": "https://github.com/example/repo/issues/65"
            })

    def test_duplicate_event_is_idempotent(self):
        first = self.transition("READY", "owner", "owner:vinh", 1, "01")
        replay = self.registry.transition_task(
            "W118-TASK-001", "READY",
            actor_principal="owner:vinh", actor_role="owner", identity_verified=True,
            expected_version=1, event_id="evt-replay", idempotency_key="idem-01",
            occurred_at="2026-11-21T06:01:00Z",
        )
        self.assertFalse(first["replayed"])
        self.assertTrue(replay["replayed"])
        self.assertEqual(replay["task"]["version"], 2)
        self.assertEqual(len(self.registry.list_events("W118-TASK-001")), 2)

    def test_idempotency_key_cannot_be_reused_for_different_operation(self):
        self.transition("READY", "owner", "owner:vinh", 1, "01")
        with self.assertRaises(IdempotencyConflict):
            self.registry.transition_task(
                "W118-TASK-001", "CANCELLED",
                actor_principal="owner:vinh", actor_role="owner", identity_verified=True,
                expected_version=2, event_id="evt-conflict", idempotency_key="idem-01",
                occurred_at="2026-11-21T06:02:00Z", details={"reason": "different operation"},
            )

    def test_owner_principal_must_match_task_owner(self):
        with self.assertRaises(TransitionDenied):
            self.registry.transition_task(
                "W118-TASK-001", "READY",
                actor_principal="owner:other", actor_role="owner", identity_verified=True,
                expected_version=1, event_id="evt-other-owner", idempotency_key="idem-other-owner",
                occurred_at="2026-11-21T06:01:00Z",
            )

    def test_transition_details_cannot_overwrite_task_identity_or_state(self):
        with self.assertRaises(TaskValidationError):
            self.registry.transition_task(
                "W118-TASK-001", "READY",
                actor_principal="owner:vinh", actor_role="owner", identity_verified=True,
                expected_version=1, event_id="evt-payload-overwrite", idempotency_key="idem-payload-overwrite",
                occurred_at="2026-11-21T06:01:00Z",
                details={"owner_principal": "owner:attacker"},
            )

    def test_invalid_transition_is_rejected(self):
        with self.assertRaises(TransitionDenied):
            self.transition("ACKED", "executor", "agent:ka-runtime", 1, "01")

    def test_external_source_observation_is_append_only_without_state_change(self):
        result = self.registry.record_observation(
            "W118-TASK-001", "source.push_bound",
            actor_principal="github:webhook", actor_role="orchestrator", identity_verified=True,
            event_id="delivery-push-001", idempotency_key="github:delivery-push-001",
            occurred_at="2026-11-21T06:20:00Z",
            evidence_refs=["github://commit/" + "a" * 40],
            details={"branch": "work/W118/task-W118-TASK-001", "commit_sha": "a" * 40, "issue_id": 65},
        )
        self.assertFalse(result["replayed"])
        self.assertEqual(result["task"]["state"], "DRAFT")
        self.assertEqual(result["task"]["version"], 1)
        event = self.registry.list_events("W118-TASK-001")[-1]
        self.assertEqual(event["event_type"], "source.push_bound")
        self.assertEqual(event["from_state"], event["to_state"])

    def test_external_observation_is_idempotent(self):
        kwargs = {
            "actor_principal": "github:webhook",
            "actor_role": "orchestrator",
            "identity_verified": True,
            "event_id": "delivery-push-002",
            "idempotency_key": "github:delivery-push-002",
            "occurred_at": "2026-11-21T06:21:00Z",
            "evidence_refs": ["github://commit/" + "b" * 40],
            "details": {"branch": "work/W118/task-W118-TASK-001", "commit_sha": "b" * 40, "issue_id": 65},
        }
        first = self.registry.record_observation("W118-TASK-001", "source.push_bound", **kwargs)
        second = self.registry.record_observation("W118-TASK-001", "source.push_bound", **kwargs)
        self.assertFalse(first["replayed"])
        self.assertTrue(second["replayed"])
        self.assertEqual(len(self.registry.list_events("W118-TASK-001")), 2)

    def test_executor_cannot_record_github_observation(self):
        with self.assertRaises(TransitionDenied):
            self.registry.record_observation(
                "W118-TASK-001", "source.push_bound",
                actor_principal="agent:ka", actor_role="executor", identity_verified=True,
                event_id="delivery-push-003", idempotency_key="github:delivery-push-003",
                occurred_at="2026-11-21T06:22:00Z",
                details={"commit_sha": "c" * 40},
            )

    def test_event_history_is_append_only_and_ordered(self):
        self.transition("READY", "owner", "owner:vinh", 1, "01")
        events = self.registry.list_events("W118-TASK-001")
        self.assertEqual([event["to_state"] for event in events], ["DRAFT", "READY"])
        self.assertEqual(events[1]["from_state"], "DRAFT")


if __name__ == "__main__":
    unittest.main()
