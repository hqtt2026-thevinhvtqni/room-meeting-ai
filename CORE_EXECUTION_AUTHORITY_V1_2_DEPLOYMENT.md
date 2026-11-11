# Core Execution Authority V1.2 — Deployment & Configuration

## Scope and fail-closed behavior

The Core HTTP entrypoint is python -m room_hop_mcp.core_http_main (default bind 127.0.0.1:8000). It mounts the existing Meeting API and the additive Core-owned Work Execution Authority in the same Core process. If identity, Work policy or durable journal configuration is absent/invalid, the Meeting API remains available and protected execution routes return 503 execution_authority_not_configured.

The Execution Host entrypoint is python -m execution_host.server (default bind 127.0.0.1:8031). Both direct HTTP servers currently reject non-loopback bind. Remote deployment is NOT implemented; a future HTTPS/private-network ingress must be separately reviewed and must not weaken the loopback-only process boundary.

## Core environment

Required environment variables:

- ROOM_HOP_EXECUTION_IDENTITIES_JSON: JSON object mapping service identity IDs to records containing credential_sha256 (64 lowercase hex), kind (agent or host), and principal_id for agent identities. Example shape: {"agent-ka-service":{"kind":"agent","principal_id":"agent-ka","credential_sha256":"<64-lowercase-hex>"},"host-8031":{"kind":"host","credential_sha256":"<64-lowercase-hex>"}}. Raw credentials are not stored in Core configuration.
- ROOM_HOP_EXECUTION_WORKS_JSON: JSON object mapping canonical Work IDs to policy records. Each policy requires work_name, repository, allowed_branches, allowed_identities, allowed_host_identities, allowed_assignments, allowed_tasks, workspace_root, execution_workspace, evidence_root, source_sha256, environment_id, test_entrypoint and max_timeout_seconds. Optional policy fields are grant_ttl_seconds (1–900) and policy_version.
- ROOM_HOP_EXECUTION_STORE_PATH: absolute durable path to the append-only, fsynced, hash-chained JSONL event journal. Core also creates a lock file. Do not use ephemeral storage.

Agent principal resolution is server-side: the enrolled agent service credential maps to an Agent Registry ID, and Core verifies that ID exists in AgentRegistry. Request bodies cannot nominate principal_id. Host identities are enrolled separately with kind=host. Raw service credentials must be high entropy (at least 32 characters); only SHA-256 digests are stored in Core configuration.

Work policy must contain non-empty allow-lists for issuer service IDs, Host service IDs, Assignment IDs and Task IDs. The source_sha256 must be generated from the exact immutable execution workspace using execution_host.source_snapshot.workspace_source_sha256. It is not a Git commit SHA. The Host recomputes the manifest/content digest and refuses mismatches. Symlinks are rejected; .git, Python caches, virtual environments and pytest caches are excluded.

Core HTTP options:
- ROOM_HOP_CORE_BIND defaults to 127.0.0.1 and is loopback-only.
- ROOM_HOP_CORE_PORT defaults to 8000.
- ROOM_HOP_MEETINGS_DIR is optional.

## Execution Host environment

Required:
- ROOM_HOP_CORE_AUTHORITY_URL: Core base URL. Loopback HTTP is permitted only for local development; remote URLs must use HTTPS.
- ROOM_HOP_EXECUTION_HOST_ID: enrolled Host service identity ID.
- ROOM_HOP_EXECUTION_HOST_CREDENTIAL: raw high-entropy Host credential (at least 32 characters), injected from the Host secret store only.
- ROOM_HOP_EXECUTION_HOST_BIND defaults to 127.0.0.1 and rejects non-loopback addresses.
- ROOM_HOP_EXECUTION_HOST_PORT defaults to 8031.

The public Host HTTP surface accepts only POST /execute-granted with work_id, grant_id and grant_token. The former caller-supplied /execute WorkContext/authorized-boolean surface is not exposed by this server. The Host obtains canonical Work binding from Core and executes only the exact Core-bound pytest entrypoint. The Host does not issue Grants.

