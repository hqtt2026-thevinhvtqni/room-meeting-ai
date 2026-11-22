[CmdletBinding()]
param(
    [string]$WorkRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$PythonPath = "",
    [switch]$InstallDependencies
)

$ErrorActionPreference = "Stop"
$WorkRoot = (Resolve-Path -LiteralPath $WorkRoot).Path
$evidenceDir = Join-Path $WorkRoot "06_EVIDENCE"
$sessionPath = Join-Path $evidenceDir "computer-agent-local-session.json"
$stamp = [DateTime]::UtcNow.ToString("yyyyMMdd_HHmmss")
$reportPath = Join-Path $evidenceDir "W10_OWNER_PC_ACCEPTANCE_$stamp.json"
$suiteLog = Join-Path $evidenceDir "W10_OWNER_PC_TESTS_$stamp.log"
$browserLog = Join-Path $evidenceDir "W10_OWNER_PC_BROWSER_E2E_$stamp.log"
$stopwatch = [System.Diagnostics.Stopwatch]::StartNew()

$report = [ordered]@{
    work_id = "10"
    result = "NOT_STARTED"
    release_gate = "OPEN"
    started_utc = [DateTime]::UtcNow.ToString("o")
    work_root = $WorkRoot
    os_caption = $null
    os_version = $null
    os_build = $null
    os_architecture = $null
    os_product_type = $null
    powershell_version = $PSVersionTable.PSVersion.ToString()
    python_version = $null
    playwright_version = $null
    chromium_executable = $null
    chromium_version = $null
    git_branch = $null
    git_commit = $null
    launcher_smoke = "NOT_RUN"
    powershell_ast = "NOT_RUN"
    suite_exit_code = $null
    browser_e2e_exit_code = $null
    suite_log = $suiteLog
    browser_e2e_log = $browserLog
    production_v8_key_configured = $false
    room_hop_integration = "NOT_VERIFIED"
    linux_cgroup_v2 = "NOT_APPLICABLE_TO_WINDOWS_HOST"
    failure_reason = $null
    source_hashes = @()
}

