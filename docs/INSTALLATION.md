# Installation Guide

This guide walks you through setting up the InternMatch project for local development from scratch. If you prefer to run the project using Docker without installing local dependencies, please refer to the Docker instructions in the [Running Guide](RUNNING.md).

## Prerequisites
Before you begin, ensure you have the following installed on your machine:
- **Git**: To clone the repository.
- **Java 17 (JDK)**: Required for the Spring Boot backend.
- **Node.js (v18+) & npm**: Required for the React frontend.
- **Python (v3.10 - v3.12)**: Required for the FastAPI AI Service.
- **MySQL (v8.0+)**: For the database.

---

## 1. Clone the Repository
Clone the repository to your local machine and enter the directory:
```bash
git clone https://github.com/YOUR_USERNAME/internship-recommendation-engine.git
cd internship-recommendation-engine
```

## 2. Environment Configuration
The project uses environment variables for configuration. A template file is provided.
1. Copy the template:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and verify the values. For a standard local MySQL installation (port 3306), the defaults should work, but ensure the `DB_USERNAME` and `DB_PASSWORD` match your local MySQL root credentials.

## 3. Database Creation & Seeding
You need to create the database schema and populate it with the baseline internship data.

1. Open your MySQL CLI or preferred database client (e.g., MySQL Workbench).
2. Log in as root:
   ```bash
   mysql -u root -p
   ```
3. Execute the following commands to create the database, import the tables, and seed the data:
   ```sql
   CREATE DATABASE internship_recommendation_engine;
   USE internship_recommendation_engine;
   
   -- Source the schema script
   SOURCE database/schema.sql;
   
   -- Source the seed script
   SOURCE database/seed_data.sql;
   
   EXIT;
   ```
*Note: Depending on your terminal, you may need to provide the absolute path to `database/schema.sql` if `SOURCE` fails.*

## 4. Python Environment Setup (AI Service)
The AI Service uses spaCy, Sentence-Transformers, and FastAPI.

1. Navigate to the AI service directory:
   ```bash
   cd ai-service
   ```
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
3. Activate the virtual environment:
   - **Windows:** `.venv\Scripts\activate`
   - **macOS/Linux:** `source .venv/bin/activate`
4. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Download the necessary spaCy NLP model:
   ```bash
   python -m spacy download en_core_web_sm
   ```
6. Return to the root directory:
   ```bash
   cd ..
   ```

## 5. Frontend Setup (React)
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install the Node modules:
   ```bash
   npm install
   ```
3. Return to the root directory:
   ```bash
   cd ..
   ```

## 6. Backend Setup (Spring Boot)
The Spring Boot backend uses Maven wrapper, meaning you do not need to install Maven globally. The dependencies will be automatically downloaded the first time you run the application.

---

### Next Steps
You have successfully installed the project dependencies and set up the database! Proceed to the **[Running Guide](RUNNING.md)** to learn how to start the servers.
