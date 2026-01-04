"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional


class ProspectCreate(BaseModel):
    """Model for creating a new prospect"""
    name: str = Field(..., min_length=1, max_length=200, description="Full name of the prospect")
    companyName: str = Field(..., min_length=1, max_length=200, description="Company name")
    email: EmailStr = Field(..., description="Email address")
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate and clean name"""
        name = v.strip()
        if not name:
            raise ValueError("Name cannot be empty")
        return name
    
    @field_validator('companyName')
    @classmethod
    def validate_company_name(cls, v: str) -> str:
        """Validate and clean company name"""
        company = v.strip()
        if not company:
            raise ValueError("Company name cannot be empty")
        return company


class ProspectUpdate(BaseModel):
    """Model for updating a prospect (optional fields)"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    companyName: Optional[str] = Field(None, min_length=1, max_length=200)
    email: Optional[EmailStr] = None


class ProspectResponse(BaseModel):
    """Model for prospect response"""
    id: int
    name: str
    company_name: str
    email: str
    created_at: str
    
    class Config:
        from_attributes = True


class ProspectStats(BaseModel):
    """Model for prospect statistics"""
    total_prospects: int
    prospects_today: int
    prospects_this_week: int
    prospects_this_month: int

