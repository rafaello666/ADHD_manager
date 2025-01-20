# main.py

import argparse
import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from tasks import get_all_tasks, save_task, complete_task, remove_task
from calculations import calculate_priority
from scales import get_scale_description
from twilio_sms import send_sms
from top_task_tracker import load_top_info, save_top_info, reset_top_info

DATA_FILE = "tasks.json"
scheduler = None

def ask_question(task_title, question_key, current_val=None):
    print(f"\nZadanie: {task_title}, klucz={question_key} (1–10 lub 'NIE WIEM','BACK').")
    if current_val is not None:
        print(f"[Aktualnie={current_val}]")
    return input_loop(question_key, current_val)

def input_loop(question_key, current_val):
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
    Interaktywny scoring w konsoli. Możesz pominąć, jeśli korzystasz tylko z GUI.
    """
    print("[SCORE] Interaktywny scoring (z BACK).")
    keys = [
        "pilne_dla_przetrwania","dlugoterminowe_znaczenie","konsekwencje_opoznienia",
        "czas_realizacji","potrzebne_zasoby","deadline_strictness",
        "wplyw_na_monike_1h","wplyw_na_monike_3h","wplyw_na_monike_12h","wplyw_na_monike_48h"
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
                    print("[INFO] Nie cofniesz się bardziej.")
            else:
                local[k] = ans
                idx += 1
        for k in keys:
            t[k] = local[k]
        save_task(t)
    print("[SCORE] Zakończono scoring.")

def remind_tasks():
    """
    Sprawdza top-zadanie, ewentualnie wysyła przypomnienia SMS, 
    a także sprawdza, czy któremuś zadaniu nie skończył się timer.
    """
    tasks = get_all_tasks()
    open_tasks = [x for x in tasks if not x.get("completed")]

    # Przelicz priorytety
    for x in open_tasks:
        prio = calculate_priority(x)
        x["priority"] = prio
        save_task(x)

    if not open_tasks:
        print("[REMIND] Brak otwartych zadań do przypominania.")
        return

    # Sort malejąco po priorytecie i bierzemy top
    open_tasks.sort(key=lambda x: x["priority"], reverse=True)
    top = open_tasks[0]
    top_id = top["id"]
    info = load_top_info()
    prev_id = info.get("previous_top_id")

    # Sprawdź, czy top się zmienił -> wyślij SMS
    if top_id != prev_id:
        print("[TOP TASK] Zmienił się top, wysyłamy SMS.")
        reset_top_info(top_id)
        msg = f"Nowy TOP: {top['title']} (Priorytet={top['priority']:.2f})"
        send_sms(msg)
    else:
        print("[REMIND] Top zadanie bez zmian.")

    # Sprawdzamy, czy timer się nie skończył
    now_ts = time.time()
    for t in open_tasks:
        if t.get("timer_running") and t.get("timer_end"):
            if now_ts >= t["timer_end"]:
                # Timer upłynął
                t["timer_running"] = False
                t["timer_end"] = None
                save_task(t)
                msg = (
                    f"UWAGA! Minął czas zadania '{t['title']}' "
                    f"({t.get('estimated_time')}h), a nie zostało ukończone."
                )
                send_sms(msg)

def reset_daily_recurring_tasks():
    """
    Codzienny reset zadań, które mają recurring='daily'.
    """
    print("[RESET] Zadania daily => completed=false.")
    tasks = get_all_tasks()
    changed = False
    for t in tasks:
        if t.get("recurring") and t.get("recurrence_pattern") == "daily":
            t["completed"] = False
            t["last_reminder"] = None
            t["priority"] = 0
            save_task(t)
            changed = True
    if changed:
        print("[RESET] Zresetowano daily tasks.")

def complete_task_cli(task_id: str):
    """
    Dla recurring -> completed = True
    Dla jednorazowych -> remove_task
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
            print("[ERROR] Nie udało się odhaczyć.")
    else:
        rem = remove_task(task_id)
        if rem:
            print("[REMOVE] Usunięto jednorazowe zadanie.")
        else:
            print("[ERROR] Nie znaleziono do usunięcia.")

def run_server():
    print("[SERVER] Start Flask + APScheduler.")
    start_scheduler()
    import server
    server.app.run(host="0.0.0.0", port=5000, debug=True)

def start_scheduler():
    global scheduler
    scheduler = BackgroundScheduler()
    # co 15 minut przypomnienia
    scheduler.add_job(remind_tasks, "interval", minutes=15)
    # codziennie o 3:00 reset
    scheduler.add_job(reset_daily_recurring_tasks, "cron", hour=3, minute=0)
    scheduler.start()

def parse_args():
    parser = argparse.ArgumentParser(description="ADHD Manager – CLI.")
    parser.add_argument("command", choices=["score","remind","complete","server","reset"])
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

if __name__ == "__main__":
    main()
