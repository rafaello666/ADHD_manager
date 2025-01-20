# scheduler.py
import time
from apscheduler.schedulers.background import BackgroundScheduler
from main import remind_tasks

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Uruchamiaj przypomnienia co godzinę
    scheduler.add_job(remind_tasks, 'interval', hours=1)
    scheduler.start()

    print("Scheduler wystartował. Przerywam klawiszem CTRL+C.")
    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

if __name__ == "__main__":
    start_scheduler()