try {
    if ([string]::IsNullOrWhiteSpace($PythonPath)) {
        $pythonCommand = Get-Command python -ErrorAction Stop
        $PythonPath = $pythonCommand.Source
    }
    if (-not (Test-Path -LiteralPath $PythonPath -PathType Leaf)) {
        throw "Python executable not found: $PythonPath"
    }

    $os = Get-CimInstance Win32_OperatingSystem
    $report.os_caption = [string]$os.Caption
    $report.os_version = [string]$os.Version
    $report.os_build = [string]$os.BuildNumber
    $report.os_architecture = [string]$os.OSArchitecture
    $report.os_product_type = [int]$os.ProductType
    if ($os.ProductType -ne 1 -or $os.Caption -notmatch "Windows 10") {
        throw "Owner PC acceptance requires Windows 10 client. Detected: $($os.Caption) / ProductType=$($os.ProductType)"
    }

    $pythonText = (& $PythonPath --version 2>&1 | Out-String).Trim()
    if ($LASTEXITCODE -ne 0 -or $pythonText -notmatch "Python 3\.12\.") {
        throw "Work 10 requires Python 3.12. Detected: $pythonText"
    }
    $report.python_version = $pythonText

    if ($InstallDependencies) {
        & $PythonPath -m pip install -r (Join-Path $WorkRoot "requirements.txt")
        if ($LASTEXITCODE -ne 0) { throw "pip install failed with exit code $LASTEXITCODE" }
        & $PythonPath -m playwright install chromium
        if ($LASTEXITCODE -ne 0) { throw "Playwright Chromium install failed with exit code $LASTEXITCODE" }
    }

    $report.playwright_version = (& $PythonPath -c "import importlib.metadata as m; print(m.version('playwright'))" 2>&1 | Out-String).Trim()
    if ($LASTEXITCODE -ne 0) { throw "Playwright Python package is not installed." }
    $report.chromium_executable = (& $PythonPath -c "from playwright.sync_api import sync_playwright; p=sync_playwright().start(); print(p.chromium.executable_path); p.stop()" 2>&1 | Out-String).Trim()
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $report.chromium_executable -PathType Leaf)) {
        throw "Playwright Chromium executable is missing. Run with -InstallDependencies."
    }
    $report.chromium_version = (& $report.chromium_executable --version 2>&1 | Out-String).Trim()

    try { $report.git_branch = (& git -C $WorkRoot rev-parse --abbrev-ref HEAD 2>$null | Out-String).Trim() } catch { $report.git_branch = "UNKNOWN" }
    try { $report.git_commit = (& git -C $WorkRoot rev-parse HEAD 2>$null | Out-String).Trim() } catch { $report.git_commit = "UNKNOWN" }

    $envKey = $env:COMPUTER_AGENT_V8_HMAC_KEY
    $report.production_v8_key_configured = -not [string]::IsNullOrWhiteSpace($envKey)
    $envKey = $null

    $launcherFiles = @(
        (Join-Path $WorkRoot "05_TEST/START_WORK10_LOCAL.ps1"),
        (Join-Path $WorkRoot "05_TEST/STOP_WORK10_LOCAL.ps1")
    )
    foreach ($file in $launcherFiles) {
        $tokens = $null
        $errors = $null
        [System.Management.Automation.Language.Parser]::ParseFile((Resolve-Path $file), [ref]$tokens, [ref]$errors) | Out-Null
        if ($errors.Count -gt 0) { throw "PowerShell AST syntax validation failed: $file" }
    }
    $report.powershell_ast = "PASS"

    try {
        & (Join-Path $WorkRoot "05_TEST/START_WORK10_LOCAL.ps1") -WorkRoot $WorkRoot -PythonPath $PythonPath -NoClipboard -NoOpenBrowser
        $report.launcher_smoke = "PASS"
    } finally {
        if (Test-Path -LiteralPath $sessionPath) {
            & (Join-Path $WorkRoot "05_TEST/STOP_WORK10_LOCAL.ps1") -WorkRoot $WorkRoot
        }
    }

    Push-Location $WorkRoot
    try {
        & $PythonPath "05_TEST/run_all_tests.py" 2>&1 | Tee-Object -FilePath $suiteLog
        $report.suite_exit_code = $LASTEXITCODE
        if ($report.suite_exit_code -ne 0) { throw "run_all_tests.py failed with exit code $($report.suite_exit_code)" }

        & $PythonPath "05_TEST/e2e_real_browser.py" 2>&1 | Tee-Object -FilePath $browserLog
        $report.browser_e2e_exit_code = $LASTEXITCODE
        if ($report.browser_e2e_exit_code -ne 0) { throw "e2e_real_browser.py failed with exit code $($report.browser_e2e_exit_code)" }
    } finally {
        Pop-Location
    }

    $report.result = "HOST_TESTS_PASS"
    $report.release_gate = "OPEN — production key, integration and Owner acceptance remain separate"
} catch {
    $report.result = "FAIL"
    $report.failure_reason = $_.Exception.Message
} finally {
    $stopwatch.Stop()
    try {
        $hashFiles = @()
        $hashFiles += Get-ChildItem (Join-Path $WorkRoot "04_CODE") -Filter "*.py" -File
        $hashFiles += Get-ChildItem (Join-Path $WorkRoot "05_TEST") -File | Where-Object { $_.Extension -in @(".py", ".ps1") }
        $hashFiles += Get-ChildItem (Join-Path $WorkRoot "03_ARCHITECTURE") -Filter "*.md" -File
        $hashFiles += Get-ChildItem (Join-Path $WorkRoot "06_EVIDENCE") -File | Where-Object { $_.Name -match "(schema|policy).*\.json$" }
        $report.source_hashes = @(
            $hashFiles | Sort-Object FullName -Unique | ForEach-Object {
                [ordered]@{
                    path = $_.FullName.Substring($WorkRoot.Length + 1)
                    sha256 = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
                }
            }
        )
    } catch {
        $report.hash_collection_error = $_.Exception.Message
    }
    $report.finished_utc = [DateTime]::UtcNow.ToString("o")
    $report.duration_seconds = [Math]::Round($stopwatch.Elapsed.TotalSeconds, 2)
    New-Item -ItemType Directory -Force -Path $evidenceDir | Out-Null
    $report | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $reportPath -Encoding UTF8
    Write-Host "Work 10 acceptance report: $reportPath"
    Write-Host "Result: $($report.result); release gate: $($report.release_gate)"
}

if ($report.result -ne "HOST_TESTS_PASS") { exit 1 }
