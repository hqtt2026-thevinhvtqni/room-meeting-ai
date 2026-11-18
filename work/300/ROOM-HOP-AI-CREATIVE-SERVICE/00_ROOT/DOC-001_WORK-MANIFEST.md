# DOC-001 — WORK MANIFEST
# W300 — AI IMAGE & PHOTO STUDIO

- Work ID: W300
- Canonical product name: AI Image & Photo Studio
- Repository: hqtt2026-thevinhvtqni/room-meeting-ai
- Canonical branch: main
- Work root: work/300/ROOM-HOP-AI-CREATIVE-SERVICE/
- Product scope: image creation, photo editing/enhancement, restoration, background/composition operations, batch image workflow and asset provenance.
- Explicit boundary: video production, image-to-video and video assembly are excluded from W300 and belong to Work 29 — HQTT AI Video Studio.
- Access direction: product access model remains OPEN; public MCP/service exposure is not authorized by this scope correction.
- Current phase: DISCOVER / DESIGN BASELINE / PILOT-01 REVIEW PREPARATION.
- Current status: ACTIVE — architecture, security, cost and QE review pending.
- User-confirmed correction: Vinh clarified on 2026-11-18/19 that W300 is dedicated to image/photo processing and creation; the earlier intro/meeting purpose is retired. Earlier W300 image+video/public-MCP direction and video-ad pilot are superseded for W300. Work 29 remains independent and owns video.
- Historical source preservation: existing Lovable dashboard source snapshot remains in 05_BUILD/04_CODE/dashboard as a preserved legacy UI prototype. It was created for the earlier creative-service scope; it is NOT accepted as the current image/photo product UI and must be reviewed before reuse. Do not delete or overwrite it.
- Provider candidates: Cloudflare Workers AI FLUX.1 schnell (text-to-image) and FLUX.2 klein 4B (image generation/editing) are documented candidates only; account access, quota, API call and output are not verified.
- Backend/provider/storage/billing/auth: NOT CONNECTED / NOT VERIFIED.
- Cash spend: 0 VND target for Pilot 01. No paid call, subscription, card activation, auto-recharge or other chargeable use.
- Architecture approval: PENDING independent review and canonical minutes.
- Build authorization: documentation/research only until Architecture/Security and QE findings are reconciled into canonical DOC-034 and the build gate is explicitly opened.
- Release status: NOT APPROVED.

## Canonical documents
DOC-001: this manifest. DOC-002: document register. DOC-003: decision log. DOC-034: canonical Biên bản / Minutes (DRAFT until review reconciliation). DOC-035: canonical execution journal. Implementation roadmap: 04_PLAN/IMPLEMENTATION_ROADMAP.md.

## Governance
Use READ → TRACE → ANALYZE → DECIDE → BUILD → VERIFY → HANDOFF. Record every operation, test and result in DOC-035. Do not report PASS without reproducible evidence. Keep one canonical document per type. Do not implement provider execution, upload user images, activate billing or build production services before review/build gates are satisfied.
