# server.py

"""
Główny moduł serwera Flask dla aplikacji ADHD Manager.
"""

import os
import sys
import time
import atexit
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_wtf import CSRFProtect
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFError

# Import modułów aplikacji
from tasks import get_all_tasks, save_task, remove_task, complete_task
from calculations import calculate_priority
from twilio_sms import send_sms
from google_calendar_integration import get_upcoming_events
from hrv_monitor import run_hrv_monitor

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

app = Flask(__name__)

# Ustaw SECRET_KEY z pliku .env
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Inicjalizacja ochrony CSRF
csrf = CSRFProtect(app)

scheduler = BackgroundScheduler()

@app.route("/")
def home():
    tasks = get_all_tasks()

    # Policz statystyki
    total = len(tasks)
    completed_count = sum(1 for t in tasks if t.get("completed"))
    completion_ratio = 0
    if total > 0:
        completion_ratio = round((completed_count / total) * 100, 1)

    # Sortuj zadania według priorytetu malejąco
    tasks.sort(key=lambda x: x.get("priority", 0), reverse=True)

    # Przygotuj dane do wykresów
    priority_counts = {
        'wysoki': sum(1 for t in tasks if t.get('priority', 0) > 7),
        'sredni': sum(1 for t in tasks if 4 < t.get('priority', 0) <= 7),
        'niski': sum(1 for t in tasks if t.get('priority', 0) <= 4),
    }

    return render_template(
        "index.html",
        tasks=tasks,
        total_tasks=total,
        completed_tasks=completed_count,
        completion_ratio=completion_ratio,
        priority_counts=priority_counts
    )

@app.route("/add_task", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    deadline = request.form.get("deadline", "")
    if not title:
        return "Brak tytułu zadania", 400

    new_id = f"task_{int(time.time())}"
    new_task = {
        "id": new_id,
        "title": title,
        "completed": False,
        "deadline": deadline if deadline else None,
        "priority": 0,
    }
    save_task(new_task)
    return redirect(url_for("home"))

@app.route("/tasks/<task_id>/complete", methods=["POST"])
def complete_task_route(task_id):
    ok = complete_task(task_id)
    if not ok:
        return "Nie udało się ukończyć zadania", 404
    return redirect(url_for("home"))

@app.route("/tasks/<task_id>/remove", methods=["POST"])
def remove_task_route(task_id):
    rem = remove_task(task_id)
    if not rem:
        return "Nie znaleziono zadania do usunięcia", 404
    return redirect(url_for("home"))

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400

def remind_tasks():
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

    print("[REMIND] Wysyłamy przypomnienie o top zadaniu.")
    msg = f"Nowy TOP: {top['title']} (Priorytet={top['priority']:.2f})"
    send_sms(msg)

def check_calendar_and_notify():
    events = get_upcoming_events(minutes_ahead=30)
    if not events:
        print("[CALENDAR] Brak wydarzeń w ciągu 30 minut.")
        return
    for ev in events:
        title = ev.get("summary", "Bez tytułu")
        loc = ev.get("location", "Brak lokalizacji")
        start_dt = ev.get("start")
        if start_dt:
            diff_min = compute_diff_minutes(start_dt)
            msg = (
                f"Uwaga! Za {diff_min} min: '{title}'. "
                f"Lokalizacja: {loc}"
            )
            print("[CALENDAR] Wyślę SMS:", msg)
            send_sms(msg)
        else:
            print("[CALENDAR] Brak informacji o czasie rozpoczęcia wydarzenia.")

def compute_diff_minutes(start_dt: datetime) -> int:
    now = datetime.now()
    diff = start_dt - now
    return int(diff.total_seconds() / 60)

def start_scheduler():
    scheduler.add_job(remind_tasks, "interval", minutes=15)
    scheduler.add_job(check_calendar_and_notify, "interval", minutes=5)
    scheduler.add_job(run_hrv_monitor, "interval", minutes=5)
    # Dodaj inne zadania według potrzeb
    scheduler.start()
    print("[SCHEDULER] Scheduler wystartował.")

@atexit.register
def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        print("[SCHEDULER] Scheduler został zatrzymany.")

if __name__ == "__main__":
    # Uruchom scheduler przed startem aplikacji
    start_scheduler()
    app.run(host="0.0.0.0", port=5000, debug=True)