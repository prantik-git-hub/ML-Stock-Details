import os
import mysql.connector


# API configuration
API_KEY = 'ghfkffu6378382826hhdjgk'
BASE_URL = 'https://bluemutualfund.in/server/api/company.php'

# MySQL Database configuration (as a valid Python dictionary)
DB_CONFIG = {
    'host': os.environ.get("MYSQL_HOST", "localhost"),
    'user': os.environ.get("MYSQL_USER", "root"),
    'password': os.environ.get("MYSQL_PASSWORD", ""),
    'database': os.environ.get("MYSQL_DATABASE", "stock_market"),
    'port': int(os.environ.get("MYSQL_PORT", 3306)),
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['MYSQL_HOST'],
            user=DB_CONFIG['MYSQL_USER'],
            password=DB_CONFIG['MYSQL_PASSWORD'],
            database=DB_CONFIG['MYSQL_DB']
        )
        print("Connected to database")
        return conn
    except mysql.connector.Error as err:
        print("Database connection error:", err)
        return None
    # Example configuration
DEBUG = True
SECRET_KEY = 'your-secret-key'

