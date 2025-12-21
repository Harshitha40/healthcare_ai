from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base


class Patient(Base):
    """
    Patient model for storing patient information
    """
    __tablename__ = "patients"

    patient_id = Column(String(50), primary_key=True, index=True)
    name = Column(String(200), nullable=True)
    age = Column(String(10), nullable=True)
    gender = Column(String(20), nullable=True)
    contact = Column(String(100), nullable=True)
    medical_history = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    visits = relationship("Visit", back_populates="patient", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Patient {self.patient_id} - {self.name}>"
