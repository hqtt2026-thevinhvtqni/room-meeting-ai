# WORK 28 — PC read-only live provenance collection

**Purpose:** close the remaining live source/process identity and raw MCP discovery evidence gaps without modifying the PC checkout or restarting any service.

## Run

Open PowerShell on the PC hosting ROOM-HOP and run:

    $repo = "D:\ROOM-HOP-CLEAN\room-meeting-ai"
    $script = Join-Path $repo "work\28\MCP-8020-TOOLING-PLATFORM\06_EVIDENCE\PC_READONLY_LIVE_PROVENANCE_COLLECTOR_20261123.ps1"
    powershell -NoProfile -ExecutionPolicy Bypass -File $script

The collector writes its output under $env:TEMP\W28_LIVE_PROVENANCE_<timestamp>\.

## What it captures

- Local Git branch, HEAD and short dirty-tree status.
- Listener process metadata for ports **8000, 8001, 8030 and 8031**: PID, executable, parent PID, creation time and parsed Python -m module name. It never prints the full process command line or environment.
- SHA-256 and metadata for the current local source files that define Core, MCP and Execution Host boundaries.
- A read-only MCP protocol handshake followed by **tools/list only** against the historical candidate endpoint https://admin-pc.tail7d6101.ts.net/build/mcp, whose existence was recorded in the October 22/23 baseline. It records the response body and its UTF-8 capture digest.

## Safety boundary

- Does not inspect or connect to historical MCP **:8020**.
- Does not call tools/call, write files in the repository, alter Git state, stop/restart processes, change environment variables, or provision credentials.
- Does not print secrets, .env values, authorization headers or full process command lines.
- Does not try another endpoint if the candidate endpoint fails. A failure remains BLOCKED and the endpoint must be re-identified before any new probe.
- A file hash from the current worktree is not proof of the bytes already loaded in a running process; it must be correlated with process start time, module path and deployment evidence.

## Return to Vi

Provide only:
1. The contents of summary.txt.
2. The contents of mcp_tools_list_raw.txt if created.
3. The exact evidence folder timestamp.

Do not send .env files, environment variables, credentials, authorization headers, or full process command lines. If the endpoint is unreachable, return the BLOCKED status and error text; do not start or restart a service as a workaround.

**Expected disposition:** this evidence can close or narrow WP0 provenance only after it is correlated with the canonical branch and exact deployed module/build. It does not by itself authorize execution, upload, deployment or release.
