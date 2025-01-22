# hrv_monitor.py

"""
Moduł monitorujący HR/HRV użytkownika i podejmujący odpowiednie działania w zależności od stanu.
"""

import time
from datetime import datetime
from typing import Tuple

from tasks import get_all_tasks, save_task

########################################
# 1) Pobieranie HR/HRV z urządzenia
########################################
def get_current_hrv() -> Tuple[int, int]:
    """
    Pobiera aktualne wartości HR i HRV z urządzenia.

    Zwraca:
        Krotka (hr, hrv), gdzie hr to tętno, a hrv to zmienność rytmu serca.
    """
    # TODO: Implementacja interfejsu z urządzeniem lub API producenta.
    # Symulacja przykładowych danych:
    hr = 90  # Przykładowe tętno
    hrv = 30  # Przykładowa zmienność rytmu serca
    return hr, hrv

########################################
# 2) Logika triggerów (stres, zmęczenie, hiperfokus)
########################################
def monitor_physiology(hr: int, hrv: int) -> str:
    """
    Określa stan użytkownika na podstawie wartości HR i HRV.

    Args:
        hr: Tętno.
        hrv: Zmienność rytmu serca.

    Zwraca:
        Stan użytkownika jako string:
          - "ALERT_STRESS"
          - "LOW_HRV"
          - "HIGH_HRV"
          - "NORMAL"
    """
    high_hr_threshold = 100
    low_hrv_threshold = 25
    high_hrv_threshold = 50

    if hr > high_hr_threshold and hrv < low_hrv_threshold:
        return "ALERT_STRESS"
    elif hrv < low_hrv_threshold:
        return "LOW_HRV"
    elif hrv > high_hrv_threshold and hr < 85:
        return "HIGH_HRV"
    else:
        return "NORMAL"

########################################
# 3) Reakcja na dany stan – dodawanie zadań lub modyfikacja priorytetu
########################################
def take_action_based_on_state(state: str):
    """
    Podejmuje odpowiednie działania w zależności od stanu użytkownika.

    Args:
        state: Stan użytkownika zwrócony przez monitor_physiology().
    """
    if state == "ALERT_STRESS":
        print("[HRV] Wysoki stres! Proponuję przerwę relaksacyjną.")
        _add_break_task("Przerwa relaksacyjna (wysoki stres)")
    elif state == "LOW_HRV":
        print("[HRV] Niska HRV. Możliwe zmęczenie – sugeruję przerwę.")
        _add_break_task("Krótka przerwa (niskie HRV)")
    elif state == "HIGH_HRV":
        print("[HRV] Wysoka HRV – dobry moment na trudne zadania.")
        # Można ewentualnie podnieść priorytet trudniejszych zadań
    else:
        print("[HRV] Stan NORMAL – brak akcji.")

def _add_break_task(title: str):
    """
    Dodaje zadanie przerwy do listy zadań.

    Args:
        title: Tytuł zadania.
    """
    tasks = get_all_tasks()
    new_id = f"hrv_{int(time.time())}"
    new_task = {
        "id": new_id,
        "title": title,
        "deadline": None,
        "completed": False,
        "recurring": False,
        "priority": 0
    }
    tasks.append(new_task)
    save_task(new_task)
    print(f"[HRV] Dodano zadanie '{title}' (id={new_id}).")

########################################
# 4) Główna funkcja – do wywołania np. co 5 min z APSchedulera
########################################
def run_hrv_monitor():
    """
    Główna funkcja uruchamiająca monitor HRV.
    """
    hr, hrv = get_current_hrv()
    state = monitor_physiology(hr, hrv)
    take_action_based_on_state(state)
    print("[HRV] Monitor zakończony.")