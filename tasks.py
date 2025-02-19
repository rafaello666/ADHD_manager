# tasks.py

import json
import os

TASKS_FILE = "tasks.json"

def _load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []

def _save_tasks(tasks_list):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks_list, f, ensure_ascii=False, indent=2)

def get_all_tasks():
    return _load_tasks()

def save_task(new_task):
    tasks = _load_tasks()
    existing = next((t for t in tasks if t["id"] == new_task["id"]), None)
    if existing:
        existing.update(new_task)
    else:
        tasks.append(new_task)
    _save_tasks(tasks)

def remove_task(task_id):
    tasks = _load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        return False
    _save_tasks(new_tasks)
    return True

def complete_task(task_id):
    tasks = _load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["completed"] = True
            _save_tasks(tasks)
            return True
    return False

def reopen_task(task_id):
    tasks = _load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["completed"] = False
            _save_tasks(tasks)
            return True
    return False
