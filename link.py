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

'''
Datagrid class in selenium requires an itteratable, get_item(item) callable datatype
A list of dictionaries satisfies these requirements
Each index in the list is a row, each key in the dict is a column
the Tab class handles creation of a datatable with the following columns:
room, book, check, day, available
'''
class Tab():
	#Initialize empty list
	def __init__(self):
		self.table = []

	#Creates an empty row and returns the row to edit in the parent function
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

	#Insertion sort a list of dictionaries by the key, criteria
	#Returns a deepcopy of the list so zone order is preserved on table
	#TODO: better order the list to distinguish daily rooms from other rooms, currently dailys are just first in list
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
'''
Import .json files into localTable = Tab()
Significantly faster than online database
TODO: Consider switching to standard table like mySQL

Returns: None
Populates local table with roomNames,
	a list of book times,
	the epoch time of the last check,
	and the days since the last check

Availability is calculated in findAvailability()
'''
@anvil.server.callable
def loadData():
	try:
		bookFile = 'reports.json'
		with open(bookFile, 'r') as f:
			if f is not None:
				books = json.load(f)
	except:
		print('book file DNE')
		books = {}

	try:
		checkFile = 'checks.json'
		with open(checkFile) as f:
			if f is not None:
				checks = json.load(f)
	except:
		print('check file DNE')
		checks{}

	print("Loading data to localTable")
	for k in books: #Only consider rooms in 25 live (though, no other rooms should exist in the response form)
		c = 0
		d = 999
		if k in checks:
			c = checks[k][0]
			d = int(checks[k][1]) #Round to floor(day)
		y = localTable.findRoom(k) #check if the room already exists in the list
		if y == None: #if it doesnt exist, add it
			y = localTable.addRow()
			y['room'] = k
		y['book'] = books[k]
		y['check'] = c
		y['day'] = d
	print("Done loading data to localTable")
	findAvailability()

'''
IN PROGRESS
Indended to backup data to online database
Backup so we can print list if raspPi server goes down
'''
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

'''
findAvailability reads from localTable to calculate when each room is available
time and datetime are heavily used in the calculations

Returns: None
Updates localTable['availability'] for all rooms
if 'availability' > 0, minutes until book
elif 'availability' < 0, minutes until open
'''
@anvil.server.callable
def findAvailability():
	print("Calculating Availability...")
	now = datetime.datetime.now()
	today = datetime.date.today()
	for row in localTable.table:
		books = row['book']
		row['available'] = 0
		t = '11:59PM'
		t = datetime.datetime.strptime(t, '%I:%M%p').time()
		t = datetime.datetime.combine(today,t)
		minTimeUntilClose = (t-now).total_seconds()/60
		for events in books:
			if events == "Noevents":
				True == True
			else:
				t = events.split('-')
				if len(t) == 1:
					print("Unexpected book format:", t)
					continue
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

'''
Fetch all data and post it to localTable

DOES NOT POST TO WEB
'''
@anvil.server.callable
def fetchData():
	web.fetch()
	sheets.fetch()
	loadData()

'''
Fetch sheet reponse data and post it to localTable

DOES NOT POST TO WEB
'''
@anvil.server.callable
def fetchSheet():
	sheets.fetch()
	loadData()

'''
Parse sort settings and return a list of dictionaries to populate datagrid in website
'''
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
