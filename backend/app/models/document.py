from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base


class RawDocument(Base):
    """
    RawDocument model for storing uploaded medical documents
    """
    __tablename__ = "raw_documents"

    document_id = Column(String(50), primary_key=True, index=True)
    visit_id = Column(String(50), ForeignKey("visits.visit_id"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(50), nullable=False)  # pdf, jpg, png, etc.
    file_size = Column(Integer, nullable=True)  # size in bytes
    upload_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    visit = relationship("Visit", back_populates="documents")

    def __repr__(self):
        return f"<RawDocument {self.document_id} - {self.filename}>"
