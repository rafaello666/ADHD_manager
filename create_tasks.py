import json
import os

DATA_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(DATA_FILE):
        print(f"Plik {DATA_FILE} nie istnieje. Nie ma czego modyfikować!")
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        print(f"Błąd przy wczytywaniu {DATA_FILE} - możliwe, że jest uszkodzony.")
        return []

def save_tasks(tasks_list):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks_list, f, indent=2, ensure_ascii=False)

def ask_yes_no(prompt_text):
    while True:
        ans = input(prompt_text + " [t/n]: ").strip().lower()
        if ans in ["t", "tak", "y", "yes"]:
            return True
        elif ans in ["n", "nie", "no"]:
            return False
        else:
            print("Wpisz 't' lub 'n'.")

def ask_string(prompt_text, default=None):
    val = input(f"{prompt_text} (obecnie: {default}): ").strip()
    if val == "":
        return default
    return val

def ask_integer_or_none(prompt_text, default=None):
    print(f"{prompt_text} (obecnie: {default}), wpisz 1–10, 'NIE WIEM' lub Enter, żeby zostawić bez zmian.")
    ans = input("→ ").strip().upper()
    if ans == "":
        return default
    if ans == "NIE WIEM":
        return None
    try:
        val = int(ans)
        if 1 <= val <= 10:
            return val
        else:
            print("Nieprawidłowy zakres. Zostawiam bez zmian.")
            return default
    except ValueError:
        print("Nieprawidłowa wartość. Zostawiam bez zmian.")
        return default

def modify_task(task):
    print(f"\n--- Modyfikacja zadania ID='{task['id']}' (tytuł: {task['title']}) ---")
    # 1. Completed?
    print(f"Obecny status 'completed': {task.get('completed', False)}")
    if ask_yes_no("Czy chcesz zmienić status ukończenia?"):
        new_status = ask_yes_no("Czy zadanie jest ukończone teraz?")
        task["completed"] = new_status

    # 2. recurring?
    old_recurring = task.get("recurring", False)
    if ask_yes_no(f"Obecnie recurring={old_recurring}. Zmienić to?"):
        new_recurring = ask_yes_no("Czy zadanie jest cykliczne?")
        task["recurring"] = new_recurring
        if new_recurring:
            old_pattern = task.get("recurrence_pattern", "")
            new_pattern = ask_string("Wpisz wzorzec powtarzania (np. 'daily')", default=old_pattern)
            task["recurrence_pattern"] = new_pattern
        else:
            task["recurrence_pattern"] = None

    # 3. deadline_strictness
    old_deadline = task.get("deadline_strictness", None)
    new_deadline = ask_integer_or_none("deadline_strictness", default=old_deadline)
    task["deadline_strictness"] = new_deadline

    # 4. description
    old_desc = task.get("description", "")
    print(f"Obecny opis: {old_desc}")
    new_desc = ask_string("Nowy opis? (Enter = bez zmian)", default=old_desc)
    task["description"] = new_desc

    # 5. notes
    old_notes = task.get("notes", "")
    print(f"Obecne notatki: {old_notes}")
    new_notes = ask_string("Nowe notatki? (Enter = bez zmian)", default=old_notes)
    task["notes"] = new_notes

def main():
    print(f"Skrypt do modyfikacji istniejących zadań w pliku {DATA_FILE}.\n")

    tasks_list = load_tasks()
    if not tasks_list:
        print("Brak zadań do modyfikacji (lub plik nie istnieje). Kończę.")
        return

    print(f"Aktualnie jest {len(tasks_list)} zadań w {DATA_FILE}.")
    print("Za chwilę przejdziemy przez każde zadanie i spytamy, czy je modyfikować.\n")

    for task in tasks_list:
        print(f"ID: {task['id']}, Title: {task.get('title','(brak)')}, Completed={task.get('completed',False)}")
        do_mod = ask_yes_no("Czy chcesz zmodyfikować to zadanie?")
        if do_mod:
            modify_task(task)
        else:
            print("Pomijam.\n")

    save_tasks(tasks_list)
    print(f"\nZapisano wszystkie zmiany do {DATA_FILE}. Dziękuję!")

if __name__ == "__main__":
    main()
