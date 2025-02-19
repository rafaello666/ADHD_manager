import pymysql
from pymysql.cursors import DictCursor

class TaskManager:
    def __init__(self, host='server2458128.home.pl', user='39129096_adhd_manager', password='Eminem@92', db='39129096_adhd_manager'):
        """
        Inicjalizacja połączenia z bazą danych MySQL.
        Parametry:
          host - server2458128.home.pl
          user -  39129096_adhd_manager
          password - Eminem@92
          db - 39129096_adhd_manager

        """
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.db,
            charset='utf8mb4',
            cursorclass=DictCursor,
            autocommit=False
        )
        self._create_table()

    def _create_table(self):
        """Tworzy tabelę 'tasks' w bazie, jeśli nie istnieje."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            due_date DATE NOT NULL,
            priority_weight INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """
        with self.connection.cursor() as cursor:
            cursor.execute(create_table_query)
        self.connection.commit()

    def add_task(self, title, due_date, priority_weight):
        """
        Dodaje nowe zadanie do bazy.
        :param title: Tytuł zadania.
        :param due_date: Termin wykonania (format YYYY-MM-DD).
        :param priority_weight: Waga priorytetu (wartość całkowita, wyższa oznacza większą ważność).
        :return: ID nowo utworzonego zadania.
        """
        query = "INSERT INTO tasks (title, due_date, priority_weight) VALUES (%s, %s, %s)"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (title, due_date, priority_weight))
            new_id = cursor.lastrowid
        self.connection.commit()
        return new_id

    def get_all_tasks(self):
        """
        Pobiera wszystkie zadania z bazy.
        :return: Lista słowników reprezentujących zadania.
        """
        query = "SELECT id, title, due_date, priority_weight FROM tasks"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            tasks = cursor.fetchall()
        return tasks

    def update_task(self, task_id, title, due_date, priority_weight):
        """
        Aktualizuje dane zadania o podanym ID.
        :param task_id: ID zadania.
        :param title: Nowy tytuł.
        :param due_date: Nowy termin wykonania (YYYY-MM-DD).
        :param priority_weight: Nowa waga priorytetu.
        :return: Liczba zmodyfikowanych wierszy (1 jeśli operacja się powiodła, 0 jeśli zadanie nie zostało znalezione).
        """
        query = "UPDATE tasks SET title=%s, due_date=%s, priority_weight=%s WHERE id=%s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (title, due_date, priority_weight, task_id))
        self.connection.commit()
        return cursor.rowcount

    def delete_task(self, task_id):
        """
        Usuwa zadanie o podanym ID.
        :param task_id: ID zadania do usunięcia.
        :return: Liczba usuniętych wierszy (1 jeśli operacja się powiodła, 0 jeśli zadanie nie istnieje).
        """
        query = "DELETE FROM tasks WHERE id=%s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (task_id,))
        self.connection.commit()
        return cursor.rowcount

    def close(self):
        """Zamyka połączenie z bazą danych."""
        self.connection.close()
