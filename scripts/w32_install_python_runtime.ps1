$ErrorActionPreference = "Stop"

# Runner-local portable CPython installation. This does not execute setup.ps1
# and does not change machine or user execution policy.
$pythonVersion = "3.12.10"
$releaseTag = "3.12.10-14343898437"
$assetName = "python-3.12.10-win32-x64.zip"
$assetUrl = "https://github.com/actions/python-versions/releases/download/$releaseTag/$assetName"

if ([string]::IsNullOrWhiteSpace($env:RUNNER_TOOL_CACHE)) {
    throw "BLOCKED: RUNNER_TOOL_CACHE is unavailable"
}

$pythonRoot = Join-Path $env:RUNNER_TOOL_CACHE "Python\$pythonVersion\x64"
$pythonExe = Join-Path $pythonRoot "python.exe"

function Test-Work32Python([string]$Path) {
    try {
        if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { return $false }
        $versionText = & $Path --version 2>&1
        return ($LASTEXITCODE -eq 0 -and "$versionText" -eq "Python $pythonVersion")
    } catch {
        return $false
    }
}

if (-not (Test-Work32Python $pythonExe)) {
    $downloadRoot = Join-Path $env:RUNNER_TEMP "w32-portable-python-$pythonVersion"
    if (Test-Path -LiteralPath $downloadRoot) {
        Remove-Item -LiteralPath $downloadRoot -Recurse -Force
    }
    New-Item -ItemType Directory -Force $downloadRoot | Out-Null
    $archive = Join-Path $downloadRoot $assetName
    $extractRoot = Join-Path $downloadRoot "extracted"
    New-Item -ItemType Directory -Force $extractRoot | Out-Null

    Invoke-WebRequest -Uri $assetUrl -OutFile $archive -UseBasicParsing
    Expand-Archive -LiteralPath $archive -DestinationPath $extractRoot -Force

    $pythonCandidate = Get-ChildItem -LiteralPath $extractRoot -Filter "python.exe" -File -Recurse |
        Select-Object -First 1
    if (-not $pythonCandidate) {
        throw "BLOCKED: downloaded Python archive contains no python.exe"
    }

    $sourceRoot = $pythonCandidate.Directory.FullName
    if (Test-Path -LiteralPath $pythonRoot) {
        Remove-Item -LiteralPath $pythonRoot -Recurse -Force
    }
    New-Item -ItemType Directory -Force $pythonRoot | Out-Null
    Copy-Item -Path (Join-Path $sourceRoot "*") -Destination $pythonRoot -Recurse -Force

    if (-not (Test-Work32Python $pythonExe)) {
        throw "BLOCKED: portable Python failed to start from runner tool cache"
    }
    Set-Content -LiteralPath (Join-Path $pythonRoot ".w32-runtime-version") -Value $pythonVersion -Encoding ascii
}

$env:PATH = "$pythonRoot;$pythonRoot\Scripts;$env:PATH"
& $pythonExe -m ensurepip --upgrade
if ($LASTEXITCODE -ne 0) {
    throw "BLOCKED: ensurepip failed for runner-local CPython"
}
& $pythonExe -m pip --version
if ($LASTEXITCODE -ne 0) {
    throw "BLOCKED: pip is unavailable in runner-local CPython"
}

@(
    "W32_PYTHON_EXE=$pythonExe",
    "W32_PYTHON_ROOT=$pythonRoot"
) | Out-File -FilePath $env:GITHUB_ENV -Append -Encoding utf8
@(
    $pythonRoot,
    (Join-Path $pythonRoot "Scripts")
) | Out-File -FilePath $env:GITHUB_PATH -Append -Encoding utf8

Write-Host "python_executable=$pythonExe"
Write-Host "python_version=$(& $pythonExe --version)"
Write-Host "python_root=$pythonRoot"
Write-Host "python_install_mode=runner-tool-cache-portable"
