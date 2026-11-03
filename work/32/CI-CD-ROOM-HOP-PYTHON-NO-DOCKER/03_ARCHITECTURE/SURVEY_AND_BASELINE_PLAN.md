# Read-only Survey and Baseline Plan

## Evidence so far
- Reviewed ROOM-HOP service topology through available MCP context.
- Repository: `hqtt2026-thevinhvtqni/room-meeting-ai`.
- Main head observed: `cc3100c835ad87ac9670a2ba38dc2c2dfae63755` (recheck before implementation).
- README SHA observed: `677ed190bf05735de326064d5e0ac323d38642ba`.
- requirements SHA observed: `59e0a4c07842154d82784eff85a9b412c6b33263`.
- Visible dependencies included pyyaml, pytest, python-dotenv and groq. Guessed missing paths are inconclusive, not proof of absence.
- No PC change and no CI activation.

## Survey checklist
1. Read governing docs: AGENTS.md, project state/context, XU docs, frozen baseline, SANDBOX_RULES and Work rules.
2. Map Python versions, dependencies, tests and current commands.
3. Inspect workflows, triggers, permissions, secrets, artifacts and branch policy.
4. Map service/test boundaries for Core :8000, Dashboard :3000, Workspace :8010, MCP :8020, Gateway :8040, Event Listener :8050, Agent Runtime :8051, Build MCP :8030, Execution Host :8031 and Browser provider :8787.
5. Define safe isolated tests, baseline commit and evidence.
6. Submit findings and acceptance plan for Vinh approval before implementation.