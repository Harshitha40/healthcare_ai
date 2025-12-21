from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PatientCreate(BaseModel):
    """Schema for creating a patient"""
    name: Optional[str] = None
    age: Optional[str] = None
    gender: Optional[str] = None
    contact: Optional[str] = None
    medical_history: Optional[str] = None


class PatientResponse(BaseModel):
    """Schema for patient response"""
    patient_id: str
    name: Optional[str] = None
    age: Optional[str] = None
    gender: Optional[str] = None
    contact: Optional[str] = None
    medical_history: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
