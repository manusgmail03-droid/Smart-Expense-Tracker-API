"""Main FastAPI application entrypoint for Smart Expense Tracker API."""

import logging
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.routes import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("smart-expense-tracker")

app = FastAPI(
    title="Smart Expense Tracker API",
    description="A production-quality REST API for tracking personal expenses with local JSON storage.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Map FastAPI/Pydantic validation errors to HTTP 400 Bad Request."""
    errors = exc.errors()
    # Format a clean detail message for invalid input
    error_messages = []
    for err in errors:
        loc = " -> ".join(str(loc_item) for loc_item in err.get("loc", []))
        msg = err.get("msg", "Invalid value")
        error_messages.append(f"{loc}: {msg}")

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": error_messages[0] if len(error_messages) == 1 else error_messages},
    )


@app.exception_handler(Exception)
async def general_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Catch-all exception handler returning HTTP 500 for unexpected failures."""
    logger.error(f"Unexpected server error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected internal server error occurred."},
    )


@app.get("/", tags=["Health Check"])
def root() -> dict:
    """Root status endpoint providing API metadata and docs link."""
    return {
        "name": "Smart Expense Tracker API",
        "status": "online",
        "documentation": "/docs",
    }
