import sys
sys.path.append(r"d:\PROJECTS\Internship-recommendation-engine\ai-service")
from resume.parser import ResumeParser
from nlp.repository import SkillsRepository

def main():
    repo = SkillsRepository()
    parser = ResumeParser(repo)
    text = "Experienced software engineer with skills in Python, Java, and Docker."
    print("Testing parser...")
    res = parser.parse(text)
    print("Parsed result:", res)

if __name__ == "__main__":
    main()
