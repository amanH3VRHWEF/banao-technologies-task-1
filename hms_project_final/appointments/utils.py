from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def create_google_calendar_event(user, slot):
    creds = Credentials(token=user.token, refresh_token=user.refresh_token)
    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': f'Doctor Appointment: {slot.doctor.name}',
        'start': {'dateTime': slot.start_time.isoformat()},
        'end': {'dateTime': slot.end_time.isoformat()},
        'attendees': [{'email': user.email}],
    }
    
    event = service.events().insert(calendarId='primary', body=event).execute()
    return event.get('htmlLink')
