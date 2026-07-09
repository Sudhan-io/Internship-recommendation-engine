import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Sudh@007",
    "database": "internship_recommendation_engine"
}

def update_schema():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    print("Dropping old recommendations table if exists...")
    cursor.execute("DROP TABLE IF EXISTS recommendations")
    
    print("Dropping recommendation_batches table if exists...")
    cursor.execute("DROP TABLE IF EXISTS recommendation_batches")

    print("Checking resumes structure:")
    cursor.execute("DESCRIBE resumes")
    for r in cursor.fetchall():
        print(r)
        
    print("Checking users structure:")
    cursor.execute("DESCRIBE users")
    for r in cursor.fetchall():
        print(r)
    
    print("Creating recommendation_batches table...")
    cursor.execute("""
        CREATE TABLE recommendation_batches (
            batch_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            resume_id BIGINT NOT NULL,
            model_name VARCHAR(100) NOT NULL,
            recommendation_count INT NOT NULL,
            generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (resume_id) REFERENCES resumes(resume_id) ON DELETE CASCADE
        )
    """)
    
    print("Creating recommendations table...")
    cursor.execute("""
        CREATE TABLE recommendations (
            recommendation_id INT AUTO_INCREMENT PRIMARY KEY,
            batch_id INT NOT NULL,
            user_id INT NOT NULL,
            internship_id INT NOT NULL,
            final_score DECIMAL(5,4) NOT NULL,
            semantic_score DECIMAL(5,4) NOT NULL,
            skill_score DECIMAL(5,4) NOT NULL,
            education_score DECIMAL(5,4) NOT NULL,
            experience_score DECIMAL(5,4) NOT NULL,
            eligibility_score DECIMAL(5,4) NOT NULL,
            explanation_text TEXT,
            matched_skills TEXT,
            missing_skills TEXT,
            FOREIGN KEY (batch_id) REFERENCES recommendation_batches(batch_id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (internship_id) REFERENCES internships(internship_id) ON DELETE CASCADE
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Database schema updated successfully!")

if __name__ == "__main__":
    update_schema()
