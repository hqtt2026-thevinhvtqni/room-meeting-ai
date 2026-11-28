# Google Workspace UI E2E — Blocked Readiness Plan

No browser/UI test executed because no Room UI or browser routing layer exists. Backend offline connection tests remain passing: 24 passed, 1 deselected.

Planned UI-01 through UI-12 cover opening without connection, OAuth start, controlled OAuth URL, callback return, connected safe metadata, browser storage audit, test connection, disconnect, old-operation rejection, REAUTH_REQUIRED, OAuth denial, and room isolation.

Offline UI tests may use a controlled callback/provider double but must be labeled OFFLINE TEST. They cannot render a mock-connected state as REAL GOOGLE Connected. Real browser OAuth tests require an authorized Google environment and runtime evidence.
