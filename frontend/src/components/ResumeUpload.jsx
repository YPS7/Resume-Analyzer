"use client";

import { useState, useRef } from "react";
import { Upload, FileText, Loader2 } from "lucide-react";
import { extractTextFromPDF } from "../utils/pdfParser";

export default function ResumeUpload({ onUpload }) {
  const [text, setText] = useState("");
  const [isReading, setIsReading] = useState(false);
  const fileInputRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (text.trim()) {
      onUpload(text);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsReading(true);
    try {
      let content = "";
      if (file.type === "application/pdf") {
        content = await extractTextFromPDF(file);
      } else {
        content = await file.text();
      }
      setText(content);
    } catch (error) {
      console.error("Failed to read file", error);
      alert("Failed to read file. Please try pasting the text instead.");
    } finally {
      setIsReading(false);
    }
  };

  return (
    <div className="card resume-upload-card">
      {/* 
        Made this entire header clickable to serve as the main upload button 
        as per user request.
      */}
      <div
        className="metallic-header clickable"
        onClick={() => fileInputRef.current?.click()}
      >
        <Upload size={20} color="#333" />
        <span>Upload Resume (PDF/TXT)</span>
      </div>

      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileUpload}
        accept=".txt,.md,.json,.pdf"
        style={{ display: 'none' }}
      />

      <form onSubmit={handleSubmit} className="upload-form">
        <div className="input-group">
          <label htmlFor="resume-text">
            {isReading ? (
              <span className="flex-center gap-2">
                <Loader2 className="animate-spin" size={14} />
                Reading file...
              </span>
            ) : "Paste Resume Content"}
          </label>
          <textarea
            id="resume-text"
            placeholder="Paste the resume text here..."
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="text-area"
          />
        </div>

        <button type="submit" className="btn btn-primary full-width">
          Save Resume
        </button>
      </form>

      <style jsx>{`
        .resume-upload-card {
          min-height: 500px;
          display: flex;
          flex-direction: column;
          padding: 2.5rem;
        }

        .metallic-header {
          display: inline-flex;
          align-items: center;
          gap: 0.75rem;
          padding: 1rem 2rem;
          background: var(--metallic-gradient);
          border-radius: var(--radius-md);
          box-shadow: var(--shadow-metallic);
          margin-bottom: 2rem;
          color: #333;
          font-weight: 600;
          font-size: 1.1rem;
          align-self: flex-start;
          border: 1px solid #ccc;
          transition: transform 0.1s, box-shadow 0.1s;
        }

        .clickable {
          cursor: pointer;
        }

        .clickable:active {
          transform: translateY(1px);
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .upload-form {
          flex: 1;
          display: flex;
          flex-direction: column;
        }

        .input-group {
          margin-bottom: 2rem;
          flex: 1;
          display: flex;
          flex-direction: column;
        }

        label {
          display: block;
          margin-bottom: 0.75rem;
          font-weight: 500;
          color: var(--text-secondary);
          font-size: 0.95rem;
        }

        .text-area {
          width: 100%;
          flex: 1;
          padding: 1rem;
          border: 1px solid #d1d5db;
          border-radius: var(--radius-sm);
          font-family: inherit;
          resize: vertical;
          min-height: 250px;
          outline: none;
          transition: border-color 0.2s;
          background-color: #fafafa;
          font-size: 0.95rem;
          color: var(--text-primary);
        }

        .text-area:focus {
          border-color: var(--text-primary);
          background-color: #fff;
        }

        .full-width {
          width: 100%;
          padding: 1rem;
          background-color: #262626; /* Dark charcoal */
          color: white;
          font-size: 1rem;
          border-radius: var(--radius-sm);
          margin-top: auto;
        }
        
        .full-width:hover {
           background-color: #000;
        }

        .gap-2 { gap: 0.5rem; }
      `}</style>
    </div>
  );
}
