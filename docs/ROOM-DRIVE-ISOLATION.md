# ROOM-DRIVE-ISOLATION — desktop.ini prevention and response

**Work:** 1111 — ROOM-HOP Technical Engineering & Debug Lab  
**Status:** IMPLEMENTED IN REPOSITORY BRANCH; PC/Google Drive isolation remains NOT VERIFIED  
**Scope:** Detect and prevent Git noise from desktop.ini; gather read-only PC evidence; do not silently delete or relocate files.

## 1. Known facts and limits

The 44 files removed from Git tracking by PR #79 contained an IconResource path naming GoogleDriveFS.exe. This is a strong Google Drive association, but it does not establish which process created each file, whether Drive backup or sync was enabled, or whether Drive currently touches the repository.

The W1111 journal records the user's statement that Google Drive for desktop had been turned off. This is user-reported state, not an independently observed process/service/configuration state. The repository at D:\ROOM-HOP-CLEAN\room-meeting-ai is not, by its path alone, proven to be outside every configured backup scope.

No connected tool in this session can inspect Windows processes, registry, DriveFS configuration, file-system event history, or the user's PC. Physical isolation and source attribution therefore cannot be certified from Sandbox or GitHub.

## 2. Protection layers

1. **Git hygiene:** .gitignore already contains desktop.ini. This prevents a new untracked file from being added accidentally; it does not untrack files already committed. PR #79 separately proposes removing the 44 tracked instances.
2. **Detection:** tools/room_drive_guard.py scans the working tree recursively (case-insensitive), excludes only .git, does not follow symlinks, correlates matches with the Git index and ignore matcher, and emits JSON or a concise alert. It never changes files.
3. **PC provenance:** tools/room_drive_isolation_pc_diagnostic.ps1 records GoogleDriveFS process/service observations, selected registry-key presence/value names, known Drive folder candidates, desktop.ini content and timestamps, and Git branch/status/ignore evidence. It does not inspect secret values or modify sync settings.
4. **Containment:** if PC evidence shows that the repository is inside an actively backed-up/synced folder, stop and design an approved isolation/backup plan before moving anything. Do not move a live checkout or change Mirror/Stream settings as an automated remediation.
5. **Recovery:** preserve the physical file and evidence first. Determine provenance and scope, take a backup, then make a separately reviewed decision about quarantine or deletion. No automatic remediation is provided.

## 3. Run the detector

From the repository root:

    python tools/room_drive_guard.py
    python tools/room_drive_guard.py --json
    python tools/room_drive_guard.py --watch --interval 30

Exit codes: 0 = no matching working-tree files and Git available; 2 = one or more desktop.ini files found; 3 = Git unavailable; 130 = watch interrupted. An alert is a repository-hygiene incident requiring review, not an application failure.

Suggested operation: run the read-only detector from Windows Task Scheduler at logon and periodically, with output redirected to a controlled log location outside any synced folder. This repository change does not install a task or create a background service.

## 4. Run the PC diagnostic

In Windows PowerShell:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\room_drive_isolation_pc_diagnostic.ps1 -RepositoryRoot 'D:\ROOM-HOP-CLEAN\room-meeting-ai'

The script writes a JSON evidence file under %TEMP% by default. Review:
- GoogleDriveProcesses and GoogleRelatedServices;
- GoogleDriveRegistryKeys and KnownDriveFoldersFound;
- DesktopIniFiles including timestamps and content;
- Git.RepositoryRootResolved, Branch, Head, Status, and IgnoreProbe.

An absent process at one instant does not prove Drive is uninstalled or backup is not configured. Registry-key presence does not prove active sync. Confirm the actual Google Drive for desktop UI's Computers / My Computer folder list and backup/sync status, and compare configured roots to the resolved repository path. Do not paste account secrets or tokens into the report.

## 5. Acceptance and incident handling

- **Clean scan:** zero physical matches; desktop.ini ignore probe matches .gitignore; no unexpected Git status. Record report timestamp and exact HEAD.
- **Detected file:** preserve it. Capture the JSON report and PC diagnostic. Check whether it is tracked, ignored, or untracked. Do not stage it, delete it, move it, or change attributes automatically.
- **Tracked file:** treat as a Git policy defect; inspect index/tree and use a reviewed PR to untrack it. The physical file may remain on disk.
- **Untracked but ignored file:** Git is protected against accidental addition, but Drive/Windows metadata generation is not prevented. Investigate the folder's actual backup/sync membership.
- **Repeat occurrence:** compare file creation/write times with process/service observations and Drive configuration; use Windows auditing/Procmon only if needed and approved. A process name in file content is not sufficient attribution.

## 6. Tests and limitations

tests/test_room_drive_guard.py covers root/nested case-insensitive detection, .git exclusion, symlink safety, and the no-mutation report contract. Run:

    python -m unittest discover -s tests -p test_room_drive_guard.py -v

Until the tests run in an evidenced CI job on the exact branch commit, this is not a CI PASS. It is not a PC integration test. The PowerShell diagnostic has not been executed on the target PC in this task.

## 7. Rollback

The detector and diagnostic are additive files. Roll back through a reviewed GitHub PR reverting the dedicated branch commit; do not reset or clean the user's checkout. The scripts themselves do not alter repository data, Windows settings, Google Drive settings, services, registry, or scheduled tasks.

## 8. Current disposition

- Git ignore rule: verified present on main.
- PR #79: open and not merged; it handles the 44 tracked Git entries only.
- New guard and diagnostic: proposed on a dedicated branch; require CI and remote readback.
- Google Drive creator/source: NOT PROVEN.
- Current Drive process/service/backup roots: NOT VERIFIED on PC.
- Physical repository isolation: NOT VERIFIED.
- End-to-end recurrence prevention and recovery on PC: BLOCKED pending PC evidence and actual configured backup/sync scope.
