# WORK 10 — ROOM-HOP INTEGRATION BOUNDARY / HANDOFF

- Document ID: W10-ROOM-HOP-INTEGRATION-HANDOFF-20261122-01
- Work: 10 — COMPUTER-AGENT
- Date-Time: 2026-11-22 06:35 (UTC+07:00)
- Prepared by: Co | AI-07 / End-to-End Architecture & Implementation Lead
- Authority: Owner's implementation delegation 2026-11-22
- Status: INTERFACE BOUNDARY DEFINED — RUNTIME INTEGRATION NOT IMPLEMENTED

## 1. Decision summary

Work 10 is the local Computer Agent capability provider. It must not bypass the ROOM-HOP Core authorization boundary, replace Work 24 PC Source Bridge, replace Work 14's canonical execution host, or create a second Dashboard listener on port 3000.

The correct integration is layered:

1. **W10 Computer Agent:** local loopback-only execution service for browser workflows and explicitly allowlisted PC host operations.
2. **W24 PC Source & Workspace Bridge:** shared cross-Work PC source access boundary; Core authorization and authenticated PC transport are required before any remote request reaches the PC.
3. **W112:** owns cross-Work contract definitions, identity/evidence correlation and integrated verification plan; its current baseline is DRAFT and not approved for runtime enforcement.
4. **W14:** sole product/delivery/release owner for the W12+W13+W14 autonomous E2E builder; Work 10 does not replace W14's canonical execution boundary.
5. **W113:** owner of the shared Universal Dashboard ingress on port 3000. Work 10's standalone operational UI is a local development/acceptance page only and uses port 3010.

## 2. Work 10 local API boundary

Work 10 currently exposes:
- `GET /health`
- `POST /agent/execute` — browser workflow
- `POST /agent/host/execute` — `list_directory`, `read_file`, `write_file`, `run_pytest`, `run_powershell_script`, `validate_acceptance_manifest`

Security controls:
- loopback binding by default;
- local bearer token;
- exact browser Origin allow-list;
- JSON-only request, bounded body and exclusive execution lease;
- ProcessSupervisor child containment and result correlation;
- filesystem allowlisted roots; writable and PowerShell roots disabled by default;
- no generic shell or inline PowerShell command.

**Critical limitation:** this is a local operator API, not a ROOM-HOP remote identity/authorization API. It does not currently consume a Core-issued `Authorization` decision, W24 signed `PCBridgeEnvelope`, nonce/expiry, or PC-initiated authenticated transport. Its local bearer token is not a substitute for Core authorization. Do not expose port 8787 to remote networks or call it directly from an AI member as a remote PC bridge.

## 3. W24 boundary and adapter requirements

W24 architecture defines a shared PC Source Bridge:
`AI member → MCP :8020 → Core :8000 authorization → authenticated PC transport → PC runtime`.

W24's current `CorePCBridgeService` is a fail-closed seam. It returns BLOCKED when the Core authorizer or authenticated PC transport is not configured. W24's `BridgeService` is a filesystem library, not an HTTP server and not yet wired to Core/MCP. The W24 acceptance plan explicitly says no real Core integration or authenticated PC transport exists yet.

Potential W24-to-W10 mapping, subject to W24/W112 approval:
- `source.list` → W10 `list_directory`
- `source.read` → W10 `read_file`
- `source.search` → W24's bounded indexed/search operation or a separately approved W10 operation; do not emulate arbitrary recursive search without a contract.
- `workspace.prepare_write/apply_write/readback` → W10 `write_file` only after W24 approval, expected preimage hash, backup/rollback and readback policy are enforced. W10 writable roots remain disabled unless the local operator explicitly configures them.
- `run_pytest` and `run_powershell_script` are execution capabilities, not source-reading operations. They must not be proxied through W24 until the owner-approved W12/W13/W14 execution-command contract explicitly permits the command IDs and caller policy.

