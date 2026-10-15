# WORK 28 — ARCHITECTURE AND DELIVERY PLAN

## 1. Mission
Build a coherent, typed and auditable MCP :8020 toolset that exposes ROOM-HOP capabilities to AI members while preserving Core :8000 as the single source of truth.

## 2. Layer boundaries
- MCP :8020: AI-facing tool schemas, identity propagation, validation, response normalization, correlation and evidence references.
- Core :8000: authoritative Work context, policy/authorization, task lifecycle and application-service routing.
- Sandbox API: Work-scoped file operations only where authorized.
- W12: canonical Work Execution Environment and WorkContext contract.
- W13: canonical Execution Host service/bridge; no duplicate runtime.
- W14: autonomous build UI/browser workflow consuming the canonical host.
- W24: shared PC source/workspace bridge with authenticated PC-initiated transport.
- W28: tool inventory, schema/version standards, adapters only where the actual Core/MCP integration seam is established, test harness and evidence standards.

## 3. Initial capability families
A. Discovery: list Works, inspect Work manifest, discover available capabilities and schemas.
B. Work files: list/read/write/search authorized Work Sandbox artifacts; validate relative paths and enforce scope.
C. Execution dispatch: submit typed WorkContext-bound execution requests to W12/W13 only through the canonical authorized route.
D. PC bridge: request source list/read/search or approved workspace operations through W24 only after Core route and authenticated transport exist.
E. Evidence: correlate task_id/request_id/run_id, record status, exit code, output references, source revision/hash and readback result.
F. Diagnostics: health/capability readiness and explicit BLOCKED reasons without exposing secrets.

## 4. Contract conventions
- Version every tool schema and document compatibility.
- Prefer structured arguments over free-form command strings.
- Require principal, Work identity/context, operation enum, bounded limits and correlation IDs where applicable.
- Normalize statuses: PASS, FAIL, BLOCKED, DENIED, TIMEOUT, NOT_FOUND, INVALID_REQUEST.
- Responses include request_id, status, safe message, result summary and evidence reference when available.
- Never promote timeout/network error/malformed response into PASS.

## 5. Security invariants
- Core owns authorization decisions; MCP does not self-authorize.
- Work-scoped root allowlists; reject traversal, absolute paths, UNC and alternate data stream paths where relevant.
- No arbitrary shell endpoint. Execution requests use approved command IDs and canonical W12/W13 policy.
- No secrets in Sandbox artifacts/logs; redact output.
- Bounded result sizes and timeouts; audit every mutation and execution.
- Separate read and write capabilities; writes require authorization and readback/hash verification.

## 6. Phases
Phase 0 — Inventory actual MCP tool list and current Core integration; distinguish existing live tools from design-only capabilities.
Phase 1 — Freeze tool schema conventions, capability registry, error model and security policy.
Phase 2 — Implement/reconcile typed adapters using actual available interfaces; do not invent routes.
Phase 3 — Contract/unit tests, denial/path traversal/timeout/size tests.
Phase 4 — Live E2E through MCP :8020 -> Core :8000 -> authorized capability -> evidence/readback.
Phase 5 — Versioning, onboarding docs, operations runbook and compatibility review.

## 7. Acceptance gates
- G1: inventory and dependency map reviewed.
- G2: schemas and policy contract reviewed.
- G3: unit/contract tests run on a real test runner with captured exit code.
- G4: negative authorization and path containment tests pass.
- G5: real MCP-to-Core E2E and artifact readback pass with correlated evidence.
- G6: compatibility verified against W12/W13/W14/W24; no duplicate execution or PC bridge.

## 8. Initial status
Work creation and document persistence can be verified through MCP responses. Tool implementation, runtime tests and live Core E2E are not yet proven by this creation step.
