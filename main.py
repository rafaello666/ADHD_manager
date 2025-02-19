import os
import json
from flask import Flask, request, jsonify, session, redirect, url_for
from dotenv import load_dotenv

from taskmanager import init_db, add_task, mark_task_done, get_all_tasks, delete_task
from google_sync import get_google_flow, get_google_credentials, save_google_credentials, create_google_calendar_event, delete_google_calendar_event, sync_google_keep

# Importy dla powiadomień
from twilio.rest import Client
from pywebpush import webpush, WebPushException

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'supersecretkey')

# Inicjalizacja bazy danych
init_db()

# Konfiguracja Twilio
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_sms_via_twilio(to_number: str, message_body: str) -> str:
    message = twilio_client.messages.create(
        body=message_body,
        from_=TWILIO_NUMBER,
        to=to_number
    )
    return message.sid

# Konfiguracja Web Push (VAPID)
VAPID_PUBLIC_KEY = os.getenv("VAPID_PUBLIC_KEY")
VAPID_PRIVATE_KEY = os.getenv("VAPID_PRIVATE_KEY")
VAPID_CLAIMS = {"sub": "mailto:[email protected]"}  # // KOMENTARZ: Uzupełnij swój kontakt

# Przechowywanie subskrypcji (dla demo – w produkcji użyj bazy danych)
subscriptions = []

# Endpointy API

@app.route('/add_task', methods=['POST'])
def api_add_task():
    data = request.json
    title = data.get('title')
    deadline = data.get('deadline')
    is_cyclic = data.get('is_cyclic', False)
    
    if not title:
        return jsonify({"error": "Title is required"}), 400

    # Synchronizacja z Google Calendar, jeśli użytkownik jest zalogowany i podano deadline
    creds = get_google_credentials()
    google_event_id = None
    if creds and deadline:
        google_event_id = create_google_calendar_event(creds, {'title': title, 'deadline': deadline})

    task_id = add_task(title, deadline, is_cyclic, google_event_id)
    return jsonify({"status": "ok", "task_id": task_id})

@app.route('/mark_done', methods=['POST'])
def api_mark_done():
    data = request.json
    task_id = data.get('task_id')
    if not task_id:
        return jsonify({"error": "task_id is required"}), 400

    success = mark_task_done(task_id)
    return jsonify({"status": "ok"}) if success else (jsonify({"error": "Task not found"}), 404)

@app.route('/get_tasks', methods=['GET'])
def api_get_tasks():
    tasks = get_all_tasks()
    return jsonify(tasks)

@app.route('/delete_task', methods=['POST'])
def api_delete_task():
    data = request.json
    task_id = data.get('task_id')
    if not task_id:
        return jsonify({"error": "task_id is required"}), 400

    # Usuwanie wydarzenia z Google Calendar, jeśli istnieje
    tasks = get_all_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task and task.get('google_event_id'):
        creds = get_google_credentials()
        if creds:
            delete_google_calendar_event(creds, task['google_event_id'])
    
    success = delete_task(task_id)
    return jsonify({"status": "ok"}) if success else (jsonify({"error": "Task not found"}), 404)

# Powiadomienia SMS
@app.route('/notify/sms', methods=['POST'])
def notify_sms():
    data = request.json
    phone = data.get('phone')
    content = data.get('message')
    if not phone or not content:
        return jsonify({"error": "Brak numeru telefonu lub treści wiadomości"}), 400
    try:
        sid = send_sms_via_twilio(phone, content)
        return jsonify({"status": "SMS sent", "sid": sid}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Powiadomienia Web Push
@app.route('/subscribe', methods=['POST'])
def subscribe_push():
    subscription_info = request.get_json()
    if not subscription_info:
        return jsonify({"error": "Brak danych subskrypcji"}), 400
    subscriptions.append(subscription_info)
    return jsonify({"status": "subscribed"}), 201

@app.route('/notify/push', methods=['POST'])
def notify_push():
    data = request.get_json() or {}
    message = data.get("message", "Powiadomienie z ADHD Manager")
    if not subscriptions:
        return jsonify({"error": "Brak subskrybentów"}), 400

    errors = []
    for sub in subscriptions:
        try:
            webpush(
                subscription_info=sub,
                data=message,
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims=VAPID_CLAIMS
            )
        except WebPushException as ex:
            errors.append(repr(ex))
    status = "sent" if not errors else "partial failure"
    return jsonify({"status": status, "errors": errors}), 200

# Google OAuth2 – logowanie i synchronizacja
@app.route('/authorize')
def authorize():
    flow = get_google_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session.get('state')
    flow = get_google_flow()
    flow.fetch_token(authorization_response=request.url)
    creds = flow.credentials
    save_google_credentials(creds)
    return redirect(url_for('api_get_tasks'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
