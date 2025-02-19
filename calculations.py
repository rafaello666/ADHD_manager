import json
import os
from datetime import datetime
from typing import Dict, Any

GOALS_FILE = "goals_config.json"

def load_goals_config() -> Dict[str, float]:
    """
    Wczytuje wagi parametrów z pliku JSON. Jeśli plik nie istnieje,
    tworzy go z wartościami domyślnymi.
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
            with open(GOALS_FILE, 'w', encoding="utf-8") as f:
                json.dump(default_weights, f, indent=4)
            return default_weights
        except Exception as e:
            print(f"[ERROR] Tworzenie {GOALS_FILE}: {e}")
            return default_weights
    try:
        with open(GOALS_FILE, 'r', encoding="utf-8") as f:
            weights = json.load(f)
        return weights
    except Exception as e:
        print(f"[ERROR] Wczytywanie {GOALS_FILE}: {e}")
        return default_weights

def dynamic_deadline_factor(task: Dict[str, Any]) -> float:
    """
    Zwiększa priorytet zadania w miarę zbliżania się do terminu (deadline).
    Format deadline: ISO string (YYYY-MM-DDTHH:MM) lub (YYYY-MM-DD HH:MM:SS).
    """
    dl = task.get("deadline")
    if not dl:
        return 1.0  # Brak deadline'u -> bez zmiany
    try:
        # Spróbujmy z .fromisoformat(); jeśli błąd, przerzucimy się na parse manualne
        dl_dt = datetime.fromisoformat(dl.replace(" ", "T"))  # drobne obejście spacji
    except ValueError:
        print(f"[ERROR] Nieprawidłowy deadline dla task {task.get('id')}: {dl}")
        return 1.0

    now = datetime.now()
    diff_h = (dl_dt - now).total_seconds() / 3600
    if diff_h <= 0:
        return 2.0  # Termin już minął => ważne
    elif diff_h < 24:
        return 1.5  # Mniej niż doba => wyższy priorytet
    else:
        return 1.0  # Ponad doba => zwykły priorytet

def calculate_priority(task: Dict[str, Any]) -> float:
    """
    Oblicza priorytet zadania na podstawie skonfigurowanych wag (goals_config.json)
    i atrybutów zadań.
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

    # Mnożnik zbliżającego się terminu
    deadline_factor = dynamic_deadline_factor(task)
    priority *= deadline_factor

    return round(priority, 2)
