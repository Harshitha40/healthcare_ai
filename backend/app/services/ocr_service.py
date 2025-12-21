import os
import cv2
import numpy as np
from paddleocr import PaddleOCR
from typing import Tuple, Optional
import logging
from PIL import Image
import fitz  # PyMuPDF for PDF handling

logger = logging.getLogger(__name__)


class OCRService:
    """
    Service for OCR text extraction using PaddleOCR
    """
    
    def __init__(self):
        """
        Initialize PaddleOCR with English language support
        """
        try:
            self.ocr = PaddleOCR(
                use_angle_cls=True,
                lang='en',
                use_gpu=False,
                show_log=False
            )
            logger.info("PaddleOCR initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing PaddleOCR: {str(e)}")
            raise
    
    def preprocess_image(self, image_path: str) -> Optional[np.ndarray]:
        """
        Preprocess image to improve OCR accuracy
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Preprocessed image as numpy array
        """
        try:
            # Read image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Could not read image: {image_path}")
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Apply denoising
            denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
            
            # Apply adaptive thresholding
            binary = cv2.adaptiveThreshold(
                denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 11, 2
            )
            
            return binary
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            return None
    
    def pdf_to_images(self, pdf_path: str) -> list:
        """
        Convert PDF pages to images
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of image arrays
        """
        try:
            images = []
            pdf_document = fitz.open(pdf_path)
            
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                
                # Render page to image (higher resolution for better OCR)
                mat = fitz.Matrix(2, 2)  # 2x zoom for better quality
                pix = page.get_pixmap(matrix=mat)
                
                # Convert to numpy array
                img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
                    pix.height, pix.width, pix.n
                )
                
                # Convert RGBA to RGB if necessary
                if pix.n == 4:
                    img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
                
                images.append(img)
            
            pdf_document.close()
            return images
        except Exception as e:
            logger.error(f"Error converting PDF to images: {str(e)}")
            return []
    
    def extract_text_from_image(self, image_path: str) -> Tuple[str, float]:
        """
        Extract text from image using PaddleOCR
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Tuple of (extracted_text, confidence_score)
        """
        try:
            # Preprocess image
            preprocessed = self.preprocess_image(image_path)
            
            # Use preprocessed image if available, otherwise use original
            input_image = preprocessed if preprocessed is not None else image_path
            
            # Perform OCR
            result = self.ocr.ocr(input_image, cls=True)
            
            if not result or not result[0]:
                return "", 0.0
            
            # Extract text and confidence scores
            extracted_lines = []
            confidence_scores = []
            
            for line in result[0]:
                text = line[1][0]
                confidence = line[1][1]
                extracted_lines.append(text)
                confidence_scores.append(confidence)
            
            # Combine all text with newlines
            full_text = "\n".join(extracted_lines)
            
            # Calculate average confidence
            avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
            
            return full_text, avg_confidence
            
        except Exception as e:
            logger.error(f"Error extracting text from image: {str(e)}")
            return "", 0.0
    
    def extract_text_from_pdf(self, pdf_path: str) -> Tuple[str, float]:
        """
        Extract text from PDF file
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Tuple of (extracted_text, average_confidence)
        """
        try:
            # First try to extract text directly from PDF (for digital PDFs)
            pdf_document = fitz.open(pdf_path)
            direct_text = ""
            
            for page in pdf_document:
                direct_text += page.get_text()
            
            pdf_document.close()
            
            # If we got substantial text directly, use it
            if len(direct_text.strip()) > 100:
                logger.info("Extracted text directly from PDF")
                return direct_text, 1.0
            
            # Otherwise, convert to images and use OCR
            logger.info("Converting PDF to images for OCR")
            images = self.pdf_to_images(pdf_path)
            
            if not images:
                return "", 0.0
            
            all_text = []
            all_confidences = []
            
            for idx, img in enumerate(images):
                # Save image temporarily
                temp_img_path = f"temp_page_{idx}.png"
                cv2.imwrite(temp_img_path, img)
                
                # Extract text
                text, confidence = self.extract_text_from_image(temp_img_path)
                all_text.append(f"--- Page {idx + 1} ---\n{text}")
                all_confidences.append(confidence)
                
                # Clean up temp file
                if os.path.exists(temp_img_path):
                    os.remove(temp_img_path)
            
            full_text = "\n\n".join(all_text)
            avg_confidence = sum(all_confidences) / len(all_confidences) if all_confidences else 0.0
            
            return full_text, avg_confidence
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            return "", 0.0
    
    def extract_text(self, file_path: str, file_type: str) -> Tuple[str, float]:
        """
        Main method to extract text from any supported file type
        
        Args:
            file_path: Path to the file
            file_type: Type of file (pdf, jpg, png, etc.)
            
        Returns:
            Tuple of (extracted_text, confidence_score)
        """
        try:
            file_type = file_type.lower()
            
            if file_type == 'pdf':
                return self.extract_text_from_pdf(file_path)
            elif file_type in ['jpg', 'jpeg', 'png', 'bmp', 'tiff']:
                return self.extract_text_from_image(file_path)
            else:
                logger.error(f"Unsupported file type: {file_type}")
                return "", 0.0
                
        except Exception as e:
            logger.error(f"Error in extract_text: {str(e)}")
            return "", 0.0
