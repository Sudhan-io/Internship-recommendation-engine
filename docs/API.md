# API Documentation

InternMatch operates primarily on REST APIs. The platform hosts two separate API gateways: the Spring Boot transactional API and the FastAPI AI Service API.

## 1. Postman Collection
For rapid testing and integration, a complete Postman collection is included in the repository.
- **File**: `docs/postman_collection.json`
- **Import Instructions**: Open Postman -> Click `Import` -> Select `postman_collection.json`.
- **Environment**: Ensure you set a local environment variable in Postman for the base URL (`http://localhost:8081` for backend) and handle the `Authorization: Bearer <token>` headers using a successful Login response.

---

## 2. Spring Boot Core Backend (Swagger / OpenAPI)
The Java backend utilizes `springdoc-openapi` to automatically generate interactive documentation for all endpoints.

**Accessing Swagger UI:**
When the backend is running locally, navigate to:
[http://localhost:8081/swagger-ui/index.html](http://localhost:8081/swagger-ui/index.html)

This interface provides:
- Complete schemas for User, StudentProfile, Resume, Internship, and Recommendation DTOs.
- Interactive "Try it out" buttons for simulating requests.
- Endpoint authorization configurations.

---

## 3. FastAPI AI Service (ReDoc / Swagger)
The AI service automatically generates documentation through FastAPI's built-in OpenAPI integration.

**Accessing FastAPI Docs:**
When the AI service is running locally, navigate to:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Primary AI Endpoint: `/recommendations/generate`
- **Method**: `POST`
- **Payload**: Requires raw `resume_text` (extracted by the backend) and a list of serialized `internships`.
- **Response**: Returns a JSON array of `RecommendationResult` objects, containing:
  - `final_score`: Weighted hybrid score.
  - `semantic_score`, `skill_score`, `education_score`, `experience_score`, `eligibility_score`.
  - `explanation`: The Explainable AI markdown string detailing the match rationale.
