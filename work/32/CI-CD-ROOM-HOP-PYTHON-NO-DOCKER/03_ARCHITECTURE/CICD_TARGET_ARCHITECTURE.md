# CI/CD Target Architecture — Python, No Docker

GitHub Actions is proposed as the CI coordinator using a hosted Python runner; Docker is not required. Initially enable validation only after approval; CD/deployment is a separate future phase.

Flow: scoped branch/PR → record source SHA and environment → run deterministic gates → retain logs/evidence → reviewer checks diff and risks → Vinh decides integration. No AI auto-merge, push or deploy.

Gates: G0 source/scope; G1 static syntax/compile; G2 unit tests; G3 safe integration tests; G4 dependency/security checks; G5 E2E when reproducible prerequisites exist; G6 evidence traceability; G7 human approval.

Status semantics: PASS = executed with evidence and passed; FAIL = executed and failed; BLOCKED = prerequisite/evidence unavailable; NOT RUN = not executed. Proposed repair loop: at most 3 attempts, then stop and request human review. No live-service mutation or deployment in this phase.

## Implemented CI status — 2026-11-04

The branch-scoped workflow is now operational and runs on every push to `work/32-ci-cd-python-ci-v2`, on pull requests targeting `main`, and on manual dispatch. Unit and Auto E2E are independent jobs, use Python 3.12, bounded timeouts, read-only `contents: read` permissions, exact triggering-SHA checkout (without submodule recursion), `pip check`, `compileall`, and JUnit artifacts with 14-day retention.

The GitHub Actions used by the workflow are pinned to the exact audited commit SHAs observed in the successful runner logs:
- `actions/setup-python`: `a26af69be951a213d495a4c3e4e4022e16d87065` (v5)
- `actions/upload-artifact`: `ea165f8d65b6e75b540449e92b4886f43607fa02` (v4)

Current successful exact-code evidence: run `41720062142`, commit `6ec0ca6aa9d8c32c912c9dfac140fab141c5b3aa`, 157 unit tests and 38 Auto E2E tests passed (one warning).

CD remains a separate, non-executable release gate. No deployment workflow is activated without a verified staging target, target owner, protected environment approval, credentials/host trust, health check, and tested rollback. A green CI workflow is not release approval.
