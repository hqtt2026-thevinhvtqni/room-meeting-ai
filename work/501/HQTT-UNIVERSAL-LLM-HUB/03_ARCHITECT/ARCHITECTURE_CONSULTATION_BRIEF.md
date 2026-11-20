# HỒ SƠ PHẢN BIỆN KIẾN TRÚC — WORK 501
- Consultation ID: W501-CONSULT-001 | Date: 2026-11-17
- Status: PREPARED; DISPATCH/ACK NOT VERIFIED
- Target: Architecture Proposal v0.1
## Bối cảnh và quyết định cố định
Vinh chốt LOCAL FIRST; GLOBAL CONTROL; MODEL ARENA = YES; ZERO-COST FIRST. Không paid API/billing/payment/billable resource nếu chưa phê duyệt riêng. Work đang ở giai đoạn thiết kế; BUILD chưa được phép. Core/Gateway/Agent Runtime giữ đúng thẩm quyền hiện hữu. Hardware chưa có dữ liệu xác minh. LiteLLM/Ollama/llama.cpp chỉ là ứng viên.
## Câu hỏi chung
1. Giả định nào chưa có bằng chứng hoặc sai về kỹ thuật?
2. Work/thành phần ROOM-HOP nào đã sở hữu chức năng tương tự?
3. Trust boundary và failure mode nguy hiểm nhất?
4. Nên reuse/extend/adopt/reject thành phần nào, vì sao?
5. Thiếu bằng chứng gì trước khi chốt kiến trúc?
6. Zero-cost có thể thất bại ở đâu (quota, overage, storage, bandwidth, electricity, account terms)?
7. Các increment nhỏ và an toàn sau khi được duyệt?
8. Nội dung nào phải loại khỏi BUILD?
## Nhiệm vụ theo reviewer
### Cla / AI-03 — Technical architecture
Review Core/Gateway/Runtime boundary, invocation contract, capability negotiation, local runtime, concurrency/queue/retry/timeout/fallback, LiteLLM overlap, API versioning and observability. Deliver corrected architecture, contracts, failure matrix and source evidence. No implementation.
### Ka / AI-02 — CSA/security/privacy
Challenge global control, paid deny, secrets, endpoint allowlist/SSRF, egress, prompt/response handling, cross-Agent isolation, model output/tool execution, provider retention, supply chain and audit integrity. Deliver threat scenarios, severity, mitigation, residual risks and mandatory gates. No implementation.
### Go / AI-06 — QE/QA (default HQTT owner under D70-026)
Review registry/policy correctness, capability mismatch, local/cloud fallback, quota exhaustion, paid-deny invariants, redaction, concurrency, audit failure, Arena partial failure, evaluator bias and reproducibility. Deliver test matrix, measurable acceptance thresholds and evidence requirements. No implementation.
### Go / AI-06 — local feasibility and cost
Use verified hardware facts only. Compare Ollama/llama.cpp/current environment; estimate CPU/GPU/RAM/VRAM/disk, throughput and concurrency; identify electricity, bandwidth, storage and overage risks. Do not install/download/create accounts/enable billing.
### Vibe — adversarial architecture challenge
Try to falsify proposal: duplicate gateway, vendor lock-in, local bottlenecks, Arena privacy/cost, false consensus, identity drift, audit gaps and simpler alternatives. Deliver dissent and rejection conditions.
### Kha — Gemini/provider and Work 23
Inspect Work 23 source/manifest and public provider constraints. Determine adapter reuse, API/model/version/quota/terms evidence and conditionality of free tier. No key creation or live calls.
### Qc — implementation feasibility, no code
Review adapter interfaces, schemas, error normalization, streaming, tool calls, structured output, multimodal support and test seams. Define minimum viable boundary. Do not write source.
### Gem — Agent operating model
Review model selection while retaining Agent identity/role/session; AUTO/MANUAL/MULTI-MODEL permissions; global controls and operator status explanations. Do not alter Agent registry.
## Required reviewer response
Verdict ACCEPT / ACCEPT WITH CONDITIONS / REVISE / REJECT. Numbered findings with severity and evidence; Work overlap/reuse; cost/privacy/security impact; required changes; open questions; BUILD blockers; objective exit criteria; reviewer identity/model/version/timestamp/source context. Unverified identity/source means UNVERIFIED and cannot count as independent review.
## Dispatch register
| Reviewer | Scope | Dispatch | ACK | Review |
|---|---|---|---|---|
| Cla / AI-03 | Technical | NOT VERIFIED | NOT VERIFIED | PENDING |
| Ka / AI-02 | Security/privacy | NOT VERIFIED | NOT VERIFIED | PENDING |
| Qw / AI-05 | QE | NOT VERIFIED | NOT VERIFIED | PENDING |
| Go / AI-06 | Local feasibility/cost | NOT VERIFIED | NOT VERIFIED | PENDING |
| Vibe | Adversarial | NOT VERIFIED | NOT VERIFIED | PENDING |
| Kha | Provider/Work 23 | NOT VERIFIED | NOT VERIFIED | PENDING |
| Qc | Adapter feasibility | NOT VERIFIED | NOT VERIFIED | PENDING |
| Gem | Agent operating model | NOT VERIFIED | NOT VERIFIED | PENDING |
## Reconciliation rule
Xu records each actual response in the canonical Minutes/Task Board/Journal, updates proposal and ADRs, and explains accepted/rejected findings. Conflicts remain open until evidence or Vinh decision resolves them. No BUILD before final design package and explicit approval.