import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTER_PATH = ROOT / "work/118/HQTT-GITHUB-WORKFLOW-AUTOMATION/04_PLAN/TASK_REGISTER.json"
SCHEMA_PATH = ROOT / "work/118/HQTT-GITHUB-WORKFLOW-AUTOMATION/04_PLAN/TASK_REGISTER.schema.json"
TASK_STATUSES = {"PLANNED", "READY", "IN_PROGRESS", "BLOCKED", "IN_REVIEW", "DONE", "CANCELLED"}
ASSIGNMENT_STATUSES = {
    "UNASSIGNED", "PROPOSED", "DISPATCHED", "ACKNOWLEDGED", "IN_PROGRESS",
    "SUBMITTED", "ACCEPTED", "REJECTED", "BLOCKED", "CANCELLED",
}


class Work118TaskRegisterContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.register = json.loads(REGISTER_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    def test_register_schema_identity_and_task_count(self):
        self.assertEqual(self.register["work_id"], "W118")
        self.assertEqual(self.register["document_id"], "TASK_REGISTER")
        self.assertEqual(self.schema["properties"]["work_id"]["const"], "W118")
        self.assertEqual(self.register["task_count"], len(self.register["tasks"]))
        self.assertEqual(self.register["task_count"], 7)

    def test_task_ids_are_unique_and_work_scoped(self):
        ids = [task["task_id"] for task in self.register["tasks"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(task_id.startswith("W118-TASK-") for task_id in ids))

    def test_task_and_assignment_status_vocabularies_are_separate(self):
        self.assertEqual(set(self.register["status_model"]), TASK_STATUSES)
        self.assertEqual(set(self.register["assignment_status_model"]), ASSIGNMENT_STATUSES)
        for task in self.register["tasks"]:
            self.assertIn(task["status"], TASK_STATUSES)
            self.assertIn(task["assignment_status"], ASSIGNMENT_STATUSES)
            self.assertNotIn(task["status"], {"ACKNOWLEDGED", "SUBMITTED", "ACCEPTED"})

    def test_dependencies_resolve_to_registered_tasks(self):
        ids = {task["task_id"] for task in self.register["tasks"]}
        for task in self.register["tasks"]:
            self.assertTrue(set(task["dependencies"]).issubset(ids))
            self.assertNotIn(task["task_id"], task["dependencies"])

    def test_unverified_runtime_agents_are_not_marked_assigned(self):
        for task in self.register["tasks"]:
            if task["assigned_identity"] is None:
                self.assertEqual(task["assignment_status"], "UNASSIGNED")

    def test_owner_directed_tasks_have_directive_but_no_fabricated_agent_identity(self):
        for task in self.register["tasks"]:
            if task["execution_mode"] == "OWNER_DIRECTED_SESSION":
                self.assertTrue(task["owner_directive_ref"])
                self.assertIsNone(task["assigned_identity"])
                self.assertEqual(task["assignment_status"], "UNASSIGNED")
            else:
                self.assertIsNone(task["owner_directive_ref"])

    def test_register_declares_sandbox_authority_and_github_mirror(self):
        self.assertIn("Sandbox", self.register["source_of_truth"])
        self.assertIn("github.com", self.register["github_mirror"])
        self.assertTrue(any("not a second canonical Task Register" in rule for rule in self.register["rules"]))


if __name__ == "__main__":
    unittest.main()
