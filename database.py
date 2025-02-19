import os
import sqlite3
import pymysql
from dotenv import load_dotenv

load_dotenv()

DB_TYPE = os.getenv("DB_TYPE", "sqlite")

if DB_TYPE == "mysql":
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DB = os.getenv("MYSQL_DB")
    
    def get_db_connection():
        return pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            cursorclass=pymysql.cursors.DictCursor
        )
else:
    SQLITE_DB = os.getenv("SQLITE_DB", "adhd_manager.db")
    
    def get_db_connection():
        conn = sqlite3.connect(SQLITE_DB)
        conn.row_factory = sqlite3.Row
        return conn
