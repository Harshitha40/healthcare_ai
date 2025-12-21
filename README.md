# Healthcare AI System

A complete, production-ready web application for processing patient medical records using AI. The system performs OCR on medical documents, cleans the extracted text, and generates concise medical summaries using LLM.

## 🏗️ Project Structure

```
proj/
├── backend/
│   ├── app/
│   │   ├── api/              # FastAPI endpoints
│   │   │   ├── upload.py     # File upload endpoint
│   │   │   ├── ocr.py        # OCR processing endpoint
│   │   │   ├── clean.py      # Text cleaning endpoint
│   │   │   ├── summarize.py  # Summary generation endpoint
│   │   │   └── visits.py     # Visit management endpoints
│   │   ├── core/             # Core configuration
│   │   │   ├── config.py     # Settings and environment variables
│   │   │   └── database.py   # Database connection and session
│   │   ├── models/           # SQLAlchemy database models
│   │   │   ├── patient.py
│   │   │   ├── visit.py
│   │   │   ├── document.py
│   │   │   ├── ocr_text.py
│   │   │   ├── cleaned_text.py
│   │   │   └── summary.py
│   │   ├── schemas/          # Pydantic schemas
│   │   └── services/         # Business logic services
│   │       ├── ocr_service.py      # PaddleOCR integration
│   │       ├── llm_service.py      # Groq LLM integration
│   │       └── database_service.py # Database operations
│   ├── uploads/              # Uploaded files storage
│   ├── main.py               # FastAPI application entry point
│   ├── requirements.txt      # Python dependencies
│   └── .env.example          # Environment variables template
│
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── FileUpload.jsx       # File upload form
│   │   │   ├── ProcessingStatus.jsx # Processing progress
│   │   │   └── SummaryView.jsx      # Summary display
│   │   ├── services/         # API services
│   │   │   └── api.js        # Axios API client
│   │   ├── styles/           # CSS files
│   │   ├── App.jsx           # Main app component
│   │   └── main.jsx          # React entry point
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
└── database/
    └── schema.sql            # PostgreSQL database schema
```

## 🚀 Features

### 1. File Upload
- Upload PDF or image medical records
- Support for scanned reports and handwritten notes
- Optional patient information input
- Automatic patient_id and visit_id generation

### 2. OCR Processing (PaddleOCR)
- Extract text from PDF and image files
- Image preprocessing for better accuracy
- Multi-page PDF support
- Confidence score tracking

### 3. Text Cleaning (LLM-Assisted)
- Fix spelling and grammar errors
- Correct medical terminology
- Remove OCR noise and artifacts
- Preserve original clinical meaning

### 4. Structured Data Extraction
- Extract patient details
- Identify symptoms
- Extract diagnosis
- List medications
- Capture test results
- Store as structured JSON

### 5. Medical Summarization
- Generate concise clinical summaries
- Doctor-friendly format
- Highlight key medical findings
- Extract key findings as bullet points

### 6. Modern React UI
- Clean, hospital-style interface
- Real-time processing status
- Side-by-side comparison view
- Tabbed interface for different views
- Responsive design

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**
- **FastAPI** - Modern web framework
- **PaddleOCR** - OCR text extraction
- **Groq API** - LLM for cleaning and summarization
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **Axios** - HTTP client
- **Modern CSS** - Styling

## 📋 Prerequisites

