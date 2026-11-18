# DOC-034 — BIÊN BẢN / W300 MINUTES

- Work: W300 — ROOM-HOP AI Creative Service
- Date: 2026-11-15
- Status: DRAFT — NOT FINAL ARCHITECTURE APPROVAL
- Chair: Xu / AI-01
- Authority: Vinh

## 1. User-confirmed product direction
W300 is intended to provide both image and video creative services. The intended access model is a public MCP endpoint, with registration/onboarding and usage tiers to be designed subsequently.

## 2. Source-code direction
Vinh instructed that W300 be synchronized to GitHub and built in Git. The canonical repository is hqtt2026-thevinhvtqni/room-meeting-ai, branch main, under work/300/ROOM-HOP-AI-CREATIVE-SERVICE/.

## 3. Current UI prototype boundary
The Lovable project is an isolated UI prototype. Demo jobs and sample data are not real production records. No real provider, customer database, storage, payment, job queue or public MCP gateway is connected.

## 4. Open review items
- Ka / AI-02: public MCP security, identity, tenant isolation, abuse and data protection.
- Cla / AI-03: service architecture, provider adapters, asynchronous jobs, retry/idempotency and operational feasibility.
- Kha / AI-04: customer journey, product tiers and service requirements.
- Go / AI-06: cost controls, quotas and unit economics.
- QE: acceptance criteria and independent verification (Cla/Ka may cover canonical QE if Qw is unavailable, subject to explicit assignment).

## 5. Decision boundary
This draft records scope and source location only. It does not reconcile reviewer opinions and does not approve the production architecture, backend implementation or public release. DOC-034 must be finalized after independent reviews and Vinh's approval.


## 6. Founder decision — W300-PILOT (2026-11-18)
**Status: APPROVED BOUNDED PILOT; NOT production architecture approval.**

Vinh approved the single workflow proposed by the Product Sponsor, with the following binding constraints:
- One supplied product image → three-scene storyboard → three generated scene images → three 5-second image-to-video clips → one assembled 15-second (±2 seconds) vertical 9:16 advertisement.
- Pilot audience hypothesis: small product shops / brands in Vietnam; this does not establish final market segmentation.
- Budget ceiling: 0 VND API spend. No paid calls, paid trials, subscriptions, card activation, automatic top-ups or other chargeable use. Any unavailable step must be marked BLOCKED.
- Deadline: 7 calendar days from 2026-11-18; target 2026-11-25.
- Provider selection: research only, prioritizing genuinely no-cost resources. No provider is selected by this decision.
- Mandatory storyboard approval by Vinh/Mê before video generation.
- Independent QA must inspect and record actual findings. QA is not required to invent an error; a clean result is acceptable only with reproducible inspection evidence.
- Required job metrics: API spend (must be 0 VND), elapsed minutes, human interventions, redo count, model/provider/version and evidence references.
- Handoff: playable final video, three source images, storyboard, execution journal and cost/time record.

## 7. Pilot exclusions and decision boundary
Public MCP exposure, customer registration/tiering, billing, production backend, new AI-agent onboarding, commercial release and unrelated feature work are excluded. This pilot authorization does not supersede DOC-001 restrictions on architecture/security approval or authorize production services. Research, documentation, storyboard preparation and verified no-cost experimentation may proceed. Any step requiring paid compute/API, a payment method, a trial that can convert to paid, or unverified terms is BLOCKED pending a new explicit Founder decision.

## 8. Provider research status at decision time
No provider is selected. Public documentation reviewed indicates that hosted media APIs may require account keys and/or usage credits; free web access is not proof of free API access. Local open-weight video generation may avoid API charges but requires capable local GPU resources and a separate hardware feasibility check. Provider/compute decision remains OPEN.


## 9. Product Sponsor confirmation — research/storyboard phase and acceptance definitions (2026-11-18)
The Product Sponsor confirms the Founder-approved W300-PILOT constraints: 0 VND API budget; deadline 2026-11-25; no image/video generation or API invocation before the detailed storyboard receives explicit approval from both Vinh and the Product Sponsor.

