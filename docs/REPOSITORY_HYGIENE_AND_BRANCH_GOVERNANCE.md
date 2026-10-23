# Repository Hygiene and Branch Governance

Status: remediation baseline opened 2026-10-23 (UTC+07:00). This document is a control plan, not a claim that all cleanup is complete.

## Findings confirmed from GitHub

- The main branch has root-level runtime/test artifacts and mixed Work folders. Some may be historical evidence; none should be deleted based on filename alone.
- `.gitignore` already contains `desktop.ini`; the remaining issue is that a tracked file remains tracked despite an ignore rule.
- `context/PROJECT_STATE.md` records mechanism/MockConnector verification but real API integration as pending.
- The Work 51 branch is divergent from main: this review found 27 commits on main not in Work 51 and 3 commits on Work 51 not in main. Do not merge blindly.
- The first full pytest CI run (commit `7e40351`) reported `214 passed, 16 failed`. Unbounded `mcp>=1.0.0` resolved MCP SDK 2.3.0, incompatible with the adapter's SDK 1.x `Server.list_tools()` decorator API. Pinning to `<2.0.0` resolved this API failure in subsequent CI.
- The same run exposed a Work 13 portability defect (`python.exe` hard-coded on Linux). The test now uses `sys.executable`; subsequent CI no longer reports that failure.
- F4 public schema tests failed because `add_paste_to_meeting.text` had no `maxLength`. Commit `2960367` declares `maxLength: 1048576`. This is a JSON Schema character limit; Core must continue enforcing the UTF-8 byte limit. A fresh run after this change showed `229 passed, 1 failed, 1 warning`; the remaining pytest failure was T8's missing `join_meeting` and `start_meeting` tools.
- Commit `a17989e` restores the two existing MCP tools and schemas required by `tests/test_message_v1.py::test_t8_existing_mcp_tools_no_regression`. Fresh CI is running/not yet verified at the time of this update.
- GitHub API tree/history inspection established that `room-meeting-ai` was a mode `160000` gitlink pointing to commit `eeb497e906b665e625a7ba7c50d93ada6ada9cfc` in this same repository. That target commit is the repository's own parentless `Initial commit clean`; its tree contains the project files but no `.gitmodules`. The gitlink first appears in parentless root commit `66b7ed52ed2e55581d0418b1ebd6b57a4bff5f38`. This was a self-referential, unconfigured gitlink, not a valid external submodule declaration. The referenced commit remains preserved in Git history. Removed only from the maintenance PR branch in commit `b5f937912ac35c223ccb003a779142e3c3a45536`; the new successful CI run no longer logs the missing-`.gitmodules` warning. `main` remains untouched.

## Mandatory cleanup sequence

1. Inventory each suspected artifact as source, test fixture, runtime output, historical evidence, or unknown. Link the owning Work and last meaningful commit.
2. Protect evidence: do not mass-delete logs, meeting records, test fixtures, or backup files until an owner and recovery path are established.
3. Branch hygiene: every Work branch must record its base commit and be compared with the target base before implementation and before PR. Report ahead/behind counts and changed paths.
4. PR gate: require Work ID, scope, changed-path summary, tests actually run, evidence links, known blockers, and independent review. Never claim CI PASS before observing a successful run.
5. CI gate: run pytest on pull requests and pushes. Treat failures as visible gates; do not weaken or skip tests merely to get green.
6. Documentation: keep the root README product-oriented. Internal governance and onboarding belong in dedicated docs; retain `AGENTS.md` as the governance entry point.
7. Work completion: update canonical project-state/Work records only after evidence is available. Keep mechanism PASS distinct from real integration PASS.

## Completion criteria

- [ ] Inventory of root-level candidates with disposition and owner.
- [ ] Work 51 branch divergence reviewed and safe synchronization plan recorded.
- [x] CI workflow has run and result is linked: run `39929032940` on commit `b5f937912ac35c223ccb003a779142e3c3a45536`, 230 passed, job success; the malformed-submodule warning is absent.
- [x] MCP SDK compatibility and Work 13 portability changes verified by CI.
- [x] F4 schema declaration and restored T8 tools verified by fresh CI: 230 passed, 0 failed.
- [x] Invalid submodule/gitlink metadata inspected; self-referential gitlink removed on maintenance branch only, referenced commit preserved.
- [ ] Real-API integration status remains accurate and changes only after a verified run.
- [ ] Cleanup PR reviewed; no unrelated Work or protected baseline changed.