1. **Python 3.8 or higher**
2. **Node.js 16 or higher**
3. **PostgreSQL 12 or higher**
4. **Groq API Key** (get from https://console.groq.com)

## 🔧 Installation & Setup

### 1. Database Setup

```bash
# Install PostgreSQL if not already installed
# Windows: Download from https://www.postgresql.org/download/windows/
# macOS: brew install postgresql
# Linux: sudo apt-get install postgresql

# Start PostgreSQL service
# Windows: Start from Services
# macOS/Linux: sudo service postgresql start

# Create database
psql -U postgres
CREATE DATABASE healthcare_ai;
\q

# Run schema (optional - SQLAlchemy will create tables automatically)
psql -U postgres -d healthcare_ai -f database/schema.sql
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env    # Windows
# cp .env.example .env    # macOS/Linux

# Edit .env file and add your credentials:
# - DATABASE_URL (PostgreSQL connection string)
# - GROQ_API_KEY (your Groq API key)
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

## ▶️ Running the Application

### Start Backend Server

```bash
# From backend directory with venv activated
cd backend
python main.py

# Server will start at http://localhost:8000
# API docs available at http://localhost:8000/docs
```

### Start Frontend Development Server

```bash
# From frontend directory (in a new terminal)
cd frontend
npm run dev

# App will open at http://localhost:3000
```

## 🔑 Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:password@localhost:5432/healthcare_ai

# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# File Upload Settings
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760

# CORS Settings
CORS_ORIGINS=["http://localhost:3000"]
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload/` | Upload medical document |
| POST | `/ocr/{visit_id}` | Perform OCR on document |
| POST | `/clean/{visit_id}` | Clean OCR text |
| POST | `/summarize/{visit_id}` | Generate medical summary |
| GET | `/summarize/{visit_id}` | Get complete summary data |
| GET | `/visits/` | List all visits |
| GET | `/visits/{visit_id}` | Get visit details |
| GET | `/health` | Health check |

## 📝 Usage Flow

1. **Upload Document**
   - Open the application at http://localhost:3000
   - Fill in optional patient information
   - Select a medical document (PDF or image)
   - Click "Upload & Process"

2. **Automatic Processing**
   - System performs OCR extraction
   - Cleans and corrects the text
   - Generates medical summary
   - Progress is shown in real-time

3. **View Results**
   - **Summary Tab**: View the AI-generated medical summary
   - **Original vs Cleaned Tab**: Compare OCR text with cleaned text
   - **Extracted Data Tab**: View structured medical information

## 🧪 Testing

### Test with Sample Medical Document

1. Create a sample medical document with text like:
```
Patient Name: John Doe
Age: 45
Chief Complaint: Fever and cough for 3 days
Diagnosis: Upper respiratory tract infection
Medications: Amoxicillin 500mg TID x 7 days
```

2. Save as PDF or image
3. Upload through the web interface

## 🔒 Security Considerations

- Never commit `.env` file with real credentials
- Use strong database passwords
- Keep Groq API key secure
- Implement proper authentication for production
- Add rate limiting
- Sanitize user inputs
- Use HTTPS in production

## 🚀 Deployment

### Backend (Example using Docker)

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend (Example using Netlify/Vercel)

```bash
# Build frontend
cd frontend
npm run build

# Deploy the 'dist' folder to your hosting provider
```

## 🐛 Troubleshooting

### PaddleOCR Installation Issues
```bash
# If PaddleOCR fails to install, try:
pip install paddlepaddle==2.6.0 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install paddleocr==2.7.0.3
```

### Database Connection Issues
- Verify PostgreSQL is running
- Check DATABASE_URL in .env
- Ensure database exists
- Check firewall settings

### CORS Issues
- Verify frontend URL is in CORS_ORIGINS
- Check browser console for specific errors

## 📦 Dependencies

### Backend Key Dependencies
- fastapi==0.109.0
- uvicorn==0.27.0
- paddleocr==2.7.0.3
- groq==0.4.2
- sqlalchemy==2.0.25
- psycopg2-binary==2.9.9

### Frontend Key Dependencies
- react==18.2.0
- axios==1.6.5
- vite==5.0.11

## 🎯 Future Enhancements

- [ ] User authentication and authorization
- [ ] Multi-user support with role-based access
- [ ] Document history and versioning
- [ ] Batch processing
- [ ] Export summaries as PDF
- [ ] Medical chat assistant
- [ ] Predictive analytics
- [ ] Integration with EHR systems

## 📄 License

This project is for educational and development purposes.

## 👥 Support

For issues and questions:
- Check the troubleshooting section
- Review API documentation at http://localhost:8000/docs
- Check application logs for error details

## 🎓 Credits

- **PaddleOCR** - OCR Engine
- **Groq** - LLM API
- **FastAPI** - Backend Framework
- **React** - Frontend Framework

---

## 📌 Important Notes

1. This is a development version - additional security measures needed for production
2. Ensure HIPAA compliance if handling real patient data
3. Regularly backup the database
4. Monitor API usage and costs (Groq API)
5. Test thoroughly with various document types

**Built with ❤️ for Healthcare AI Innovation**
