import pymysql

try:
    conn = pymysql.connect(
        host='127.0.0.1',  # zamiast 'localhost'
        user='39129096_adhd_manager',
        password='Eminem@92',
        db='39129096_adhd_manager'
    )
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    results = cursor.fetchall()
    
    for row in results:
        print(row)
    
    cursor.close()
    conn.close()
    print("Operacja zakończona sukcesem!")
    
except Exception as e:
    print("Błąd połączenia lub operacji:", e)
