import mysql.connector

def seed():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sudh@007",
        database="internship_recommendation_engine"
    )
    cursor = conn.cursor()
    
    # 12 clean internships matching Spring Boot Entity
    internships = [
        (1, "Frontend Developer Intern", "TechCorp Inc.", "Remote", "ONLINE", "3 Months", "$2000/Month", "Build and optimize modern user interfaces using React, JavaScript, and HTML/CSS.", "React, JavaScript, HTML, CSS", "Enrolled in Computer Science or related degree. Basic HTML/CSS/React skills.", "https://techcorp.com/careers/frontend-intern"),
        (2, "Data Science Intern", "DataSolutions Ltd.", "San Francisco, CA", "HYBRID", "6 Months", "$2500/Month", "Analyze complex datasets, build machine learning models, and write analytical queries.", "Python, SQL, Machine Learning", "Good knowledge of Python and SQL. Experience with Pandas/NumPy.", "https://datasolutions.com/careers/ds-intern"),
        (3, "Backend Engineer Intern", "DevFlow Solutions", "Seattle, WA", "OFFLINE", "4 Months", "$2200/Month", "Develop clean, scalable microservices using Spring Boot and relational databases.", "Java, Spring Boot, SQL, Git", "Proficiency in Java. Familiarity with Spring Boot and SQL.", "https://devflow.io/careers/backend-intern"),
        (4, "Software Developer Intern", "CodeSoft Systems", "Remote", "ONLINE", "3 Months", "$1800/Month", "Develop applications using modern tools and container environments (Docker, Git).", "C++, Git, Docker", "Knowledge of C++, Git and fundamental container concepts.", "https://codesoft.com/careers/sde-intern"),
        (5, "Java Developer Associate", "Amazon", "Seattle WA", "HYBRID", "6 Months", "$3000/Month", "Build scalable backend with Java and Spring Boot.", "Java, Spring Boot", "Enrolled in Computer Science or related.", "https://careers.amazon.com/jobs/8"),
        (6, "Senior Software Architect", "Netflix", "Los Gatos CA", "HYBRID", "12 Months", "$10000/Month", "Lead architectural design for streaming engine.", "AWS, Java", "BS/MS in Computer Science.", "https://careers.netflix.com/jobs/5"),
        (7, "Full Stack Trainee", "Microsoft", "Redmond WA", "ONLINE", "6 Months", "$4000/Month", "Develop enterprise apps using Spring Boot and SQL.", "SQL, Spring Boot", "Computer Science background.", "https://careers.microsoft.com/jobs/4"),
        (8, "Software Engineer Intern", "Google", "Mountain View CA", "HYBRID", "3 Months", "$5000/Month", "Work with Google's search team using Python and C++.", "C++, Python", "Enrolled in BS/MS/PhD in Computer Science.", "https://careers.google.com/jobs/1"),
        (9, "Data Analyst Intern", "Amazon", "Seattle WA", "ONLINE", "3 Months", "$2500/Month", "Learn big data analytics using SQL and Python.", "Python, SQL", "Math, Statistics or CS major.", "https://careers.amazon.com/jobs/2"),
        (10, "Cloud Engineer Intern", "Netflix", "Los Gatos CA", "ONLINE", "6 Months", "$6000/Month", "Deploy microservices to AWS cloud.", "AWS, Docker", "Familiarity with cloud platforms and containers.", "https://careers.netflix.com/jobs/7"),
        (11, "Associate Frontend Developer", "Meta", "Menlo Park CA", "OFFLINE", "6 Months", "$4500/Month", "Build user interfaces with React and JavaScript.", "JavaScript, React", "React developer experience.", "https://careers.meta.com/jobs/3"),
        (12, "Data Scientist Graduate", "Apple", "Cupertino CA", "OFFLINE", "6 Months", "$5500/Month", "Work on core machine learning models with PyTorch.", "PyTorch, Python", "Graduate in Machine Learning or Data Science.", "https://careers.apple.com/jobs/6")
    ]
    
    insert_query = """
    INSERT INTO internships (internship_id, title, company, location, mode, duration, stipend, description, required_skills, eligibility, apply_url)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE title=VALUES(title), company=VALUES(company)
    """
    
    for item in internships:
        cursor.execute(insert_query, item)
        
    conn.commit()
    cursor.close()
    conn.close()
    print("Seeded 12 internships successfully!")

if __name__ == "__main__":
    seed()
