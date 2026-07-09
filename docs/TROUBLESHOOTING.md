# Troubleshooting Guide

This document outlines solutions to common issues encountered when setting up and running InternMatch.

## 1. Database Connection Failures
**Error:** `com.mysql.cj.jdbc.exceptions.CommunicationsException: Communications link failure`
**Solution:**
- Ensure MySQL is running on your machine (or Docker container).
- Verify the credentials in your `.env` file match your MySQL setup.
- Check if MySQL is running on a port other than `3306`. Update `DB_URL` accordingly.

## 2. Port Conflicts
**Error:** `Web server failed to start. Port 8081 was already in use.`
**Error:** `[Errno 98] Address already in use`
**Solution:**
- Identify the process blocking the port and terminate it.
- **Windows:** `netstat -ano | findstr :8081`, then `taskkill /PID <pid> /F`
- **Mac/Linux:** `lsof -i :8081`, then `kill -9 <pid>`

## 3. Missing spaCy NLP Model
**Error:** `OSError: [E050] Can't find model 'en_core_web_sm'.`
**Solution:**
The NLP model wasn't downloaded during setup. Run the following command inside the active python virtual environment:
```bash
python -m spacy download en_core_web_sm
```

## 4. Frontend API CORS Errors
**Error:** `Access to XMLHttpRequest at 'http://localhost:8081/...' from origin 'http://localhost:5173' has been blocked by CORS policy`
**Solution:**
- The Spring Boot backend includes a global CORS configuration allowing requests from `http://localhost:5173`. Ensure you are accessing the frontend via `localhost` and not `127.0.0.1` or a network IP.

## 5. Token Expiration / Unauthorized
**Error:** `401 Unauthorized` on API requests after a period of inactivity.
**Solution:**
- The JWT token has expired (default is 24 hours). Log out from the frontend and log back in to generate a fresh token.

## 6. Docker Build Failures
**Error:** Node/Python package installation timeouts during `docker compose up --build`.
**Solution:**
- Ensure you have a stable internet connection. Docker caches layers, so re-running the command will resume from where it failed.
