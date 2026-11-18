# DOC-003 — DECISION LOG / W300

## D300-001 — Product scope (historical)
- Date: 2026-11-15
- Decision by: Vinh
- Original decision: image + video creative service, with a public MCP direction.
- Status: SUPERSEDED where conflicting by D300-005 (2026-11-19).

## D300-002 — Git source of truth
- Date: 2026-11-15
- Decision by: Vinh
- Decision: maintain W300 source in hqtt2026-thevinhvtqni/room-meeting-ai on main under work/300/ROOM-HOP-AI-CREATIVE-SERVICE/
- Status: USER-INSTRUCTED.

## D300-003 — UI/backend boundary
- Date: 2026-11-15
- Decision by: Xu
- Decision: existing Lovable project is a UI prototype and demo-only request simulator; it must not claim real AI generation, live progress, billing, persistence or MCP connectivity.
- Status: ACTIVE SAFETY CONSTRAINT; source preserved as legacy prototype pending review.

## D300-004 — W300-PILOT authorization (historical)
- Date: 2026-11-18
- Decision by: Vinh
- Original decision: bounded 15-second product video advertisement pilot with three scenes and image-to-video.
- Status: SUPERSEDED for W300 by D300-005. Preserve as audit history; video work belongs to Work 29.

## D300-005 — Scope correction: W300 is image/photo only
- Date: 2026-11-19
- Decision by: Vinh (Work Owner); recorded by Xu / AI-01.
- Decision: W300 is dedicated to image processing, photo editing/enhancement, AI image creation and Photo AI workflows. Work 29 remains the independent HQTT AI Video Studio.
- Supersedes D300-001 and D300-004 wherever they assign video production, image-to-video, video assembly or public-MCP exposure to W300. Historical entries are retained and not deleted.
- Public MCP, registration, tiers and public release are outside the current W300 scope and remain unauthorized unless separately decided.
- Current pilot proposal: zero-cash image pilot with text-to-image (FLUX.1 schnell candidate), image editing (FLUX.2 klein 4B candidate) and deterministic local image utilities. Model IDs/pricing are documented candidates only; account/quota/terms and actual quality remain unverified.
- Safety: no paid calls, payment method activation, auto-recharge, API invocation or private/customer-image upload. Initial cloud test cap is at most 3 requests, only after visible free quota and overage safeguards are verified.
- Build gate: no product code or provider integration until Architecture/Security and QE findings are reconciled into the single canonical DOC-034 and the build gate is explicitly opened.
- Status: ACTIVE SCOPE CORRECTION; reviews pending.
