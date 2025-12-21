from pydantic import BaseModel
from datetime import datetime


class DocumentResponse(BaseModel):
    """Schema for document response"""
    document_id: str
    visit_id: str
    filename: str
    file_path: str
    file_type: str
    file_size: int
    upload_date: datetime

    class Config:
        from_attributes = True
