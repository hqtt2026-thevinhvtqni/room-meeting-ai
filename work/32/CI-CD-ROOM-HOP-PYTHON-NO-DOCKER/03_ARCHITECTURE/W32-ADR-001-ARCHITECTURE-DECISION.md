# W32-ADR-001 — CI/CD Architecture Decision

- Document Number: W32-ADR-001
- Priority: P1
- Author: Ka — CSA / architecture owner delegated by Vinh
- Date: 2026-11-03 08:43 UTC+07:00
- Status: DECIDED; implementation draft only; not released

## Decision

1. Adopt CI-first, Python 3.12, hosted GitHub Actions runner, least-privilege read-only repository permission.
2. Keep CD as a separate later phase requiring exact reviewed SHA, protected-environment approval, health checks and tested rollback.
3. Docker is not required for Work 32. Docker Compose is optional only if a later VPS runtime survey proves it useful; it must not change Core or Connector contracts.
4. Sandbox is the AI build zone. GitHub main is the source baseline. Do not enable two-way auto-sync.
5. No secrets in the CI pilot; no live-service mutation, auto-merge or auto-deploy.

## Evidence

- Repository: hqtt2026-thevinhvtqni/room-meeting-ai; default branch main.
- Main HEAD observed: 9e4002cbd93a6b92684b17623d79a1adda161d37.
- Legacy branch: work/32-ci-cd-room-hop-python-no-docker.
- Compare main...legacy branch: diverged; ahead 12, behind 530; merge base cc3100c835ad87ac9670a2ba38dc2c2dfae63755.
- The 12 commits ahead add Work 32 documentation only; no application code is included in that compare.
- Current pytest.ini SHA: b48b6676b85e30970e00a04a58fad3277be8c3e2.
- Current requirements.txt SHA: 59e0a4c07842154d82784eff85a9b412c6b33263; it declares pyyaml, pytest, python-dotenv and groq only.
- Current .github/workflows directory was not found in main.
- The frozen 104-test report is dated 2026-08-16 and is not proof of current main HEAD.
- tests/test_browser_agent_adapter_e2e.py calls localhost:8787 and an external site; tests/test_integration.py starts an MCP stdio session; exclude both from a generic hosted-runner pilot until isolated fixtures are proven.
- tests/test_mcp_server.py imports the MCP SDK, which is not declared in requirements.txt; do not silently add an unverified dependency.

## CI pilot

Candidate tests only (not yet executed against current HEAD): tests/test_agent_registry.py, tests/test_connectors.py, tests/test_context_loader.py, tests/test_discussion.py, tests/test_e2e.py and tests/test_meeting.py. Run compileall, install declared requirements, pip check, then pytest with JUnit output. This selection is a bounded pilot candidate, not a PASS claim.

## Branch and release controls

- Preserve the divergent legacy branch as historical evidence. Do not merge, rebase, force-push or cherry-pick its 12 commits.
- Create the next implementation branch from the then-current main only after rechecking its SHA. Proposed: work/32-ci-cd-python-ci-v2.
- Do not create branches, commit, push, merge, activate CI or deploy from this decision record; repository change-control rules remain in force.
- Workflow file remains a non-executable Sandbox draft until exact-SHA baseline and authorized promotion.

## Current disposition

Architecture decision: DECIDED. CI: DRAFT / NOT ACTIVATED. Current-main baseline: NOT RUN. CD/VPS: NOT RUN. Production release: NOT AUTHORIZED.


## Implementation addendum — 2026-11-04

- The CI-first architecture has been implemented on `work/32-ci-cd-python-ci-v2`.
- Vinh explicitly authorized branch-scoped CI implementation and push for Work 32 on 2026-11-04; this does not authorize main merge, production deployment, or secrets changes.
- Exact-SHA code validation: commit `fa625d1d7b99f5b326c0ff87641e6c3344d2dd73`, Actions run `41719444619` SUCCESS; unit 157 passed; Auto E2E 38 passed, 1 warning.
- GitHub Actions dependencies are pinned to audited commit SHAs. Workflow permissions remain `contents: read`.
- Current branch is still diverged from main (61 ahead / 31 behind at the last recorded comparison); no merge/rebase/cherry-pick has been performed.
- CD remains NOT RUN / BLOCKED pending an attested staging target and deployment safety controls. Production remains NOT AUTHORIZED.


## Final validation addendum — 2026-11-04

- Final branch SHA `6ec0ca6aa9d8c32c912c9dfac140fab141c5b3aa` passed Actions run #61 (`41720062142`).
- Unit gate: 157 passed; Auto E2E gate: 38 passed, 1 warning.
- The immutable action pins were exercised by run #58 (`41719864578`), also SUCCESS.
- Current branch remains 61 ahead / 31 behind main. Do not merge or rebase without independent review and a fresh exact-SHA reconciliation.
- CD / release remains BLOCKED / NOT RUN; production is not authorized.
