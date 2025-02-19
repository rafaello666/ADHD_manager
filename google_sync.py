import os
from flask import session, redirect, url_for, request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

# Konfiguracja Google
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/keep'
]

def get_google_flow():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [GOOGLE_REDIRECT_URI]
            }
        },
        scopes=SCOPES
    )
    flow.redirect_uri = GOOGLE_REDIRECT_URI
    return flow

def get_google_credentials():
    if 'credentials' not in session:
        return None
    credentials_data = session['credentials']
    return Credentials(**credentials_data)

def save_google_credentials(creds):
    session['credentials'] = {
        'token': creds.token,
        'refresh_token': creds.refresh_token,
        'token_uri': creds.token_uri,
        'client_id': creds.client_id,
        'client_secret': creds.client_secret,
        'scopes': creds.scopes
    }

def create_google_calendar_event(creds, task):
    service = build('calendar', 'v3', credentials=creds)
    event = {
        'summary': task['title'],
        'start': {
            'dateTime': task['deadline'] if task['deadline'] else '2025-01-01T09:00:00',  # // KOMENTARZ: Uzupełnij domyślną datę, jeśli brak deadline
            'timeZone': 'Europe/Warsaw'
        },
        'end': {
            'dateTime': task['deadline'] if task['deadline'] else '2025-01-01T10:00:00',
            'timeZone': 'Europe/Warsaw'
        }
    }
    created_event = service.events().insert(calendarId='primary', body=event).execute()
    return created_event.get('id')

def update_google_calendar_event(creds, google_event_id, task):
    service = build('calendar', 'v3', credentials=creds)
    event = service.events().get(calendarId='primary', eventId=google_event_id).execute()
    event['summary'] = task['title']
    if task['deadline']:
        event['start'] = {'dateTime': task['deadline'], 'timeZone': 'Europe/Warsaw'}
        event['end'] = {'dateTime': task['deadline'], 'timeZone': 'Europe/Warsaw'}
    updated_event = service.events().update(calendarId='primary', eventId=google_event_id, body=event).execute()
    return updated_event

def delete_google_calendar_event(creds, google_event_id):
    service = build('calendar', 'v3', credentials=creds)
    service.events().delete(calendarId='primary', eventId=google_event_id).execute()
    return True

def sync_google_keep(creds, task):
    # // KOMENTARZ: Google Keep nie posiada oficjalnego API.
    # Możesz rozważyć użycie zewnętrznych narzędzi lub bibliotek reverse-engineered.
    return True
