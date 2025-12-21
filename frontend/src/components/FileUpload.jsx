import React, { useState } from 'react';
import '../styles/FileUpload.css';

const FileUpload = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [patientName, setPatientName] = useState('');
  const [patientAge, setPatientAge] = useState('');
  const [patientGender, setPatientGender] = useState('');
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      const validTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
      if (validTypes.includes(selectedFile.type)) {
        setFile(selectedFile);
        setError(null);
      } else {
        setError('Please upload a PDF or image file (JPG, PNG)');
        setFile(null);
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!file) {
      setError('Please select a file');
      return;
    }

    setUploading(true);
    setError(null);

    try {
      const { uploadDocument } = await import('../services/api');
      const result = await uploadDocument(file, {
        name: patientName,
        age: patientAge,
        gender: patientGender,
      });

      onUploadSuccess(result);
      
      // Reset form
      setFile(null);
      setPatientName('');
      setPatientAge('');
      setPatientGender('');
      e.target.reset();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to upload file');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="file-upload-container">
      <div className="upload-card">
        <h2>Upload Medical Record</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Patient Name (Optional)</label>
            <input
              type="text"
              value={patientName}
              onChange={(e) => setPatientName(e.target.value)}
              placeholder="Enter patient name"
              className="form-input"
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Age (Optional)</label>
              <input
                type="text"
                value={patientAge}
                onChange={(e) => setPatientAge(e.target.value)}
                placeholder="Age"
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label>Gender (Optional)</label>
              <select
                value={patientGender}
                onChange={(e) => setPatientGender(e.target.value)}
                className="form-input"
              >
                <option value="">Select</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>
          </div>

          <div className="form-group">
            <label>Medical Document *</label>
            <div className="file-input-wrapper">
              <input
                type="file"
                onChange={handleFileChange}
                accept=".pdf,.jpg,.jpeg,.png"
                className="file-input"
                required
              />
              <div className="file-info">
                {file ? (
                  <span className="file-name">📄 {file.name}</span>
                ) : (
                  <span className="file-placeholder">Choose PDF or Image file</span>
                )}
              </div>
            </div>
          </div>

          {error && <div className="error-message">{error}</div>}

          <button
            type="submit"
            className="submit-button"
            disabled={uploading}
          >
            {uploading ? 'Uploading...' : 'Upload & Process'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default FileUpload;
