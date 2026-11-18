# W300 — PILOT-01 REVIEW PACKET: AI IMAGE & PHOTO STUDIO
Date: 2026-11-19
Status: DESIGN BASELINE / INDEPENDENT REVIEW REQUESTED / BUILD NOT AUTHORIZED

## 1. Confirmed product boundary
W300 is dedicated to image processing, photo editing/enhancement, AI image creation and Photo AI. Work 29 is the independent HQTT AI Video Studio. Video generation, image-to-video, storyboard-to-video, video assembly and public MCP exposure are excluded from current W300 scope. The previous W300 video pilot is historical and superseded.

The existing Lovable dashboard source in 05_BUILD/04_CODE/dashboard is preserved as a legacy UI prototype from the earlier scope. It is not accepted as the current image/photo product UI and must not be overwritten or assumed functional.

## 2. Product scope candidate
- Image creation from text and/or permitted reference images.
- Photo editing with requested changes and subject/layout preservation where feasible.
- Enhancement/restoration: upscale, denoise, sharpen.
- Background/composition: remove/replace background, outpaint, crop/expand and object removal where supported.
- Batch workflows, presets, history and export.
- Asset provenance: source/rights, model/provider, prompt/settings, timestamps, metadata and hashes.

Initial pilot candidates: text-to-image, image-to-image editing and local deterministic utilities (inspect dimensions/format, resize, crop, convert supported formats, thumbnails and SHA-256). This is a proposed scope, not build authorization.

## 3. Architecture baseline
Provider-agnostic orchestration; local-first where practical; explicit consent for cloud processing; fail closed when cost/quota/terms are unknown; traceable input/output artifacts; secrets never in source, prompts or journals.

Proposed components: Workspace; Job Orchestrator; Image Task Adapters; Local Processing Engine; Artifact Store; Quality Gate; Provider Registry. Security must cover image rights, explicit cloud transfer, region, retention/deletion, commercial terms and key handling.

## 4. Provider discovery
| Provider/model | Task | Public pricing/free allocation | Current state |
|---|---|---|---|
| Cloudflare Workers AI @cf/black-forest-labs/flux-1-schnell | Text-to-image | 10,000 Neurons/day free allocation; 4.80 Neurons per 512x512 tile + 9.60 per step | DOCUMENTED candidate; account/quota not verified |
| Cloudflare Workers AI @cf/black-forest-labs/flux-2-klein-4b | Image generation/editing | 5.37 Neurons per input 512x512 tile + 26.05 per output tile | DOCUMENTED candidate; account/quota not verified |
| Stability AI Stable Image API | Endpoint-dependent image tasks | Eligible new Google-sign-in accounts may receive 25 credits; endpoint cost varies | Conditional fallback; account not checked |
| Local deterministic tools | Inspect/resize/crop/convert/hash | No API fee; local CPU/storage required | Candidate; runtime tests not run |

Cloudflare one-tile FLUX.1 schnell at 20 steps is approximately 196.8 Neurons (4.8 + 20×9.6), about 50 requests within 10,000 Neurons if no other usage. Actual usage depends on parameters and metering. Free allocation is not unlimited; account and overage safeguards must be verified.

Official references:
- https://developers.cloudflare.com/workers-ai/models/
- https://developers.cloudflare.com/workers-ai/platform/pricing/
- https://www.cloudflare.com/products/workers-ai/
- https://platform.stability.ai/docs
- https://platform.stability.ai/docs/api-reference/
- https://platform.stability.ai/pricing

Other providers (Gemini Image, OpenAI Image, Adobe Firefly, fal.ai) remain comparison candidates only. UI free credits are not proof of API quota. Retention, ZDR, rights and regional terms require model/account-specific verification.

## 5. Zero-cash Pilot 01
Workflows:
1. Prompt → FLUX.1 schnell candidate → preview → QC → export.
2. Synthetic/licensed source + edit instruction → FLUX.2 klein 4B candidate → preview → QC → export.
3. Local deterministic image utilities.

