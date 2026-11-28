# Work 05 — GOOGLE_READINESS

## Auth model

The loader is service-account JSON based. `build_google_services` uses `google.oauth2.service_account.Credentials.from_service_account_file(...)`. It is not an OAuth user/browser flow. `W05_GOOGLE_CREDENTIALS_FILE` must be provisioned through an approved secret/file channel and never pasted into chat or committed.

## Required scopes and dependencies

Minimum intended scopes are `https://www.googleapis.com/auth/documents` and `https://www.googleapis.com/auth/drive`. Required APIs are Google Docs and Google Drive. Required Python packages are `google-auth` and `google-api-python-client`.

Current Sandbox readiness: `googleapiclient` unavailable, `google.auth` unavailable, and `gws auth_method` is `none`. No package was installed during readiness work.

## Target contract

`W05_GOOGLE_PARENT_ID` is the Drive parent folder, `W05_GOOGLE_DRIVE_ID` is an optional Shared Drive ID, and `W05_REAL_TEST_DOCUMENT_ID` is the approved safe document target. No target was supplied.

## Inputs required

Provide through approved secure configuration: authorized credential path, approved scopes, test parent folder, safe test document, optional Shared Drive ID, enabled Docs/Drive APIs, and approved dependencies.
