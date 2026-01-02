"use client";

import Link from "next/link";
import { FileText, Github } from "lucide-react";

export default function Header() {
  return (
    <header className="header">
      <div className="container header-content">
        <Link href="/" className="logo">
          <FileText className="logo-icon" size={24} />
          <span className="logo-text">Resume<span className="text-primary">Analyzer</span></span>
        </Link>

        <nav className="nav">
          <a
            href="https://github.com/YPS7/Resume-Analyzer"
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-secondary nav-item"
          >
            <Github size={18} style={{ marginRight: '8px' }} />
            GitHub
          </a>
        </nav>
      </div>

      <style jsx>{`
        .header {
          background-color: var(--header-bg);
          border-bottom: 1px solid var(--border-color);
          position: sticky;
          top: 0;
          z-index: 100;
          height: 70px;
          display: flex;
          align-items: center;
        }

        .header-content {
          display: flex;
          align-items: center;
          justify-content: space-between;
          width: 100%;
        }

        .logo {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          font-weight: 700;
          font-size: 1.25rem;
          font-family: 'Inter', sans-serif;
          color: var(--text-primary);
        }

        .logo-icon {
          color: var(--text-primary);
        }
      `}</style>
    </header>
  );
}
