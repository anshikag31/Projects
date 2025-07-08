import datetime
import dateparser
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dateparser import parse as parse_date
from datetime import timedelta

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'service_account.json'
CALENDAR_ID = 'anshikagoel3108@gmail.com'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)

def parse_future_datetime(text: str):
    dt = dateparser.parse(
        text,
        settings={
            'PREFER_DATES_FROM': 'future',
            'RELATIVE_BASE': datetime.datetime.now()
        }
    )
    if not dt:
        return None
    return dt


def check_availability(start_text: str, end_text: str) -> str:
    start_dt = parse_time(start_text)
    end_dt = parse_time(end_text)

    if not start_dt or not end_dt:
        return "❌ Could not parse start or end time."

    start_iso = start_dt.isoformat()
    end_iso = end_dt.isoformat()

    # Append timezone offset if missing (RFC3339 format)
    if start_dt.tzinfo is None:
        start_iso += "+05:30"
    if end_dt.tzinfo is None:
        end_iso += "+05:30"

    print(f"🔍 Checking availability from {start_iso} to {end_iso}")

    try:
        events_result = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=start_iso,
            timeMax=end_iso,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        return "✅ Available" if len(events) == 0 else "❌ Not available"
    except Exception as e:
        return f"❌ Error checking availability: {e}"

def book_appointment(summary, start_time, end_time=None):
    start_dt = dateparser.parse(
        start_time,
        settings={
            'PREFER_DATES_FROM': 'future',
            'RELATIVE_BASE': datetime.datetime.now()
        }
    )
    if not start_dt:
        return "❌ Could not understand the start time."

    if end_time:
        end_dt = dateparser.parse(
            end_time,
            settings={
                'PREFER_DATES_FROM': 'future',
                'RELATIVE_BASE': datetime.datetime.now()
            }
        )
    else:
        end_dt = start_dt + timedelta(minutes=30)

    start_iso = start_dt.isoformat()
    end_iso = end_dt.isoformat()

    event = {
        'summary': summary,
        'start': {'dateTime': start_iso, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_iso, 'timeZone': 'Asia/Kolkata'},
    }

    try:
        service.events().insert(calendarId=CALENDAR_ID, body=event).execute()

        # Human-readable format
        readable_start = start_dt.strftime("%A, %d %B %Y at %I:%M %p")
        readable_end = end_dt.strftime("%I:%M %p")

        return f"✅ Meeting booked on {readable_start} to {readable_end}."
    except Exception as e:
        return f"❌ Error booking meeting: {e}"
