import os
import json
import logging
from typing import Dict, Any, Optional
from groq import Groq
from ..core.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    """
    Service for LLM-based text processing using Groq API
    """
    
    def __init__(self):
        """
        Initialize Groq client
        """
        try:
            if not settings.GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY not found in environment variables")
            
            self.client = Groq(api_key=settings.GROQ_API_KEY)
            self.model = settings.GROQ_MODEL
            logger.info(f"Groq LLM client initialized with model: {self.model}")
        except Exception as e:
            logger.error(f"Error initializing Groq client: {str(e)}")
            raise
    
    def clean_ocr_text(self, ocr_text: str) -> str:
        """
        Clean OCR-extracted text using LLM
        
        Args:
            ocr_text: Raw OCR extracted text
            
        Returns:
            Cleaned and corrected text
        """
        try:
            prompt = f"""You are a medical language expert.

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

Provide ONLY the cleaned text without any explanations or additional comments."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a medical text processing expert. Clean and correct OCR text while preserving original medical information."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=2048
            )
            
            cleaned_text = response.choices[0].message.content.strip()
            return cleaned_text
            
        except Exception as e:
            logger.error(f"Error cleaning OCR text: {str(e)}")
            return ocr_text  # Return original text if cleaning fails
    
    def extract_structured_data(self, cleaned_text: str) -> Dict[str, Any]:
        """
        Extract structured medical data from cleaned text
        
        Args:
            cleaned_text: Cleaned medical text
            
        Returns:
            Dictionary containing structured medical information
        """
        try:
            prompt = f"""You are a medical data extraction expert.

Extract the following information from the medical text below.
Return ONLY a valid JSON object with these fields (use null if information is not available):
{{
    "patient_name": "string or null",
    "age": "string or null",
    "gender": "string or null",
    "symptoms": ["list of symptoms"],
    "diagnosis": "string or null",
    "medications": ["list of medications with dosage"],
    "test_results": ["list of test results"],
    "vital_signs": {{}},
    "doctor_notes": "string or null",
    "date_of_visit": "string or null"
}}

Medical Text:
{cleaned_text}

Return ONLY the JSON object, no additional text."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a medical data extraction expert. Extract structured information from medical text and return valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2,
                max_tokens=1024
            )
            
            json_text = response.choices[0].message.content.strip()
            
            # Try to parse JSON
            try:
                # Remove markdown code blocks if present
                if json_text.startswith("```"):
                    json_text = json_text.split("```")[1]
                    if json_text.startswith("json"):
                        json_text = json_text[4:]
                    json_text = json_text.strip()
                
                structured_data = json.loads(json_text)
                return structured_data
            except json.JSONDecodeError:
                logger.warning("Could not parse JSON response, returning empty structure")
                return {
                    "patient_name": None,
                    "age": None,
                    "gender": None,
                    "symptoms": [],
                    "diagnosis": None,
                    "medications": [],
                    "test_results": [],
                    "vital_signs": {},
                    "doctor_notes": None,
                    "date_of_visit": None
                }
            
        except Exception as e:
            logger.error(f"Error extracting structured data: {str(e)}")
            return {}
    
    def generate_medical_summary(self, cleaned_text: str) -> str:
        """
        Generate concise medical summary from cleaned text
        
        Args:
            cleaned_text: Cleaned medical text
            
        Returns:
            Generated medical summary
        """
        try:
            prompt = f"""You are an assistant helping doctors review medical records.

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

Provide a well-structured medical summary."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a medical summarization expert. Generate concise, accurate clinical summaries for healthcare professionals."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=1024
            )
            
            summary = response.choices[0].message.content.strip()
            return summary
            
        except Exception as e:
            logger.error(f"Error generating medical summary: {str(e)}")
            return "Error generating summary. Please try again."
    
    def extract_key_findings(self, summary_text: str) -> str:
        """
        Extract bullet points of key findings from summary
        
        Args:
            summary_text: Generated summary text
            
        Returns:
            Key findings as bullet points
        """
        try:
            prompt = f"""Extract 3-5 key medical findings from this summary as bullet points.

Summary:
{summary_text}

Provide ONLY the bullet points, one per line, starting with a dash (-)."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=256
            )
            
            key_findings = response.choices[0].message.content.strip()
            return key_findings
            
        except Exception as e:
            logger.error(f"Error extracting key findings: {str(e)}")
            return ""
