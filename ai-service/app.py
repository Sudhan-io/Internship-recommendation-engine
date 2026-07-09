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
    try:
        from dataset.pipeline import IngestionPipeline
        import mysql.connector
        from routers.recommendation import embedding_service
        
        print("Pre-warming internship embeddings cache on startup...")
        pipeline = IngestionPipeline()
        conn = mysql.connector.connect(**pipeline.db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM internships")
        internships = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if internships:
            internship_tuples = []
            for item in internships:
                iid = item.get("internship_id") or item.get("internshipId")
                internship_tuples.append((iid, item))
                
            uncached = []
            for iid, item in internship_tuples:
                if not embedding_service.repository.get_internship_embedding(iid):
                    uncached.append((iid, item))
                    
            if uncached:
                print(f"Generating embeddings for {len(uncached)} internships on startup...")
                embedding_service.generate_internships_batch(uncached)
                print("Cache pre-warmed successfully!")
            else:
                print("All internship embeddings already cached.")
    except Exception as e:
        print(f"Failed to pre-warm cache: {e}")
