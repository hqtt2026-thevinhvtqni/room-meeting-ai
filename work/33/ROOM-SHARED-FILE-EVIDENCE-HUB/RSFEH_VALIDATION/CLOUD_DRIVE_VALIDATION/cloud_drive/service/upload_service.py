"""Fail-closed application service wrapping resumable upload operations."""
from __future__ import annotations

from typing import BinaryIO

from ..storage.protocol import StoredObject
from ..uploads.session_manager import UploadSession, UploadSessionManager
from .authorization import Authorizer, Principal, AuthorizationDenied
from .audit import AuditWriteError


class UploadService:
    """Enforces an authorization check before each upload-session operation.

    The principal must come from a verified authentication layer, never from a
    caller-controlled agent-name or free-form request field.
    """

    def __init__(self, sessions: UploadSessionManager, authorizer: Authorizer):
        self.sessions = sessions
        self.authorizer = authorizer
        if self.sessions.audit_writer is None:
            raise ValueError("UploadService requires transactional audit to be configured")

    def _authorize(self, *, principal: Principal, scope_id: str, action: str) -> None:
        """Record every authorization decision; fail closed if its audit cannot be stored."""
        audit = self.sessions.audit_writer
        try:
            self.authorizer.authorize(principal=principal, scope_id=scope_id, action=action)
        except AuthorizationDenied:
            audit.append(actor_id=principal.subject_id, action="AUTHORIZATION_DENIED",
                         resource_type="scope", resource_id=scope_id, outcome="DENY",
                         detail={"requested_action": action})
            raise
        except Exception as exc:
            audit.append(actor_id=principal.subject_id, action="AUTHORIZATION_ERROR",
                         resource_type="scope", resource_id=scope_id, outcome="ERROR",
                         detail={"requested_action": action, "error_type": type(exc).__name__})
            raise AuthorizationDenied("authorization could not be completed") from exc
        audit.append(actor_id=principal.subject_id, action="AUTHORIZATION_ALLOWED",
                     resource_type="scope", resource_id=scope_id, outcome="ALLOW",
                     detail={"requested_action": action})

    def begin(
        self, *, principal: Principal, scope_id: str, expected_size: int,
        expected_sha256: str | None = None,
    ) -> UploadSession:
        self._authorize(principal=principal, scope_id=scope_id, action="object:create")
        return self.sessions.begin_upload(
            scope_id=scope_id, expected_size=expected_size, expected_sha256=expected_sha256,
            actor_id=principal.subject_id
        )

    def put_part(
        self, *, principal: Principal, scope_id: str, session_id: str,
        part_number: int, source: BinaryIO,
    ) -> dict[str, int | str]:
        self._authorize(principal=principal, scope_id=scope_id, action="object:upload")
        return self.sessions.put_part(
            session_id=session_id, scope_id=scope_id, part_number=part_number, source=source,
            actor_id=principal.subject_id
        )

    def list_parts(
        self, *, principal: Principal, scope_id: str, session_id: str,
    ) -> list[dict[str, int | str]]:
        self._authorize(principal=principal, scope_id=scope_id, action="object:read")
        result = self.sessions.list_parts(session_id=session_id, scope_id=scope_id)
        self.sessions.audit_writer.append(
            actor_id=principal.subject_id, action="UPLOAD_PARTS_LISTED",
            resource_type="upload", resource_id=session_id, outcome="SUCCESS",
            detail={"scope_id": scope_id, "part_count": len(result)},
        )
        return result

    def complete(
        self, *, principal: Principal, scope_id: str, session_id: str,
    ) -> StoredObject:
        self.authorizer.authorize(principal=principal, scope_id=scope_id, action="object:upload")
        return self.sessions.complete_upload(session_id=session_id, scope_id=scope_id, actor_id=principal.subject_id)

    def abort(
        self, *, principal: Principal, scope_id: str, session_id: str,
    ) -> None:
        self._authorize(principal=principal, scope_id=scope_id, action="object:delete")
        self.sessions.abort_upload(session_id=session_id, scope_id=scope_id, actor_id=principal.subject_id)
