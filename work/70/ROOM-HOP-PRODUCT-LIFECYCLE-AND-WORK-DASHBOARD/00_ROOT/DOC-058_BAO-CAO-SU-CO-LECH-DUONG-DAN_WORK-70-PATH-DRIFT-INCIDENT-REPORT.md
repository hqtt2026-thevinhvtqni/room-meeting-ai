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


## 9. Actual remediation result — 2026-10-31
- DONE: two Ka architecture drafts copied to canonical Sandbox Work-root 05_BUILD/03_ARCHITECTURE and exact-synced to GitHub branch work/70/05-build; exact content equality verified.
- DONE: misplaced journal fragment summarized in canonical DOC-035; canonical journal synced to GitHub main.
- DONE: three misplaced files removed from direct Sandbox root only after canonical copies/readback were confirmed.
- DONE: nine empty .gitkeep placeholders removed from GitHub main; current main tree contains no Work 70 05_BUILD path. Actual branch content remains on work/70/05-build.
- DONE: DOC-057, DOC-058 and updated DOC-055 synced/read back on GitHub main.
- BLOCKED: Sandbox 8030 exposes file deletion only; attempts to delete empty directories return IsADirectoryError. Empty direct Sandbox directories 00_ROOT and 05_BUILD/03_ARCHITECT (and parent 05_BUILD) remain. No directory-delete capability was found.
- PRESERVED: nested Sandbox duplicate work/70/ROOM-HOP-PRODUCT-LIFECYCLE-AND-WORK-DASHBOARD remains quarantined per DOC-003; it has not been deleted or treated as canonical.
- Overall: PARTIAL RESTORATION — canonical content restored and GitHub branch boundary corrected; Sandbox directory cleanup and nested duplicate reconciliation remain open.
