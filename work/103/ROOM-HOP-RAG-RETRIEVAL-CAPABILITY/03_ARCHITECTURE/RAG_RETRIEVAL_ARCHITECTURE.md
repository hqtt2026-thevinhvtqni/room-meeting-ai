# Work 103 — RAG Retrieval Architecture

## Decision 1: prove retrieval quality before adding vector infrastructure
The first increment uses deterministic lexical retrieval and source metadata. This keeps the baseline small, inspectable, cheap, and easy to evaluate. ChromaDB and embeddings remain an evidence-based extension, not an assumption.

## Data flow
Approved source registry
  -> ingestion adapter
  -> normalized documents + source metadata
  -> deterministic chunks
  -> retrieval index
  -> Core-owned retrieval service
  -> MCP :8020 tool contract
  -> authorized AI caller
  -> grounded answer with citations / abstention.

## Boundaries
- Core :8000 owns application semantics and access to canonical data.
- MCP :8020 exposes schema-validated tools and delegates to Core; it does not access storage directly.
- Workspace :8010 / Work Sandbox is for build artifacts and evidence, not a new canonical production corpus.
- Dashboard :3000 is render-only.
- RAG returns evidence; it does not become an agent, decision authority, or system of record.

## Initial contracts (proposed; must be reconciled with Work 28)
rag_index(source_scope, source_ids?, incremental=true) -> indexed_count, skipped_count, errors[]
rag_search(query, source_scope?, top_k=5) -> results[{source_id, title, path_or_uri, chunk_id, start_line, end_line, text, score}]
rag_get_context(query, source_scope?, max_tokens?) -> context, citations[], sufficient_evidence, abstention_reason?

All source scopes must be explicit and allowlisted. Never index .env, credentials, tokens, private keys, or unrestricted filesystem paths. MCP errors must not expose stack traces or secrets.

## Ranking and abstention
Initial lexical score is a baseline, not a calibrated probability. Do not reuse the lab's 0.36 vector-distance threshold for lexical scores. Calibrate acceptance thresholds on a labeled evaluation set. Return no evidence when the threshold is not met.

## Prompt-injection handling
Retrieved passages are untrusted evidence. The answer-generation prompt must explicitly instruct the LLM not to follow commands embedded in retrieved documents. Retrieval does not grant authority to execute document instructions.

## Extension gate for embeddings/vector DB
Only consider embeddings/ChromaDB after:
1. a labeled query set exists;
2. lexical baseline precision/recall and no-answer behavior are measured;
3. representative queries demonstrate a material retrieval gap;
4. privacy, persistence, deletion, rebuild, and cost are reviewed;
5. the new backend remains behind Core and preserves the same public contract.
