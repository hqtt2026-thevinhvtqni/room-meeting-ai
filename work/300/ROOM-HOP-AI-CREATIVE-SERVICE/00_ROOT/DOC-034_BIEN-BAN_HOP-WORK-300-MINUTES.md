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


---

# 11. INDEPENDENT REVIEW CONSOLIDATION — PILOT 01 (2026-11-19)
**Status: REVIEW IN PROGRESS / APPROVE WITH CONDITIONS / ARCHITECTURE NOT FROZEN / BUILD NOT AUTHORIZED**

## 11.1 Evidence and reviewer status
This section consolidates reviewer reports supplied to Xu and the Cla report read back from Sandbox Work 300. A report is not treated as an independent runtime test. No provider call, account inspection, image upload, billing operation or code execution is evidenced in this review round.

| Reviewer | Scope | Result received | Evidence location / qualification |
|---|---|---|---|
| Ka / AI-02 | Architecture, security, privacy | APPROVE WITH CONDITIONS; 8 findings KAI-300-01…08 | Reported in GitHub DOC-035 Entry 015; reviewer reports GitHub readback. |
| Cla / AI-03 | API contract, technical architecture, local processing | APPROVE WITH CONDITIONS; 8 findings CLA-300-01…08 | Sandbox `TRAO-DOI-VA-GIOI-THIEU/03_ARCHITECTURE/CLA_REVIEW_PILOT_01.md`, readback 16,796 bytes. |
| Kha / AI-04 | Product strategy/provider selection | Recommendations received; no final approval verdict stated in supplied report | User-forwarded review text; no canonical reviewer file/commit supplied. |
| Go / AI-06 | Free quota, overage and cost controls | APPROVE WITH CONDITIONS; 6 findings | User-forwarded review text; no canonical reviewer file/commit supplied. |
| Nu / Manus | Independent feasibility | NOT COUNTED as completed review | Supplied note only confirms a synchronization/status check; no technical findings or verified runtime identity. |
| Qw / AI-05 | Independent QE | PENDING | No review report received. |

## 11.2 Consolidated findings register
### P1 — Must resolve before any BUILD authorization
1. **Model contract / steps (KAI-300-02, CLA-300-01):** The packet's illustrative 20-step FLUX.1 schnell cost example is invalid according to the reviewers' cited model schema. Ka and Cla report default 4 steps and maximum 8. Correct the estimate and pin the exact model request/response schema, document date and model version. Validate prompt length and reject unsupported fields. Output dimensions/format must be measured from returned bytes, not assumed.
2. **FLUX.2 klein workflow naming and limitations (CLA-300-02, Go Finding 3):** Do not describe the candidate as guaranteed source-preserving photo editing or mask/inpaint. Cla reports a reference-conditioned image-to-image contract, up to four reference images, no mask, and input-size constraints that remain partly ASSUMED for klein 4B. Rename P300-02 to reference-conditioned image generation/editing; explicitly state that pixel/layout preservation is not guaranteed. Keep this model out of the initial pilot until its exact model-specific schema and price are independently pinned.
3. **Zero-spend gate (KAI-300-03, CLA-300-03, Go Findings 1–4, 6):** A three-request cap is only a smoke-test bound, not proof of zero spend. Before any cloud call, verify account plan is Workers Free, payment method/paid overage is not enabled, the exact model is available on Free, and quota is visible. If any check is unavailable or a model requires Paid, mark BLOCKED and do not upgrade. Add a deterministic pre-flight estimator with conservative tile rounding, a daily pilot budget/buffer, one job at a time, no automatic retry, and stop-all on quota/unknown error. Treat timeout as potentially consumed until reconciled. Capture dashboard usage before/after a permitted call. The 10,000 Neurons/day allocation and per-model prices remain public-document figures until account evidence is recorded.
4. **Job lifecycle and duplicate spend (CLA-300-04):** Specify CREATED → VALIDATED → APPROVED → SUBMITTED → SUCCEEDED / FAILED / BLOCKED, single-flight admission, duplicate-job prevention, explicit timeout semantics, no automatic retry and no async queue for Pilot 01. Any unknown error fails closed.
5. **Local-first prerequisite (CLA-300-05, Go Finding 5):** Implement and pass local deterministic image utilities before cloud adapters. Keep the implementation lightweight for the reported HP EliteBook 840 G3 constraints; first verify current device measurements rather than treating the historical hardware note as current. Include safe decode, byte/pixel limits, magic-byte format detection, EXIF orientation, metadata/GPS removal policy, resize/crop/convert, SHA-256 and atomic writes.
6. **Security, privacy, rights and retention (KAI-300-04, 06, 08; CLA-300-06):** Complete data-flow/trust-boundary diagram and threat model; define image rights/consent, cloud-transfer approval, retention/deletion, logging, metadata and secret handling. Do not log prompts/base64/image URLs/tokens; remove GPS/EXIF from exported outputs by default unless the owner explicitly approves another policy.
7. **Technical acceptance and quality (KAI-300-07, CLA-300-07):** Keep human visual rubric but add objective gates: successful decode, expected dimensions/format from actual bytes, non-empty/non-uniform image checks, metadata/hash manifest and critical-defect veto. A mean score cannot override a critical failure.
8. **Canonical source/path ambiguity (CLA-300-08):** Publish one path map distinguishing Work ID, Sandbox runtime folder, product identity and GitHub canonical root. GitHub main is the canonical record location; Sandbox remains working/evidence mirror. Do not claim all Sandbox files are synchronized until explicitly compared.

