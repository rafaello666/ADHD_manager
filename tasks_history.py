# tasks_history.py

"""
Moduł zarządzający historią ukończonych zadań.
"""

import json
import os
from typing import List, Dict

HISTORY_FILE = "task_history.json"

def load_history() -> List[Dict]:
    """
    Zwraca listę rekordów historii (wykonanych zadań) z pliku JSON.

    Zwraca:
        Lista słowników z historią zadań.
    """
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Wczytywanie {HISTORY_FILE}: {e}")
        return []

def save_history(data: List[Dict]):
    """
    Zapisuje listę historii zadań do pliku JSON.

    Args:
        data: Lista słowników z historią zadań.
    """
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[ERROR] Zapisywanie {HISTORY_FILE}: {e}")

def add_history_record(task_id: str, completion_time: str, time_spent: float,
                       system_priority: float, deadline_gap: float,
                       user_importance: float = None, was_interrupted: bool = False):
    """
    Dodaje nowy rekord do historii.

    Args:
        task_id: ID zadania.
        completion_time: Czas ukończenia zadania.
        time_spent: Czas spędzony na zadaniu.
        system_priority: Priorytet nadany przez system.
        deadline_gap: Różnica czasu do terminu.
        user_importance: Ważność zadania zdaniem użytkownika.
        was_interrupted: Czy zadanie zostało przerwane.
    """
    hist_data = load_history()
    new_id = f"hist_{len(hist_data) + 1}"

    record = {
        "id": new_id,
        "task_id": task_id,
        "completion_time": completion_time,
        "time_spent": time_spent,
        "system_priority": system_priority,
        "actual_deadline_gap": deadline_gap,
        "user_importance": user_importance,
        "was_interrupted": was_interrupted
    }
    hist_data.append(record)
    save_history(hist_data)
    print(f"[HISTORY] Dodano rekord {new_id} (task_id={task_id})")