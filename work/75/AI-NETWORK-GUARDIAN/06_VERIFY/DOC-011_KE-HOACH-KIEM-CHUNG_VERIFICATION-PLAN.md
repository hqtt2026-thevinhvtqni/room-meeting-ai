# DOC-011 — Kế hoạch kiểm chứng / Verification Plan

## Product and platform
- Verify role-based sign-in on PC and Mobile.
- Verify both clients use the same backend identity, inventory and incident records.
- Verify responsive PC/mobile layouts and accessibility.
- Verify notification delivery, acknowledgement and audit history.

## Network collection
- Test read-only credentials and prove no configuration writes occur.
- Validate collector source, timestamps, freshness and behavior during router/API outage.
- Test duplicate IP and conflicting DHCP observations with controlled fixtures.
- Include negative cases to measure false positives.

## AI
- Every diagnosis must cite observation/evidence references.
- Test unsupported claims, stale evidence, missing data and conflicting observations.
- Verify abstention when evidence is insufficient.
- Verify AI cannot execute router configuration changes or invoke mutation tools.

## Dashboard and data
- Validate JSON against the published schema.
- Browser E2E on desktop and mobile viewport.
- Verify UNKNOWN/STALE/SNAPSHOT states and no fabricated live status.

## Release criteria
No release until security review, QA evidence, owner acceptance and documented rollback/recovery plan are complete.
