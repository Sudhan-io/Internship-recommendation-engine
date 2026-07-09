# Development Artifacts & Tools Inventory

Welcome to the `tools/` directory. This folder contains all the helper scripts, verification utilities, data pipelines, and debugging tools created during Sprints 1–22.

These scripts are intended for development, testing, and diagnostic purposes. 

## Directory Structure

### 1. `dataset/`
Contains scripts used to fetch and load internship data into the database. Note that the core preprocessing logic has been moved to the canonical Dataset Engineering Module located at `ai-service/dataset/scripts/`.

- `download_dataset.py`: Fetches the dataset from the remote source.
- `download_linkedin_dataset.py`: Specifically fetches the LinkedIn job postings dataset.
- `run_database_seed.py` / `seed_clean_internships.py`: Connects to MySQL to insert clean internship records.
- `update_db_schema.py` / `run_schema.py`: Executes DDL scripts or updates table structures.
- `run_import_verification.py`: Verifies that the dataset import succeeded.
- `insert_admin.py` / `insert_admin.sql`: Helper to generate a default admin user.

### 2. `verification/`
Contains End-to-End (E2E) and integration verification scripts. Most of these scripts require the FastAPI and Spring Boot servers to be running.
- `verify_parser.py`: Tests the NLP resume parser independently.
- `verify_normalization.py`: Tests the skill normalization pipeline.
- `verify_embedding.py` / `verify_similarity.py`: Tests the Hugging Face embedding generation and cosine similarity calculation.
- `verify_recommendation.py` / `verify_recommendation_api.py`: Tests the AI recommendation endpoint.
- `verify_recommendations_db.py`: Verifies that generated recommendations are persisted in the MySQL database.
- `verify_frontend_integration.py`: Simulates frontend API calls to ensure CORS and JSON responses are correct.
- `verify_five_recommendations.py`: Comprehensive E2E script simulating 5 synthetic student profiles, uploading resumes, generating AI recommendations, and asserting success.

### 3. `debugging/`
Contains isolated scripts for debugging specific components.
- `verify_debug.py`: General AI pipeline debugging.
- `verify_columns.py` / `test_*_columns.py`: Validates the structure and columns of datasets.
- `list_hf_files.py`: Lists cached Hugging Face models in the `.cache/huggingface` directory.
- `audit_quality.py`: Executes an offline quality audit of the recommendation scoring logic (Semantic, Skill, Education, Experience, Eligibility).
- `inspect_resumes.py`: Lists and inspects uploaded PDF resumes in the backend uploads directory.

### 4. `benchmarking/`
Contains performance tests and output logs.
- `verify_explanation.py`: Checks the latency and quality of AI explanations.
- `five_tests_results.json`: Cached JSON output from `verify_five_recommendations.py`.

## Usage Instructions

1. **Python Environment**: Ensure you activate the virtual environment located in `ai-service/.venv` before running Python scripts.
   ```bash
   cd d:\PROJECTS\Internship-recommendation-engine\ai-service
   .venv\Scripts\activate
   ```
2. **Servers**: For verification scripts that hit the APIs, ensure both servers are running:
   - FastAPI: `.venv\Scripts\python.exe -m uvicorn app:app --port 8000`
   - Spring Boot: `.\mvnw.cmd spring-boot:run`
3. **Execution**: Execute the tools from the `ai-service` directory to ensure Python module paths resolve correctly:
   ```bash
   python ..\tools\verification\verify_five_recommendations.py
   ```
