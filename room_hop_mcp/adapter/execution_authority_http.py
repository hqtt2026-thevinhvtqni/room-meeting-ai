"""HTTP routes for Core-owned Work execution grants and run records."""
from __future__ import annotations

import re
from typing import Any

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from core.execution_authority import ExecutionAuthority, ExecutionAuthorityConfigError

_SHA256 = re.compile(r"^[0-9a-f]{64}$")


class GrantRequest(BaseModel):
    purpose: str = Field(min_length=1, max_length=64)
    max_timeout_seconds: int = Field(default=60, ge=1, le=900)


class RunRecordRequest(BaseModel):
    source_sha256: str
    exit_status: str
    output_refs: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    handoff_ids: list[str] = Field(default_factory=list)


def mount_execution_authority_routes(app: FastAPI, authority: ExecutionAuthority | None) -> None:
    """Mount fail-closed routes; unavailable configuration returns 503."""

    def configured() -> ExecutionAuthority:
        if authority is None:
            raise HTTPException(status_code=503, detail="execution_authority_not_configured")
        return authority

    def bearer(value: str | None) -> str:
        if not value or not value.startswith("Bearer ") or not value[7:].strip():
            raise HTTPException(status_code=401, detail="execution_grant_invalid")
        return value[7:].strip()

    @app.post("/works/{work_id}/execution-grants")
    def issue_execution_grant(
        work_id: str,
        body: GrantRequest,
        service_credential: str | None = Header(default=None, alias="X-ROOM-HOP-SERVICE-CREDENTIAL"),
    ) -> dict[str, Any]:
        core = configured()
        try:
            identity = core.authenticate(service_credential)
            if not core.is_identity_allowed_for_work(identity, work_id):
                raise HTTPException(status_code=403, detail="caller_not_authorized_for_work")
            grant = core.issue_grant(identity, work_id, body.purpose, body.max_timeout_seconds)
            # Token is returned once over the authenticated private transport.
            # Callers must keep it in memory and never log it.
            return grant
        except KeyError:
            raise HTTPException(status_code=404, detail="unknown_work") from None
        except PermissionError as exc:
            code = str(exc)
            status = 401 if code == "caller_authentication_failed" else 403
            raise HTTPException(status_code=status, detail=code) from None
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from None

    @app.get("/works/{work_id}/execution-grants/{grant_id}")
    def get_execution_grant_status(
        work_id: str,
        grant_id: str,
        service_credential: str | None = Header(default=None, alias="X-ROOM-HOP-SERVICE-CREDENTIAL"),
    ) -> dict[str, Any]:
        core = configured()
        try:
            identity = core.authenticate(service_credential)
            result = core.get_grant_status(grant_id)
            if result["work_id"] != work_id or result["identity"] != identity:
                raise HTTPException(status_code=403, detail="execution_grant_work_mismatch_or_identity_mismatch")
            return result
        except KeyError:
            raise HTTPException(status_code=404, detail="unknown_grant") from None
        except PermissionError as exc:
            raise HTTPException(status_code=401, detail=str(exc)) from None

    @app.get("/works/{work_id}/execution-grants/{grant_id}/validate")
    def validate_execution_grant(
        work_id: str,
        grant_id: str,
        authorization: str | None = Header(default=None, alias="Authorization"),
    ) -> dict[str, Any]:
        core = configured()
        try:
            result = core.validate_grant_token(grant_id, bearer(authorization))
            if result["work_id"] != work_id:
                raise HTTPException(status_code=403, detail="execution_grant_work_mismatch")
            return result
        except KeyError:
            raise HTTPException(status_code=404, detail="unknown_grant") from None
        except PermissionError as exc:
            raise HTTPException(status_code=403, detail=str(exc)) from None

    @app.post("/works/{work_id}/execution-grants/{grant_id}/runs")
    def record_execution_run(
        work_id: str,
        grant_id: str,
        body: RunRecordRequest,
        authorization: str | None = Header(default=None, alias="Authorization"),
    ) -> dict[str, Any]:
        core = configured()
        token = bearer(authorization)
        try:
            grant = core.validate_grant_token(grant_id, token)
            if grant["work_id"] != work_id:
                raise HTTPException(status_code=403, detail="execution_grant_work_mismatch")
            if not _SHA256.fullmatch(body.source_sha256):
                raise HTTPException(status_code=400, detail="invalid_source_sha256")
            return core.record_run(
                grant_id,
                grant_token=token,
                source_sha256=body.source_sha256,
                exit_status=body.exit_status,
                output_refs=body.output_refs,
                evidence_refs=body.evidence_refs,
                handoff_ids=body.handoff_ids,
            )
        except KeyError:
            raise HTTPException(status_code=404, detail="unknown_grant") from None
        except PermissionError as exc:
            raise HTTPException(status_code=403, detail=str(exc)) from None
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from None

    @app.post("/works/{work_id}/execution-grants/{grant_id}/revoke")
    def revoke_execution_grant(
        work_id: str,
        grant_id: str,
        authorization: str | None = Header(default=None, alias="Authorization"),
    ) -> dict[str, Any]:
        core = configured()
        token = bearer(authorization)
        try:
            grant = core.validate_grant_token(grant_id, token)
            if grant["work_id"] != work_id:
                raise HTTPException(status_code=403, detail="execution_grant_work_mismatch")
            return core.revoke_grant(grant_id)
        except KeyError:
            raise HTTPException(status_code=404, detail="unknown_grant") from None
        except PermissionError as exc:
            raise HTTPException(status_code=403, detail=str(exc)) from None
