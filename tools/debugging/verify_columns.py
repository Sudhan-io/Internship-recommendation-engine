import mysql.connector

config = {
    "host": "localhost",
    "user": "root",
    "password": "Sudh@007",
    "database": "internship_recommendation_engine"
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    for table in ["skills", "internship_skills"]:
        cursor.execute(f"DESCRIBE {table}")
        cols = cursor.fetchall()
        print(f"=== Column details for table '{table}' ===")
        for col in cols:
            print(col)
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Failed to describe: {e}")
