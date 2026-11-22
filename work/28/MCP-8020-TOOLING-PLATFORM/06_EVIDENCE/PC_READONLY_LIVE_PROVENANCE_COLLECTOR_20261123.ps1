# WORK 28 — read-only deployed provenance collector
# Date: 2026-11-23 (UTC+07)
# Captures listener/process identity, local source hashes, and raw MCP tools/list.
# Never probes historical :8020, never calls tools/call, never restarts services, never reads secrets.
$ErrorActionPreference = "Stop"
$repo = "D:\ROOM-HOP-CLEAN\room-meeting-ai"
# Candidate endpoint from the historical 2026-10-22/23 MCP 8030 baseline; failure stays BLOCKED.
$mcpEndpoint = "https://admin-pc.tail7d6101.ts.net/build/mcp"
$ports = @(8000, 8001, 8030, 8031)
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$outDir = Join-Path $env:TEMP ("W28_LIVE_PROVENANCE_" + $stamp)
New-Item -ItemType Directory -Path $outDir -Force | Out-Null
$summaryPath = Join-Path $outDir "summary.txt"
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Write-Section([string]$Name, $Value) {
    [Environment]::NewLine + "=== $Name ===" | Tee-Object -FilePath $summaryPath -Append
    if ($Value -is [string]) { $Value | Tee-Object -FilePath $summaryPath -Append }
    else { ($Value | ConvertTo-Json -Depth 20) | Tee-Object -FilePath $summaryPath -Append }
}

if (-not (Test-Path -LiteralPath $repo -PathType Container)) { throw "Repository path not found: $repo" }
$branch = (& git -C $repo branch --show-current 2>&1 | Out-String).Trim()
$head = (& git -C $repo rev-parse HEAD 2>&1 | Out-String).Trim()
$status = @(& git -C $repo status --short 2>&1)
Write-Section "LOCAL REPOSITORY" ([pscustomobject]@{
    repo = $repo; branch = $branch; head = $head
    dirty = ($status.Count -gt 0); status_short = $status
})

# Listener inventory: do not print full process command lines or environment variables.
$listeners = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue |
    Where-Object { $ports -contains $_.LocalPort } |
    Sort-Object LocalPort, LocalAddress, OwningProcess)
$processEvidence = foreach ($listener in $listeners) {
    $proc = Get-CimInstance Win32_Process -Filter ("ProcessId = " + [int]$listener.OwningProcess) -ErrorAction SilentlyContinue
    if ($null -eq $proc) { continue }
    $module = "<not-resolved>"
    if ($proc.CommandLine -match '(?i)(?:^|\s)-m\s+([A-Za-z0-9_.]+)') { $module = $Matches[1] }
    $parent = Get-CimInstance Win32_Process -Filter ("ProcessId = " + [int]$proc.ParentProcessId) -ErrorAction SilentlyContinue
    $moduleFile = $null; $moduleSha256 = $null
    if ($module -ne "<not-resolved>") {
        $relative = ($module.Replace(".", [IO.Path]::DirectorySeparatorChar)) + ".py"
        $candidate = Join-Path $repo $relative
        if (-not (Test-Path -LiteralPath $candidate -PathType Leaf)) {
            $moduleDir = Join-Path $repo ($module.Replace(".", [IO.Path]::DirectorySeparatorChar))
            $candidate = Join-Path $moduleDir "__init__.py"
        }
        if (Test-Path -LiteralPath $candidate -PathType Leaf) {
            $moduleFile = $candidate
            $moduleSha256 = (Get-FileHash -LiteralPath $candidate -Algorithm SHA256).Hash.ToLowerInvariant()
        }
    }
    [pscustomobject]@{
        address = $listener.LocalAddress; port = [int]$listener.LocalPort
        pid = [int]$proc.ProcessId; process = $proc.Name; executable = $proc.ExecutablePath
        parent_pid = [int]$proc.ParentProcessId
        parent_process = if ($parent) { $parent.Name } else { $null }
        process_created = $proc.CreationDate; python_module = $module
        module_file_candidate = $moduleFile; module_file_sha256 = $moduleSha256
    }
}
Write-Section "LISTENERS (NO 8020 PROBE)" $processEvidence

# Hash canonical files from the current local worktree (not assumed clean or equal to process memory).
$sourceFiles = @(
    "room_hop_mcp/adapter/server.py",
    "room_hop_mcp/adapter/http_server.py",
    "room_hop_mcp/__main__.py",
    "core/execution_authority/http_server.py",
    "core/execution_authority/authority.py",
    "execution_host/server.py",
    "work/28/MCP-8020-TOOLING-PLATFORM/04_CODE/mcp8020_unified_registry_v1.py",
    "work/28/MCP-8020-TOOLING-PLATFORM/04_CODE/mcp8020_unified_server_v1.py"
)
$hashes = foreach ($relative in $sourceFiles) {
    $full = Join-Path $repo $relative
    if (Test-Path -LiteralPath $full -PathType Leaf) {
        $item = Get-Item -LiteralPath $full
        [pscustomobject]@{
            path = $relative
            sha256 = (Get-FileHash -LiteralPath $full -Algorithm SHA256).Hash.ToLowerInvariant()
            length = $item.Length; last_write_utc = $item.LastWriteTimeUtc
        }
    } else {
        [pscustomobject]@{ path = $relative; sha256 = $null; length = $null; last_write_utc = $null; status = "NOT_FOUND" }
    }
}
Write-Section "SOURCE FILE HASHES (LOCAL WORKTREE)" $hashes

