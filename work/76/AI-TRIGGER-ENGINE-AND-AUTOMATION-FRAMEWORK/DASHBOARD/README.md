# WORK 76 DASHBOARD

Read-only dashboard for Trigger Engine lifecycle, work packages, blockers and evidence.
- index.html: responsive static dashboard.
- PRODUCT_STATUS.json: local snapshot.
- PRODUCT_STATUS.schema.json: JSON Schema for snapshot validation.
Dashboard is not an authorization surface and cannot create, edit, enable, disable or execute Triggers.
If data cannot be loaded or freshness cannot be established, show UNKNOWN. Never substitute fabricated values.
Serve this folder with a local HTTP server for fetch-based JSON loading.
