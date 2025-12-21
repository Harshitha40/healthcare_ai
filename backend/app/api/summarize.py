import time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..services.llm_service import LLMService
from ..services.database_service import DatabaseService
from ..schemas import SummaryResponse

router = APIRouter(prefix="/summarize", tags=["Summarize"])

# Initialize LLM service
llm_service = LLMService()


@router.post("/{visit_id}", response_model=SummaryResponse)
async def generate_summary(
    visit_id: str,
    db: Session = Depends(get_db)
):
    """
    Generate medical summary using LLM
    
    - Gets cleaned text
    - Generates concise medical summary
    - Extracts key findings
    - Stores summary
    """
    try:
        # Get visit
        visit = DatabaseService.get_visit(db, visit_id)
        if not visit:
            raise HTTPException(status_code=404, detail="Visit not found")
        
        # Get cleaned text
        cleaned_text = DatabaseService.get_cleaned_text_by_visit(db, visit_id)
        if not cleaned_text:
            raise HTTPException(
                status_code=404,
                detail="No cleaned text found. Please run cleaning first."
            )
        
        # Update visit status
        DatabaseService.update_visit_status(db, visit_id, "processing_summary")
        
        # Generate summary using LLM
        start_time = time.time()
        summary_text = llm_service.generate_medical_summary(cleaned_text.cleaned_text)
        
        # Extract key findings
        key_findings = llm_service.extract_key_findings(summary_text)
        
        processing_time = f"{time.time() - start_time:.2f}s"
        
        # Save summary
        summary_result = DatabaseService.create_summary(
            db=db,
            visit_id=visit_id,
            summary_text=summary_text,
            key_findings=key_findings,
            processing_time=processing_time
        )
        
        # Update visit status
        DatabaseService.update_visit_status(db, visit_id, "completed")
        
        return summary_result
        
    except HTTPException:
        raise
    except Exception as e:
        DatabaseService.update_visit_status(db, visit_id, "summary_failed")
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")


@router.get("/{visit_id}", response_model=dict)
async def get_summary(
    visit_id: str,
    db: Session = Depends(get_db)
):
    """
    Get complete summary data for a visit
    
    - Returns original OCR text
    - Returns cleaned text
    - Returns generated summary
    - Returns structured extracted data
    """
    try:
        # Get visit
        visit = DatabaseService.get_visit(db, visit_id)
        if not visit:
            raise HTTPException(status_code=404, detail="Visit not found")
        
        # Get all data
        ocr_text = DatabaseService.get_ocr_text_by_visit(db, visit_id)
        cleaned_text = DatabaseService.get_cleaned_text_by_visit(db, visit_id)
        summary = DatabaseService.get_summary_by_visit(db, visit_id)
        
        return {
            "visit_id": visit_id,
            "status": visit.status,
            "ocr_text": ocr_text.raw_text if ocr_text else None,
            "ocr_confidence": ocr_text.confidence_score if ocr_text else None,
            "cleaned_text": cleaned_text.cleaned_text if cleaned_text else None,
            "extracted_data": cleaned_text.extracted_data if cleaned_text else None,
            "summary": summary.summary_text if summary else None,
            "key_findings": summary.key_findings if summary else None,
            "patient_id": visit.patient_id,
            "visit_date": visit.visit_date.isoformat() if visit.visit_date else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving summary: {str(e)}")
