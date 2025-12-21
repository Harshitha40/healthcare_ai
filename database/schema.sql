-- Healthcare AI System Database Schema
-- PostgreSQL Database Setup

-- Create database (run this separately if needed)
-- CREATE DATABASE healthcare_ai;

-- Connect to the database
\c healthcare_ai;

-- Create patients table
CREATE TABLE IF NOT EXISTS patients (
    patient_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(200),
    age VARCHAR(10),
    gender VARCHAR(20),
    contact VARCHAR(100),
    medical_history TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create visits table
CREATE TABLE IF NOT EXISTS visits (
    visit_id VARCHAR(50) PRIMARY KEY,
    patient_id VARCHAR(50) NOT NULL,
    visit_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    visit_type VARCHAR(100),
    status VARCHAR(50) DEFAULT 'pending',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
);

-- Create raw_documents table
CREATE TABLE IF NOT EXISTS raw_documents (
    document_id VARCHAR(50) PRIMARY KEY,
    visit_id VARCHAR(50) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    file_size INTEGER,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (visit_id) REFERENCES visits(visit_id) ON DELETE CASCADE
);

-- Create ocr_texts table
CREATE TABLE IF NOT EXISTS ocr_texts (
    ocr_id VARCHAR(50) PRIMARY KEY,
    visit_id VARCHAR(50) NOT NULL,
    raw_text TEXT NOT NULL,
    confidence_score VARCHAR(10),
    processing_time VARCHAR(20),
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (visit_id) REFERENCES visits(visit_id) ON DELETE CASCADE
);

-- Create cleaned_texts table
CREATE TABLE IF NOT EXISTS cleaned_texts (
    cleaned_id VARCHAR(50) PRIMARY KEY,
    visit_id VARCHAR(50) NOT NULL,
    cleaned_text TEXT NOT NULL,
    extracted_data JSONB,
    processing_time VARCHAR(20),
    cleaned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (visit_id) REFERENCES visits(visit_id) ON DELETE CASCADE
);

-- Create summaries table
CREATE TABLE IF NOT EXISTS summaries (
    summary_id VARCHAR(50) PRIMARY KEY,
    visit_id VARCHAR(50) NOT NULL,
    summary_text TEXT NOT NULL,
    key_findings TEXT,
    generated_by VARCHAR(100) DEFAULT 'Groq LLM',
    processing_time VARCHAR(20),
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (visit_id) REFERENCES visits(visit_id) ON DELETE CASCADE
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_visits_patient_id ON visits(patient_id);
CREATE INDEX IF NOT EXISTS idx_visits_status ON visits(status);
CREATE INDEX IF NOT EXISTS idx_documents_visit_id ON raw_documents(visit_id);
CREATE INDEX IF NOT EXISTS idx_ocr_texts_visit_id ON ocr_texts(visit_id);
CREATE INDEX IF NOT EXISTS idx_cleaned_texts_visit_id ON cleaned_texts(visit_id);
CREATE INDEX IF NOT EXISTS idx_summaries_visit_id ON summaries(visit_id);

-- Grant permissions (adjust username as needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_username;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_username;
