# W300 — IMPLEMENTATION ROADMAP / KẾ HOẠCH TRIỂN KHAI

## Phase 01_DISCOVER — current
1. Confirm scope and public-access direction — DONE by Vinh.
2. Inspect ROOM-HOP gateway/runtime/storage capabilities — BLOCKED pending stable Sandbox/MCP 8030 access.
3. Collect independent architecture reviews from Ka, Cla, Kha, Go and QE — PENDING.
4. Reconcile review opinions into final DOC-034 — PENDING.
5. Obtain Vinh approval of final architecture — PENDING.

## Phase 02_DESIGN
1. Finalize public MCP contract and tool schemas.
2. Define authentication/onboarding, tenant isolation and authorization.
3. Define asynchronous job lifecycle, idempotency, retries, cancellation and job ownership.
4. Define provider adapter interface for image/video.
5. Define storage, asset delivery, retention and deletion policy.
6. Define cost ledger, quotas, abuse protection and customer tiers.
7. Define quality checks, moderation, audit and operational monitoring.

## Phase 03_BUILD — gated
1. Build isolated public gateway only after architecture/security approval.
2. Implement image pipeline and verify against acceptance criteria.
3. Implement video pipeline and verify asynchronous lifecycle.
4. Connect storage/delivery and customer project/job persistence.
5. Integrate auth, quota/cost controls and audit.
6. Keep internal ROOM-HOP Core, Runtime, Sandbox and Build MCP inaccessible from customer routes.

## Phase 04_VERIFY
- Contract tests, unit/integration tests, tenant isolation tests, security tests, abuse/cost tests, failure/retry/idempotency tests, image/video output quality tests, independent QE.
- Each test result must be recorded in DOC-035 with method, evidence and PASS/FAIL/BLOCKED.

## Phase 05_RELEASE
- Public release only after gates G0–G8, operational readiness and Vinh's explicit release approval.

## Current gates
- G0 Scope: USER-CONFIRMED.
- G1 Architecture: PENDING.
- G2 Security: PENDING.
- G3 MCP contract: PENDING.
- G4 Image pipeline: NOT BUILT.
- G5 Video pipeline: NOT BUILT.
- G6 QE: NOT RUN.
- G7 Operations/cost: NOT READY.
- G8 Public release: NOT APPROVED.

## UI prototype
The Lovable UI snapshot is a demo-only front-end shell. It may be refined independently as a visual prototype, but it does not close any production gate above.


---

## Bounded execution track — W300-PILOT (Founder-approved 2026-11-18)
This track is a constrained validation experiment inside W300; it does not replace the broader product roadmap or approve production architecture.

### Approved objective
Produce one playable 15-second (±2s), 9:16 product advertisement from one customer-supplied product photo and one brief, using three scenes: opening, coffee pour, product close/CTA. The pilot brief is a test input; do not invent product claims, origin, certifications or ingredients beyond what the supplied asset/brief explicitly states.

### Work sequence and gates
1. READ: inspect supplied image and brief; create job/work record; identify unknowns and prohibited assumptions.
2. TRACE: record agent/operator, provider/model/version, timestamps, usage/token data when exposed, compute source and evidence.
3. ANALYZE: prepare concept and exactly three storyboard scenes.
4. DECIDE: obtain explicit Vinh/Mê storyboard approval before image/video generation.
5. BUILD: only use resources verified to incur zero API/compute charges and requiring no payment activation. Create three scene images, three 5-second clips and assemble the final video. If infeasible, stop and record BLOCKED.
6. VERIFY: independent QA checks duration, aspect ratio, scene coverage, product/logo/text integrity, playability and source-to-output correspondence. Do not require fabricated defects.
7. HANDOFF: deliver final playable video, three source images, storyboard, journal and cost/time record.

### Acceptance criteria
- Playable video link/file; not a screenshot.
- Three scenes match approved storyboard; duration 13–17 seconds; aspect ratio 9:16.
- Product identity/logo/packaging text are inspected against the original. Any visible distortion is recorded; no unsupported claim may be introduced.
- DOC-035 contains reproducible evidence for each operation, model/provider/version, time and approval.
- Independent QA report includes checks performed, evidence, defects if any, remediation and final disposition.
- API spend = 0 VND; elapsed time in minutes, human interventions and redo count are recorded.
- Any paid or payment-card-gated operation is prohibited. A blocked workflow is an honest result, not a PASS.

### Fixed constraints
- API budget: 0 VND.
- Deadline: 2026-11-25 (7 calendar days from approval date 2026-11-18).
- Provider status: RESEARCH ONLY; no provider selected.
- Excluded: public MCP, registration/tiering, billing, production backend, public release, new AI agents and unrelated feature expansion.
- Storyboard approval is mandatory before generating images/video. No generation is authorized by this roadmap update alone.

