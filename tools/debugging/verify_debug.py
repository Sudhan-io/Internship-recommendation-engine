import sys
import os
import traceback

sys.path.append("d:\\PROJECTS\\Internship-recommendation-engine\\ai-service")

from dataset.pipeline import IngestionPipeline

pipeline = IngestionPipeline()
csv_path = "d:\\PROJECTS\\Internship-recommendation-engine\\ai-service\\dataset\\linkedin_jobs.csv"

try:
    print("Running IngestionPipeline import_csv directly...")
    imported, rejected = pipeline.import_csv(csv_path)
    print(f"Imported: {imported}, Rejected: {rejected}")
except Exception as e:
    print("Exception occurred:")
    traceback.print_exc()
