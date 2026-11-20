import unittest
from pathlib import Path

import yaml


WORKFLOW = Path(".github/workflows/w118-workflow-automation.yml")
DIAGNOSTICS = Path(".github/workflows/w118-failure-diagnostics.yml")


class Work118WorkflowContractTests(unittest.TestCase):
    def load_yaml(self, path):
        return yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)

    def test_orchestrator_has_required_events(self):
        data = self.load_yaml(WORKFLOW)
        triggers = data["on"]
        for event in ("push", "pull_request", "workflow_dispatch", "issues", "issue_comment", "pull_request_review"):
            self.assertIn(event, triggers)

    def test_orchestrator_is_read_only_by_default(self):
        data = self.load_yaml(WORKFLOW)
        self.assertEqual(data["permissions"], {"contents": "read"})

    def test_diagnostics_is_separate_and_does_not_list_itself(self):
        data = self.load_yaml(DIAGNOSTICS)
        workflows = data["on"]["workflow_run"]["workflows"]
        self.assertIn("W118 Auto E2E Validation", workflows)
        self.assertNotIn("W118 Failure Diagnostics", workflows)

    def test_diagnostics_only_runs_for_failed_upstream_runs(self):
        data = self.load_yaml(DIAGNOSTICS)
        condition = data["jobs"]["diagnostics"]["if"]
        self.assertIn("failure", condition)


if __name__ == "__main__":
    unittest.main()
