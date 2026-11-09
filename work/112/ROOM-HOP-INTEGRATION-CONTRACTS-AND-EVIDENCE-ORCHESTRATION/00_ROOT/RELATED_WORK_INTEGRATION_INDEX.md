# WORK 112 — RELATED WORK INTEGRATION & GITHUB SYNC INDEX
- Date: 2026-11-09
- Parent / system authority: Work 70
- Work 112 status: ACTIVE — DISCOVER / DEFINE
- Purpose: Record the Work set connected to W112 and the actual GitHub branch/path synchronization boundary.
- Rule: A branch existing is not proof of a canonical Work document path. No new branch, merge, main promotion or overwrite of unrelated files is implied.

## Related Work portfolio and GitHub disposition

| Work | Responsibility in unified machine | GitHub disposition as of 2026-11-09 |
|---|---|---|
| W70 | Central Control Plane / system authority | MAIN — DOC-095, DOC-035, DOC-055 updated and read back |
| W112 | Cross-Work integration contracts, dependency/event/evidence correlation and integrated verification | MAIN — Manifest, Charter, Journal and related-work index read back |
| W0000 | Work portfolio, governance, AI identity/authority registry | Branch work/0000-governance-baseline — DOC-018 and DOC-020 mirrored; DOC-003 journal updated |
| W32 | CI/CD and quality engine | Branch work/32-ci-runner-owned-fixture-v2 — integration journal entry; no main merge |
| W1111 | Technical engineering and debug lab | MAIN — canonical DOC-003 journal updated |
| W33 | Shared File & Evidence Hub | Branch work/33/ROOM-SHARED-FILE-EVIDENCE-HUB — WORK_LOG updated |
| W51 | Coder-Tester capability | Branch work/51-hqtt-coder-tester — SYNC_STATUS_WORK51 updated |
| W52 | AI communication/orchestration | Branch work/52-room-universal-ai-communication-orchestration exists in room-meeting-ai, but branch has no W52 Work-document subtree/path; Sandbox journal records an earlier failed sync attempt. NOT SYNCED |
| W14 | Execution-host / autonomous E2E ownership | PARTIAL SYNC — on release/work14-w14-release-20261010t053516, two Sandbox files under work/14/06_EVIDENCE match GitHub exactly: W14_RESTORATION_CONTINUATION_20261103_ADDENDUM2.md (SHA 2a7bfc96e44ae3cf14bc0808e23e423a3efc47fb) and W14_W70_COMPLIANCE_MAPPING_20261103.md (SHA b7ecfb0fcd10ef3b95c2a3cf359fc81be5f4ba16). Release branch is not assumed to be the ongoing development target. |
| W16 | Workflow engine | Sandbox manifest/charter establish Work identity and active specification-bootstrap, but do not pin GitHub repository/branch/path. work/31-room-hop-workflow-model is a separate Work 31 candidate; no W16 ownership evidence. NOT SYNCED |
| W21 | Agent skills | Manifest explicitly declares canonical repository hqtt2026-thevinhvtqni/room-meeting-ai, but says GitHub sync NOT VERIFIED and requires exact branch/path/commit pinning. No W21/skills branch found in the inspected branch inventory. Repository known; target unresolved; NOT SYNCED |
| W37 | Core :8000 evidence/investigation workspace | Detailed requirements and mirror policy define evidence-first analysis of the one live Core; not Core 2 and no write-back by default. No GitHub target. NOT SYNCED |
| W38 | Gateway :8040 investigation workspace | Manifest scopes it to surveying :8040; source/runtime audit NOT STARTED at initialization and PC/Main Source changes require Vinh approval. No GitHub target. NOT SYNCED |
| W39 | Build MCP :8030 investigation/evidence workspace | Minimal Manifest; journal records initialization only, no live endpoint/tools/list/Build test. Structure reference says not a replacement service. No GitHub target. NOT SYNCED |

## Integration boundaries
- W70 owns lifecycle, assignment, authority, gates, decisions and system dashboard.
- W112 owns only cross-Work contracts and integration verification; it does not replace component owners.
- W32 owns CI engine; W33 evidence storage; W52 AI communication; W16 workflow-engine domain; W14 execution host; W37 investigates/evidences the single live Core; W38 investigates Gateway :8040; W39 investigates Build MCP :8030; W0000 governance registry; W21 skills; W51 coder-tester. W37–W39 Sandbox workspaces are not proof of deployable component implementations.
- Component implementation remains with its owner. W112 coordinates interface contracts and cross-component tests.
- Statuses in this index are documentation/branch synchronization states only; they do not assert runtime integration or acceptance PASS.

## Canonical-source and branch controls discovered
- W0000 DOC-014 identifies hqtt-ai-platform/main as the original HQTT AI Platform source repository and requires preservation/read-only handling during intake. This does not automatically make it the source repo for every component Work.
- W0000 DOC-018 is a discovery/portfolio snapshot, not a per-Work GitHub path register. It flags W37/W38/W39 as NAME_ANOMALY_REVIEW because their registry names were generic folder labels; individual Work manifests still establish their identities.
- room-meeting-ai branch work/missing-work-roots-20261028 contains WORKS_SYNC_MATRIX.md. That matrix scopes its controlled common-root reconciliation to W15 and W98, requires branch/PR workflow (no direct main writes), and explicitly says the full mapping of all Works is incomplete.
- PR #30 for that branch is OPEN and UNMERGED; its body says draft. It is not a merged common-root baseline and does not authorize W112 to add unrelated Work roots there.
- The branch inventory across the nine installed repositories found no exact W16/W21/W37/W38/W39 branch name. This is a branch-name result, not proof that no file/source exists under another name.
- W16 branch candidates W31 and W32 are not accepted as W16. Generic core branches are not accepted as W37. W52 branch exists but does not contain a W52 Work-document subtree.
- No branch or root is to be created as a substitute for missing owner-approved canonical mapping.

