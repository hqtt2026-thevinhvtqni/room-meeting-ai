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


---

## REVIEW ADDENDUM — corrections after independent review (2026-11-19)
This addendum supersedes conflicting examples/labels earlier in this packet. See canonical DOC-034 section 11 for the consolidated decision.

### FLUX.1 schnell
- Do not use the earlier illustrative 20-step example. Ka and Cla report the official model schema default is 4 steps and maximum is 8. The exact schema must be pinned to a dated official model page before implementation.
- The earlier estimate of 196.8 Neurons for 20 steps is invalid for this model and is withdrawn.
- A provisional arithmetic example based on the published pricing formula, one 512×512 tile and 4 steps, is 4.80 + (4 × 9.60) = 43.2 Neurons. This is a calculation from published rates, not measured usage; tile rounding and actual account metering remain to be verified.

### FLUX.2 klein 4B
- Do not describe this candidate as guaranteed source-preserving photo editing, mask editing or inpainting.
- Cla's review characterizes the documented workflow as reference-conditioned image generation; exact klein-specific input limits and steps contain unresolved documentation discrepancies. Treat any assumed limit as UNKNOWN until the exact official model page/changelog confirms it.
- Defer this model from Pilot 01 cloud calls until the model-specific request/response schema, image limits and pricing are independently pinned. It is not required to pass the initial pilot.

### Zero-spend hard gates
- A maximum of three requests is only a smoke-test cap, not proof of zero cost.
- Before any cloud request: verify Workers Free plan, no Paid upgrade/payment method/auto-recharge, exact model eligibility on Free, visible remaining free quota, and a conservative preflight cost estimate with buffer.
- If any fact is unavailable, a model requires Paid, or any quota/unknown error occurs: BLOCK and stop; never upgrade, retry automatically or submit a second job concurrently.
- Treat timeout as potentially billable/consumed until usage is reconciled. Capture account usage before and after any separately authorized call.
- No cloud request is authorized by this addendum.

### Local-first prerequisite
- Local image inspection, safe decode, dimensions/pixel/byte limits, magic-byte format detection, EXIF orientation, metadata/GPS policy, resize/crop/convert, SHA-256, thumbnails and atomic output handling must be specified and tested before any cloud adapter.
- Keep dependencies lightweight. Re-measure the target PC before using historical hardware figures as current facts.

### P300-02 wording
Rename the candidate workflow to **reference-conditioned image generation/editing**. Explicitly state that source pixel/layout preservation is not guaranteed. Local deterministic transformations remain separate from generative editing.

### Evidence status
All model schema and pricing observations above are attributed to reviewer static research. They are not account-level or experimentally verified measurements. Architecture remains unfrozen; BUILD and provider calls remain unauthorized.


---

## CROSS-WORK INTEROPERABILITY NOTE — KHA REVIEW (2026-11-19)
Kha's static review concludes that deferring FLUX.2 klein 4B does not block future W300↔W29 interoperability. A model-neutral, versioned image artifact contract is proposed. Candidate mandatory fields: `contract_version`, `asset_id`, `artifact_uri`, `media_type`, `width_px`, `height_px`, `created_at`. Recommended integrity/provenance fields: `sha256`, `byte_size`, rights/consent reference, task/provider/model/version, prompt reference, seed where supported, QC status and metadata policy. Other fields remain optional.

**Not frozen / not an integration requirement:** W117 is a secondary audit, not W29's original source tree. Inspect W29's real DTO/import path, validation/error handling, file and batch limits, authorization and storage lifecycle before freezing the contract. Use a storage-neutral authorized artifact URI; do not assume local absolute paths or public URLs. W300 must not call W29 internals and must remain image/photo-only. See DOC-034 section 12 and DOC-035 Entry 020.


---

## QE ADDENDUM — Qw review and mandatory fatal vetoes (2026-11-19)

### Neurons terminology correction
Cloudflare Workers AI Neurons are the platform usage-meter unit used in pricing; they are not FLOPs, VRAM or a direct hardware-performance metric. The provisional 43.2 value (one 512×512 tile, four steps) is arithmetic from published rates only, not measured consumption. Do not describe it as an estimate of FLOPs/VRAM or as actual billed usage.

### Circuit Breaker — mandatory design requirements (not implemented)
- One centralized gateway is the only route to provider network calls.
- Persistently and atomically reserve/count submissions across process restarts and concurrent workers; cap the entire Pilot 01 at three submissions, not merely three per process/session.
- Require an explicit budget-enable flag and verified zero-spend account gate. Missing/corrupt/unavailable state, zero budget or unknown budget fails closed before network dispatch.
- Reserve the count before dispatch; no automatic retry, no duplicate submission, one in-flight job at a time. A timeout is UNKNOWN/POTENTIALLY CONSUMED and must not release the reservation until usage is reconciled.
- Local image validation (byte signature, decode, format, byte/pixel/dimension limits) must pass before any cloud transfer. Fail locally with stable error codes.

### Fatal vetoes
1. FATAL-01: more than three pilot submissions, any automatic retry/duplicate, or any submission while cost gate is closed.
2. FATAL-02: wrong execution boundary, verified runtime resource/time limit breach, or unsafe retry after ambiguous timeout. Pin exact product/plan/execution-mode limits; do not copy generic CPU figures. Local Python processing does not use Worker CPU unless executed in the Worker.
3. FATAL-03: local OOM/resource exhaustion due to unbounded image decode/allocation; enforce safe limits before allocation.
4. FATAL-04: HTTP 200 with error payload, malformed/empty/non-image response, failed decode, zero-byte output or metadata mismatch is never SUCCEEDED.

These are design/acceptance requirements only. No implementation or API call is authorized. See DOC-034 sections 12–13 and DOC-035 Entries 020–021.
