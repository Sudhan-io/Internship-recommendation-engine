import urllib.request
import json

def list_files():
    url = "https://huggingface.co/api/datasets/xanderios/linkedin-job-postings"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode("utf-8"))
            print("Keys:", data.keys())
            if "siblings" in data:
                print("Siblings:", data["siblings"])
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    list_files()