## Verification rules
Every synchronized file must be fetched from the exact target branch after write. Existing divergent files are not overwritten without comparison. Missing branch/path is recorded NOT SYNCED, not fabricated as PASS. Use branch + PR for synchronization where the controlling repository contract requires it; do not write directly to main during a preservation/intake workflow.

## Search coverage limitation
- Installed repository inventory query returned nine repositories: hqtt-ai-platform, hqtt-android-app, room-meeting-ai, hqtt-Dashboard-note, bh-alert-5p, 004.ont-customer-protection-platform, PL.room-meeting-ai.dash, Computer-Agent, Work-89-Ximang.
- Branch inventory was read across all nine; the room-meeting-ai first branch page returned the currently visible branch set, including relevant W14/W16/W21/W37/W38/W39/W52 candidate checks.
- Code search remains limited to repositories with an available index and the indexed default-branch search; it is not an exhaustive search of all branches or all possible repositories.
- Next action is to derive owner-authorized exact repo + branch + path + base commit from each Work's own controlling record. Do not infer ownership from keywords or create substitute branches.


## Work 37–39 ownership/scope correction (2026-11-09)
- W37's detailed requirements define it as an evidence-first investigation workspace for the single live Core :8000. Its own rule says the live Core remains unique source of truth, Work 37 is not Core 2, and no write-back to live Core / MAIN_SOURCE / PC / GitHub by default. The initialization log records only Sandbox creation and folder-structure PASS; source correctness, live Core, APIs, tests, CI and GitHub sync were NOT TESTED.
- W37's structure reference points to the full read-only MAIN_SOURCE tree snapshot held in W99. It explicitly says that tree is not source-code content, not a byte-for-byte backup, and does not prove which files are loaded by Core.
- W38's Manifest scopes Work 38 to recording/surveying TCP :8040 Gateway behavior. At initialization it says no GitHub sync; its journal says source audit, live process/port, endpoints and runtime are not started/verified. It forbids PC/Main Source edits, service restart or config changes without Vinh approval.
- W39's Manifest is only a minimal identity/status record; its journal says Work creation is DONE but service survey is OPEN and no live :8030 endpoint, tools/list or Build tool was tested. Its structure reference points to W99's read-only MAIN_SOURCE tree and says Work 39 is an isolated evidence/analysis workspace, not a replacement service.
- Therefore the Work labels Core / Gateway / Build MCP describe investigation domains, not proof that W37/W38/W39 own or contain deployable component implementations. Do not describe them as canonical source-code owners or use their Sandbox folders as runtime mirrors.
- W99 snapshot is a MAIN_SOURCE directory-tree observation, not a GitHub repository/branch mapping. It cannot be used to infer a component Work's GitHub path.


## Exact path cross-check (2026-11-09)
- W21 Manifest says its Sandbox canonical source is represented by AI-SKILLS/ plus root-level Work records, while explicitly requiring exact GitHub mapping/commit pinning before synchronization. The nine installed repositories' default-root listings and room-meeting-ai/main/work listing did not show AI-SKILLS or Work16/21/37/38/39 common roots.
- W16 Charter requires an auditable branch/PR but does not name a repository, branch or path. The similarly named work/31-room-hop-workflow-model is not accepted as W16.
- room-meeting-ai/main/work currently lists only 0001, 103, 1111, 112, 28, 70, 75 and 76. This confirms the common-root absence on main at the time checked; it does not prove absence from every historical branch or external source.
- W52 branch root has general repository files and no W52 Work-document subtree. Its Sandbox journal records a failed synchronization attempt; do not equate branch existence with Work record synchronization.


## 2026-11-09 — W70 structure alignment and contract baseline
- Added W112 DOC-001 v1.0 at 03_ARCHITECT as the canonical cross-Work contract design baseline (DRAFT; not approved for runtime enforcement).
- W112 Manifest now adopts W70's canonical lifecycle directory set and 05_BUILD child layout.
- Legacy root scaffold paths remain preserved and mapped in Manifest; no files were moved/deleted. Physical migration is OPEN.
- Sandbox structure create acknowledgements cover the standard lifecycle folders and 05_BUILD child set. Directory readback and GitHub placeholder parity are tracked separately; no phase/gate status is implied.
- GitHub main exact content readback PASS for W112 Manifest, Integration Charter, Execution Journal (through event 017), and DOC-001. Latest commits: Manifest 5f3f072b7f75735f0b48de617dd4c94a31152b26; Charter ef93dac210c8501df1fb355a0a48edc0fece19d9; Journal 070b451ed17f237f245241d48d46c65185dde809; DOC-001 6b856f8f3a319cea79b6782e3f535ddc3f44b038.
- No component Work files, branches or services changed; no runtime, integration, QE or acceptance PASS claimed.
