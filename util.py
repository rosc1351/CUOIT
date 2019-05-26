import numpy as np
import pandas as pd
import glob
import os
import json
import requests

def readReport(df):
	(m,n) = df.shape
	i = 1
	myDict = {}
	while i < m:
		cell = df.iloc[i,0]
		if cell == "Event Times":
			room = df.iloc[i-1,0]
			schedTime = []
			while i+2 < m and df.iloc[i+2,0] != "Event Times":
				i += 1
				t = df.iloc[i,0]
				if t == t:
					t = t.replace(' ','')
					schedTime.append(t)
			if i+2 == m:
				i += 1
				t = df.iloc[i,0]
				if t == t:
					t = t.replace(' ','')
					schedTime.append(t)
			myDict[room] = schedTime
		i += 1
	return myDict

def getNewestFile(path):
	#path of form: '/Users/royceschultz/Downloads/*.xlsx'
	#*. specifies file format in folder
	return max(glob.glob(path), key=os.path.getctime)

def testPost(link):
	myDict = {}
	myDict['OIT'] = 'sux'
	myDict['oitcu'] = '.com'
	print(myDict)

	with open('testPost.json', 'w') as outfile:
		json.dump(myDict,outfile)

	'''
	with open('testPost.json','rb') as outfile:
		r = requests.post(link, files={"data.txt":outfile})
		print(r.text)
	'''
