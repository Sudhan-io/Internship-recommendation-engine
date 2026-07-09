import urllib.request
import json
import time
import mysql.connector

BASE_URL = "http://localhost:8081/api"

# MySQL connection parameters (from application.properties)
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Sudh@007",
    "database": "internship_recommendation_engine"
}

def make_request(url, method="GET", data=None, token=None):
    headers = {
        "Content-Type": "application/json",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    req_data = None
    if data:
        req_data = json.dumps(data).encode("utf-8")
        
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
        return {"success": False, "status_code": e.code, "message": e.read().decode('utf-8')}
    except Exception as e:
        print(f"Connection Error: {e}")
        return {"success": False, "status_code": 503, "message": str(e)}

def query_db(query, params=None):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res

def test_sprint20():
    print("=== SPRINT 20 END-TO-END ORCHESTRATION & PERSISTENCE VERIFICATION ===")
    
    unique_suffix = int(time.time())
    email = f"sprint20_{unique_suffix}@college.edu"
    password = "password123"
    name = f"Sprint20 Student {unique_suffix}"
    
    # 1. Register and Login
    print("\n[Test 1] Registering and Logging In...")
    reg_payload = {"fullName": name, "email": email, "password": password}
    reg_res = make_request(f"{BASE_URL}/auth/register", "POST", reg_payload)
    assert reg_res["success"] is True
    
    login_res = make_request(f"{BASE_URL}/auth/login", "POST", {"email": email, "password": password})
    token = login_res["data"]["token"]
    print("JWT Token acquired successfully.")
    
    # 2. Setup Profile
    print("\n[Test 2] Creating Student Profile...")
    profile_payload = {
        "collegeName": "Stanford University",
        "department": "Computer Science",
        "yearOfStudy": 3,
        "cgpa": 9.20,
        "phone": "9876543210",
        "linkedinUrl": "https://linkedin.com",
        "githubUrl": "https://github"
    }
    create_res = make_request(f"{BASE_URL}/student/profile", "POST", profile_payload, token)
    assert create_res["success"] is True
    
    # 3. Test Missing Resume HTTP 404
    print("\n[Test 3] Requesting recommendations with missing resume (Should be HTTP 404)...")
    rec_404_res = make_request(f"{BASE_URL}/recommendations", "GET", None, token)
    assert rec_404_res["status_code"] == 404
    print("-> Missing resume HTTP 404 verified successfully.")

    # 4. Upload Resume
    print("\n[Test 4] Uploading PDF Resume...")
    boundary = "----WebKitFormBoundarySprint20Boundary"
    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Authorization": f"Bearer {token}"
    }
    pdf_content = (
        b"%PDF-1.4\n1 0 obj <</Type/Catalog/Pages 2 0 R>> endobj\n2 0 obj <</Type/Pages/Kids[3 0 R]/Count 1>> endobj\n"
        b"3 0 obj <</Type/Page/Parent 2 0 R/Resources<<>>/Contents 4 0 R>> endobj\n4 0 obj <</Length 60>> stream\n"
        b"BT\n/F1 12 Tf\n72 712 Td\n(Skills: Python, SQL. Education: Bachelor of Engineering.) Tj\nET\nendstream\nendobj\n"
        b"xref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000056 00000 n\n0000000111 00000 n\n0000000173 00000 n\n"
        b"trailer <</Size 5/Root 1 0 R>>\nstartxref\n283\n%%EOF\n"
    )
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="sprint20_resume.pdf"\r\n'
        f"Content-Type: application/pdf\r\n\r\n"
    ).encode("utf-8") + pdf_content + f"\r\n--{boundary}--\r\n".encode("utf-8")
    
    req = urllib.request.Request(f"{BASE_URL}/resumes/upload", data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req) as res:
        upload_res = json.loads(res.read().decode("utf-8"))
        assert upload_res["success"] is True
        resume_id = upload_res["data"]["resumeId"]
        print(f"Resume uploaded. ID: {resume_id}, Status: {upload_res['data']['processingStatus']}")
        assert upload_res["data"]["processingStatus"] == "TEXT_EXTRACTED"
        
    # 5. Generate Recommendations (POST)
    print("\n[Test 5] Explicitly generating recommendations (POST)...")
    start_time = time.time()
    gen_res = make_request(f"{BASE_URL}/recommendations/generate", "POST", None, token)
    latency = (time.time() - start_time) * 1000
    assert gen_res["success"] is True
    print(f"Recommendations generated in {latency:.2f} ms.")
    recs = gen_res["data"]
    assert len(recs) > 0
    print(f"Returned {len(recs)} matches.")
    
    # Assert descending order
    scores = [r["final_score"] for r in recs]
    assert scores == sorted(scores, reverse=True)
    print("-> Recommendations are sorted by score descending.")
    
    # Check DB records
    batches = query_db("SELECT * FROM recommendation_batches WHERE resume_id = %s", (resume_id,))
    assert len(batches) == 1
    batch = batches[0]
    print(f"RecommendationBatch persisted. ID: {batch['batch_id']}, Model: {batch['model_name']}, Count: {batch['recommendation_count']}")
    
    db_recs = query_db("SELECT * FROM recommendations WHERE batch_id = %s", (batch['batch_id'],))
    assert len(db_recs) == len(recs)
    print(f"Saved {len(db_recs)} Recommendation records to DB.")
    
    # Check resume status in DB has transitioned to RECOMMENDATION_READY
    db_resume = query_db("SELECT * FROM resumes WHERE resume_id = %s", (resume_id,))[0]
    assert db_resume["processing_status"] == "RECOMMENDATION_READY"
    assert db_resume["embedding_generated"] == 1
    print("-> Resume status transitioned to RECOMMENDATION_READY in DB.")

    # 6. Retrieve Cached Recommendations (GET)
    print("\n[Test 6] Querying cached recommendations (GET)...")
    start_time = time.time()
    get_res = make_request(f"{BASE_URL}/recommendations", "GET", None, token)
    cache_latency = (time.time() - start_time) * 1000
    assert get_res["success"] is True
    print(f"Cache retrieved in {cache_latency:.2f} ms (FastAPI call avoided).")
    
    # Check that scores and count match exactly
    cached_recs = get_res["data"]
    assert len(cached_recs) == len(recs)
    assert [r["final_score"] for r in cached_recs] == scores
    print("-> Caching and retrieval verified successfully.")

    # 7. Incremental Regeneration on New Resume
    print("\n[Test 7] Uploading a second resume to test incremental regeneration...")
    req = urllib.request.Request(f"{BASE_URL}/resumes/upload", data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req) as res:
        upload_res2 = json.loads(res.read().decode("utf-8"))
        resume_id2 = upload_res2["data"]["resumeId"]
        assert resume_id2 != resume_id
        
    print(f"Second resume uploaded. ID: {resume_id2}. Querying GET /recommendations...")
    # This should automatically trigger regeneration since no batch exists for resume_id2
    start_time = time.time()
    get_res2 = make_request(f"{BASE_URL}/recommendations", "GET", None, token)
    regen_latency = (time.time() - start_time) * 1000
    assert get_res2["success"] is True
    print(f"Recommendations regenerated automatically in {regen_latency:.2f} ms.")
    
    # Check database
    batches2 = query_db("SELECT * FROM recommendation_batches WHERE resume_id = %s", (resume_id2,))
    assert len(batches2) == 1
    print(f"-> Incremental regeneration for new resume verified successfully. New batch ID: {batches2[0]['batch_id']}.")
    
    print("\n=== ALL SPRINT 20 E2E SCENARIOS VERIFIED SUCCESSFULLY! ===")

if __name__ == "__main__":
    test_sprint20()
