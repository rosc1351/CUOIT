import pandas as pd
import glob
import os
import json

'''
Parses 25live location report provided in the form of a pandas dataframe (df)
Format:
0. DATE
1. Room1
2. Event Times, Event, Contact
3. --
4. No Events
5. Room2
6. Event Times, Event, Contact
3. event1
4. Room3
5. ...

RETURNS: A dictionary with roomNames as keys and lists of bookings as values

Utilized in web.py to parse location reports before saving as a .json
'''
def readReport(newFile):
	df = pd.read_excel(io=newFile)
	(m,n) = df.shape
	i = 1
	myDict = {}
	while i < m: #Read line by line until end of list
		cell = df.iloc[i,0] #get the cell at the index
		if cell == "Event Times":
			room = df.iloc[i-1,0]
			schedTime = []
			print(room)
			while i+2 < m and df.iloc[i+2,0] != "Event Times":
				i += 1
				t = df.iloc[i,0] #Cell may be empty == NaN
				print(t)
				if t == t: #if cell is not empty == NOT NaN
					t = t.replace(' ','') #Strip spaces for easier parsing later
					schedTime.append(t)
			if i+2 == m: #If at end of list
				         #Second (and) condition in the while loop will fail due to index range
				i += 1
				t = df.iloc[i,0]
				if t == t:
					t = t.replace(' ','')
					schedTime.append(t)
			myDict[room] = schedTime
		i += 1
	return myDict

'''
RETURNS: paththe newest file in the given folder

Utilized in web.py to detect when a new file is created by the 25live report generator
'''
def getNewestFile(path):
	#path of form: '/Users/user1/folder/*.xlsx'
	#*. specifies file format in folder
	return max(glob.glob(path), key=os.path.getctime)