## Grant issuer / WEE environment

Required for the WEE Core-grant adapter:
- ROOM_HOP_CORE_AUTHORITY_URL
- ROOM_HOP_EXECUTION_AGENT_ID: enrolled issuer service identity ID.
- ROOM_HOP_EXECUTION_AGENT_CREDENTIAL: raw high-entropy agent service credential from the agent secret store.
- EXECUTION_HOST_URL: Host URL; defaults to http://127.0.0.1:8031 for loopback development.

Canonical WorkContext must contain repository, branch, expected_head (Git commit SHA), assignment_id, task_id, environment_id, host_identity_id and test_entrypoint in addition to the existing Work/workspace/evidence binding. Core checks repository and branch against the Work policy and binds expected_head into the Grant. Host independently checks git rev-parse HEAD and git branch --show-current against the Grant before it creates a Run Record. The adapter computes the source hash from that canonical workspace, requests a Grant from Core, invokes the Host, and requests revocation after the attempt. The requested Host HTTP timeout is bounded to cover the configured test timeout plus a safety margin.

## Grant and Run Record protocol

- POST /works/{work_id}/execution-grants: enrolled agent service credential; issues a short-lived, single-use pytest_run Grant and returns the token once.
- GET /works/{work_id}/execution-grants/{grant_id}: issuer status query; reports active, expired or revoked.
- GET /works/{work_id}/execution-grants/{grant_id}/validate: Host service credential plus Bearer Grant token; returns canonical binding only while active and unexpired.
- POST /works/{work_id}/execution-grants/{grant_id}/runs: Host service credential plus Bearer Grant token; appends run_started before process creation.
- POST /works/{work_id}/execution-grants/{grant_id}/runs/{run_id}/complete: appends run_completed with outcome, exit code and evidence digest.
- POST /works/{work_id}/execution-grants/{grant_id}/revoke: issuer credential; revokes the active Grant.

Run Record is two-phase. Host first validates online, verifies source, and asks Core to persist run_started. Host then revalidates online immediately before process creation. If the Grant is revoked before that second check, no process is spawned. Host executes the exact pytest entrypoint, writes local stdout/stderr and RUN_EVIDENCE.json, hashes the evidence, then asks Core to append run_completed. A Grant may start only one run. Revocation blocks new starts; completion of an already-started attempt remains recordable after revocation. No cached ALLOW is used.

Grant token is returned once and only its SHA-256 digest is persisted. Tokens and raw service credentials must never be logged, printed or placed in evidence. Run journal events include grant_issued, grant_revoked, run_started and run_completed. Hash-chain corruption, unknown event types, invalid transitions or journal I/O errors fail closed.

## Operational gates still required

1. Provision identity credential digests, Work policy allow-lists, exact source hash and durable store path in the approved secret/config manager; do not commit raw credentials.
2. Verify Agent Registry resolution and that the issuer Agent is the intended W32 actor.
3. Verify Work Sandbox canonical context has Assignment/Task/Environment/Host binding matching Core policy.
4. Run exact-SHA CI, including focused Core/Host/WEE tests, on the final candidate head.
5. Independently review credential rotation, cross-process journal locking, expiry/revocation races, run-intent/completion replay and evidence persistence.
6. Configure and start Core/Host only under the approved service manager after exact config review; do not start a second Core process on an occupied port.
7. Verify process build hash, source hash, PID, loopback listener and actual workspace/evidence path.
8. Run live positive and negative probes: missing/invalid credentials, wrong Agent, wrong Work, Assignment, Task, Host, purpose, environment, source hash, command, timeout, expired/revoked/reused Grant, Core outage, run-start persistence failure, run-completion persistence failure and journal corruption.
9. Verify records survive Core restart and exact source/branch readback matches the executed workspace.

No production identity, credential, Work policy, storage path, deployment host or existing Core process is fabricated by this document.

**Current status:** source implementation candidate; live runtime configuration and deployment are not verified. PROTECTED EXECUTION DENIED.