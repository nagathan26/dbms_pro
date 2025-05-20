
import mysql.connector
from config import Config

def get_db_connection():
    """Create and return a new database connection"""
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )