# W116 — AGENT RESOURCE DISCOVERY GUIDE

1. Read RESOURCE_CATALOG.json to discover registered sources/resources.
2. Follow each record's canonical_url or documentation_url; do not infer endpoints.
3. Check status before use:
   - DISCOVERY_DIRECTORY: browse for candidates only.
   - CANDIDATE: identified but not tested.
   - TESTED: the stated test passed under the recorded scope.
   - APPROVED_FOR_USE: explicitly cleared for the stated Work/Agent and scope.
   - BLOCKED / DEPRECATED: do not use.
4. A source entry does not itself grant permission to call a provider.
5. Follow the provider's authentication, privacy, pricing, rate limits and terms.
6. Never store API keys, tokens or passwords in this Work, prompts, catalog records or Git.
7. When an Agent finds a useful tool, propose a concise record update with the exact docs and observed evidence. Do not label it TESTED without a real test.

Minimum resource fields:
resource_id, name, type, category, purpose, canonical_url, documentation_url, protocol_or_endpoint, auth, pricing_or_quota, constraints, compatible_work_ids, status, test_scope, test_result, last_checked.
