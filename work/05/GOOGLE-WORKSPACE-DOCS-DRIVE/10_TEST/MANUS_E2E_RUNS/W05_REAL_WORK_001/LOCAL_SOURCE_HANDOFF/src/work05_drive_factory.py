"""Trusted OAuth-user -> Google Drive API v3 factory for Work 05.

Call only after ConnectionManager.credential_for_operation(room_id, user_id,
connection_id) has authorized the caller. Client secret comes from secure
runtime configuration, never from a browser request or the credential record.
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
    """Build an adapter bound to one user's OAuth token.

    The caller MUST perform Work/user authorization before passing the
    credential. This function does not accept arbitrary connection IDs and
    does not perform authorization itself.
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
            refresh_token=credential.get("refresh_token"),
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
