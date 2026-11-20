# 09 — AI Templates Library Research: Phan Đông Giang / aitmpl.com

- Work: 21 — AI-SKILLS
- Record type: External library research note
- Status: RESEARCH ONLY — NO INSTALLATION / NO IMPLEMENTATION AUTHORIZED
- Research date: 2026-11-20 (UTC+07)
- Research coordinator: Xu / AI-01
- Product Owner / Final Authority: Vinh
- Primary entry: https://phandonggiang.com/ai-templates
- Referenced source library: https://aitmpl.com/
- Scope boundary: Evaluate the library as a source of reusable AI Skills / Agent Skills and adjacent configuration patterns for ROOM-HOP. This note does not authorize importing, installing, executing, copying code, changing runtime, changing any Work's configuration, GitHub record synchronization is permitted only under Vinh's explicit instruction, using the Work 21 branch and exact-path readback; this does not authorize installation or implementation.

## 1. Purpose

Capture the AI Templates library introduced by Vinh and establish a controlled research track within the existing Work 21 (AI-SKILLS). The goal is to discover reusable capabilities that may inform portable, evidence-first Skills for ROOM-HOP, not to collect tools indiscriminately.

## 2. Directly observed source facts

A direct page read of the Phan Đông Giang AI Templates page on 2026-11-20 showed:
- Page title: “AI Templates — Kho Agent, Skill & Công cụ cho Claude Code”.
- The page describes itself as a library for “Claude Code & ChatGPT Codex”.
- It displays 11 category labels: Skills, Agents, Commands, MCPs, Plugins, Hooks, Settings, Loops, Mods, Sandbox, Templates.
- It labels the library as open source and refers to the source library as MIT.
- The page links to aitmpl.com as the reference library.
- At the time of the page read, the visible catalog area showed “Đang tải thư viện…”, so the individual catalog entries and total counts were not independently enumerated in this inspection.

Primary evidence URL: https://phandonggiang.com/ai-templates
Reference URL: https://aitmpl.com/
Observation status: PAGE READ — CATEGORY LABELS CONFIRMED; ITEM-LEVEL INVENTORY NOT YET VERIFIED.

Important qualification: The page-level MIT label is not proof that every third-party item has identical licensing. License must be checked per repository/item before any future reuse.

## 3. Research taxonomy

| Category | Research question for ROOM-HOP |
|---|---|
| Skills | Can the procedure, inputs/outputs, preconditions, verification and failure handling be represented in the W21 Skill contract? |
| Agents | Are roles, boundaries, tool access and handoff contracts explicit and portable? |
| Commands | Are commands reproducible, scoped and safe for the relevant provider/runtime? |
| MCPs | What external capabilities and permissions do they expose? |
| Plugins | Are dependencies, lifecycle, provider compatibility and data access documented? |
| Hooks | What events trigger them; can they mutate state or run commands unexpectedly? |
| Settings | Which settings affect identity, permissions, model behavior or project scope? |
| Loops | Are stop conditions, retry budgets, idempotency and evidence capture defined? |
| Mods | What behavior or system configuration is changed, and how is rollback handled? |
| Sandbox | What isolation boundary is actually provided; what host/file/network access remains? |
| Templates | Are generated artifacts deterministic, reviewable and aligned with ROOM-HOP document standards? |

## 4. ROOM-HOP evaluation criteria

Every candidate item must be assessed against:
1. Functional value and concrete gap addressed in ROOM-HOP.
2. Platform/provider compatibility (Claude Code, GPT/Codex, Gemini, Qwen, Manus and other actual team environments); no compatibility inferred from marketing labels.
3. Portability: separate reusable procedure from provider-specific syntax or runtime assumptions.
4. Security: permissions, secrets, filesystem/network access, command execution, prompt injection and supply-chain risk.
5. Evidence: inputs, outputs, source version, execution method, logs, reproducibility and independently checkable result.
6. Maintenance: owner, versioning, dependencies, update cadence and upstream health.
7. License and reuse conditions at the individual source/repository level.
8. Integration boundary with W21 Skill schema/registry and existing ROOM-HOP MCP/A2A/Execution contracts.
9. Cost and operational prerequisites; no paid service or resource commitment without Vinh's explicit approval.
10. Duplication check against existing Work 21 skills and other Work owners before recommending adoption.

## 5. Priority research sequence

- P0: Skills and Agents — identify reusable capability patterns and role/skill boundaries.
- P1: Loops, Hooks and Commands — inspect automation, retries, event triggers and command safety.
- P1: MCPs and Plugins — map permissions, integration contracts and provider/runtime constraints.
- P2: Settings, Sandbox, Mods and Templates — inspect configuration, isolation and artifact generation.

This is a research order, not an adoption decision. Candidate ranking must be evidence-based after item-level inspection.

## 6. Required output for each candidate

- Candidate ID and exact upstream URL/repository/path.
- Exact version, commit or release inspected, and inspection date.
- Category and concise capability description.
- Prerequisites and supported platforms (verified, not assumed).
- License and attribution requirements.
- Security/permission review.
- Compatibility mapping to W21 Skill schema and ROOM-HOP contracts.
- Duplication/ownership check against existing Works.
- Reproducible evidence or explicit “not tested”.
- Recommendation: REJECT / RESEARCH FURTHER / ADAPT PROPOSAL / ELIGIBLE FOR FUTURE REVIEW.
- Any future implementation proposal must be separately approved before execution.

## 7. Explicit exclusions and safety controls

- No installation, package execution, script execution, MCP connection, plugin activation or configuration import in this research phase.
- No direct copy of upstream code into ROOM-HOP.
- No secrets, tokens, credentials or private user data may be supplied to external templates.
- No writes to Core, runtime, PC, GitHub main or other Works as part of this research note.
- No claim that a listed item is safe, compatible, MIT-licensed or functional until its exact source is inspected.
- Do not use category totals or download counts as a proxy for quality.
- Keep research artifacts in Work 21; do not create a parallel Work for the same AI Skills research scope.

## 8. Current findings and open questions

- The 11 top-level category labels are directly observed on the Phan Đông Giang page.
- The page presents the library as oriented to Claude Code and ChatGPT Codex; compatibility with the full ROOM-HOP AI roster is unverified.
- Item-level counts, complete catalog, source commit/version, per-item licenses, security posture, dependencies and runtime compatibility remain OPEN.
- No item has been selected for adoption.
- No technical test or installation has been performed.

## 9. Next research steps

1. Enumerate the actual upstream catalog and capture stable item URLs.
2. Inspect the source repository, version/commit and license metadata.
3. Sample candidates across the 11 categories, starting with Skills and Agents.
4. Run static review only: inspect source, scripts and declared permissions without executing them.
5. Compare candidates with W21's existing schema, registry, research backlog and existing Skills.
6. Produce an evidence-backed shortlist and recommendation for Vinh; keep implementation unauthorized until an explicit decision.

## 10. Source

- Phan Đông Giang AI Templates: https://phandonggiang.com/ai-templates
- Reference library: https://aitmpl.com/

