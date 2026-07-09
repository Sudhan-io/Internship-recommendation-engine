-- ====================================================================
-- InternMatch Database Seed Script (For Demonstration & Testing Only)
-- Run this script on your MySQL database to insert sample seed data.
-- ====================================================================

USE internship_recommendation_engine;

-- 1. Insert Sample Skills
INSERT INTO skills (skill_id, skill_name) VALUES
(1, 'Python'),
(2, 'SQL'),
(3, 'Java'),
(4, 'React'),
(5, 'JavaScript'),
(6, 'Machine Learning'),
(7, 'Spring Boot'),
(8, 'Git'),
(9, 'Docker'),
(10, 'HTML'),
(11, 'CSS'),
(12, 'C++')
ON DUPLICATE KEY UPDATE skill_name=VALUES(skill_name);

-- 2. Insert Sample Internships
INSERT INTO internships (internship_id, title, company_name, location, mode, duration, stipend, description, eligibility, apply_url, application_deadline) VALUES
(1, 'Frontend Developer Intern', 'TechCorp Inc.', 'Remote', 'ONLINE', '3 Months', '$2000/Month', 'Build and optimize modern user interfaces using React, JavaScript, and HTML/CSS.', 'Enrolled in Computer Science or related degree. Basic HTML/CSS/React skills.', 'https://techcorp.com/careers/frontend-intern', '2026-08-31'),
(2, 'Data Science Intern', 'DataSolutions Ltd.', 'San Francisco, CA', 'HYBRID', '6 Months', '$2500/Month', 'Analyze complex datasets, build machine learning models, and write analytical queries.', 'Good knowledge of Python and SQL. Experience with Pandas/NumPy.', 'https://datasolutions.com/careers/ds-intern', '2026-09-15'),
(3, 'Backend Engineer Intern', 'DevFlow Solutions', 'Seattle, WA', 'OFFLINE', '4 Months', '$2200/Month', 'Develop clean, scalable microservices using Spring Boot and relational databases.', 'Proficiency in Java. Familiarity with Spring Boot and SQL.', 'https://devflow.io/careers/backend-intern', '2026-08-15'),
(4, 'Software Developer Intern', 'CodeSoft Systems', 'Remote', 'ONLINE', '3 Months', '$1800/Month', 'Develop applications using modern tools and container environments (Docker, Git).', 'Knowledge of C++, Git and fundamental container concepts.', 'https://codesoft.com/careers/sde-intern', '2026-10-01')
ON DUPLICATE KEY UPDATE title=VALUES(title), company_name=VALUES(company_name);

-- 3. Insert Internship-Skill Mappings
INSERT INTO internship_skills (internship_id, skill_id) VALUES
-- Frontend Developer Intern -> React, JavaScript, HTML, CSS
(1, 4),
(1, 5),
(1, 10),
(1, 11),
-- Data Science Intern -> Python, SQL, Machine Learning
(2, 1),
(2, 2),
(2, 6),
-- Backend Engineer Intern -> Java, Spring Boot, SQL, Git
(3, 3),
(3, 7),
(3, 2),
(3, 8),
-- Software Developer Intern -> C++, Git, Docker
(4, 12),
(4, 8),
(4, 9)
ON DUPLICATE KEY UPDATE internship_id=VALUES(internship_id), skill_id=VALUES(skill_id);
