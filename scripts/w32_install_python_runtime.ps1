$ErrorActionPreference = "Stop"

# Python embeddable distribution: no MSI, no setup.ps1, no user-profile install.
# Pinned official python.org release and published MD5 integrity value.
$pythonVersion = "3.12.10"
$archiveName = "python-$pythonVersion-embed-amd64.zip"
$archiveUrl = "https://www.python.org/ftp/python/$pythonVersion/$archiveName"
$expectedMd5 = "fe8ef205f2e9c3ba44d0cf9954e1abd3"

if ([string]::IsNullOrWhiteSpace($env:RUNNER_TOOL_CACHE)) {
    throw "BLOCKED: RUNNER_TOOL_CACHE is unavailable"
}

$pythonRoot = Join-Path $env:RUNNER_TOOL_CACHE "Python\$pythonVersion\x64"
$pythonExe = Join-Path $pythonRoot "python.exe"
$sitePackages = Join-Path $pythonRoot "Lib\site-packages"

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
    $downloadRoot = Join-Path $env:RUNNER_TEMP "w32-python-embed-$pythonVersion"
    New-Item -ItemType Directory -Force $downloadRoot | Out-Null
    $archive = Join-Path $downloadRoot $archiveName
    Invoke-WebRequest -Uri $archiveUrl -OutFile $archive -UseBasicParsing

    $actualMd5 = (Get-FileHash -LiteralPath $archive -Algorithm MD5).Hash.ToLowerInvariant()
    if ($actualMd5 -ne $expectedMd5) {
        throw "BLOCKED: official Python embeddable archive checksum mismatch"
    }

    if (Test-Path -LiteralPath $pythonRoot) {
        Remove-Item -LiteralPath $pythonRoot -Recurse -Force
    }
    New-Item -ItemType Directory -Force $pythonRoot | Out-Null
    Expand-Archive -LiteralPath $archive -DestinationPath $pythonRoot -Force

    $pth = Join-Path $pythonRoot "python312._pth"
    if (-not (Test-Path -LiteralPath $pth -PathType Leaf)) {
        throw "BLOCKED: embeddable Python path configuration is missing"
    }
    New-Item -ItemType Directory -Force $sitePackages | Out-Null
    $pthLines = @(Get-Content -LiteralPath $pth)
    if ($pthLines -notcontains "Lib\site-packages") {
        $pthLines += "Lib\site-packages"
    }
    $pthLines = @($pthLines | ForEach-Object {
        if ($_ -eq "#import site") { "import site" } else { $_ }
    })
    if ($pthLines -notcontains "import site") { $pthLines += "import site" }
    Set-Content -LiteralPath $pth -Value $pthLines -Encoding ascii

    if (-not (Test-Work32Python $pythonExe)) {
        throw "BLOCKED: embedded CPython failed its version check"
    }

}

# RUNNER_TOOL_CACHE persists between jobs. Recreate site-packages for each run
# so old httpx/httpx2 versions cannot leak into the current constrained install.
if (Test-Path -LiteralPath $sitePackages) {
    Remove-Item -LiteralPath $sitePackages -Recurse -Force
}
New-Item -ItemType Directory -Force $sitePackages | Out-Null

$getPip = Join-Path $env:RUNNER_TEMP ("w32-get-pip-" + $env:GITHUB_RUN_ID + ".py")
Invoke-WebRequest -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile $getPip -UseBasicParsing
& $pythonExe $getPip --no-warn-script-location --no-compile --target $sitePackages
if ($LASTEXITCODE -ne 0) {
    throw "BLOCKED: pip bootstrap into clean runner-local site-packages failed"
}

$env:PATH = "$pythonRoot;$env:PATH"
$env:PYTHONPATH = $sitePackages
"PYTHONPATH=$sitePackages" | Out-File -FilePath $env:GITHUB_ENV -Append -Encoding utf8
& $pythonExe -m pip --version
if ($LASTEXITCODE -ne 0) {
    throw "BLOCKED: pip is unavailable in embedded CPython"
}
$version = & $pythonExe --version
if ($LASTEXITCODE -ne 0 -or "$version" -ne "Python $pythonVersion") {
    throw "BLOCKED: embedded CPython version attestation failed"
}

@(
    "W32_PYTHON_EXE=$pythonExe",
    "W32_PYTHON_ROOT=$pythonRoot",
    "W32_PYTHON_SITE_PACKAGES=$sitePackages"
) | Out-File -FilePath $env:GITHUB_ENV -Append -Encoding utf8
@($pythonRoot) | Out-File -FilePath $env:GITHUB_PATH -Append -Encoding utf8

Write-Host "python_executable=$pythonExe"
Write-Host "python_version=$version"
Write-Host "python_root=$pythonRoot"
Write-Host "python_site_packages=$sitePackages"
Write-Host "python_install_mode=official-embeddable-zip"
Write-Host "python_archive_md5=$actualMd5"
