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
            "objective": "Track Task and Assignment as separate state machines",
            "scope_in": ["Task schema", "Assignment lifecycle", "event history"],
            "scope_out": ["GitHub API calls", "live Agent runtime dispatch"],
            "priority": "P0",
            "acceptance_criteria": [{
                "id": "AC-1",
                "description": "Task and Assignment statuses are independent",
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

    def task_status(self, status, role, principal, version, suffix, details=None, evidence=()):
        return self.registry.transition_task(
            "W118-TASK-001", status,
            actor_principal=principal, actor_role=role, identity_verified=True,
            expected_version=version, event_id=f"evt-task-{suffix}",
            idempotency_key=f"idem-task-{suffix}",
            occurred_at=f"2026-11-21T06:{int(suffix):02d}:00Z",
            details=details or {}, evidence_refs=evidence,
        )

    def assignment_status(self, status, role, principal, version, suffix, details=None, evidence=()):
        return self.registry.transition_assignment(
            "W118-TASK-001", status,
            actor_principal=principal, actor_role=role, identity_verified=True,
            expected_version=version, event_id=f"evt-asg-{suffix}",
            idempotency_key=f"idem-asg-{suffix}",
            occurred_at=f"2026-11-21T07:{int(suffix):02d}:00Z",
            details=details or {}, evidence_refs=evidence,
        )

    def ready_and_link_issue(self):
        self.task_status("READY", "owner", "owner:vinh", 1, "01")
        return self.registry.link_issue(
            "W118-TASK-001", 65, "https://github.com/example/repo/issues/65",
            actor_principal="room:orchestrator", actor_role="orchestrator", identity_verified=True,
            expected_version=2, event_id="evt-issue-link", idempotency_key="idem-issue-link",
            occurred_at="2026-11-21T06:02:00Z", evidence_refs=["github://issues/65/readback"],
        )

    def propose_dispatch_ack(self):
        self.ready_and_link_issue()
        self.assignment_status("PROPOSED", "orchestrator", "room:orchestrator", 3, "01", {
            "assignment_id": "asg-001",
            "assigned_agent_id": "agent-ka",
            "assigned_principal": "agent:ka-runtime",
            "assignment_policy_version": "policy-1",
            "capability_match": ["python"],
            "assignment_evidence_ref": "assignment://001",
        })
        self.assignment_status("DISPATCHED", "orchestrator", "room:orchestrator", 4, "02", {
            "dispatch_id": "dispatch-001",
            "dispatch_receipt_ref": "dispatch://receipt-001",
        })
        self.assignment_status("ACKNOWLEDGED", "executor", "agent:ka-runtime", 5, "03", {
            "dispatch_id": "dispatch-001",
            "ack_event_id": "ack-001",
            "ack_nonce_ref": "nonce-ref-001",
        })

    def test_create_starts_planned_and_unassigned(self):
        task = self.registry.get_task("W118-TASK-001")
        self.assertEqual(task["status"], "PLANNED")
        self.assertEqual(task["assignment_status"], "UNASSIGNED")
        self.assertEqual(task["version"], 1)
        self.assertEqual(self.registry.list_events("W118-TASK-001")[0]["event_type"], "task.created")

    def test_only_verified_owner_can_create_task(self):
        with self.assertRaises(TransitionDenied):
            self.registry.create_task(
                {**self.task, "task_id": "W118-TASK-002"},
                actor_principal="agent:ka", actor_role="executor", identity_verified=True,
                event_id="evt-create-2", occurred_at="2026-11-21T06:00:00Z",
            )

    def test_unverified_actor_fails_closed(self):
        with self.assertRaises(TransitionDenied):
            self.registry.transition_task(
                "W118-TASK-001", "READY",
                actor_principal="owner:vinh", actor_role="owner", identity_verified=False,
                expected_version=1, event_id="evt-unverified", idempotency_key="idem-unverified",
                occurred_at="2026-11-21T06:01:00Z",
            )

    def test_invalid_task_contract_is_rejected(self):
        invalid = {**self.task, "task_id": "W118-TASK-003", "acceptance_criteria": []}
        with self.assertRaises(TaskValidationError):
            self.registry.create_task(
                invalid, actor_principal="owner:vinh", actor_role="owner",
                identity_verified=True, event_id="evt-invalid", occurred_at="2026-11-21T06:00:00Z",
            )

    def test_task_id_must_match_work_id_contract(self):
        invalid = {**self.task, "task_id": "W117-TASK-002"}
        with self.assertRaises(TaskValidationError):
            self.registry.create_task(
                invalid, actor_principal="owner:vinh", actor_role="owner",
                identity_verified=True, event_id="evt-wrong-work-id",
                occurred_at="2026-11-21T06:00:00Z",
            )

    def test_task_ready_requires_owner_or_orchestrator(self):
        with self.assertRaises(TransitionDenied):
            self.task_status("READY", "executor", "agent:ka-runtime", 1, "01")

    def test_owner_principal_must_match_task_owner(self):
        with self.assertRaises(TransitionDenied):
            self.task_status("READY", "owner", "owner:other", 1, "01")

    def test_issue_link_requires_readback_evidence(self):
        self.task_status("READY", "owner", "owner:vinh", 1, "01")
        with self.assertRaises(TaskValidationError):
            self.registry.link_issue(
                "W118-TASK-001", 65, "https://github.com/example/repo/issues/65",
                actor_principal="room:orchestrator", actor_role="orchestrator", identity_verified=True,
                expected_version=2, event_id="evt-issue-no-evidence", idempotency_key="idem-issue-no-evidence",
                occurred_at="2026-11-21T06:02:00Z", evidence_refs=[],
            )

    def test_issue_link_is_idempotent_and_readback_verified(self):
        self.task_status("READY", "owner", "owner:vinh", 1, "01")
        kwargs = {
            "actor_principal": "room:orchestrator", "actor_role": "orchestrator",
            "identity_verified": True, "expected_version": 2,
            "event_id": "evt-issue-link", "idempotency_key": "idem-issue-link",
            "occurred_at": "2026-11-21T06:02:00Z", "evidence_refs": ["github://issues/65/readback"],
        }
        first = self.registry.link_issue("W118-TASK-001", 65, "https://github.com/example/repo/issues/65", **kwargs)
        replay = self.registry.link_issue("W118-TASK-001", 65, "https://github.com/example/repo/issues/65", **kwargs)
        self.assertFalse(first["replayed"])
        self.assertTrue(replay["replayed"])
        self.assertEqual(replay["task"]["issue_id"], 65)
        self.assertEqual(replay["task"]["status"], "READY")

    def test_assignment_lifecycle_is_separate_from_task_status(self):
        self.propose_dispatch_ack()
        task = self.registry.get_task("W118-TASK-001")
        self.assertEqual(task["assignment_status"], "ACKNOWLEDGED")
        self.assertEqual(task["status"], "READY")

    def test_executor_ack_must_match_assignment_and_dispatch(self):
        self.ready_and_link_issue()
        self.assignment_status("PROPOSED", "orchestrator", "room:orchestrator", 3, "01", {
            "assignment_id": "asg-001", "assigned_agent_id": "agent-ka",
            "assigned_principal": "agent:ka-runtime", "assignment_policy_version": "policy-1",
            "capability_match": ["python"], "assignment_evidence_ref": "assignment://001",
        })
        self.assignment_status("DISPATCHED", "orchestrator", "room:orchestrator", 4, "02", {
            "dispatch_id": "dispatch-001", "dispatch_receipt_ref": "dispatch://receipt-001",
        })
        with self.assertRaises(TransitionDenied):
            self.assignment_status("ACKNOWLEDGED", "executor", "agent:other", 5, "03", {
                "dispatch_id": "dispatch-001", "ack_event_id": "ack-001", "ack_nonce_ref": "nonce-ref-001",
            })
        with self.assertRaises(TransitionDenied):
            self.assignment_status("ACKNOWLEDGED", "executor", "agent:ka-runtime", 5, "04", {
                "dispatch_id": "dispatch-wrong", "ack_event_id": "ack-002", "ack_nonce_ref": "nonce-ref-002",
            })

    def test_task_in_progress_requires_acknowledged_assignment(self):
        self.ready_and_link_issue()
        with self.assertRaises(TransitionDenied):
            self.task_status("IN_PROGRESS", "orchestrator", "room:orchestrator", 3, "01")

    def test_agent_cannot_accept_own_assignment(self):
        self.propose_dispatch_ack()
        self.assignment_status("IN_PROGRESS", "executor", "agent:ka-runtime", 6, "04")
        self.assignment_status("SUBMITTED", "executor", "agent:ka-runtime", 7, "05", {
            "result_ref": "result://001",
        })
        with self.assertRaises(TransitionDenied):
            self.assignment_status("ACCEPTED", "executor", "agent:ka-runtime", 8, "06", evidence=["evidence://self"])

    def test_full_task_and_assignment_lifecycle(self):
        self.propose_dispatch_ack()
        self.assignment_status("IN_PROGRESS", "executor", "agent:ka-runtime", 6, "04")
        self.task_status("IN_PROGRESS", "orchestrator", "room:orchestrator", 7, "02")
        self.assignment_status("SUBMITTED", "executor", "agent:ka-runtime", 8, "05", {
            "result_ref": "result://001",
        })
        self.task_status("IN_REVIEW", "orchestrator", "room:orchestrator", 9, "03", {
            "review_request_ref": "review://001",
        })
        self.assignment_status("ACCEPTED", "verifier", "qe:go", 10, "06", evidence=["evidence://qe-pass"])
        self.task_status("DONE", "owner", "owner:vinh", 11, "04", evidence=["evidence://owner-accept"])
        task = self.registry.get_task("W118-TASK-001")
        self.assertEqual(task["status"], "DONE")
        self.assertEqual(task["assignment_status"], "ACCEPTED")
        self.assertEqual(task["version"], 12)

    def test_task_done_requires_assignment_accepted_and_owner_evidence(self):
        self.task_status("READY", "owner", "owner:vinh", 1, "01")
        with self.assertRaises(TransitionDenied):
            self.task_status("DONE", "owner", "owner:vinh", 2, "02", evidence=["evidence://fake"])

    def test_assignment_accepted_requires_verifier_evidence(self):
        self.propose_dispatch_ack()
        self.assignment_status("IN_PROGRESS", "executor", "agent:ka-runtime", 6, "04")
        self.assignment_status("SUBMITTED", "executor", "agent:ka-runtime", 7, "05", {"result_ref": "result://001"})
        with self.assertRaises(TaskValidationError):
            self.assignment_status("ACCEPTED", "verifier", "qe:go", 8, "06")

    def test_stale_version_is_rejected(self):
        self.task_status("READY", "owner", "owner:vinh", 1, "01")
        with self.assertRaises(VersionConflict):
            self.registry.link_issue(
                "W118-TASK-001", 65, "https://github.com/example/repo/issues/65",
                actor_principal="room:orchestrator", actor_role="orchestrator", identity_verified=True,
                expected_version=1, event_id="evt-stale-link", idempotency_key="idem-stale-link",
                occurred_at="2026-11-21T06:02:00Z", evidence_refs=["github://issues/65/readback"],
            )

    def test_duplicate_task_status_event_is_idempotent(self):
        first = self.task_status("READY", "owner", "owner:vinh", 1, "01")
        replay = self.registry.transition_task(
            "W118-TASK-001", "READY", actor_principal="owner:vinh", actor_role="owner",
            identity_verified=True, expected_version=1, event_id="evt-replay",
            idempotency_key="idem-task-01", occurred_at="2026-11-21T06:01:00Z",
        )
        self.assertFalse(first["replayed"])
        self.assertTrue(replay["replayed"])
        self.assertEqual(replay["task"]["version"], 2)

    def test_idempotency_key_cannot_be_reused_for_different_status(self):
        self.task_status("READY", "owner", "owner:vinh", 1, "01")
        with self.assertRaises(IdempotencyConflict):
            self.registry.transition_task(
                "W118-TASK-001", "CANCELLED", actor_principal="owner:vinh", actor_role="owner",
                identity_verified=True, expected_version=2, event_id="evt-conflict",
                idempotency_key="idem-task-01", occurred_at="2026-11-21T06:02:00Z",
                details={"reason": "different operation"},
            )

    def test_transition_details_cannot_overwrite_task_identity(self):
        with self.assertRaises(TaskValidationError):
            self.registry.transition_task(
                "W118-TASK-001", "READY", actor_principal="owner:vinh", actor_role="owner",
                identity_verified=True, expected_version=1, event_id="evt-overwrite",
                idempotency_key="idem-overwrite", occurred_at="2026-11-21T06:01:00Z",
                details={"owner_principal": "owner:attacker"},
            )

    def test_external_source_observation_is_append_only_without_status_change(self):
        result = self.registry.record_observation(
            "W118-TASK-001", "source.push_bound",
            actor_principal="room-hop:event-listener", actor_role="orchestrator", identity_verified=True,
            event_id="delivery-push-001", idempotency_key="github:delivery-push-001",
            occurred_at="2026-11-21T06:20:00Z",
            evidence_refs=["github://commit/" + "a" * 40],
            details={"branch": "work/W118/task-W118-TASK-001", "head_sha": "a" * 40, "issue_id": 65},
        )
        self.assertFalse(result["replayed"])
        self.assertEqual(result["task"]["status"], "PLANNED")
        self.assertEqual(result["task"]["assignment_status"], "UNASSIGNED")
        self.assertEqual(result["task"]["version"], 1)
        event = self.registry.list_events("W118-TASK-001")[-1]
        self.assertEqual(event["event_type"], "source.push_bound")
        self.assertEqual(event["from_state"], event["to_state"])

    def test_external_observation_is_idempotent(self):
        kwargs = {
            "actor_principal": "room-hop:event-listener", "actor_role": "orchestrator",
            "identity_verified": True, "event_id": "delivery-push-002",
            "idempotency_key": "github:delivery-push-002", "occurred_at": "2026-11-21T06:21:00Z",
            "evidence_refs": ["github://commit/" + "b" * 40],
            "details": {"branch": "work/W118/task-W118-TASK-001", "head_sha": "b" * 40, "issue_id": 65},
        }
        first = self.registry.record_observation("W118-TASK-001", "source.push_bound", **kwargs)
        second = self.registry.record_observation("W118-TASK-001", "source.push_bound", **kwargs)
        self.assertFalse(first["replayed"])
        self.assertTrue(second["replayed"])
        self.assertEqual(len(self.registry.list_events("W118-TASK-001")), 2)

    def test_executor_cannot_record_github_observation(self):
        with self.assertRaises(TransitionDenied):
            self.registry.record_observation(
                "W118-TASK-001", "source.push_bound", actor_principal="agent:ka",
                actor_role="executor", identity_verified=True, event_id="delivery-push-003",
                idempotency_key="github:delivery-push-003", occurred_at="2026-11-21T06:22:00Z",
                details={"commit_sha": "c" * 40},
            )

    def test_event_history_is_append_only_and_ordered(self):
        self.task_status("READY", "owner", "owner:vinh", 1, "01")
        events = self.registry.list_events("W118-TASK-001")
        self.assertEqual([event["to_state"] for event in events], ["PLANNED", "READY"])
        self.assertEqual(events[1]["from_state"], "PLANNED")


if __name__ == "__main__":
    unittest.main()
