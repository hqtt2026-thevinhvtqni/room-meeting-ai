import unittest

from scripts.w118.core_task_adapter import (
    CoreTaskContractError,
    normalize_core_task_snapshot,
    project_core_task_to_issue,
)


FIELD_MAP = {
    "work_id": "identity.work_id",
    "task_id": "identity.task_id",
    "correlation_id": "identity.correlation_id",
    "title": "instruction.title",
    "instruction": "instruction.body",
    "status": "state.status",
    "source_revision": "revision",
    "acceptance_checks": "acceptance",
    "wp_id": "identity.wp_id",
    "priority": "instruction.priority",
    "scope_in": "instruction.scope_in",
    "scope_out": "instruction.scope_out",
    "assigned_identity": "assignment.identity",
    "issue_id": "github.issue_id",
    "source_bindings": "source.bindings",
}


def snapshot():
    return {
        "identity": {
            "work_id": "W118", "task_id": "W118-TASK-016",
            "correlation_id": "corr-016", "wp_id": "W118-16",
        },
        "instruction": {
            "title": "Mirror Core Task", "body": "Use the canonical Core Task snapshot.",
            "priority": "P1", "scope_in": ["Issue projection"], "scope_out": ["Task persistence"],
        },
        "state": {"status": "IN_PROGRESS"},
        "revision": "core-rev-1",
        "acceptance": [{"id": "AC-1", "description": "Body reflects Core snapshot"}],
        "assignment": {"identity": None},
        "github": {"issue_id": 65},
        "source": {"bindings": [{"branch": "work/W118/task-W118-TASK-016", "head_sha": "a" * 40, "issue_id": 65}]},
    }


class CoreTaskAdapterTests(unittest.TestCase):
    def test_normalizes_core_snapshot_only_with_explicit_field_map(self):
        projection = normalize_core_task_snapshot(snapshot(), field_map=FIELD_MAP)
        self.assertEqual(projection.task_id, "W118-TASK-016")
        self.assertEqual(projection.status, "IN_PROGRESS")
        self.assertEqual(projection.source_revision, "core-rev-1")
        self.assertEqual(projection.issue_id, 65)
        self.assertEqual(projection.source_bindings[0]["head_sha"], "a" * 40)

    def test_missing_field_mapping_is_rejected(self):
        field_map = dict(FIELD_MAP)
        field_map.pop("task_id")
        with self.assertRaises(CoreTaskContractError):
            normalize_core_task_snapshot(snapshot(), field_map=field_map)

    def test_missing_snapshot_path_is_rejected(self):
        broken = dict(FIELD_MAP)
        broken["task_id"] = "identity.nonexistent"
        with self.assertRaises(CoreTaskContractError):
            normalize_core_task_snapshot(snapshot(), field_map=broken)

    def test_duplicate_acceptance_ids_are_rejected(self):
        bad = snapshot()
        bad["acceptance"] = [
            {"id": "AC-1", "description": "first"},
            {"id": "AC-1", "description": "second"},
        ]
        with self.assertRaises(CoreTaskContractError):
            normalize_core_task_snapshot(bad, field_map=FIELD_MAP)

    def test_issue_id_must_be_positive_or_null(self):
        bad = snapshot()
        bad["github"]["issue_id"] = 0
        with self.assertRaises(CoreTaskContractError):
            normalize_core_task_snapshot(bad, field_map=FIELD_MAP)

    def test_issue_projection_has_stable_marker_and_core_authority(self):
        projection = normalize_core_task_snapshot(snapshot(), field_map=FIELD_MAP)
        issue = project_core_task_to_issue(projection)
        self.assertIn("<!-- room-hop-core-task:W118-TASK-016 -->", issue["body"])
        self.assertIn("Core :8000 is the canonical Task/Assignment/Event authority", issue["body"])
        self.assertIn("room-hop/core-task", issue["labels"])
        self.assertEqual(issue["title"], "[W118] Mirror Core Task")

    def test_issue_projection_does_not_assign_github_user_or_change_core_state(self):
        source = snapshot()
        projection = normalize_core_task_snapshot(source, field_map=FIELD_MAP)
        issue = project_core_task_to_issue(projection)
        self.assertNotIn("assignees", issue)
        self.assertEqual(source["state"]["status"], "IN_PROGRESS")
        self.assertNotIn("event_id", issue)
        self.assertNotIn("seq", issue)


if __name__ == "__main__":
    unittest.main()
