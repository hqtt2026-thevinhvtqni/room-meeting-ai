# Data Policy and Threat Model — Work 23
Date: 2026-10-10
Status: SAFEGUARDS DOCUMENTED; ENFORCEMENT NOT VERIFIED

## Assets
Gemini API keys, prompts/responses, internal source code, customer data, usage/quota/billing metadata and audit records.

## Threats and controls
- Key leakage: keep keys in protected server-side configuration/secret storage; never place them in source, frontend, chat, prompts, logs or evidence.
- Unauthorized data egress: default to synthetic/minimal data; require policy authorization for sensitive data; fail closed when classification is unknown.
- Quota/cost exhaustion: bounded calls, timeout, retry/backoff, usage monitoring and budget controls before real integration.
- Untrusted output: validate provider response structure and treat generated content as untrusted input.
- Unsafe fallback: do not send sensitive data to another provider without explicit policy.
- Audit leakage: record actor, purpose, model, time, outcome and correlation ID; do not log sensitive prompt/response by default.

## Current status
The sample checks key presence in REAL_API mode but does not make a provider request. Policy gate, secret manager integration, redaction tests, quota guard and secret scan have not been executed.

Never change billing or incur unapproved costs.