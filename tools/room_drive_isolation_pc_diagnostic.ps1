[CmdletBinding()]
param(
    [string]$RepositoryRoot = "D:\ROOM-HOP-CLEAN\room-meeting-ai",
    [string]$OutputPath = (Join-Path $env:TEMP ("room-drive-isolation-" + (Get-Date -Format "yyyyMMdd-HHmmss") + ".json"))
)
$ErrorActionPreference = "Continue"
$resolvedRoot = $null
if (Test-Path -LiteralPath $RepositoryRoot -PathType Container) {
    $resolvedRoot = (Resolve-Path -LiteralPath $RepositoryRoot).Path
}
$driveProcesses = @()
try {
    $driveProcesses = @(Get-CimInstance Win32_Process -Filter "Name='GoogleDriveFS.exe'" |
        Select-Object ProcessId, ExecutablePath, CreationDate)
} catch {
    try { $driveProcesses = @(Get-Process -Name GoogleDriveFS -ErrorAction SilentlyContinue |
        Select-Object Id, Path, StartTime) } catch {}
}
$driveServices = @()
try {
    $driveServices = @(Get-Service -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -match 'Google|Drive' -or $_.DisplayName -match 'Google Drive' } |
        Select-Object Name, DisplayName, Status, StartType)
} catch {}
$registry = @()
foreach ($key in @("HKCU:\Software\Google\DriveFS", "HKCU:\Software\Google\Drive")) {
    if (Test-Path $key) {
        try {
            $names = (Get-ItemProperty -Path $key).PSObject.Properties |
                Where-Object { $_.Name -notmatch '^PS' } | Select-Object -ExpandProperty Name
            $registry += [pscustomobject]@{ Key=$key; Present=$true; ValueNames=@($names) }
        } catch { $registry += [pscustomobject]@{ Key=$key; Present=$true; ReadError=$_.Exception.Message } }
    } else { $registry += [pscustomobject]@{ Key=$key; Present=$false; ValueNames=@() } }
}
$knownRoots = @()
foreach ($candidate in @((Join-Path $env:USERPROFILE "Google Drive"),
                         (Join-Path $env:USERPROFILE "My Drive"), "G:\My Drive", "H:\My Drive")) {
    if (Test-Path -LiteralPath $candidate -PathType Container) {
        $knownRoots += (Resolve-Path -LiteralPath $candidate).Path
    }
}
$desktopFiles = @()
if ($resolvedRoot) {
    try {
        $desktopFiles = @(Get-ChildItem -LiteralPath $resolvedRoot -Force -File -Recurse -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -ieq "desktop.ini" -and $_.FullName -notmatch '[\\/]\.git[\\/]' } |
            ForEach-Object {
                $content = $null
                try { $content = Get-Content -LiteralPath $_.FullName -Raw -ErrorAction Stop } catch {}
                [pscustomobject]@{ Path=$_.FullName; Length=$_.Length;
                    CreationTimeUtc=$_.CreationTimeUtc.ToString("o");
                    LastWriteTimeUtc=$_.LastWriteTimeUtc.ToString("o");
                    Attributes=[string]$_.Attributes; Content=$content }
            })
    } catch {}
}
$git = [ordered]@{ IsWorktree=$false; Branch=$null; Head=$null; Status=@(); IgnoreProbe=@() }
if ($resolvedRoot) {
    $inside = & git -C $resolvedRoot rev-parse --is-inside-work-tree 2>$null
    $git.IsWorktree = ($LASTEXITCODE -eq 0 -and $inside -eq "true")
    if ($git.IsWorktree) {
        $git.Branch = (& git -C $resolvedRoot branch --show-current 2>$null | Out-String).Trim()
        $git.Head = (& git -C $resolvedRoot rev-parse HEAD 2>$null | Out-String).Trim()
        $git.Status = @(& git -C $resolvedRoot status --porcelain=v1 --untracked-files=all 2>$null)
        $git.IgnoreProbe = @(& git -C $resolvedRoot check-ignore -v --no-index -- desktop.ini 2>$null)
    }
}
$report = [ordered]@{
    Schema="room-drive-isolation-pc-diagnostic/v1"
    GeneratedAtUtc=(Get-Date).ToUniversalTime().ToString("o")
    ComputerName=$env:COMPUTERNAME
    RepositoryRootRequested=$RepositoryRoot
    RepositoryRootResolved=$resolvedRoot
    GoogleDriveProcesses=$driveProcesses
    GoogleRelatedServices=$driveServices
    GoogleDriveRegistryKeys=$registry
    KnownDriveFoldersFound=$knownRoots
    DesktopIniFiles=$desktopFiles
    Git=$git
    Safety="Read-only inspection. No file, repository, service, registry, sync or backup configuration was changed."
    Interpretation="An IconResource string naming GoogleDriveFS.exe is a provenance clue, not proof the process created the file. Correlate timestamps, process/service state and actual Drive backup/sync configuration."
}
$json = $report | ConvertTo-Json -Depth 8
$json | Set-Content -LiteralPath $OutputPath -Encoding UTF8
Write-Output $json
Write-Host "Evidence saved to: $OutputPath"
