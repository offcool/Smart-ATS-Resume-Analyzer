// App.js - Updated for PDF File Upload with FormData

import React, { useState } from 'react';
import './App.css';
import logo from './logo.png';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch, faFileAlt, faCheckCircle, faTimesCircle, faUpload, faCopyright } from '@fortawesome/free-solid-svg-icons';

function App() {
  const [jobDescription, setJobDescription] = useState('');
  const [resumeFile, setResumeFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setResumeFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!resumeFile || !jobDescription) {
      alert("⚠️ Please upload a resume and enter the job description.");
      return;
    }

    setLoading(true);
    setResult(null);

    const formData = new FormData(); // Create FormData object
    formData.append('resume', resumeFile); // Append the file with key 'resume'
    formData.append('job_description', jobDescription); // Append job description text

    try {
      const response = await fetch('http://127.0.0.1:5000/api/analyze', {
        method: 'POST',
        body: formData, // Send FormData as the body
        // Remove Content-Type header - browser sets it automatically for FormData
      });

      if (!response.ok) {
        const errorData = await response.json(); // Try to get error details from JSON response
        let errorMessage = `HTTP error! status: ${response.status}`;
        if (errorData && errorData.error) {
          errorMessage += ` - Backend Error: ${errorData.error}`; // Append backend error if available
        }
        throw new Error(errorMessage);
      }

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Error during analysis:", error);
      console.log("Fetch error object:", error);
      setResult({
        'JD Match': 'Error',
        'MissingKeywords': [error.message || 'An error occurred during analysis. Please try again.'], // Use error.message if available
        'Profile Summary': 'Failed to retrieve analysis results.',
      });
      alert(`⚠️ Analysis failed. ${error.message || 'Please check the backend and try again.'}`); // Show detailed error in alert
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} alt="Logo" className="logo" />
        <h1>Smart ATS - Resume Evaluator</h1>
        <p>Unlock your career potential with AI-driven resume optimization.  Get tailored insights to conquer Applicant Tracking Systems and land your dream job.</p>
      </header>
      <div className="form-container">
        <form onSubmit={handleSubmit}>
          <textarea
            placeholder="📝 Paste the Job Description Here. The more detailed, the better the analysis."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            rows="8"
            className="textarea"
          />
          <label htmlFor="resumeUpload" className="file-input-label">
            <FontAwesomeIcon icon={faUpload}  />
            <span>
              {resumeFile ? 'File Uploaded:' : 'Upload Your Resume (PDF)'}
              {resumeFile ? <span className="file-name">{resumeFile.name}</span> : <span>(PDF format)</span>}
            </span>

          </label>
          <input
            id="resumeUpload"
            type="file"
            accept="application/pdf"
            onChange={handleFileChange}
            className="file-input"
          />
          <button type="submit" className="submit-button">
            <FontAwesomeIcon icon={faSearch} style={{ marginRight: '8px' }} /> Analyze My Resume ✨
          </button>
        </form>
      </div>
      {loading && <p className="loading"><FontAwesomeIcon icon={faSearch} spin style={{ marginRight: '8px' }} /> Smartly Analyzing Your Resume...</p>}
      {result && result['JD Match'] !== 'Error' && (
        <div className="result-container">
          <h2><FontAwesomeIcon icon={faCheckCircle} style={{ marginRight: '10px', color: '#2ecc71' }} /> ATS Evaluation Insights</h2>
          <p><strong>Job Description Match Score:</strong>  {result['JD Match']}</p>
          <h3><FontAwesomeIcon icon={faTimesCircle} style={{ marginRight: '10px', color: '#e74c3c' }} /> Key Improvement Areas</h3>
          {result['MissingKeywords'] && result['MissingKeywords'].length > 0 ? (
            <ul>
              {result['MissingKeywords'].map((keyword, index) => (
                <li key={index}>{keyword}</li>
              ))}
            </ul>
          ) : (
            <p>Excellent! Your resume keywords are strongly aligned with the job description.</p>
          )}
          <h3><FontAwesomeIcon icon={faFileAlt} style={{ marginRight: '10px', color: '#3498db' }} /> Professional Summary Highlights</h3>
          <p>{result['Profile Summary'] || 'Analyzing profile summary...'}</p>
        </div>
      )}
      {result && result['JD Match'] === 'Error' && (
        <div className="result-container error-result">
          <h2><FontAwesomeIcon icon={faTimesCircle} style={{ marginRight: '10px', color: '#e74c3c' }} /> Analysis Error Encountered</h2>
          <p className="error-message">
            Oops! Something went wrong during the analysis. Please double-check your inputs and try again.
          </p>
          <p className="error-details">
            {result['MissingKeywords'] && result['MissingKeywords'].length > 0 ? result['MissingKeywords'][0] : 'If issue persists, contact support.'}
          </p>
        </div>
      )}

      <footer className="app-footer">
        <FontAwesomeIcon icon={faCopyright} className="copyright-icon" /> Sherpa Engineering MENA 2025
      </footer>
    </div>
  );
}

export default App;