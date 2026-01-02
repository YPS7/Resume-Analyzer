# Resume Analyzer Backend

## How to Run
Since you do not have Maven (`mvn`) installed globally, you should run this project using your IDE (VS Code).

1. **Open the Main Class**:
   Navigate to: `src/main/java/com/yashresumeanalyzer/resumebackend/ResumeBackendApplication.java`

2. **Run the Application**:
   - In VS Code, you should see "Run | Debug" buttons just above the `public static void main` line.
   - Click **Run**.

## Database Configuration
**Important**: You currently have `application.yml` configured to connect to `resume_postgres`.
- If you are running this app **locally** (via VS Code), `resume_postgres` will likely **fail** because your computer doesn't know that hostname.
- **Fix**: Change `url` back to `localhost` in `src/main/resources/application.yml` for local testing:
  ```yaml
  url: jdbc:postgresql://localhost:5432/resume_db
  ```
- Ensure your PostgreSQL database is running and accessible on port 5432.
