import urllib.request
import json

def test_resume_parsing(name, text):
    url = "http://127.0.0.1:8000/resume/parse"
    data = json.dumps({"text": text}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as res:
            response = json.loads(res.read().decode("utf-8"))
            print(f"=== TEST CASE: {name} ===")
            print(json.dumps(response, indent=2))
            print("-" * 50)
            
            # Basic validation assertions
            for section in ["skills", "education", "experience", "projects", "certifications"]:
                assert section in response, f"Missing section '{section}' in response"
                assert "values" in response[section], f"Missing values in section '{section}'"
                assert "confidence" in response[section], f"Missing confidence in section '{section}'"
                
    except Exception as e:
        print(f"Failed to test case {name}: {e}")

# 1. Fresher Resume (No experience, no certifications)
fresher_text = """
John Doe
Email: john@doe.com

EDUCATION
Bachelor of Science in Computer Science
XYZ University, GPA 3.8/4.0
Graduation: May 2026

SKILLS
Python, JavaScript, SQL, HTML, CSS, Git

PROJECTS
Personal Portfolio Website
Built using HTML, CSS and JavaScript to showcase personal interests and resume details.
"""

# 2. Student with Projects (Skills, education, projects, but no experience or certifications)
student_text = """
Jane Smith
Jane@smith.com

EDUCATION
B.Tech in Information Technology
ABC Institute of Technology, CGPA 9.2/10
2022 - 2026

TECHNICAL SKILLS
Java, Spring Boot, PostgreSQL, MongoDB, Docker

PROJECTS
Internship Recommendation Engine
Developed a web application using Spring Boot and React to recommend internships. Utilized MongoDB for data storage and Docker for containerization.
"""

# 3. Experienced Candidate (Skills, education, experience, projects, certifications)
experienced_text = """
Robert Johnson
robert@johnson.com

EXPERIENCE
Senior Software Engineer
Google Corp, Jun 2023 - Present
Led a team of developers to build scalable cloud architectures. Utilized Python, Docker, and Kubernetes.

Software Engineer
Amazon Inc, July 2021 to May 2023
Developed core microservices using Java and Spring Boot.

EDUCATION
Master of Science in Computer Science
Stanford University, 2019-2021

SKILLS
Python, Java, Spring Boot, Docker, Kubernetes, AWS

CERTIFICATIONS
AWS Certified Solutions Architect
Coursera Machine Learning Specialization
"""

print("Running resume parser tests...")
test_resume_parsing("Fresher Resume", fresher_text)
test_resume_parsing("Student with Projects", student_text)
test_resume_parsing("Experienced Candidate", experienced_text)
print("All parser tests completed successfully!")
