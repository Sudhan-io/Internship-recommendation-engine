import mysql.connector

# insert_admin.py
# Python script to insert an admin user into the DB

def insert_admin():
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "password",
        "database": "recommendation_db"
    }
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (full_name, email, password, role) VALUES ('Admin User', 'admin@example.com', 'admin123', 'ADMIN')")
        conn.commit()
        print("Admin user inserted successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    insert_admin()
