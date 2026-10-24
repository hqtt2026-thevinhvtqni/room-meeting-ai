# G2 Implementation Progress — Work 104

- Date: 2026-10-24 (UTC+7)
- Coordinator: Xu (AI-01 GPT CEO / architecture coordinator)
- Scope authority: Vinh's instruction to start G2, against G1 REV 6.
- Status: **IN PROGRESS — NOT PASS; G3 NOT STARTED**.
- Branch: `work/104-ai-usage-evidence-tracking`.

## Changes written to branch

1. `core/usage_ledger.py` — in-memory event creation before provider request; schema-v1 allowlist; provider usage normalization for Anthropic/OpenAI/Groq/Google; append-only JSONL; monthly default path; 20 MiB rotation and best-effort index; failure counter + stderr fallback; unavailable cost stays null; prompt/response raw fields and arbitrary extra fields are not serialized.
2. `tests/test_usage_ledger.py` — unit tests for provider mapping, absent usage, event correlation, one-row append, redaction, and non-raising write failure.
3. `core/connectors.py` — instrumentation for Anthropic and OpenAI meeting-turn connectors.
4. `core/intent_router.py` — instrumentation for Claude intent routing.
5. `core/llama_intent_router.py` — instrumentation for Groq intent routing.
6. `core/gemini_intent_router.py` — instrumentation for Gemini usage, including model fallback attempts.
7. `llama_chat_v2.py` — instrumentation for both Groq completions in the shared-client chat path.

## Known limits / blockers

- MCP 8030 connection failed in this session; writes were made through the connected GitHub tool on the approved Work 104 branch instead.
- The tests have **not yet been executed** in an authorized runtime. No test result is claimed.
- No real provider call was run. `agents/xu.yaml` and `agents/claude.yaml` still have empty model fields; do not claim live usage for those configured agents.
- G0 remains NOT PASS because the root `room-meeting-ai/` gitlink source URL has not been supplied. The gitlink was not changed.
- #7c remains OPEN and was not implemented.
- Pricing provenance (#7b) is not implemented; cost remains `unavailable` / `null`.
- The initial implementation is a candidate requiring code review and G3 verification. Do not claim system-wide coverage or completeness.

## Commits written

- Ledger module: `a945405926a89763eae1cc924fe909c6a6c47317`
- Ledger test: `0c0b763524570592199790e881e084f8df41c516`
- Ledger failure-path configuration: `bf25599f6744f393b532a3dad65fdd243228795e`
- Meeting connectors: `c432f68e695b0eaae88c268117dcedbc10741b5a`
- Claude intent router: `7782fd2fc2a4c5eaf022877138d426e0fbde55ff`
- Groq intent router: `5e730aa32769933f5425ca3bc5b814b830fc83c3`
- Gemini intent router: `3a68fdc9873eec4a97ebd2f19f94a82d2dc0cda3`
- Shared Groq chat consumer: `6c28e0551524f6efdebbd032ba270e388665b0c7`

## Next gate

Before G2 can be declared complete: run the new unit tests and relevant existing regression tests in an authorized Python environment; review all changes for syntax, provider SDK field compatibility, error-path accounting, concurrency/rotation behavior, and no-regression to AI request flow. G3 remains a separate verification gate with independent review.


## Addendum — implementation delta

- `core/connectors.py` also records Mock/Internal connector events as `usage_source=unavailable`, consistent with G1 §3; these are not provider-billed calls.
- Latest follow-up commits: ledger counter scope `df7d40ddeba08f0ea9b2b35b17082e89e19d4540`; connectors including Mock/Internal `3ff659047831cbde8444536854b6fdfb3745d684`.
- The earlier commit list above records initial commits; these two follow-up commits supersede the initial file snapshots.
- Tests remain NOT RUN. This addendum changes no gate status.
