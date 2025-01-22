# partial_scoring.py
import sys
from tasks import get_all_tasks, save_task
from calculations import load_goals_config

def run_partial_scoring():
    """
    1) Wczytuje tasks.json
    2) Sprawdza brakujące klucze (z goals_config.json + np. deadline_strictness)
    3) Pyta w CLI i zapisuje
    """
    print("[SCORING] start partial scoring CLI")

    tasks = get_all_tasks()
    config = load_goals_config()
    extra_keys = ["deadline_strictness"]  # np. jeśli nie jest w config
    interesting_keys = list(config.keys()) + extra_keys

    not_done = [t for t in tasks if not t.get("completed")]
    changed = False

    for z in not_done:
        updated = False
        for k in interesting_keys:
            if z.get(k) is None:
                prompt = f"[?] Zadanie '{z['title']}' - podaj {k} (1–10, Enter=ignoruj): "
                ans = input(prompt)
                ans = ans.strip()
                if ans.isdigit():
                    val = int(ans)
                    if 1<=val<=10:
                        z[k] = val
                        updated = True
                    else:
                        print("[!] Niepoprawna liczba, pomijam")
                else:
                    print("[i] Pominięto brak wpisu")

        if updated:
            save_task(z)
            changed = True

    if changed:
        print("[SCORING] Zaktualizowano parametry w tasks.json")
    else:
        print("[SCORING] Nic nie zmieniono.")

    print("[SCORING] Koniec partial scoring.")

if __name__=="__main__":
    run_partial_scoring()
