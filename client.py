"""
Expense Tracker - client.py

Author: Zach Chin
Last modified: May 30, 2021

Usage: 
	python3 client.py

TODO:
	o Add ability to prevent duplicate entries?
	o Add insert row at proper location rather than needing to sort all at the end
	o Error trap when no items are entered
	o Prevent negative numbers
"""

from receipt import Receipt, Item
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

DEBUG = 1					# choose whether to use test worksheet or actual worksheet
SCOPE = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
KEYFILE_NAME = "expense-tracker.json"
SPREADSHEET = "Expenses"	# specify which spreadsheet to open

class Client:
	def __init__(self):
		# use creds to create a client to interact with the Google Drive API
		self.scope = SCOPE
		self.creds = ServiceAccountCredentials.from_json_keyfile_name(KEYFILE_NAME, SCOPE)
		self.client = gspread.authorize(self.creds)

		# Find a workbook by name and open the first sheet
		print("Connecting to spreadsheet \"" + SPREADSHEET + "\"...")
		self.spreadsheet = self.client.open(SPREADSHEET)
		if DEBUG == 0:
			self.worksheet = self.spreadsheet.sheet1
		if DEBUG == 1:
			self.worksheet = self.spreadsheet.worksheet("Sheet2") # Test sheet
		print("Connected successfully to worksheet \"" + str(self.worksheet.title) + "\"!")

	def get_date(self):
		return input("Enter the date of the receipt (MM/DD/YYYY): ")

	def is_valid_date(self, date):
		# Split date string
		date_parts = date.split('/')

		# Check that there are three parts to the date string
		if len(date_parts) == 3:
			if (int(date_parts[0]) >= 1 and int(date_parts[0]) <= 12 and # Check month is valid
				int(date_parts[1]) >= 1 and int(date_parts[1]) <= 31 and # Check day is valid
				int(date_parts[2]) >= 1000):							 # Check year is valid
				return True
		
		# If tests above fail
		print("Invalid date format!")
		return False

	def get_items(self, receipt):
		print("\nEnter your item name and cost (without $ sign) separated by a double slash (//)." +\
				"\nRead the README for complete help on entering items." +\
				"\nType \"done\" to quit.")
		while True:
			item = input("  New item> ")
			quit_cmd = item.lower()
			if quit_cmd == "done" or quit_cmd == "quit" or quit_cmd == "exit":
				break	
			# Verify that there is a '//' between the item name and cost
			try:
				# Get the name and cost
				attributes = item.split('//')
				name = attributes[0].strip()
				cost = attributes[1].strip()
				owners = ["Me"]					# owners defaults to "Me"

				if len(attributes) > 2:
					owners = [owner.strip() for owner in attributes[2].strip().split(',')]
					receipt.set_type("Shared")

				# Verify that cost is a number
				try:
					receipt.add_item(Item(name, float(cost), owners))
				except ValueError:
					print("The given cost is not a number!")
			except:
				print("Put the separator \'//\' between the item name and cost!")

	def get_tax(self, receipt):
		tax = input("Enter the tax amount (press enter to continue if no tax): ")
		while True:
			# If the user presses enter, assume tax is 0
			if tax == '': 
				tax = 0.0
			# Verify that the entered tax is a floating point number
			try:
				receipt.add_item(Item('Tax', float(tax), ["Me"]))
				break
			except ValueError:
				tax = input("The given tax is not a number! Enter the tax amount: ")

	def get_notes(self, receipt):
		notes = input("Add notes (hit enter to continue): ")
		receipt.set_notes(notes)

	def add_receipt(self):
		# Get the date for the receipt and verify it is valid
		date = self.get_date()
		while not self.is_valid_date(date):
			date = self.get_date()

		# Get store name
		store = input("Enter the store name: ")

		# Create receipt
		receipt = Receipt(date, store)

		# Get items on receipt
		self.get_items(receipt)

		# Get tax
		self.get_tax(receipt)

		# Get notes
		self.get_notes(receipt)

		# Put receipt data into dataframe
		data = [date, 											# date
				store, 											# location
				'$' + str(round(receipt.get_total_cost(), 2)), 	# total cost
				receipt.get_item_list(), 						# list of items bought
				receipt.get_type(),								# type of receipt (Personal or Shared)
				receipt.get_notes()]							# notes
		
		print("Adding receipt...")

		# Append row of data to the worksheet
		self.worksheet.append_row(data, value_input_option='USER_ENTERED')
		print(receipt)
		print("Receipt added!")

	def sort(self, colname):
		# Load all worksheet data into a dataframe
		df = pd.DataFrame(self.worksheet.get_all_records())
		# test_worksheet = self.spreadsheet.add_worksheet(title="Test", rows="100", cols="5")

		# Get the dates in the dataframe as DateTime objects
		date_sr = pd.to_datetime(df['Date'])

		# Change the dates to be in YYYY/MM/DD format
		df['Date'] = date_sr.dt.strftime('%Y/%m/%d')

		# Sort the dates
		df = df.sort_values(by=['Date'], ascending=True)

		# Change the dates back to MM/DD/YYYY format
		df['Date'] = date_sr.dt.strftime('%m/%d/%Y')

		# Write the dataframe back to the worksheet
		self.worksheet.update([df.columns.values.tolist()] + df.values.tolist())

	def print_receipts(self):
		# Load all worksheet data into a dataframe
		df = pd.DataFrame(self.worksheet.get_all_records())

		# Print receipts in dataframe
		print("\nReceipts: \n")
		print(df)

	def print_connection_info(self):
		print("\nConnection information:\n" +\
				"  Spreadsheet title: " + self.spreadsheet.title + "\n" +\
				"  Worksheet title: " + self.worksheet.title + "\n")

	def run(self):
		# Display menu continuously until user quits
		while True:
			print("\n***** Expense Tracker Menu *****\n" +\
				"  1. Enter a new receipt\n" +\
				"  2. Sort receipts by date\n" +\
				"  3. Sort receipts by cost\n" +\
				"  4. Print receipts\n" +\
				"  5. Print connection information\n" +\
				"  Q. Quit the program")
			menu_choice = input("Select an option by typing the number: ")
			if menu_choice == '1':
				self.add_receipt()
			elif menu_choice == '2':
				self.sort('Date')
			elif menu_choice == '3':
				# self.sort('Total')
				print("TODO")
			elif menu_choice == '4':
				self.print_receipts()
			elif menu_choice == '5':
				self.print_connection_info()
			elif menu_choice.lower() == 'q':
				break
			else:
				print("\nInvalid option!")


# Initialize client
client = Client()
client.run()