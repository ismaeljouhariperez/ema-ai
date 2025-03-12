from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from loguru import logger
from typing import Dict, Any, Optional

class EmaAIException(HTTPException):
    """Base exception for EMA-AI service"""
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str = "INTERNAL_ERROR",
        headers: Optional[Dict[str, Any]] = None
    ):
        self.error_code = error_code
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class PromptProcessingError(EmaAIException):
    """Exception raised when there's an error processing a prompt"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=500,
            detail=detail,
            error_code="PROMPT_PROCESSING_ERROR"
        )

class OpenAIError(EmaAIException):
    """Exception raised when there's an error with OpenAI API"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=503,
            detail=detail,
            error_code="OPENAI_API_ERROR"
        )

class InvalidPromptError(EmaAIException):
    """Exception raised when the prompt is invalid"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=400,
            detail=detail,
            error_code="INVALID_PROMPT"
        )

class AdventureNotFoundError(EmaAIException):
    """Exception raised when an adventure is not found"""
    def __init__(self, adventure_id: int):
        super().__init__(
            status_code=404,
            detail=f"Adventure with ID {adventure_id} not found",
            error_code="ADVENTURE_NOT_FOUND"
        )

async def ema_exception_handler(request: Request, exc: EmaAIException) -> JSONResponse:
    """
    Custom exception handler for EMA-AI exceptions
    Returns a consistent JSON response for all exceptions
    """
    logger.error(f"EMA-AI Exception: {exc.error_code} - {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "code": exc.error_code,
            "message": exc.detail,
            "path": request.url.path
        }
    ) 