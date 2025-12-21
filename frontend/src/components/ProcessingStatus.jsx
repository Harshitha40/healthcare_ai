import React, { useEffect, useState } from 'react';
import '../styles/ProcessingStatus.css';

const ProcessingStatus = ({ visitId, onComplete }) => {
  const [status, setStatus] = useState('Starting...');
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState(null);
  const [currentStep, setCurrentStep] = useState(0);

  const steps = [
    { name: 'OCR Extraction', key: 'ocr' },
    { name: 'Text Cleaning', key: 'clean' },
    { name: 'Summary Generation', key: 'summarize' },
  ];

  useEffect(() => {
    const processDocument = async () => {
      try {
        const { performOCR, cleanText, generateSummary } = await import('../services/api');

        // Step 1: OCR
        setCurrentStep(0);
        setStatus('Extracting text from document...');
        setProgress(33);
        await performOCR(visitId);

        // Step 2: Clean
        setCurrentStep(1);
        setStatus('Cleaning and correcting text...');
        setProgress(66);
        await cleanText(visitId);

        // Step 3: Summarize
        setCurrentStep(2);
        setStatus('Generating medical summary...');
        setProgress(90);
        await generateSummary(visitId);

        setStatus('Complete!');
        setProgress(100);
        
        setTimeout(() => {
          onComplete(visitId);
        }, 500);
      } catch (err) {
        setError(err.response?.data?.detail || 'Processing failed');
        setStatus('Error');
      }
    };

    if (visitId) {
      processDocument();
    }
  }, [visitId, onComplete]);

  return (
    <div className="processing-status">
      <div className="status-card">
        <h3>Processing Medical Record</h3>
        <div className="status-info">
          <p className="status-text">{status}</p>
          {error && <p className="error-text">{error}</p>}
        </div>

        <div className="progress-bar">
          <div
            className="progress-fill"
            style={{ width: `${progress}%` }}
          ></div>
        </div>

        <div className="steps-container">
          {steps.map((step, index) => (
            <div
              key={step.key}
              className={`step ${index < currentStep ? 'completed' : ''} ${
                index === currentStep ? 'active' : ''
              }`}
            >
              <div className="step-indicator">
                {index < currentStep ? '✓' : index + 1}
              </div>
              <div className="step-name">{step.name}</div>
            </div>
          ))}
        </div>

        {!error && progress < 100 && (
          <div className="spinner-container">
            <div className="spinner"></div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProcessingStatus;
