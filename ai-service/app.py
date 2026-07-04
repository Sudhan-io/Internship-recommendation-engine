from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.resume import router as resume_router
from routers.dataset import router as dataset_router
from routers.recommendation import router as rec_router

app = FastAPI(
    title="InternMatch AI Service",
    description="AI/NLP services for internship recommendation engine",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume_router)
app.include_router(dataset_router)
app.include_router(rec_router)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ai-service",
        "version": "1.0.0"
    }

@app.on_event("startup")
def startup_event():
    print("AI Service started successfully.")
