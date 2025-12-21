from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base


class Summary(Base):
    """
    Summary model for storing AI-generated medical summaries
    """
    __tablename__ = "summaries"

    summary_id = Column(String(50), primary_key=True, index=True)
    visit_id = Column(String(50), ForeignKey("visits.visit_id"), nullable=False)
    summary_text = Column(Text, nullable=False)
    key_findings = Column(Text, nullable=True)
    generated_by = Column(String(100), default="Groq LLM")
    processing_time = Column(String(20), nullable=True)
    generated_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    visit = relationship("Visit", back_populates="summaries")

    def __repr__(self):
        return f"<Summary {self.summary_id} - Visit {self.visit_id}>"
