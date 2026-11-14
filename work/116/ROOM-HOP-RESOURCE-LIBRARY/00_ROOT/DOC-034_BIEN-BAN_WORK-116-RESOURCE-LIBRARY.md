# DOC-034 — BIÊN BẢN / WORK 116 RESOURCE LIBRARY
- Date: 2026-11-14
- Status: ACTIVE WORKING DECISION
- Authority: Vinh
- Coordinator: Xu / AI-01

## Agreed purpose
W116 is the shared ROOM-HOP resource library. Its job is to evaluate whether a source or tool is practically usable, normalize its information, and make it visible and understandable to ROOM-HOP Agents.

## Operating approach
Keep the workflow lightweight:
1. Find a source/tool.
2. Check that the source is reachable and determine what it actually provides.
3. Distinguish a directory/catalog from an executable API, MCP server, SDK or library.
4. Record purpose, canonical link, category, access/auth, protocol, constraints and actual test status.
5. Publish the normalized record so Agents can discover it.
6. Update the record when source or compatibility changes.

## Agent usage rule
Catalog visibility means discoverable, not automatically authorized to execute. Agents must use the documented official endpoint/tool and respect its authentication, privacy, cost and permission requirements. Never put secrets in W116.

## First source decision
public-apis/public-apis is accepted as a discovery directory, not as a directly callable service. Its README includes API entries and an MCP Servers section. The repository itself is not an API endpoint and its README is not proof that listed providers are live, free, safe or compatible.

## Scope boundary
No elaborate approval committee, no new Work per resource category, no bulk blind import, no credentials stored in the library. Keep only useful and understandable resource records.
