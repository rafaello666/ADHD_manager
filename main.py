# main.py

"""
Główny plik uruchamiający aplikację ADHD Manager.
Obsługuje interaktywny scoring zadań, przypomnienia oraz uruchamia serwer.
"""

import argparse

from apscheduler.schedulers.background import BackgroundScheduler

from tasks import get_all_tasks, save_task, complete_task, remove_task
from calculations import calculate_priority
from scales import get_scale_description
from twilio_sms import send_sms
from top_task_tracker import load_top_info, save_top_info, reset_top_info
from hrv_monitor import run_hrv_monitor

# Inicjalizacja APSchedulera
scheduler = None

def ask_question(task_title: str, question_key: str, current_val=None):
    """
    Zadaje pytanie użytkownikowi w celu oceny zadania.

    Args:
        task_title: Tytuł zadania.
        question_key: Klucz pytania.
        current_val: Aktualna wartość (opcjonalnie).

    Zwraca:
        Wartość oceny lub specjalne komendy ('BACK' lub None).
    """
    print(f"\nZadanie: {task_title}, klucz={question_key} (1–10 lub 'NIE WIEM','BACK').")
    if current_val is not None:
        print(f"[Aktualnie={current_val}]")
    print(get_scale_description(question_key))
    while True:
        ans = input("Twoja ocena: ").strip().upper()
        if ans == "NIE WIEM":
            return None
        elif ans == "BACK":
            return "BACK"
        else:
            try:
                val = int(ans)
                if 1 <= val <= 10:
                    return val
                else:
                    print("Podaj liczbę 1–10 lub 'NIE WIEM','BACK'.")
            except ValueError:
                print("Nieprawidłowe. Spróbuj.")

def score_tasks_interactively():
    """
    Interfejs do interaktywnego oceniania zadań przez użytkownika.
    """
    print("[SCORE] Interaktywny scoring (z możliwością cofania).")
    keys = [
        "pilne_dla_przetrwania", "dlugoterminowe_znaczenie", "konsekwencje_opoznienia",
        "czas_realizacji", "potrzebne_zasoby", "deadline_strictness",
        "wplyw_na_monike_1h", "wplyw_na_monike_3h", "wplyw_na_monike_12h", "wplyw_na_monike_48h"
    ]
    tasks = get_all_tasks()
    for t in tasks:
        if t.get("completed"):
            continue
        title = t["title"]
        print(f"\n=== Zadanie: {title} (ID={t['id']}) ===")
        local = {}
        for k in keys:
            local[k] = t.get(k)
        idx = 0
        while idx < len(keys):
            k = keys[idx]
            ans = ask_question(title, k, local[k])
            if ans == "BACK":
                if idx > 0:
                    idx -= 1
                else:
                    print("[INFO] Nie można cofnąć się bardziej.")
            else:
                local[k] = ans
                idx += 1
        for k in keys:
            t[k] = local[k]
        save_task(t)
    print("[SCORE] Zakończono scoring.")

def remind_tasks():
    """
    Sprawdza otwarte zadania, przelicza priorytety,
    wybiera top i jeśli się zmienił – wysyła SMS.
    """
    tasks = get_all_tasks()
    open_tasks = [x for x in tasks if not x.get("completed")]

    for x in open_tasks:
        prio = calculate_priority(x)
        x["priority"] = prio
        save_task(x)

    if not open_tasks:
        print("[REMIND] Brak otwartych zadań.")
        return

    open_tasks.sort(key=lambda x: x["priority"], reverse=True)
    top = open_tasks[0]
    top_id = top["id"]
    info = load_top_info()
    prev_id = info.get("previous_top_id")

    if top_id != prev_id:
        print("[TOP TASK] Zmienił się top, wysyłamy SMS.")
        reset_top_info(top_id)
        msg = f"Nowy TOP: {top['title']} (Priorytet={top['priority']:.2f})"
        send_sms(msg)
    else:
        print("[REMIND] Top zadanie bez zmian.")

def reset_daily_recurring_tasks():
    """
    Codzienny reset zadań cyklicznych (nawyków) – ustawia completed=False.
    """
    print("[RESET] Resetowanie zadań daily (ustawienie completed=False).")
    tasks = get_all_tasks()
    changed = False
    for t in tasks:
        if t.get("recurring") and t.get("recurrence_pattern") == "daily":
            t["completed"] = False
            t["priority"] = 0
            save_task(t)
            changed = True
    if changed:
        print("[RESET] Zresetowano daily tasks.")

def complete_task_cli(task_id: str):
    """
    Odhacza zadanie jako ukończone lub usuwa je (jeśli nie jest cykliczne).

    Args:
        task_id: ID zadania.
    """
    tasks = get_all_tasks()
    t = next((x for x in tasks if x["id"] == task_id), None)
    if not t:
        print("[ERROR] Nie znaleziono zadania.")
        return
    if t.get("recurring", False):
        ok = complete_task(task_id)
        if ok:
            print("[COMPLETE] Zadanie cykliczne ukończone.")
        else:
            print("[ERROR] Nie udało się odhaczyć zadania.")
    else:
        rem = remove_task(task_id)
        if rem:
            print("[REMOVE] Usunięto jednorazowe zadanie.")
        else:
            print("[ERROR] Nie znaleziono zadania do usunięcia.")

def run_server():
    """
    Uruchamia serwer Flask wraz z APSchedulerem.
    """
    print("[SERVER] Start Flask + APScheduler.")
    start_scheduler()
    from server import app  # Import lokalny
    app.run(host="0.0.0.0", port=5000, debug=True)

def start_scheduler():
    """
    Inicjalizuje i uruchamia APScheduler z zaplanowanymi zadaniami.
    """
    global scheduler
    scheduler = BackgroundScheduler()
    # Co 15 minut przypomnienia
    scheduler.add_job(remind_tasks, "interval", minutes=15)
    # Co 5 minut monitor HRV
    scheduler.add_job(run_hrv_monitor, "interval", minutes=5)
    # Codziennie o 3:00 reset zadań daily
    scheduler.add_job(reset_daily_recurring_tasks, "cron", hour=3, minute=0)
    scheduler.start()

def parse_args():
    """
    Parsuje argumenty wiersza poleceń.

    Zwraca:
        Argumenty przekazane do skryptu.
    """
    parser = argparse.ArgumentParser(description="ADHD Manager – CLI.")
    parser.add_argument("command", choices=["score", "remind", "complete", "server", "reset", "hrvtest"])
    parser.add_argument("--task_id", help="ID zadania")
    return parser.parse_args()

def main():
    args = parse_args()
    if args.command == "score":
        score_tasks_interactively()
    elif args.command == "remind":
        remind_tasks()
    elif args.command == "complete":
        if not args.task_id:
            print("Musisz podać --task_id=..")
        else:
            complete_task_cli(args.task_id)
    elif args.command == "server":
        run_server()
    elif args.command == "reset":
        reset_daily_recurring_tasks()
    elif args.command == "hrvtest":
        run_hrv_monitor()

if __name__ == "__main__":
    main()