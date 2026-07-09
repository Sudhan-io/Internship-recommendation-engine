import urllib.request

def check_columns():
    url = "https://raw.githubusercontent.com/prajaktawaghmare13/industry-skill-insights/main/data/job_postings.csv"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as res:
        # Read first 1000 bytes
        content = res.read(2000).decode("utf-8")
        print("First 2000 bytes:")
        print(content)

if __name__ == "__main__":
    check_columns()
