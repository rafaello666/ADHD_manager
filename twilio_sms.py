import os
from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()  # wczyta zmienne z pliku .env

# Pobieramy zmienne środowiskowe – tam ma być SID, TOKEN itd.
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_number = os.getenv("TWILIO_FROM_NUMBER")  # np. numer przydzielony przez Twilio
to_number = os.getenv("TWILIO_TO_NUMBER")      # Twój docelowy numer

def send_sms(message: str):
    if not account_sid or not auth_token:
        print("[ERROR] Brak danych uwierzytelniających Twilio (SID / TOKEN).")
        return None

    client = Client(account_sid, auth_token)
    msg = client.messages.create(
        body=message,
        from_=from_number,
        to=to_number
    )
    print("[SMS] Wysłano wiadomość:", msg.sid)
    return msg.sid
