# google_calendar.py

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import os.path
import pickle
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def authenticate_google_account():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens
    # and is created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Build the service to interact with Google Calendar API
    service = build('calendar', 'v3', credentials=creds)
    return service


def get_available_slots(service, start_date, end_date):
    # Get events from the Google Calendar for the specified date range
    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_date.isoformat() + 'Z',  # 'Z' indicates UTC time
        timeMax=end_date.isoformat() + 'Z',
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    busy_slots = []

    for event in events:
        busy_slots.append({
            'start': event['start']['dateTime'],
            'end': event['end']['dateTime'],
        })

    # Now, based on these busy slots, find the free time slots
    available_slots = []
    current_time = start_date
    work_day_start = datetime(current_time.year, current_time.month, current_time.day, 9, 0)
    work_day_end = datetime(current_time.year, current_time.month, current_time.day, 17, 0)

    # Loop through the day and check for free slots
    while current_time < work_day_end:
        free_time_start = current_time
        free_time_end = current_time + timedelta(hours=1)  # Let's assume 1-hour slots
        for busy_slot in busy_slots:
            if free_time_start < datetime.fromisoformat(busy_slot['end']) and free_time_end > datetime.fromisoformat(
                    busy_slot['start']):
                break
        else:
            available_slots.append({
                'start': free_time_start,
                'end': free_time_end,
            })
        current_time = free_time_end

    return available_slots
