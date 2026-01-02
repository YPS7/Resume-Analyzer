"use client";

import { useState } from "react";
import axios from "axios";
import { Loader2, ArrowRight } from "lucide-react";
import ResumeUpload from "@/components/ResumeUpload";
import JobDescriptionInput from "@/components/JobDescriptionInput";
import AnalysisResult from "@/components/AnalysisResult";

export default function Home() {
  const [step, setStep] = useState(1); // 1: Resume, 2: JD, 3: Result
  const [resumeId, setResumeId] = useState(null);
  const [jdId, setJdId] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Helper to generate simple checksum/ID
  const generateChecksum = (str) => {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      hash = (hash << 5) - hash + str.charCodeAt(i);
      hash |= 0;
    }
    return "chk_" + Math.abs(hash);
  };

  const handleResumeUpload = async (text) => {
    setLoading(true);
    setError(null);
    try {
      const payload = {
        contentText: text,
        sourceType: "TEXT",
        checksum: generateChecksum(text)
      };

      const response = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/resumes`, payload);
      setResumeId(response.data.id);
      setStep(2);
    } catch (err) {
      console.error(err);
      setError("Failed to upload resume. Please ensure backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const handleJDUpload = async ({ title, text }) => {
    setLoading(true);
    setError(null);
    try {
      const payload = {
        title: title,
        contentText: text,
        checksum: generateChecksum(text)
      };

      const response = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/job-descriptions`, payload);
      setJdId(response.data.id);

      // Immediately trigger analysis after JD upload
      await analyze(resumeId, response.data.id);
    } catch (err) {
      console.error(err);
      setError("Failed to upload job description.");
      setLoading(false);
    }
  };

  const analyze = async (rId, jId) => {
    // setLoading is already true from handleJDUpload
    try {
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/api/analyze?resumeId=${rId}&jdId=${jId}`
      );
      setResult(response.data);
      setStep(3);
    } catch (err) {
      console.error(err);
      setError("Analysis failed. The AI engine might be busy or unreachable.");
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setStep(1);
    setResumeId(null);
    setJdId(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="container main-container">
      <div className="hero-section">
        <h1>AI Resume Analyzer</h1>
        <p className="subtitle">
          Optimize your resume for any job description using our advanced AI scoring engine.
        </p>
      </div>

      <div className="content-area">
        {loading && (
          <div className="loading-overlay">
            <Loader2 className="animate-spin" size={48} color="var(--primary-color)" />
            <p>Processing with AI...</p>
          </div>
        )}

        {error && (
          <div className="error-banner">
            {error}
          </div>
        )}

        {step === 1 && (
          <div className="step-container fade-in">
            <ResumeUpload onUpload={handleResumeUpload} />
          </div>
        )}

        {step === 2 && (
          <div className="step-container fade-in">
            <JobDescriptionInput onUpload={handleJDUpload} />
          </div>
        )}

        {step === 3 && result && (
          <div className="step-container fade-in">
            <AnalysisResult result={result} />
            <div className="actions">
              <button onClick={reset} className="btn btn-secondary">
                Analyze Another
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Progress Indicators */}
      <div className="progress-steps">
        <div className={`step-dot ${step >= 1 ? 'active' : ''}`}>1</div>
        <div className="step-line"></div>
        <div className={`step-dot ${step >= 2 ? 'active' : ''}`}>2</div>
        <div className="step-line"></div>
        <div className={`step-dot ${step >= 3 ? 'active' : ''}`}>3</div>
      </div>

      <style jsx>{`
        .main-container {
          padding-top: 3rem;
          padding-bottom: 5rem;
          max-width: 800px;
        }

        .hero-section {
          text-align: center;
          margin-bottom: 3rem;
        }

        h1 {
          font-size: 4rem;
          margin-bottom: 1rem;
          color: var(--text-primary);
          font-family: 'Playfair Display', serif;
          font-weight: 400;
          letter-spacing: -0.02em;
        }

        .subtitle {
          color: var(--text-secondary);
          font-size: 1.15rem;
          font-weight: 400;
          max-width: 600px;
          margin: 0 auto;
        }

        .content-area {
          position: relative;
          min-height: 400px;
        }

        .step-container {
          animation: fadeIn 0.4s ease-out;
        }

        .loading-overlay {
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(255, 255, 255, 0.9);
          backdrop-filter: blur(4px);
          z-index: 10;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          gap: 1rem;
          border-radius: var(--radius-lg);
        }

        .error-banner {
          background-color: #fef2f2;
          color: var(--accent-error);
          padding: 1rem;
          border-radius: var(--radius-md);
          margin-bottom: 1.5rem;
          border: 1px solid #fecaca;
        }

        .actions {
          margin-top: 2rem;
          display: flex;
          justify-content: center;
        }

        .progress-steps {
          display: flex;
          align-items: center;
          justify-content: center;
          margin-top: 4rem;
          opacity: 0.5;
        }

        .step-dot {
          width: 32px;
          height: 32px;
          border-radius: 50%;
          background-color: var(--border-color);
          color: var(--text-secondary);
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: 600;
          font-size: 0.9rem;
          transition: all 0.3s;
        }

        .step-dot.active {
          background-color: var(--primary-color);
          color: white;
        }

        .step-line {
          width: 60px;
          height: 2px;
          background-color: var(--border-color);
          margin: 0 0.5rem;
        }

        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }

        .animate-spin {
          animation: spin 1s linear infinite;
        }

        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}
