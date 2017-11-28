from oauth2client.client import flow_from_clientsecrets
import pickle
import dbRequests
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'

def get_flow():
    flow = flow_from_clientsecrets.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES,redirect_uri='/google_auth_code')
    return flow

def get_step1(flow):
    return flow.step1_get_authorize_url(flow)

def set_credentials(code, userID, flow):
    credentials = flow.step2_exchange(code)
    my_pickle = pickle.dumps()
    dbRequests.setGoogleCredentials(userID, my_pickle)





