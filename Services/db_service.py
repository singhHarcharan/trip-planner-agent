import os
import psycopg2
import sys
from dotenv import load_dotenv
from datetime import date

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

def get_holidays_dates(employee_id):
    """
    Returns upcoming holidays for the given employee_id from today's date onward.
    """
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        today = date.today()

        query = """
            SELECT holidays FROM holidays_table
            WHERE employee_id = %s AND holidays >= %s
            ORDER BY holidays ASC
        """
        cursor.execute(query, (employee_id, today))
        results = cursor.fetchall()

        return [row[0].isoformat() for row in results]

    except Exception as e:
        print("❌ Error in get_availability():", e, sys.exc_info())
        return []

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
