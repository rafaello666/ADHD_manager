# calendar_monitor.py

"""
Moduł monitorujący kalendarz Google i wysyłający powiadomienia o nadchodzących wydarzeniach.
"""

from datetime import datetime
from typing import Optional

from google_calendar_integration import get_upcoming_events
from twilio_sms import send_sms

def check_calendar_and_notify():
    """
    Sprawdza najbliższe wydarzenia (start w ciągu 30 minut).
    Jeśli coś jest, wysyła SMS przez Twilio z krótką informacją.
    """
    events = get_upcoming_events(minutes_ahead=30)
    if not events:
        print("[CALENDAR] Brak wydarzeń w ciągu 30 minut.")
        return
    for ev in events:
        # ...existing code...
        title = ev.get("summary", "Bez tytułu")
        loc = ev.get("location", "Brak lokalizacji")
# ...existing code...
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
    """
    Oblicza różnicę czasu między teraz a czasem rozpoczęcia wydarzenia w minutach.

    Args:
        start_dt: Datetime rozpoczęcia wydarzenia.

    Zwraca:
        Liczba minut do rozpoczęcia wydarzenia (int).
    """
    now = datetime.now()
    diff = start_dt - now
    return int(diff.total_seconds() / 60)