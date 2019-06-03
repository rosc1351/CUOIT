from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import requests
import os
import glob
import pandas as pd
import json
import time

#Local dependencies
import util

'''
Fetch data from 25 live using selenium webdriver
Generates an excel location report for each zone
Then parses the sheet to a dicitonary so it can be saved as a json

Returns: None
writes a dict to 'reports.json'
Key = roomName
Dict[key] = [book1, book2,...]

Requirements:
1. MUST UPDATE DOWNLOADS FOLDER FOR LOCAL SYSTEM BEFORE RUNNING
2. MUST INCLUDE CHROMEDRIVER.EXE IN LOCAL DIRECTORY FOR SELENIUM'S WEBDRIVER
	download: chromedriver.chromium.org/downloads
'''
def fetch():
	display = Display(visible = 0, size = (1024,768))
	display.start()
	url25live = 'https://25live.collegenet.com/cusys/'

	#1. UPFATE DOWNLOADS PATH FOR LOCAL SYSTEM
	downloadsPath = '/home/pi/Downloads/*.xlsx'
	#2. POINTS TO CHROMEDRIVER.EXE
	driver = webdriver.Firefox()

	print('Fetching locaiton reports from 25 live')
	driver.get(url25live)
	print('Waiting while application loads...')
	while True:
		try: #Try to find the button
			driver.find_element_by_xpath("//div[@id='headerText']/span[4]").click()
			break #if the button is found, break and continue to the next button
		except: #If the button doesnt exist yet (because it hasn't finished loading)
			True == True #do nothing
	print('Username')
	while True:
		try:
			driver.find_element_by_id('LoginUserName').send_keys('warec')
			break
		except:
			True == True

	print('Password')
	while True:
		try:
			driver.find_element_by_id('LoginPassword').send_keys('OITv842')
			break
		except:
			True == True

	print('Logging in...')
	while True:
		try:
			driver.find_element_by_id('LoginBtn').click()
			break
		except:
			True == True
	time.sleep(10)

	print('Reports Tab')
	while True:
		try:
			driver.find_element_by_id('s25-tabitem-reports').click()
			break
		except:
			True == True

	print('Location Reports')
	while True:
		try:
			driver.find_element_by_xpath("//div[@id='ReportsSubtabs']/ul[1]/li[3]").click()
			break
		except:
			True == True

	print('Select Dropdown')
	while True:
		try:
			driver.find_element_by_xpath("//div[@class='ReportSelect space_reports']/select[1]/option[2]").click()
			break
		except:
			True == True

	#Add Zones here
	#TODO: Simplify zones. Only dailys and all the rest. This will speed up execution as well.
	zone = ["Daily Rooms", "Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5", "Zone 6", "Zone 7", "Zone 8", "Zone 9", "Zone 10"]
	myDict = {}
	for z in zone:
		print("Select Zone: ", z) #Select zone in dropdown menu
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

		referenceFile = util.getNewestFile(downloadsPath) #newest file before new report
		print("Run Report")
		while True:
			try:
				driver.find_element_by_xpath("//*[@id='layout-tabbox-groups']/div[8]/div/div[3]/div/div[2]/table/tbody/tr[2]/td/button/div").click()
				break
			except:
				True == True

		print("Waiting while file is created...")
		newFile = util.getNewestFile(downloadsPath)
		while newFile == referenceFile: #detect when report is downloaded
			newFile = util.getNewestFile(downloadsPath)
		myDict.update(util.readReport(newFile))

	with open('reports.json', 'w') as outfile:
			json.dump(myDict,outfile)

	driver.quit() #close out to be polite to the activity manager
	display.stop()
