import mysql.connector

conn = mysql.connector.connect(
        host='localhost',  # Używamy adresu IP
        user='39129096_adhd_manager',
        password='Eminem@92',
        database='39129096_adhd_manager',
        port=3380 
    )
    
print("Połączono!") if conn.is_connected() else print("Błąd połączenia.")