### Provider research — preliminary, not a selection
- Pollinations documentation describes image and video API endpoints, but generation requests require a secret key and account-specific Pollen/payment or user-authorized usage flows; do not assume API calls are free. Verify live model pricing and account balance/limits before any call. (Docs: https://gen.pollinations.ai/docs)
- Cloudflare Workers AI documents a 10,000-Neuron/day free allocation on Workers Free, with overage failing unless upgraded; model-specific restrictions apply. It may be considered for image generation only after confirming the exact model is available within the free allocation. It does not establish a complete free video pipeline. (Docs: https://developers.cloudflare.com/workers-ai/platform/pricing/)
- Wan2.2 provides open image-to-video weights, including TI2V-5B at 720p/24fps, but official documentation identifies consumer GPU requirements (e.g. RTX 4090 for the 5B path). It is a local-compute candidate only after hardware verification; local electricity/time are not API charges but must be disclosed as operational cost. (Repo: https://github.com/Wan-Video/Wan2.2)
- Conclusion: NO END-TO-END ZERO-COST PROVIDER/COMPUTE PATH VERIFIED YET. No API request or model download is authorized merely by this research note.

### Pilot status
- Founder authorization: PASS.
- Storyboard approval: PENDING.
- Provider/compute feasibility: BLOCKED / NOT VERIFIED.
- Generation: NOT STARTED.
- QA: NOT RUN.
- Handoff: NOT READY.


## Sponsor amendment — research/storyboard restrictions and outcome classes (2026-11-18)

### Before storyboard approval — RESEARCH ONLY
1. Cloudflare Workers AI: produce a model-by-model evidence table from official docs showing model name, task support, Free allocation/quota, card/payment requirement, restrictions and source link. Mark each model USE-ELIGIBLE / UNVERIFIED / BLOCKED. Do not call any API.
2. Pollinations: presume prohibited unless the exact API route is proven to be fully no-cost with no Pollen purchase, BYOP key, payment method or paid trial. No API call.
3. Wan 2.2: ask Vinh for CPU/GPU/RAM/free disk and verify against official requirements. No inference about his hardware; no downloads or installations.
4. Prepare a blank three-scene storyboard template only. No stock imagery, AI demo imagery or substitute product image. Each scene must specify camera angle, lighting, action and on-screen text. Wait for the real product photo and explicit Vinh + Sponsor approval.
5. No image/video API call or local generation of any kind before storyboard approval, including nominally free endpoints. No personal API keys and no card-required trials.

### Acceptance outcome classes
- PASS: playable 15-second final video and all six original Sponsor acceptance criteria satisfied.
- PARTIAL PASS: approved storyboard + documented test of at least one verified free provider after approval + playable 5-second one-scene demo + evidence-based BLOCKED explanation for the other two scenes under the 0 VND ceiling.
- FAIL: evidence absent; paid API used without authorization; fabricated/substituted product image used; or completion claimed without a playable video link/file.

QA must report actual defects, not manufacture one. A no-defect result is valid only with reproducible inspection evidence.

### W500 integration boundary
Work 500 is a candidate orchestration/model-routing layer only. Its demo, agent flow or UI screenshot does not prove image or video generation. W500 integration is outside this Pilot until a focused technical review establishes a working, no-cost-compatible provider adapter and Vinh approves a scope change.

The Sponsor's acceptance amendment does not relax the storyboard approval gate, 0 VND ceiling or 2026-11-25 deadline.


---

## 2026-11-19 — Current roadmap correction: W300 image/photo only
This current section supersedes the earlier video-oriented W300 pilot and roadmap items where they conflict. Video generation, image-to-video, storyboard-to-video and video assembly belong to Work 29, not W300.

### Phase 01 — Discovery / review (current)
1. Confirm image/photo-only scope — recorded in DOC-003 D300-005.
2. Preserve the existing dashboard source as LEGACY / NOT VERIFIED; do not treat it as the accepted current product UI.
3. Obtain independent reviews from Ka, Cla, Kha, Go, Qw and Nu if available.
4. Reconcile reviewer findings into the single canonical DOC-034.
5. Obtain Vinh's decision on the final architecture and explicit build gate.

### Phase 02 — Design (gated)
1. Finalize image task contracts and provider-agnostic adapter interface.
2. Define local/cloud data flow, explicit consent and image provenance.
3. Define input/output formats, dimensions, size limits and metadata.
4. Define quota, cost and paid-overage fail-closed controls.
5. Define retention/deletion, region, rights and secret-handling policies.
6. Finalize quality rubric and objective file/image validation.

### Phase 03 — Build (NOT AUTHORIZED)
1. Start with deterministic local utilities after architecture approval.
2. Add text-to-image and image-editing adapters only after account/quota/terms checks and explicit build authorization.
3. Keep provider integrations replaceable; do not build public MCP or video functions in W300.

### Phase 04 — Verify
- Unit/integration tests for local utilities and provider adapters.
- File validity, metadata/hash, dimensions and format checks.
- Independent visual quality review, privacy/security checks and quota/overage verification.
- Record every result in DOC-035 with method, evidence and PASS/FAIL/BLOCKED.

### Current gates
- Image/photo scope: DOCUMENTED.
- Provider candidates/pricing: DOCUMENTED; account access/quota/retention/rights not verified.
- Architecture/security review: PENDING.
- Independent QE review: PENDING.
- Build: NOT AUTHORIZED.
- Provider calls/image uploads: NOT RUN.
- E2E/product acceptance: NOT RUN.
- Video and public MCP: EXCLUDED from current W300 scope.


---

> **SCOPE CONTROL NOTICE — 2026-11-19:** W300 is image/photo only. Earlier video-generation, image-to-video, video assembly and public-MCP items in this roadmap are historical/superseded and are not active W300 scope. Video belongs to Work 29. Current review and build-gate status is governed by DOC-034 section 11. BUILD remains NOT AUTHORIZED.
