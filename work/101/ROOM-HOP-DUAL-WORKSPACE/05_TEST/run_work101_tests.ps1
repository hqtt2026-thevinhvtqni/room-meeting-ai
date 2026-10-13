# Work 101 local unit-test runner
# Read-only with respect to application/runtime data; writes one test-evidence file.
# Does not sync, push, merge, release, or call ROOM-HOP services.
$ErrorActionPreference = "Stop"

$ExpectedRepo = "hqtt2026-thevinhvtqni/room-meeting-ai"
$ExpectedBranch = "work/101-room-hop-dual-workspace"
$RepoRoot = (git rev-parse --show-toplevel 2>$null).Trim()
if (-not $RepoRoot) { throw "NOT_A_GIT_REPOSITORY" }
$CurrentRoot = (Get-Location).Path.TrimEnd("\")
if ($RepoRoot.TrimEnd("\") -ne $CurrentRoot) {
    throw "RUN_FROM_REPOSITORY_ROOT_ONLY"
}

$Origin = (git remote get-url origin 2>$null).Trim()
if (-not $Origin -or $Origin -notmatch [regex]::Escape("room-meeting-ai")) {
    throw "UNEXPECTED_ORIGIN_REPOSITORY"
}
$Branch = (git branch --show-current).Trim()
if ($Branch -ne $ExpectedBranch) {
    throw "WRONG_BRANCH_EXPECTED_$ExpectedBranch_GOT_$Branch"
}
if ($Branch -in @("main", "master")) { throw "PROTECTED_BRANCH_TEST_BLOCK" }

$Head = (git rev-parse HEAD).Trim()
$WorkRoot = Join-Path $RepoRoot "work/101/ROOM-HOP-DUAL-WORKSPACE"
$TestDir = Join-Path $WorkRoot "05_TEST"
$EvidenceDir = Join-Path $WorkRoot "06_EVIDENCE"
if (-not (Test-Path (Join-Path $WorkRoot "04_CODE/sync_policy.py"))) { throw "POLICY_MODULE_MISSING" }
if (-not (Test-Path (Join-Path $TestDir "test_sync_policy.py"))) { throw "TEST_MODULE_MISSING" }
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw "PYTHON_NOT_FOUND" }

$PythonVersion = (& python --version 2>&1 | Out-String).Trim()
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$EvidencePath = Join-Path $EvidenceDir "LOCAL_UNIT_TEST_$Timestamp.txt"
$OldNoBytecode = $env:PYTHONDONTWRITEBYTECODE
$env:PYTHONDONTWRITEBYTECODE = "1"
$TestOutput = @()
$ExitCode = 1
try {
    $TestOutput = @(& python -m unittest discover -s $TestDir -p "test_*.py" -v 2>&1)
    $ExitCode = $LASTEXITCODE
} finally {
    $env:PYTHONDONTWRITEBYTECODE = $OldNoBytecode
}
$Result = if ($ExitCode -eq 0) { "PASS" } else { "FAIL" }
$Evidence = @(
    "WORK_ID=101"
    "TIMESTAMP_LOCAL=$((Get-Date).ToString('o'))"
    "REPOSITORY=$ExpectedRepo"
    "ORIGIN=$Origin"
    "BRANCH=$Branch"
    "HEAD=$Head"
    "PYTHON=$PythonVersion"
    "COMMAND=python -m unittest discover -s 05_TEST -p test_*.py -v"
    "EXIT_CODE=$ExitCode"
    "RESULT=$Result"
    ""
    "----- TEST OUTPUT -----"
    ($TestOutput | ForEach-Object { "$_" })
) -join "`r`n"
New-Item -ItemType Directory -Path $EvidenceDir -Force | Out-Null
Set-Content -LiteralPath $EvidencePath -Value $Evidence -Encoding UTF8
Write-Host "RESULT=$Result"
Write-Host "EVIDENCE=$EvidencePath"
if ($ExitCode -ne 0) { exit $ExitCode }
