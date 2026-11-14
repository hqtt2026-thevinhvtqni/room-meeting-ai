# W116 — ROOM-HOP RESOURCE LIBRARY
**Kho tài nguyên dùng chung ROOM-HOP**

W116 helps ROOM-HOP Agents discover useful APIs, MCP servers, SDKs, libraries, models, datasets and developer tools.

## How Agents use this Work
1. Start with [RESOURCE_CATALOG.json](01_DISCOVER/RESOURCE_CATALOG.json).
2. Read [AGENT_RESOURCE_DISCOVERY_GUIDE.md](01_DISCOVER/AGENT_RESOURCE_DISCOVERY_GUIDE.md).
3. Open the linked source and provider documentation.
4. Check each resource's status, authentication, cost/quota, constraints and test evidence.
5. Use only the official documented interface and only where the Agent/Work already has permission.

## Finance and investment resources
W116 has dedicated finance classifications: RES-03 Finance & Investment, RES-04 Market Data and RES-05 Banking & Economy. See [finance source records](01_DISCOVER/SOURCE_CATALOG.md#finance--investment-resources) and filter `RESOURCE_CATALOG.json` by category.

## Expanded resource domains
W116 now classifies public administration/e-government, legal/regulatory, public investment, public procurement, construction and construction costs, health, education, I Ching and classical texts (RES-13 to RES-23). See the source catalog and filter `RESOURCE_CATALOG.json` by category. New entries GOV-001..002, PUB-001..002, CON-001..002, HLT-001, EDU-001 and ICH-001 are candidates; portal/API access and runtime status are explicitly distinguished.

## Vietnam law and legal research
Dedicated category RES-24 includes the National Law Portal, National Database of Legal Documents, Official Gazette, National Assembly, Supreme People's Court and treaty sources (LAW-001..LAW-006). Prefer official primary sources; verify exact document version, legal status, effective date and amendments. No public API is assumed unless separately verified.

## Current source
- [public-apis/public-apis](01_DISCOVER/SOURCE_CATALOG.md) — useful discovery directory for public APIs and MCP server candidates.
- It is a catalog, not a callable API or an automatic permission grant.

## Work boundaries
W116 discovers, evaluates and documents resources. It does not replace ROOM-HOP execution, Gateway, integration contracts, Agent orchestration or credential management. Never commit secrets.
