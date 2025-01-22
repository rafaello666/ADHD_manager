# calculations.py

"""
Moduł odpowiedzialny za obliczanie priorytetów zadań na podstawie skonfigurowanych wag i parametrów zadań.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any

GOALS_FILE = "goals_config.json"

def load_goals_config() -> Dict[str, float]:
    """
    Wczytuje wagi parametrów z pliku JSON.

    Zwraca:
        Słownik z wagami parametrów.
    """
    default_weights = {
        "pilne_dla_przetrwania": 0.15,
        "dlugoterminowe_znaczenie": 0.1,
        "konsekwencje_opoznienia": 0.15,
        "czas_realizacji": 0.1,
        "potrzebne_zasoby": 0.1,
        "deadline_strictness": 0.1,
        "cel_dziewczyna": 0.2,
        "cel_finanse": 0.2
    }
    if not os.path.exists(GOALS_FILE):
        try:
            with open(GOALS_FILE, 'w') as f:
                json.dump(default_weights, f, indent=4)
            return default_weights
        except Exception as e:
            print(f"Error creating {GOALS_FILE}: {e}")
            return default_weights
    try:
        with open(GOALS_FILE, 'r') as f:
            weights = json.load(f)
        return weights
    except Exception as e:
        print(f"Error loading {GOALS_FILE}: {e}")
        return default_weights

def dynamic_deadline_factor(task: Dict[str, Any]) -> float:
    """
    Zwiększa priorytet zadania w miarę zbliżania się do terminu (deadline).

    Args:
        task: Słownik z danymi zadania.

    Zwraca:
        Mnożnik priorytetu w zależności od czasu pozostałego do deadline'u.
    """
    dl = task.get("deadline")
    if not dl:
        return 1.0  # No deadline, no adjustment
    try:
        dl_dt = datetime.fromisoformat(dl)
    except ValueError:
        print(f"Invalid deadline format for task {task.get('id')}: {dl}")
        return 1.0
    now = datetime.now()
    diff_h = (dl_dt - now).total_seconds() / 3600
    if diff_h <= 0:
        return 2.0  # Deadline passed
    elif diff_h < 24:
        return 1.5  # Less than a day
    else:
        return 1.0  # More than a day

def calculate_priority(task: Dict[str, Any]) -> float:
    """
    Oblicza priorytet zadania na podstawie skonfigurowanych wag i parametrów zadań.

    Args:
        task: Słownik z danymi zadania.

    Zwraca:
        Obliczony priorytet jako float.
    """
    weights = load_goals_config()
    priority = 0.0
    priority += task.get("pilne_dla_przetrwania", 0) * weights.get("pilne_dla_przetrwania", 0)
    priority += task.get("dlugoterminowe_znaczenie", 0) * weights.get("dlugoterminowe_znaczenie", 0)
    priority += task.get("konsekwencje_opoznienia", 0) * weights.get("konsekwencje_opoznienia", 0)
    priority += task.get("czas_realizacji", 0) * weights.get("czas_realizacji", 0)
    priority += task.get("potrzebne_zasoby", 0) * weights.get("potrzebne_zasoby", 0)
    priority += task.get("deadline_strictness", 0) * weights.get("deadline_strictness", 0)
    priority += task.get("cel_dziewczyna", 0) * weights.get("cel_dziewczyna", 0)
    priority += task.get("cel_finanse", 0) * weights.get("cel_finanse", 0)

    # Apply dynamic deadline factor
    deadline_factor = dynamic_deadline_factor(task)
    priority *= deadline_factor

    return round(priority, 2)
