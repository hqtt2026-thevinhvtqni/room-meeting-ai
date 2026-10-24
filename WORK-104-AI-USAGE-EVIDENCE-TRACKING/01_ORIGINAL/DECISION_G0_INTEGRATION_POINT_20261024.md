# W104-G0-006 — Decision: Integration Point
- Date: 2026-10-24 (UTC+7)
- Decision owner: Xu (AI-01 GPT CEO / architecture coordinator)
- Input evidence: `06_EVIDENCE/G0_DISCOVERY_INVENTORY_20261024.md` (blob SHA `764c352d32a4b38c62c352a6df71bb59fe9a6d44`)
- Decision status: **DECISION — direction approved for G1 design; not an implementation approval and not a G0 PASS.**

## Decision
Proceed to G1 design with a small in-process usage ledger module at the provider-response handling boundary, initially proposed as `core/usage_ledger.py`, emitting append-only JSONL events. Do not introduce a LiteLLM/FastAPI proxy for the first vertical slice.

## Alternatives considered
1. **Instrument provider-response handling points (selected for G1 design).** Reads usage fields where available and correlates the event with task/work context. Small initial change and uses the existing JSONL audit precedent. Must be non-blocking and redact sensitive fields.
2. **Introduce a proxy/gateway.** Deferred: larger architecture and rollout surface than needed to test the first end-to-end slice; reconsider only if the survey shows provider coverage cannot be achieved reliably at current call sites.
3. **Instrument only MCP 8030 tool calls.** Not selected as the sole integration point: it can observe tool activity but cannot recover provider usage already discarded inside Core connectors/routers.

## Scope and caveats
- G1 must define the event contract, provider-specific usage extraction, idempotency, redaction, failure isolation, storage/retention and pricing provenance before implementation.
- Record only fields actually returned by each provider. Use provenance labels `provider_reported`, `gateway_observed`, `estimated`, or `unavailable` according to the approved schema; never fabricate zero tokens or cost.
- The inventory is static-only and explicitly does not establish runtime behavior. It has not covered all potential invocation paths under `30/`, `10/COMPUTER-AGENT`, `integration/`, and `research/`. Coverage is therefore incomplete and must be expanded before claiming system-wide coverage.
- The inventory's statement that MCP 8030 exposes four tools may describe the inspected adapter subset; it must not be treated as the complete live Build MCP catalog without separate runtime evidence.
- `agents/xu.yaml` and `agents/claude.yaml` reportedly have empty model fields. Real-provider usage from those configured paths remains blocked until valid models are configured and a real call is evidenced.
- Work 102 remains NOT PASS / NOT RELEASED on its separate branch. This decision does not waive its gates or declare a cross-work dependency.

## Conditions to enter implementation
1. Vinh acknowledges the G1 schema/privacy/pricing design.
2. G1 specifies tests for extraction, missing usage, duplicate/retry handling, redaction and ledger write failure.
3. A reproducible authorized test environment is identified.
4. Implementation remains in the approved work branch/sandbox boundary; no Protected Core authority changes.

## Acceptance evidence for the first vertical slice
One real or explicitly labelled test-provider call yields a correlated event in the ledger; the record includes source/provenance and evidence references; missing fields remain missing; tests reproduce the result; a reporting query summarizes that event; and an independent reviewer verifies the artifacts.

## Gate statement
**DECISION recorded; G0 remains RECORDED / NOT PASS pending expanded discovery evidence and explicit gate review. G1 design may proceed as a proposal for Vinh's ACK.**
