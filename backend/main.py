"""
Main FastAPI application entry point
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import logging
import sys

from config import settings
from database import init_db
from routes import router
from limiter import limiter

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API for Clovix landing page prospect management",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# Setup rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        init_db()
        logger.info(f"Application started in {settings.environment} mode")
        logger.info(f"Database: {settings.database_path}")
        if settings.api_key:
            logger.info("API key authentication enabled")
        else:
            logger.warning("API key not set - admin endpoints are open")
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        raise


# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "environment": settings.environment
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy"}


# Include routers
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower()
    )
