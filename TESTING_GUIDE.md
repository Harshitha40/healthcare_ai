# Testing the Healthcare AI System

## Sample Medical Records for Testing

### Creating Test Documents

You can create sample medical documents to test the system. Here are some examples:

---

## Sample 1: Basic Medical Report

Create a text file and save as PDF or convert to image:

```
MEDICAL CENTER HOSPITAL
Patient Medical Record

Patient Name: John Doe
Date of Birth: 05/15/1978
Age: 45 years
Gender: Male
Date of Visit: December 20, 2025

CHIEF COMPLAINT:
Patient presents with persistent fever and dry cough for the past 3 days.

VITAL SIGNS:
Temperature: 101.5°F
Blood Pressure: 130/85 mmHg
Heart Rate: 88 bpm
Respiratory Rate: 18/min
SpO2: 96% on room air

PHYSICAL EXAMINATION:
- General: Patient appears mildly uncomfortable
- Respiratory: Bilateral clear lung sounds, no wheezing
- Cardiovascular: Regular rate and rhythm

LABORATORY RESULTS:
WBC: 12,500 cells/μL (elevated)
Hemoglobin: 14.2 g/dL
Platelets: 245,000/μL
COVID-19 PCR: Negative

DIAGNOSIS:
Upper Respiratory Tract Infection (URTI)

TREATMENT PLAN:
1. Amoxicillin 500mg TID x 7 days
2. Acetaminophen 650mg PRN for fever
3. Adequate hydration
4. Rest

FOLLOW-UP:
Return if symptoms worsen or persist beyond 7 days.

Dr. Sarah Johnson, MD
License #: 12345
```

---

## Sample 2: Prescription Record

```
PRESCRIPTION

Patient: Emily Chen
Age: 32
Gender: Female
Date: 12/20/2025

Rx:
1. Metformin 500mg - Take 1 tablet twice daily with meals
   Duration: 30 days
   Refills: 2

2. Lisinopril 10mg - Take 1 tablet once daily in the morning
   Duration: 30 days
   Refills: 3

3. Atorvastatin 20mg - Take 1 tablet at bedtime
   Duration: 30 days
   Refills: 3

DIAGNOSIS: Type 2 Diabetes Mellitus, Hypertension

NOTES: Patient advised regarding lifestyle modifications,
dietary changes, and regular blood glucose monitoring.

Dr. Michael Brown
Internal Medicine
DEA: AB1234567
```

---

## Sample 3: Lab Report

```
LABORATORY REPORT

Patient: Robert Smith
MR#: 789456
DOB: 03/22/1960
Date Collected: 12/19/2025
Date Reported: 12/20/2025

COMPLETE BLOOD COUNT (CBC):
WBC: 7,200 cells/μL (Normal: 4,000-11,000)
RBC: 4.8 million/μL (Normal: 4.5-5.5)
Hemoglobin: 14.5 g/dL (Normal: 13.5-17.5)
Hematocrit: 42% (Normal: 38-50)
Platelets: 250,000/μL (Normal: 150,000-400,000)

COMPREHENSIVE METABOLIC PANEL:
Glucose: 105 mg/dL (Normal: 70-100) - Slightly Elevated
Creatinine: 1.0 mg/dL (Normal: 0.7-1.3)
BUN: 18 mg/dL (Normal: 7-20)
Sodium: 140 mEq/L (Normal: 136-145)
Potassium: 4.2 mEq/L (Normal: 3.5-5.1)

LIPID PANEL:
Total Cholesterol: 210 mg/dL (Borderline High)
LDL: 130 mg/dL (Borderline High)
HDL: 45 mg/dL (Low)
Triglycerides: 175 mg/dL (Borderline High)

INTERPRETATION:
Prediabetic glucose levels. Lipid profile shows borderline
cardiovascular risk. Recommend lifestyle modifications.

Reviewed by: Dr. Jennifer Lee, MD
Pathologist
```

---

## Sample 4: Emergency Room Visit

```
EMERGENCY DEPARTMENT REPORT

Patient Name: Maria Garcia
Age: 28 years
Gender: Female
Arrival Time: 12/20/2025 22:30
Chief Complaint: Severe abdominal pain

HISTORY OF PRESENT ILLNESS:
28-year-old female presents with sudden onset severe right
lower quadrant abdominal pain for the past 6 hours.
Associated with nausea and one episode of vomiting.
Denies fever, diarrhea, or urinary symptoms.

PHYSICAL EXAMINATION:
Vitals: BP 125/80, HR 92, Temp 98.8°F, RR 16
Abdomen: Tender in RLQ with rebound tenderness
McBurney's point positive
No guarding, normal bowel sounds

INVESTIGATIONS:
CBC: WBC 14,200 (elevated)
Ultrasound: Findings suggestive of acute appendicitis
CT Abdomen: Inflamed appendix, no perforation

DIAGNOSIS:
Acute Appendicitis

DISPOSITION:
Patient admitted for emergency appendectomy
Surgery consultation obtained
Patient and family counseled regarding procedure

Attending Physician: Dr. David Martinez, MD
Emergency Medicine
```

