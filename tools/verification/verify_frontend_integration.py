import urllib.request
import json
import time

BASE_URL = "http://localhost:8081/api"

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
        raise e

def test_integration():
    print("=== END-TO-END INTEGRATION TEST FOR SPRINT 19 ===")
    
    # Generate unique email to prevent duplicate registration issues
    unique_suffix = int(time.time())
    email = f"student_{unique_suffix}@stanford.edu"
    password = "password123"
    name = f"Test Student {unique_suffix}"
    
    # 1. Register
    print("\n[Step 1] Registering User...")
    reg_payload = {
        "fullName": name,
        "email": email,
        "password": password
    }
    reg_res = make_request(f"{BASE_URL}/auth/register", "POST", reg_payload)
    print(json.dumps(reg_res, indent=2))
    assert reg_res["success"] is True
    
    # 2. Login
    print("\n[Step 2] Logging In...")
    login_payload = {
        "email": email,
        "password": password
    }
    login_res = make_request(f"{BASE_URL}/auth/login", "POST", login_payload)
    print(json.dumps(login_res, indent=2))
    assert login_res["success"] is True
    token = login_res["data"]["token"]
    print("JWT Token acquired successfully.")
    
    # 3. Create Profile
    print("\n[Step 3] Creating Student Profile...")
    profile_payload = {
        "collegeName": "Stanford University",
        "department": "Computer Science",
        "yearOfStudy": 3,
        "cgpa": 9.40,
        "phone": "1234567890",
        "linkedinUrl": "https://linkedin.com/in/test",
        "githubUrl": "https://github.com/test"
    }
    create_res = make_request(f"{BASE_URL}/student/profile", "POST", profile_payload, token)
    print(json.dumps(create_res, indent=2))
    assert create_res["success"] is True
    
    # 4. Get Profile
    print("\n[Step 4] Querying Profile details...")
    get_res = make_request(f"{BASE_URL}/student/profile", "GET", None, token)
    print(json.dumps(get_res, indent=2))
    assert get_res["success"] is True
    assert get_res["data"]["collegeName"] == "Stanford University"
    
    # 5. Update Profile
    print("\n[Step 5] Updating Profile details...")
    profile_payload["cgpa"] = 9.85
    profile_payload["phone"] = "9876543210"
    update_res = make_request(f"{BASE_URL}/student/profile", "PUT", profile_payload, token)
    print(json.dumps(update_res, indent=2))
    assert update_res["success"] is True
    assert update_res["data"]["cgpa"] == 9.85
    assert update_res["data"]["phone"] == "9876543210"
    
    # 6. Upload Resume
    print("\n[Step 6] Uploading PDF Resume...")
    # Let's create a boundary multipart form upload
    boundary = "----WebKitFormBoundaryE2eTestBoundary"
    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Authorization": f"Bearer {token}"
    }
    
    # Let's generate a tiny mock PDF stream
    # PDFBox parses text from PDF. Since we need it to parse python/SQL skills to get good matches:
    # We can create a simple PDF with resume content!
    # Wait, instead of generating locally, we can read the test PDF we created in ResumeServiceTest
    # Or create a minimal PDF stream containing text:
    pdf_text = "John Doe. Skills: Python, SQL. Education: Bachelor of Engineering."
    # A simple PDF structure
    pdf_content = (
        b"%PDF-1.4\n"
        b"1 0 obj <</Type/Catalog/Pages 2 0 R>> endobj\n"
        b"2 0 obj <</Type/Pages/Kids[3 0 R]/Count 1>> endobj\n"
        b"3 0 obj <</Type/Page/Parent 2 0 R/Resources<<>>/Contents 4 0 R>> endobj\n"
        b"4 0 obj <</Length 60>> stream\n"
        b"BT\n/F1 12 Tf\n72 712 Td\n(John Doe. Skills: Python, SQL. Education: Bachelor of Engineering.) Tj\nET\n"
        b"endstream\nendobj\n"
        b"xref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000056 00000 n\n0000000111 00000 n\n0000000173 00000 n\n"
        b"trailer <</Size 5/Root 1 0 R>>\n"
        b"startxref\n283\n%%EOF\n"
    )
    
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="test_resume.pdf"\r\n'
        f"Content-Type: application/pdf\r\n\r\n"
    ).encode("utf-8") + pdf_content + f"\r\n--{boundary}--\r\n".encode("utf-8")
    
    url = f"{BASE_URL}/resumes/upload"
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as res:
            upload_res = json.loads(res.read().decode("utf-8"))
            print(json.dumps(upload_res, indent=2))
            assert upload_res["success"] is True
            assert upload_res["data"]["processingStatus"] == "TEXT_EXTRACTED"
    except Exception as ex:
        print(f"Resume upload failed: {ex}")
        raise ex
        
    # 7. Get Resume Status
    print("\n[Step 7] Checking Resume status...")
    resume_res = make_request(f"{BASE_URL}/resumes/my-resume", "GET", None, token)
    print(json.dumps(resume_res, indent=2))
    assert resume_res["success"] is True
    assert resume_res["data"]["fileName"].startswith("resume_")
    
    # 8. Generate Recommendations
    print("\n[Step 8] Triggering AI Recommendation Engine...")
    rec_res = make_request(f"{BASE_URL}/recommendations", "GET", None, token)
    print("=== Recommendations Output (First Result) ===")
    if rec_res["success"] and len(rec_res["data"]) > 0:
        first_match = rec_res["data"][0]
        print(json.dumps(first_match, indent=2))
        assert first_match["final_score"] > 0
        assert len(first_match["matched_skills"]) > 0
        print("\n-> E2E backend integration verified successfully!")
    else:
        print(json.dumps(rec_res, indent=2))
        raise AssertionError("No recommendations returned or service failed")

if __name__ == "__main__":
    time.sleep(5) # Allow Spring Boot time to fully start up
    test_integration()
