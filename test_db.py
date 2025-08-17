import os
import psycopg2
import sys
from dotenv import load_dotenv

load_dotenv()
EMPLOYEE_ID = 1001  # Harcharanpreet's ID
cursor = None
conn = None
dbname = os.getenv("DB_NAME")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")


DB_CONFIG = {
    "dbname": dbname,
    "user": username,
    "password": password,
    "host": host,
    "port": port
}
try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    print("✅ Connected to the database!")

    # Query holidays for the given employee_id
    cursor.execute("""
        SELECT holidays FROM holidays_table
        WHERE employee_id = %s
    """, (EMPLOYEE_ID,))

    results = cursor.fetchall()
    for row in results:
        print("Holiday:", row[0])

except Exception as e:
    print("❌ Error:", e, sys.exc_info())

finally:
    if cursor is not None:
        cursor.close()
    if conn is not None:
        conn.close()
