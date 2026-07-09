# Changelog

All notable changes to the **AI-Based Internship Recommendation Engine** will be documented in this file.

---

## [1.0.0] - 2026-07-04

### Added
- **Sprint 21: Production Hardening**
  - Parameterized all database properties, JWT secret, and FastAPI service urls with environment variables and fallback configuration.
  - Implemented 5MB upload constraints, mime-type verification (`application/pdf`), and case-insensitive extension validations for resumes.
  - Configured `@Slf4j` structured logging mapping logins, resume uploads, recommendations, and unexpected exception traces.
  - Added bean validation requirements on `StudentProfileRequest` mapping errors to 400 responses.
  - Implemented static internship caching in AI router, avoiding redundant SentenceTransformer encodings.
- **Sprint 20: End-to-End Orchestration & Caching**
  - Set up `RecommendationBatch` and `Recommendation` database entities supporting version history.
  - Developed transactional orchestrator service pipeline coordinating similarity engine and explainability model under a single database transaction boundary.
  - Integrated React frontend state with orchestrator API endpoints, verifying latency under 35ms on cache hits.
- **Sprint 19: Frontend Page Integration**
  - Built complete auth workflows (Login, Register, Logout, JWT persist/refresh) andProtectedRoutes.
  - Completed student Dashboard, Setup Profile form, AI Recommendations grids, application buttons, and match explanation modals.
- **Sprint 18: Explainable AI Module**
  - Developed Explainable AI LIME-inspired modeling tracing matching logic across semantic alignment, skill density, experience overlap, and eligibility status.
  - Configured Spring Boot backend to parse and format explanation structures into readable Markdown descriptions.
- **Sprint 9 to 17: Core AI Pipeline & Matching**
  - Integrated hybrid recommendation algorithms weighing semantic embedding similarity and custom business rules.
  - Designed skill matching density functions, qualification filters, and experience overlap scorings.
  - Configured spaCy parser for entity extraction, phrase detection, and vocabulary mapping.
  - Set up PDFBox parser and text normalizer pipeline.
