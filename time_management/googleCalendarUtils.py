import os.path
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from datetime import datetime
from calendar import monthrange
from .models import TimePeriod
import google.oauth2.credentials
import google_auth_oauthlib.flow

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly','https://www.googleapis.com/auth/drive.metadata.readonly']
CLIENT_SECRETS_FILE = "time_management/credentials.json"
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'

def end_of_month(datetext):
    """ for given date function checks month and returns end of this month in  isoformat"""
    now = datetext.split("T")
    date_now = [ int(x) for x in now[0].split("-") ] # today in format [year,month,day]
    now[1] = now[1][:-1] # delete Z to easy cast string -> int
    time_now = [ int(float(x)) for x in now[1].split(":") ] # "now" time in format [hour,minute,second]
    end_of_month_day = monthrange(date_now[0],date_now[1])[1]
    end_of_month_date = datetime(date_now[0],date_now[1],end_of_month_day,23,59,59).isoformat()
    return end_of_month_date + 'Z'


def save_data(request, start_event, end_event, name):
    if 'T' in start_event and 'T' in end_event:
        start_data = start_event.split('T')
        end_data = end_event.split('T')
        date_s = start_data[0]
        start_hour = start_data[1].split('+')[0]
        end_hour = end_data[1].split('+')[0]
        temp = TimePeriod(person = request.user , day = date_s, start_hour = start_hour, end_hour = end_hour, time_type = 'O', time_name = name)
        # if so there's no duplicates
        if not TimePeriod.objects.filter(person = request.user , day = date_s, start_hour = start_hour, end_hour = end_hour, time_type = 'O', time_name = name).exists():
            temp.save()
            return True
    return False

def get_google_authentication_url(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('time_management/credentials.json',scopes=SCOPES)
    flow.redirect_uri = 'https://walkk-for-the-dog.herokuapp.com/calendar/oauth2callback/'
    authorization_url, state = flow.authorization_url(
    access_type='online',
    include_granted_scopes='true')
    return authorization_url

def load_data(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = "https://walkk-for-the-dog.herokuapp.com/calendar/oauth2callback/"
    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)
    creds = flow.credentials
    service = build('calendar', 'v3', credentials=creds)
    calendar_list = service.calendarList().list(showHidden = True).execute()
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    for calendar in calendar_list['items']:
        events_result = service.events().list(calendarId=calendar['id'], timeMin = now, timeMax = end_of_month(now), singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            print('No upcoming events found.')
        else:
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end_event = event['end'].get('dateTime', event['end'].get('date'))
                save_data(request, start, end_event, event['summary'])