[CmdletBinding()]
param(
    [string]$WorkRoot = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = "Stop"
$WorkRoot = (Resolve-Path -LiteralPath $WorkRoot).Path
$sessionPath = Join-Path $WorkRoot "06_EVIDENCE\computer-agent-local-session.json"

if (-not (Test-Path -LiteralPath $sessionPath -PathType Leaf)) {
    Write-Host "No Work 10 local session record found."
    return
}

$session = Get-Content -LiteralPath $sessionPath -Raw | ConvertFrom-Json
if ([string]$session.work_id -ne "10" -or [string]$session.work_root -ne $WorkRoot) {
    throw "Session identity/root mismatch; refusing to stop any process."
}

try {
    $health = Invoke-RestMethod -Uri "http://127.0.0.1:8787/health" -TimeoutSec 2
    if ($health.execution_busy) {
        throw "Work 10 reports an active execution. Wait for completion before stopping the service."
    }
} catch {
    if ($_.Exception.Message -like "*active execution*") { throw }
    # API may already be down; process identity checks below still apply.
}

function Stop-VerifiedProcess([int]$ProcessId, [string]$ExpectedCommand, [string]$ExpectedStart) {
    $process = Get-Process -Id $ProcessId -ErrorAction SilentlyContinue
    if (-not $process) {
        Write-Host "Process $ProcessId is already stopped."
        return
    }
    $cim = Get-CimInstance Win32_Process -Filter "ProcessId=$ProcessId" -ErrorAction Stop
    if (-not $cim -or $cim.CommandLine -notmatch $ExpectedCommand) {
        throw "PID $ProcessId command line does not match the Work 10 session; refusing to stop it."
    }
    $actualStart = $process.StartTime.ToUniversalTime()
    $expected = [DateTime]::Parse($ExpectedStart).ToUniversalTime()
    if ([Math]::Abs(($actualStart - $expected).TotalSeconds) -gt 5) {
        throw "PID $ProcessId start time does not match the Work 10 session; refusing to stop it."
    }
    Stop-Process -Id $ProcessId -Force
    Wait-Process -Id $ProcessId -Timeout 10 -ErrorAction SilentlyContinue
    if (Get-Process -Id $ProcessId -ErrorAction SilentlyContinue) {
        throw "PID $ProcessId did not stop."
    }
    Write-Host "Stopped verified Work 10 process PID $ProcessId."
}

# Stop Dashboard first, then Agent API. API worker containment is owned by its Job Object.
Stop-VerifiedProcess -ProcessId ([int]$session.dashboard_pid) -ExpectedCommand "http\.server\s+3010" -ExpectedStart ([string]$session.dashboard_started_utc)
Stop-VerifiedProcess -ProcessId ([int]$session.api_pid) -ExpectedCommand "agent_api\.py" -ExpectedStart ([string]$session.api_started_utc)

Remove-Item -LiteralPath $sessionPath -Force
Write-Host "WORK 10 LOCAL AGENT STOPPED. Logs remain in 06_EVIDENCE."
