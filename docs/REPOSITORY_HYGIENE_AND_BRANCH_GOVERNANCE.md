# Repository Hygiene and Branch Governance

Status: remediation baseline opened 2026-10-23 (UTC+07:00). This document is a control plan, not a claim that all cleanup is complete.

## Findings confirmed from GitHub

- The main branch has root-level runtime/test artifacts and mixed Work folders. Some may be historical evidence; none should be deleted based on filename alone.
- .gitignore already contains desktop.ini; do not report that rule as missing on main.
- context/PROJECT_STATE.md records mechanism/MockConnector verification but real API integration as pending.
- The Work 51 branch is divergent from main: this review found 27 commits on main not in Work 51 and 3 commits on Work 51 not in main. Do not merge blindly.

## Mandatory cleanup sequence

1. Inventory each suspected artifact as source, test fixture, runtime output, historical evidence, or unknown. Link the owning Work and last meaningful commit.
2. Protect evidence: do not mass-delete logs, meeting records, test fixtures, or backup files until an owner and recovery path are established.
3. Branch hygiene: every Work branch must record its base commit and be compared with the target base before implementation and before PR. Report ahead/behind counts and changed paths.
4. PR gate: require Work ID, scope, changed-path summary, tests actually run, evidence links, known blockers, and independent review. Never claim CI PASS before observing a successful run.
5. CI gate: run pytest on pull requests and pushes. Treat failures as visible gates; do not weaken or skip tests merely to get green.
6. Documentation: keep the root README product-oriented. Internal governance and onboarding belong in dedicated docs; retain AGENTS.md as the governance entry point.
7. Work completion: update canonical project-state/Work records only after evidence is available. Keep mechanism PASS distinct from real integration PASS.

## Completion criteria

- [ ] Inventory of root-level candidates with disposition and owner.
- [ ] Work 51 branch divergence reviewed and safe synchronization plan recorded.
- [ ] CI workflow has run and result is linked.
- [ ] Real-API integration status remains accurate and changes only after a verified run.
- [ ] Cleanup PR reviewed; no unrelated Work or protected baseline changed.
