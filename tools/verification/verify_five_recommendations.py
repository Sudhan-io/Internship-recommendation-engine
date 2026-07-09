import urllib.request
import urllib.error
import json
import glob
import os
import time

BASE_URL = "http://localhost:8081/api"

def make_request(url, method="GET", payload=None, token=None, custom_headers=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if custom_headers:
        headers.update(custom_headers)
    elif payload is not None:
        headers["Content-Type"] = "application/json"
        
    data = None
    if payload is not None:
        if isinstance(payload, bytes):
            data = payload
        else:
            data = json.dumps(payload).encode("utf-8")
            
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read().decode("utf-8")), res.status
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            return json.loads(body), e.code
        except:
            return {"error": body}, e.code
    except Exception as e:
        return {"error": str(e)}, 500

def register_and_login(username, email, password):
    # Register
    reg_payload = {"fullName": username, "email": email, "password": password, "role": "STUDENT"}
    make_request(f"{BASE_URL}/auth/register", "POST", reg_payload)
    
    # Login
    login_res, code = make_request(f"{BASE_URL}/auth/login", "POST", {"email": email, "password": password})
    if code == 200 and login_res.get("success"):
        return login_res["data"]["token"]
    raise RuntimeError(f"Login failed: {login_res}")

def create_profile(token, college, dept, year, cgpa, phone):
    profile_payload = {
        "collegeName": college,
        "department": dept,
        "yearOfStudy": year,
        "cgpa": cgpa,
        "phone": phone,
        "linkedinUrl": "https://linkedin.com/in/test",
        "githubUrl": "https://github.com/test"
    }
    res, code = make_request(f"{BASE_URL}/student/profile", "POST", profile_payload, token)
    if code == 200 and res.get("success"):
        return res
    raise RuntimeError(f"Profile creation failed: {res}")

def upload_resume(token, pdf_path):
    boundary = "----WebKitFormBoundaryFiveRecsBoundary"
    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}"
    }
    with open(pdf_path, "rb") as f:
        pdf_content = f.read()
        
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{os.path.basename(pdf_path)}"\r\n'
        f"Content-Type: application/pdf\r\n\r\n"
    ).encode("utf-8") + pdf_content + f"\r\n--{boundary}--\r\n".encode("utf-8")
    
    res, code = make_request(f"{BASE_URL}/resumes/upload", "POST", body, token, headers)
    if code == 200 and res.get("success"):
        return res
    raise RuntimeError(f"Resume upload failed: {res}")

def get_recommendations(token):
    res, code = make_request(f"{BASE_URL}/recommendations", "GET", None, token)
    if code == 200 and res.get("success"):
        return res["data"]
    raise RuntimeError(f"Recommendations failed: {res}")

def main():
    print("=== STARTING FIVE RECOMMENDATION TESTS ===")
    resumes_dir = r"d:\PROJECTS\Internship-recommendation-engine\backend\uploads\resumes"
    pdf_files = glob.glob(os.path.join(resumes_dir, "resume_*.pdf"))
    if len(pdf_files) < 5:
        print(f"Error: Need at least 5 PDF files, found {len(pdf_files)}")
        return
        
    # We will pick 5 different PDF resumes from the directory
    # Standard profile configurations representing different study branches
    test_cases = [
        {"name": "Alice Frontend Dev", "email": "alice_front@stanford.edu", "dept": "Computer Science (Frontend UI)", "cgpa": 8.8, "pdf": pdf_files[0]},
        {"name": "Bob Data Scientist", "email": "bob_ds@stanford.edu", "dept": "Data Science & AI", "cgpa": 9.2, "pdf": pdf_files[1]},
        {"name": "Charlie Cloud Ops", "email": "charlie_ops@stanford.edu", "dept": "DevOps & Cloud Computing", "cgpa": 7.5, "pdf": pdf_files[2]},
        {"name": "Diana Cyber Security", "email": "diana_sec@stanford.edu", "dept": "Cybersecurity & Networks", "cgpa": 8.1, "pdf": pdf_files[3]},
        {"name": "Ethan Systems Engineer", "email": "ethan_sys@stanford.edu", "dept": "Computer Engineering (Backend)", "cgpa": 9.5, "pdf": pdf_files[4]}
    ]
    
    results = []
    
    for i, tc in enumerate(test_cases, 1):
        print(f"\n--- Running Test Case {i}: {tc['name']} ---")
        try:
            print("Authenticating...")
            token = register_and_login(tc["name"], tc["email"], "password123")
            
            print(f"Setting up profile with department: {tc['dept']}...")
            try:
                create_profile(token, "Stanford University", tc["dept"], 3, tc["cgpa"], "9876543210")
            except Exception as e:
                if "Profile already exists" in str(e):
                    print("Profile already exists, proceeding...")
                else:
                    raise e
            
            print(f"Uploading resume: {os.path.basename(tc['pdf'])}...")
            upload_resume(token, tc["pdf"])
            
            print("Requesting AI recommendations...")
            recs = get_recommendations(token)
            
            print(f"Successfully received {len(recs)} recommendations!")
            top_3 = recs[:3]
            for idx, r in enumerate(top_3, 1):
                score = r.get('finalScore') or r.get('final_score')
                score_str = f"{score:.4f}" if score is not None else "N/A"
                print(f"  #{idx} Title: {r.get('title')} | Company: {r.get('company')} | Score: {score_str}")
                print(f"     Matched Skills: {r.get('matchedSkills')}")
                
            results.append({
                "test_case": i,
                "name": tc["name"],
                "dept": tc["dept"],
                "resume_file": os.path.basename(tc["pdf"]),
                "recs_count": len(recs),
                "top_recommendations": [
                    {
                        "title": r.get("title"),
                        "company": r.get("company"),
                        "score": r.get("finalScore") or r.get("final_score"),
                        "matched_skills": r.get("matchedSkills"),
                        "missing_skills": r.get("missingSkills")
                    } for r in top_3
                ]
            })
        except Exception as e:
            print(f"Test case {i} failed: {e}")
            
    print("\n=== VERIFICATION RESULTS JSON ===")
    print(json.dumps(results, indent=2))
    
    # Save results as JSON for the report
    with open(r"C:\Users\SUDHAN D\.gemini\antigravity\brain\38c173ec-aa21-4eed-97d2-325c838f8657\scratch\five_tests_results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
