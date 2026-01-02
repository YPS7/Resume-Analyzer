# AI Resume Analyzer

A sophisticated Resume Analysis Engine leveraging Hybrid AI to evaluate candidate suitability against job descriptions. This system mimics a human recruiter's intuition while maintaining machine precision, packaged in a premium, modern web application.

---

# 🏗️ System Architecture

The system is designed as a **Microservices-based architecture**, where distinct components handle specific responsibilities (UI, Orchestration, Intelligence, Persistence).

## 🧩 Sub-Architectures

### 1. The Frontend Architecture (Client Layer)
**Tech Stack:** Next.js 14, React, CSS Modules (Earthy Premium Theme), `pdfjs-dist`.

*   **Role**: Provides the user interface for uploading documents and viewing results.
*   **Key Components**:
    *   **`FileParser`**: a client-side utility that extracts raw text from PDF/TXT/MD files directly in the browser using a Web Worker. This ensures document privacy and reduces server load.
    *   **`Orchestrator` (`page.js`)**: Manages the multi-step state (Upload -> Input -> Analyze) and handles API communication.
    *   **`Visualizer` (`AnalysisResult`)**: Renders complex JSON AI outputs into rich, readable formats (Score Rings, Markdown Summaries, Dealbreaker Badges).

### 2. The Backend Architecture (Orchestration Layer)
**Tech Stack:** Java Spring Boot 3, Hibernate (JPA), RestTemplate, Lombok.

*   **Role**: The central nervous system that orchestrates data flow between the User, Database, and AI Brain.
*   **Core Modules**:
    *   **`ResumeController` / `JobDescriptionController`**: REST Endpoints that handle data ingestion and validation.
    *   **`AnalysisService`**: The logic hub. It:
        1.  Retrieves entities from the DB.
        2.  Formats payloads for the AI Engine.
        3.  Parses the AI response.
        4.  Transactional saves of the final `MatchResult`.
    *   **Security**: Manages connection secrets (via Environment Variables) for secure database access.

### 3. The Intelligence Architecture (AI Engine)
**Tech Stack:** Python, FastAPI, PyTorch (SentenceTransformers), Spacy, LLM Integration (Mistral/OpenAI).

*   **Role**: The "Brain" that performs the cognitive analysis.
*   **Pipeline**:
    1.  **Semantic Processing**: Converts text to vectors (`all-MiniLM-L6-v2`) for conceptual matching.
    2.  **Entity Audit**: Extracts strict skills using Named Entity Recognition (NER).
    3.  **LLM Verification**: A probabilistic "Second Opinion" layer that resolves ambiguities (e.g., inferring "Python" knowledge from "Pandas usage").
    *   *Hosted independently on an AWS EC2 instance.*

### 4. The Cloud & Persistence Architecture
**Tech Stack:** Supabase (PostgreSQL), AWS EC2.

*   **Role**: Durable storage and reliable hosting.
*   **Supabase (Managed PostgreSQL)**: 
    *   Stores `Resume` text, `JobDescription` text, and structured `AnalysisResults`.
    *   Accessed via JDBC over SSL.
*   **AWS EC2**:
    *   Hosts the resource-heavy Python AI Engine API, exposing it via HTTP for the Spring Boot backend to consume.

---

## 🔗 Complete Combined Architecture

The following flow illustrates how these sub-architectures combine to deliver the final result:

```mermaid
graph TD
    User[👤 User] -->|1. Uploads PDF| FE[🖥️ Frontend (Next.js)]
    FE -->|2. Extracts Text (Client-Side)| FE
    FE -->|3. POST /api/analyze| BE[⚙️ Backend (Spring Boot)]
    
    subgraph Data Flow
        BE -->|4. Save Content| DB[(🗄️ Supabase Postgres)]
        BE -->|5. Request Analysis| AI[🧠 AI Engine (EC2)]
        AI -->|6. Semantic + LLM Scoring| AI
        AI -->|7. Return JSON Result| BE
        BE -->|8. Save Result| DB
    end
    
    BE -->|9. Return DTO| FE
    FE -->|10. Render UI| User
```

1.  **Ingestion**: User uploads a file. The **Frontend** strips the text.
2.  **Submission**: Frontend sends text to the **Backend**.
3.  **Persistence**: Backend saves the raw data to **Supabase**.
4.  **Intelligence**: Backend calls the **AI Engine** with the resume and JD text.
5.  **Processing**: AI Engine runs its 3-stage pipeline (Vector -> NER -> LLM) and returns a score.
6.  **Delivery**: Backend saves the score and returns it to the Frontend for display.

---

# ☁️ Cloud & Supabase Integration Flow

This project uses a **Hybrid Cloud** approach:

### Database: Supabase (PostgreSQL)
*   **Connection**: The Spring Boot Application connects to Supabase using the standard PostgreSQL JDBC Driver.
*   **Security**: 
    *   Connection strings are externalized in `.env` files (e.g., `DB_URL`, `DB_PASSWORD`).
    *   SSL Mode (`?sslmode=require`) is enforced to ensure encrypted transit over the public internet.
*   **Schema Validation**: Hibernate (`ddl-auto: validate`) checks the schema on startup to ensure the Java Entities match the Cloud Database tables perfectly.

### AI Compute: AWS EC2
*   The AI Engine is containerized and running on a remote EC2 instance.
*   The Java Backend communicates with it via standard HTTP REST calls (`RestTemplate`).
*   This decouples the heavy ML processing from the lightweight Java web server.

---

# 🚀 Getting Started

## Frontend
```bash
cd frontend
# Install dependencies (including pdfjs-dist, react-markdown)
npm install 
# Run Development Server
npm run dev
```
*Access at `http://localhost:3000`*

## Backend
```bash
cd backend
# Run Spring Boot App
./mvnw spring-boot:run
```
*Server runs on `http://localhost:8080`*
