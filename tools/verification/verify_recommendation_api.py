import urllib.request
import json

def test_recommendation_api():
    url = "http://127.0.0.1:8000/recommendations/generate"
    req_data = {
        "resume_text": "John Doe. Skills: Python, SQL. Education: Bachelor of Engineering."
    }
    
    headers = {"Content-Type": "application/json"}
    data_bytes = json.dumps(req_data).encode("utf-8")
    
    req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")
    try:
        print("Calling /recommendation/generate API...")
        with urllib.request.urlopen(req) as res:
            response = json.loads(res.read().decode("utf-8"))
            print("=== Ingestion Endpoint Response ===")
            print(json.dumps(response, indent=2)[:1000] + "\n... truncated ...")
            assert response["status"] == "success"
            print("-> API response verified successfully!")
    except Exception as e:
        print(f"Failed to test dataset import: {e}")

test_recommendation_api()
