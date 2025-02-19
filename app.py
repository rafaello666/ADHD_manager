# app.py (fragment)
import os
from flask import Flask, request, jsonify
from twilio.rest import Client
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

app = Flask(__name__)

# Konfiguracja Twilio z .env
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# Inicjalizacja klienta Twilio
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_sms_via_twilio(to_number: str, message_body: str) -> str:
    """Wysyła SMS za pomocą Twilio API. Zwraca SID wysłanej wiadomości."""
    message = twilio_client.messages.create(
        body=message_body,
        from_=TWILIO_NUMBER,
        to=to_number
    )
    return message.sid

# Endpoint Flask do wysyłki SMS (np. wywoływany gdy trzeba wysłać powiadomienie)
@app.route("/notify/sms", methods=["POST"])
def notify_sms():
    data = request.get_json()
    phone = data.get("phone")      # numer telefonu użytkownika
    content = data.get("message")  # treść powiadomienia
    if not phone or not content:
        return jsonify({"error": "Brak numeru telefonu lub treści wiadomości"}), 400

    try:
        sid = send_sms_via_twilio(phone, content)
        return jsonify({"status": "SMS sent", "sid": sid}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
