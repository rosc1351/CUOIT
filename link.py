import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

import json
import time
import datetime
import copy

import web
import sheets

class Tab():
	def __init__(self):
		self.table = []

	def addRow(self):
		data = {}
		data['room'] = ""
		data['book'] = []
		data['check'] = 0
		data['days'] = 999
		data['available'] = 0
		self.table.append(data)
		return data

	def findRoom(self, room):
		for row in self.table:
			if row['room'] == room:
				return row
		return None

	def newSortedList(self, criteria):
		s = copy.deepcopy(self.table)
		l = len(s)
		for i in range(l):
			for j in range(i):
				if s[i][criteria] < s[j][criteria]:
					x = s.pop(i)
					s.insert(j,x)
					break
		return s

@anvil.server.callable
def loadData():
	bookFile = 'data.json'
	checkFile = 'checks.json'
	with open(bookFile, 'r') as f:
		books = json.load(f)
	with open(checkFile) as f:
		checks = json.load(f)
	print("Uploading .json files to database")
	for k in books:
		c = 0
		d = 999
		if k in checks:
			c = checks[k][0]
			d = int(checks[k][1])
		y = localTable.findRoom(k)
		if y:
			y['book'] = books[k]
			y['check'] = c
			y['day'] = d
		else:
			y = localTable.addRow()
			y['room'] = k
			y['book'] = books[k]
			y['check'] = c
			y['day'] = d

	print("Done uploading .json files to database")
	findAvailability()

@anvil.server.callable
def backupTable():
	for row in localTable.table:
		x = app_tables.booking.get(room = row['room'])
		if x:
			x['book'] = row['book']
			x['check'] = row['check']
			x['day'] = row['day']
		else:
			app_tables.booking.add_row(room = row['room'],
			                           book = row['book'],
			                           check = row['check'],
			                           day = row['day'])


def findAvailability():
	print("Calculating Availability...")
	now = datetime.datetime.now()
	today = datetime.date.today()
	for row in localTable.table:
		books = row['book']
		row["available"] = 0
		t = '11:59PM'
		t = datetime.datetime.strptime(t, '%I:%M%p').time()
		t = datetime.datetime.combine(today,t)
		minTimeUntilClose = (t-now).total_seconds()/60
		for events in books:
			if events == "Noevents":
				True == True
			else:
				t = events.split('-')
				if t[0] == "contd":
					t[0] = "12:01AM"
				if t[1] == "contd":
					t[1] = "11:59PM"
				start = datetime.datetime.strptime(t[0], '%I:%M%p').time()
				start = datetime.datetime.combine(today,start)
				end = datetime.datetime.strptime(t[1], '%I:%M%p').time()
				end = datetime.datetime.combine(today,end)

				if start < now and end > now: #if booked
					row["available"] = (now - end).total_seconds()/60
				elif start > now:
					timeUntil = (start-now).total_seconds()/60
					if timeUntil < minTimeUntilClose:
						minTimeUntilClose = timeUntil
		if row['available'] == 0:
			row['available'] = minTimeUntilClose
	print("Done calculating availability")

@anvil.server.callable
def fetchData():
	print("Fetching data from 25Live")
	web.fetch()
	print("Done fetching data from 25Live")
	print("Fetching response sheet data")
	sheets.fetch()
	print("Done fetching sheet data")
	postData()

@anvil.server.callable
def fetchSheet():
	print("Fetching response sheet data")
	sheets.fetch()
	print("Done fetching sheet data")
	postData()

@anvil.server.callable
def get_dispData(criteria, inc):
	print(criteria)
	if inc == 'Increasing':
		inc = True
	else:
		inc = False
	if criteria == 'Zone':
		r = localTable.table
	elif criteria == 'Room':
		if inc:
			r = localTable.newSortedList('room')
		else:
			r = localTable.newSortedList('room')[::-1]
	elif criteria == 'Days':
		if inc:
			r = localTable.newSortedList('day')
		else:
			r = localTable.newSortedList('day')[::-1]
	elif criteria == 'Available':
		if inc:
			r = localTable.newSortedList('available')
		else:
			r = localTable.newSortedList('available')[::-1]

	r = [d for d in r if d['day'] > 14]
	r = [d for d in r if d['available'] > 0]
	return r

anvil.server.connect("XJPM266UCJKWY3D4IQELSDLD-KO4OTPRMQVUUFNTP")
localTable = Tab()
anvil.server.wait_forever()
