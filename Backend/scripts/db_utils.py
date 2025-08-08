import mysql.connector
from config import DB_CONFIG

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def insert_raw_data(company_id, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO company_data (company_id, json_data) VALUES (%s, %s)", (company_id, str(data)))
    conn.commit()
    conn.close()

def insert_analysis(company_id, pros, cons):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ml_results (company_id, pros, cons) VALUES (%s, %s, %s)", (company_id, '\n'.join(pros), '\n'.join(cons)))
    conn.commit()
    conn.close()