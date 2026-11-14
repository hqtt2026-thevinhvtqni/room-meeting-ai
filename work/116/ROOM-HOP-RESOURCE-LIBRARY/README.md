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

## Current source
- [public-apis/public-apis](01_DISCOVER/SOURCE_CATALOG.md) — useful discovery directory for public APIs and MCP server candidates.
- It is a catalog, not a callable API or an automatic permission grant.

## Work boundaries
W116 discovers, evaluates and documents resources. It does not replace ROOM-HOP execution, Gateway, integration contracts, Agent orchestration or credential management. Never commit secrets.
