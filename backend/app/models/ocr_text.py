from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base


class OCRText(Base):
    """
    OCRText model for storing raw OCR extracted text
    """
    __tablename__ = "ocr_texts"

    ocr_id = Column(String(50), primary_key=True, index=True)
    visit_id = Column(String(50), ForeignKey("visits.visit_id"), nullable=False)
    raw_text = Column(Text, nullable=False)
    confidence_score = Column(String(10), nullable=True)
    processing_time = Column(String(20), nullable=True)  # time taken for OCR
    extracted_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    visit = relationship("Visit", back_populates="ocr_texts")

    def __repr__(self):
        return f"<OCRText {self.ocr_id} - Visit {self.visit_id}>"
