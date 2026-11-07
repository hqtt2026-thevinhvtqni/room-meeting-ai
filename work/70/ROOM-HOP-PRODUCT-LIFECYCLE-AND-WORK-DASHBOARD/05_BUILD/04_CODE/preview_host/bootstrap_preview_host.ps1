param(
    [int]$Port = 8060,
    [switch]$SyncMain,
    [switch]$Start
)
$ErrorActionPreference = "Stop"
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $Here "..\..\..\..\..\..")).Path
$Server = Join-Path $Here "server.py"
$Tests = Join-Path $Here "test_server.py"
$Launcher = Join-Path $Here "preview_host.ps1"

function Invoke-GitChecked {
    param([string[]]$GitArgs)
    & git -C $RepoRoot @GitArgs
    if ($LASTEXITCODE -ne 0) { throw "Git command failed: git $($GitArgs -join ' ')" }
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw "Git is required." }
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw "Python 3 is required." }
$ActualRoot = (& git -C $RepoRoot rev-parse --show-toplevel 2>$null | Out-String).Trim()
if ($LASTEXITCODE -ne 0) { throw "The package is not inside a Git repository." }
if ([IO.Path]::GetFullPath($ActualRoot) -ne [IO.Path]::GetFullPath($RepoRoot)) {
    throw "Git root mismatch. Expected $RepoRoot, got $ActualRoot"
}
$Branch = (& git -C $RepoRoot branch --show-current 2>$null | Out-String).Trim()
if ($Branch -ne "main") { throw "Work 70 requires the shared main branch; current branch is '$Branch'. No branch switch performed." }
$Dirty = (& git -C $RepoRoot status --porcelain --untracked-files=all | Out-String).Trim()
if ($Dirty) { throw "Working tree is not clean. No pull or overwrite performed. Inspect git status first." }

if ($SyncMain) {
    Invoke-GitChecked @("fetch", "origin", "main")
    Invoke-GitChecked @("pull", "--ff-only", "origin", "main")
}
$Branch = (& git -C $RepoRoot branch --show-current 2>$null | Out-String).Trim()
if ($Branch -ne "main") { throw "Branch changed unexpectedly; stopping." }
$Dirty = (& git -C $RepoRoot status --porcelain --untracked-files=all | Out-String).Trim()
if ($Dirty) { throw "Working tree became dirty after sync; stopping before tests." }

& python --version
if ($LASTEXITCODE -ne 0) { throw "Python version check failed." }
& python -m py_compile $Server
if ($LASTEXITCODE -ne 0) { throw "Python compile failed." }
Push-Location $Here
try {
    & python -m unittest -v test_server.py
    if ($LASTEXITCODE -ne 0) { throw "Preview Host unit tests failed." }
}
finally {
    Pop-Location
}
Write-Output "LOCAL_TESTS=PASS"
if ($Start) {
    & $Launcher -Action Start -Port $Port
    if ($LASTEXITCODE -ne 0) { throw "Preview Host start command failed." }
    $health = Invoke-RestMethod -Uri "http://127.0.0.1:$Port/healthz" -TimeoutSec 5
    if ($health.status -ne "ok" -or $health.mode -ne "read_only") { throw "Health response did not match the read-only host contract." }
    Write-Output "HOST=RUNNING"
    Write-Output "HEALTH=PASS"
    Write-Output "EXECUTION=http://127.0.0.1:$Port/work/70/execution/"
    Write-Output "PRODUCT=http://127.0.0.1:$Port/work/70/product/"
}
else {
    Write-Output "HOST=NOT_STARTED (rerun with -Start after reviewing the test results)"
}
