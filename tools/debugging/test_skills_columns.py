import urllib.request

def check_skills_columns():
    url = "https://raw.githubusercontent.com/prajaktawaghmare13/industry-skill-insights/main/data/job_skills.csv"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as res:
        content = res.read(2000).decode("utf-8")
        print("First 2000 bytes of job_skills.csv:")
        print(content)

if __name__ == "__main__":
    check_skills_columns()
