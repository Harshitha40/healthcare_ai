import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import ProcessingStatus from './components/ProcessingStatus';
import SummaryView from './components/SummaryView';
import './styles/App.css';

function App() {
  const [currentView, setCurrentView] = useState('upload');
  const [visitId, setVisitId] = useState(null);

  const handleUploadSuccess = (result) => {
    setVisitId(result.visit_id);
    setCurrentView('processing');
  };

  const handleProcessingComplete = (visitId) => {
    setCurrentView('summary');
  };

  const handleBackToUpload = () => {
    setCurrentView('upload');
    setVisitId(null);
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>🏥 Healthcare AI System</h1>
          <p className="tagline">Medical Record Processing & Summarization</p>
        </div>
      </header>

      <main className="app-main">
        {currentView === 'upload' && (
          <FileUpload onUploadSuccess={handleUploadSuccess} />
        )}

        {currentView === 'processing' && (
          <ProcessingStatus
            visitId={visitId}
            onComplete={handleProcessingComplete}
          />
        )}

        {currentView === 'summary' && (
          <SummaryView visitId={visitId} onBack={handleBackToUpload} />
        )}
      </main>

      <footer className="app-footer">
        <p>Healthcare AI System v1.0 | Powered by PaddleOCR & Groq LLM</p>
      </footer>
    </div>
  );
}

export default App;