---

## Sample 5: Handwritten-Style Report (for OCR Testing)

Create this in a document with some intentional "OCR errors":

```
Patient Naame: Willam Jonhson
Aga: 67 yrs
Gendr: Male

Cheif Complaint:
Shortnes of breath and chast pain

Medicatins:
- Asprin 81mg daily
- Metropolol 50mg BID
- Atorvastitin 40mg HS

Dignosis:
Coronary artery disese
Hypertension

Plan:
Continue medicatons
Cardiology folowup in 2 weks
```

This will test the LLM's ability to clean and correct OCR errors!

---

## How to Create Test PDFs

### Method 1: Using Word/Google Docs
1. Copy any sample above
2. Paste into Word or Google Docs
3. Save/Export as PDF

### Method 2: Using Print to PDF
1. Paste text into Notepad or any text editor
2. Print → Choose "Microsoft Print to PDF"
3. Save the PDF

### Method 3: Create Image Files
1. Take a screenshot of the text
2. Save as JPG or PNG
3. Or use your phone to take a photo of printed text

---

## Testing Different Scenarios

### Test 1: Clear Digital Text
Use Sample 1 or 2 as a clean PDF
**Expected**: High OCR confidence, minimal cleaning needed

### Test 2: Low-Quality Scan
Convert Sample 3 to image, then print and scan
**Expected**: Lower OCR confidence, more LLM cleaning

### Test 3: Handwritten/OCR Errors
Use Sample 5 with intentional errors
**Expected**: LLM should correct spelling and medical terms

### Test 4: Complex Medical Terminology
Use Sample 4 with complex terms
**Expected**: Proper extraction of medical terms

---

## What to Look For

### OCR Quality
- ✅ Text extraction accuracy
- ✅ Handling of medical terminology
- ✅ Multi-line and paragraph handling

### Text Cleaning
- ✅ Spelling corrections
- ✅ Medical term corrections
- ✅ Grammar improvements
- ✅ Format preservation

### Structured Extraction
- ✅ Patient name extraction
- ✅ Age and gender identification
- ✅ Symptoms list
- ✅ Diagnosis extraction
- ✅ Medications with dosages
- ✅ Test results

### Summary Quality
- ✅ Concise and accurate
- ✅ Key findings highlighted
- ✅ Doctor-friendly language
- ✅ No hallucinations

---

## Performance Benchmarks

Expected processing times (approximate):

- **Upload**: < 1 second
- **OCR** (1-page PDF): 3-10 seconds
- **OCR** (image): 5-15 seconds
- **Cleaning**: 5-10 seconds
- **Summarization**: 5-10 seconds
- **Total**: 15-40 seconds

---

## Common OCR Challenges

1. **Poor Image Quality**: Blurry or low-resolution images
2. **Handwritten Text**: Difficult to OCR, may need manual entry
3. **Complex Layouts**: Tables and multi-column formats
4. **Special Characters**: Medical symbols may not OCR well
5. **Scanned Documents**: Older scans with noise

---

## Tips for Best Results

1. **Use high-resolution images** (300+ DPI)
2. **Ensure good lighting** for photos
3. **Avoid shadows** on documents
4. **Keep text horizontal** (no rotation)
5. **Use clean, printed text** when possible

---

## Real-World Testing

For real medical records:
- ⚠️ **NEVER** upload actual patient data during development
- ✅ **Remove** all identifying information (HIPAA)
- ✅ **Create** realistic but fake examples
- ✅ **Use** de-identified historical records if available

---

## Automated Testing

You can automate testing with scripts:

```python
# Example test script
import requests

def test_upload():
    files = {'file': open('sample_report.pdf', 'rb')}
    data = {
        'patient_name': 'Test Patient',
        'patient_age': '45',
        'patient_gender': 'Male'
    }
    response = requests.post('http://localhost:8000/upload/', 
                            files=files, data=data)
    return response.json()

# Run test
result = test_upload()
print(f"Visit ID: {result['visit_id']}")
```

---

## Troubleshooting Test Issues

### OCR Returns Empty Text
- Check file format (PDF vs image)
- Verify file is not corrupted
- Try a cleaner, simpler document first

### LLM Cleaning Takes Too Long
- Check Groq API key is valid
- Verify internet connection
- Check Groq API rate limits

### Summary is Inaccurate
- Verify cleaned text is correct first
- Try adjusting LLM prompts
- Check if medical terminology is preserved

---

**Happy Testing! 🧪**
