# DOC-007 — Identity Registry vs Authenticated Principal Boundary

- Work: 33 — ROOM-SHARED-FILE-EVIDENCE-HUB
- Date: 2026-11-27
- Status: SOURCE TRACE COMPLETE / SECURITY GAP OPEN
- Method: read-only inspection of GitHub main; no code execution or runtime probe.

## Exact source evidence (main)

| File | Blob SHA | Relevant fact |
|---|---|---|
| core/principal_registry.py | 1eda0c80f413c1405415f92e0e2ff3b82a43b5ef | YAML directory of human principals; module states it does not process authorization/JOIN. |
| core/agent_registry.py | 7e4b98e68fa1a208ebd5788d9235d9c222e402a3 | YAML directory of AI agents; permissions/authority fields are forward-compatible and not processed in this version. |
| core/identity_resolution.py | 207c0ea74e3c77929c1723b0e66beba4ccf36201 | Resolves caller-provided identity_id by checking whether it exists in either registry. |
| core/message_identity.py | d5096c77492c32d6f34956c404fb98a0c784d271 | Builds display/message header from registry data; no credential proof. |
| core/meeting_manager.py | d4d7b28f0f0df9208648d0870c42cb6e451eda50 | join_request(identity_id) accepts identity_id string, resolves registry membership and invitation policy, then writes auth_verified=true. |
| room_hop_mcp/adapter/http_server.py | 54cb3ecbce2e6b13083f31c14f0c1f0738f1457d | Join DTO contains identity_id only; inspected app has no bearer authentication dependency/middleware. |
| room_hop_mcp/core_http_main.py | 8dd6bb5ea500026d932ca52eb6079c980d722ab0 | Docstring says additive authority mount exists, but build_app returns create_http_app(service); actual imported adapter does not mount it. |

## Findings

1. PrincipalRegistry and AgentRegistry establish that an ID is present in a YAML registry. They do not prove the caller controls that human/AI identity.
2. IdentityResolution classifies registry membership. It is not authentication.
3. MeetingManager.join_request receives caller-supplied identity_id. It checks registry membership and invitation/creator membership, then sets identity.auth_verified=true. No authenticated session/token/cryptographic proof is checked in this method. This field therefore overstates the evidence and must not be reused as proof of identity for Cloud Drive.
4. HTTP JoinMeetingRequest contains only identity_id. In the inspected adapter, caller can choose the ID submitted to the Core route. No bearer principal dependency or request-auth middleware is wired in this adapter.
5. Message header resolution is attribution/display metadata, not authenticated request origin.
6. Core HTTP entrypoint docstring says execution-authority mount exists, but the actual imported adapter has no such mount. This is a source/docstring contradiction and must be corrected by the owning Core work; Work 33 will not edit Core.

## Cloud Drive security decision

- Never derive Cloud Drive Principal from request JSON identity_id, Message Header, registry lookup, Agent name, auth_verified, or caller-supplied authorized.
- Cloud Drive must receive an authenticated principal from a verified trust boundary before authorization.
- Until such a boundary exists, UnconfiguredAuthorizer remains DENY ALL.
- Core contract must distinguish: registry record, authenticated session/token, authorization decision. Do not overload one field for all three.
- Minimum token/session contract to verify before implementation: trusted issuer, signature verification/key rotation, audience, subject ID and principal type, tenant/Work scope, expiry/not-before, token ID/revocation, credential lifecycle, and explicit resource/action decision. No field names, routes or key URLs are assumed.
- Negative tests must prove caller cannot spoof another registered human or AI by changing identity_id; missing/invalid/expired/revoked token denies; wrong audience/issuer denies; cross-tenant/Work access denies; Core timeout denies.

## Disposition

- Registry discovery: VERIFIED in source.
- Cryptographic caller authentication in inspected main Core HTTP adapter: NOT FOUND / NOT VERIFIED.
- Authenticated identity binding in Meeting JOIN: NOT VERIFIED; auth_verified=true is unsupported by inspected evidence.
- Core Execution Authority route in main adapter: NOT MOUNTED in inspected source, despite stale entrypoint docstring.
- Cloud Drive authenticated principal integration: BLOCKED / NOT IMPLEMENTED.
- No tests executed, no runtime probe, no secrets/configuration, no code changes to Core, no merge/deployment.