Test assets:
- TEST-IMG-01 geometric still-life/product mockup.
- TEST-IMG-02 landscape.
- TEST-IMG-03 fictional illustrated portrait, not a real person.
Record source method, rights, dimensions, format and SHA-256.

Test matrix: P300-01 generation; P300-02 editing; P300-03 local utilities; P300-04 privacy/secrets/cost; P300-05 repeatability.

Proposed quality rubric (not yet approved): 0–5 for prompt/operation adherence, subject/structure consistency, visual defects (5=no material defects), detail/sharpness, color/composition, output validity/metadata. Proposed threshold average >=4.0/5, no critical defect, all privacy/secret/cost gates PASS.

Budget and safety:
- Target spend 0 VND.
- Maximum initial cloud batch 3 requests, only after account dashboard proves remaining free quota and paid-overage safeguards.
- No paid calls, paid trials, subscriptions, payment-method activation or auto-recharge.
- No personal/family/customer images; synthetic or licensed assets only.
- If quota/overage, retention, region or rights are unknown, no cloud call/upload.
- Never request/store API credentials in chat or Work files.

Exit criteria: one successful generation and one successful edit, or evidence-backed BLOCKED; local utility tests pass; outputs open and metadata/hash recorded; independent QE review recorded; provider/model/cost/quota/retention/region documented; DOC-035 has method, timestamp, evidence and status.

## 6. Acceptance criteria
| ID | Criterion | Verification | Status |
|---|---|---|---|
| AC-300-01 | W300 identity is image/photo only and separate from Work 29 | DOC-001/DOC-003 | DOCUMENTED; Sandbox folder metadata remains legacy |
| AC-300-02 | Provider matrix records model IDs, pricing/quota and evidence level | Official docs | PARTIAL; account terms/quota/retention open |
| AC-300-03 | No paid spend/overage | Account dashboard and billing controls | NOT RUN |
| AC-300-04 | Test assets have rights/provenance/dimensions/format/hash | Asset manifest | NOT RUN |
| AC-300-05 | Text-to-image E2E | P300-01 | NOT RUN |
| AC-300-06 | Image editing E2E | P300-02 | NOT RUN |
| AC-300-07 | Output validity | File validation | NOT RUN |
| AC-300-08 | Visual quality rubric | Independent QE | NOT RUN |
| AC-300-09 | No secret/PII leak; cloud route explicit | Security review and scan | NOT RUN |
| AC-300-10 | Reviews reconciled before code | Reviewer responses and DOC-034 | BLOCKED — responses pending |
| AC-300-11 | Local utilities tests | Unit tests | NOT RUN |

## 7. Review questions
1. Is the image-only boundary clear and consistent with Work 29?
2. Are the two FLUX model candidates suitable for first workflows?
3. What exact API schemas, dimensions, formats and limits must be pinned?
4. What input/output provenance metadata is mandatory?
5. What safeguards prove no paid overage can occur?
6. What retention/deletion/region and commercial-rights facts must be checked before upload?
7. Is the three-request cap sufficient? What stop conditions are missing?
8. Is the proposed rubric and >=4.0/5 threshold defensible? What objective checks are missing?
9. Which local operations should be implemented first?
10. What failure modes/security risks/acceptance gaps are missing?

## 8. Requested AI reviewer roles
- Ka / AI-02: architecture, security, privacy and data flow.
- Cla / AI-03: API contracts, technical architecture and local processing.
- Kha / AI-04: product workflows and provider alternatives.
- Go / AI-06: free quota, overage and cost controls.
- Qw / AI-05: independent QE and acceptance criteria.
- Nu / Manus: independent feasibility research if available.

For every finding: finding / evidence or source / severity / recommendation / acceptance test. Mark DOCUMENTED, ASSUMED, UNKNOWN or EXPERIMENTALLY VERIFIED. End with APPROVE, APPROVE WITH CONDITIONS or BLOCK.

## 9. Hard review boundary
No code, provider call, image upload, billing activation, paid use or credential exchange during review. Return findings to Xu/Vinh for reconciliation into the single canonical DOC-034. Review completion does not authorize build; explicit build-gate decision is required.
