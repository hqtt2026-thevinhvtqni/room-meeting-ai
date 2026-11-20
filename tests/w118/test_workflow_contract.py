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


    def test_handoff_and_ack_jobs_are_event_scoped(self):
        data = self.load_yaml(WORKFLOW)
        self.assertIn("issues", data["on"])
        self.assertIn("issue_comment", data["on"])
        self.assertIn("w118-handoff", data["jobs"]["handoff"]["if"])
        self.assertIn("ACKED-", data["jobs"]["ack-verification"]["if"])

    def test_mutation_permissions_are_job_scoped(self):
        data = self.load_yaml(WORKFLOW)
        self.assertEqual(data["jobs"]["validate"]["permissions"], {"contents": "read"})
        self.assertEqual(data["jobs"]["handoff"]["permissions"]["issues"], "write")
        self.assertEqual(data["jobs"]["ack-verification"]["permissions"]["issues"], "write")
        self.assertEqual(data["permissions"], {"contents": "read"})

    def test_review_job_does_not_merge_or_release(self):
        data = self.load_yaml(WORKFLOW)
        self.assertIn("pull_request_review", data["on"])
        review_steps = str(data["jobs"]["acceptance-review"])
        self.assertNotIn("gh pr merge", review_steps)
        self.assertNotIn("auto-merge", review_steps)


    def test_handoff_idempotency_distinguishes_reapplied_label(self):
        data = self.load_yaml(WORKFLOW)
        steps = data["jobs"]["handoff"]["steps"]
        env = next(step["env"] for step in steps if "ISSUE_UPDATED_AT" in step.get("env", {}))
        self.assertEqual(env["ISSUE_UPDATED_AT"], "${{ github.event.issue.updated_at }}")
        run_script = next(step["run"] for step in steps if "MARKER=" in step.get("run", ""))
        self.assertIn("${ISSUE_UPDATED_AT}", run_script)


    def test_controlled_failure_dispatch_is_owner_gated_and_branch_scoped(self):
        data = self.load_yaml(WORKFLOW)
        dispatch = data["jobs"]["controlled-failure-dispatch"]
        self.assertEqual(dispatch["permissions"]["actions"], "write")
        self.assertIn("W118-TEST-DIAGNOSTICS", dispatch["if"])
        self.assertIn("[W118 E2E TEST]", dispatch["if"])
        self.assertIn("steps.authorize_controlled_failure.outputs.authorized", dispatch["steps"][-1]["if"])
        controlled = data["jobs"]["controlled-failure"]
        self.assertIn("refs/heads/work/118-auto-e2e-v2", controlled["if"])


    def test_controlled_dispatch_targets_isolated_branch_and_input(self):
        data = self.load_yaml(WORKFLOW)
        dispatch = data["jobs"]["controlled-failure-dispatch"]
        run_script = next(step["run"] for step in dispatch["steps"] if "gh workflow run" in step.get("run", ""))
        self.assertIn("--ref work/118-auto-e2e-v2", run_script)
        self.assertIn("failure_injection=controlled", run_script)

    def test_diagnostics_listens_to_w118_w300_and_work70(self):
        data = self.load_yaml(DIAGNOSTICS)
        workflows = data["on"]["workflow_run"]["workflows"]
        self.assertIn("W118 Auto E2E Validation", workflows)
        self.assertIn("W300 Dashboard CI", workflows)
        self.assertIn("Work 70 Preview Host Tests", workflows)

    def test_ack_result_is_deduplicated_by_source_comment_id(self):
        data = self.load_yaml(WORKFLOW)
        run_script = next(step["run"] for step in data["jobs"]["ack-verification"]["steps"] if "MARKER=" in step.get("run", ""))
        self.assertIn("w118-ack-result", run_script)
        self.assertIn("COMMENT_ID", run_script)

    def test_diagnostics_runtime_uses_workflow_sha_and_attempt_keys(self):
        data = self.load_yaml(DIAGNOSTICS)
        run_script = data["jobs"]["diagnostics"]["steps"][-1]["run"]
        self.assertIn('--workflow-id "$WF_ID"', run_script)
        self.assertIn('--sha "$SHA"', run_script)
        self.assertIn('--attempt "$RUN_ATTEMPT"', run_script)

    def test_diagnostics_planner_is_part_of_runtime(self):
        self.assertTrue(Path("scripts/w118/diagnostics.py").is_file())
        self.assertTrue(Path("tests/w118/test_diagnostics.py").is_file())

    def test_diagnostics_only_runs_for_failed_upstream_runs(self):
        data = self.load_yaml(DIAGNOSTICS)
        condition = data["jobs"]["diagnostics"]["if"]
        self.assertIn("failure", condition)


if __name__ == "__main__":
    unittest.main()
