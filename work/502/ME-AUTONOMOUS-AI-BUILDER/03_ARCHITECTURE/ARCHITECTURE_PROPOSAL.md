# KIẾN TRÚC ĐỀ XUẤT — MÊ AUTONOMOUS AI BUILDER
- Document ID: W502-ARCH-001
- Version: 0.1
- Date: 2026-11-18
- Status: PROPOSAL — CHỜ PHẢN BIỆN; BUILD NOT AUTHORIZED

## 1. Architecture decision
Use AutoGPT Platform as a candidate agent/workflow execution engine, self-hosted and isolated. MÊ is the product layer and ROOM-HOP remains the authority plane. AutoGPT does not become a replacement for ROOM-HOP Core, Work 501 or the canonical Work lifecycle.

## 2. Logical components
1. MÊ Intake/UI: accepts one natural-language request; captures attachments and optional constraints; displays assumptions and progress.
2. MÊ Manager: converts intent to PRD, task graph, dependencies, acceptance criteria, budgets and state transitions.
3. Role workflows: Research, Architect, Coder, Designer, QA and Deploy. Each role is a reusable AutoGPT agent/workflow graph with explicit inputs/outputs and tool permissions.
4. AutoGPT Platform: executes block graphs, task runs, queues and its own persistence as a subordinate runtime.
5. ROOM-HOP MÊ Adapter: authenticates/authorizes requests with ROOM-HOP; maps ROOM-HOP task/session/identity references to AutoGPT run IDs; enforces allowlists and budgets; records status and evidence references.
6. Model capability adapter: obtains approved model options from Work 501. Model routing is not reimplemented in MÊ.
7. Tool Gateway: controlled interfaces to GitHub, filesystem/workspace, terminal, browser, database, image generation and deployment. Every tool has schema, permission, timeout, resource cap, audit and side-effect class.
8. Evidence and QA: immutable run records, source commit references, test logs, screenshots, QA verdicts and handoff package.
9. MÊ Dashboard: read-only projection of canonical task state and evidence; command actions require ROOM-HOP authorization.

## 3. Role contracts
- Research: Input = PRD/unknowns; output = source-backed research with URL, date, license, confidence and open questions.
- Architect: Input = approved discovery; output = PRD, architecture, data/API model, ADRs, risk and acceptance criteria.
- Coder: Input = scoped task + architecture + source baseline; output = patch, changed-file list, test results and commit/branch reference where authorized.
- Designer: Input = user flows and brand constraints; output = wireframes/design tokens/assets and accessibility notes.
- QA: Input = acceptance criteria + immutable build candidate; output = independent test report, repro steps, logs, screenshots and PASS/FAIL/BLOCKED/NOT RUN.
- Deploy: Input = accepted release candidate + deployment authorization; output = deployment record, URL, environment, version, health checks and rollback reference.
- Manager: owns task graph and transitions, but cannot self-approve security, QA or production release.

## 4. Model topology
The architecture supports:
- SINGLE_MODEL: one approved LLM handles all six roles with role-specific prompts/tools.
- MULTI_MODEL: multiple approved models assigned by role or task.
- MIXED: one default model plus specialist models for selected tasks.
All model calls pass through Work 501 policy/router. Default pilot preference is one eligible local/zero-cost model until Work 501 establishes approved alternatives. No model ID/provider is final in this Work.

## 5. End-to-end flow
User request → Intake → assumption ledger → PRD → Research → Architect → task DAG → Manager assignment → role workflow execution → Coder/Designer changes in isolated workspace → automated checks → independent QA → bounded repair loop → acceptance → authorized preview/deploy → handoff.
- Parallelism only for independent tasks after interface contracts and workspace ownership are fixed.
- Concurrent writers must use separate branches/worktrees or explicit file locks; never permit unsynchronized edits to the same files.
- Retry policy: at most 3 attempts for the same approach; then change strategy or BLOCKED.
- Each task has maximum runtime/steps, model/token budget, tool budget, concurrency limit and cancellation path.

