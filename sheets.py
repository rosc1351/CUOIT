from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import time
import json

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1p6t4qG76h26ChcaIIhpbAAZRx2BvvZ75-mfodP-60tA'
SAMPLE_RANGE_NAME = 'Form Responses 4!A2:B'

'''
BEGIN GOOGLE QUICKSTART
literally copied from the sheets API quickstart
so idk how it works

Make sure you have credentials.json from your API dashboard
Delete token.pickle on first run. You will log in through a browser to get a token
The token can be reused as long as the account is the same
'''
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid: # If there are no (valid) credentials available, let the user log in.
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server()
    with open('token.pickle', 'wb') as token: # Save the credentials for the next run
        pickle.dump(creds, token)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range=SAMPLE_RANGE_NAME).execute()
values = result.get('values', [])

#END GOOGLE QUICKSTART

times = []
rooms = []

if not values:
    print('No data found.')
else:
    for i,row in enumerate(values):
        if row[0] == '':
        	True == True
        else:
        	pattern = '%m/%d/%Y %H:%M:%S'
        	epoch = int(time.mktime(time.strptime(row[0],pattern)))
        	times.append(epoch)
        	rooms.append(row[1])

roomSet = sorted(set(rooms))

checks = {}
now = time.time()

for r in roomSet:
	l = 0
	for i,k in enumerate(rooms):
		if k == r and times[i] > l:
				l = times[i]
	checks[r] = [l, (now - l) / (60 * 60 * 24) ]

for k in checks:
	print(k, checks[k])

with open('data.json', 'w') as outfile:
	json.dump(checks,outfile)

#with open('data.json', 'rb') as outfile:
#	r = requests.post("https://oitcu.com/api/rooms.php", files={"data.txt":outfile})
#	print(r.text)
