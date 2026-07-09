import urllib.request
import json
import time

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

def test_sprint21():
    print("=== SPRINT 21 PRODUCTION HARDENING VERIFICATION ===")
    
    # 1. Setup Unique User
    unique_suffix = int(time.time())
    email = f"hardening_{unique_suffix}@college.edu"
    password = "password123"
    name = f"Hardened Student {unique_suffix}"
    
    print("\n[Security & Login] Registering and logging in...")
    reg_payload = {"fullName": name, "email": email, "password": password}
    reg_res, reg_code = make_request(f"{BASE_URL}/auth/register", "POST", reg_payload)
    assert reg_code == 200 and reg_res["success"] is True
    
    login_res, login_code = make_request(f"{BASE_URL}/auth/login", "POST", {"email": email, "password": password})
    assert login_code == 200 and login_res["success"] is True
    token = login_res["data"]["token"]
    print("-> Registered and logged in successfully.")
    
    # 2. Test Invalid/Malformed Requests
    print("\n[Validation] Sending malformed JSON (malformed payload)...")
    malformed_json = '{"fullName": "Hardened", "email": "hardening@test.com", "password": }' # syntax error
    res, code = make_request(f"{BASE_URL}/auth/login", "POST", malformed_json)
    print(f"Response: {res}, HTTP Code: {code}")
    assert code == 400 and res["success"] is False
    assert "Malformed request payload" in res["message"]
    print("-> Malformed JSON request successfully rejected with HTTP 400.")

    # 3. Test Invalid Inputs (Null values on profile fields)
    print("\n[Validation] Sending profile request with missing/null mandatory fields...")
    profile_payload_missing = {
        "collegeName": "",
        "department": "Computer Science",
        "yearOfStudy": 3,
        "cgpa": 12.5, # invalid CGPA > 10
        "phone": "abc" # invalid phone format
    }
    res, code = make_request(f"{BASE_URL}/student/profile", "POST", profile_payload_missing, token)
    print(f"Response: {res}, HTTP Code: {code}")
    assert code == 400 and res["success"] is False
    assert "Validation failed:" in res["message"]
    print("-> Profile field validations successfully enforced with detailed validation errors.")

    # 4. Test File Upload Mime-Type Validation
    print("\n[Security] Uploading non-PDF file (txt)...")
    boundary = "----WebKitFormBoundaryHardeningBoundary"
    headers_txt = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Authorization": f"Bearer {token}"
    }
    body_txt = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="malicious.txt"\r\n'
        f"Content-Type: text/plain\r\n\r\n"
        f"This is a text file content\r\n"
        f"--{boundary}--\r\n"
    ).encode("utf-8")
    res, code = make_request(f"{BASE_URL}/resumes/upload", "POST", body_txt, token, headers_txt)
    print(f"Response: {res}, HTTP Code: {code}")
    assert code in [400, 415] and res["success"] is False
    print("-> Non-PDF upload rejected with proper HTTP code.")

    # 5. Test File Upload Size Limit Validation (Oversized payload)
    print("\n[Security] Uploading oversized file (>5MB)...")
    # Simulate a file larger than 5MB
    large_pdf_content = b"%PDF-1.4\n" + (b"A" * (5 * 1024 * 1024 + 100))
    body_large = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="large.pdf"\r\n'
        f"Content-Type: application/pdf\r\n\r\n"
    ).encode("utf-8") + large_pdf_content + f"\r\n--{boundary}--\r\n".encode("utf-8")
    
    res, code = make_request(f"{BASE_URL}/resumes/upload", "POST", body_large, token, headers_txt)
    print(f"Response: {res}, HTTP Code: {code}")
    assert code == 413 and res["success"] is False
    print("-> Oversized upload successfully rejected with HTTP 413 Payload Too Large.")

    print("\n=== ALL SPRINT 21 PRODUCTION HARDENING SCENARIOS VERIFIED SUCCESSFULLY! ===")

if __name__ == "__main__":
    test_sprint21()
