from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import time
import json
import requests

'''
Uses google API to get roomcheck response data

Returns: None
Writes a dict to 'checks.json'
Key = roomName
Dict[Key] = [epochTime of last check, Days since last check]

Requirements:
1. NEED 'credentials.json' TO USE GOOGLE API
	download: console.developers.google.com/apis/credentials
2. NEED CORRECT 'token.pickle'
	delete the existing pickle file
	ensure you have the correct credentials file
	run fetch() and a popup window will prompt a login to your google account
	a new, reuable token will be automatically generated
'''
def fetch():
	print("Fetching response sheet data")
	SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
	SPREADSHEET_ID = '1p6t4qG76h26ChcaIIhpbAAZRx2BvvZ75-mfodP-60tA'
	RANGE_NAME = 'Form Responses 4!A2:B' #Get first and second columns, timestamp and roomName

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
	        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
	        creds = flow.run_local_server()
	    with open('token.pickle', 'wb') as token: pickle.dump(creds, token) # Save the credentials for the next run
	service = build('sheets', 'v4', credentials=creds)
	sheet = service.spreadsheets()
	result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
	values = result.get('values', [])
	#END GOOGLE QUICKSTART

	times = []
	rooms = []
	if not values:
	    print('No data found.')
	else:
		#Row = [timestamp, room]
	    for i,row in enumerate(values):
	        if row[0] == '':
	        	True == True
	        else:
	        	pattern = '%m/%d/%Y %H:%M:%S'
	        	epoch = int(time.mktime(time.strptime(row[0],pattern)))
	        	times.append(epoch)
	        	rooms.append(row[1])
	now = time.time()
	roomSet = sorted(set(rooms))
	checks = {}
	for r in roomSet: #For each unique room
		l = 0
		for i,k in enumerate(rooms): #find the maximum time
			if k == r and times[i] > l:
					l = times[i]
		checks[r] = [l, (now - l) / (60 * 60 * 24) ] #[Epoch time of latest check, days since last check]

	with open('checks.json', 'w') as outfile:
		json.dump(checks,outfile)
	print("Done fetching sheet data")
