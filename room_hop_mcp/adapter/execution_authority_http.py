from __future__ import annotations

from typing import Any, Literal

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from core.execution_authority import AuthorityError, ExecutionAuthority


class GrantIssueRequest(BaseModel):
    purpose: str = Field(min_length=1, max_length=64)
    repository: str = Field(min_length=3, max_length=256)
    branch: str = Field(min_length=1, max_length=256)
    expected_head: str = Field(min_length=40, max_length=64)
    assignment_id: str = Field(min_length=1, max_length=128)
    task_id: str = Field(min_length=1, max_length=128)
    host_identity_id: str = Field(min_length=1, max_length=128)
    source_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    environment_id: str = Field(min_length=1, max_length=128)
    test_entrypoint: list[str]
    requested_timeout_seconds: int | None = Field(default=None, ge=1, le=3600)

    model_config = ConfigDict(extra="forbid")


class RunStartRequest(BaseModel):
    run_id: str = Field(min_length=1, max_length=128)
    repository: str = Field(min_length=3, max_length=256)
    branch: str = Field(min_length=1, max_length=256)
    expected_head: str = Field(min_length=40, max_length=64)
    command: list[str]
    source_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    environment_id: str = Field(min_length=1, max_length=128)
    started_at: str

    model_config = ConfigDict(extra="forbid")


class RunCompleteRequest(BaseModel):
    run_id: str = Field(min_length=1, max_length=128)
    finished_at: str
    status: Literal["PASS", "FAILED", "TIMEOUT", "BLOCKED"]
    exit_code: int | None
    evidence_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    evidence_ref: str | None = None
    stdout_sha256: str | None = None
    stderr_sha256: str | None = None

    model_config = ConfigDict(extra="forbid")


def create_execution_authority_router(
    authority: ExecutionAuthority | None,
) -> APIRouter:
    router = APIRouter()

    def require_authority() -> ExecutionAuthority:
        if authority is None:
            raise HTTPException(
                status_code=503,
                detail="execution_authority_not_configured",
            )
        return authority

    def invoke(callable_, *args, **kwargs) -> Any:
        try:
            return callable_(*args, **kwargs)
        except AuthorityError as exc:
            raise HTTPException(
                status_code=exc.status_code,
                detail=exc.code,
            ) from None

    @router.post("/works/{work_id}/execution-grants")
    def issue_grant(
        work_id: str,
        body: dict[str, Any],
        x_room_hop_service_id: str | None = Header(default=None),
        x_room_hop_service_credential: str | None = Header(default=None),
    ) -> dict[str, Any]:
        service = require_authority()
        try:
            request_body = GrantIssueRequest.model_validate(body)
        except Exception:
            raise HTTPException(status_code=422, detail="execution_grant_request_invalid") from None
        return invoke(
            service.issue_grant,
            work_id=work_id,
            service_id=x_room_hop_service_id or "",
            credential=x_room_hop_service_credential or "",
            request=request_body.model_dump(),
        )

    @router.get("/works/{work_id}/execution-grants/{grant_id}")
    def grant_status(
        work_id: str,
        grant_id: str,
        x_room_hop_service_id: str | None = Header(default=None),
        x_room_hop_service_credential: str | None = Header(default=None),
    ) -> dict[str, Any]:
        service = require_authority()
        return invoke(
            service.grant_status,
            work_id=work_id,
            grant_id=grant_id,
            service_id=x_room_hop_service_id or "",
            credential=x_room_hop_service_credential or "",
        )

    @router.get("/works/{work_id}/execution-grants/{grant_id}/validate")
    def validate_grant(
        work_id: str,
        grant_id: str,
        authorization: str | None = Header(default=None),
        x_room_hop_service_id: str | None = Header(default=None),
        x_room_hop_service_credential: str | None = Header(default=None),
    ) -> dict[str, Any]:
        service = require_authority()
        scheme, _, token = (authorization or "").partition(" ")
        if scheme.lower() != "bearer" or not token:
            raise HTTPException(status_code=401, detail="grant_bearer_required")
        return invoke(
            service.validate_grant,
            work_id=work_id,
            grant_id=grant_id,
            token=token,
            host_service_id=x_room_hop_service_id or "",
            host_credential=x_room_hop_service_credential or "",
        )

    @router.post("/works/{work_id}/execution-grants/{grant_id}/runs")
    def start_run(
        work_id: str,
        grant_id: str,
        body: dict[str, Any],
        authorization: str | None = Header(default=None),
        x_room_hop_service_id: str | None = Header(default=None),
        x_room_hop_service_credential: str | None = Header(default=None),
    ) -> dict[str, Any]:
        service = require_authority()
        try:
            request_body = RunStartRequest.model_validate(body)
        except Exception:
            raise HTTPException(status_code=422, detail="execution_run_start_invalid") from None
        scheme, _, token = (authorization or "").partition(" ")
        if scheme.lower() != "bearer" or not token:
            raise HTTPException(status_code=401, detail="grant_bearer_required")
        return invoke(
            service.start_run,
            work_id=work_id,
            grant_id=grant_id,
            token=token,
            host_service_id=x_room_hop_service_id or "",
            host_credential=x_room_hop_service_credential or "",
            record=request_body.model_dump(),
        )

    @router.post("/works/{work_id}/execution-grants/{grant_id}/runs/{run_id}/complete")
    def complete_run(
        work_id: str,
        grant_id: str,
        run_id: str,
        body: dict[str, Any],
        authorization: str | None = Header(default=None),
        x_room_hop_service_id: str | None = Header(default=None),
        x_room_hop_service_credential: str | None = Header(default=None),
    ) -> dict[str, Any]:
        service = require_authority()
        if "run_id" in body and body["run_id"] != run_id:
            raise HTTPException(
                status_code=422,
                detail="execution_run_id_mismatch",
            )
        try:
            request_body = RunCompleteRequest.model_validate({**body, "run_id": run_id})
        except Exception:
            raise HTTPException(status_code=422, detail="execution_run_completion_invalid") from None
        scheme, _, token = (authorization or "").partition(" ")
        if scheme.lower() != "bearer" or not token:
            raise HTTPException(status_code=401, detail="grant_bearer_required")
        return invoke(
            service.complete_run,
            work_id=work_id,
            grant_id=grant_id,
            token=token,
            host_service_id=x_room_hop_service_id or "",
            host_credential=x_room_hop_service_credential or "",
            record=request_body.model_dump(),
        )

    @router.post("/works/{work_id}/execution-grants/{grant_id}/revoke")
    def revoke_grant(
        work_id: str,
        grant_id: str,
        x_room_hop_service_id: str | None = Header(default=None),
        x_room_hop_service_credential: str | None = Header(default=None),
    ) -> dict[str, Any]:
        service = require_authority()
        return invoke(
            service.revoke_grant,
            work_id=work_id,
            grant_id=grant_id,
            service_id=x_room_hop_service_id or "",
            credential=x_room_hop_service_credential or "",
        )

    return router
