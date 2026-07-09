import urllib.request
import json
import mysql.connector

def verify_db_records():
    # Load DB config directly
    config = {
        "host": "localhost",
        "user": "root",
        "password": "Sudh@007", # Use password from application.properties
        "database": "internship_recommendation_engine"
    }
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        # Check internships
        cursor.execute("SELECT COUNT(*) FROM internships")
        count = cursor.fetchone()[0]
        print(f"Total internships in database: {count}")
        
        # Select first few internships to show normalized fields
        cursor.execute("SELECT internship_id, title, company, location, mode FROM internships LIMIT 5")
        rows = cursor.fetchall()
        print("\nFirst 5 Internship Records:")
        for r in rows:
            print(f"ID: {r[0]}, Title: {r[1]}, Company: {r[2]}, Location: {r[3]}, Mode: {r[4]}")
            
            # Print associated skills
            cursor.execute(
                """SELECT s.skill_name FROM skills s 
                   JOIN internship_skills is_link ON s.skill_id = is_link.skill_id 
                   WHERE is_link.internship_id = %s""",
                (r[0],)
            )
            skills = [row[0] for row in cursor.fetchall()]
            print(f"  -> Skills: {skills}")
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Database query failed: {e}")

def test_import():
    url = "http://127.0.0.1:8000/dataset/import"
    req = urllib.request.Request(url, method="POST")
    try:
        print("Calling /dataset/import API...")
        with urllib.request.urlopen(req) as res:
            response = json.loads(res.read().decode("utf-8"))
            print("=== Ingestion Endpoint Response ===")
            print(json.dumps(response, indent=2))
            print("-" * 50)
            
            # Verify DB content
            verify_db_records()
            
    except Exception as e:
        print(f"Failed to test dataset import: {e}")

test_import()