## 6. Trust boundaries and authority
- Vinh: final human authority.
- ROOM-HOP Core: canonical Agent identity, authorization, session/task ownership and global controls.
- Work 501: provider/model capability plane, routing and cost policy.
- AutoGPT: subordinate workflow runtime; its internal user/agent IDs are not authoritative ROOM-HOP identities.
- Tool Gateway/Sandbox: only execution route; no unrestricted host shell, production secret or arbitrary egress.
- GitHub: canonical source only after manifest path/branch is approved. No AI merge/push unless separately authorized by current ROOM-HOP policy.
- Model output, retrieved web pages, repository content and tool output are untrusted data; prompt injection must not alter policy or permissions.

## 7. AutoGPT platform fit and constraints (preliminary)
- Official docs describe a visual Agent Builder made of typed blocks and workflows, with API/MCP integration and self-hosting options.
- Current self-host quick-start documents a Docker-based single-container option bundling application/API/workers and supporting data services; manual multi-service setup is also available.
- Self-hosted model access requires owner-supplied credentials or a supported local model; hosted service and usage credits are not assumed free.
- Platform and Classic have different licenses. Current repository README identifies Platform under Polyform Shield and Classic under MIT. Exact release license and permitted internal/commercial use must be checked before adoption.
- Deployment must be private by default. Official setup warnings about network exposure and signup require explicit hardening; bind services to loopback or private network, disable open signup, set strong secrets and restrict service ports.

## 8. Data and persistence
Canonical MÊ business state remains in ROOM-HOP/Work-owned records. AutoGPT database/memory may be runtime state/cache and must have export, retention, backup and reconciliation rules. Do not create a competing source-of-truth for Work status. Store only references to secrets, never secret values. Content logging defaults to metadata/redacted; retention and deletion rules require review.

## 9. Failure and recovery
- Work 501 unavailable or no eligible model: BLOCKED; no direct provider bypass.
- ROOM-HOP authorization unavailable: fail closed.
- AutoGPT worker/queue/database unavailable: pause task, preserve state, retry only within bounded policy.
- Tool timeout/quota: record typed failure; do not silently switch to paid provider.
- QA failure: return to scoped repair; no acceptance.
- Evidence write failure: no PASS/ACCEPT/RELEASE.
- Deploy failure: rollback or remain on preview; no false demo URL.
- Orchestrator loop limit reached: stop and report blocker with evidence.

## 10. Security requirements
Threat model covers prompt injection, tool abuse, path traversal, command injection, SSRF, credential exfiltration, cross-tenant/Agent data leakage, malicious blocks/dependencies, supply-chain attacks, uncontrolled egress, resource exhaustion, audit tampering and unsafe deployment.
Required controls: per-task authorization, least privilege, allowlisted tools/hosts/commands, isolated workspaces, network egress controls, secret references, output validation, human approval for irreversible/high-impact actions, signed/pinned dependencies where practical, rate/concurrency/resource limits and append-only evidence.

## 11. Open ADRs
- ADR-001: AutoGPT Platform version and license/use permission.
- ADR-002: AutoGPT deployment topology and private-network hardening.
- ADR-003: ROOM-HOP ↔ AutoGPT identity/task/session mapping.
- ADR-004: Work 501 model invocation contract and SINGLE/MULTI routing.
- ADR-005: tool gateway and sandbox execution contract.
- ADR-006: canonical state, memory, evidence, retention and backup.
- ADR-007: concurrency, queue, retry, timeout and cancellation.
- ADR-008: QA independence and release/deploy authorization.
- ADR-009: dashboard data contract and controls.
All ADRs OPEN.

## 12. Build gate
No installation, model download, code implementation or deployment until source/contract discovery, license/security review, independent challenge, measurable QA plan, resource/cost budget and explicit Vinh approval are complete.