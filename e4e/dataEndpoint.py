import os
import pickle
import datetime as dt
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import IPython
import pandas as pd
import pytz

def authenticate(SCOPES, credentialsPath):
    creds = None
    if os.path.exists('aa2.pickle'):
        with open('aa2.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentialsPath, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next runwith open('aa2.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def getData(credentialsFile):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SPREADSHEET_ID = '1UvvFQRp5lwRD6BSit4_Rpjb6enjxjdhKmQNzOmhE1j4'
    DATA_RANGE_NAME = 'Sheet1'

    creds = authenticate(SCOPES, credentialsFile)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=DATA_RANGE_NAME).execute()
    values = result.get('values', [])
    df = pd.DataFrame(values[1:], columns=values[0])
    timezone = pytz.timezone('UTC')
    df['Publish Timestamp'] = [timezone.localize(dt.datetime.strptime(timestamp.strip('Z') + '000', "%Y-%m-%dT%H:%M:%S.%f")) for timestamp in df['published_at']]
    return df

if __name__ == "__main__":
    df = getData('credentials.json')
    IPython.embed()