Required adapter controls before integration:
1. Core authorizes `principal_id + work_id + operation + root_id` and returns a decision reference.
2. PC transport is authenticated and PC-initiated/managed; no guessed listener, URL or unauthenticated port.
3. Envelope includes request ID, nonce, expiry, principal, Work ID, decision reference, operation, root ID and bounded payload.
4. W10-side adapter validates the envelope and binds the Core decision to the local operation; replay/expiry/correlation failures BLOCK.
5. Response includes request ID, status, runtime instance/build hash and evidence reference.
6. W24/W112 define path-root mapping, file size/extension/secret redaction, audit semantics and write approval.
7. Any local API credential remains local; do not copy it into ROOM-HOP messages or use it as the cross-Work trust root.

Until these controls are implemented and tested, W24 must remain fail-closed and W10 remains local-only.

## 4. W14 / W09 execution boundary

- W14 manifest identifies W14 as sole product/delivery/release owner for W12+W13+W14 consolidation.
- W14 consumes W09/09.1 Browser Agent/Browser Workflow Engine through the canonical W13 `POST /execute` boundary.
- W10's ProcessSupervisor protects W10's own local agent worker and host operations. It is not a replacement for W14's canonical execution host and does not claim to own the W14 lifecycle.
- If W14 wants to consume W10 capabilities, define a versioned provider adapter and owner-approved command/permission contract through W112. Do not silently route W14 execution through W10's local API.

## 5. W113 shared Dashboard boundary

- W113 owns the single shared ROOM-HOP Dashboard ingress on port `3000`.
- Work 10's `08_DASHBOARD/` remains a standalone local development/acceptance UI and now uses loopback port `3010`.
- Work 10 must not bind port 3000 or start a second listener.
- Production route/module integration must be registered by W113 using its approved Work route and server-side identity/authorization contract. No route path is invented by Work 10.
- If W113 serves the Work 10 UI from a different origin, configure the Work 10 API's exact Origin allow-list to that approved origin only after the route and authentication design are accepted. The API remains loopback-only unless a separately approved authenticated transport is implemented.
- Static Dashboard contract test and hosted CI do not prove live W113 integration.

## 6. Ownership and handoff actions

| Work | Owns | Required next action |
|---|---|---|
| W10 | Local Computer Agent API/runtime/host operations | Maintain local-only boundary; provide versioned capability contract, test evidence and runbook |
| W24 | Shared PC Source Bridge / Core auth + authenticated PC transport | Design and implement authenticated adapter to a local PC capability provider; keep fail-closed until real Core/transport exist |
| W112 | Cross-Work contracts and integration verification | Define identity, operation, correlation, evidence and dependency contracts for W10↔W24↔W14↔W113 |
| W14 | Autonomous E2E builder product/runtime | Decide whether/how W10 capability provider is consumed without replacing W14 canonical execution boundary |
| W113 | Universal Dashboard / shared port 3000 | Register Work 10 operational UI as an authorized Work module; preserve one listener |
| W1111 | Technical engineering/debug lab | Investigate integration defects only when a reproducible issue and evidence are handed over; does not own W113 product UI |

## 7. Verification status

- W10 local API + ProcessSupervisor + host operations: hosted CI PASS on Windows Server 2022 and Ubuntu 24.04; physical Windows 10 acceptance remains NOT RUN.
- W24 Core authorization / authenticated PC transport: BLOCKED / NOT IMPLEMENTED per W24 architecture and acceptance plan.
- W112 cross-Work contract: DRAFT — DESIGN BASELINE; NOT APPROVED FOR RUNTIME ENFORCEMENT.
- W14 consuming W10: NOT IMPLEMENTED / NOT VERIFIED.
- W113 serving W10 Dashboard through shared port 3000: NOT IMPLEMENTED / NOT VERIFIED.
- W10 standalone Dashboard local port: changed to 3010 to avoid collision with shared 3000; hosted CI Run #69 must be followed by a fresh CI run after this change.

## 8. Non-actions

- No W24 source files changed.
- No W112 integration contract changed.
- No W14 execution boundary changed.
- No W113 product source or shared port-3000 listener changed.
- No remote W10 API exposure or direct Core bypass introduced.
- No cross-Work integration PASS is claimed.

**Disposition:** Work 10 local Computer Agent implementation continues independently. Cross-Work runtime integration is explicitly handed to the owning Works under W112 contract governance; it remains a separate gate and must not be fabricated inside Work 10.

**KÝ: Co | AI-07 / End-to-End Architecture & Implementation Lead**
