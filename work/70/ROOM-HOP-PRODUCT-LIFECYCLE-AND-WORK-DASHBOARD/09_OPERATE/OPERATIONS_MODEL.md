# 09 — OPERATE / VẬN HÀNH

Status: NOT ACTIVE — FUTURE OPERATING MODEL

## Ownership
Assign a named Operations Owner and backup before production release. Core owns authoritative lifecycle state; the Dashboard is a read-only projection.

## Operational controls
- monitor Core/Dashboard availability and data freshness;
- detect stale/missing evidence references and integrity mismatches;
- monitor gate failures, unresolved blockers and WP aging;
- audit lifecycle transitions, evidence storage, exports and access denials;
- apply backup, restore, retention and expiry policies;
- monitor error rates, latency, storage growth, export failures and cost;
- maintain incident response, escalation and rollback runbooks;
- feed incidents, user feedback and usage metrics into the next DISCOVER/DEFINE cycle.

No monitoring, alerting, backup or production operations are claimed as implemented until runtime evidence is attached.
