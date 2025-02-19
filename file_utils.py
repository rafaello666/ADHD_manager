# file_utils.py

import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"
HISTORY_FILE = "history.json"

def load_json_file(path):
    """
    Ładuje zawartość pliku JSON i zwraca jako strukturę Python (listę lub słownik).
    Jeśli plik nie istnieje lub jest uszkodzony, zwraca pustą listę.
    """
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []

def save_json_file(path, data):
    """
    Zapisuje strukturę Python (listę/słownik) do pliku JSON, z wcięciem i UTF-8.
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def now_str():
    """
    Zwraca aktualny czas w formacie ISO8601, np. '2025-01-22T21:14:00.123456'
    """
    return datetime.now().isoformat()
