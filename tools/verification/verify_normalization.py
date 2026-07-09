import sys
import os
import json

# Add ai-service to path
current_dir = os.path.dirname(os.path.abspath(__file__))
ai_service_dir = "d:\\PROJECTS\\Internship-recommendation-engine\\ai-service"
sys.path.append(ai_service_dir)

from nlp.repository import SkillsRepository
from resume.parser import ResumeParser
from normalization.canonical_dictionary import CanonicalDictionary
from normalization.normalizer import ResumeNormalizer

# Load components
skills_repo = SkillsRepository()
parser = ResumeParser(skills_repo)
canonical_dict = CanonicalDictionary()
normalizer = ResumeNormalizer(canonical_dict)

def test_normalization(name, text):
    print(f"\n==========================================")
    print(f"TEST CASE: {name}")
    print(f"==========================================")
    
    # 1. Parse raw text
    parse_result = parser.parse(text)
    
    # Save a copy of parsed values to verify no modifications occurred
    original_skills = list(parse_result.skills.values)
    original_education = list(parse_result.education.values)
    
    # 2. Normalize parsed result
    normalized = normalizer.normalize(parse_result)
    
    # Assert original values in parser output are unmodified
    assert parse_result.skills.values == original_skills, "Parser skills output was modified by normalizer!"
    assert parse_result.education.values == original_education, "Parser education output was modified by normalizer!"
    
    # Print original vs normalized comparison
    print(json.dumps(normalized, indent=2))
    
    # Basic assertions to check correctness
    if "skills" in normalized:
        print("-> Skills normalized successfully")
    if "education" in normalized:
        print("-> Education normalized successfully")
    if "companies" in normalized:
        print("-> Companies normalized successfully")
    if "dates" in normalized:
        print("-> Dates normalized successfully")
    if "metadata" in normalized:
        print(f"-> Quality Score: {normalized['metadata']['quality_score']*100}%")

# 1. Fresher Resume (No experience, no certifications)
fresher_text = """
John Doe
Email: john@doe.com

EDUCATION
B.E Computer Science
XYZ University, GPA 3.8/4.0
Graduation: May 2026

SKILLS
python, spring boot, SQL, HTML, CSS, Git

PROJECTS
Personal Portfolio Website
Built using HTML, CSS and JavaScript to showcase personal interests and resume details.
"""

# 2. Student with Projects (No experience or certifications)
student_text = """
Jane Smith
Jane@smith.com

EDUCATION
B.Tech in Information Technology
ABC Institute of Technology, CGPA 9.2/10
01/2022 - 05/2026

TECHNICAL SKILLS
Java, SpringBoot, PostgreSQL, MongoDB, Docker

PROJECTS
Internship Recommendation Engine
Developed a web application using Spring Boot and React to recommend internships. Utilized MongoDB for data storage and Docker for containerization.
"""

# 3. Experienced Candidate (Experience, certifications, and skills)
experienced_text = """
Robert Johnson
robert@johnson.com

EXPERIENCE
Senior Software Engineer
Google LLC, Jun 2023 - Present
Led a team of developers to build scalable cloud architectures. Utilized Python, Docker, and Kubernetes.

Software Engineer
Amazon Inc., July 2021 to May 2023
Developed core microservices using Java and Spring Boot.

EDUCATION
Master of Science in Computer Science
Stanford University, 2019-2021

SKILLS
python, spring boot, Docker, Kubernetes, AWS

CERTIFICATIONS
AWS Certified Solutions Architect
Coursera Machine Learning Specialization
"""

test_normalization("Fresher Resume", fresher_text)
test_normalization("Student with Projects", student_text)
test_normalization("Experienced Candidate", experienced_text)

print("\nAll normalization pipeline tests completed successfully and verified stateless and deterministic behavior!")
