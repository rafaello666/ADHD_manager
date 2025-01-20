# server.py

from flask import Flask, render_template, request, redirect, url_for, jsonify
import time
from tasks import get_all_tasks, save_task, complete_task, remove_task, _save_tasks_to_file
from calculations import calculate_priority

app = Flask(__name__)

@app.route("/")
def home():
    tasks = get_all_tasks()
    now = time.time()

    # Przelicz priorytety i wyłącz timery, które upłynęły
    for t in tasks:
        prio = calculate_priority(t)
        t["priority"] = prio

        if t.get("timer_running"):
            end_ts = t.get("timer_end", 0)
            if now >= end_ts:
                t["timer_running"] = False
                t["timer_end"] = None
                save_task(t)

    tasks_sorted = sorted(tasks, key=lambda x: x["priority"], reverse=True)
    total = len(tasks_sorted)
    completed_count = sum(1 for x in tasks_sorted if x.get("completed"))
    not_completed_count = total - completed_count
    completion_ratio = (completed_count / total * 100) if total else 0

    # Przekazujemy też czas serwera do synchronizacji w JS
    server_now = time.time()

    return render_template(
        "index.html",
        tasks=tasks_sorted,
        total_tasks=total,
        completed_tasks=completed_count,
        not_completed=not_completed_count,
        completion_ratio=round(completion_ratio, 1),
        server_now=server_now
    )

@app.route("/tasks/<task_id>/complete", methods=["POST"])
def complete_task_route(task_id):
    """
    Dla recurring -> ustawia completed=True
    Dla jednorazowych -> remove_task
    """
    tasks = get_all_tasks()
    task = next((x for x in tasks if x["id"] == task_id), None)
    if not task:
        return "Nie znaleziono zadania", 404

    if task.get("recurring", False):
        ok = complete_task(task_id)
        if ok:
            return redirect(url_for("home"))
        else:
            return "Błąd: nie da się odhaczyć", 404
    else:
        removed = remove_task(task_id)
        if removed:
            return redirect(url_for("home"))
        else:
            return "Błąd: nie znaleziono do usunięcia", 404

@app.route("/tasks/<task_id>/remove", methods=["POST"])
def remove_task_route(task_id):
    tasks = get_all_tasks()
    t = next((x for x in tasks if x["id"] == task_id), None)
    if not t:
        return "Nie znaleziono zadania", 404

    rem = remove_task(task_id)
    if rem:
        return redirect(url_for("home"))
    else:
        return "Błąd: nie znaleziono do usunięcia", 404

@app.route("/tasks/<task_id>/edit", methods=["GET","POST"])
def edit_task_route(task_id):
    tasks = get_all_tasks()
    task_to_edit = next((x for x in tasks if x["id"] == task_id), None)
    if not task_to_edit:
        return "Nie znaleziono zadania", 404

    if request.method == "POST":
        # Zmiana tytułu
        task_to_edit["title"] = request.form.get("title", task_to_edit["title"])

        # Zmiana est_time
        et_str = request.form.get("estimated_time","")
        if et_str:
            try:
                et_val = float(et_str)
                task_to_edit["estimated_time"] = et_val
            except ValueError:
                pass

        # Tagi
        tags_str = request.form.get("tags","")
        if tags_str:
            task_to_edit["tags"] = tags_str

        # Subtasks
        subs_str = request.form.get("subtasks","").strip()
        if subs_str:
            st_list = [s.strip() for s in subs_str.split(",")]
            task_to_edit["subtasks"] = st_list

        save_task(task_to_edit)
        return redirect(url_for("home"))
    else:
        # Uwaga: tu zmieniamy "edit_tasks.html" na "edit_task.html"
        return render_template("edit_task.html", task=task_to_edit)

@app.route("/tasks/archive_completed", methods=["POST"])
def archive_completed():
    tasks = get_all_tasks()
    new_tasks = [x for x in tasks if not x.get("completed")]
    _save_tasks_to_file(new_tasks)
    return redirect(url_for("home"))

@app.route("/tasks/search", methods=["GET"])
def search_tasks():
    query = request.args.get("q","").lower()
    tasks = get_all_tasks()
    filtered = []
    for t in tasks:
        title = t["title"].lower() if t["title"] else ""
        tags = t.get("tags","").lower()
        if query in title or (query and query in tags):
            filtered.append(t)
    return jsonify(filtered)

##########################
# TIMERY (GLOBALNE)
##########################
@app.route("/tasks/<task_id>/start_timer", methods=["POST"])
def start_timer_route(task_id):
    tasks = get_all_tasks()
    task = next((x for x in tasks if x["id"] == task_id), None)
    if not task:
        return "Nie znaleziono zadania", 404

    # Wyłączamy timery w innych zadaniach, aby w danej chwili tylko jeden był aktywny
    for t in tasks:
        if t["id"] != task_id and t.get("timer_running"):
            t["timer_running"] = False
            t["timer_end"] = None
            save_task(t)

    est = float(task.get("estimated_time", 0))
    if est <= 0:
        # Brak sensownego czasu => zignoruj
        return redirect(url_for("home"))

    now_ts = time.time()
    end_ts = now_ts + (est * 3600)
    task["timer_running"] = True
    task["timer_end"] = end_ts
    save_task(task)
    return redirect(url_for("home"))

@app.route("/tasks/<task_id>/stop_timer", methods=["POST"])
def stop_timer_route(task_id):
    tasks = get_all_tasks()
    task = next((x for x in tasks if x["id"] == task_id), None)
    if not task:
        return "Nie znaleziono zadania", 404

    task["timer_running"] = False
    task["timer_end"] = None
    save_task(task)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
