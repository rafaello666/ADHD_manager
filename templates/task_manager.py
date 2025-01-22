# tasks_manager.py

import json
import os
from datetime import datetime

TASKS_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")

def load_tasks():
    """Wczytuje listę zadań z pliku JSON."""
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    """Zapisuje listę zadań do pliku JSON."""
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

def get_all_tasks():
    """Zwraca wszystkie zadania."""
    return load_tasks()

def add_quick_task(title, deadline=None, cyclic_type=None):
    """
    Dodaje zadanie z minimalnym zestawem informacji:
    - title (str)
    - deadline (str, np. '2025-02-10 15:00')
    - cyclic_type (None / 'daily' / 'weekly' itp.)
    """
    tasks = load_tasks()
    new_task = {
        "id": generate_task_id(tasks),
        "title": title,
        "deadline": deadline,
        "cyclic_type": cyclic_type,  # daily, weekly, monthly...
        "done": False,               # czy ukończone
        "created_at": datetime.now().isoformat()
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return new_task

def generate_task_id(tasks):
    """Prosty generator ID (np. max istniejącego + 1)."""
    if not tasks:
        return 1
    return max(task.get("id", 0) for task in tasks) + 1

def reset_cyclic_tasks():
    """
    Przegląda listę zadań i jeżeli zadanie ma ustawione 'cyclic_type' (np. daily),
    resetuje jego status (done=False) jeśli trzeba.
    Warunek: 
      - Możesz dopasować, by resetować TYLKO raz dziennie 
        (sprawdzać, czy jest data 'last_reset' etc.).
      - Tu dla uproszczenia przyjmujemy, że to jest wywoływane raz dziennie 
        przez APScheduler, więc resetujemy wszystko, co ma daily/weekly.
    """
    tasks = load_tasks()
    for t in tasks:
        if t.get("cyclic_type") in ["daily", "weekly"]:
            t["done"] = False
    save_tasks(tasks)

def mark_task_done(task_id, done=True):
    """Oznacza zadanie jako ukończone/niewykonane."""
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = done
            break
    save_tasks(tasks)

def update_task(task_id, **kwargs):
    """
    Aktualizuje dowolne pola zadania (np. deadline, title, itp.).
    Przykład użycia: update_task(3, title="Nowy tytuł", deadline="2025-03-01 10:00")
    """
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            for k, v in kwargs.items():
                t[k] = v
            break
    save_tasks(tasks)
