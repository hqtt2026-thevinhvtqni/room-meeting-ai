# W1111 PC READ-ONLY ATTESTATION — CONSOLIDATED 2026-11-10

- Prepared by: Co — Coder / W1111
- Date: 2026-11-10 (UTC+7)
- Target repository: `D:\\ROOM-HOP-CLEAN\\room-meeting-ai`
- Purpose: collect the minimum current evidence needed to close the PC/runtime identity gap.
- Safety: READ ONLY. This script does not start/stop/restart services, call `/execute`, read secret values, write project files, or change Git state.

## Run instructions

Open **64-bit PowerShell** in VS Code terminal (or PowerShell) at any directory. Paste the complete script below. Send Co the complete output. Do not redact PID, SHA, paths, branch, or commit; secret-like variable values are never printed.

```powershell
$ErrorActionPreference = 'Continue'
$repoRoot = 'D:\\ROOM-HOP-CLEAN\\room-meeting-ai'
Set-Location $repoRoot

'=== 1. LISTENERS :8000 / :8031 ==='
$listenerRows = @(Get-NetTCPConnection -State Listen -LocalPort 8000,8031 -ErrorAction SilentlyContinue |
    Sort-Object LocalPort,OwningProcess -Unique)
if (-not $listenerRows) { 'NO LISTENER FOUND on 8000/8031' }
foreach ($row in $listenerRows) {
    $proc = Get-CimInstance Win32_Process -Filter "ProcessId = $($row.OwningProcess)" -ErrorAction SilentlyContinue
    $safeCommandLine = [string]$proc.CommandLine
$safeCommandLine = [regex]::Replace($safeCommandLine, '(?i)((?:--)?(?:token|secret|password|api[-_]?key|credential)(?:=|\s+))(?:"[^"]*"|\S+)', '$1<REDACTED>')
    [pscustomobject]@{
        LocalAddress = $row.LocalAddress
        LocalPort = $row.LocalPort
        PID = $row.OwningProcess
        ParentPID = $proc.ParentProcessId
        ExecutablePath = $proc.ExecutablePath
        CommandLine = $safeCommandLine
        CreationDate = $proc.CreationDate
    } | Format-List
}

'=== 2. HISTORICAL W13 PIDS (14280 / 16484) ==='
foreach ($targetPid in @(14280,16484)) {
    $proc = Get-CimInstance Win32_Process -Filter "ProcessId = $targetPid" -ErrorAction SilentlyContinue
    if ($proc) {
        $safeCommandLine = [string]$proc.CommandLine
$safeCommandLine = [regex]::Replace($safeCommandLine, '(?i)((?:--)?(?:token|secret|password|api[-_]?key|credential)(?:=|\s+))(?:"[^"]*"|\S+)', '$1<REDACTED>')
        [pscustomobject]@{
            PID=$proc.ProcessId
            ParentPID=$proc.ParentProcessId
            ExecutablePath=$proc.ExecutablePath
            CommandLine=$safeCommandLine
            CreationDate=$proc.CreationDate
        } | Format-List
    } else {
        [pscustomobject]@{PID=$targetPid;Present=$false} | Format-List
    }
}

'=== 3. SOURCE SHA256 (CORE + W13) ==='
$relativeFiles = @(
 'room_hop_mcp\core_http_main.py',
 'room_hop_mcp\adapter\http_server.py',
 '13\EXECUTION-HOST-INFRASTRUCTURE\04_CODE\execution_host\server.py',
 '13\EXECUTION-HOST-INFRASTRUCTURE\04_CODE\execution_host\host.py',
 '13\EXECUTION-HOST-INFRASTRUCTURE\04_CODE\execution_host\w12_adapter.py',
 '13\EXECUTION-HOST-INFRASTRUCTURE\04_CODE\execution_host\wee_bridge.py'
)
foreach ($relative in $relativeFiles) {
    $full = Join-Path $repoRoot $relative
    if (Test-Path -LiteralPath $full -PathType Leaf) {
        Get-FileHash -Algorithm SHA256 -LiteralPath $full |
            Select-Object @{n='RelativePath';e={$relative}},Hash,Path | Format-List
    } else {
        [pscustomobject]@{RelativePath=$relative;Hash='MISSING';Path=$full} | Format-List
    }
}

'=== 4. PYTHON MODULE RESOLUTION (NO TARGET MODULE IMPORT) ==='
$python = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $python) { 'PYTHON_NOT_FOUND' }
else {
    & $python -c "import importlib.util, importlib.machinery as m; names=['room_hop_mcp','execution_host']; print('python_executable=',__import__('sys').executable); print('python_version=',__import__('sys').version); [(lambda s,n: print(n, 'origin=', getattr(s,'origin',None), 'locations=', list(s.submodule_search_locations or []) if s else None))(importlib.util.find_spec(n),n) for n in names]; s=importlib.util.find_spec('room_hop_mcp'); print('room_hop_mcp.core_http_main=', m.PathFinder.find_spec('core_http_main', list(s.submodule_search_locations)) if s and s.submodule_search_locations else None); e=importlib.util.find_spec('execution_host'); print('execution_host.server=', m.PathFinder.find_spec('server', list(e.submodule_search_locations)) if e and e.submodule_search_locations else None)"
}

'=== 5. GIT REVISION / DIRTY STATE ==='
git -C $repoRoot branch --show-current
git -C $repoRoot rev-parse HEAD
git -C $repoRoot status --short

'=== 6. SECRET CONFIG PRESENCE ONLY ==='
$secretNames = @(Get-ChildItem Env: | Where-Object { $_.Name -match '(?i)(TOKEN|SECRET|CREDENTIAL|AUTH|API.?KEY|PRIVATE.?KEY)' })
[pscustomobject]@{
    SecretLikeEnvironmentVariablePresent = ($secretNames.Count -gt 0)
    SecretLikeEnvironmentVariableCount = $secretNames.Count
} | Format-List
```

## Interpretation rules

- A listener PID is not proof of which Python module/source was imported.
- The module-resolution section reports what the current PowerShell Python interpreter would resolve from the repository root; it is not proof of the running process's import path. Compare it with the process command line, working directory and source hashes.
- Missing files, no listeners, or missing environment variables are valid results; do not repair anything during this collection.
- Do not paste secret values. This script reports only presence and count.
- For current working-directory evidence of the historical W13 PIDs, also run the existing `PC_READONLY_ATTESTATION_PACK_20261109.md` PEB read-only section. If a PID differs from 14280/16484, report the listener PID and Co will prepare a matching read-only PEB query.

## Return to Co

Paste the full output sections 1–6. Co will reconcile:
1. Core :8000 listener → process → entrypoint/module.
2. Host :8031 listener → process → W13 source hashes.
3. PC branch/HEAD/dirty tree versus GitHub branch/HEAD.
4. Environment configuration presence (without exposing values).

No restart, deployment, credential creation, or live execution is authorized by this read-only pack.
