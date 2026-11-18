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
