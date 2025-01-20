# twilio_sms.py
import os
from twilio.rest import Client

account_sid = "AC858c345bb5670c5eeda6f77f27e7e750"
auth_token = "ff72bdb7768b11b467cecc094cb9865b"
from_number = "+1 6206759113"
to_number = "+48 514395284"  # docelowy

def send_sms(message: str):
    client = Client(account_sid, auth_token)
    msg = client.messages.create(
        body=message,
        from_=from_number,
        to=to_number
    )
    print("[SMS] Wysłano wiadomość:", msg.sid)
    return msg.sid
