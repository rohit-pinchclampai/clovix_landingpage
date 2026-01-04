"""
Middleware for authentication and security
"""
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from config import settings
import logging

logger = logging.getLogger(__name__)

# API Key authentication for admin endpoints
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    Verify API key for admin endpoints
    
    In production, you should use a proper authentication system.
    For now, this is a simple API key check.
    """
    if not settings.api_key:
        # If no API key is set, allow access (development mode)
        logger.warning("API_KEY not set - allowing access (development mode)")
        return "dev"
    
    if not api_key or api_key != settings.api_key:
        logger.warning(f"Invalid API key attempt")
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )
    
    return api_key



