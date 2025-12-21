from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base


class Visit(Base):
    """
    Visit model for storing patient visit information
    """
    __tablename__ = "visits"

    visit_id = Column(String(50), primary_key=True, index=True)
    patient_id = Column(String(50), ForeignKey("patients.patient_id"), nullable=False)
    visit_date = Column(DateTime, default=datetime.utcnow)
    visit_type = Column(String(100), nullable=True)  # e.g., "consultation", "follow-up"
    status = Column(String(50), default="pending")  # pending, processing, completed, failed
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patient = relationship("Patient", back_populates="visits")
    documents = relationship("RawDocument", back_populates="visit", cascade="all, delete-orphan")
    ocr_texts = relationship("OCRText", back_populates="visit", cascade="all, delete-orphan")
    cleaned_texts = relationship("CleanedText", back_populates="visit", cascade="all, delete-orphan")
    summaries = relationship("Summary", back_populates="visit", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Visit {self.visit_id} - Patient {self.patient_id}>"
