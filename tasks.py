# tasks.py
import json
import os

DATA_FILE = "tasks.json"

def _load_tasks_from_file():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        print(f"[ERROR] Wczytywanie {DATA_FILE}.")
        return []

def _save_tasks_to_file(tasks_list):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks_list, f, indent=2, ensure_ascii=False)

def get_all_tasks():
    """ Zwraca listę wszystkich zadań (dict) z pliku JSON. """
    return _load_tasks_from_file()

def save_task(updated_task):
    """
    Nadpisuje (lub dodaje) zadanie w pliku. 
    Jeżeli nie ma zadania o danym 'id', dodaje nowe.
    """
    tasks = _load_tasks_from_file()
    for i, t in enumerate(tasks):
        if t["id"] == updated_task["id"]:
            tasks[i] = updated_task
            break
    else:
        tasks.append(updated_task)
    _save_tasks_to_file(tasks)

def complete_task(task_id: str) -> bool:
    """ Ustawia completed=True w zadaniu o danym ID. Zwraca True, jeśli się uda. """
    tasks = _load_tasks_from_file()
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            t["completed"] = True
            _save_tasks_to_file(tasks)
            return True
    return False

def remove_task(task_id: str) -> bool:
    """ Usuwa zadanie z listy, zwraca True, jeśli faktycznie coś usunięto. """
    tasks = _load_tasks_from_file()
    init_len = len(tasks)
    tasks = [x for x in tasks if x["id"] != task_id]
    if len(tasks) < init_len:
        _save_tasks_to_file(tasks)
        return True
    return False
