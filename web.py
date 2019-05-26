from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import requests
import os
import time
import glob
import numpy as np
import pandas as pd
import json

import util

def fetch():
	url25live = "https://25live.collegenet.com/cusys/"
	os.environ["PATH"] += os.pathsep;
	downloadsPath = '/Users/royceschultz/Downloads/*.xlsx'

	driver = webdriver.Chrome() #points to chromedriver.exe
	driver.get(url25live) #go to website
	print("Waiting while application loads...")
	while True:
		try:
			driver.find_element_by_xpath("//div[@id='headerText']/span[4]").click()
			break
		except:
			True == True
	print("Username")
	while True:
		try:
			driver.find_element_by_id('LoginUserName').send_keys('warec')
			break
		except:
			True == True

	print("Password")
	while True:
		try:
			driver.find_element_by_id('LoginPassword').send_keys('OITv842')
			break
		except:
			True == True

	print("Logging in...")
	while True:
		try:
			driver.find_element_by_id('LoginBtn').click()
			break
		except:
			True == True
	time.sleep(2)

	print("Reports Tab")
	while True:
		try:
			driver.find_element_by_id('s25-tabitem-reports').click()
			break
		except:
			True == True

	print("Location Reports")
	while True:
		try:
			driver.find_element_by_xpath("//div[@id='ReportsSubtabs']/ul[1]/li[3]").click()
			break
		except:
			True == True

	print("Select Dropdown")
	while True:
		try:
			driver.find_element_by_xpath("//div[@class='ReportSelect space_reports']/select[1]/option[2]").click()
			break
		except:
			True == True

	zone = ["Daily Rooms", "Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5", "Zone 6", "Zone 7", "Zone 8", "Zone 9", "Zone 10"]
	myDict = {}
	for z in zone:
		print("Select Zone: ", z)
		while True:
			try:
				select = Select(driver.find_element_by_xpath("//*[@id='layout-tabbox-groups']/div[8]/div/div[3]/div/div[2]/table/tbody/tr[1]/td[2]/div[2]/div[2]/div[2]/div/div/div/select"))
				select.select_by_visible_text(z)
				break
			except:
				True == True

		print("Format (Excel)")
		while True:
			try:
				driver.find_element_by_xpath("//*[@id='layout-tabbox-groups']/div[8]/div/div[3]/div/div[2]/table/tbody/tr[1]/td[4]/div[2]/div/div[2]/label").click()
				break
			except:
				True == True

		newFile = util.getNewestFile(downloadsPath) #newest file before new report
		print("Run Report")
		while True:
			try:
				driver.find_element_by_xpath("//*[@id='layout-tabbox-groups']/div[8]/div/div[3]/div/div[2]/table/tbody/tr[2]/td/button/div").click()
				break
			except:
				True == True

		print("Waiting while file is created...")
		f = util.getNewestFile(downloadsPath)
		while f == newFile: #detect when report is downloaded
			f = util.getNewestFile(downloadsPath)
		df = pd.read_excel(io=f)
		myDict.update(util.readReport(df))

	with open('data.json', 'w') as outfile:
			json.dump(myDict,outfile)

	'''
	with open('data.json', 'rb') as outfile:
		r = requests.post("https://oitcu.com/api/rooms.php", files={"data.txt":outfile})
		print(r.text)
	'''

	driver.quit() #close out to be polite to the activity manager
