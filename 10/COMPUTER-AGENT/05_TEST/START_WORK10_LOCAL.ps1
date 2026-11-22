[CmdletBinding()]
param(
    [string]$WorkRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$PythonPath = "",
    [switch]$InstallDependencies,
    [switch]$NoClipboard,
    [switch]$NoOpenBrowser
)

$ErrorActionPreference = "Stop"
$WorkRoot = (Resolve-Path -LiteralPath $WorkRoot).Path
$apiScript = Join-Path $WorkRoot "04_CODE\agent_api.py"
$dashboardDir = Join-Path $WorkRoot "08_DASHBOARD"
$requirements = Join-Path $WorkRoot "requirements.txt"
$evidenceDir = Join-Path $WorkRoot "06_EVIDENCE"
$sessionPath = Join-Path $evidenceDir "computer-agent-local-session.json"

function Test-LoopbackPortAvailable([int]$Port) {
    $listener = $null
    try {
        $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, $Port)
        $listener.Start()
        return $true
    } catch {
        return $false
    } finally {
        if ($listener) { $listener.Stop() }
    }
}

function Stop-StartedProcess($Process) {
    if ($null -eq $Process) { return }
    try {
        $current = Get-Process -Id $Process.Id -ErrorAction SilentlyContinue
        if ($current) {
            Stop-Process -Id $Process.Id -Force -ErrorAction SilentlyContinue
            Wait-Process -Id $Process.Id -Timeout 5 -ErrorAction SilentlyContinue
        }
    } catch { }
}

if (-not (Test-Path -LiteralPath $apiScript -PathType Leaf)) { throw "Missing Agent API: $apiScript" }
if (-not (Test-Path -LiteralPath $dashboardDir -PathType Container)) { throw "Missing Dashboard directory: $dashboardDir" }
if (Test-Path -LiteralPath $sessionPath) { throw "A Work 10 local session record already exists. Run STOP_WORK10_LOCAL.ps1 first." }

if ([string]::IsNullOrWhiteSpace($PythonPath)) {
    $pythonCommand = Get-Command python -ErrorAction Stop
    $PythonPath = $pythonCommand.Source
}
if (-not (Test-Path -LiteralPath $PythonPath -PathType Leaf)) { throw "Python executable not found: $PythonPath" }

$versionText = (& $PythonPath --version 2>&1 | Out-String).Trim()
if ($LASTEXITCODE -ne 0 -or $versionText -notmatch "Python 3\.12\.") {
    throw "Work 10 requires Python 3.12. Detected: $versionText"
}

if ($InstallDependencies) {
    & $PythonPath -m pip install -r $requirements
    if ($LASTEXITCODE -ne 0) { throw "pip install failed with exit code $LASTEXITCODE" }
    & $PythonPath -m playwright install chromium
    if ($LASTEXITCODE -ne 0) { throw "Playwright Chromium install failed with exit code $LASTEXITCODE" }
}

foreach ($port in @(8787, 3010)) {
    if (-not (Test-LoopbackPortAvailable -Port $port)) {
        throw "Loopback port $port is already in use. Work 10 will not terminate an unknown process."
    }
}

New-Item -ItemType Directory -Force -Path $evidenceDir | Out-Null
$randomBytes = New-Object byte[] 32
$rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
try { $rng.GetBytes($randomBytes) } finally { $rng.Dispose() }
$token = [Convert]::ToBase64String($randomBytes).TrimEnd("=").Replace("+", "-").Replace("/", "_")

# Local-only defaults. Writes and PowerShell remain disabled unless separately configured.
$env:COMPUTER_AGENT_API_TOKEN = $token
$env:COMPUTER_AGENT_ALLOWED_ORIGINS = "http://127.0.0.1:3010"
$env:COMPUTER_AGENT_WORK_ID = "10"
$env:COMPUTER_AGENT_PORT = "8787"
$env:COMPUTER_AGENT_HOST_ALLOWED_ROOTS = $WorkRoot
$env:COMPUTER_AGENT_HOST_WRITABLE_ROOTS = ""
$env:COMPUTER_AGENT_HOST_POWERSHELL_ROOTS = ""

