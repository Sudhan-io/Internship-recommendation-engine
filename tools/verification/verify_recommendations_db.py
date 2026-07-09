import urllib.request
import json
import time
import mysql.connector

BASE_URL = "http://localhost:8081/api"

def make_request(url, method="GET", data=None, token=None, headers_override=None):
    headers = {
        "Content-Type": "application/json",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if headers_override:
        headers.update(headers_override)
        
    req_data = None
    if data is not None:
        if isinstance(data, bytes):
            req_data = data
        elif isinstance(data, str):
            req_data = data.encode("utf-8")
        else:
            req_data = json.dumps(data).encode("utf-8")
        
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read().decode("utf-8")), res.status
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        try:
            return json.loads(body), e.code
        except Exception:
            return {"success": False, "message": body}, e.code
    except Exception as e:
        return {"success": False, "message": str(e)}, 500

def test_recommendation_flow():
    print("=== STARTING RECOMMENDATION SYSTEM E2E DB PERSISTENCE TEST ===")
    
    # 1. Setup Unique User
    unique_suffix = int(time.time())
    email = f"student_{unique_suffix}@stanford.edu"
    password = "password123"
    name = f"Stanford Student {unique_suffix}"
    
    print("\n[Step 1] Registering and logging in...")
    reg_payload = {"fullName": name, "email": email, "password": password}
    reg_res, reg_code = make_request(f"{BASE_URL}/auth/register", "POST", reg_payload)
    assert reg_code == 200 and reg_res["success"] is True
    
    login_res, login_code = make_request(f"{BASE_URL}/auth/login", "POST", {"email": email, "password": password})
    assert login_code == 200 and login_res["success"] is True
    token = login_res["data"]["token"]
    print("User authenticated successfully.")
    
    # 2. Setup Student Profile
    print("\n[Step 2] Setting up student profile...")
    profile_payload = {
        "collegeName": "Stanford University",
        "department": "Computer Science",
        "yearOfStudy": 3,
        "cgpa": 9.4,
        "phone": "1234567890",
        "linkedinUrl": "https://linkedin.com/in/stanford-student",
        "githubUrl": "https://github.com/stanford-student"
    }
    prof_res, prof_code = make_request(f"{BASE_URL}/student/profile", "POST", profile_payload, token)
    assert prof_code == 200 and prof_res["success"] is True
    print("Profile created successfully.")
    
    # 3. Upload Mock PDF Resume
    print("\n[Step 3] Uploading resume...")
    boundary = "----WebKitFormBoundaryE2EDBPersistBoundary"
    headers_multipart = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Authorization": f"Bearer {token}"
    }
    # Load an existing real PDF file to satisfy PDFBox validation
    import glob
    pdf_files = glob.glob(r"d:\PROJECTS\Internship-recommendation-engine\backend\uploads\resumes\resume_*.pdf")
    if pdf_files:
        print(f"Reading valid PDF file: {pdf_files[0]}")
        with open(pdf_files[0], "rb") as f:
            pdf_content = f.read()
    else:
        pdf_content = b"%PDF-1.4\n%mock resume content\nSkills: Python, SQL, Git, React, JavaScript"

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="resume.pdf"\r\n'
        f"Content-Type: application/pdf\r\n\r\n"
    ).encode("utf-8") + pdf_content + f"\r\n--{boundary}--\r\n".encode("utf-8")
    
    upload_res, upload_code = make_request(f"{BASE_URL}/resumes/upload", "POST", body, token, headers_multipart)
    assert upload_code == 200 and upload_res["success"] is True
    print("Resume uploaded successfully.")
    
    # 4. Generate recommendations
    print("\n[Step 4] Requesting AI recommendations (will trigger generation)...")
    recs_res, recs_code = make_request(f"{BASE_URL}/recommendations", "GET", None, token)
    
    print(f"Response Code: {recs_code}")
    print(f"Success: {recs_res.get('success')}")
    if recs_code == 200:
        data = recs_res.get("data", [])
        print(f"Number of recommendations returned: {len(data)}")
        if len(data) > 0:
            print("First recommendation snippet:")
            first = data[0]
            print(f"  Internship ID: {first.get('internship_id')}")
            print(f"  Title: {first.get('title')}")
            print(f"  Company: {first.get('company')}")
            print(f"  Final Score: {first.get('final_score')}")
            print(f"  Explanation: {first.get('explanation_text')}")
    else:
        print(f"Error: {recs_res.get('message')}")
        assert False, "Recommendations call failed"

    # 5. Direct MySQL Database inspection
    print("\n[Step 5] Direct MySQL Inspection...")
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sudh@007",
        database="internship_recommendation_engine"
    )
    cursor = conn.cursor(dictionary=True)
    
    # Count recommendation batches
    cursor.execute("SELECT COUNT(*) as count FROM recommendation_batches")
    batch_count = cursor.fetchone()["count"]
    print(f"Total batches in DB: {batch_count}")
    
    # Count individual recommendations
    cursor.execute("SELECT COUNT(*) as count FROM recommendations")
    rec_count = cursor.fetchone()["count"]
    print(f"Total recommendations in DB: {rec_count}")
    
    # Inspect columns of last recommendation
    cursor.execute("SELECT * FROM recommendations ORDER BY recommendation_id DESC LIMIT 1")
    last_rec = cursor.fetchone()
    print("Saved recommendation columns and values:")
    for col, val in last_rec.items():
        print(f"  {col}: {val}")
        
    cursor.close()
    conn.close()
    print("\n=== E2E RECOMMENDATION SYSTEM DB PERSISTENCE TEST COMPLETED SUCCESSFULLY ===")

if __name__ == "__main__":
    test_recommendation_flow()
