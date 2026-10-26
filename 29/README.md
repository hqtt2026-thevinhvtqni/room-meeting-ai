# WORK 29 — HQTT AI VIDEO STUDIO

**Authority:** Vinh  
**Build owner:** Xu  
**Status:** IN PROGRESS — DESIGN BASELINE CREATED; IMPLEMENTATION NOT YET VERIFIED  
**Sandbox:** `sandbox/works/29`  
**Purpose:** Build an AI-directed, provider-pluggable video production system callable by ROOM-HOP agents through MCP.

## Product goal
A user submits a natural-language brief. The system turns it into a storyboard, creates or reuses brand/character assets, generates shots and voice/audio, assembles the final video, runs quality checks, and records reproducible evidence.

## MVP scope
1. Brief intake and structured project specification.
2. Script and shot-list generation.
3. Asset registry for characters, products, logos, and reference images.
4. Provider adapter contract for video/image/voice generation.
5. Render pipeline using FFmpeg when available.
6. Quality gate: output exists, decodes, duration/aspect ratio match, audio presence when required, subtitle/brand checks where automatable.
7. Project manifest, job states, costs/credits, logs, retry policy, and artifact references.
8. ROOM-HOP integration plan through MCP 8020 -> Core 8000 -> Workspace; never bypass Core.

## Non-goals for MVP
- Training our own foundation video model.
- Guaranteeing perfect character consistency or flawless generated text.
- Publishing automatically to social channels without explicit approval.
- Storing provider secrets in source files or logs.

## Architecture decision
Use a provider-neutral orchestration core with adapters. Start with a local/mock provider and deterministic render/test pipeline; add a real generation provider only after credentials, terms, and spend limits are configured. Runway has an official MCP endpoint and developer API; treat it as an optional provider, not a hard dependency.

## Build rule
No claim of PASS without runtime evidence. No paid generation in tests. External generation must be opt-in and cost-limited. Do not mark Work 29 COMPLETED or LOCKED until full E2E verification is real.
