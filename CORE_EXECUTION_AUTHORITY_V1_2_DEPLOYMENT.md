# Core Execution Authority V1.2 — Deployment & Configuration

## Scope and fail-closed behavior

The Core HTTP entrypoint is \`python -m room_hop_mcp.core_http_main\` (default
bind \`127.0.0.1:8000\`). It mounts the existing Meeting API and additive
Work execution-grant routes in the same Core process. Missing or invalid
authority configuration leaves the Meeting API available and execution
routes return \`503 execution_authority_not_configured\`.

Do not bind Core or Execution Host to a public interface. For a remote Host,
use a private network with TLS and firewall rules allowing only the enrolled
service identities. Plain HTTP is accepted by the Host client only for
loopback development.

## Core environment

Required environment variables:

- \`ROOM_HOP_EXECUTION_IDENTITIES_JSON\`: JSON object mapping enrolled service
  identity IDs to SHA-256 digests of their high-entropy credentials. Example
  shape: \`{"mcp-8020":"<64-lowercase-hex-sha256>"}\`. Do not place raw
  credentials here.
- \`ROOM_HOP_EXECUTION_WORKS_JSON\`: JSON object mapping canonical Work IDs
  (\`W<number>\`) to the Work policy. Each policy must include
  \`work_name\`, \`allowed_identities\`, \`workspace_root\`,
  \`execution_workspace\`, \`evidence_root\`, and \`source_sha256\`.
  \`allowed_purposes\` defaults to \`["pytest_run"]\`.
- \`ROOM_HOP_EXECUTION_STORE_PATH\`: absolute path to a persistent directory
  on durable storage. Core writes an append-only, fsynced, hash-chained JSONL
  event journal and a lock file. Do not place it on ephemeral storage.

The \`source_sha256\` value must be generated from the exact immutable
execution workspace using \`execution_host.source_snapshot.workspace_source_sha256\`.
The Host recomputes this digest before every execution and refuses mismatches.
Do not use a Git commit SHA in this field; it is a SHA-256 of the canonical
workspace file manifest and contents.

Core HTTP runtime options:

- \`ROOM_HOP_CORE_BIND\` (default \`127.0.0.1\`)
- \`ROOM_HOP_CORE_PORT\` (default \`8000\`)
- \`ROOM_HOP_MEETINGS_DIR\` (optional)

## Service identity secret

Generate a high-entropy credential out-of-band. Store only its SHA-256 digest
in Core's \`ROOM_HOP_EXECUTION_IDENTITIES_JSON\`; inject the raw credential
only into the enrolled MCP service's secret store and send it in
\`X-ROOM-HOP-SERVICE-CREDENTIAL\` over TLS/private transport. Never commit it,
print it, include it in logs, or put it in evidence.

Grant tokens are returned once by grant issuance, held in memory by the
requesting service, sent as \`Authorization: Bearer ...\` to the Host, and
never persisted in clear text.

## Execution Host environment

Required:

- \`ROOM_HOP_CORE_AUTHORITY_URL\`: private Core base URL, e.g.
  \`https://core.internal.example\`. Loopback HTTP is allowed only for local
  development.
- \`ROOM_HOP_EXECUTION_HOST_BIND\`: private interface address; defaults to
  \`127.0.0.1\`.
- \`ROOM_HOP_EXECUTION_HOST_PORT\`: defaults to \`8031\`.

The Host accepts only the \`pytest_run\` operation in this implementation.
The caller cannot submit a WorkContext or set \`authorized=true\`; the Host
retrieves Work paths and source hash from Core after validating the grant
online. The command must be a pytest invocation and its timeout cannot exceed
the grant's \`max_timeout_seconds\`.

## Routes

- \`POST /works/{work_id}/execution-grants\` — enrolled service credential;
  issues a Work/purpose-scoped short-lived grant and returns the token once.
- \`GET /works/{work_id}/execution-grants/{grant_id}\` — enrolled identity
  status query; returns active/expired/revoked.
- \`GET /works/{work_id}/execution-grants/{grant_id}/validate\` — bearer grant
  validation for Host; returns canonical Work binding only when active.
- \`POST /works/{work_id}/execution-grants/{grant_id}/runs\` — bearer grant
  revalidation followed by append-only run record.
- \`POST /works/{work_id}/execution-grants/{grant_id}/revoke\` — revoke active
  grant.

## Operational gates still required

1. Configure and protect the Core credential digest, Work policy, source hash,
   and persistent store in the real deployment secret/config manager.
2. Deploy this Core entrypoint through the existing approved Core service
   manager; do not start a second Core process on an occupied port.
3. Deploy the Host build and configure private Core reachability.
4. Verify runtime build hash, source hash, network boundary and PID.
5. Run live positive and negative probes: missing credential, invalid
   credential, wrong identity, wrong Work, wrong purpose, expired/revoked
   grant, source hash mismatch, timeout above grant, command outside pytest,
   Core unavailable, run-record failure.
6. Verify durable records survive Core restart and remote GitHub source/branch
   readback matches the exact executed source snapshot.

No production identity, Work policy, secret, storage path, deployment host,
or existing Core process is fabricated by this document.
