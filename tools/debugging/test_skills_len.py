import os
import csv
from dataset.pipeline import IngestionPipeline

def test_lengths():
    pipeline = IngestionPipeline()
    csv_path = r"d:\PROJECTS\Internship-recommendation-engine\ai-service\dataset\processed\internships_filtered.csv"
    
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            try:
                cleaned = pipeline.clean_row(row)
                skills_joined = ", ".join(cleaned["skills"])
                if len(skills_joined) > 255:
                    print(f"Row {i} exceeds 255! Length: {len(skills_joined)}")
                    print(f"  Title: {cleaned['title']}")
                    print(f"  Company: {cleaned['company_name']}")
                    print(f"  Skills: {skills_joined}")
            except Exception as e:
                print(f"Row {i} failed clean_row: {e}")

if __name__ == "__main__":
    test_lengths()