### Provider research requirements
- Cloudflare Workers AI: verify model-by-model which image models are available under the Free allocation, daily quota/Neuron limits, account/card requirements and applicable restrictions. Cite official documentation; do not infer that a model is free merely because the platform has a Free tier.
- Pollinations: treat as NOT AUTHORIZED unless official terms prove the exact API route can be used without Pollen purchase, BYOP key, payment method, paid trial or other charge.
- Wan 2.2 local: do not declare feasibility until Vinh's actual CPU, GPU, RAM and free disk capacity are documented and compared with the exact model's official requirements. No model download or installation is authorized in this research phase.
- No personal API keys, paid trials or credit-card-gated trials. No API calls of any kind before storyboard approval.

### Storyboard preparation
Prepare a blank three-scene storyboard template only. Do not insert stock images, AI demo images or an unapproved product image. Each scene must specify camera angle, lighting, action and exact on-screen text. Product identity and claims must come only from the actual product photo and facts explicitly confirmed by Vinh.

### Pilot acceptance status definitions
- PASS: playable final 15-second video and all six quantitative acceptance criteria from the original Sponsor review are met, including three-scene coverage, 9:16 aspect ratio, product integrity, complete evidence, independent QA and measured cost/time.
- PARTIAL PASS: approved storyboard exists; at least one provider has been tested with documented proof of genuinely free use after storyboard approval; one playable 5-second single-scene demo exists; and the remaining two scenes are explicitly BLOCKED with evidence explaining why they cannot be completed at 0 VND. This is a valid partial outcome, not full product acceptance.
- FAIL: no supporting evidence; unauthorized paid API use; fabricated/substituted product image; or claiming completion without a playable video link/file.
- QA must report actual findings. QA is not required to invent a defect; absence of defects is acceptable only with reproducible inspection evidence.

These definitions do not authorize BUILD before storyboard approval and do not change the 0 VND ceiling.

### Work 500 relationship
Work 500 (LLM HUB) may be evaluated as a possible orchestration/model-routing layer, but its demo or agent orchestration is not evidence of image-generation or image-to-video capability. No W500 integration is included in W300-PILOT until a focused technical review verifies a concrete adapter/provider contract and the Founder approves any scope change.


## 10. Founder scope correction — W300 image/photo only (2026-11-19)
**CURRENT PRODUCT DIRECTION — supersedes earlier video-oriented W300 scope and pilot where they conflict.**

Vinh clarified that Work 300 is for image processing, photo editing/enhancement, AI image creation and Photo AI. Work 29 remains the separate HQTT AI Video Studio.

- Remove video generation, image-to-video, storyboard-to-video and video assembly from W300's active product scope.
- The earlier 15-second video-ad pilot recorded in D300-004 remains historical evidence only; it is superseded for W300 and must not drive current implementation.
- The previous public MCP direction is not part of the current W300 baseline and is not authorized by this correction.
- Preserve the existing Lovable UI source snapshot in GitHub for auditability, but label it LEGACY / NOT VERIFIED. Do not delete it or treat it as the current product.
- Current review target: AI Image & Photo Studio architecture and bounded zero-cash image pilot covering text-to-image, image editing and local deterministic image utilities.
- Cloudflare FLUX.1 schnell and FLUX.2 klein 4B are candidates documented in the review packet, not account-verified or experimentally validated.
- No provider calls, image uploads, paid activity, billing activation or product code before review reconciliation and an explicit build-gate decision.
- Requested reviewers: Ka (architecture/security), Cla (technical architecture/API), Kha (product/provider strategy), Go (cost controls), Qw (independent QE), and Nu (Manus) for independent research if available.
- This is a scope correction, not final architecture approval. DOC-034 remains DRAFT until reviewer findings are reconciled and Vinh approves the final decision.
