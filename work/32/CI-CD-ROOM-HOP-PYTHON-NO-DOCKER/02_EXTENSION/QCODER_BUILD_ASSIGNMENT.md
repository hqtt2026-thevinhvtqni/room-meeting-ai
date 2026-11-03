# QCODER BUILD ASSIGNMENT — WORK 32
## W32-03: Minimal Python CI Candidate (No Docker)

- Requester / final authority: Vinh
- Assignment prepared by: Ka — CSA / Independent Reviewer
- Date/time: 2026-10-21, Asia/Ho_Chi_Minh (UTC+07:00)
- Target repo: hqtt2026-thevinhvtqni/room-meeting-ai
- Target branch: work/32-ci-cd-room-hop-python-no-docker
- Sandbox Work ID: 32
- Priority: P0 for Work 32 implementation candidate
- Status: ASSIGNMENT PREPARED; delivery not yet received

## Mission
Build a minimal, safe GitHub Actions CI candidate for the existing Python ROOM HOP project. Do not Dockerize the project and do not add deployment.

## Required deliverables
1. Candidate workflow YAML under .github/workflows/ (provide exact diff in Work 32 Sandbox first).
2. A short rationale for event triggers, Python version, permissions, timeout, caching, artifacts and security.
3. A validation report covering YAML syntax, compile/import validation, pytest -q, dependency install, and exact source SHA.
4. Separate PASS / FAIL / BLOCKED / NOT RUN per gate; include logs and run URLs when an actual GitHub run exists.
5. Update the single official Work 32 NHAT_KY_HOP_THI_CONG.md; do not create a competing journal.

## Constraints
- Python hosted runner; no Docker.
- No deployment, release, publish, auto-merge, secret access, external service mutation or live PC change.
- No modifications to protected Core files or frozen baseline files.
- Do not trust pytest_output.txt as a current run. It is historical and reports 35 tests, whereas the frozen baseline document reports 104; run pytest -q against the exact target SHA and explain discrepancies.
- Use requirements.txt and existing pytest.ini; do not invent a new dependency manifest unless evidence requires it.
- Prefer least-privilege permissions (contents: read), bounded timeout, and no secrets.
- Trigger scope should be conservative and documented. Do not activate the workflow in GitHub or commit/push/merge without Vinh's explicit approval after Ka review.
- Keep candidate files in Sandbox and provide a patch/diff for independent review first.
- Maximum three repair attempts; then stop and report BLOCKED.

## Acceptance
PASS only when candidate YAML is valid, commands are grounded in repository files, test results are fresh and traceable to exact SHA, and no forbidden side effects are introduced. Merely creating the workflow file is not a PASS.
