from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class LeadBase(BaseModel):
    full_name: str = Field(..., min_length=2)
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    message: Optional[str] = None
    source: Optional[str] = "web_form"

class LeadCreate(LeadBase):
    pass

class LeadResponse(LeadBase):
    id: int
    status: str
    lead_score: int
    ai_category: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True