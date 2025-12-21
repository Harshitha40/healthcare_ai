# 📁 PROJECT STRUCTURE OVERVIEW

## Complete File Tree

```
C:\Users\Lenovo\aimlel\proj\
│
├── 📄 README.md                          # Main documentation
├── 📄 QUICKSTART.md                      # Quick setup guide
├── 📄 PROMPTS.md                         # LLM prompts documentation
│
├── 📁 backend/                           # Python FastAPI Backend
│   ├── 📁 app/
│   │   ├── 📁 api/                       # API Endpoints
│   │   │   ├── __init__.py
│   │   │   ├── upload.py                 # POST /upload - File upload
│   │   │   ├── ocr.py                    # POST /ocr/{visit_id} - OCR processing
│   │   │   ├── clean.py                  # POST /clean/{visit_id} - Text cleaning
│   │   │   ├── summarize.py              # POST /summarize/{visit_id} - Summary generation
│   │   │   └── visits.py                 # GET /visits - Visit management
│   │   │
│   │   ├── 📁 core/                      # Core Configuration
│   │   │   ├── __init__.py
│   │   │   ├── config.py                 # Settings & environment variables
│   │   │   └── database.py               # Database connection & session
│   │   │
│   │   ├── 📁 models/                    # SQLAlchemy Database Models
│   │   │   ├── __init__.py
│   │   │   ├── patient.py                # Patient model
│   │   │   ├── visit.py                  # Visit model
│   │   │   ├── document.py               # RawDocument model
│   │   │   ├── ocr_text.py               # OCRText model
│   │   │   ├── cleaned_text.py           # CleanedText model
│   │   │   └── summary.py                # Summary model
│   │   │
│   │   ├── 📁 schemas/                   # Pydantic Schemas (Request/Response)
│   │   │   ├── __init__.py
│   │   │   ├── patient.py                # Patient schemas
│   │   │   ├── visit.py                  # Visit schemas
│   │   │   ├── document.py               # Document schemas
│   │   │   ├── ocr.py                    # OCR schemas
│   │   │   ├── cleaned.py                # Cleaned text schemas
│   │   │   └── summary.py                # Summary schemas
│   │   │
│   │   ├── 📁 services/                  # Business Logic Services
│   │   │   ├── __init__.py
│   │   │   ├── ocr_service.py            # PaddleOCR integration
│   │   │   ├── llm_service.py            # Groq LLM integration
│   │   │   └── database_service.py       # Database operations
│   │   │
│   │   └── __init__.py
│   │
│   ├── 📁 uploads/                       # Uploaded files storage (created at runtime)
│   ├── 📄 main.py                        # FastAPI application entry point
│   ├── 📄 requirements.txt               # Python dependencies
│   ├── 📄 .env.example                   # Environment variables template
│   └── 📄 .gitignore                     # Git ignore rules
│
├── 📁 frontend/                          # React Frontend
│   ├── 📁 public/
│   ├── 📁 src/
│   │   ├── 📁 components/                # React Components
│   │   │   ├── FileUpload.jsx            # File upload form component
│   │   │   ├── ProcessingStatus.jsx      # Processing progress component
│   │   │   └── SummaryView.jsx           # Summary display component
│   │   │
│   │   ├── 📁 services/                  # API Services
│   │   │   └── api.js                    # Axios API client
│   │   │
│   │   ├── 📁 styles/                    # CSS Stylesheets
│   │   │   ├── index.css                 # Global styles
│   │   │   ├── App.css                   # App component styles
│   │   │   ├── FileUpload.css            # Upload component styles
│   │   │   ├── ProcessingStatus.css      # Processing component styles
│   │   │   └── SummaryView.css           # Summary component styles
│   │   │
│   │   ├── App.jsx                       # Main application component
│   │   └── main.jsx                      # React entry point
│   │
│   ├── 📄 index.html                     # HTML template
│   ├── 📄 package.json                   # Node.js dependencies
│   ├── 📄 vite.config.js                 # Vite configuration
│   └── 📄 .gitignore                     # Git ignore rules
│
└── 📁 database/                          # Database Scripts
    └── 📄 schema.sql                     # PostgreSQL database schema
```

## File Counts

- **Total Files**: ~45 files
- **Backend Python Files**: ~25 files
- **Frontend React/JS Files**: ~15 files
- **Configuration Files**: ~5 files
- **Documentation Files**: ~3 files

## Key Components

### Backend Architecture

#### API Layer (`app/api/`)
- **upload.py**: Handles file uploads, creates patient and visit records
- **ocr.py**: Triggers OCR processing using PaddleOCR
- **clean.py**: Cleans OCR text using Groq LLM
- **summarize.py**: Generates medical summaries
- **visits.py**: Manages visit queries

#### Service Layer (`app/services/`)
- **ocr_service.py**: 
  - PaddleOCR integration
  - Image preprocessing
  - PDF to image conversion
  - Text extraction with confidence scores

