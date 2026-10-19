# Role and Tool Routing

- Vinh: owner and final approval authority.
- Xu (AI-01): coordination, architecture, planning, evidence and handoff.
- Coder: scoped implementation only after approval.
- Tester/QE: independent checks and raw evidence.
- Reviewer: checks diff, scope, risks and test evidence.

ROOM-HOP path: AI/tooling → MCP :8020 → Core :8000 (source of truth) → Workspace :8010. Other services: Dashboard :3000 (render-only), Gateway :8040, Event Listener :8050, Agent Runtime :8051, Build MCP :8030, Execution Host :8031, Browser provider :8787.

Proposed CI path: GitHub branch/PR → Actions Python runner → gates → evidence → reviewer → Vinh decision. Do not bypass Core, expose secrets, or claim PASS without inspectable evidence.