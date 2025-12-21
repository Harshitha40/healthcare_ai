# HEALTHCARE AI SYSTEM - ARCHITECTURE DIAGRAMS

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│                    http://localhost:3000                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP Requests
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      REACT FRONTEND                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ FileUpload   │  │ Processing   │  │ SummaryView  │          │
│  │ Component    │  │ Status       │  │ Component    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                             │                                    │
│                    ┌────────▼────────┐                          │
│                    │   API Service    │                          │
│                    │   (Axios)        │                          │
│                    └────────┬────────┘                          │
└─────────────────────────────┼────────────────────────────────────┘
                              │
                              │ REST API Calls
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND                               │
│                  http://localhost:8000                           │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    API ENDPOINTS                          │  │
│  │  /upload  /ocr/{id}  /clean/{id}  /summarize/{id}        │  │
│  └────┬─────────┬────────────┬─────────────┬────────────────┘  │
│       │         │            │             │                    │
│  ┌────▼─────────▼────────────▼─────────────▼────────────────┐  │
│  │                   SERVICE LAYER                           │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────────────┐ │  │
│  │  │    OCR     │  │    LLM     │  │     Database       │ │  │
│  │  │  Service   │  │  Service   │  │     Service        │ │  │
│  │  │            │  │            │  │                    │ │  │
│  │  │ PaddleOCR  │  │ Groq API   │  │   SQLAlchemy ORM   │ │  │
│  │  └────────────┘  └────────────┘  └──────────┬─────────┘ │  │
│  └──────────────────────────────────────────────┼───────────┘  │
└───────────────────────────────────────────────┬─┼───────────────┘
                                                │ │
                      ┌─────────────────────────┘ │
                      │                           │
            ┌─────────▼─────────┐    ┌───────────▼────────────┐
            │   FILE STORAGE    │    │   POSTGRESQL DATABASE  │
            │   (uploads/)      │    │   healthcare_ai        │
            │                   │    │                        │
            │  PDF/Image Files  │    │  ┌──────────────────┐ │
            └───────────────────┘    │  │  patients        │ │
                                     │  │  visits          │ │
                                     │  │  raw_documents   │ │
                                     │  │  ocr_texts       │ │
                                     │  │  cleaned_texts   │ │
                                     │  │  summaries       │ │
                                     │  └──────────────────┘ │
                                     └───────────────────────┘
```

## Data Flow Diagram

```
┌────────────┐
│   USER     │
└─────┬──────┘
      │
      │ 1. Upload Document
      ▼
┌─────────────────┐
│  FileUpload UI  │
└────────┬────────┘
         │
         │ 2. POST /upload/
         ▼
┌─────────────────────┐
│  Upload Endpoint    │────► Create Patient Record
│                     │────► Create Visit Record
│                     │────► Save File to Disk
│                     │────► Create Document Record
└──────────┬──────────┘
           │
           │ 3. Return visit_id
           ▼
┌─────────────────────┐
│ ProcessingStatus UI │
└──────────┬──────────┘
           │
           │ 4. POST /ocr/{visit_id}
           ▼
┌─────────────────────┐
│   OCR Endpoint      │
└──────────┬──────────┘
           │
           │ 5. Call OCR Service
           ▼
┌─────────────────────┐
│   PaddleOCR         │────► Extract Text
│   (ocr_service.py)  │────► Image Preprocessing
│                     │────► PDF Handling
└──────────┬──────────┘
           │
           │ 6. Save OCR Text to DB
           │
           │ 7. POST /clean/{visit_id}
           ▼
┌─────────────────────┐
│  Clean Endpoint     │
└──────────┬──────────┘
           │
           │ 8. Call LLM Service
           ▼
┌─────────────────────┐
│   Groq LLM          │────► Clean Text
│   (llm_service.py)  │────► Extract Structured Data
└──────────┬──────────┘
           │
           │ 9. Save Cleaned Text + Data to DB
           │
           │ 10. POST /summarize/{visit_id}
           ▼
┌─────────────────────┐
│ Summarize Endpoint  │
└──────────┬──────────┘
           │
           │ 11. Call LLM Service
           ▼
