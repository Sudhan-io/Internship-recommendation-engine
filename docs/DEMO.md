# Presentation & Demo Script

This document provides a recommended 5–10 minute demonstration flow for presenting InternMatch to interviewers, evaluators, or open-source contributors.

## Recommended Demonstration Flow

### 1. Registration & Authentication (1 min)
- **Action**: Navigate to the Login page and register a new student account.
- **Talking Point**: Highlight the stateless JWT authentication architecture. Mention that passwords are securely hashed via BCrypt in the Spring Boot backend.

### 2. Profile Setup (1 min)
- **Action**: Fill in the basic academic profile (CGPA, Department, Year).
- **Talking Point**: Emphasize how the backend enforces data integrity (e.g. CGPA validation) and links profile records securely to the authenticated User context.

### 3. Resume Upload & Processing (2 mins)
- **Action**: Drag and drop a sample PDF resume into the dashboard upload zone.
- **Talking Point**: Describe the NLP pipeline. As it uploads, explain that the FastAPI AI service uses `spaCy` to parse the layout and extract Named Entities (Skills, Education, Experience). Explain that these entities are passed to a `SentenceTransformer` (`all-MiniLM-L6-v2`) to generate dense semantic vector embeddings.

### 4. Explainable AI Recommendations (2 mins)
- **Action**: Click to view the generated recommendations. Open the specific details modal for the top match.
- **Talking Point**: Highlight the **Hybrid Scoring Engine**. Explain that it doesn't just use simple vector similarity, but a weighted formula (Semantic Score, Skill Density, Education, Experience, Eligibility). Show the Explainable AI (XAI) markdown output that transparently explains *why* the student matched, highlighting exact missing vs. matching skills.

### 5. Caching & Performance (1 min)
- **Action**: Navigate away from the recommendations page and navigate back.
- **Talking Point**: Show how the recommendations load instantly. Explain the **Batch Persistence Architecture**—scores are calculated asynchronously and cached in the MySQL database, preventing expensive repeated AI inferences.

### 6. API Documentation (1 min)
- **Action**: Open `http://localhost:8081/swagger-ui/index.html` and `http://localhost:8000/docs`.
- **Talking Point**: Show the auto-generated Swagger interfaces. Explain the microservice separation of concerns (Java for transactions, Python for Data Science).

---

## Common Interviewer Questions & Answers

**Q: Why separate Spring Boot and FastAPI instead of using one monolithic backend?**
> *A: Separation of concerns. Java (Spring Boot) is unparalleled for enterprise security, ORM transactional safety, and robust web APIs. However, Python (FastAPI) is the industry standard for AI/ML. Running spaCy and PyTorch models in Java is inefficient. This microservice architecture uses the best tool for each specific job.*

**Q: How do you handle unstructured resume layouts?**
> *A: We use a combination of regex-based bounding boxes and a trained spaCy Named Entity Recognition (NER) pipeline. It identifies headers (Education, Experience) and tokenizes the text beneath them, normalizing the output against a canonical dictionary to handle variations (e.g., mapping "JS" to "JavaScript").*

**Q: Is the vector search scalable?**
> *A: Currently, we use an in-memory optimized Numpy cosine similarity matrix, which is exceptionally fast for our curated dataset of ~1,000 internships. For production scaling to millions of records, the architecture is designed so the `EmbeddingRepository` interface can easily swap to a persistent vector database like Pgvector or Qdrant without rewriting the scoring engine.*
