import os
import shutil
import urllib.request
import urllib.error
import json
import mysql.connector

def run_import():
    print("=== STARTING IMPORT PROCESS ===")
    dataset_dir = r"d:\PROJECTS\Internship-recommendation-engine\ai-service\dataset"
    processed_csv = os.path.join(dataset_dir, "processed", "internships_filtered.csv")
    target_csv = os.path.join(dataset_dir, "linkedin_jobs.csv")
    backup_csv = os.path.join(dataset_dir, "linkedin_jobs.csv.bak")
    
    # 1. Backup existing linkedin_jobs.csv
    if os.path.exists(target_csv):
        print(f"Backing up {target_csv} -> {backup_csv}")
        shutil.copy2(target_csv, backup_csv)
        
    # 2. Copy processed CSV to target
    print(f"Copying {processed_csv} -> {target_csv}")
    shutil.copy2(processed_csv, target_csv)
    
    # 3. Call POST /dataset/import
    url = "http://localhost:8000/dataset/import"
    print(f"Triggering import via API: {url}...")
    req = urllib.request.Request(url, method="POST", headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as res:
            res_data = json.loads(res.read().decode("utf-8"))
            print("Import response:")
            print(json.dumps(res_data, indent=2))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"Import API failed (HTTP {e.code}): {error_body}")
        # Restore backup
        if os.path.exists(backup_csv):
            shutil.move(backup_csv, target_csv)
        raise
    except Exception as e:
        print(f"Import API failed: {e}")
        # Restore backup
        if os.path.exists(backup_csv):
            shutil.move(backup_csv, target_csv)
        raise
        
    # 4. Restore original file
    if os.path.exists(backup_csv):
        print(f"Restoring backup -> {target_csv}")
        shutil.move(backup_csv, target_csv)
        
    # 5. Verify database counts
    print("\nVerifying database counts...")
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sudh@007",
        database="internship_recommendation_engine"
    )
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT COUNT(*) as count FROM internships")
    internship_count = cursor.fetchone()["count"]
    print(f"Total internships in database: {internship_count}")
    
    cursor.execute("SELECT COUNT(*) as count FROM skills")
    skills_count = cursor.fetchone()["count"]
    print(f"Total skills in database: {skills_count}")
    
    cursor.execute("SELECT COUNT(*) as count FROM internship_skills")
    links_count = cursor.fetchone()["count"]
    print(f"Total internship_skills links: {links_count}")
    
    cursor.close()
    conn.close()
    print("=== IMPORT PROCESS COMPLETED ===")

if __name__ == "__main__":
    run_import()
