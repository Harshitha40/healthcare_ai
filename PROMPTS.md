# GROQ LLM PROMPTS USED IN THE SYSTEM

This document contains all the prompts used in the Healthcare AI System for reference and customization.

## 1. OCR Text Cleaning Prompt

**Location:** `backend/app/services/llm_service.py` - `clean_ocr_text()` method

**Purpose:** Clean and correct raw OCR-extracted text from medical documents

**Prompt:**
```
You are a medical language expert.

Clean the following OCR-extracted medical text:
- Fix spelling and grammar errors
- Correct medical terminology
- Remove OCR artifacts and noise
- Fix formatting issues
- Do NOT add new information
- Do NOT make assumptions
- Preserve clinical meaning exactly

OCR Text:
{ocr_text}

Provide ONLY the cleaned text without any explanations or additional comments.
```

**System Message:**
```
You are a medical text processing expert. Clean and correct OCR text while preserving original medical information.
```

**Parameters:**
- Temperature: 0.3 (low temperature for consistency)
- Max Tokens: 2048

---

## 2. Structured Data Extraction Prompt

**Location:** `backend/app/services/llm_service.py` - `extract_structured_data()` method

**Purpose:** Extract structured medical information from cleaned text

**Prompt:**
```
You are a medical data extraction expert.

Extract the following information from the medical text below.
Return ONLY a valid JSON object with these fields (use null if information is not available):
{
    "patient_name": "string or null",
    "age": "string or null",
    "gender": "string or null",
    "symptoms": ["list of symptoms"],
    "diagnosis": "string or null",
    "medications": ["list of medications with dosage"],
    "test_results": ["list of test results"],
    "vital_signs": {},
    "doctor_notes": "string or null",
    "date_of_visit": "string or null"
}

Medical Text:
{cleaned_text}

Return ONLY the JSON object, no additional text.
```

**System Message:**
```
You are a medical data extraction expert. Extract structured information from medical text and return valid JSON.
```

**Parameters:**
- Temperature: 0.2 (very low for consistent structured output)
- Max Tokens: 1024

---

## 3. Medical Summary Generation Prompt

**Location:** `backend/app/services/llm_service.py` - `generate_medical_summary()` method

**Purpose:** Generate concise, doctor-friendly medical summary

**Prompt:**
```
You are an assistant helping doctors review medical records.

Generate a concise medical summary from the following clinical text.

Focus on:
- Key symptoms and complaints
- Diagnosis (if mentioned)
- Medications prescribed
- Important test results and vital signs
- Critical observations
- Follow-up recommendations

Guidelines:
- Be concise and doctor-friendly
- Use medical terminology appropriately
- Do NOT make assumptions or new diagnoses
- Do NOT add information not present in the text
- Highlight only key medical findings
- Structure the summary clearly

Clinical Text:
{cleaned_text}

Provide a well-structured medical summary.
```

**System Message:**
```
You are a medical summarization expert. Generate concise, accurate clinical summaries for healthcare professionals.
```

**Parameters:**
- Temperature: 0.3 (low temperature for medical accuracy)
- Max Tokens: 1024

---

## 4. Key Findings Extraction Prompt

**Location:** `backend/app/services/llm_service.py` - `extract_key_findings()` method

**Purpose:** Extract 3-5 key bullet points from the summary

**Prompt:**
```
Extract 3-5 key medical findings from this summary as bullet points.

Summary:
{summary_text}

Provide ONLY the bullet points, one per line, starting with a dash (-).
```

**Parameters:**
- Temperature: 0.3
- Max Tokens: 256

---

## Customization Guide

### Adjusting Temperature
- **Lower (0.0-0.3)**: More deterministic, consistent outputs (recommended for medical text)
- **Medium (0.4-0.7)**: Balanced creativity and consistency
- **Higher (0.8-1.0)**: More creative but less consistent (NOT recommended for medical use)

### Modifying Prompts

To modify these prompts, edit the files in:
```
backend/app/services/llm_service.py
```

### Example Customization

**Add more fields to structured extraction:**
```python
{
    "patient_name": "string or null",
    "age": "string or null",
    "gender": "string or null",
    "symptoms": ["list of symptoms"],
    "diagnosis": "string or null",
    "medications": ["list of medications with dosage"],
    "test_results": ["list of test results"],
    "vital_signs": {},
    "doctor_notes": "string or null",
    "date_of_visit": "string or null",
    
    # Add these new fields:
    "allergies": ["list of allergies"],
    "family_history": "string or null",
    "social_history": "string or null",
    "immunizations": ["list of immunizations"]
}
```

### Testing Different Models

Edit `backend/.env`:
```env
# Available Groq models:
GROQ_MODEL=llama-3.3-70b-versatile     # Default, best balance
# GROQ_MODEL=llama-3.1-70b-versatile   # Alternative
# GROQ_MODEL=mixtral-8x7b-32768        # Longer context
```

### Best Practices

1. **Always test with real medical documents** after changing prompts
2. **Keep temperature low (0.2-0.3)** for medical accuracy
3. **Be explicit** about what NOT to do (no assumptions, no new info)
4. **Use structured output** (JSON) for data extraction
5. **Preserve medical terminology** - don't oversimplify
6. **Include error handling** for LLM failures

### Monitoring Prompt Performance

Add logging to track:
- Processing time per prompt
- Token usage
- Error rates
- Output quality

### Example Enhanced Error Handling

```python
try:
    response = self.client.chat.completions.create(...)
    return response.choices[0].message.content.strip()
except Exception as e:
    logger.error(f"LLM Error: {str(e)}")
    # Fallback behavior
    return original_text
```

---

## Performance Tips

1. **Batch processing**: Process multiple documents in parallel
2. **Caching**: Cache common cleaning patterns
3. **Prompt optimization**: Shorter prompts = faster responses
4. **Streaming**: Use streaming for real-time feedback
5. **Retries**: Implement retry logic for failures

---

## Compliance Notes

When modifying prompts for production:
- Ensure HIPAA compliance
- Add data anonymization instructions
- Include PHI handling guidelines
- Document all prompt changes
- Test thoroughly with varied inputs
