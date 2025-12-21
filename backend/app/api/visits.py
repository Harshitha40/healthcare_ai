from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..core.database import get_db
from ..services.database_service import DatabaseService
from ..schemas import VisitResponse

router = APIRouter(prefix="/visits", tags=["Visits"])


@router.get("/", response_model=List[dict])
async def get_all_visits(
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Get all visits with their status
    """
    try:
        visits = DatabaseService.get_all_visits(db, limit)
        
        result = []
        for visit in visits:
            result.append({
                "visit_id": visit.visit_id,
                "patient_id": visit.patient_id,
                "visit_date": visit.visit_date.isoformat() if visit.visit_date else None,
                "status": visit.status,
                "visit_type": visit.visit_type
            })
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving visits: {str(e)}")


@router.get("/{visit_id}", response_model=dict)
async def get_visit_details(
    visit_id: str,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a visit
    """
    try:
        visit = DatabaseService.get_visit(db, visit_id)
        if not visit:
            raise HTTPException(status_code=404, detail="Visit not found")
        
        documents = DatabaseService.get_documents_by_visit(db, visit_id)
        
        return {
            "visit_id": visit.visit_id,
            "patient_id": visit.patient_id,
            "visit_date": visit.visit_date.isoformat() if visit.visit_date else None,
            "status": visit.status,
            "visit_type": visit.visit_type,
            "documents": [
                {
                    "document_id": doc.document_id,
                    "filename": doc.filename,
                    "file_type": doc.file_type,
                    "file_size": doc.file_size
                }
                for doc in documents
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving visit details: {str(e)}")
