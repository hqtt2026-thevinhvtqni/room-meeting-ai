# ROOM-HOP AI Capability Registry — Phase 1

**Canonical architecture:** DOC-086  
**Implementation plan:** DOC-087  
**Registry status:** INITIALIZED_EMPTY  
**Current claim:** No model capability has been verified by this registry.

## Files
- `schema/capability-registry.schema.json` — JSON Schema Draft 2020-12.
- `data/registry.json` — canonical registry data file.
- `templates/capability-record.template.json` — non-verified starter record.

## Rules
1. Add one record per narrowly testable capability, not one broad claim per AI brand.
2. Record exact provider, model ID, model version, deployment mode and tool/endpoint. Use `UNKNOWN` where not established.
3. Keep capability status at `UNVERIFIED` until a reproducible test and reviewable evidence exist.
4. `VERIFIED` requires a dated test, method, result, evidence URI and reviewer. A model's own self-report is not sufficient evidence.
5. `freshness_status` is independent of capability status. Mark `STALE` when model/version/runtime/evidence is no longer current.
6. Registry entries do not grant identity, permissions, secrets, tool access or authority to execute network/system actions.
7. Never store API keys, tokens, passwords, cookies, private user data or secret payloads here.
8. Do not record latency, cost or resource figures unless measured with units, environment and timestamp.
9. Do not add placeholder records to the canonical `data/registry.json`. Use the template only as a working copy, then replace every placeholder before submission.
10. Changes must be reviewed and logged in Work 70 DOC-035.

## Minimal validation
- Parse all JSON files.
- Validate `data/registry.json` against the schema using an approved JSON Schema Draft 2020-12 validator before accepting contributed records.
- Check that every `VERIFIED` entry has test evidence and reviewer.
- Check for secrets and unauthorized personal data.
- Read back the committed files from GitHub and record the commit/blob evidence.

## Phase 1 boundary
This is a static, version-controlled data contract. No database, API, UI, scheduled job, provider integration, model benchmark or automatic dispatch is included.
