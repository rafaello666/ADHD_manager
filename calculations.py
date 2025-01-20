# calculations.py

"""
Logika priorytetu (stare + monikowe klucze),
dynamic_deadline_factor, wagi, normalizacja. 
"""

from datetime import datetime

weights = {
    "pilne_dla_przetrwania": 0.15,
    "dlugoterminowe_znaczenie": 0.1,
    "konsekwencje_opoznienia": 0.15,
    "czas_realizacji": 0.1,
    "potrzebne_zasoby": 0.1,
    "deadline_strictness": 0.1,
    "wplyw_na_monike_1h": 0.2,
    "wplyw_na_monike_3h": 0.05,
    "wplyw_na_monike_12h": 0.05,
    "wplyw_na_monike_48h": 0.05
}

def dynamic_deadline_factor(task):
    dl = task.get("deadline")
    if not dl:
        return 1.0
    try:
        dl_dt = datetime.fromisoformat(dl)
    except ValueError:
        return 1.0
    now = datetime.now()
    diff_h = (dl_dt - now).total_seconds()/3600
    if diff_h <= 0:
        return 2.0
    elif diff_h < 24:
        factor = 1.0 + (24 - diff_h)/24
        return factor
    else:
        return 1.0

def calculate_priority(task):
    base_sum = 0.0
    total_w = 0.0

    for key, w in weights.items():
        val = task.get(key)
        if val is None:
            continue
        # Normalizacja (zakładamy wartości 1–10)
        norm = (val - 1)/9
        if norm < 0: norm = 0
        if norm > 1: norm = 1
        base_sum += norm*w
        total_w += w

    if total_w > 0:
        base_score = (base_sum/total_w)*10
    else:
        base_score = 0.0

    dd_factor = dynamic_deadline_factor(task)
    final = base_score * dd_factor
    return final
