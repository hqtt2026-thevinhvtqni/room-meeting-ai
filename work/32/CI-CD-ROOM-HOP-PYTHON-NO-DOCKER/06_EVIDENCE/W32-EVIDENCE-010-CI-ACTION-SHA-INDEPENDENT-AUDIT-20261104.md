# W32-EVIDENCE-010 — CI Workflow Action-SHA Independent Audit (2026-11-04)

- Auditor: Vibe (GLM via Mistral), independent of Ka and Xu.
- Trigger: Xu's review order — "P0: Ka xác minh và sửa sai lệch SHA của setup-python trên workflow hardening; truy nguyên run #4."

## 1. Method
- Read exact file blobs via GitHub Contents API at branch head (commit e2af6001cbaf9df71ceb4a0d80d64073679bc139) — not the rendered HTML page.
- Enumerated every `uses:` line in both workflows.
- Cross-checked SHAs against upstream dependabot bump records outside this repository.

## 2. Raw occurrences

| File | Step | Pinned action | Version |
|---|---|---|---|
| ci-validation.yml | unit / Set up Python | actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065 | v5.6.0 ✅ |
| ci-validation.yml | tooling / Set up Python | actions/setup-python@a26af69… | v5.6.0 ✅ |
| ci-validation.yml | e2e / Set up Python | actions/setup-python@a26af69… | v5.6.0 ✅ |
| ci-validation.yml | product_artifact / Set up Python | actions/setup-python@a26af69… | v5.6.0 ✅ |
| ci.yml | unit, e2e, product_artifact / Set up Python | actions/setup-python@a26af69… | v5.6.0 ✅ |
| both files | all 7 "Retain … evidence" steps | actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02 | v4.6.2 ✅ |

No step pins upload-artifact's SHA on setup-python. The claim of "setup-python@ea165…" is a false positive caused by rendered-page line-wrapping during reading.

## 3. Upstream cross-check (independent of this repo)
- actions/setup-python a26af69be951a213d495a4c3e4e4022e16d87065 = v5.6.0 (Apache Arrow-go bump 5.5.0→5.6.0; hass-nabucasa dependabot #847).
- actions/upload-artifact ea165f8d65b6e75b540449e92b4886f43607fa02 = v4.6.2 (Apache Arrow bump 4.6.1→4.6.2; Grails dependabot #14079).

## 4. Conclusion on run #4
CI Hardening run #4 (SUCCESS) used correctly pinned actions; no correction to workflows is required. Ka is NOT blocked by P0.

## 5. Open item (P1, needs Xu/Vinh approval)
Two workflows (ci.yml Pilot, ci-validation.yml Hardening) both run on push to work/32-ci-cd-python-ci-v2 — duplicate cost and verified drift (Hardening includes test_meeting.py, constraints-ci.txt, tooling job; Pilot does not). Proposal: keep ci-validation.yml as sole standard; remove ci.yml push trigger (keep workflow_dispatch) or delete ci.yml. No change executed without approval.
