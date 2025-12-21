from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base


class CleanedText(Base):
    """
    CleanedText model for storing LLM-cleaned medical text
    """
    __tablename__ = "cleaned_texts"

    cleaned_id = Column(String(50), primary_key=True, index=True)
    visit_id = Column(String(50), ForeignKey("visits.visit_id"), nullable=False)
    cleaned_text = Column(Text, nullable=False)
    extracted_data = Column(JSON, nullable=True)  # Structured medical data extraction
    processing_time = Column(String(20), nullable=True)
    cleaned_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    visit = relationship("Visit", back_populates="cleaned_texts")

    def __repr__(self):
        return f"<CleanedText {self.cleaned_id} - Visit {self.visit_id}>"
