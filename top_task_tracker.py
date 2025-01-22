# top_task_tracker.py
import json
import os
from datetime import datetime

TRACK_FILE = "top_task_tracker.json"

def load_top_info():
    """Wczytuje info o top-zadaniu z pliku JSON."""
    if not os.path.exists(TRACK_FILE):
        return {
            "previous_top_id": None,
            "time_of_start": None,
            "spent_cycles": 0
        }
    with open(TRACK_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_top_info(info: dict):
    """Zapisuje info do top_task_tracker.json."""
    with open(TRACK_FILE, "w", encoding="utf-8") as f:
        json.dump(info, f, indent=2, ensure_ascii=False)

def reset_top_info(new_top_id: str):
    """Ustawia nowy top z time_of_start=now, spent_cycles=0."""
    now_str = datetime.now().isoformat()
    data = {
        "previous_top_id": new_top_id,
        "time_of_start": now_str,
        "spent_cycles": 0
    }
    save_top_info(data)
