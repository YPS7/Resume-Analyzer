"use client";

import { AlertCircle } from "lucide-react";
import ReactMarkdown from 'react-markdown';

export default function AnalysisResult({ result }) {
  if (!result) return null;

  // Earthy tones for score
  const getScoreColor = (score) => {
    if (score >= 80) return "#2d2d2d"; // Dark charcoal for high score
    if (score >= 50) return "#854d0e"; // Bronze/Gold for medium
    return "#991b1b"; // Deep red for low
  };

  const scoreColor = getScoreColor(result.score);

  return (
    <div className="card result-card">
      <div className="result-header">
        <div className="score-ring">
          <svg viewBox="0 0 36 36" className="circular-chart">
            <path
              className="circle-bg"
              d="M18 2.0845
                a 15.9155 15.9155 0 0 1 0 31.831
                a 15.9155 15.9155 0 0 1 0 -31.831"
            />
            <path
              className="circle"
              strokeDasharray={`${result.score}, 100`}
              d="M18 2.0845
                a 15.9155 15.9155 0 0 1 0 31.831
                a 15.9155 15.9155 0 0 1 0 -31.831"
              style={{ stroke: scoreColor }}
            />
            <text x="18" y="20.35" className="percentage" style={{ fill: scoreColor }}>
              {result.score}%
            </text>
          </svg>
        </div>

        <div className="verdict-container">
          <h2>{result.verdict}</h2>
          {result.dealbreaker && (
            <div className="badge badge-error">
              <AlertCircle size={14} />
              <span>Dealbreaker Detected</span>
            </div>
          )}
        </div>
      </div>

      <div className="result-body">
        <section className="section">
          <h4>AI Summary</h4>
          <div className="markdown-content">
            <ReactMarkdown>{result.summary}</ReactMarkdown>
          </div>
        </section>

        {result.missingSkills && (
          <section className="section">
            <h4>Missing Skills</h4>
            <div className="skills-list">
              {result.missingSkills.split(',').map((skill, index) => (
                <span key={index} className="skill-tag">
                  {skill.trim()}
                </span>
              ))}
            </div>
          </section>
        )}
      </div>

      <style jsx>{`
        .result-card {
          margin-top: 2rem;
          animation: slideUp 0.5s ease-out;
          padding: 3rem;
        }

        .result-header {
          display: flex;
          align-items: center;
          gap: 3rem;
          margin-bottom: 3rem;
          padding-bottom: 2rem;
          border-bottom: 1px solid #e5e5e5;
        }

        .score-ring {
          width: 120px;
          height: 120px;
          flex-shrink: 0;
        }

        .circular-chart {
          display: block;
          margin: 0 auto;
          max-width: 100%;
          max-height: 100%;
        }

        .circle-bg {
          fill: none;
          stroke: #e6ddd0; /* Light beige ring */
          stroke-width: 2;
        }

        .circle {
          fill: none;
          stroke-width: 2.5;
          stroke-linecap: round;
          animation: progress 1s ease-out forwards;
        }

        .percentage {
          font-family: 'Playfair Display', serif;
          font-weight: bold;
          font-size: 0.5em;
          text-anchor: middle;
        }

        .verdict-container h2 {
          margin: 0;
          font-size: 2.5rem;
          color: var(--text-primary);
          font-family: 'Playfair Display', serif;
        }

        .badge {
          display: inline-flex;
          align-items: center;
          gap: 0.25rem;
          padding: 0.25rem 0.75rem;
          border-radius: 999px;
          font-size: 0.75rem;
          font-weight: 600;
          margin-top: 0.5rem;
        }

        .badge-error {
          background-color: #fef2f2;
          color: #991b1b;
          border: 1px solid #fecaca;
        }

        .section {
          margin-bottom: 2rem;
        }

        .section h4 {
          font-size: 0.9rem;
          text-transform: uppercase;
          letter-spacing: 0.1em;
          color: var(--text-secondary);
          margin-bottom: 1rem;
          font-weight: 600;
        }

        /* Markdown Styling */
        .markdown-content {
          color: var(--text-primary);
          line-height: 1.8;
          font-size: 1.05rem;
        }
        
        .markdown-content :global(p) {
          margin-bottom: 1em;
        }

        .markdown-content :global(strong) {
          color: #1a1a1a;
          font-weight: 600;
        }

        .markdown-content :global(ul) {
          list-style-type: disc;
          padding-left: 1.5em;
          margin-bottom: 1em;
        }

        .markdown-content :global(li) {
          margin-bottom: 0.5em;
        }

        .skills-list {
          display: flex;
          flex-wrap: wrap;
          gap: 0.75rem;
        }

        .skill-tag {
          background-color: #f5f5f4;
          color: var(--text-primary);
          padding: 0.4rem 1rem;
          border-radius: var(--radius-sm);
          font-size: 0.9rem;
          border: 1px solid #e7e5e4;
        }

        @keyframes progress {
          0% { stroke-dasharray: 0 100; }
        }

        @keyframes slideUp {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </div>
  );
}
