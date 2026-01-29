import os.path
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']


def add_event_to_calendar(doctor_email, patient_email, start_time_str):
    creds = None
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': 'HMS Medical Appointment',
        'description': f'Appointment between {doctor_email} and {patient_email}',
        'start': {
            'dateTime': start_time_str,  # Format: '2023-10-28T09:00:00Z'
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': start_time_str,
            'timeZone': 'UTC',
        },
        'attendees': [
            {'email': doctor_email},
            {'email': patient_email},
        ],
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    return event.get('htmlLink')