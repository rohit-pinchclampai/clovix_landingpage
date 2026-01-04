"""
API routes for the Clovix backend
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List
import logging
from datetime import datetime
from models import ProspectCreate, ProspectResponse, ProspectStats
from database import get_db
from middleware import verify_api_key
from config import settings
from limiter import limiter

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["prospects"])


@router.post("/prospects", response_model=ProspectResponse, status_code=201)
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
async def create_prospect(request: Request, prospect: ProspectCreate):
    """
    Create a new prospect registration
    
    - **name**: Full name of the prospect
    - **companyName**: Company name
    - **email**: Email address (must be unique)
    """
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Check if email already exists
            cursor.execute("SELECT id FROM prospects WHERE email = ?", (prospect.email,))
            existing = cursor.fetchone()
            
            if existing:
                logger.info(f"Duplicate registration attempt for email: {prospect.email}")
                raise HTTPException(
                    status_code=400,
                    detail="Email already registered"
                )
            
            # Insert new prospect
            cursor.execute("""
                INSERT INTO prospects (name, company_name, email)
                VALUES (?, ?, ?)
            """, (prospect.name, prospect.companyName, prospect.email))
            
            prospect_id = cursor.lastrowid
            
            # Fetch the created prospect
            cursor.execute("""
                SELECT id, name, company_name, email, created_at
                FROM prospects WHERE id = ?
            """, (prospect_id,))
            
            row = cursor.fetchone()
            logger.info(f"New prospect registered: {prospect.email} (ID: {prospect_id})")
            
            return ProspectResponse(
                id=row[0],
                name=row[1],
                company_name=row[2],
                email=row[3],
                created_at=row[4]
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating prospect: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail="An error occurred while processing your request"
        )


@router.get("/prospects", response_model=List[ProspectResponse])
async def get_prospects(
    skip: int = 0,
    limit: int = 100,
    api_key: str = Depends(verify_api_key)
):
    """
    Get all prospects (admin only)
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return (max 1000)
    """
    if limit > 1000:
        limit = 1000
    
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, company_name, email, created_at
                FROM prospects
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            """, (limit, skip))
            
            rows = cursor.fetchall()
            return [
                ProspectResponse(
                    id=row[0],
                    name=row[1],
                    company_name=row[2],
                    email=row[3],
                    created_at=row[4]
                )
                for row in rows
            ]
    except Exception as e:
        logger.error(f"Error fetching prospects: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while fetching prospects"
        )


@router.get("/prospects/{prospect_id}", response_model=ProspectResponse)
async def get_prospect(
    prospect_id: int,
    api_key: str = Depends(verify_api_key)
):
    """
    Get a specific prospect by ID (admin only)
    """
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, company_name, email, created_at
                FROM prospects WHERE id = ?
            """, (prospect_id,))
            
            row = cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Prospect not found")
            
            return ProspectResponse(
                id=row[0],
                name=row[1],
                company_name=row[2],
                email=row[3],
                created_at=row[4]
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching prospect {prospect_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while fetching the prospect"
        )


@router.get("/prospects/stats/summary", response_model=ProspectStats)
async def get_prospect_stats(api_key: str = Depends(verify_api_key)):
    """
    Get prospect statistics (admin only)
    """
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Total prospects
            cursor.execute("SELECT COUNT(*) FROM prospects")
            total = cursor.fetchone()[0]
            
            # Prospects today
            cursor.execute("""
                SELECT COUNT(*) FROM prospects
                WHERE DATE(created_at) = DATE('now')
            """)
            today = cursor.fetchone()[0]
            
            # Prospects this week
            cursor.execute("""
                SELECT COUNT(*) FROM prospects
                WHERE created_at >= datetime('now', '-7 days')
            """)
            this_week = cursor.fetchone()[0]
            
            # Prospects this month
            cursor.execute("""
                SELECT COUNT(*) FROM prospects
                WHERE created_at >= datetime('now', '-30 days')
            """)
            this_month = cursor.fetchone()[0]
            
            return ProspectStats(
                total_prospects=total,
                prospects_today=today,
                prospects_this_week=this_week,
                prospects_this_month=this_month
            )
    except Exception as e:
        logger.error(f"Error fetching stats: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while fetching statistics"
        )

