import time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..services.ocr_service import OCRService
from ..services.database_service import DatabaseService
from ..schemas import OCRResponse

router = APIRouter(prefix="/ocr", tags=["OCR"])

# Initialize OCR service
ocr_service = OCRService()


@router.post("/{visit_id}", response_model=OCRResponse)
async def perform_ocr(
    visit_id: str,
    db: Session = Depends(get_db)
):
    """
    Perform OCR on uploaded document
    
    - Extracts text from PDF or image
    - Stores raw OCR text in database
    - Returns extracted text and confidence score
    """
    try:
        # Get visit
        visit = DatabaseService.get_visit(db, visit_id)
        if not visit:
            raise HTTPException(status_code=404, detail="Visit not found")
        
        # Get documents for this visit
        documents = DatabaseService.get_documents_by_visit(db, visit_id)
        if not documents:
            raise HTTPException(status_code=404, detail="No documents found for this visit")
        
        # Use the first document
        document = documents[0]
        
        # Update visit status
        DatabaseService.update_visit_status(db, visit_id, "processing_ocr")
        
        # Perform OCR
        start_time = time.time()
        extracted_text, confidence = ocr_service.extract_text(
            document.file_path,
            document.file_type
        )
        processing_time = f"{time.time() - start_time:.2f}s"
        
        if not extracted_text:
            raise HTTPException(status_code=500, detail="Could not extract text from document")
        
        # Save OCR result
        ocr_result = DatabaseService.create_ocr_text(
            db=db,
            visit_id=visit_id,
            raw_text=extracted_text,
            confidence_score=f"{confidence:.2f}",
            processing_time=processing_time
        )
        
        # Update visit status
        DatabaseService.update_visit_status(db, visit_id, "ocr_completed")
        
        return ocr_result
        
    except HTTPException:
        raise
    except Exception as e:
        DatabaseService.update_visit_status(db, visit_id, "ocr_failed")
        raise HTTPException(status_code=500, detail=f"Error performing OCR: {str(e)}")
