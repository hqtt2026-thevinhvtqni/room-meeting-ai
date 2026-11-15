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
