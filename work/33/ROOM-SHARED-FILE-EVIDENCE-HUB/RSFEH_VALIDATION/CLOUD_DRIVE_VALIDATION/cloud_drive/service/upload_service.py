"""Fail-closed application service wrapping resumable upload operations."""
from __future__ import annotations

from typing import BinaryIO

from ..storage.protocol import StoredObject
from ..uploads.session_manager import UploadSession, UploadSessionManager
from .authorization import Authorizer, Principal


class UploadService:
    """Enforces an authorization check before each upload-session operation.

    The principal must come from a verified authentication layer, never from a
    caller-controlled agent-name or free-form request field.
    """

    def __init__(self, sessions: UploadSessionManager, authorizer: Authorizer):
        self.sessions = sessions
        self.authorizer = authorizer

    def begin(
        self, *, principal: Principal, scope_id: str, expected_size: int,
        expected_sha256: str | None = None,
    ) -> UploadSession:
        self.authorizer.authorize(principal=principal, scope_id=scope_id, action="object:create")
        return self.sessions.begin_upload(
            scope_id=scope_id, expected_size=expected_size, expected_sha256=expected_sha256,
            actor_id=principal.subject_id
        )

    def put_part(
        self, *, principal: Principal, scope_id: str, session_id: str,
        part_number: int, source: BinaryIO,
    ) -> dict[str, int | str]:
        self.authorizer.authorize(principal=principal, scope_id=scope_id, action="object:upload")
        return self.sessions.put_part(
            session_id=session_id, scope_id=scope_id, part_number=part_number, source=source,
            actor_id=principal.subject_id
        )

    def list_parts(
        self, *, principal: Principal, scope_id: str, session_id: str,
    ) -> list[dict[str, int | str]]:
        self.authorizer.authorize(principal=principal, scope_id=scope_id, action="object:read")
        return self.sessions.list_parts(session_id=session_id, scope_id=scope_id)

    def complete(
        self, *, principal: Principal, scope_id: str, session_id: str,
    ) -> StoredObject:
        self.authorizer.authorize(principal=principal, scope_id=scope_id, action="object:upload")
        return self.sessions.complete_upload(session_id=session_id, scope_id=scope_id, actor_id=principal.subject_id)

    def abort(
        self, *, principal: Principal, scope_id: str, session_id: str,
    ) -> None:
        self.authorizer.authorize(principal=principal, scope_id=scope_id, action="object:delete")
        self.sessions.abort_upload(session_id=session_id, scope_id=scope_id, actor_id=principal.subject_id)