$api = $null
$dashboard = $null
try {
    $apiOut = Join-Path $evidenceDir "computer-agent-api.stdout.log"
    $apiErr = Join-Path $evidenceDir "computer-agent-api.stderr.log"
    $dashboardOut = Join-Path $evidenceDir "computer-agent-dashboard.stdout.log"
    $dashboardErr = Join-Path $evidenceDir "computer-agent-dashboard.stderr.log"

    $apiArguments = '"' + $apiScript + '"'
    $api = Start-Process -FilePath $PythonPath -ArgumentList $apiArguments -WorkingDirectory $WorkRoot -PassThru -WindowStyle Hidden -RedirectStandardOutput $apiOut -RedirectStandardError $apiErr

    $dashboardArguments = '-m http.server 3010 --bind 127.0.0.1 --directory "' + $dashboardDir + '"'
    $dashboard = Start-Process -FilePath $PythonPath -ArgumentList $dashboardArguments -WorkingDirectory $WorkRoot -PassThru -WindowStyle Hidden -RedirectStandardOutput $dashboardOut -RedirectStandardError $dashboardErr

    $health = $null
    for ($attempt = 0; $attempt -lt 60; $attempt++) {
        if ($api.HasExited) { throw "Agent API exited early. Inspect $apiErr" }
        try {
            $health = Invoke-RestMethod -Uri "http://127.0.0.1:8787/health" -TimeoutSec 1
            if ([string]$health.work_id -eq "10" -and $health.status -eq "ok") { break }
        } catch { }
        Start-Sleep -Milliseconds 250
    }
    if (-not $health -or [string]$health.work_id -ne "10" -or $health.status -ne "ok") {
        throw "Agent API did not report healthy Work ID 10. Inspect $apiErr"
    }

    $dashboardResponse = Invoke-WebRequest -Uri "http://127.0.0.1:3010/" -UseBasicParsing -TimeoutSec 5
    if ($dashboardResponse.StatusCode -ne 200) { throw "Dashboard HTTP status was $($dashboardResponse.StatusCode)" }

    $apiProcess = Get-Process -Id $api.Id
    $dashboardProcess = Get-Process -Id $dashboard.Id
    $session = [ordered]@{
        work_id = "10"
        work_root = $WorkRoot
        api_pid = $api.Id
        api_started_utc = $apiProcess.StartTime.ToUniversalTime().ToString("o")
        dashboard_pid = $dashboard.Id
        dashboard_started_utc = $dashboardProcess.StartTime.ToUniversalTime().ToString("o")
        api_port = 8787
        dashboard_port = 3010
        started_utc = [DateTime]::UtcNow.ToString("o")
    }
    $session | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $sessionPath -Encoding UTF8

    if (-not $NoClipboard) { Set-Clipboard -Value $token }
    $token = $null
    [Array]::Clear($randomBytes, 0, $randomBytes.Length)
    $env:COMPUTER_AGENT_API_TOKEN = $null

    Write-Host "WORK 10 LOCAL AGENT STARTED" -ForegroundColor Green
    Write-Host "API:       http://127.0.0.1:8787"
    Write-Host "Dashboard: http://127.0.0.1:3010"
    Write-Host "Work ID:   10"
    if (-not $NoClipboard) { Write-Host "Bearer token copied to clipboard; paste into the Dashboard password field." }
    else { Write-Host "Clipboard disabled for non-interactive smoke test." }
    Write-Host "Writable roots: DISABLED"
    Write-Host "PowerShell roots: DISABLED"
    Write-Host "Port 3000 is untouched and remains reserved for the shared ROOM-HOP Dashboard."
    Write-Host "Session record: $sessionPath"
    Write-Host "Stop with: .\STOP_WORK10_LOCAL.ps1"
    if (-not $NoOpenBrowser) { Start-Process "http://127.0.0.1:3010" }
} catch {
    Stop-StartedProcess $dashboard
    Stop-StartedProcess $api
    $env:COMPUTER_AGENT_API_TOKEN = $null
    throw
}
