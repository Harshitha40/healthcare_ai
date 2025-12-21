from .upload import router as upload_router
from .ocr import router as ocr_router
from .clean import router as clean_router
from .summarize import router as summarize_router
from .visits import router as visits_router

__all__ = [
    "upload_router",
    "ocr_router",
    "clean_router",
    "summarize_router",
    "visits_router"
]
