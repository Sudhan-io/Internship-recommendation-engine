# Deployment Guide

This guide explains how to deploy the InternMatch architecture to production environments.

The system is designed as a modular, multi-container architecture consisting of:
1. **React Frontend**
2. **Spring Boot Core Backend**
3. **FastAPI AI Service**
4. **MySQL Database**

## Deployment Strategies

### 1. Docker Compose (VPS / Self-Hosted)
The simplest way to deploy the entire stack is using a single Virtual Private Server (VPS) via DigitalOcean, AWS EC2, or Linode using the provided `docker-compose.yml`.

1. Provision a Linux server with at least 4GB RAM (NLP models require significant memory).
2. Install Docker and Docker Compose on the server.
3. Clone the repository to the server.
4. Modify the `.env` file with secure production passwords.
5. Run the detached deployment:
   ```bash
   docker compose up --build -d
   ```
6. Set up a reverse proxy (like NGINX or Traefik) to route traffic to the containers and terminate SSL/TLS.

---

### 2. Managed Cloud Providers (PaaS)
For high availability and easier CI/CD pipelines, deploying individual services to specialized PaaS providers is recommended.

#### Database (PlanetScale / AWS RDS)
Deploy a MySQL 8.0 instance on a managed provider.
- Retrieve the connection URL.
- Run the `database/schema.sql` and `database/seed_data.sql` scripts against it using a MySQL client.

#### FastAPI AI Service (Render / Railway)
- **Service**: Render or Railway
- **Environment**: Python
- **Build Command**: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
- **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
- **Notes**: Ensure the instance has at least 1GB of memory.

#### Spring Boot Backend (Railway)
- **Service**: Railway
- **Environment**: Java (Maven)
- **Environment Variables**:
  - `DB_URL`: The connection string from your managed database.
  - `DB_USERNAME` / `DB_PASSWORD`: Database credentials.
  - `JWT_SECRET`: A secure randomly generated string.
  - `AI_SERVICE_URL`: The public URL of the deployed FastAPI service.
- Railway will automatically detect the `pom.xml`, build the JAR, and execute it.

#### React Frontend (Vercel / Netlify)
- **Service**: Vercel
- **Framework Preset**: Vite
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Environment Variables**: Update Axios base URLs in the frontend codebase (if currently hardcoded to localhost) to point to your Railway Spring Boot API URL.

## Pre-Flight Checklist
Before releasing your deployment:
- [ ] Change `JWT_SECRET` to a cryptographically secure random string.
- [ ] Ensure database credentials differ from the default `root` / `Sudh@007`.
- [ ] Verify that the frontend can successfully reach the backend API via HTTPS.
- [ ] Verify the backend can successfully communicate with the AI service.
