# Folder Contract

`08_DASHBOARD/` is the canonical Dashboard UI and data contract. `09_DASHBOARD_PREVIEW/` is the separate static preview and visual review surface. Store runtime screenshots, browser logs and acceptance evidence in `06_EVIDENCE/`.

Preview is read-only and must not fabricate live status. File read-back is not runtime verification. Sync stays DRY_RUN; no integration before exact operation approval.