- **llm_service.py**:
  - Groq API client
  - Text cleaning prompts
  - Structured data extraction
  - Summary generation
  - Key findings extraction

- **database_service.py**:
  - CRUD operations for all models
  - ID generation
  - Transaction management

#### Data Layer (`app/models/`)
- **patient.py**: Patient information
- **visit.py**: Patient visits
- **document.py**: Uploaded documents
- **ocr_text.py**: Raw OCR output
- **cleaned_text.py**: LLM-cleaned text + structured data
- **summary.py**: Generated summaries

### Frontend Architecture

#### Components (`src/components/`)
- **FileUpload.jsx**: 
  - File selection and validation
  - Patient info input form
  - Upload handling

- **ProcessingStatus.jsx**:
  - Real-time progress tracking
  - Step-by-step status display
  - Animated progress indicators

- **SummaryView.jsx**:
  - Tabbed interface
  - Summary display
  - Original vs cleaned comparison
  - Structured data visualization

#### Services (`src/services/`)
- **api.js**: Centralized API client with all endpoint methods

## Data Flow

```
1. User uploads document
   ↓
2. Backend saves file → Creates Patient → Creates Visit → Creates Document record
   ↓
3. User clicks process OR auto-processes
   ↓
4. OCR Service extracts text → Saves to ocr_texts table
   ↓
5. LLM Service cleans text → Extracts structured data → Saves to cleaned_texts table
   ↓
6. LLM Service generates summary → Saves to summaries table
   ↓
7. Frontend displays all results in tabbed interface
```

## Database Schema

```
patients (1) ──┐
               │
               ├──> visits (many) ──┐
                                    │
                                    ├──> raw_documents (many)
                                    ├──> ocr_texts (many)
                                    ├──> cleaned_texts (many)
                                    └──> summaries (many)
```

## Technology Stack Summary

### Backend
- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL
- **OCR**: PaddleOCR
- **LLM**: Groq API (Llama 3.3 70B)
- **Image Processing**: OpenCV, Pillow
- **PDF Processing**: PyMuPDF

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **HTTP Client**: Axios
- **Styling**: Pure CSS (no framework)

## Environment Variables

```env
# Backend .env
DATABASE_URL=postgresql://postgres:password@localhost:5432/healthcare_ai
GROQ_API_KEY=your_api_key
GROQ_MODEL=llama-3.3-70b-versatile
HOST=0.0.0.0
PORT=8000
DEBUG=True
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760
CORS_ORIGINS=["http://localhost:3000"]
```

## API Endpoints Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Root endpoint |
| `/health` | GET | Health check |
| `/upload/` | POST | Upload document |
| `/ocr/{visit_id}` | POST | Perform OCR |
| `/clean/{visit_id}` | POST | Clean text |
| `/summarize/{visit_id}` | POST | Generate summary |
| `/summarize/{visit_id}` | GET | Get summary data |
| `/visits/` | GET | List visits |
| `/visits/{visit_id}` | GET | Get visit details |

## State Management (Frontend)

```javascript
App Component State:
- currentView: 'upload' | 'processing' | 'summary'
- visitId: string | null

FileUpload State:
- file: File | null
- patientName: string
- patientAge: string
- patientGender: string
- uploading: boolean
- error: string | null

ProcessingStatus State:
- status: string
- progress: number (0-100)
- error: string | null
- currentStep: number (0-2)

SummaryView State:
- data: object | null
- loading: boolean
- error: string | null
- activeTab: 'summary' | 'comparison' | 'extracted'
```

## Error Handling

### Backend
- Try-catch blocks in all endpoints
- Proper HTTP status codes
- Detailed error messages
- Database rollback on errors
- Logging with Python logging module

### Frontend
- Axios error interceptors
- User-friendly error messages
- Loading states
- Graceful degradation

## Security Features

- Environment variable isolation
- CORS configuration
- File type validation
- File size limits
- SQL injection protection (SQLAlchemy)
- Input sanitization

## Performance Optimizations

### Backend
- Database connection pooling
- Async/await where applicable
- Image preprocessing for better OCR
- Efficient file storage

### Frontend
- Component lazy loading
- Optimized re-renders
- CSS animations (GPU-accelerated)
- Vite's fast build process

## Scalability Considerations

- Stateless API design
- Database indexing on foreign keys
- File storage can be moved to S3/cloud storage
- Can add Redis for caching
- Can containerize with Docker
- Can add message queue for background processing

---

## Development Commands

### Backend
```bash
# Install
pip install -r requirements.txt

# Run
python main.py

# Run with auto-reload
uvicorn main:app --reload
```

### Frontend
```bash
# Install
npm install

# Development
npm run dev

# Build
npm run build

# Preview production build
npm run preview
```

---

**Total Lines of Code**: ~3,500+ lines
**Development Time**: Production-ready in hours
**Maintenance**: Modular, easy to extend