### P2 — Resolve in design or before cross-Work integration
9. **Provenance manifest (CLA-300-06):** Define versioned per-job manifest with input/output hashes, dimensions, detected formats, byte sizes, rights/consent reference, transforms, provider/model, contract date, parameter record, estimated/actual usage, request/status/latency, retry count, QC and terms snapshot reference. Never store secrets or base64.
10. **Cross-Work data contract (Kha):** Kha proposes a shared schema/DTO for possible future W300-to-Work-29 image handoff. Treat this as a future interoperability recommendation, not a dependency or scope expansion. Define only a minimal export metadata contract now; do not couple W300 build to video or implement Image-to-Video.
11. **Legacy dashboard isolation (Kha):** Kha recommends moving legacy dashboard to an archive branch or read-only area outside build scope. Decision: preserve current source untouched and mark it LEGACY / NOT VERIFIED. No physical move, branch migration or deletion until impact/dependency review and explicit authorization; a clear build exclusion and dependency boundary is required first.

## 11.3 Provider and pilot decision
- **FLUX.1 schnell:** retain as the only first cloud candidate, conditional on model contract correction, Workers Free eligibility and zero-spend controls. Use the documented default of 4 steps unless current official schema says otherwise; reject steps above the verified maximum.
- **FLUX.2 klein 4B:** defer from initial cloud pilot until exact schema, input constraints and pricing are independently verified. Do not label it source-preserving photo editing.
- **Local deterministic utilities:** first implementation and test target after BUILD gate; design and test specifications may continue now.
- **Stability AI and other providers:** remain conditional alternatives, not active dependencies.
- **No provider API call, image upload, paid use, billing activation or credential exchange is authorized by this review.**

## 11.4 Kha recommendations — disposition
- Prefer FLUX.1 schnell for a bounded PoC: ACCEPT AS CONDITIONAL CANDIDATE, not final model approval.
- Consider FLUX.2 klein 4B as later benchmark: ACCEPT DEFERMENT.
- Prepare a minimal output metadata/DTO for possible future Work 29 interoperability: ACCEPT FOR DESIGN ONLY; no video scope in W300.
- Physically isolate legacy dashboard: DEFER pending dependency/impact assessment; preserve source in place and exclude it from current build.

## 11.5 Gate decision by Xu / AI-01
**DECISION: APPROVE WITH CONDITIONS FOR DOCUMENTATION / RESEARCH / DESIGN ONLY.**
- Architecture freeze: NOT APPROVED.
- Product code/provider adapter: NOT AUTHORIZED.
- Cloud/API test: NOT AUTHORIZED.
- Billing/payment changes: NOT AUTHORIZED.
- BUILD gate: CLOSED.

Conditions to return for owner decision: resolve P1 items 1–8, receive Qw independent QE review, obtain any outstanding Kha/Go reports as canonical artifacts if required, verify provider terms/account/quota and current hardware evidence, then present one reconciled decision in this DOC-034. Vinh retains final authority to open BUILD.
