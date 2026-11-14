# KẾ HOẠCH THI CÔNG XU — WORK 32

- Chủ trì kế hoạch: Xu (AI-01)
- Reviewer: Ka (CSA)
- Owner/final authority: Vinh
- Cập nhật: 2026-10-21 Asia/Ho_Chi_Minh (UTC+07:00)
- Trạng thái: IMPLEMENTATION CANDIDATE / ACTIVATION GATED

| ID | Công việc | Phụ trách | Tiêu chí hoàn thành | Trạng thái |
|---|---|---|---|---|
| W32-01 | Read-only source survey | Ka | Branch, dependencies, pytest config, baseline and workflows evidenced | DONE (survey only) |
| W32-02 | Resolve test baseline | Qcoder + Ka review | Run exact branch SHA with pytest -q; reconcile 104 frozen baseline vs historical 35-test log | BLOCKED / NOT RUN here |
| W32-03 | Build minimal CI candidate | Qcoder | YAML syntax valid; Python runner; install requirements.txt; compile/import and pytest -q; logs/artifacts; least permissions; no Docker/CD/secrets | ASSIGNMENT PREPARED |
| W32-04 | Test workflow candidate | Qcoder | Validate YAML and commands; provide exact diff, source SHA, run logs or explain why not runnable in Sandbox | NOT RUN |
| W32-05 | Independent review | Ka (CSA) | Inspect changed paths, security permissions, trigger scope, test behavior and evidence | PENDING |
| W32-06 | Approval gate | Vinh | Explicit acceptance of baseline, patch and activation plan | NOT RUN |
| W32-07 | GitHub activation / PR | Vinh or authorized implementer | Only after W32-06; no auto-merge/deploy | NOT AUTHORIZED |

## Hard boundaries
- Python runner only; no Docker.
- Main branch and frozen regression baseline are read-only.
- Do not use stale pytest_output.txt as current PASS.
- No claim of CI PASS until a real run on the candidate SHA has a run URL, conclusion, logs and source SHA.
- Maximum three repair attempts; then stop and report BLOCKED.
