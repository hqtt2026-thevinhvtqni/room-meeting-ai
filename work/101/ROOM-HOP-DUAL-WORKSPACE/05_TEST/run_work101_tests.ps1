# Work 101 local test runner (Unit + E2E Fixture + Full Suite)
# Read-only with respect to application/runtime data; writes test-evidence files.
# Does not sync, push, merge, release, or call ROOM-HOP services.
# Supports: unit tests, e2e fixture tests, full test suite, dashboard verification
$ErrorActionPreference = "Stop"

$ExpectedRepo = "hqtt2026-thevinhvtqni/room-meeting-ai"
$ExpectedBranch = "work/101-room-hop-dual-workspace"

# Test modes
param(
    [string]$Mode = "full",  # unit, e2e, full, dashboard
    [string]$OutputPrefix = ""
)

$RepoRootRaw = git rev-parse --show-toplevel 2>$null
if ($LASTEXITCODE -ne 0 -or -not $RepoRootRaw) { throw "NOT_A_GIT_REPOSITORY" }
$RepoRoot = $RepoRootRaw.Trim()
$CurrentRoot = (Get-Location).Path.TrimEnd("\")
if ($RepoRoot.TrimEnd("\") -ne $CurrentRoot) { throw "RUN_FROM_REPOSITORY_ROOT_ONLY" }

$OriginRaw = git remote get-url origin 2>$null
if ($LASTEXITCODE -ne 0 -or -not $OriginRaw) { throw "ORIGIN_NOT_CONFIGURED" }
$Origin = $OriginRaw.Trim()
if ($Origin -notmatch '(?i)(github\.com[:/])hqtt2026-thevinhvtqni/room-meeting-ai(?:\.git)?$') { throw "UNEXPECTED_ORIGIN_REPOSITORY" }

$Branch = (git branch --show-current).Trim()
if ($Branch -ne $ExpectedBranch) { throw "WRONG_BRANCH_EXPECTED_${ExpectedBranch}_GOT_${Branch}" }
if ($Branch -in @("main", "master")) { throw "PROTECTED_BRANCH_TEST_BLOCK" }

$Head = (git rev-parse HEAD).Trim()
$WorkRoot = Join-Path $RepoRoot "work/101/ROOM-HOP-DUAL-WORKSPACE"
$TestDir = Join-Path $WorkRoot "05_TEST"
$EvidenceDir = Join-Path $WorkRoot "06_EVIDENCE"
$DashboardDir = Join-Path $WorkRoot "08_DASHBOARD"
$PreviewDir = Join-Path $WorkRoot "09_DASHBOARD_PREVIEW"

if (-not (Test-Path (Join-Path $WorkRoot "04_CODE/sync_policy.py"))) { throw "POLICY_MODULE_MISSING" }
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw "PYTHON_NOT_FOUND" }

$PythonVersion = (& python --version 2>&1 | Out-String).Trim()
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$EvidencePath = Join-Path $EvidenceDir "LOCAL_${Mode}_TEST_$Timestamp.txt"
$OldNoBytecode = $env:PYTHONDONTWRITEBYTECODE
$env:PYTHONDONTWRITEBYTECODE = "1"

function Write-Evidence {
    param($Content, $Path)
    New-Item -ItemType Directory -Path $EvidenceDir -Force | Out-Null
    Set-Content -LiteralPath $Path -Value $Content -Encoding UTF8
}

function Run-Tests {
    param($TestPattern, $Description)
    $TestOutput = @()
    $ExitCode = 1
    try {
        $TestOutput = @(& python -m unittest discover -s $TestDir -p $TestPattern -v 2>&1)
        $ExitCode = $LASTEXITCODE
    } catch {
        $TestOutput = @($_.Exception.Message)
        $ExitCode = 1
    }
    return @{ ExitCode = $ExitCode; Output = $TestOutput }
}

# Main test execution
$Results = @()
$TotalTests = 0
$FailedTests = 0

switch ($Mode) {
    "unit" {
        Write-Host "Running UNIT tests only..."
        $result = Run-Tests -TestPattern "test_sync_policy.py" -Description "Unit Tests"
        $Results += $result
        $TotalTests += ($result.Output | Select-String "Ran.*test" | ForEach-Object { $_ -replace "[^0-9]", "" })
    }
    "e2e" {
        Write-Host "Running E2E FIXTURE tests only..."
        $result = Run-Tests -TestPattern "test_sync_e2e_fixture.py" -Description "E2E Fixture Tests"
        $Results += $result
        $TotalTests += ($result.Output | Select-String "Ran.*test" | ForEach-Object { $_ -replace "[^0-9]", "" })
    }
    "dashboard" {
        Write-Host "Running DASHBOARD verification..."
        # Verify dashboard files exist
        $DashboardChecks = @()
        $DashboardFiles = @(
            "$DashboardDir/index.html",
            "$DashboardDir/dashboard-contract.schema.json",
            "$DashboardDir/README.md",
            "$PreviewDir/index.html",
            "$PreviewDir/README.md"
        )
        
        foreach ($file in $DashboardFiles) {
            if (Test-Path $file) {
                $DashboardChecks += "PASS: $file exists"
            } else {
                $DashboardChecks += "FAIL: $file missing"
            }
        }
        
        # Verify schema JSON
        try {
            $schema = Get-Content -Path "$DashboardDir/dashboard-contract.schema.json" -Raw | ConvertFrom-Json
            $DashboardChecks += "PASS: dashboard-contract.schema.json is valid JSON"
        } catch {
            $DashboardChecks += "FAIL: dashboard-contract.schema.json is invalid JSON"
        }
        
        $Results += @{ ExitCode = 0; Output = $DashboardChecks }
    }
    "full" {
        Write-Host "Running FULL test suite..."
        
        # Run unit tests
        Write-Host "  - Running unit tests..."
        $result = Run-Tests -TestPattern "test_sync_policy.py" -Description "Unit Tests"
        $Results += $result
        
        # Run E2E fixture tests
        Write-Host "  - Running E2E fixture tests..."
        $result = Run-Tests -TestPattern "test_sync_e2e_fixture.py" -Description "E2E Fixture Tests"
        $Results += $result
        
        # Run dashboard verification
        Write-Host "  - Running dashboard verification..."
        $DashboardChecks = @()
        $DashboardFiles = @(
            "$DashboardDir/index.html",
            "$DashboardDir/dashboard-contract.schema.json",
            "$DashboardDir/README.md",
            "$PreviewDir/index.html",
            "$PreviewDir/README.md"
        )
        
        foreach ($file in $DashboardFiles) {
            if (Test-Path $file) {
                $DashboardChecks += "PASS: $file exists"
            } else {
                $DashboardChecks += "FAIL: $file missing"
            }
        }
        
        try {
            $schema = Get-Content -Path "$DashboardDir/dashboard-contract.schema.json" -Raw | ConvertFrom-Json
            $DashboardChecks += "PASS: dashboard-contract.schema.json is valid JSON"
        } catch {
            $DashboardChecks += "FAIL: dashboard-contract.schema.json is invalid JSON"
        }
        
        $Results += @{ ExitCode = 0; Output = $DashboardChecks }
    }
    default {
        Write-Host "Unknown mode: $Mode. Use: unit, e2e, full, dashboard"
        exit 1
    }
}

# Generate evidence
$EvidenceLines = @(
    "WORK_ID=101"
    "TIMESTAMP_LOCAL=$((Get-Date).ToString('o'))"
    "REPOSITORY=$ExpectedRepo"
    "ORIGIN=$Origin"
    "BRANCH=$Branch"
    "HEAD=$Head"
    "PYTHON=$PythonVersion"
    "MODE=$Mode"
    ""
    "----- TEST RESULTS -----"
)

foreach ($result in $Results) {
    $EvidenceLines += "--- $($result.Description) ---"
    $EvidenceLines += $result.Output
    $EvidenceLines += ""
    if ($result.ExitCode -ne 0) { $FailedTests++ }
}

$OverallStatus = if ($FailedTests -eq 0) { "PASS" } else { "FAIL" }
$EvidenceLines += "----- SUMMARY -----"
$EvidenceLines += "OVERALL_STATUS=$OverallStatus"
$EvidenceLines += "FAILED_SUITES=$FailedTests"

$Evidence = $EvidenceLines -join "`r`n"
Write-Evidence -Content $Evidence -Path $EvidencePath

Write-Host "RESULT=$OverallStatus"
Write-Host "EVIDENCE=$EvidencePath"

# Exit with error if any test failed
if ($FailedTests -gt 0) { exit 1 }
$env:PYTHONDONTWRITEBYTECODE = $OldNoBytecode
