import time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..services.llm_service import LLMService
from ..services.database_service import DatabaseService
from ..schemas import CleanedTextResponse

router = APIRouter(prefix="/clean", tags=["Clean"])

# Initialize LLM service
llm_service = LLMService()


@router.post("/{visit_id}", response_model=CleanedTextResponse)
async def clean_ocr_text(
    visit_id: str,
    db: Session = Depends(get_db)
):
    """
    Clean OCR text using LLM
    
    - Gets raw OCR text
    - Cleans and corrects text using Groq LLM
    - Extracts structured medical data
    - Stores cleaned text and extracted data
    """
    try:
        # Get visit
        visit = DatabaseService.get_visit(db, visit_id)
        if not visit:
            raise HTTPException(status_code=404, detail="Visit not found")
        
        # Get OCR text
        ocr_text = DatabaseService.get_ocr_text_by_visit(db, visit_id)
        if not ocr_text:
            raise HTTPException(
                status_code=404,
                detail="No OCR text found. Please run OCR first."
            )
        
        # Update visit status
        DatabaseService.update_visit_status(db, visit_id, "processing_cleaning")
        
        # Clean text using LLM
        start_time = time.time()
        cleaned_text = llm_service.clean_ocr_text(ocr_text.raw_text)
        
        # Extract structured data
        extracted_data = llm_service.extract_structured_data(cleaned_text)
        
        processing_time = f"{time.time() - start_time:.2f}s"
        
        # Save cleaned text and structured data
        cleaned_result = DatabaseService.create_cleaned_text(
            db=db,
            visit_id=visit_id,
            cleaned_text=cleaned_text,
            extracted_data=extracted_data,
            processing_time=processing_time
        )
        
        # Update visit status
        DatabaseService.update_visit_status(db, visit_id, "cleaning_completed")
        
        return cleaned_result
        
    except HTTPException:
        raise
    except Exception as e:
        DatabaseService.update_visit_status(db, visit_id, "cleaning_failed")
        raise HTTPException(status_code=500, detail=f"Error cleaning text: {str(e)}")
