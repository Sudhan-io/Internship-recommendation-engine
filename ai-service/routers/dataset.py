from fastapi import APIRouter, HTTPException
from dataset.pipeline import IngestionPipeline
import os

router = APIRouter(prefix="/dataset", tags=["Dataset"])
pipeline = IngestionPipeline()

@router.post("/import")
def import_dataset():
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(current_dir, "dataset", "linkedin_jobs.csv")
    
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="Dataset CSV not found")
        
    try:
        imported, rejected = pipeline.import_csv(csv_path)
        return {
            "status": "success",
            "imported_records": imported,
            "rejected_records": rejected,
            "message": "Dataset imported and cleaned successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
