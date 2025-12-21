from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SummaryResponse(BaseModel):
    """Schema for summary response"""
    summary_id: str
    visit_id: str
    summary_text: str
    key_findings: Optional[str] = None
    generated_by: str
    processing_time: Optional[str] = None
    generated_at: datetime

    class Config:
        from_attributes = True
