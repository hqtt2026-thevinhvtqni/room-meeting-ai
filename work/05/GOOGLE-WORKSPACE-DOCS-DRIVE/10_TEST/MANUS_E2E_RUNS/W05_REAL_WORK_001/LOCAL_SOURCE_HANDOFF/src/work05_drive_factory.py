"""Trusted OAuth-user -> Google Drive API v3 factory for Work 05.

Call only after ConnectionManager.credential_for_operation(room_id, user_id,
connection_id) has authorized the caller. Client secret comes from secure
runtime configuration, never from a browser request or the credential record.

Refresh ownership stays in ConnectionManager. The Google SDK receives an
access-token-only credential so its authorized transport cannot independently
refresh using a stored refresh token and bypass Work 05 single-flight,
invalid_grant handling, or ambiguous-outcome policy. A 401 recovery must be
performed by the Work 33/Work 05 capability boundary, then rebuild the adapter.
"""
from __future__ import annotations

from typing import Callable, Mapping

DRIVE_FILE_SCOPE = "https://www.googleapis.com/auth/drive.file"
GOOGLE_TOKEN_URI = "https://oauth2.googleapis.com/token"


class DriveFactoryError(RuntimeError):
    """Sanitized failure constructing an authorized Drive client."""


def build_user_drive_adapter(
    credential: Mapping[str, object],
    *,
    client_id: str,
    client_secret: str,
    parent_id: str,
    adapter_factory: Callable,
    credentials_factory: Callable | None = None,
    google_build: Callable | None = None,
    scopes: tuple[str, ...] = (DRIVE_FILE_SCOPE,),
):
    """Build an adapter bound to one user's OAuth access token.

    The caller MUST perform Work/user authorization before passing the
    credential. Refresh tokens are deliberately not passed to Google SDK
    Credentials; refresh must go through ConnectionManager.
    """
    if not isinstance(credential, Mapping):
        raise DriveFactoryError("OAuth credential unavailable")
    if not all(isinstance(v, str) and v.strip() for v in
               (credential.get("access_token"), client_id, client_secret, parent_id)):
        raise DriveFactoryError("OAuth Drive configuration incomplete")
    if DRIVE_FILE_SCOPE not in scopes:
        raise DriveFactoryError("least-privilege drive.file scope is required")

    granted = credential.get("scopes")
    if granted and DRIVE_FILE_SCOPE not in granted:
        raise DriveFactoryError("Google connection lacks drive.file permission")

    try:
        if credentials_factory is None:
            from google.oauth2.credentials import Credentials
            credentials_factory = Credentials
        if google_build is None:
            from googleapiclient.discovery import build
            google_build = build

        credentials = credentials_factory(
            token=credential["access_token"],
            # Intentionally omit refresh_token: SDK-managed refresh would
            # bypass ConnectionManager's per-connection single-flight lock.
            token_uri=GOOGLE_TOKEN_URI,
            client_id=client_id,
            client_secret=client_secret,
            scopes=list(scopes),
        )
        service = google_build("drive", "v3", credentials=credentials,
                               cache_discovery=False)
        return adapter_factory(service, parent_id=parent_id)
    except DriveFactoryError:
        raise
    except ImportError:
        raise DriveFactoryError("Google API dependencies are not installed") from None
    except Exception:
        raise DriveFactoryError("Google Drive client could not be initialized") from None


def build_connection_bound_drive_adapter(
    manager,
    room_id: str,
    user_id: str,
    connection_id: str,
    *,
    client_id: str,
    client_secret: str,
    parent_id: str,
    adapter_factory: Callable,
    credentials_factory: Callable | None = None,
    google_build: Callable | None = None,
):
    """Resolve the exact owner's credential, then build the Drive adapter."""
    try:
        credential = manager.credential_for_operation(room_id, user_id, connection_id)
    except Exception:
        raise DriveFactoryError("Google connection is not authorized for this user and Work") from None
    return build_user_drive_adapter(
        credential,
        client_id=client_id,
        client_secret=client_secret,
        parent_id=parent_id,
        adapter_factory=adapter_factory,
        credentials_factory=credentials_factory,
        google_build=google_build,
        scopes=(DRIVE_FILE_SCOPE,),
    )


def refresh_connection_bound_drive_adapter(
    manager,
    room_id: str,
    user_id: str,
    connection_id: str,
    *,
    failed_access_token: str,
    client_id: str,
    client_secret: str,
    parent_id: str,
    adapter_factory: Callable,
    credentials_factory: Callable | None = None,
    google_build: Callable | None = None,
):
    """Refresh through ConnectionManager, then rebuild the Drive adapter.

    Call only in response to one 401 for the current upload/API operation.
    The caller owns the one-replay budget: after this function returns a new
    adapter, replay the original operation at most once. Never call this again
    for a second 401. The failed token is passed as the stale-call marker so
    concurrent requests can reuse a refresh winner under RT-06.
    """
    if not isinstance(failed_access_token, str) or not failed_access_token:
        raise DriveFactoryError("failed access token marker is required")
    try:
        manager.refresh(
            room_id,
            user_id,
            connection_id,
            expected_access_token=failed_access_token,
        )
        credential = manager.credential_for_operation(
            room_id, user_id, connection_id
        )
    except Exception:
        # ConnectionManager owns the typed refresh/reauth error contract.
        # Do not expose token-store/provider details through this factory.
        raise
    return build_user_drive_adapter(
        credential,
        client_id=client_id,
        client_secret=client_secret,
        parent_id=parent_id,
        adapter_factory=adapter_factory,
        credentials_factory=credentials_factory,
        google_build=google_build,
        scopes=(DRIVE_FILE_SCOPE,),
    )
