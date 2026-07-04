DROP DATABASE IF EXISTS internship_recommendation_engine;

CREATE DATABASE internship_recommendation_engine;

USE internship_recommendation_engine;
-- =============================================
-- USERS
-- =============================================

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,

    full_name VARCHAR(100) NOT NULL,

    email VARCHAR(100) NOT NULL UNIQUE,

    password_hash VARCHAR(255) NOT NULL,

    role ENUM('STUDENT','ADMIN')
        DEFAULT 'STUDENT',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- =============================================
-- STUDENT PROFILES
-- =============================================

CREATE TABLE student_profiles (

    profile_id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL UNIQUE,

    college_name VARCHAR(150) NOT NULL,

    department VARCHAR(100) NOT NULL,

    year_of_study TINYINT NOT NULL,

    cgpa DECIMAL(3,2),

    phone VARCHAR(15),

    linkedin_url VARCHAR(255),

    github_url VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE

);
-- =============================================
-- RESUMES
-- =============================================

CREATE TABLE resumes (

    resume_id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    file_name VARCHAR(255) NOT NULL,

    file_path VARCHAR(500) NOT NULL,

    file_size BIGINT,

    mime_type VARCHAR(100),

    extracted_text LONGTEXT,

    processing_status VARCHAR(50) DEFAULT 'UPLOADED',

    embedding_generated BOOLEAN DEFAULT FALSE,

    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE

);
-- =============================================
-- SKILLS
-- =============================================

CREATE TABLE skills (

    skill_id INT AUTO_INCREMENT PRIMARY KEY,

    skill_name VARCHAR(100) NOT NULL UNIQUE

);
-- =============================================
-- INTERNSHIPS
-- =============================================

CREATE TABLE internships (

    internship_id INT AUTO_INCREMENT PRIMARY KEY,

    title VARCHAR(150) NOT NULL,

    company_name VARCHAR(150) NOT NULL,

    location VARCHAR(100),

    mode ENUM('ONLINE','OFFLINE','HYBRID'),

    duration VARCHAR(50),

    stipend VARCHAR(50),

    description TEXT,

    eligibility TEXT,

    apply_url VARCHAR(255),

    application_deadline DATE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);
-- =============================================
-- INTERNSHIP SKILLS
-- =============================================

CREATE TABLE internship_skills (

    internship_skill_id INT AUTO_INCREMENT PRIMARY KEY,

    internship_id INT NOT NULL,

    skill_id INT NOT NULL,

    FOREIGN KEY (internship_id)
        REFERENCES internships(internship_id)
        ON DELETE CASCADE,

    FOREIGN KEY (skill_id)
        REFERENCES skills(skill_id)
        ON DELETE CASCADE,

    UNIQUE (internship_id, skill_id)

);
-- =============================================
-- APPLICATIONS
-- =============================================

CREATE TABLE applications (

    application_id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    internship_id INT NOT NULL,

    status ENUM('APPLIED','SHORTLISTED','REJECTED','ACCEPTED')
        DEFAULT 'APPLIED',

    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    FOREIGN KEY (internship_id)
        REFERENCES internships(internship_id)
        ON DELETE CASCADE

);
-- =============================================
-- RECOMMENDATIONS
-- =============================================

CREATE TABLE recommendations (

    recommendation_id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    internship_id INT NOT NULL,

    match_score DECIMAL(5,2) NOT NULL,

    recommended_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    FOREIGN KEY (internship_id)
        REFERENCES internships(internship_id)
        ON DELETE CASCADE

);