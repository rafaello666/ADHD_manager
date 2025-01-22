# google_calendar_integration.py

"""
Moduł integrujący się z Google Calendar API w celu pobierania wydarzeń.
"""

import os
import pickle
from datetime import datetime, timedelta
from typing import List, Dict

from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.pickle'

def get_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)
    return service

def get_upcoming_events(minutes_ahead: int = 30) -> List[Dict]:
    """
    Pobiera nadchodzące wydarzenia z kalendarza.

    Args:
        minutes_ahead: Liczba minut do przodu, w której szukamy wydarzeń.

    Zwraca:
        Listę słowników z informacjami o wydarzeniach.
    """
    service = get_service()
    if not service:
        return []

    now = datetime.utcnow()
    max_time = now + timedelta(minutes=minutes_ahead)

    try:
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now.isoformat() + 'Z',  # 'Z' oznacza UTC
            timeMax=max_time.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        upcoming_events = []
        for event in events:
            start_str = event['start'].get('dateTime', event['start'].get('date'))
            start_dt = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
            upcoming_events.append({
                'summary': event.get('summary', 'Bez tytułu'),
                'location': event.get('location', 'Brak lokalizacji'),
                'start': start_dt
            })
        return upcoming_events
    except HttpError as err:
        print("[CAL] Błąd pobierania wydarzeń:", err)
        return []