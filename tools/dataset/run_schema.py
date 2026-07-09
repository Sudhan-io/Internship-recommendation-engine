import mysql.connector
import re

def run_schema():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sudh@007"
    )
    cursor = conn.cursor()
    
    with open(r"d:\PROJECTS\Internship-recommendation-engine\database\schema.sql", "r", encoding="utf-8") as f:
        sql = f.read()
        
    # Remove SQL comments
    sql = re.sub(r'--.*?\n', '\n', sql)
    
    # Split by semicolon
    queries = sql.split(";")
    for q in queries:
        q = q.strip()
        if q:
            print(f"Executing: {q[:80]}...")
            try:
                cursor.execute(q)
            except Exception as e:
                print(f"Error: {e}")
                
    conn.commit()
    cursor.close()
    conn.close()
    print("Schema executed successfully!")

if __name__ == "__main__":
    run_schema()
