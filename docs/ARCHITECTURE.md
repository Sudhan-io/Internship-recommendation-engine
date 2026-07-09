# System Architecture

InternMatch is designed as a hybrid-microservice architecture that separates heavy Natural Language Processing (NLP) workloads from transactional web requests.

## 1. High-Level Architecture
The architecture comprises three main application tiers communicating securely over REST.

```mermaid
graph TD
    Client[Vite + React Frontend] <-->|REST API + JWT| Backend[Spring Boot Core Service]
    Backend <-->|JPA / JDBC| DB[(MySQL Database)]
    Backend <-->|JSON Rest API| AI[FastAPI AI Recommendation Service]
    AI -->|NLP / Embeddings| Models(spaCy + SentenceTransformers)
```

## 2. Component Subsystems
To ensure maintainability and separation of concerns, the application is divided into distinct containers:

```mermaid
graph TD
    subgraph Frontend [React Frontend Container]
        UI[React Pages & Components]
        API_Client[Axios Interceptors]
        Context[Auth Context State]
    end

    subgraph Backend_App [Spring Boot Core Container]
        Controller[REST Controllers]
        Security[Spring Security & JWT Filters]
        Service[Orchestration Service]
        Repo[JPA Repository Layer]
    end

    subgraph AI_App [FastAPI Service Container]
        Router[Recommendation API Router]
        Parser[spaCy Resume Parser]
        Normalizer[Entity Normalizer]
        Embed[SentenceTransformer Service]
        Engine[Hybrid Scoring Engine]
        XAI[Explainability Generator]
    end

    subgraph Storage [Database Container]
        MySQL[(MySQL Server)]
    end

    UI --> API_Client
    API_Client --> Security
    Security --> Controller
    Controller --> Service
    Service --> Repo
    Service --> Router
    Repo --> MySQL
    Router --> Parser
    Parser --> Normalizer
    Normalizer --> Embed
    Embed --> Engine
    Engine --> XAI
```

## 3. The Recommendation Workflow
The AI Recommendation pipeline involves a complex synchronization between the transactional database and the stateless AI inference engine.

```mermaid
sequenceDiagram
    autonumber
    actor Student as Student (React Web App)
    participant Spring as Spring Boot Core
    participant DB as MySQL DB
    participant FastAPI as FastAPI AI Service

    Student->>Spring: POST /api/recommendations/generate
    Note over Spring: Verify JWT authentication
    Spring->>DB: Fetch user's latest Resume and Profile
    DB-->>Spring: Return resume record
    Spring->>DB: Retrieve all available internships
    DB-->>Spring: Return list of internships
    Spring->>FastAPI: POST /recommendations/generate (resume_text, internships)
    
    Note over FastAPI: Run spaCy NER Text Parsing
    Note over FastAPI: Normalize skills, education & experience dates
    Note over FastAPI: Fetch cache or encode dense embeddings (all-MiniLM-L6-v2)
    Note over FastAPI: Compute Cosine Similarity & Hybrid score metrics
    Note over FastAPI: Run Explainable AI matching trace generator
    FastAPI-->>Spring: Return scored internships & match explanations
    
    Note over Spring: Start Database Transaction (@Transactional)
    Spring->>DB: Persist new RecommendationBatch
    Spring->>DB: Save list of scored Recommendation records
    Spring->>DB: Transition Resume status -> RECOMMENDATION_READY
    Note over Spring: Commit Database Transaction
    
    Spring-->>Student: Return sorted recommendations list
```

## 4. Rationale
- **Spring Boot Core:** Java is utilized for the primary backend due to its robust ecosystem for handling transactional safety (`@Transactional`), complex relational mappings (JPA/Hibernate), and enterprise-grade security (Spring Security/JWT).
- **FastAPI AI Service:** Python is the undisputed leader in AI/ML ecosystems. Attempting to run spaCy and Hugging Face models in Java would be highly inefficient. FastAPI provides an asynchronous, lightning-fast bridge to expose these Python data-science models to the Java backend.
- **Batch Persistence:** Recommendations are generated dynamically but are persisted in MySQL linked to a `batch_id`. This allows the student to log off and return later to instantly view their cached recommendations without regenerating the embeddings.