function Convert-McpResponseToObject([string]$Raw) {
    if ([string]::IsNullOrWhiteSpace($Raw)) { throw "empty_mcp_response" }
    $trimmed = $Raw.Trim()
    if ($trimmed.StartsWith("{")) { return ($trimmed | ConvertFrom-Json) }
    $dataLines = @($Raw -split '\r?\n' | Where-Object { $_ -match '^data:\s*' })
    if ($dataLines.Count -eq 0) { throw "mcp_response_has_no_json_data_event" }
    $jsonText = ($dataLines[-1] -replace '^data:\s*', '').Trim()
    return ($jsonText | ConvertFrom-Json)
}

$mcpResult = [ordered]@{
    endpoint = $mcpEndpoint; status = "NOT_RUN"; protocol_version = $null
    tool_count = $null; tool_names = @(); captured_body_utf8_sha256 = $null; error = $null
}
try {
    $accept = "application/json, text/event-stream"
    $initBody = @{
        jsonrpc = "2.0"; id = 1; method = "initialize"
        params = @{
            protocolVersion = "2025-03-26"; capabilities = @{}
            clientInfo = @{ name = "work28-readonly-provenance"; version = "1.0.0" }
        }
    } | ConvertTo-Json -Depth 10 -Compress
    $initResponse = Invoke-WebRequest -Uri $mcpEndpoint -Method Post -UseBasicParsing -Headers @{ Accept = $accept } -ContentType "application/json" -Body $initBody -TimeoutSec 20
    $initRaw = [string]$initResponse.Content
    [IO.File]::WriteAllText((Join-Path $outDir "mcp_initialize_raw.txt"), $initRaw, $utf8NoBom)
    $initObject = Convert-McpResponseToObject $initRaw
    if ($initObject.error) { throw ("mcp_initialize_error: " + ($initObject.error | ConvertTo-Json -Compress)) }
    $negotiated = $initObject.result.protocolVersion
    if (-not $negotiated) { $negotiated = "2025-03-26" }
    $headers = @{ Accept = $accept; "MCP-Protocol-Version" = [string]$negotiated }
    $sessionId = [string]$initResponse.Headers["Mcp-Session-Id"]
    if (-not [string]::IsNullOrWhiteSpace($sessionId)) { $headers["Mcp-Session-Id"] = $sessionId }

    $notifyBody = @{ jsonrpc = "2.0"; method = "notifications/initialized"; params = @{} } | ConvertTo-Json -Depth 5 -Compress
    $null = Invoke-WebRequest -Uri $mcpEndpoint -Method Post -UseBasicParsing -Headers $headers -ContentType "application/json" -Body $notifyBody -TimeoutSec 20

    $listBody = @{ jsonrpc = "2.0"; id = 2; method = "tools/list"; params = @{} } | ConvertTo-Json -Depth 5 -Compress
    $listResponse = Invoke-WebRequest -Uri $mcpEndpoint -Method Post -UseBasicParsing -Headers $headers -ContentType "application/json" -Body $listBody -TimeoutSec 30
    $raw = [string]$listResponse.Content
    $rawPath = Join-Path $outDir "mcp_tools_list_raw.txt"
    [IO.File]::WriteAllText($rawPath, $raw, $utf8NoBom)
    $listObject = Convert-McpResponseToObject $raw
    if ($listObject.error) { throw ("mcp_tools_list_error: " + ($listObject.error | ConvertTo-Json -Compress)) }
    $tools = @($listObject.result.tools)
    $mcpResult.status = "PASS_READONLY_PROTOCOL_RESPONSE"
    $mcpResult.protocol_version = $negotiated
    $mcpResult.tool_count = $tools.Count
    $mcpResult.tool_names = @($tools | ForEach-Object { $_.name })
    $mcpResult.captured_body_utf8_sha256 = (Get-FileHash -LiteralPath $rawPath -Algorithm SHA256).Hash.ToLowerInvariant()
    [IO.File]::WriteAllText((Join-Path $outDir "mcp_tools_list_parsed.json"), ($listObject | ConvertTo-Json -Depth 40), $utf8NoBom)
} catch {
    $mcpResult.status = "BLOCKED"
    $mcpResult.error = $_.Exception.Message
}
Write-Section "RAW MCP TOOLS/LIST (READ ONLY; NO TOOLS/CALL)" ([pscustomobject]$mcpResult)
[Environment]::NewLine + "Evidence folder: $outDir" | Tee-Object -FilePath $summaryPath -Append
"Do not send .env files, environment variables, credentials, authorization headers, or full process command lines."
