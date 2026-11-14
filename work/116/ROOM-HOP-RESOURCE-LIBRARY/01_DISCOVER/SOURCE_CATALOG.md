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
- Important caveat: MIT applies to the repository's own content. It does not replace each API provider's terms, license, pricing, privacy policy or usage limits.
- Source freshness: Check the upstream README and provider docs when selecting a specific entry; do not assume the catalog entry is current.

## Selection rule
Prioritize tools that solve an identified ROOM-HOP need. For each selected entry, create one concise resource record with its own source URL, purpose, protocol/endpoint, authentication, cost/quota, privacy/security notes, compatibility, test evidence and status.
