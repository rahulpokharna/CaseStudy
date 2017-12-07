from oauth2client.client import flow_from_clientsecrets
import pickle
import dbRequests
import httplib2
from apiclient import discovery
import datetime
import json
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly',
          'https://www.googleapis.com/auth/userinfo.profile']
CLIENT_SECRET_FILE = 'client_secret.json'
REDIRECT_URI = 'http://localhost:5000/google_auth_code'
def get_flow():
    flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES, redirect_uri=REDIRECT_URI)
    return flow

def get_step1(flow):
    return flow.step1_get_authorize_url()

def set_credentials(code, userID, flow):
    credentials = flow.step2_exchange(code)
    my_pickle = pickle.dumps(credentials)
    dbRequests.setGoogleCredentials(userID, my_pickle)

def add_events(pickled_credentials, userId):
    credentials = pickle.loads(pickled_credentials)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=100, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    for event in events:
        # c.execute('INSERT INTO event VALUES(:EventID, :UserID, :Start, :End, :Description, :ImportanceRanking, :Title, :ProgramID, :EventType, :StudyPlan, :StudyType, :Color, :Recurring)', tempEvent)
        eventDict = {}
        eventDict['UserID'] = userId
        if 'dateTime' in event['start']:
            eventDict['Start'] = event['start']['dateTime']
        else:
            eventDict['Start'] = event['start']['date']

        if 'dateTime' in event['end']:
            eventDict['End'] = event['end']['dateTime']
        else:
            eventDict['End'] = event['end']['date']

        eventDict['Description'] = 'Google Event'
        eventDict['Title'] = event['summary']
        dbRequests.addNewEvent(eventDict)
    return len(events)

def profileImage(pickled_credentials):
    credentials = pickle.loads(pickled_credentials)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('plus', 'v1', http=http)
    people = service.people()
    request = people.get(userId='me')
    me = request.execute()
    if 'image' in me:
        image = me['image']
        if 'url' in image:
            return image['url']
    return None


