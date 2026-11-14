# W116 SOURCE CATALOG — FIRST SOURCE

## SRC-001 — public-apis/public-apis
- Type: DISCOVERY_DIRECTORY
- Canonical URL: https://github.com/public-apis/public-apis
- Default branch inspected: master
- Visibility: Public
- Archived: No (repository metadata at inspection)
- Repository license: MIT (LICENSE file read from master)
- README finding: The repository describes itself as a manually curated public API list and currently includes both API entries and a section named MCP Servers.
- Useful for ROOM-HOP: Discover candidate APIs and Agent-callable MCP servers by category; compare the metadata exposed by the directory; identify provider documentation and installation links.
- Not useful for: Directly executing an API call, proving a provider is live, proving that an API is free, or granting an Agent permission.
- Practical assessment: PASS as a source directory; NOT AN EXECUTABLE SERVICE.
- Runtime test: NOT APPLICABLE to the repository itself. Individual entries are NOT TESTED until separately inspected/called in an authorized test.
- Important caveat: MIT applies to the repository's own content. It does not replace each API provider's terms, license, pricing, authentication, privacy policy or usage limits.
- Source freshness: Check the upstream README and provider docs when selecting a specific entry; do not assume the catalog entry is current.

## Selection rule
Prioritize tools that solve an identified ROOM-HOP need. For each selected entry, create one concise resource record with its own source URL, purpose, protocol/endpoint, authentication, cost/quota, privacy/security notes, compatibility, test evidence and status.


# FINANCE & INVESTMENT RESOURCES — INITIAL EXPANSION

## Financial classification
- RES-03 Finance & Investment: issuer research, statements, portfolio analytics, valuation, quant research.
- RES-04 Market Data: prices, OHLCV, order books, indices, corporate actions and crypto market data.
- RES-05 Banking & Economy: central-bank series, rates, FX, inflation, GDP and macroeconomic indicators.

## FIN-001 — SSI FastConnect API
Official Vietnamese broker API documentation describes REST market data for HOSE/HNX/UPCOM, daily trading data, OHLCV intervals, indices, corporate actions and WebSocket streams. It also documents order placement/amend/cancel, account and portfolio access. Classified as CANDIDATE: official documentation reviewed; no credentials or runtime calls used. Market-data read scope must be separated from trading scopes.
Source: https://developers.ssi.com.vn/docs/getting-started/overview

## FIN-002 — FRED API
Official St. Louis Fed API for FRED/ALFRED economic time series, observations, releases and historical vintages. API key required. Documentation reviewed; runtime not tested.
Source: https://fred.stlouisfed.org/docs/api/fred/

## FIN-003 — SEC EDGAR APIs
Official SEC public submissions and XBRL company facts/filings data. Public API access uses a declared User-Agent and fair-access requirements. Documentation reference recorded; runtime not tested.
Source: https://www.sec.gov/edgar/sec-api-documentation

## FIN-004 — CCXT
Mature open-source multi-exchange library. Public market data can be accessed without exchange keys on supported venues; private API methods can read accounts and execute trades/transfers. Catalog as CANDIDATE for read-only market-data integration; private methods remain out of scope. Documentation/repository reviewed; runtime not tested.
Sources: https://github.com/ccxt/ccxt and https://github.com/ccxt/ccxt/wiki/Manual

## FIN-005 — fin-data-mcp
Community MCP project aggregates several finance data providers. GitHub snapshot showed a very small project (4 stars, 1 commit); record as LOW-MATURITY CANDIDATE only. Requires code/dependency/security review and runtime tests before installation.
Source: https://github.com/CohenD/fin-data-mcp

## FIN-006 — awesome-finance-mcp
Curated discovery directory for finance MCP servers. It is a directory, not an executable MCP service. Each listed server requires independent source, license, maintenance, security and runtime review.
Source: https://github.com/BlockRunAI/awesome-finance-mcp

## FIN-007 — Frankfurter API
Reference exchange-rate API based on central-bank data including ECB reference rates. Useful for historical/reference FX, not a live executable quote. Documentation reference recorded; runtime not tested.
Source: https://frankfurter.dev/

## FIN-008 — World Bank Indicators API
Official public API for development and macro indicators across countries. Useful for long-horizon macro context; verify indicator definition, unit, frequency and release lag. Runtime not tested.
Source: https://datahelpdesk.worldbank.org/knowledgebase/topics/125589-developer-information

## Important status distinction
These additions are documented candidates, not runtime PASS. Only the upstream documentation/repository was reviewed. No broker account, API key, trade endpoint or external MCP server was connected or executed.
