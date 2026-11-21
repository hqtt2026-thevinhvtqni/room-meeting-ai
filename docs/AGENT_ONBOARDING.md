# Internal Agent Onboarding

This document contains internal ROOM HOP agent onboarding and governance context. It is intentionally separate from the public-facing project overview in the root README.

## Required reading order

1. `AGENTS.md` — governance contract.
2. `context/PROJECT_STATE.md` — verified project state.
3. `context/XU_CORE.md` — Xu identity and authority context, if available in the working copy.
4. `context/XU_SESSION.md` — current session context, if available.
5. `context/XU_MEMORY.md` — long-term memory, if available.
6. `meetings/{latest}/` — historical evidence only; never treat a meeting log as the canonical project state.
7. `ROOM-2026-001-BASELINE-FROZEN-v0.2.1.md` and relevant sign-off/evidence files when the task touches that baseline.

## Context and authority

- `AGENTS.md` is the governance contract; it is not itself an authority actor.
- `context/PROJECT_STATE.md` is the canonical verified project-state record.
- Meeting logs are evidence, not current state.
- Authority hierarchy is defined by the project governance documents.
- Do not modify protected core files or a frozen baseline without the required authorization.

## Work record governance

Each Work should have one canonical record for each required record type, with duplicates explicitly marked superseded only after inventory and cross-linking. Never delete historical evidence merely to make the tree look clean.

Before changing a Work, locate its canonical plan, decision record, and running log. Update existing canonical records rather than creating competing copies. Every material log entry must identify the actor and role, timestamp in UTC+07:00, task, action, observed result, status, evidence link, owner, and next step.

Use only evidence-supported statuses: `DONE`, `PASS`, `BLOCKED`, `DECISION`, or `NOT VERIFIED`. A code change, a test execution, and acceptance are separate events.
