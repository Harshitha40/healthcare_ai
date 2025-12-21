from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OCRResponse(BaseModel):
    """Schema for OCR response"""
    ocr_id: str
    visit_id: str
    raw_text: str
    confidence_score: Optional[str] = None
    processing_time: Optional[str] = None
    extracted_at: datetime

    class Config:
        from_attributes = True
