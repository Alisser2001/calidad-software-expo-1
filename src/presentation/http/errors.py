from __future__ import annotations
from typing import Any, Dict
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from domain.exceptions import (
    DomainError, 
    ValidationError, 
    NotFoundError
)
from application.exceptions import (
    ApplicationError, 
    OrchestrationError
)

import logging
logger = logging.getLogger("app.presentation.http.errors")

def _problem(status: int, title: str, detail: str, type: str, extra: Dict[str, Any] | None = None):
    payload = {
        "type": type,
        "title": title,
        "status": status,
        "detail": detail,
    }
    if extra:
        payload["extra"] = extra
    return payload

def add_exception_handlers(app: FastAPI) -> None:
    # DOMAIN
    @app.exception_handler(ValidationError)
    async def domain_validation_handler(_: Request, exc: ValidationError):
        logger.info("Domain validation error: %s", exc.message, extra=getattr(exc, "extra", None))
        return JSONResponse(
            status_code=422,
            content=_problem(422, "Validation error", exc.message, exc.code, getattr(exc, "extra", None))
        )

    @app.exception_handler(NotFoundError)
    async def domain_not_found_handler(_: Request, exc: NotFoundError):
        logger.info("Domain not found: %s", exc.message)
        return JSONResponse(
            status_code=404,
            content=_problem(404, "Not found", exc.message, exc.code, getattr(exc, "extra", None))
        )

    @app.exception_handler(DomainError)
    async def domain_generic_handler(_: Request, exc: DomainError):
        logger.warning("Domain error: %s", exc.message)
        return JSONResponse(
            status_code=400,
            content=_problem(400, "Domain error", exc.message, exc.code, getattr(exc, "extra", None))
        )

    # APPLICATION
    @app.exception_handler(OrchestrationError)
    async def app_orchestration_handler(_: Request, exc: OrchestrationError):
        logger.error("Orchestration error: %s", exc.message, exc_info=True)
        return JSONResponse(
            status_code=500,
            content=_problem(500, "Orchestration error", exc.message, exc.code, getattr(exc, "extra", None))
        )

    @app.exception_handler(ApplicationError)
    async def app_generic_handler(_: Request, exc: ApplicationError):
        logger.error("Application error: %s", exc.message, exc_info=True)
        return JSONResponse(
            status_code=500,
            content=_problem(500, "Application error", exc.message, exc.code, getattr(exc, "extra", None))
        )

    # FASTAPI
    @app.exception_handler(RequestValidationError)
    async def request_validation_handler(_: Request, exc: RequestValidationError):
        logger.info("Request validation: %s", exc)
        return JSONResponse(
            status_code=422,
            content=_problem(
                422, 
                "Request validation error", 
                "Invalid request body or params", 
                "request_validation_error", 
                {"errors": exc.errors()}
            )
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(_: Request, exc: StarletteHTTPException):
        logger.info("HTTP exception: %s", exc.detail)
        return JSONResponse(
            status_code=exc.status_code,
            content=_problem(exc.status_code, "HTTP error", str(exc.detail), "http_error")
        )

    # FALLBACK
    @app.exception_handler(Exception)
    async def unhandled_handler(_: Request, exc: Exception):
        logger.exception("Unhandled error")
        return JSONResponse(
            status_code=500,
            content=_problem(500, "Internal server error", "Unexpected error", "internal_server_error")
        )