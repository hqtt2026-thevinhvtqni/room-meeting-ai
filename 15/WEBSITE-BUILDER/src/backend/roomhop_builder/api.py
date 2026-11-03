"""HTTP contract for the Work 15 backend (issue #34, part A).

FastAPI app factory. Contains **no business logic**: it validates request
shape via Pydantic models, calls ``BuilderService``, and maps domain errors
to stable JSON error responses — the same discipline as the locked Core
contract (``API_CONTRACT.md`` §1).

Error envelope (all non-2xx):

    {"error": {"code": "...", "message": "...", "details": {...}}}

Endpoint summary
----------------
GET  /health                     liveness + wired ports (never claims PASS)
POST /v1/websites/jobs           create a build job (QUEUED)
GET  /v1/websites/jobs?state=    list jobs, optional state filter
GET  /v1/websites/jobs/{id}      job detail incl. transition history
POST /v1/websites/jobs/{id}/transitions  guarded lifecycle move
POST /v1/websites/jobs/{id}/run          orchestrate builder+runtime (dev trigger)
GET  /v1/websites/jobs/{id}/evidence     evidence manifest
POST /v1/websites/jobs/{id}/evidence     append one evidence record
GET  /v1/websites/jobs/{id}/runtime      live runtime probe
"""

from __future__ import annotations

from typing import Any, Literal, Optional

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

from .errors import BuilderError, ValidationError
from .jobs import JobState, MAX_INTENT_LENGTH, MAX_SITE_NAME_LENGTH
from .service import BuilderService

StateLiteral = Literal["QUEUED", "RUNNING", "SUCCEEDED", "FAILED", "BLOCKED"]
EvidenceKindLiteral = Literal["diff", "log", "preview", "e2e", "runtime_status", "note"]


# ---------------------------------------------------------------------------
# Request/response models — the machine-readable API contract.
# ---------------------------------------------------------------------------


class CreateJobRequest(BaseModel):
    model_config = {"extra": "forbid"}

    intent: str = Field(min_length=1, max_length=MAX_INTENT_LENGTH,
                        description="natural-language website request")
    site_name: str = Field(min_length=1, max_length=MAX_SITE_NAME_LENGTH)
    created_by: str = Field(min_length=1, max_length=MAX_SITE_NAME_LENGTH,
                            description="identity id from Principal/Agent registry; never inferred")

    @field_validator("intent", "site_name", "created_by")
    @classmethod
    def _not_blank(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("must not be blank")
        return stripped


class CreateJobResponse(BaseModel):
    id: str
    state: StateLiteral
    terminal: bool
    created_at: str
    intent: str
    site_name: str
    created_by: str


class TransitionRequest(BaseModel):
    model_config = {"extra": "forbid"}

    to: StateLiteral
    reason: str = Field(min_length=1, max_length=1000)
    error: Optional[str] = None

    @field_validator("reason")
    @classmethod
    def _reasonNotBlank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("reason must not be blank")
        return value.strip()


class RunRequest(BaseModel):
    model_config = {"extra": "forbid"}

    e2e_summary: Optional[str] = Field(
        default=None, max_length=2000,
        description="result of an ACTUAL end-to-end verification run; "
                    "without it the job cannot reach SUCCEEDED",
    )


class EvidenceRequest(BaseModel):
    model_config = {"extra": "forbid"}

    kind: EvidenceKindLiteral
    summary: str = Field(min_length=1, max_length=2000)
    payload: dict[str, Any] = Field(default_factory=dict)

    @field_validator("summary")
    @classmethod
    def _summaryNotBlank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("summary must not be blank")
        return value.strip()


# ---------------------------------------------------------------------------
# App factory.
# ---------------------------------------------------------------------------


def create_app(service: Optional[BuilderService] = None) -> FastAPI:
    app = FastAPI(
        title="Room Hop Website Builder — Backend Foundation",
        version="0.1.0",
        summary="Work 15 / issue #34. Contract-first, evidence-gated.",
    )
    app.state.service = service or BuilderService()

    # -- error mapping ------------------------------------------------------

    @app.exception_handler(BuilderError)
    async def _domain_error(_request: Request, exc: BuilderError) -> JSONResponse:
        return JSONResponse(status_code=exc.http_status, content={"error": exc.to_dict()})

    # Pydantic validation failures get reshaped into the same envelope so
    # clients only ever parse one error format.
    from fastapi.exceptions import RequestValidationError

    @app.exception_handler(RequestValidationError)
    async def _request_invalid(_request: Request, exc: RequestValidationError) -> JSONResponse:
        problems = [
            {"field": ".".join(str(p) for p in err.get("loc", [])[1:]), "problem": err.get("msg")}
            for err in exc.errors()
        ]
        payload = ValidationError("request body/params failed contract validation",
                                  details={"problems": problems}).to_dict()
        return JSONResponse(status_code=422, content={"error": payload})

    # -- routes -------------------------------------------------------------

    def svc() -> BuilderService:
        return app.state.service

    @app.get("/health")
    def health() -> dict[str, Any]:
        s = svc()
        return {
            "component": "work15-backend",
            "version": "0.1.0",
            "builder_port": s.builder.name,
            "runtime_port": s.runtime.name,
            "code_version": s.code_version,
            "wired_for_execution": s.builder.name not in ("null-builder",)
            and s.runtime.name not in ("refused-runtime",),
        }

    @app.post("/v1/websites/jobs", response_model=CreateJobResponse, status_code=201)
    def create_job(body: CreateJobRequest) -> Any:
        job = svc().create_job(body.model_dump())
        return job.to_dict()

    @app.get("/v1/websites/jobs")
    def list_jobs(state: Optional[str] = None) -> dict[str, Any]:
        jobs = svc().list_jobs(state)
        return {"count": len(jobs), "jobs": [j.to_dict() for j in jobs]}

    @app.get("/v1/websites/jobs/{job_id}")
    def get_job(job_id: str) -> dict[str, Any]:
        return svc().get_job(job_id).to_dict()

    @app.post("/v1/websites/jobs/{job_id}/transitions")
    def transition(job_id: str, body: TransitionRequest) -> dict[str, Any]:
        job = svc().jobs.transition(
            job_id, JobState(body.to), reason=body.reason, error=body.error
        )
        return job.to_dict()

    @app.post("/v1/websites/jobs/{job_id}/run")
    def run_job(job_id: str, body: Optional[RunRequest] = None) -> dict[str, Any]:
        outcome = svc().run_job(job_id, e2e_summary=(body.e2e_summary if body else None))
        return {
            "note": outcome.note,
            "job": outcome.job.to_dict(),
            "build": outcome.build.to_dict() if outcome.build else None,
            "runtime": outcome.runtime,
        }

    @app.get("/v1/websites/jobs/{job_id}/evidence")
    def evidence_manifest(job_id: str) -> dict[str, Any]:
        return svc().evidence_manifest(job_id)

    @app.post("/v1/websites/jobs/{job_id}/evidence", status_code=201)
    def add_evidence(job_id: str, body: EvidenceRequest) -> dict[str, Any]:
        return svc().add_evidence(job_id, body.kind, summary=body.summary, payload=body.payload)

    @app.get("/v1/websites/jobs/{job_id}/runtime")
    def runtime_status(job_id: str) -> dict[str, Any]:
        return svc().runtime_status(job_id)

    return app
