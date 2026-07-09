# Running Guide

This document describes how to start the InternMatch application. You can either run the services manually for local development, or use Docker Compose to spin up the entire stack.

---

## Option A: Daily Development Workflow (Manual Startup)

If you are developing or modifying the codebase, you will need to start three terminal windows. Make sure you have completed the [Installation Guide](INSTALLATION.md) first.

### Terminal 1: AI Service (FastAPI)
Starts the NLP and Recommendation engine.
```bash
cd ai-service
# Activate your virtual environment
# Windows:
.venv\Scripts\activate
# Mac/Linux:
# source .venv/bin/activate

# Start the FastAPI server on port 8000
uvicorn app:app --port 8000 --reload
```
*API Documentation will be available at: http://localhost:8000/docs*

### Terminal 2: Core Backend (Spring Boot)
Starts the Java REST API.
```bash
cd backend
# Use the Maven wrapper to run the application
# Windows:
.\mvnw.cmd spring-boot:run
# Mac/Linux:
# ./mvnw spring-boot:run
```
*API Documentation will be available at: http://localhost:8081/swagger-ui/index.html*

### Terminal 3: Web Application (React)
Starts the Vite development server.
```bash
cd frontend
npm run dev
```
*The web interface will be available at: http://localhost:5173*

---

## Option B: Docker Compose (Full Stack Deployment)

If you just want to run the application without installing Java, Python, or Node locally, you can use Docker. 

Ensure you have **Docker Desktop** installed and running.

### 1. Build and Start
From the root of the repository, run:
```bash
docker compose up --build -d
```
> **Note:** The first build takes several minutes as it downloads Java dependencies, Node modules, Python packages, and the spaCy language models inside the containers.

### 2. Access the Application
- **React Frontend**: http://localhost
- **Spring Boot Backend**: http://localhost:8081
- **FastAPI AI**: http://localhost:8000
- **MySQL**: `localhost:3306`

### 3. View Logs
To view the logs of all running containers in real-time:
```bash
docker compose logs -f
```
To view logs for a specific service:
```bash
docker compose logs -f internmatch-backend
```

### 4. Restarting Services
If you make changes to a `.env` file or want to bounce a specific container:
```bash
docker compose restart internmatch-frontend
```

### 5. Stop the Application
To stop all containers and tear down the network:
```bash
docker compose down
```
If you also want to delete the persistent database volume (wiping the database entirely):
```bash
docker compose down -v
```

---

## Docker Container Breakdown
The `docker-compose.yml` spins up four integrated services:
1. **`internmatch-db`**: MySQL 8 database. Automatically executes `database/schema.sql` and `database/seed_data.sql` on initialization.
2. **`internmatch-ai`**: Python FastAPI container. Installs dependencies and NLP models during the build phase.
3. **`internmatch-backend`**: Java Spring Boot container. Compiles the `.jar` during a multi-stage build, then runs the lightweight JRE image.
4. **`internmatch-frontend`**: React SPA container. Builds the static HTML/JS via Node, and serves it using an NGINX web server proxy.
