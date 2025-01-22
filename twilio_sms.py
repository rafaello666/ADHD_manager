# twilio_sms.py

"""
Moduł odpowiedzialny za wysyłanie SMS-ów za pomocą Twilio.
"""

import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.getenv("TWILIO_FROM_NUMBER")
TWILIO_TO = os.getenv("TWILIO_TO_NUMBER")

def send_sms(message: str):
    """
    Wysyła SMS z podaną treścią.

    Args:
        message: Treść wiadomości SMS.
    """
    if not TWILIO_SID or not TWILIO_TOKEN:
        print("[TWILIO] Brak SID/TOKEN w zmiennych środowiskowych, nie wysyłam SMS.")
        return
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    try:
        msg = client.messages.create(
            body=message,
            from_=TWILIO_FROM,
            to=TWILIO_TO
        )
        print("[SMS] Wysłano wiadomość:", msg.sid)
    except Exception as e:
        print(f"[SMS] Błąd podczas wysyłania wiadomości: {e}")