┌─────────────────────┐
│   Groq LLM          │────► Generate Summary
│   (llm_service.py)  │────► Extract Key Findings
└──────────┬──────────┘
           │
           │ 12. Save Summary to DB
           │
           │ 13. GET /summarize/{visit_id}
           ▼
┌─────────────────────┐
│  SummaryView UI     │────► Display Summary
│                     │────► Show Comparison
│                     │────► Show Structured Data
└─────────────────────┘
```

## Database Schema Diagram

```
┌─────────────────────┐
│     patients        │
├─────────────────────┤
│ patient_id (PK)     │◄─────┐
│ name                │      │
│ age                 │      │
│ gender              │      │
│ contact             │      │
│ medical_history     │      │
│ created_at          │      │
│ updated_at          │      │
└─────────────────────┘      │
                             │ 1:N
                    ┌────────┴────────┐
                    │     visits      │
                    ├─────────────────┤
                    │ visit_id (PK)   │◄─────┐
                    │ patient_id (FK) │      │
                    │ visit_date      │      │
                    │ visit_type      │      │
                    │ status          │      │
                    │ notes           │      │
                    │ created_at      │      │
                    └─────────────────┘      │
                             │               │
                ┌────────────┼───────────┬───┼───┬────────────┐
                │            │           │   │   │            │
                │ 1:N        │ 1:N       │ 1:N   │ 1:N        │ 1:N
        ┌───────▼──────┐ ┌──▼──────┐ ┌──▼───────▼───┐ ┌──────▼──────┐
        │raw_documents │ │ocr_texts│ │cleaned_texts │ │  summaries  │
        ├──────────────┤ ├─────────┤ ├──────────────┤ ├─────────────┤
        │document_id(PK│ │ocr_id(PK│ │cleaned_id(PK)│ │summary_id(PK│
        │visit_id (FK) │ │visit_id │ │visit_id (FK) │ │visit_id (FK)│
        │filename      │ │raw_text │ │cleaned_text  │ │summary_text │
        │file_path     │ │confid   │ │extracted_data│ │key_findings │
        │file_type     │ │proc_time│ │proc_time     │ │generated_by │
        │file_size     │ │extract  │ │cleaned_at    │ │proc_time    │
        │upload_date   │ │created  │ │created_at    │ │generated_at │
        └──────────────┘ └─────────┘ └──────────────┘ └─────────────┘
```

## Component Hierarchy (Frontend)

```
App
├── Header
│   ├── Title: "Healthcare AI System"
│   └── Tagline
│
├── Main Content (conditional rendering)
│   │
│   ├── FileUpload (currentView === 'upload')
│   │   ├── Form
│   │   │   ├── Patient Name Input
│   │   │   ├── Age Input
│   │   │   ├── Gender Select
│   │   │   ├── File Input
│   │   │   └── Submit Button
│   │   └── Error Display
│   │
│   ├── ProcessingStatus (currentView === 'processing')
│   │   ├── Status Text
│   │   ├── Progress Bar
│   │   ├── Step Indicators
│   │   │   ├── OCR Step
│   │   │   ├── Cleaning Step
│   │   │   └── Summary Step
│   │   └── Spinner
│   │
│   └── SummaryView (currentView === 'summary')
│       ├── Header
│       │   ├── Back Button
│       │   └── Visit Info
│       ├── Tabs
│       │   ├── Summary Tab
│       │   ├── Comparison Tab
│       │   └── Extracted Data Tab
│       └── Tab Content (dynamic)
│           ├── Summary Content
│           │   ├── Medical Summary
│           │   ├── Key Findings
│           │   └── Quick Info
│           ├── Comparison View
│           │   ├── Original OCR Text
│           │   └── Cleaned Text
│           └── Extracted Data
│               ├── Symptoms List
│               ├── Medications List
│               ├── Test Results
│               └── JSON Display
│
└── Footer
```

## API Request Flow

```
UPLOAD FLOW:
Client ──POST /upload/──► Backend
         FormData          │
         (file, metadata)  │
                          │
                          ├─► Save File
                          ├─► Create Patient
                          ├─► Create Visit
                          └─► Create Document
                          
Response ◄────────────────┘
         { visit_id, 
           patient_id,
           document_id }

OCR FLOW:
Client ──POST /ocr/{visit_id}──► Backend
                                  │
                                  ├─► Get Document
                                  ├─► OCR Service
                                  │   └─► PaddleOCR
                                  └─► Save OCR Text
                                  
Response ◄────────────────────────┘
         { ocr_id,
           raw_text,
           confidence }

CLEAN FLOW:
Client ──POST /clean/{visit_id}──► Backend
                                   │
                                   ├─► Get OCR Text
                                   ├─► LLM Service
                                   │   └─► Groq API
                                   │       ├─► Clean Text
                                   │       └─► Extract Data
                                   └─► Save Cleaned Text
                                   
Response ◄─────────────────────────┘
         { cleaned_id,
           cleaned_text,
           extracted_data }

SUMMARIZE FLOW:
Client ──POST /summarize/{visit_id}──► Backend
                                       │
                                       ├─► Get Cleaned Text
                                       ├─► LLM Service
                                       │   └─► Groq API
                                       │       ├─► Generate Summary
                                       │       └─► Extract Findings
                                       └─► Save Summary
                                       
Response ◄─────────────────────────────┘
         { summary_id,
           summary_text,
           key_findings }

GET SUMMARY FLOW:
Client ──GET /summarize/{visit_id}──► Backend
                                      │
                                      ├─► Get Visit
                                      ├─► Get OCR Text
                                      ├─► Get Cleaned Text
                                      └─► Get Summary
                                      
Response ◄────────────────────────────┘
         { ocr_text,
           cleaned_text,
           extracted_data,
           summary,
           key_findings }
```

## File Storage Structure

```
backend/
└── uploads/
    ├── VIS_ABC123DEF456/          (visit_id)
    │   ├── medical_report.pdf
    │   └── lab_results.jpg
    │
    ├── VIS_XYZ789GHI012/
    │   └── prescription.pdf
    │
    └── VIS_LMN345PQR678/
        ├── xray.jpg
        └── blood_test.pdf

Each visit has its own folder for file organization.
```

## Technology Stack Layers

```
┌─────────────────────────────────────────┐
│         PRESENTATION LAYER               │
│  React, HTML, CSS, JavaScript            │
│  Components, Styling, User Interaction   │
└───────────────┬─────────────────────────┘
                │
┌───────────────▼─────────────────────────┐
│         APPLICATION LAYER                │
│  FastAPI, Python                         │
│  API Endpoints, Business Logic           │
└───────────────┬─────────────────────────┘
                │
┌───────────────▼─────────────────────────┐
│         SERVICE LAYER                    │
│  OCR Service, LLM Service, DB Service    │
│  PaddleOCR, Groq API, SQLAlchemy         │
└───────────────┬─────────────────────────┘
                │
┌───────────────▼─────────────────────────┐
│         DATA LAYER                       │
│  PostgreSQL Database                     │
│  File Storage System                     │
└─────────────────────────────────────────┘
```

## Error Handling Flow

```
┌─────────────┐
│   Request   │
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│ Try-Catch Block  │
└──────┬───────────┘
       │
       ├──► Success ──► Return Response (200)
       │
       └──► Error
             │
             ├──► Validation Error ──► 400 Bad Request
             ├──► Not Found ──► 404 Not Found
             ├──► Database Error ──► 500 Internal Error
             ├──► OCR Error ──► 500 + Fallback
             ├──► LLM Error ──► 500 + Fallback
             └──► General Error ──► 500 + Log
```

---

## Quick Reference

**Frontend**: React (Port 3000)
**Backend**: FastAPI (Port 8000)
**Database**: PostgreSQL (Port 5432)
**OCR**: PaddleOCR
**LLM**: Groq API (Llama 3.3 70B)

**Total Pipeline**: Upload → OCR → Clean → Summarize → Display
**Estimated Time**: 15-40 seconds
