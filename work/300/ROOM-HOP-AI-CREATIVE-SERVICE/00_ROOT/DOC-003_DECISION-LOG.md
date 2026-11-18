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


## D300-004 — W300-PILOT authorization
- Date: 2026-11-18
- Decision by: Vinh (Founder)
- Decision: approve one bounded pilot workflow: create a 15-second 9:16 product advertisement from one supplied product photo; create three storyboard scenes (opening, coffee pour, product/CTA); obtain storyboard approval before any video generation; generate three scene images, three 5-second clips and assemble one final video; perform independent QA and handoff the final video, source images, storyboard, execution journal and cost record.
- Pilot customer hypothesis: small product shops / brands in Vietnam. This is a pilot hypothesis, not a confirmed market-wide segmentation decision.
- Budget: API spend ceiling = 0 VND. No paid API calls, paid trials, subscriptions, credit-card activation, automatic top-ups or other chargeable usage are authorized. If a step cannot be completed using verified no-cost resources, record BLOCKED and report; do not switch to paid resources.
- Deadline: 7 calendar days from 2026-11-18; target completion by 2026-11-25. Deadline does not override safety, approval or evidence gates.
- Provider: research only; prefer genuinely free options. No provider is selected until access terms, free allowance, billing safeguards, model identity, commercial-use terms and feasibility are verified.
- Scope exclusions: public MCP, registration, tiering, billing, production backend, new AI agents, public release and unrelated feature expansion remain out of this pilot.
- Approval gates: storyboard must be approved by Vinh/Mê before video generation. No paid spend is permitted under this decision. Existing DOC-001 architecture/security restrictions remain in force.
- Status: USER-AUTHORIZED BOUNDED PILOT; execution remains gated by zero-cost provider/compute feasibility and storyboard approval.
