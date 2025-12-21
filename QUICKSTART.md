# Quick Start Guide

## Step-by-Step Setup (Windows)

### 1. Install Prerequisites

#### PostgreSQL
1. Download from: https://www.postgresql.org/download/windows/
2. Run installer (keep default port 5432)
3. Remember the password you set for 'postgres' user
4. Add PostgreSQL to PATH (installer option)

#### Python
1. Download Python 3.10+ from: https://www.python.org/downloads/
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Verify: `python --version`

#### Node.js
1. Download from: https://nodejs.org/
2. Run installer (LTS version recommended)
3. Verify: `node --version` and `npm --version`

### 2. Setup Database

```powershell
# Open PowerShell and connect to PostgreSQL
psql -U postgres

# In PostgreSQL prompt:
CREATE DATABASE healthcare_ai;
\q
```

### 3. Setup Backend

```powershell
# Navigate to backend folder
cd C:\Users\Lenovo\aimlel\proj\backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies (this may take 5-10 minutes)
pip install -r requirements.txt

# Copy environment file
copy .env.example .env

# Edit .env file (use notepad or any text editor)
notepad .env
```

**Edit .env file:**
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/healthcare_ai
GROQ_API_KEY=your_groq_api_key_here
```

**Get Groq API Key:**
1. Go to https://console.groq.com
2. Sign up / Log in
3. Go to API Keys section
4. Create new API key
5. Copy and paste into .env file

### 4. Setup Frontend

```powershell
# Open NEW PowerShell window
cd C:\Users\Lenovo\aimlel\proj\frontend

# Install dependencies
npm install
```

### 5. Run the Application

#### Terminal 1 - Backend:
```powershell
cd C:\Users\Lenovo\aimlel\proj\backend
.\venv\Scripts\activate
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### Terminal 2 - Frontend:
```powershell
cd C:\Users\Lenovo\aimlel\proj\frontend
npm run dev
```

You should see:
```
  VITE v5.0.11  ready in XXX ms

  ➜  Local:   http://localhost:3000/
```

### 6. Access the Application

Open browser and go to: **http://localhost:3000**

### 7. Test the Application

1. Click "Choose PDF or Image file"
2. Select a medical document (PDF or image)
3. Fill in optional patient info
4. Click "Upload & Process"
5. Wait for processing (OCR → Cleaning → Summary)
6. View results!

---

## Common Issues & Solutions

### Issue: "psycopg2 installation failed"
**Solution:**
```powershell
pip install psycopg2-binary
```

### Issue: "PaddleOCR installation failed"
**Solution:**
```powershell
pip install paddlepaddle==2.6.0
pip install paddleocr==2.7.0.3
```

### Issue: "Cannot connect to database"
**Solutions:**
1. Check PostgreSQL is running (Services → PostgreSQL)
2. Verify password in .env file
3. Test connection:
```powershell
psql -U postgres -d healthcare_ai
```

### Issue: "GROQ_API_KEY not found"
**Solution:**
1. Make sure .env file exists in backend folder
2. Check API key is correctly pasted (no extra spaces)
3. Restart backend server

### Issue: "CORS error in browser"
**Solution:**
1. Make sure backend is running on port 8000
2. Make sure frontend is running on port 3000
3. Check browser console for specific error

### Issue: "Port already in use"
**Solution - Backend:**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000
# Kill process (use PID from above)
taskkill /PID <PID> /F
```

**Solution - Frontend:**
```powershell
# Find process using port 3000
netstat -ano | findstr :3000
# Kill process
taskkill /PID <PID> /F
```

---

## First Time Run Checklist

- [ ] PostgreSQL installed and running
- [ ] Python 3.10+ installed
- [ ] Node.js installed
- [ ] Database 'healthcare_ai' created
- [ ] Backend virtual environment created
- [ ] Backend dependencies installed
- [ ] .env file created with correct values
- [ ] GROQ_API_KEY added to .env
- [ ] Frontend dependencies installed
- [ ] Backend server running (port 8000)
- [ ] Frontend server running (port 3000)
- [ ] Browser opened to http://localhost:3000

---

## Stopping the Application

### Stop Backend:
- Press `Ctrl+C` in backend terminal

### Stop Frontend:
- Press `Ctrl+C` in frontend terminal

### Deactivate Virtual Environment:
```powershell
deactivate
```

---

## Daily Development Workflow

### Start Development:
```powershell
# Terminal 1 - Backend
cd C:\Users\Lenovo\aimlel\proj\backend
.\venv\Scripts\activate
python main.py

# Terminal 2 - Frontend
cd C:\Users\Lenovo\aimlel\proj\frontend
npm run dev
```

### Stop Development:
- Press `Ctrl+C` in both terminals

---

## Testing API Directly

### Using Browser:
Visit: http://localhost:8000/docs

This opens FastAPI's interactive API documentation where you can test all endpoints.

### Health Check:
Visit: http://localhost:8000/health

Should return:
```json
{
  "status": "healthy",
  "service": "Healthcare AI System"
}
```

---

## Next Steps

1. ✅ Get the system running
2. 📄 Test with sample medical documents
3. 🎨 Customize the UI (frontend/src/styles/)
4. 🔧 Adjust prompts (PROMPTS.md)
5. 📊 Add more features
6. 🚀 Deploy to production

---

## Support & Resources

- **API Documentation**: http://localhost:8000/docs
- **Groq API Docs**: https://console.groq.com/docs
- **PaddleOCR Docs**: https://github.com/PaddlePaddle/PaddleOCR
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **React Docs**: https://react.dev/

---

**🎉 You're ready to build amazing healthcare AI applications!**
