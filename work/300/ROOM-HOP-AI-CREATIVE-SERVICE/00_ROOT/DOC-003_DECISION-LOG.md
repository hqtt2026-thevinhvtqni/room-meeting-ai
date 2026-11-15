# DOC-003 — DECISION LOG / W300

## D300-001 — Product scope
- Date: 2026-11-15
- Decision by: Vinh
- Decision: W300 covers both image and video; access direction is a public MCP service, with user registration to be introduced later.
- Status: USER-CONFIRMED SCOPE.
- Conditions: public endpoint must be isolated from internal ROOM-HOP; quotas, abuse protection, identity, tenant isolation and cost controls remain mandatory design topics.
- Not implied: anonymous unlimited access, real provider selection, production release.

## D300-002 — Git source of truth
- Date: 2026-11-15
- Decision by: Vinh
- Decision: build and maintain W300 source in the existing ROOM-HOP GitHub repository on main.
- Canonical location: work/300/ROOM-HOP-AI-CREATIVE-SERVICE/
- Status: USER-INSTRUCTED.
- Implementation: preserve the existing Lovable UI prototype as an isolated Work subproject. Do not connect Lovable to the repository root because that could overwrite unrelated ROOM-HOP files.

## D300-003 — UI/backend boundary
- Date: 2026-11-15
- Decision by: Xu (coordination safeguard)
- Decision: the Lovable project is a UI prototype and demo-only request simulator. It must not claim real AI generation, live progress, billing, persistence or MCP connectivity.
- Status: ACTIVE SAFETY CONSTRAINT.
- Architecture review remains pending. Production backend implementation is not authorized by this UI snapshot.
