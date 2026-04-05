from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger(__name__)

async def integrity_error_handler(request: Request, exc: IntegrityError):
    """
    Catch global database integrity constraints, like Foreign Key violations,
    so the application does not crash and returns a clean 400 Bad Request.
    """
    logger.error(f"Integrity Error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Database constraint violation. Check foreign keys and unique constraints."},
    )

async def generic_exception_handler(request: Request, exc: Exception):
    """
    Fallback for any unhandled internal server exceptions.
    """
    logger.error(f"Unhandled Exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected internal server error occurred."},
    )
