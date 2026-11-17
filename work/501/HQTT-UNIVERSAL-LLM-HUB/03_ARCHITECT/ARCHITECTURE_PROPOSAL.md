# ARCHITECTURE PROPOSAL — HQTT UNIVERSAL LLM HUB
- Version: 0.1 | Date: 2026-11-17 | Status: PROPOSAL — NOT APPROVED FOR BUILD
## 1. Intent
Provider-neutral LLM capability plane for ROOM-HOP. Local inference preferred; free cloud fallback only under explicit policy; paid denied by default; Model Arena is first-class.
## 2. Components
1. Provider Registry: provider, endpoint class, auth reference, region, terms/privacy review and health.
2. Model Registry: immutable model ID/version, modalities, context, tool/function support, structured output, license, provenance and verification date.
3. Global Policy Engine: Vinh's global controls; Agent/role/task grants; data classification; provider/model allowlists; cost ceiling currently zero.
4. Model Router: capability matching, local-first preference, health/capacity, deterministic selection and explicit fallback.
5. Provider Adapters: normalized invocation contract for local runtimes and cloud APIs.
6. Secret integration: reference existing approved secret store; do not create duplicate vault without evidence.
7. Usage/Audit: provider/model/version, Agent/task/session refs, policy decision, timestamp, latency, usage when returned, fallback and error; redact content by default.
8. Arena Orchestrator: independent first pass, sealed submissions, optional challenge, rubric scoring and provenance.
9. Dashboard: live canonical data only; authorized controls; NOT VERIFIED for unavailable data.
## 3. Trust boundaries
Vinh is global human authority. ROOM-HOP Core is expected to remain authoritative for Agent identity/authorization; verify source contract. Existing Gateway/Agent Runtime remain invocation boundaries unless discovery and ADR prove otherwise. LLM Hub cannot issue identities, grant permissions, own sessions or bypass Core. Provider secrets remain server-side. Model output is untrusted and tool execution remains subject to existing authorization.
## 4. Invocation flow
Agent task → ROOM-HOP authorization → LLM Hub policy → capability filter → local-first router → adapter → runtime/provider → normalized response → audit/usage → Agent. If local unavailable, only explicitly allowed free cloud can be considered. If no eligible option exists, return BLOCKED. No silent paid fallback.
## 5. Local runtime candidates — not decisions
Ollama and llama.cpp are candidates. Existing Agent Runtime/provider adapters may already cover some capabilities. Compare OS/hardware, CPU/GPU/VRAM/RAM, quantization, throughput, concurrency, context, tool calling, structured output, multimodal needs, license, model provenance, security/update process and operational burden. No install or model download authorized.
## 6. Gateway candidates — not decisions
LiteLLM is a candidate; existing ROOM-HOP Gateway/adapters are preferred reuse targets if they meet policy, auth, provider-neutral contract, observability and fallback needs. Do not deploy a second gateway by default. Decide after source inspection, license/security review and approved design.
## 7. Model Arena
Freeze task/input/context/model versions/parameters/rubric; run independent blind first pass; preserve immutable submissions; optionally run separate cross-critique; score against task-specific rubric and authoritative evidence; record evaluator and conflicts; human adjudication for high-impact results. Controls: model allowlist, data-egress policy, concurrency/token/resource caps, timeout, rate limit, zero-cost guard, reproducibility where supported. Majority vote is not ground truth.
## 8. Data model candidates
Provider, ModelVersion, AgentModelGrant, RoutingPolicy, Invocation, UsageRecord, ArenaRun, ArenaSubmission, ArenaEvaluation, PolicyDecision. Final schema/storage owner depends on Core/Gateway contracts.
## 9. Failure behavior
Local unavailable: eligible local alternatives, then approved free cloud or BLOCKED. Quota exhaustion: mark QUOTA_EXHAUSTED and report retry info if provided. Invalid credential: fail closed. Unsupported capability: reject candidate. Partial Arena: label incomplete. Audit failure: define fail-closed policy during review. Egress denied: remain local-only.
## 10. Threats
Prompt injection, malicious model output, SSRF/custom endpoints, credential exfiltration, cross-Agent leakage, provider retention/training, model supply chain, tool misuse, quota abuse, denial of service and audit tampering. Controls include endpoint allowlists, egress policy, TLS, scoped secrets, redaction, rate/concurrency/resource limits, model provenance and authorization on every invocation.
## 11. Open ADRs
ADR-001 existing Gateway vs LiteLLM vs custom adapter; ADR-002 local runtime; ADR-003 registry schema/storage; ADR-004 Core policy/grants; ADR-005 Arena isolation/rubric; ADR-006 logs/privacy/retention/secrets; ADR-007 dashboard ownership. All OPEN.
## 12. Build gate
No BUILD until related source/runtime inspection, hardware assessment, security/privacy/cost review, independent Cla/Ka/Qw/Vibe findings, provider review, QE acceptance plan, ADR reconciliation and explicit Vinh approval.