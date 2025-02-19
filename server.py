import os
import json
from flask import Flask, jsonify, request, send_from_directory
import logging

app = Flask(__name__, static_folder="static")
app.logger.setLevel(logging.INFO)

TASKS_JSON_PATH = "tasks.json"

def get_tasks_from_json():
    """
    Odczytuje zadania z pliku JSON, usuwa klucze zaczynające się od "wplyw_na_monike"
    i zwraca listę zadań.
    """
    if not os.path.exists(TASKS_JSON_PATH):
        app.logger.warning("Plik %s nie istnieje.", TASKS_JSON_PATH)
        return []
    try:
        with open(TASKS_JSON_PATH, "r", encoding="utf-8") as f:
            tasks = json.load(f)
        filtered_tasks = []
        for task in tasks:
            # Usuń klucze zaczynające się od "wplyw_na_monike"
            filtered_task = { key: value for key, value in task.items() if not key.startswith("wplyw_na_monike") }
            filtered_tasks.append(filtered_task)
        return filtered_tasks
    except Exception as e:
        app.logger.error("Błąd odczytu pliku JSON: %s", str(e))
        return []

def save_tasks_to_json(tasks):
    """
    Zapisuje listę zadań do pliku JSON.
    """
    try:
        with open(TASKS_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        app.logger.error("Błąd zapisu do pliku JSON: %s", str(e))
        return False

@app.route('/tasks_json', methods=['GET'])
def tasks_json():
    """
    Zwraca zadania z pliku tasks.json, posortowane według:
      - 'priority' malejąco,
      - 'deadline' rosnąco (jeśli brak, traktowane jako pusty string).
    """
    try:
        tasks = get_tasks_from_json()
        tasks = sorted(tasks, key=lambda t: (-t.get('priority', 0), t.get('deadline') or ""))
        return jsonify(tasks), 200
    except Exception as e:
        app.logger.error("Błąd w /tasks_json: %s", str(e))
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/update_task_priority', methods=['POST'])
def update_task_priority():
    """
    Aktualizuje pole 'priority' (i opcjonalnie 'deadline') dla zadania.
    Oczekuje JSON z:
      - id: identyfikator zadania (np. "task_2")
      - priority: nowa wartość (liczba)
      - deadline: opcjonalna wartość deadline (string, np. "2025-02-15")
    """
    try:
        data = request.get_json()
        task_id = data.get("id")
        new_priority = data.get("priority")
        new_deadline = data.get("deadline")  # opcjonalnie
        if not task_id or new_priority is None:
            return jsonify({"error": "id and priority are required"}), 400

        tasks = get_tasks_from_json()
        task_found = False
        for task in tasks:
            if task.get("id") == task_id:
                task["priority"] = new_priority
                # Aktualizuj deadline, jeśli podano – może być pusta wartość (przyjmujemy null, jeśli brak)
                if new_deadline is not None:
                    task["deadline"] = new_deadline
                task_found = True
                break
        if not task_found:
            return jsonify({"error": "Task not found"}), 404

        if save_tasks_to_json(tasks):
            return jsonify({"message": "Priority updated successfully"}), 200
        else:
            return jsonify({"error": "Failed to save tasks"}), 500
    except Exception as e:
        app.logger.error("Błąd w /update_task_priority: %s", str(e))
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/add_task', methods=['POST'])
def add_task():
    """
    Dodaje nowe zadanie.
    Oczekuje JSON z:
      - title: tytuł zadania
      - priority: priorytet zadania (1-10)
    Nowe zadanie otrzyma unikalne ID (np. "task_N"). Inne pola ustawiamy domyślnie.
    """
    try:
        data = request.get_json()
        title = data.get("title")
        priority = data.get("priority")
        if not title or priority is None:
            return jsonify({"error": "title and priority are required"}), 400

        tasks = get_tasks_from_json()
        # Generowanie nowego ID
        existing_ids = [t.get("id", "") for t in tasks if t.get("id", "").startswith("task_")]
        if existing_ids:
            numbers = []
            # Wyodrębnij liczby z identyfikatorów
            for tid in existing_ids:
                try:
                    num = int(tid.split("_")[1])
                    numbers.append(num)
                except:
                    continue
            if numbers:
                new_id = "task_" + str(max(numbers) + 1)
            else:
                new_id = "task_1"
        else:
            new_id = "task_1"
        # Ustawiamy domyślne wartości dla pozostałych pól
        new_task = {
            "id": new_id,
            "title": title,
            "completed": False,
            "last_reminder": None,
            "priority": priority,
            "pilne_dla_przetrwania": None,
            "dlugoterminowe_znaczenie": None,
            "konsekwencje_opoznienia": None,
            "czas_realizacji": None,
            "potrzebne_zasoby": None,
            "deadline_strictness": None,
            "wplyw_na_monike_1h": None,
            "wplyw_na_monike_3h": None,
            "wplyw_na_monike_12h": None,
            "wplyw_na_monike_48h": None,
            "deadline": None,
            "estimated_time": None,
            "recurring": False,
            "recurrence_pattern": None,
            "tags": "",
            "subtasks": [],
            "timer_running": False,
            "timer_end": None,
            "description": "",
            "notes": ""
        }
        tasks.append(new_task)
        if save_tasks_to_json(tasks):
            return jsonify({"message": "Task added successfully", "task": new_task}), 201
        else:
            return jsonify({"error": "Failed to save task"}), 500
    except Exception as e:
        app.logger.error("Błąd w /add_task: %s", str(e))
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/')
def index():
    """
    Serwuje interfejs użytkownika (plik index.html) z katalogu static.
    """
    return send_from_directory(app.static_folder, "index.html")

if __name__ == '__main__':
    app.run(debug=True)
