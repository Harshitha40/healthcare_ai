from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class VisitCreate(BaseModel):
    """Schema for creating a visit"""
    patient_id: str
    visit_type: Optional[str] = "consultation"
    notes: Optional[str] = None


class VisitResponse(BaseModel):
    """Schema for visit response"""
    visit_id: str
    patient_id: str
    visit_date: datetime
    visit_type: Optional[str] = None
    status: str
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
