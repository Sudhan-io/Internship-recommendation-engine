# inspect_resumes.py
import os
import glob

def inspect():
    resumes_dir = r"d:\PROJECTS\Internship-recommendation-engine\backend\uploads\resumes"
    pdfs = glob.glob(os.path.join(resumes_dir, "*.pdf"))
    print(f"Found {len(pdfs)} resumes in {resumes_dir}")
    for p in pdfs:
        print(f" - {os.path.basename(p)}")

if __name__ == "__main__":
    inspect()
