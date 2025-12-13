import React, { useState } from 'react';
import { cvService } from '../services/api';
import './CVUpload.css';

const CVUpload = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [dragActive, setDragActive] = useState(false);

  const handleFileChange = (e) => {
    setError('');
    const selectedFile = e.target.files[0];
    validateAndSetFile(selectedFile);
  };

  const validateAndSetFile = (selectedFile) => {
    if (selectedFile) {
      const validTypes = ['application/pdf', 'application/msword', 
                         'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                         'text/plain'];
      
      if (!validTypes.includes(selectedFile.type)) {
        setError('Please upload a PDF, DOC, DOCX, or TXT file');
        return;
      }
      
      if (selectedFile.size > 16 * 1024 * 1024) {
        setError('File size must be less than 16MB');
        return;
      }
      
      setFile(selectedFile);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    setError('');
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    setUploading(true);
    setError('');

    try {
      const result = await cvService.uploadCV(file);
      onUploadSuccess(result);
      setFile(null);
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="cv-upload">
      <div 
        className={`upload-area ${dragActive ? 'drag-active' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          type="file"
          id="cv-file"
          accept=".pdf,.doc,.docx,.txt"
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />
        
        <label htmlFor="cv-file" className="upload-label">
          <div className="upload-icon">📄</div>
          <p className="upload-text">
            {file ? file.name : 'Drag and drop your CV here or click to browse'}
          </p>
          <p className="upload-hint">Supports PDF, DOC, DOCX, TXT (Max 16MB)</p>
        </label>
      </div>

      {error && <div className="error-message">{error}</div>}

      {file && (
        <button 
          onClick={handleUpload} 
          className="btn-primary upload-btn"
          disabled={uploading}
        >
          {uploading ? 'Analyzing and matching...' : 'Upload and Find Matches'}
        </button>
      )}
    </div>
  );
};

export default CVUpload;
