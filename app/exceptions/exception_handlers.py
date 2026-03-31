from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging

from app.exceptions.custom_exceptions import AppException

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(_: Request, exc: AppException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle Pydantic validation errors with helpful messages"""
        errors = []
        for error in exc.errors():
            field = ".".join(str(x) for x in error["loc"][1:])
            msg = error["msg"]
            errors.append(f"{field}: {msg}")
        
        detail = f"Validation error: {'; '.join(errors)}"
        logger.warning(f"Validation error from {request.method} {request.url}: {detail}")
        
        return JSONResponse(
            status_code=422,
            content={
                "detail": detail,
                "errors": [
                    {
                        "field": ".".join(str(x) for x in error["loc"][1:]),
                        "message": error["msg"],
                        "type": error["type"]
                    }
                    for error in exc.errors()
                ]
            }
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(_: Request, exc: Exception):
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
        return JSONResponse(status_code=500, content={"detail": str(exc)})
