import mysql.connector
import os
import re

def seed():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sudh@007"
    )
    cursor = conn.cursor()
    
    # Read seed_data.sql
    seed_file_path = r"d:\PROJECTS\Internship-recommendation-engine\database\seed_data.sql"
    with open(seed_file_path, "r", encoding="utf-8") as f:
        sql_content = f.read()
    
    # Remove comments
    sql_content = re.sub(r'--.*?\n', '\n', sql_content)
    
    # Split queries by semicolon (avoiding semicolons inside quotes if possible)
    # Simple split is usually sufficient for simple SQL scripts.
    queries = sql_content.split(";")
    
    for query in queries:
        query_str = query.strip()
        if not query_str:
            continue
        try:
            print(f"Executing: {query_str[:80]}...")
            cursor.execute(query_str)
        except Exception as e:
            print(f"Error executing query: {e}")
            
    conn.commit()
    cursor.close()
    conn.close()
    print("Database seeding completed successfully.")

if __name__ == "__main__":
    seed()
