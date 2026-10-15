# WORK 28 — PC LISTENER IDENTITY EVIDENCE
Date: 2026-10-15 (UTC+07)
Reporter: Vinh / PC PowerShell output
Status: PARTIAL EVIDENCE — G0 NOT CLOSED

## Observed facts
- Local TCP listener: 127.0.0.1:8020, State=Listen, OwningProcess=6748.
- Process PID 6748: Python executable C:\Users\Admin\AppData\Local\Programs\Python\Python312\python.exe
- CommandLine: python.exe -m room_hop_mcp.mcp_http_main
- CreationDate: 2026-10-15 04:20:30 (PC-reported local time)
- Python version: 3.12.9
- Git HEAD in D:\ROOM-HOP-CLEAN\room-meeting-ai: d7c90d9d31062d389810808e43dfdd19d7711b75
- git status shows a heavily modified working tree and many untracked files, including room_hop_mcp/mcp_http_main.py, adapter modules, Core and execution_host files.
- Reported PC timestamp: 2026-10-15 05:02:41 +07:00.

## Interpretation
This establishes that a Python process is listening on local port 8020 and identifies its command line. It does NOT yet prove the process's effective working directory, loaded module path, runtime configuration, source hashes, or live MCP tools/list response. The HEAD SHA is not sufficient because the working tree is modified.

## Gate status
- G0 listener existence/PID/command line: PARTIAL PASS.
- G0 bind PID to effective source path + source hashes + config + raw live tools/list: BLOCKED.
- G1 canonical tests: NOT RUN / NO EVIDENCE.
- Cla security review: NOT PROVIDED.
- Go independent live E2E: BLOCKED.
- python_run registration, registry changes, sync writes, merge/release: NO-GO.

## Next read-only collection
1. Capture parent process PID 15124 details and listener PID again.
2. Inspect the actual route and protocol in room_hop_mcp/mcp_http_main.py and room_hop_mcp/adapter/http_server.py.
3. Hash the effective entrypoint and imported adapter files after establishing the process working directory/module path.
4. Execute initialize + tools/list against the live local listener using the protocol/endpoint found in source; save raw request/response, timestamps, exit code, and response hash.
5. Do not change files, restart the process, enable python_run, or mutate registry/sync state during evidence collection.
