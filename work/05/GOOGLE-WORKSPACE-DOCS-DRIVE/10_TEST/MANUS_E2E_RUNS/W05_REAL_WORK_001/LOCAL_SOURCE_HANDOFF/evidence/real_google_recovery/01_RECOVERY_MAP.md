# Work 05 — REAL GOOGLE Recovery Map

**Mode:** read-only recovery and preflight; no implementation changes.

## DONE

- Phase-1 through Phase-4 Work 05 evidence reviewed.
- Core-first boundary preserved: AI → MCP :8020 → Core :8000 → Google Workspace Adapter.
- Local/mock Core and MCP implementation passed its final QE.
- Provider contract and GoogleWorkspaceAdapter passed fake-provider E2E.
- Lazy real Google provider boundary and configuration validator exist.
- REAL GOOGLE tests are isolated from offline tests.
- Local continuation later added G09 and connection/OAuth offline coverage.

## BLOCKED

- G01 AUTH: blocked before client construction.
- G02–G10 and RG01–RG15: blocked/not run because external authentication and target are absent.
- `W05_GOOGLE_CREDENTIALS_FILE`, `W05_GOOGLE_SCOPES`, and `W05_GOOGLE_PARENT_ID` are absent.
- `gws auth_method=none`; no client config, token cache, or credential store.
- `googleapiclient` and `google.auth` unavailable.
- No safe real Google document/Shared Drive target supplied.

## MISSING

- Authorized credentials and approved scopes.
- Google client dependencies.
- Explicit safe test corpus/document and Shared Drive target.
- Real-Google evidence records containing actual resource IDs and runtime timestamps.

## RISK

Treating provider-shape tests as Google runtime evidence would be a false PASS. Running mutations without a dedicated target could affect uncontrolled external data.

## REQUIRED_ACTION

Supply approved Google credentials/scopes, expose client libraries, provide a safe test document and Shared Drive target, and rerun the real suite without replacing tests with mocks.
