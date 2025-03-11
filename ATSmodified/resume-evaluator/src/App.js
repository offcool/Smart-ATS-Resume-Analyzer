import React, { useState } from 'react';
import './App.css';
import logo from './logo.png'; // Ensure your logo is in the src folder

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
    const formData = new FormData();
    formData.append('resume', resumeFile);
    formData.append('job_description', jobDescription);

    const response = await fetch('/api/analyze', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} alt="Logo" className="logo" />
        <h1>Smart ATS - Resume Evaluator</h1>
        <p>🚀 Optimize your resume for Applicant Tracking Systems (ATS) & boost your job search success!</p>
      </header>
      <div className="form-container">
        <form onSubmit={handleSubmit}>
          <textarea
            placeholder="📌 Paste the Job Description Below"
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            rows="5"
            className="textarea"
          />
          <input type="file" accept="application/pdf" onChange={handleFileChange} className="file-input" />
          <button type="submit" className="submit-button">✨ Analyze Resume</button>
        </form>
      </div>
      {loading && <p className="loading">🔍 Analyzing Resume...</p>}
      {result && (
        <div className="result-container">
          <h2>ATS Evaluation Results</h2>
          <p>Your resume matches: <strong>{result['JD Match']}</strong></p>
          <h3>❌ Missing Keywords</h3>
          <ul>
            {result['MissingKeywords'].map((keyword, index) => (
              <li key={index}>{keyword}</li>
            ))}
          </ul>
          <h3>📄 Profile Summary</h3>
          <p>{result['Profile Summary']}</p>
        </div>
      )}
    </div>
  );
}

export default App;