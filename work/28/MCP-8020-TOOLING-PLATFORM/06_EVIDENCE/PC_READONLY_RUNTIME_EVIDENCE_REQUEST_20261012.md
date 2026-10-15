# PC READ-ONLY RUNTIME EVIDENCE REQUEST — WORK 28
Date: 2026-10-12 (+07)
Purpose: identify the deployed source/runtime state without changing files, restarting services, or printing secrets.
Requested by: Ka (CSA)
Status: NEEDED TO UNBLOCK DEPLOYED-SOURCE ALIGNMENT; not an execution authorization.

Run in PowerShell on the PC hosting ROOM-HOP:

```powershell
$repo = 'D:\ROOM-HOP-CLEAN\room-meeting-ai'
"REPO_HEAD=" + (git -C $repo rev-parse HEAD)
"REPO_BRANCH=" + (git -C $repo branch --show-current)
git -C $repo status --short

$ports = 8000, 8020, 8031
Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue |
  Where-Object { $_.LocalPort -in $ports } |
  ForEach-Object {
    $proc = Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue
    [pscustomobject]@{
      Address = $_.LocalAddress
      Port = $_.LocalPort
      PID = $_.OwningProcess
      Process = $proc.ProcessName
      Executable = $proc.Path
    }
  } | Format-Table -AutoSize
```

## Handling
- This is read-only: it does not stop, restart, bind, or call any service.
- Do not paste environment variables, .env contents, API keys, authorization headers, or full process command lines.
- Return only HEAD, branch, short git status, and listener table.
- If a port has no listener, keep it absent from output; do not start a new host as a workaround.
- These facts will be compared to the GitHub source map before any live integration decision.
