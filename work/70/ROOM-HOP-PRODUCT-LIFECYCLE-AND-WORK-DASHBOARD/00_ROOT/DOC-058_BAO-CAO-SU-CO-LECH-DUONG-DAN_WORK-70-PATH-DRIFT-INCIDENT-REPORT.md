# DOC-058 — WORK 70 PATH DRIFT INCIDENT REPORT
Date: 2026-10-31 (UTC+7)
Status: INCIDENT CONFIRMED / CORRECTIVE ACTIONS IN PROGRESS
Severity: P2 — structural integrity and sync-boundary defect

## Confirmed evidence
1. DOC-003 v1.1 defines Sandbox root as `ROOM-HOP-PRODUCT-LIFECYCLE-AND-WORK-DASHBOARD/`; `work/70/` is only a GitHub repository path prefix. It explicitly records a previous erroneous Sandbox write under `work/70/ROOM-HOP-PRODUCT-LIFECYCLE-AND-WORK-DASHBOARD/` and requires preservation until controlled cleanup.
2. DOC-035 entries 011–014 record Xu / AI-01 discovering and retaining that duplicate tree during governance/sync remediation. This identifies the logged operation as Xu / AI-01, not the underlying human/session that initiated it.
3. Sandbox root inventory showed `00_ROOT/NHAT_KY_THI_CONG.md` and two files under `05_BUILD/03_ARCHITECTURE/` outside the canonical Work root. The misplaced journal fragment records Ka / AI-02 created those two architecture drafts at those incorrect relative paths on 2026-10-31.
4. GitHub main commit `91e6fa972c865732480fc2513eed39d6595606db` contained only .gitkeep placeholders in Work 70/05_BUILD. The branch `work/70/05-build` at `97df13095eff29744a56fac5dbcecce83cda112f` contains actual Build records.
5. GitHub commit history shows the main 05_BUILD scaffold was created by nine commits between 2026-10-30 02:03:54Z and 02:04:16Z. Commit metadata identifies the connected GitHub account, not the actual operator.

## Root cause
Primary: Sandbox path contract was not enforced at the write boundary. Operators used paths relative to repository root or Work subtree, while the Sandbox API requires paths prefixed by the canonical Work root.
Contributors: no machine-enforced path preflight; task handoff omitted canonical path binding; no structural CI rule prevented branch-scope leakage; no mandatory post-write audit blocked duplicate trees.

## VS Code assessment
No available evidence attributes these writes to VS Code. Evidence points to explicit Sandbox/API writes using incorrect relative_path values. VS Code is NOT established as the cause. GitHub committer metadata alone cannot identify the person/AI at the keyboard.

## Impact
Duplicate/noncanonical paths could be mistaken for authoritative source. Two AI-02 drafts and one journal fragment were outside the canonical Sandbox Work root. Main held a redundant empty Build scaffold. No evidence from this incident shows canonical Work-root records or actual branch Build records were overwritten.

## Attribution
Confirmed from journal: Xu / AI-01 logged the earlier erroneous duplicate-path sync; Ka / AI-02 logged the direct out-of-root architecture writes. Underlying initiating user/session remains unproven.
Root-cause confidence: HIGH for path-contract enforcement failure; MEDIUM for complete chronology.

## Corrective actions and status
- Copy AI-02 drafts into canonical Sandbox 05_BUILD and GitHub work/70/05-build; exact readback required before removing misplaced copies.
- Append recovered journal fragment to canonical DOC-035; verify before removing misplaced fragment.
- Remove only empty 05_BUILD placeholder scaffold from GitHub main; retain actual Build files on work/70/05-build.
- Preserve nested duplicate Sandbox tree pending separate content comparison, backup and cleanup plan.
- Add Sandbox path preflight, root allow-list, branch allow-list, structural CI and post-write readback gate.

This report is an incident record, not a release or acceptance statement.
