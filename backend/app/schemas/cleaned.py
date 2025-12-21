from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class CleanedTextResponse(BaseModel):
    """Schema for cleaned text response"""
    cleaned_id: str
    visit_id: str
    cleaned_text: str
    extracted_data: Optional[Dict[str, Any]] = None
    processing_time: Optional[str] = None
    cleaned_at: datetime

    class Config:
        from_attributes = True
