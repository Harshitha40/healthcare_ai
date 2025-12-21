import React, { useEffect, useState } from 'react';
import '../styles/SummaryView.css';

const SummaryView = ({ visitId, onBack }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('summary');

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const { getSummary } = await import('../services/api');
        const result = await getSummary(visitId);
        setData(result);
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to fetch summary');
      } finally {
        setLoading(false);
      }
    };

    fetchSummary();
  }, [visitId]);

  if (loading) {
    return (
      <div className="summary-view">
        <div className="loading">Loading summary...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="summary-view">
        <div className="error">{error}</div>
        <button onClick={onBack} className="back-button">
          ← Back to Upload
        </button>
      </div>
    );
  }

  return (
    <div className="summary-view">
      <div className="summary-header">
        <button onClick={onBack} className="back-button">
          ← Upload New Record
        </button>
        <div className="header-info">
          <h2>Medical Record Summary</h2>
          <div className="visit-info">
            <span className="badge">Visit ID: {visitId}</span>
            <span className="badge status-badge">{data.status}</span>
          </div>
        </div>
      </div>

      <div className="tabs">
        <button
          className={`tab ${activeTab === 'summary' ? 'active' : ''}`}
          onClick={() => setActiveTab('summary')}
        >
          📋 Summary
        </button>
        <button
          className={`tab ${activeTab === 'comparison' ? 'active' : ''}`}
          onClick={() => setActiveTab('comparison')}
        >
          🔄 Original vs Cleaned
        </button>
        <button
          className={`tab ${activeTab === 'extracted' ? 'active' : ''}`}
          onClick={() => setActiveTab('extracted')}
        >
          📊 Extracted Data
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'summary' && (
          <div className="summary-content">
            <div className="summary-section">
              <h3>Medical Summary</h3>
              <div className="summary-text">
                {data.summary || 'No summary available'}
              </div>
            </div>

            {data.key_findings && (
              <div className="summary-section key-findings">
                <h3>Key Findings</h3>
                <div className="findings-text">
                  {data.key_findings}
                </div>
              </div>
            )}

            {data.extracted_data && (
              <div className="summary-section quick-info">
                <h3>Quick Information</h3>
                <div className="info-grid">
                  {data.extracted_data.patient_name && (
                    <div className="info-item">
                      <span className="label">Patient:</span>
                      <span className="value">{data.extracted_data.patient_name}</span>
                    </div>
                  )}
                  {data.extracted_data.age && (
                    <div className="info-item">
                      <span className="label">Age:</span>
                      <span className="value">{data.extracted_data.age}</span>
                    </div>
                  )}
                  {data.extracted_data.gender && (
                    <div className="info-item">
                      <span className="label">Gender:</span>
                      <span className="value">{data.extracted_data.gender}</span>
                    </div>
                  )}
                  {data.extracted_data.diagnosis && (
                    <div className="info-item">
                      <span className="label">Diagnosis:</span>
                      <span className="value">{data.extracted_data.diagnosis}</span>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'comparison' && (
          <div className="comparison-view">
            <div className="text-panel">
              <h3>Original OCR Text</h3>
              <div className="text-content ocr-text">
                {data.ocr_text || 'No OCR text available'}
              </div>
              {data.ocr_confidence && (
                <div className="confidence">
                  Confidence: {data.ocr_confidence}
                </div>
              )}
            </div>

            <div className="divider"></div>

            <div className="text-panel">
              <h3>Cleaned Text</h3>
              <div className="text-content cleaned-text">
                {data.cleaned_text || 'No cleaned text available'}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'extracted' && (
          <div className="extracted-data">
            {data.extracted_data ? (
              <div className="data-sections">
                {data.extracted_data.symptoms && data.extracted_data.symptoms.length > 0 && (
                  <div className="data-section">
                    <h4>Symptoms</h4>
                    <ul>
                      {data.extracted_data.symptoms.map((symptom, idx) => (
                        <li key={idx}>{symptom}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {data.extracted_data.medications && data.extracted_data.medications.length > 0 && (
                  <div className="data-section">
                    <h4>Medications</h4>
                    <ul>
                      {data.extracted_data.medications.map((med, idx) => (
                        <li key={idx}>{med}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {data.extracted_data.test_results && data.extracted_data.test_results.length > 0 && (
                  <div className="data-section">
                    <h4>Test Results</h4>
                    <ul>
                      {data.extracted_data.test_results.map((test, idx) => (
                        <li key={idx}>{test}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {data.extracted_data.doctor_notes && (
                  <div className="data-section">
                    <h4>Doctor's Notes</h4>
                    <p>{data.extracted_data.doctor_notes}</p>
                  </div>
                )}

                <div className="data-section">
                  <h4>Full Extracted Data (JSON)</h4>
                  <pre className="json-data">
                    {JSON.stringify(data.extracted_data, null, 2)}
                  </pre>
                </div>
              </div>
            ) : (
              <div className="no-data">No extracted data available</div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default SummaryView;
