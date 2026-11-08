$ErrorActionPreference = "Stop"

# Install CPython into the self-hosted runner tool cache as the runner identity.
# This uses the signed python.org installer directly; it does not execute setup.ps1
# and does not change machine or user execution policy.
$pythonVersion = "3.12.10"
$installerUrl = "https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe"

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
    $installRoot = Join-Path $env:RUNNER_TEMP "w32-python-installer-$pythonVersion"
    New-Item -ItemType Directory -Force $installRoot | Out-Null
    $installer = Join-Path $installRoot "python-$pythonVersion-amd64.exe"
    Invoke-WebRequest -Uri $installerUrl -OutFile $installer -UseBasicParsing

    $signature = Get-AuthenticodeSignature -FilePath $installer
    if ($signature.Status -ne "Valid") {
        throw "BLOCKED: downloaded CPython installer Authenticode signature is not valid"
    }
    if ($signature.SignerCertificate.Subject -notmatch "Python Software Foundation") {
        throw "BLOCKED: CPython installer signer is not Python Software Foundation"
    }

    New-Item -ItemType Directory -Force $pythonRoot | Out-Null
    $arguments = @(
        "/quiet",
        "InstallAllUsers=0",
        "TargetDir=$pythonRoot",
        "Include_pip=1",
        "Include_launcher=0",
        "Include_test=0",
        "PrependPath=0",
        "Shortcuts=0",
        "AssociateFiles=0",
        "CompileAll=0"
    )
    $install = Start-Process -FilePath $installer -ArgumentList $arguments -Wait -PassThru
    if ($install.ExitCode -ne 0) {
        throw "BLOCKED: python.org installer exited with code $($install.ExitCode)"
    }
    if (-not (Test-Work32Python $pythonExe)) {
        throw "BLOCKED: installed CPython did not start from runner tool cache"
    }
}

$env:PATH = "$pythonRoot;$pythonRoot\Scripts;$env:PATH"
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
Write-Host "python_install_mode=python-org-signed-per-runner-user"
