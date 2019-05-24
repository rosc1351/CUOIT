import anvil.server

import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json

@anvil.server.callable
def say_hello(name):
  print("Hello, " + name + "!")
  app_tables.visitors.add_row(names = name)
  return 42

@anvil.server.callable
def postData(bookFile, checkFile):
	with open(bookFile, 'r') as f:
		books = json.load(f)
	with open(checkFile) as f:
		checks = json.load(f)

	print(books,checks)

	for k in books:
		c = 0
		d = 999
		if k in checks:
			c = checks[k][0]
			d = int(checks[k][1])
		print(k,c,d,books[k])
		app_tables.booking.add_row(room = k, book = books[k], check = c, day = d)

@anvil.server.callable
def get_dispData():
  return app_tables.booking.search(day = q.greater_than(30))



anvil.server.connect("XJPM266UCJKWY3D4IQELSDLD-KO4OTPRMQVUUFNTP")


anvil.server.wait_forever()