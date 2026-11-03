# WORK 28 — ARCHITECTURE DECISION V2

**Decision ID:** AD-W28-20261103-001  
**Date:** 2026-11-03  
**Authority:** Vinh  
**Decision owner / coordinator:** Xu  
**Status:** DECIDED — implementation and runtime verification pending

## 1. Decision

Work 28 uses two distinct MCP service roles, with Core as the sole authority:

- **MCP Build/Verification :8030** — supported service for build, Work Sandbox verification and evidence support.
- **Runtime MCP — clean rebuild** — a separate runtime-facing MCP service, rebuilt from controlled source and deployed with a new service identity. The historical MCP :8020 listener is quarantined and DO NOT USE. No request, test, probe, restart, activation, mutation or traffic may be sent to that historical listener. Any future service at the intended Runtime MCP address must be a new deployment with proven process/source identity and an explicit migration record; it cannot inherit the old process or state.
- **Core :8000** — sole authority for identity, Work context, authorization, application policy and task lifecycle.
- **Execution Host :8031** — approved execution boundary. Runtime MCP may invoke only the authorized contract; it may not expose arbitrary shell or create a second execution host.

## 2. Authority flow

`AI/client → MCP interface → Core :8000 authorization and task authority → approved Runtime MCP/adapter → Execution Host :8031 → evidence and readback`

MCP :8030 remains the separate Build/Verification lane. It is not a substitute for Core authorization and must not become a parallel application authority.

## 3. Mandatory security properties

1. Deny by default; missing identity, Work context, policy decision or capability grant means BLOCKED/DENIED.
2. No direct database or Workspace access from MCP.
3. No Core bypass and no duplicate task/authorization authority.
4. No arbitrary command strings; execution uses bounded, approved command contracts.
5. Work-scoped path containment, symlink/traversal defenses, output limits, timeout/cancellation and audit evidence.
6. Process-tree containment must be established before untrusted command code executes. On Windows, spawning normally and assigning a Job Object afterward is not sufficient because it creates a race.
7. OS sandboxing is a separate control from process-tree containment. Keep OS isolation NOT_VERIFIED until independently evidenced.
8. Secrets must not enter logs, artifacts or tool responses.
9. Binary Sandbox uploads must be Work-authorized, bounded, staged safely, checksum-verified (SHA-256), atomically committed and auditable. Partial or checksum-mismatched uploads must fail closed; path traversal, symlink escape and unauthorized overwrite must be rejected.

## 4. Sandbox binary upload contract (WP3)

The Build/Verification MCP :8030 must provide a registered binary upload capability for authorized Work-scoped storage. The implementation may use bounded streaming/chunking when required by transport limits, but must preserve original bytes. It must enforce identity/Work scope, destination containment, quotas and no-overwrite-by-default; stage incomplete content outside the final destination; verify byte count and SHA-256; atomically promote only after successful verification; and write append-only audit evidence. The result must include upload/correlation ID, Work ID, normalized destination, size, SHA-256, service/build identity and final status. A readback check must independently confirm size and checksum. GitHub publication/synchronization is a separate operation and is not implied by Sandbox upload.

## 5. Service and deployment identity

Each service must expose a non-secret build identity and service identity. Evidence must bind:
- repository and commit SHA;
- build artifact hash;
- service identity and process identity;
- configured endpoint and port;
- startup time and health/readiness result;
- registered tool names and schema versions;
- runtime test run and evidence references.

A matching port or endpoint string alone is not proof that the intended binary is running.

## 6. Compatibility and migration

- Do not change existing consumers or production routing as a side effect of source changes.
- Do not touch the quarantined historical MCP :8020 listener.
- A new Runtime MCP deployment requires clean process identity, clean deployment path, verified contracts, security tests and rollback plan.
- Cutover is a separate gated decision. No migration or release is implied by this architecture decision.

## 7. Supersession

This decision supersedes conflicting statements in older Work 28 plans/architecture notes that treat the historical MCP :8020 listener as a supported live test target or the current runtime. Older documents remain preserved as historical evidence and must be interpreted through this decision and the current Work Manifest.
