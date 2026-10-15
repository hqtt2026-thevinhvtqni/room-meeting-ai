# WORK 28 — GO TASK: INDEPENDENT E2E ACCEPTANCE
Date: 2026-10-15 UTC+07
Owner: Go — Independent E2E Acceptance
Coordinator: Ka — CSA; final authority: Vinh
Status: ASSIGNED; live E2E BLOCKED pending prerequisites.

1. Read the Work 28 coordination order, manifest, latest Go blocked report, and PC listener evidence.
2. Readiness only: bind live listener PID to effective module path, source SHA-256, runtime configuration, and raw initialize/tools/list response. Check Cla security review.
3. If prerequisites are missing, report BLOCKED and exact missing evidence. Do not claim PASS from Sandbox access.
4. Only after prerequisites are proven, independently test the real MCP-to-Core/runtime path: Core-derived identity and WorkContext; read-only authorization; reject spoofed principal, cross-Work access, operation_kind spoofing; validate snapshot digest/revision before process creation; DRY_RUN only; replay/idempotency; missing/replaced evidence; evidence readback; intentional errors, timeout and cleanup.
5. Preserve raw request/response, logs, command, timestamp, exit code, run ID, PID/runtime identity, effective source SHA-256, per-gate expected/actual results, and readback proof.
6. No source changes, restart, python_run enablement, registry mutation, sync writes, merge, or release.

Known state: PC reported 127.0.0.1:8020 LISTEN PID 6748; command python -m room_hop_mcp.mcp_http_main; Python 3.12.9; Git HEAD d7c90d9d31062d389810808e43dfdd19d7711b75 with heavily modified working tree. Source/process/config/tools-list binding remains BLOCKED; canonical tests not evidenced; Cla review not provided; live E2E remains BLOCKED.