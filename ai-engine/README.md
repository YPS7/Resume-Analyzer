# AI Resume Analyzer

A sophisticated Resume Analysis Engine leveraging Hybrid AI to evaluate candidate suitability against job descriptions.

## 🧠 AI Engine
The core of this project is a **Hybrid Intelligence System** that combines deterministic rule-based logic with probabilistic LLM reasoning.

### Architecture
The engine operates on a multi-stage pipeline designed to mimic human recruiter intuition while maintaining machine precision.

1.  **Ingestion Layer**:
    -   Extracts clean text from PDF resumes using `pypdf`.
    -   Normalizes text (acronym expansion, removal of stop concepts).

2.  **Semantic Processing (The "Gut Feeling")**:
    -   **Model**: `all-MiniLM-L6-v2` (SentenceTransformer).
    -   Converts the Job Description (JD) and Resume into high-dimensional vector embeddings.
    -   Calculates a **Cosine Similarity Score** to measure conceptual alignment.

3.  **Entity-Driven Audit (The "Checklist")**:
    -   **NER Engine**: Spacy + Custom Matcher patterns.
    -   Extracts Technical Skills, Tools, and Frameworks from the JD.
    -   Performs a "Smart Search" on the resume:
        -   *Exact Match*: Direct keyword hits.
        -   *Semantic Match*: Using vector distance to validate synonyms (e.g., "Postgres" ≈ "SQL").
        -   *Proficiency Check*: Penalizes "weak" context words (e.g., "watched tutorial on X").

4.  **Dealbreaker Logic**:
    -   Hard filters for critical blockers (e.g., Citizenship requiremenst, Security Clearance).

5.  **LLM Verification Layer (The "Second Opinion")**:
    -   **Model**: Mistral / OpenAI via OpenRouter.
    -   If the deterministic layer marks a skill as "Missing", the LLM is called to read the resume deeply.
    -   It looks for "implied" experience (e.g., "Used Pandas/NumPy" → Implies "Python").
    -   Recovers "False Negatives" and adjusts the final score.

6.  **Scoring & Reporting**:
    -   Synthesizes a final weighted score: `(Semantic * 0.3) + (Rules * 0.7)`.
    -   Generates a Senior Recruiter Persona Executive Summary explaining *why* the candidate fits or fails.

## 🖥️ Backend
*[Coming Soon]*

## 🎨 Frontend
*[Coming Soon]*
