# AI Agent Tool Stack 2026 — Production Readiness

Work: 19 — CẤU TRÚC HỌC TẬP
Prepared by: Xu (AI-01), coordinator
Date: 2026-10-20 (UTC+07:00)
Status: Learning baseline; ROOM-HOP mappings are hypotheses until verified with evidence.

## 1. Six layers of an AI Agent production stack
1. Orchestration and control flow — agent loop, planning, tool selection, workflow/state transitions, retries, timeouts, handoffs and human approval gates.
2. Protocol and tool integration — MCP (Model Context Protocol — giao thức kết nối mô hình với công cụ), typed tool contracts, authentication, input validation, least-privilege access and error semantics.
3. Model layer — model/provider abstraction, model routing, structured output, context limits, fallback policies and provider-specific behavior.
4. Memory and data — working/session state, durable records, document storage, indexing/retrieval when justified, data lineage, retention, backup and restore.
5. Observability and governance — traces, structured logs, metrics, audit records, identity, authorization, evaluation, policy enforcement and evidence.
6. Deployment and infrastructure — runtime isolation, resource limits, secrets, networking, service health, scaling, deployment/release controls and recovery.

These are conceptual layers, not a mandate to install six separate frameworks. Prefer the smallest architecture that satisfies a demonstrated use case.

## 2. Production readiness properties
- Reliability: bounded retries, timeouts, idempotency where needed, graceful failure, clear error contracts and recovery tests.
- Scalability: known workload assumptions, resource budgets, queue/backpressure strategy and measured capacity.
- Security: authentication, authorization, least privilege, input/output validation, secret handling, isolation and auditability.
- Observability: correlated request IDs, logs/traces/metrics, useful health checks and inspectable evidence.
- Cost optimization: token/tool/runtime cost measurement, budgets, limits, caching only when correctness permits, and cost per successful task.
- Evaluation: representative test cases, regression suite, quality/safety metrics, failure analysis and explicit acceptance thresholds.

A localhost demo or a successful single request is not, by itself, evidence of production readiness.

## 3. Preliminary mapping to ROOM-HOP
| Concern | Candidate component or Work | Verification boundary |
|---|---|---|
| Source of truth / control plane | Core :8000 | Verify contracts and authoritative state; do not infer from Dashboard display. |
| Human-facing rendering | Dashboard :3000 | Render-only; verify it does not become a competing state store. |
| AI tool boundary | MCP :8020 | Verify initialize, tools/list, invocation, errors and MCP → Core path. |
| Build workspace | App Workspace :8010 | Verify isolation and artifact lifecycle. |
| Gateway | Gateway :8040 | Verify routing, authentication and failure behavior. |
| Event delivery | Event Listener :8050 | Verify event contract, ordering/duplication assumptions and logs. |
| Agent execution | Agent Runtime :8051 | Verify runtime selection, policy enforcement and bounded execution. |
| Build tools | Build MCP :8030 | Historical state: blocked in a prior start-dev check; re-test before updating status. |
| Execution host | Execution Host :8031 | Verify isolation, resource limits, process lifecycle and artifact capture. |
| Browser execution | Browser Provider :8787 | Verify request-to-Chromium path and inspectable artifact. |
| Multi-runtime design | Work 27 | Verify contract/policy/adapter boundaries and runtime tests. |
| MCP tooling platform | Work 28 | Verify tools/list count and live MCP → Core → runtime evidence. |
| E2E builder | Work 14 | Verify real end-to-end evidence; do not promote based on plan or unit tests alone. |
| Evidence and handoff | Work 13 / Work 33 | Verify provenance, links, read-back and handoff completeness. |
| Provider integration | Work 23 | Verify provider contract, failure handling and cost boundaries. |

This mapping is an investigation index, not a live status report. Every status must be rechecked against current evidence before use.

## 4. Evidence and handoff are cross-cutting
For every meaningful operation, capture:
- who/which AI performed it and their role;
- date/time in UTC+07:00;
- task identifier and relevant version/commit;
- actual result and status;
- command, test, trace, log or artifact location;
- verifier and criterion passed or not passed;
- known limitations and next action.

Keep DONE (performed) distinct from PASS (verified). Never fabricate evidence or infer PASS from a successful write response.

## 5. Initial learning and review checklist
- [ ] Draw the actual request path and identify the source of truth.
- [ ] Document contracts at every boundary: request, response, error, identity and timeout.
- [ ] Trace one real request from AI/MCP through Core/runtime to a persisted artifact.
- [ ] Test unauthorized calls, malformed inputs, timeouts, duplicate requests and unavailable dependencies.
- [ ] Measure resource use and cost for a representative workload.
- [ ] Verify logs, correlation IDs, artifact links and evidence read-back.
- [ ] Test backup/restore and recovery for the data that matters.
- [ ] Define evaluation cases and explicit acceptance thresholds.
- [ ] Record unresolved gaps and owner decisions before implementation expansion.

## 6. Scope discipline
Do not add a vector database/RAG, Kubernetes, multi-provider routing, A2A or another framework solely because it appears in a stack diagram. First identify a concrete use case, volume, risk, measurable requirement and operating cost. Keep architecture before code and documentation before implementation.

## Conclusion
Production readiness is an evidence-backed property of the complete system, not a list of tools. For ROOM-HOP, prioritize a verified end-to-end trace, boundary contracts, security/resource controls, observability, recovery and reproducible acceptance evidence.
