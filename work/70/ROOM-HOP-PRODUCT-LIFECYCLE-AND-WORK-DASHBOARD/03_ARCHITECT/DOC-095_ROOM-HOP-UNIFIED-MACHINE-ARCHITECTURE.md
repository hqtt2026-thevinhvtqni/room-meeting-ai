# DOC-095 — KIẾN TRÚC TỔNG THỂ BỘ MÁY ROOM-HOP
- Document ID: DOC-095
- Priority: P0
- Status: DESIGN BASELINE — IMPLEMENTATION NOT AUTHORIZED
- Owner: Xu / xu
- Authority: Vinh
- Date: 2026-11-09
## 1. Quyết định kiến trúc
ROOM-HOP là MỘT BỘ MÁY THỐNG NHẤT. W70 là đầu não điều phối và kiểm soát. Các Work còn lại là phân hệ/năng lực được tích hợp; Agent là thành phần tham gia theo vai trò, quyền và năng lực đã xác minh, không phải các bộ máy độc lập.
## 2. Phân hệ và ranh giới trách nhiệm
- W70: Control Plane — lifecycle, Work/WP/Task orchestration, assignment, authority, gate, decision, dashboard projection và kiểm soát bằng chứng.
- W32: Quality/CI Engine — pipeline, test execution, artifact, quality gate và kết quả kiểm thử dùng chung.
- W1111: Technical Engineering & Debug Lab — điều tra, sửa lỗi và kỹ thuật nền tảng.
- W0000: Governance Registry — danh mục Work, governance, AI roster/identity và quyền.
- W21: AI Skills — năng lực/skill của Agent.
- W33: Shared File & Evidence Hub — dịch vụ lưu/chia sẻ evidence; chưa mặc định đã tích hợp hoặc đạt runtime acceptance.
- W52: Universal AI Communication & Orchestration — miền giao tiếp/điều phối AI; cần đối chiếu contract với W70.
- W16: Workflow Engine — workflow execution; cần xác định ranh giới với lifecycle authority của W70.
- W51: Coder-Tester orchestration — consumer/adapter theo hợp đồng, không thay thế W70.
- W39: Build MCP 8030 service/tooling ownership.
- W37: Core 8000 ownership.
- W38: Gateway 8040 ownership.
- W14: Autonomous E2E Builder / canonical execution-host integration owner theo disposition đã ghi nhận.
- W112: Cross-Work Integration Contracts & Evidence Orchestration — hợp đồng tích hợp liên phân hệ, dependency graph, event/evidence correlation, idempotency, consistency, integration test orchestration và gap ownership. Không sở hữu lại các component trên.
## 3. Nguyên tắc dữ liệu
GitHub main là nguồn mã chuẩn; Sandbox/MCP là vùng làm việc và kiểm chứng. Mọi trạng thái phải truy nguyên tới Work, Task, Agent identity, source revision/commit SHA, test run, artifact/evidence và timestamp. Journal là lịch sử nghiệp vụ chính thức; Dashboard là projection, không phải nguồn sự thật.
## 4. Agent là thành phần của máy
Agent chỉ nhận việc sau khi xác minh identity, capability, permission, scope và session. QE độc lập với coder; Agent không tự nâng gate/acceptance. Một Agent có thể tham gia nhiều Work/Task khi dependency, lock và quyền cho phép.
## 5. Phát triển song song
Các phân hệ phát triển song song theo contract-first. Chỉ tích hợp khi interface contract, owner, test harness, evidence schema và compatibility version được công bố. Dependency có trạng thái READY/BLOCKED/NOT_VERIFIED kèm bằng chứng.
## 6. Gates cấp hệ thống
S0 inventory/ownership; S1 contracts approved; S2 component tests; S3 integration tests; S4 concurrency/idempotency/recovery/security; S5 independent QE; S6 Founder acceptance. PASS chỉ khi có bằng chứng tái lập. Chưa chạy là NOT RUN, thiếu căn cứ là NOT VERIFIED.
## 7. Phạm vi chưa được xác nhận
Runtime dispatch, event delivery, evidence parity, multi-agent concurrency, recovery, cross-work dashboard live data, CI trigger from task lifecycle và QE independence enforcement chưa được xác minh đầy đủ. Không tuyên bố bộ máy hoàn thành trước khi các phép thử PASS.


## 8. Retrieval capability architecture addendum — 2026-11-11
- Retrieval is a pluggable capability, not a second Core/control plane. ROOM-HOP may support lexical, dense-vector, hybrid, reranking, hierarchical/DecisionRAG and graph strategies behind a common evidence-result contract.
- Strategy outputs must preserve source ID, document revision, exact locator/span, chunk/node ID, retrieval trace, access decision, timestamp and abstention metadata. Generation receives only authorized, traceable evidence.
- DecisionRAG is a research candidate only. It does not replace the current Work 103 baseline or authorize production implementation. See DOC-096 and Work 103 `03_ARCHITECTURE/DECISIONRAG_RETRIEVAL_EXPERIMENT_PLAN_20261111.md`.
- No retrieval strategy is selected on R@1 alone; evaluate recall/ranking, false abstention, unsupported-answer/leak rate, permission violations, provenance, pruning misses, p50/p95 latency, token/cost and reproducibility.
- Architecture status: design direction recorded; implementation, benchmark and production adoption NOT AUTHORIZED / NOT VERIFIED.


## 9. Ownership baseline — Framework / Agent Orchestration / Workflow / RAG (D70-023, 2026-11-13)
- **W70 — Work Control Plane:** Work lifecycle, WP governance, phase gates, evidence policy, dashboards and cross-Work governance.
- **W52 — Agent Orchestration:** provider-neutral Agent-to-Agent task/event contracts, provider adapters, capability negotiation, dispatch/ACK semantics and agent/task lifecycle transitions.
- **W16 — Workflow Engine:** deterministic workflow graph and step semantics, schema/validation/compile, sequencing, workflow-level timeout/retry/cancel and run persistence requirements.
- **W103 — Retrieval Capability:** source-aware ingestion/indexing, retrieval/ranking, evidence packaging, abstention and retrieval evaluation. It is not generic Agent Runtime or decision authority.
- **W112 — Integration Contracts:** cross-Work contracts, mappings, integration evidence and test coordination; not a competing control plane.
- **W37:** Core source of truth. **W14:** execution boundary/host. **W32:** CI. **W33:** Evidence Hub. **W38:** Gateway. **W39:** Build MCP.

**Boundary rules:**
1. Work lifecycle orchestration (W70), Agent task/event orchestration (W52) and deterministic workflow execution (W16) are distinct responsibilities and must not be collapsed.
2. W16 consumes W52 task contracts where needed; W52 does not become a workflow engine. W52/W16 cannot bypass Core authority or W14 execution grants.
3. W103 returns traceable evidence only. Retrieved content is untrusted data, not executable instruction or authority.
4. Durable scheduler/queue ownership, outbox/idempotency and retry division between W52 delivery and W16 workflow steps remain unresolved contract items; no implementation until assigned, versioned and tested.
5. LangGraph, LangChain, CrewAI and similar libraries are implementation candidates, not separate ownership domains. Select only after requirements and benchmark.
6. DecisionRAG remains EXPERIMENT / NOT APPROVED under W103 until blind labeled evaluation, corpus/query snapshot/hash, false-abstention vs unsupported-answer/leak analysis, Precision@k, Recall@k, MRR, answerability/coverage, latency/cost and independent review are complete.

Status: architecture ownership baseline recorded under delegated authority D70-018 / decision D70-023. Independent review pending; no implementation, migration, acceptance or release approval implied.
