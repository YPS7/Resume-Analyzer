# Backend Project Structure Guide

This document provides a detailed breakdown of your **Spring Boot Backend** project structure.

## 📂 Root Directory (`backend/`)

- **`pom.xml`**: The **Project Object Model**. This is the heart of your Maven project.
    - **Purpose**: It defines your project's identity (Group ID, Artifact ID), version, and **dependencies** (libraries like Spring Web, Spring Data JPA, Lombok, PostgreSQL Driver).
    - **Usage**: You edit this file to add new libraries or change the Java version.

- **`README.md`**: Project documentation file containing setup and run instructions.

## 📂 Source Code (`src/main/java/`)

All your Java code lives here, under the package `com.yashresumeanalyzer.resumebackend`.

### 1. `ResumeBackendApplication.java`
- **Location**: Root of the package.
- **Purpose**: The **Entry Point**. This class contains the `main` method that starts the Spring Boot application.
- **Annotation**: `@SpringBootApplication` tells Spring to scan this package (and sub-packages) for components to load.

### 2. `config/`
- **Purpose**: Configuration classes.
- **Usage**: Place global configurations here, such as `SecurityConfig` (for JWT/Auth), `CorsConfig` (to allow frontend access), or `SwaggerConfig` (for API documentation).

### 3. `controller/`
- **Purpose**: The **API Layer** (REST Controllers).
- **Usage**: Classes here handle incoming HTTP requests (GET, POST, PUT, DELETE) from the frontend.
- **Example**: `ResumeController` would have endpoints like `@PostMapping("/upload")` to receive resume files. They talk to the **Service** layer.

### 4. `service/`
- **Purpose**: The **Business Logic Layer**.
- **Usage**: This is where the actual work happens. Controllers call methods here.
- **Example**: `ResumeService` would verify if a resume is valid, parse it, and then ask the **Repository** to save it.

### 5. `repository/`
- **Purpose**: The **Data Access Layer** (DAO).
- **Usage**: Interfaces that extend `JpaRepository`. They provide methods to talk to the database (SQL) without writing SQL.
- **Your Files**:
    - `ResumeRepository.java`: Custom SQL methods for `Resume` table (e.g., `findByChecksum`).
    - `JobDescriptionRepository.java`: For `JobDescription` table.
    - `MatchResultRepository.java`: For `MatchResult` table.

### 6. `entity/`
- **Purpose**: The **Data Models** (Database Tables).
- **Usage**: Plain Java classes annotated with `@Entity`. Each class maps directly to a database table.
- **Example**: Not yet created, but expected to have `Resume.java`, `JobDescription.java`, etc.

### 7. `dto/`
- **Purpose**: **Data Transfer Objects**.
- **Usage**: Simple classes used to pass data between the client (frontend) and the server, avoiding exposing your direct Database Entities.
- **Example**: `ResumeUploadRequest`, `AnalysisResponse`.

## 📂 Resources (`src/main/resources/`)

- **`application.yml`**: The **Application Configuration**.
    - **Purpose**: Controls settings like Database URL (`jdbc:postgresql://...`), Server Port (`8080`), and Logging.
    - **Usage**: Edit this to change environments (e.g., switch from LocalDB to EC2 DB).
