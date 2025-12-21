import uuid
import logging
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime

from ..models import Patient, Visit, RawDocument, OCRText, CleanedText, Summary
from ..schemas import (
    PatientCreate, PatientResponse,
    VisitCreate, VisitResponse,
    DocumentResponse, OCRResponse,
    CleanedTextResponse, SummaryResponse
)

logger = logging.getLogger(__name__)


class DatabaseService:
    """
    Service for database operations
    """
    
    @staticmethod
    def generate_id(prefix: str) -> str:
        """
        Generate unique ID with prefix
        
        Args:
            prefix: Prefix for the ID (e.g., 'PAT', 'VIS', 'DOC')
            
        Returns:
            Generated unique ID
        """
        return f"{prefix}_{uuid.uuid4().hex[:12].upper()}"
    
    # Patient operations
    @staticmethod
    def create_patient(db: Session, patient_data: Optional[PatientCreate] = None) -> Patient:
        """
        Create a new patient
        
        Args:
            db: Database session
            patient_data: Patient creation data
            
        Returns:
            Created patient object
        """
        try:
            patient_id = DatabaseService.generate_id("PAT")
            
            patient = Patient(
                patient_id=patient_id,
                name=patient_data.name if patient_data else None,
                age=patient_data.age if patient_data else None,
                gender=patient_data.gender if patient_data else None,
                contact=patient_data.contact if patient_data else None,
                medical_history=patient_data.medical_history if patient_data else None
            )
            
            db.add(patient)
            db.commit()
            db.refresh(patient)
            
            logger.info(f"Created patient: {patient_id}")
            return patient
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating patient: {str(e)}")
            raise
    
    @staticmethod
    def get_patient(db: Session, patient_id: str) -> Optional[Patient]:
        """Get patient by ID"""
        return db.query(Patient).filter(Patient.patient_id == patient_id).first()
    
    # Visit operations
    @staticmethod
    def create_visit(db: Session, visit_data: VisitCreate) -> Visit:
        """
        Create a new visit
        
        Args:
            db: Database session
            visit_data: Visit creation data
            
        Returns:
            Created visit object
        """
        try:
            visit_id = DatabaseService.generate_id("VIS")
            
            visit = Visit(
                visit_id=visit_id,
                patient_id=visit_data.patient_id,
                visit_type=visit_data.visit_type,
                notes=visit_data.notes,
                status="pending"
            )
            
            db.add(visit)
            db.commit()
            db.refresh(visit)
            
            logger.info(f"Created visit: {visit_id}")
            return visit
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating visit: {str(e)}")
            raise
    
    @staticmethod
    def get_visit(db: Session, visit_id: str) -> Optional[Visit]:
        """Get visit by ID"""
        return db.query(Visit).filter(Visit.visit_id == visit_id).first()
    
    @staticmethod
    def update_visit_status(db: Session, visit_id: str, status: str) -> None:
        """Update visit status"""
        try:
            visit = db.query(Visit).filter(Visit.visit_id == visit_id).first()
            if visit:
                visit.status = status
                db.commit()
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating visit status: {str(e)}")
            raise
    
    # Document operations
    @staticmethod
    def create_document(
        db: Session,
        visit_id: str,
        filename: str,
        file_path: str,
        file_type: str,
        file_size: int
    ) -> RawDocument:
        """
        Create a new document record
        
        Args:
            db: Database session
            visit_id: Visit ID
            filename: Original filename
            file_path: Saved file path
            file_type: File type
            file_size: File size in bytes
            
        Returns:
            Created document object
        """
        try:
            document_id = DatabaseService.generate_id("DOC")
            
            document = RawDocument(
                document_id=document_id,
                visit_id=visit_id,
                filename=filename,
                file_path=file_path,
                file_type=file_type,
                file_size=file_size
            )
            
            db.add(document)
            db.commit()
            db.refresh(document)
            
            logger.info(f"Created document: {document_id}")
            return document
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating document: {str(e)}")
            raise
    
    @staticmethod
    def get_documents_by_visit(db: Session, visit_id: str) -> List[RawDocument]:
        """Get all documents for a visit"""
        return db.query(RawDocument).filter(RawDocument.visit_id == visit_id).all()
    
    # OCR Text operations
    @staticmethod
    def create_ocr_text(
        db: Session,
        visit_id: str,
        raw_text: str,
        confidence_score: str,
        processing_time: str
    ) -> OCRText:
        """
        Create OCR text record
        
        Args:
            db: Database session
            visit_id: Visit ID
            raw_text: Extracted OCR text
            confidence_score: OCR confidence score
            processing_time: Time taken for OCR
            
        Returns:
            Created OCR text object
        """
        try:
            ocr_id = DatabaseService.generate_id("OCR")
            
            ocr_text = OCRText(
                ocr_id=ocr_id,
                visit_id=visit_id,
                raw_text=raw_text,
                confidence_score=confidence_score,
                processing_time=processing_time
            )
            
            db.add(ocr_text)
            db.commit()
            db.refresh(ocr_text)
            
            logger.info(f"Created OCR text: {ocr_id}")
            return ocr_text
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating OCR text: {str(e)}")
            raise
    
    @staticmethod
    def get_ocr_text_by_visit(db: Session, visit_id: str) -> Optional[OCRText]:
        """Get latest OCR text for a visit"""
        return db.query(OCRText).filter(OCRText.visit_id == visit_id).order_by(OCRText.created_at.desc()).first()
    
    # Cleaned Text operations
    @staticmethod
    def create_cleaned_text(
        db: Session,
        visit_id: str,
        cleaned_text: str,
        extracted_data: dict,
        processing_time: str
    ) -> CleanedText:
        """
        Create cleaned text record
        
        Args:
            db: Database session
            visit_id: Visit ID
            cleaned_text: LLM-cleaned text
            extracted_data: Structured data extraction
            processing_time: Time taken for cleaning
            
        Returns:
            Created cleaned text object
        """
        try:
            cleaned_id = DatabaseService.generate_id("CLN")
            
            cleaned = CleanedText(
                cleaned_id=cleaned_id,
                visit_id=visit_id,
                cleaned_text=cleaned_text,
                extracted_data=extracted_data,
                processing_time=processing_time
            )
            
            db.add(cleaned)
            db.commit()
            db.refresh(cleaned)
            
            logger.info(f"Created cleaned text: {cleaned_id}")
            return cleaned
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating cleaned text: {str(e)}")
            raise
    
    @staticmethod
    def get_cleaned_text_by_visit(db: Session, visit_id: str) -> Optional[CleanedText]:
        """Get latest cleaned text for a visit"""
        return db.query(CleanedText).filter(CleanedText.visit_id == visit_id).order_by(CleanedText.created_at.desc()).first()
    
    # Summary operations
    @staticmethod
    def create_summary(
        db: Session,
        visit_id: str,
        summary_text: str,
        key_findings: str,
        processing_time: str
    ) -> Summary:
        """
        Create summary record
        
        Args:
            db: Database session
            visit_id: Visit ID
            summary_text: Generated summary
            key_findings: Key findings
            processing_time: Time taken for summarization
            
        Returns:
            Created summary object
        """
        try:
            summary_id = DatabaseService.generate_id("SUM")
            
            summary = Summary(
                summary_id=summary_id,
                visit_id=visit_id,
                summary_text=summary_text,
                key_findings=key_findings,
                processing_time=processing_time
            )
            
            db.add(summary)
            db.commit()
            db.refresh(summary)
            
            logger.info(f"Created summary: {summary_id}")
            return summary
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating summary: {str(e)}")
            raise
    
    @staticmethod
    def get_summary_by_visit(db: Session, visit_id: str) -> Optional[Summary]:
        """Get latest summary for a visit"""
        return db.query(Summary).filter(Summary.visit_id == visit_id).order_by(Summary.created_at.desc()).first()
    
    @staticmethod
    def get_all_visits(db: Session, limit: int = 50) -> List[Visit]:
        """Get all visits"""
        return db.query(Visit).order_by(Visit.created_at.desc()).limit(limit).all()
