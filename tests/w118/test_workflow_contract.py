import re
import unittest
from pathlib import Path

import yaml


WORKFLOW = Path(".github/workflows/w118-workflow-automation.yml")
DIAGNOSTICS = Path(".github/workflows/w118-failure-diagnostics.yml")
PR_CHECKLIST = Path(".github/workflows/w118-pr-review-checklist.yml")


class Work118WorkflowContractTests(unittest.TestCase):
    def test_all_workflow_actions_are_pinned_to_full_commit_shas(self):
        for path in (WORKFLOW, DIAGNOSTICS, PR_CHECKLIST):
            references = re.findall(r"^\s*uses:\s*([^\s#]+)", path.read_text(encoding="utf-8"), re.MULTILINE)
            for reference in references:
                self.assertRegex(
                    reference,
                    r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[0-9a-f]{40}$",
                    f"{path} contains a mutable or non-SHA action reference: {reference}",
                )

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
        self.assertIn("w118-handoff", data["jobs"]["handoff-request-capture"]["if"])
        self.assertIn("ACKED-", data["jobs"]["ack-claim-capture"]["if"])

    def test_mutation_permissions_are_job_scoped(self):
        data = self.load_yaml(WORKFLOW)
        self.assertEqual(data["jobs"]["validate"]["permissions"], {"contents": "read"})
        self.assertEqual(data["jobs"]["handoff-request-capture"]["permissions"]["issues"], "write")
        self.assertEqual(data["jobs"]["ack-claim-capture"]["permissions"]["issues"], "write")
        self.assertEqual(data["permissions"], {"contents": "read"})

    def test_review_observation_captures_pr_revisions_without_authorizing_acceptance(self):
        data = self.load_yaml(WORKFLOW)
        steps = data["jobs"]["review-observation-capture"]["steps"]
        evidence_step = next(step for step in steps if step.get("name") == "Write review observation evidence")
        self.assertEqual(evidence_step["env"]["PR_HEAD_SHA"], "${{ github.event.pull_request.head.sha }}")
        self.assertEqual(evidence_step["env"]["PR_BASE_SHA"], "${{ github.event.pull_request.base.sha }}")
        self.assertIn('"reviewer_authority_verified": False', evidence_step["run"])
        self.assertIn('"task_acceptance_changed": False', evidence_step["run"])
        self.assertNotIn("review_authorization.py", str(steps))

    def test_ack_claim_capture_is_scoped_but_does_not_verify_or_transition_assignment(self):
        data = self.load_yaml(WORKFLOW)
        condition = data["jobs"]["ack-claim-capture"]["if"]
        self.assertIn("w118-handoff", condition)
        self.assertIn("ACKED-", condition)
        steps = data["jobs"]["ack-claim-capture"]["steps"]
        capture = next(step for step in steps if step.get("name") == "Capture ACK claim without authorizing Agent identity")
        self.assertNotIn("authorization.py", capture["run"])
        self.assertNotIn("gh issue edit", capture["run"])
        self.assertIn("No Assignment ACKNOWLEDGED state", capture["run"])

    def test_review_observation_does_not_merge_or_release(self):
        data = self.load_yaml(WORKFLOW)
        self.assertIn("pull_request_review", data["on"])
        review_steps = str(data["jobs"]["review-observation-capture"])
        self.assertNotIn("gh pr merge", review_steps)
        self.assertNotIn("auto-merge", review_steps)


    def test_handoff_idempotency_distinguishes_reapplied_label(self):
        data = self.load_yaml(WORKFLOW)
        steps = data["jobs"]["handoff-request-capture"]["steps"]
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


    def test_direct_controlled_failure_dispatch_is_role_authorized(self):
        data = self.load_yaml(WORKFLOW)
        job = data["jobs"]["controlled-failure"]
        steps = job["steps"]
        checkout = next(step for step in steps if step.get("name") == "Checkout trusted controlled-test policy")
        self.assertEqual(checkout["with"]["ref"], "${{ github.event.repository.default_branch }}")
        auth = next(step for step in steps if step.get("name") == "Authorize direct controlled-failure dispatch actor")
        self.assertEqual(auth["env"]["AUTHOR"], "${{ github.actor }}")
        self.assertIn("controlled_test_authorization.py", auth["run"])
        failure = next(step for step in steps if step.get("name") == "Emit controlled failure for diagnostics E2E")
        self.assertEqual(failure["if"], "steps.authorize_direct_dispatch.outputs.authorized == 'true'")

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
        self.assertIn("W118 PR Review Checklist", workflows)
        self.assertIn("W300 Dashboard CI", workflows)
        self.assertIn("Work 70 Preview Host Tests", workflows)

    def test_ack_result_is_deduplicated_by_source_comment_id(self):
        data = self.load_yaml(WORKFLOW)
        run_script = next(step["run"] for step in data["jobs"]["ack-claim-capture"]["steps"] if "MARKER=" in step.get("run", ""))
        self.assertIn("w118-ack-result", run_script)
        self.assertIn("COMMENT_ID", run_script)

    def test_diagnostics_runtime_uses_workflow_sha_and_attempt_keys(self):
        data = self.load_yaml(DIAGNOSTICS)
        run_script = data["jobs"]["diagnostics"]["steps"][-1]["run"]
        self.assertIn('--workflow-id "$WF_ID"', run_script)
        self.assertIn('--sha "$SHA"', run_script)
        self.assertIn('--attempt "$RUN_ATTEMPT"', run_script)


    def test_pr_checklist_uses_safe_pull_request_target(self):
        data = self.load_yaml(PR_CHECKLIST)
        self.assertIn("pull_request_target", data["on"])
        self.assertEqual(data["permissions"], {"contents": "read", "issues": "write"})
        job = data["jobs"]["checklist"]
        self.assertIn("head.repo.full_name == github.repository", job["if"])
        self.assertFalse(any("checkout" in step.get("uses", "") for step in job["steps"]))
        run_script = next(step["run"] for step in job["steps"] if "MARKER=" in step.get("run", ""))
        self.assertIn("w118-pr-checklist", run_script)
        self.assertIn("HEAD_SHA", run_script)
        self.assertIn("gh issue comment", run_script)

    def test_no_github_ack_label_is_treated_as_assignment_state(self):
        data = self.load_yaml(WORKFLOW)
        steps = data["jobs"]["ack-claim-capture"]["steps"]
        run_script = next(step["run"] for step in steps if step.get("name") == "Capture ACK claim without authorizing Agent identity")
        self.assertNotIn("w118-acked", run_script)
        self.assertNotIn("gh issue edit", run_script)
        self.assertIn("assignment", run_script.lower())

    def test_event_jobs_upload_recorder_artifacts(self):
        data = self.load_yaml(WORKFLOW)
        for job_name in ("handoff-request-capture", "ack-claim-capture", "review-observation-capture"):
            steps = data["jobs"][job_name]["steps"]
            self.assertTrue(any(step.get("uses") == "actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02" for step in steps), job_name)
            self.assertTrue(any("event evidence" in step.get("name", "").lower() for step in steps), job_name)


    def test_pr_checklist_workflow_is_covered_by_orchestrator_path_filters(self):
        data = self.load_yaml(WORKFLOW)
        path = ".github/workflows/w118-pr-review-checklist.yml"
        self.assertIn(path, data["on"]["push"]["paths"])
        self.assertIn(path, data["on"]["pull_request"]["paths"])


    def test_ci_run_evidence_is_classified_as_ci_contract_not_runtime(self):
        data = self.load_yaml(WORKFLOW)
        steps = data["jobs"]["validate"]["steps"]
        run_script = next(step["run"] for step in steps if step.get("name") == "Write run evidence")
        self.assertIn('"evidence_type": "CI_CONTRACT"', run_script)
        self.assertNotIn('"evidence_type": "RUNTIME"', run_script)
        self.assertIn('"state": "RECORDED"', run_script)
        self.assertIn("CI evidence does not constitute independent review or Work acceptance", run_script)

    def test_ci_evidence_binds_source_and_tested_revision(self):
        data = self.load_yaml(WORKFLOW)
        steps = data["jobs"]["validate"]["steps"]
        run_script = next(step["run"] for step in steps if step.get("name") == "Write run evidence")
        for field in ('"repository"', '"run_url"', '"actor"', '"source_ref"', '"source_commit"', '"tested_ref"', '"tested_commit"', '"pull_request_number"'):
            self.assertIn(field, run_script)
        self.assertIn('"state": "RECORDED"', run_script)

    def test_diagnostics_planner_is_part_of_runtime(self):
        self.assertTrue(Path("scripts/w118/diagnostics.py").is_file())
        self.assertTrue(Path("tests/w118/test_diagnostics.py").is_file())

    def test_diagnostics_reuses_closed_issue_for_same_idempotency_key(self):
        data = self.load_yaml(DIAGNOSTICS)
        steps = data["jobs"]["diagnostics"]["steps"]
        run_script = next(step["run"] for step in steps if step.get("name") == "Create or update one diagnostic issue per workflow and commit")
        self.assertIn('--state all', run_script)
        self.assertIn('gh issue reopen', run_script)
        self.assertIn('--workflow-id "$WF_ID"', run_script)
        self.assertIn('--sha "$SHA"', run_script)

    def test_diagnostics_only_runs_for_failed_upstream_runs(self):
        data = self.load_yaml(DIAGNOSTICS)
        condition = data["jobs"]["diagnostics"]["if"]
        self.assertIn("failure", condition)


    def test_push_workflow_enforces_task_source_binding_and_records_outcome(self):
        data = self.load_yaml(WORKFLOW)
        self.assertIn("work/W*/task-W*-TASK-*", data["on"]["push"]["branches"])
        steps = data["jobs"]["validate"]["steps"]
        binding = next(step for step in steps if step.get("id") == "source_binding")
        self.assertEqual(binding["if"], "github.event_name == 'push'")
        self.assertIn("source_binding.py", binding["run"])
        self.assertIn("--event", binding["run"])
        self.assertIn("--repository", binding["run"])
        evidence = next(step for step in steps if step.get("name") == "Write run evidence")
        self.assertIn("SOURCE_BINDING_STATUS", evidence["env"])
        self.assertIn('"source_binding_status"', evidence["run"])
        upload = next(step for step in steps if step.get("name") == "Upload immutable run evidence")
        self.assertIn(".w118-evidence/run-evidence.json", upload["with"]["path"])
        self.assertIn(".w118-evidence/source-binding.json", upload["with"]["path"])
        self.assertEqual(upload["with"]["if-no-files-found"], "warn")

if __name__ == "__main__":
    unittest.main()
