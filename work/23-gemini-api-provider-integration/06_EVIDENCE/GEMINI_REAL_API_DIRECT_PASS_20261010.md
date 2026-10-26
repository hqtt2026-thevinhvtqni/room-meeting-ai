# Work 23 — Direct Gemini API Evidence
Date: 2026-10-10
Source: owner-provided Windows PowerShell output.

- Result: PASS — direct HTTPS generateContent call.
- Model: gemini-3.8-flash.
- Status: HTTP_STATUS=PASS.
- Returned text: OK.
- Prompt feedback: empty object.
- Finish reason: MAX_TOKENS.
- Usage: prompt 3 tokens; candidate 1; total 31; thoughts 27; service tier standard.

Interpretation: the direct request returned the expected text and verifies direct endpoint access for this request. MAX_TOKENS indicates the configured generation budget was reached, though OK was returned.

Security: supplied output did not disclose the API key; no key value or secret-bearing header is recorded here.

Limitations: this direct HTTP request bypassed the provider adapter, MCP :8020, and Core :8000. Adapter REAL_API and full MCP/Core E2E remain unverified. Work 23 remains ACTIVE; do not mark COMPLETED/LOCKED.