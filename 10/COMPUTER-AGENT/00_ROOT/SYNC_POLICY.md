# WORK 10 — SYNC POLICY
Version: 1.2
Date: 2026-11-16
Status: ACTIVE — reconciled with owner decision

## 1. Single source of truth
- Canonical repository: `hqtt2026-thevinhvtqni/room-meeting-ai`.
- Canonical branch: `work/10-computer-agent-mirror`.
- Protected baseline: `0cad66c59560450d68b06e76a659a6c44104e811`.
- Work 10 Sandbox (`work_id=10`, root `COMPUTER-AGENT/`) is the working, diagnostic, test-evidence and handoff mirror. It is not an independent canonical source.

## 2. Synchronization rules
1. Read and compare GitHub and Sandbox before every sync.
2. Classify each path as KEEP, UPDATE, CONFLICT, or SANDBOX-ONLY.
3. Never overwrite a divergent file without a file-level decision and verification.
4. Preserve the protected baseline and branch history; no force push or history rewrite.
5. Do not commit or push unverified code.
6. Locked contracts remain protected: `SAFETY_POLICY.md`, `ACTION_CONTRACT.md`, `WORKFLOW_CONTRACT.md`. Any proposed change requires explicit review and a compatibility decision.
7. Sandbox-only evidence and proposed patches remain evidence/proposals until independently tested and accepted.
8. A successful CI run proves only the tested commit and workflow contents; it does not prove that later Sandbox files are synchronized.

## 3. Current reconciliation snapshot (2026-11-16)
- GitHub branch exists and is canonical by owner decision.
- Branch comparison from protected baseline: 1 commit ahead, 0 behind; the additional commit changes the real-browser workflow only.
- CI run #5 for commit `7ea300b2d3d14552f9dfc31038b83b59d1dc2ab6` completed SUCCESS, including Offline contract tests and Real Chromium E2E steps.
- Sandbox and GitHub versions of root policies, README, locked contracts and sampled runtime/test files differ.
- Sandbox includes additional debug evidence and review findings not yet represented on the canonical branch.
- Therefore source-code synchronization is NOT COMPLETE. Do not describe Work 10 as fully synchronized or release-ready.

## 4. Completion gate
Synchronization may be marked COMPLETE only after:
- a full path inventory is reconciled;
- each divergent source/test file has an accepted disposition;
- accepted changes are applied without violating locked contracts;
- tests are run against the resulting exact commit;
- GitHub commit, CI run and Sandbox readback are recorded.

## 5. Authority
This version supersedes conflicting Sandbox statements that identify another repository or claim the canonical branch is absent. The owner-approved canonical target is the repository and branch stated in section 1.


## Read-only canonical recheck — 2026-11-17
- Compared protected baseline 0cad66c59560450d68b06e76a659a6c44104e811 to canonical branch work/10-computer-agent-mirror: ahead 1, behind 0, total commits 1; the only changed path is .github/workflows/work10-real-browser-e2e.yml (5 additions, 1 deletion).
- Canonical blobs fetched: agent_api.py 98db4b060a2727e57e2fa1cc9bebd37dc9e8a32b; agent_runtime.py e8153c180afc571efc5fe3e2b2afdee3afc88d13; browser_adapter.py a25849fef0e2259ace7a0693bd6146152e1471db; test_p0_p5.py af730f03f5116b5f82a8b44886c8543e4b3dde21.
- The latter three hashes match the inspected Candidate branch report. Canonical test_http.py and Work Manifest fetches returned 404.
- Conclusion: no Sandbox v1.3.0 remediation has been synchronized to canonical. G0 remains BLOCKED. Read-only audit only; no GitHub write occurred.


## Full path reconciliation addendum — 2026-11-22 06:32 (UTC+07:00)

- Inventory under `COMPUTER-AGENT/`: Sandbox 157 files; GitHub branch 64 files; shared paths 64; Sandbox-only files 93; GitHub-only files 0. Sandbox also retains one Sandbox-only `.github/` directory for its local workflow copy.
- All accepted source/test/architecture/config paths are shared and exact UTF-8 match in the independent comparison set; the three LOCKED contracts are exact-match.
- Current operational Dashboard, host API contract, host runbook, V8 validator, current CI evidence, Owner handover package, Work Manifest, BIÊN BẢN and NHẬT KÝ are represented on the canonical branch.
- The 93 Sandbox-only files are explicitly classified in `06_EVIDENCE/W10_FULL_PATH_INVENTORY_DISPOSITION_20261122.md`: 10 generated/transient files, 8 original/reference/preview files (including Sandbox-local duplicate workflow), 47 historical evidence/design files, 26 immutable AI debug handoff files, 1 superseded 2026-11-17 handover and 1 transcript archive.
- KEEP / SANDBOX-ONLY is intentional; do not bulk-copy caches, locks, runtime-generated outputs, sample previews, historical AI debug packages or superseded handover material into the canonical branch.
- No source/test/config divergence remains among accepted shared implementation files. The directory trees are reconciled by explicit dispositions, not by identical file counts.
- Evidence: `06_EVIDENCE/W10_FULL_PATH_INVENTORY_DISPOSITION_20261122.md`.
- Work 10 remains ACTIVE — NOT RELEASED. Physical Windows 10, production V8 trust configuration, Linux cgroup-v2, ROOM-HOP integration and Owner acceptance remain open.


## Inventory count correction — 2026-11-22 06:33 (UTC+07:00)

After adding the full inventory disposition document itself, the live snapshot is: Sandbox 158 files; GitHub 65 files; shared 65; Sandbox-only 93; GitHub-only 0; one Sandbox-only `.github/` directory. The prior 157/64/64 count was the immediately preceding snapshot before the inventory document was added. The 93 Sandbox-only file dispositions are unchanged and fully itemized in `06_EVIDENCE/W10_FULL_PATH_INVENTORY_DISPOSITION_20261122.md`.
