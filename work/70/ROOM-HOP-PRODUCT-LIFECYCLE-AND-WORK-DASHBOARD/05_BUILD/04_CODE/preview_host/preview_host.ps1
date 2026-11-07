param(
    [ValidateSet("Start", "Stop", "Status")]
    [string]$Action = "Status",
    [int]$Port = 8060
)
$ErrorActionPreference = "Stop"
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $Here "..\..\..\..\..\..")).Path
$Server = Join-Path $Here "server.py"
$Registry = Join-Path $Here "preview_registry.json"
$StateDir = Join-Path $Here "runtime"
$PidFile = Join-Path $StateDir "preview-host.pid"
$LogFile = Join-Path $StateDir "preview-host.log"
$ErrFile = Join-Path $StateDir "preview-host.err.log"

function Get-PreviewProcess {
    if (-not (Test-Path $PidFile)) { return $null }
    $saved = Get-Content $PidFile -Raw
    $id = 0
    if (-not [int]::TryParse($saved.Trim(), [ref]$id)) { return $null }
    $entry = Get-CimInstance Win32_Process -Filter "ProcessId = $id" -ErrorAction SilentlyContinue
    if ($entry -and $entry.CommandLine -and $entry.CommandLine.Contains($Server)) {
        return Get-Process -Id $id -ErrorAction SilentlyContinue
    }
    return $null
}

switch ($Action) {
    "Start" {
        if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw "Python 3 not found in PATH." }
        if (-not (Test-Path $Server) -or -not (Test-Path $Registry)) { throw "Preview Host source or registry missing." }
        if (-not (Test-Path $StateDir)) { New-Item -ItemType Directory -Path $StateDir | Out-Null }
        if (Get-PreviewProcess) { Write-Output "ALREADY_RUNNING"; break }
        $listener = Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue
        if ($listener) { throw "Port $Port is already in use. Inspect the owning process before choosing another port." }
        $proc = Start-Process -FilePath "python" -ArgumentList @($Server, "--registry", $Registry, "--repo-root", $RepoRoot, "--host", "127.0.0.1", "--port", "$Port") -WorkingDirectory $RepoRoot -PassThru -WindowStyle Hidden -RedirectStandardOutput $LogFile -RedirectStandardError $ErrFile
        Set-Content -Path $PidFile -Value $proc.Id -NoNewline
        Start-Sleep -Milliseconds 700
        if ($proc.HasExited) { Remove-Item $PidFile -ErrorAction SilentlyContinue; throw "Preview Host exited. Inspect runtime logs." }
        Write-Output "STARTED pid=$($proc.Id) port=$Port bind=127.0.0.1"
    }
    "Stop" {
        $proc = Get-PreviewProcess
        if ($proc) { Stop-Process -Id $proc.Id -Force; Write-Output "STOPPED pid=$($proc.Id)" }
        else { Write-Output "NOT_RUNNING" }
        Remove-Item $PidFile -ErrorAction SilentlyContinue
    }
    "Status" {
        $proc = Get-PreviewProcess
        if ($proc) {
            Write-Output "RUNNING pid=$($proc.Id)"
            try {
                $r = Invoke-WebRequest -Uri "http://127.0.0.1:$Port/" -TimeoutSec 2 -UseBasicParsing
                Write-Output "HTTP=$($r.StatusCode)"
            } catch { Write-Output "HTTP_CHECK_FAILED=$($_.Exception.Message)" }
        } else { Write-Output "NOT_RUNNING" }
    }
}
