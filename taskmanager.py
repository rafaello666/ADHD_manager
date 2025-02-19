import sqlite3
from datetime import datetime

class TaskManager:
    def __init__(self, db_path="tasks.db"):
        """
        Inicjalizuje połączenie z bazą SQLite.
        :param db_path: Ścieżka do pliku bazy (domyślnie "tasks.db")
        """
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row  # Umożliwia dostęp do wyników jako słowniki
        self._create_table()

    def _create_table(self):
        """Tworzy tabelę 'tasks' jeśli nie istnieje."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            due_date TEXT NOT NULL,
            priority_weight INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor = self.connection.cursor()
        cursor.execute(create_table_query)
        self.connection.commit()

    def add_task(self, title, due_date, priority_weight):
        """
        Dodaje nowe zadanie do bazy.
        :param title: Tytuł zadania.
        :param due_date: Termin wykonania (w formacie 'YYYY-MM-DD').
        :param priority_weight: Waga priorytetu (liczba całkowita, wyższa wartość oznacza większą ważność).
        :return: ID nowo dodanego zadania.
        """
        query = "INSERT INTO tasks (title, due_date, priority_weight) VALUES (?, ?, ?)"
        cursor = self.connection.cursor()
        cursor.execute(query, (title, due_date, priority_weight))
        self.connection.commit()
        return cursor.lastrowid

    def get_all_tasks(self):
        """
        Pobiera wszystkie zadania z bazy.
        :return: Lista słowników z danymi zadań.
        """
        query = "SELECT id, title, due_date, priority_weight FROM tasks"
        cursor = self.connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        tasks = []
        for row in rows:
            tasks.append({
                "id": row["id"],
                "title": row["title"],
                "due_date": row["due_date"],
                "priority_weight": row["priority_weight"]
            })
        return tasks

    def update_task(self, task_id, title, due_date, priority_weight):
        """
        Aktualizuje dane zadania o podanym ID.
        :param task_id: ID zadania.
        :param title: Nowy tytuł.
        :param due_date: Nowy termin wykonania (YYYY-MM-DD).
        :param priority_weight: Nowa waga priorytetu.
        :return: Liczba zmodyfikowanych wierszy (1, jeśli operacja się powiodła, 0, jeśli zadanie nie istnieje).
        """
        query = "UPDATE tasks SET title=?, due_date=?, priority_weight=?, updated_at=CURRENT_TIMESTAMP WHERE id=?"
        cursor = self.connection.cursor()
        cursor.execute(query, (title, due_date, priority_weight, task_id))
        self.connection.commit()
        return cursor.rowcount

    def delete_task(self, task_id):
        """
        Usuwa zadanie o podanym ID.
        :param task_id: ID zadania.
        :return: Liczba usuniętych wierszy (1, jeśli operacja się powiodła, 0, jeśli zadanie nie istnieje).
        """
        query = "DELETE FROM tasks WHERE id=?"
        cursor = self.connection.cursor()
        cursor.execute(query, (task_id,))
        self.connection.commit()
        return cursor.rowcount

    def close(self):
        """Zamyka połączenie z bazą danych."""
        self.connection.close()

# Przykładowe użycie (można je usunąć, gdy integrujemy z serwerem Flask):
if __name__ == "__main__":
    tm = TaskManager()
    new_id = tm.add_task("Testowe zadanie", "2025-02-15", 5)
    print("Dodano zadanie o ID:", new_id)
    tasks = tm.get_all_tasks()
    print("Aktualna lista zadań:")
    for task in tasks:
        print(task)
    tm.close()
