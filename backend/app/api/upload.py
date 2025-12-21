import os
import shutil
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from ..core.database import get_db
from ..core.config import settings
from ..services.database_service import DatabaseService
from ..schemas import PatientCreate, VisitResponse

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/", response_model=dict)
async def upload_medical_document(
    file: UploadFile = File(...),
    patient_name: Optional[str] = None,
    patient_age: Optional[str] = None,
    patient_gender: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Upload medical document (PDF or image)
    
    - Creates patient if needed
    - Creates visit
    - Saves document
    - Returns patient_id and visit_id
    """
    try:
        # Validate file type
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file_ext} not allowed. Allowed types: {settings.ALLOWED_EXTENSIONS}"
            )
        
        # Create patient
        patient_data = PatientCreate(
            name=patient_name,
            age=patient_age,
            gender=patient_gender
        )
        patient = DatabaseService.create_patient(db, patient_data)
        
        # Create visit
        from ..schemas import VisitCreate
        visit_data = VisitCreate(
            patient_id=patient.patient_id,
            visit_type="consultation"
        )
        visit = DatabaseService.create_visit(db, visit_data)
        
        # Save file
        upload_dir = os.path.join(settings.UPLOAD_DIR, visit.visit_id)
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        file_size = os.path.getsize(file_path)
        
        # Create document record
        document = DatabaseService.create_document(
            db=db,
            visit_id=visit.visit_id,
            filename=file.filename,
            file_path=file_path,
            file_type=file_ext[1:],  # Remove the dot
            file_size=file_size
        )
        
        # Update visit status
        DatabaseService.update_visit_status(db, visit.visit_id, "uploaded")
        
        return {
            "message": "File uploaded successfully",
            "patient_id": patient.patient_id,
            "visit_id": visit.visit_id,
            "document_id": document.document_id,
            "filename": file.filename,
            "file_size": file_size
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")
